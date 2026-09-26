# German regulatory and actuarial reference library — annotated bibliography

Cross-product references for Germany life insurance liability cash flow modeling. Compiled **2026-08-29** (all access dates
2026-08-29). Citation ids **R1–R56 are frozen**: the ten delib product documents and the library's
`references/regulatory-and-actuarial-references.md` cite these tags verbatim as `[REG-R#]`; **never renumber**. Unused ids are
omitted downstream, leaving gaps, and each `sources.md` records which ids are absent and why.

This file is the citation ground truth for everything in `delib` that is not a primary product document. It carries no `S#`
sources: an insurer's *Allgemeine Versicherungsbedingungen*, its *Produktinformationsblatt*, its *Basisinformationsblatt* and
its *Tarifblatt* belong in the ten per-product research files and are cited there. What is here is the *law, the regulation, the
supervisory practice, the professional standards, the tax architecture and the market aggregates* that all ten products sit
inside.

The file is organised into five domains — prudential and supervisory (R1–R21), contract law and conduct (R22–R37), tax and the
three-layer state-subsidised pension architecture (R38–R46), biometric bases and market statistics (R47–R53), and accounting and
professional standards (R54–R56) — and closes with a **gaps and caveats register** that is a substantial part of the document's
value rather than a formality: what no search could establish, where results disagreed, which figures are vintage-sensitive, and
what is proprietary and therefore not shippable.

---

## Retrieval conditions — read this before using a single line below

This is the most important section in the file and it is unlike anything the sister libraries `uslib`, `uklib`, `jplib` and
`frlib` had to record. It has two halves, and both belong in the record. **Half one** is how this library was *built*, on
2026-08-29, under two limits that are stated here without softening. **Half two** is what the *re-verification* of 2026-08-30
established once the first of those limits was lifted. Half one is not withdrawn: it is why the entries below read as they do,
and why some of them still read as they do.

**1. No document cited anywhere in this file had been retrieved when it was written.** Direct HTTP egress from the build
environment was blocked by an organisation network policy: `WebFetch` and `curl` were refused with **HTTP 403 at the egress
gateway** for every host outside a short package-registry allowlist. The hosts that matter for German life insurance were all
tried and all refused:

| Host | What it would have served | Result |
|---|---|---|
| `gesetze-im-internet.de` | VAG, VVG, DeckRV, MindZV, RfBV, RechVersV, BerVersV, HGB, EStG, AltZertG, ZPO, SGB V/VI/XI | refused, HTTP 403 |
| `bafin.de` | Rundschreiben, Auslegungsentscheidungen, Merkblätter, Erstversicherungsstatistik, Jahresbericht | refused, HTTP 403 |
| `aktuar.de` | DAV press releases, Zinsberichte, Fachwissen fact sheets | refused, HTTP 403 |
| `gdv.de` | *Die deutsche Lebensversicherung in Zahlen*, statistics pages, Musterbedingungen | refused, HTTP 403 |
| `bundesfinanzministerium.de` | Referentenentwürfe, BMF-Schreiben, Muster-Produktinformationsblatt | refused, HTTP 403 |
| `destatis.de` | Sterbetafeln, Generationensterbetafeln, Pflegestatistik | refused, HTTP 403 |
| `dejure.org` | statute mirrors, BGBl citations, case-law cross-references | refused, HTTP 403 |
| `eur-lex.europa.eu` | Solvency II, the Delegated Regulation, PRIIPs, the IDD | refused, HTTP 403 |
| `de.wikipedia.org` | general-reference corroboration | refused, HTTP 403 |

Not one statutory text, not one BaFin circular, not one DAV table, not one BGH judgment and not one statistical release was
opened while the library was drafted. **A delib citation was then a pointer, not a certificate**: it named the instrument a
claim should be checked against without asserting that anyone had checked it — a weaker thing than an frlib citation, where
Légifrance served in full, and the difference was stated rather than glossed. **That is the statement the re-verification
changed**, and paragraph 3 below says how far.

**2. The only research channel was `WebSearch`, and its budget ran out mid-build.** The session carries a 200-call `WebSearch`
budget. `WebSearch` returns titles, URLs and a search-engine summary of the matched pages — real evidence, which does return
substantive content (several long German sentences of statutory wording reached this library that way), but a *secondary
summary*, never a retrieved document. The budget was consumed as follows and was **exhausted** before the sweep finished:

- the **prudential, supervisory and accounting** sweep ran roughly **35** German-language queries and recorded, per fact, how
  many independent publishers agreed;
- the **contract law, conduct and disclosure** sweep ran roughly **45** German-language queries on the same discipline;
- the ten **per-product** sweeps consumed most of the remainder;
- the **tax** sweep issued two queries and **both were refused** for budget — it ran **zero** successful searches;
- the **biometric bases and market statistics** sweep issued two queries and **both were refused** — it also ran **zero**
  successful searches;
- the compilation of this file issued one confirming query, which was likewise refused.

**What follows, exactly, and it applies to every entry below.**

- **Every entry records its retrieval status honestly.** As drafted the form was `Retrieved: no — direct HTTP egress blocked in
  the build environment`, followed by `; corroborated by web search` with the query and publisher counts where a sweep recorded
  them, or `; no search corroboration (session search budget exhausted)` where none exists. No entry recorded a successful
  retrieval while that network policy stood. **Every entry now carries a `Retrieved:` line of its own written on 2026-08-30**,
  and it is that line, not this paragraph, that says what was opened.
- **No verbatim quotation below is attributed to an instrument.** Where a German sentence appears in quotation marks, the
  quotation is **of a search-result summary**, not of the statute, and the entry says so. What an instrument *provides* is
  written in the compiler's own words.
- **No URL below is fabricated.** A URL appears only where (a) a search result actually returned it — the great majority of the
  URLs in R1–R37 are of this kind — or (b) it is the obvious canonical `gesetze-im-internet.de` section form
  `https://www.gesetze-im-internet.de/<slug>/__<section>.html`, whose pattern dozens of returned pages confirm, in which case it
  carries `[unverified]`. Where neither holds the entry says **not established**. No Bundesgesetzblatt citation, document
  reference number or page count is invented.
- **`[unverified]` is used generously and means what it says.** It is applied to every specific paragraph number, effective
  date, monetary amount, percentage and market figure that no search result confirmed. It is *not* applied to the general shape
  of a well-established mechanic, because that would drown the signal — but the moment a claim becomes *specific and numeric* it
  carries either a corroborated source or the tag.
- **Corroboration is graded, and the grades are not equal.** Statutory *titles and section numbers* that came back identically
  from five to ten independent publishers (`gesetze-im-internet.de`, `dejure.org`, `buzer.de`, `lxgesetze.de`, `juraforum.de`,
  `freirecht.de`, `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`, `rewis.io`, `haufe.de`) are **strongly corroborated** — those
  are mirrors of one official text but independent publishers, so agreement on a title is strong. Statutory *substance*
  summarised by one to three of them is **moderately corroborated**. A figure from a single trade-press page is
  **single-source**. A claim with no search behind it at all is **general knowledge**, and every one of those is tagged.
- **Prefer to say less, precisely, than more, loosely.** Where a figure is needed by the reference implementation and cannot be
  confirmed, the honest form downstream is a `**[std]**` parameter with a stated rationale and, where possible, an argued
  plausible range — **not** a `[REG-R#]` citation. A `[std]` number is honest; a wrong `[REG-R#]` number is not.

**The uneven evidence base as this file was drafted, stated once.** The five domains were **not** equally supported by the
search phase, and the reference library must not present them as if they were. Each entry's own `Retrieved:` line says what the
pass of 2026-08-30 then added to the domain:

| Domain | Entries | Evidence behind it at drafting |
|---|---|---|
| Prudential and supervisory | R1–R21 | ~35 German queries; statutory titles across 5–10 publishers; substance across 1–3 |
| Contract law and conduct | R22–R37 | ~45 German queries; the strongest block in the library, with several summaries reproducing statutory wording |
| Tax and the three layers | R38–R46 | **zero successful searches**; second-hand corroboration from the two sweeps above, otherwise general knowledge |
| Biometric bases and market statistics | R47–R53 | **zero successful searches**; the market aggregates are second-hand from the prudential sweep, the tables are general knowledge |
| Accounting and professional standards | R54–R56 | partial: HGB/RechVersV/BerVersV and IFRS 17 came from the prudential sweep; the DAV standards did not |

The **tax layer and the biometric layer were the least-verified parts of `delib` as drafted**, and every product document that
touches them says so in its own header. The re-verification below reached them: R38–R46 and R47–R53 were opened on 2026-08-30
like the rest, and the four entries in this file that are still `Retrieved: no` sit in those two blocks. What the pass could not
mend is the *table* problem set out in the structural warning below, which is a licensing fact and not a network one.

**3. The re-verification of 2026-08-30.** The network policy was lifted and the citations were checked against the primary
documents. Library-wide, all fifteen German instruments delib cites were read as canonical XML from `gesetze-im-internet.de`
with each law's amendment `Stand` recorded, 950 statutory section references were checked and 950 were correct, and insurer AVB,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read; **501 of the library's 805 source
entries, 62 %, now read `Retrieved: yes`.** In this file: **43 of the 56 entries read `Retrieved: yes`, four read `no` —
[R38], [R48], [R49] and [R50] — and nine are partial**, opening one limb of a multi-document entry and naming what stopped the
other. The four are of two kinds and both are stated at the entry: an act whose own *Regelungstext* was not located at any
address ([R38]), and **the DAV tables, which are the association's property and are not published at all** ([R48], [R49],
[R50]) — `aktuar.de` was browsed on 2026-08-30 and serves, but the tables are not on it. That is the one status no network
policy can change.

**What an entry now means.** A **`Retrieved: yes`** line means the document was opened and the passage the entry rests on was
read, and the line records the law's `Stand` for a statute and the edition for a publication. **Where an entry quotes German in
its `Read in the 2026-08-30 pass` bullet, that quotation is from the instrument**; where it quotes German elsewhere, the older
caveat holds and it is a quotation of a search summary. A **`Retrieved: no`** line means the entry is still **a pointer rather
than a certificate**, and is marked as one. **The re-verification changed things**: eleven of the twenty-two items in the gaps
register were closed by it, several by a retrieved document contradicting what the entry had said, and the register names each.
Treat a claim in this library as sound where its entry says `Retrieved: yes`, and as provisional where it does not.

**One structural warning that governs the whole biometric section.** The five tables at the centre of German life pricing —
**DAV 2008 T**, **DAV 2004 R**, **DAV 2004 R-Bestand**, **DAV 1997 I / RI / TI** and **DAV 2008 P** — are the property of the
Deutsche Aktuarvereinigung, are distributed to members and licensees rather than published, and are **not redistributable**.
`delib` ships **none of them**, quotes **no $q_x$ or incidence value from any of them**, and every decrement CSV in the library
is a `**[std]**` proxy anchored so that the product's own worked example reproduces exactly. That is the same posture `frlib`
took towards TH 00-02 and TGH05, and it is not a workaround: it is the only lawful and honest way to ship a public reference
library against a proprietary basis.

---

## A note on German terminology

`delib` is written in **English prose about German products**. Product names, statutory terms and document titles stay German,
italicised on first use with a gloss, and are then used untranslated. Tables and headings are in English. The following terms
carry the library and are worth fixing here once, because several of them have no English equivalent and two of them are
routinely mistranslated.

**The surplus chassis.**

- ***Überschussbeteiligung*** — the policyholder's participation in the insurer's surplus. It is **not** the French
  *participation aux bénéfices* and should never be rendered that way in a comparative sentence: the French version is a
  *collective statutory minimum* computed from a regulated account, whereas the German version is an **individual contractual
  entitlement** (§ 153 VVG, R24) with a **statutory minimum transfer to a reserve** on top (the MindZV, R18). Two instruments,
  two mechanics.
- ***Rückstellung für Beitragsrückerstattung (RfB)*** — the balance-sheet provision into which surplus earmarked for
  policyholders goes if it is not credited immediately (§ 139 Abs. 1 VAG, R9). Market writing splits it into ***gebundene*** and
  ***freie RfB***; the statutory vocabulary is ***ungebundene*** RfB (RfBV, R19) and the ***Schlussüberschussanteilfonds*** (§
  28 RechVersV, R54). `delib` defines both pairs once and then uses the market terms.
- ***Direktgutschrift*** — surplus credited to the contract immediately rather than parked in the RfB. It is **deducted** from
  the MindZV minimum (R18), which is why the MindZV is a minimum *transfer*, not a minimum *payout*.
- ***Abrechnungsverband*** — the sub-portfolio for which a declaration is made. Declared *Überschussanteilsätze* are published
  per *Abrechnungsverband* in the *Anhang* of the German statutory accounts by force of § 28 Abs. 8 RechVersV (R54).
- ***laufende Verzinsung*** — the declared annual credited rate. It is the ***Garantieverzinsung plus the laufende
  Zinsüberschussbeteiligung***, **not** a surplus rate on top of the guarantee. Adding a declared *laufende Verzinsung* to the
  guaranteed rate is the single most common arithmetic error in describing a German contract and it is a numbered pitfall in
  every affected product. ***Gesamtverzinsung*** adds the *Schlussüberschussanteil* and any *Bewertungsreserven* share.
- ***Schlussüberschussanteil*** — the terminal bonus, declared but not vested until maturity.
- ***Bewertungsreserven*** — unrealised gains on the insurer's assets. § 153 Abs. 3 VVG (R24) gives the policyholder half of the
  amount attributed to the contract on termination; § 139 Abs. 3 and 4 VAG (R9) then subtracts a ***Sicherungsbedarf*** from the
  fixed-income pool first, and the BGH has held that constitutional (R36).

**Reserving and pricing.**

- ***Deckungsrückstellung*** — the German statutory (HGB) reserve, prospective, computed on the *Rechnungsgrundlagen* of the
  premium calculation (§ 341f HGB, R54; DeckRV, R14). It is **not** the Solvency II best estimate, and the whole German picture
  depends on keeping the two apart: an insurer carries **two liability measures**, and the *Überschussbeteiligung*, the
  *Zinszusatzreserve* and the *Bewertungsreserven* test all run on the **HGB** side.
- ***Deckungskapital*** — the contract-level reserve, the base measure of the *Rückkaufswert* under § 169 VVG (R28).
- ***Höchstzinssatz*** — the maximum rate at which the *Deckungsrückstellung* may be discounted, **the statute's own term** and
  the heading of § 2 DeckRV, fixed at 1 Prozent by § 2 Abs. 1 Satz 1 (R14). ***Höchstrechnungszins*** is the same rate under the name
  BaFin, the BMF and the DAV use, and delib writes *Höchstzinssatz* when citing § 2 and *Höchstrechnungszins* when reporting the
  market (R15). Neither is the *Garantiezins*: § 2 caps the **reserving** rate and the guaranteed rate a policy carries is a tariff
  decision that may be lower — a distinction the DAV states in terms (R56).
- ***Rechnungszins*** — the rate a particular tariff actually uses, at or below the cap; it stays with the contract for its
  whole term, which is why a German in-force book is a stack of cohorts (R15).
- ***Zillmerung*** — offsetting a contract's one-off acquisition costs against its first premiums, the *Zillmersatz* capped by
  § 4 Abs. 1 Satz 2 DeckRV at **25 Promille der Summe aller Prämien** — the *Beitragssumme* of market language (R16).
- ***Zinszusatzreserve (ZZR)*** — the additional HGB reserve that arises when the § 5 Abs. 3 DeckRV *Referenzzins* falls below a
  contract's tariff rate (R17). It exists in no other jurisdiction in this repository.
- ***Rechnungsgrundlagen erster / zweiter Ordnung*** — first-order (prudent, pricing and reserving) and second-order
  (best-estimate) bases. The wedge between them is the ***Sicherheitszuschlag***, and its systematic release is the
  *Risikoüberschuss* (R47). This distinction is the German name for the three-way assumption split every delib
  `technical-notes.md` uses.

**Contract mechanics.**

- ***Rückkaufswert*** — the surrender value (§ 169 VVG, R28), floored at the *Deckungskapital* that results from spreading the
  charged acquisition and distribution costs evenly over the **first five contract years**.
- ***Stornoabzug*** — the surrender deduction, permitted only if *vereinbart, beziffert und angemessen* (§ 169 Abs. 5 VVG, R28).
- ***Beitragsfreistellung*** / ***prämienfreie Versicherung*** — conversion to a paid-up policy (§ 165 VVG, R28). In Germany
  this is a **distinct decrement from surrender**, not a variant of it, and a model that implements only surrender has modelled
  the wrong book.
- ***Bruttobeitrag*** and ***Zahlbeitrag*** — the tariff premium and the premium actually collected after surplus is applied as
  a *Beitragsverrechnung*. The gap is large and persistent in *Berufsunfähigkeit* (R53) and the *Zahlbeitrag* is **not
  guaranteed**.
- ***Rentenfaktor*** — euros of monthly annuity per €10,000 of accumulated capital; the number that converts a unit-linked or
  index account value into an annuity. The BGH struck down asymmetric unilateral reduction clauses in 2025 (R36).
- ***Beitragsgarantie*** — a guarantee that at least the contributions paid are available at the start of the payout phase;
  statutory for a certified Riester contract (R43).
- ***Berufsunfähigkeit*** — inability to pursue **the last occupation as it was structured before the impairment** (§ 172 Abs. 2
  VVG, R29). It is *not* "disability" in the general-labour-market sense; the statutory scheme's *Erwerbsminderung* is that, and
  the two use different definitions of the same event (R53).
- ***Pflegegrad*** — one of the five care levels of § 15 SGB XI, which replaced the three ***Pflegestufen*** on 1 January 2017
  (R51). The replacement is a **definitional break**, not a change in the underlying risk, and the BGH has refused to map the
  two scales (R36).

**Institutional vocabulary.**

- ***Altbestand*** / ***Neubestand*** — contracts concluded before / from **29 July 1994**, the deregulation date (R11). All ten
  delib products are **Neubestand** business and every product document says so.
- ***Verantwortlicher Aktuar*** — the statutory responsible actuary of § 141 VAG (R11), who makes the written proposal on the
  *Überschussbeteiligung*. Distinct from the Solvency II ***versicherungsmathematische Funktion*** of the MaGo (R21); `delib`
  does not conflate them.
- ***Sicherungsvermögen*** — the ring-fenced asset pool (§ 125 VAG, R7); ***Anlagestock*** is the segregated section of it that
  backs unit-linked benefits.
- ***Sicherungsfonds*** — the statutory guarantee scheme (§§ 221 ff. VAG), whose tasks are carried by **Protektor
  Lebensversicherungs-AG** (R12).
- ***Drei-Schichten-Modell*** — the three-layer sorting of retirement products introduced by the *Alterseinkünftegesetz* with
  effect from 1 January 2005 (R38). Schicht 1 is the *Basisversorgung* including the ***Basisrente*** (Rürup); Schicht 2 the
  subsidised supplementary layer including the ***Riester-Rente***; Schicht 3 everything unsubsidised.

---

## The German regulatory architecture in one page

**Who supervises what.** German insurance supervision is exercised by the **Bundesanstalt für Finanzdienstleistungsaufsicht
(BaFin)**, created in **2002** by the *Finanzdienstleistungs- aufsichtsgesetz* of **22 May 2002** out of the three predecessor
authorities for banking, securities and insurance; the merger was organisational and did not create new competences [R21]. BaFin
is subject to the *Rechts- und Fachaufsicht* of the **Bundesministerium der Finanzen**, and supervises under the KWG, the
**VAG** and the WpHG. Its stated main objective in insurance is to *ensure the permanent fulfilment capability of insurance
contracts* — the ***dauernde Erfüllbarkeit*** standard, which reappears verbatim in § 138 Abs. 1 VAG on premium adequacy [R8]
and in § 341e HGB on technical provisions [R54] — together with the protection of the insured and beneficiaries [R21]. German
usage splits the function into *Finanzaufsicht* (solvency), *Rechtsaufsicht* (proper conduct of business) and
*Missstandsaufsicht*.

There is **no second national insurance supervisor**. Unlike France, where the ACPR and the AMF share competence over
unit-linked distribution, and unlike the United Kingdom's twin peaks, Germany runs conduct and prudential supervision inside one
authority. The consequences are visible in this file: the same body issues the *Auslegungsentscheidungen* that govern how the
MindZV minimum allocation works in unit-linked business [R21] and the *Merkblatt* that tells insurers their savings products
must deliver an *angemessener Kundennutzen* [R35]. Above BaFin sits **EIOPA**, whose published risk-free curves are made binding
on German undertakings by § 83 VAG [R6][R4].

**Why a German life model reads VAG and VVG and DeckRV and MindZV together.** This is the single most important structural fact
about the German market, and it has no counterpart in the sister libraries. France puts prudential rules and contract law in
**one** code — the *Code des assurances*, Livre III and Livre I. Germany splits them across **two statutes with different
addressees**, and then delegates the arithmetic to **two regulations**:

- The **VAG** (*Versicherungsaufsichtsgesetz* 2016) is **supervisory law**. It binds the undertaking to the supervisor. It says
  how the balance sheet is valued (§§ 74–88), how much capital is required (§§ 96–110), how the assets must be invested (§§
  124–125), that premiums must be *auf der Grundlage angemessener versicherungsmathematischer Annahmen* and adequate to fund the
  *Deckungsrückstellung* (§ 138), that surplus earmarked for policyholders goes into the RfB (§ 139) and may be used only for
  them (§ 140), and that a named *Verantwortlicher Aktuar* proposes the declaration (§ 141). It gives the policyholder no claim.
- The **VVG** (*Versicherungsvertragsgesetz* 2008) is **contract law**. It binds the insurer to the policyholder. Its Kapitel 5
  (§§ 150–171) supplies the entitlement to *Überschussbeteiligung* (§ 153), the right to convert to paid-up (§ 165), the right
  to surrender and the surrender-value floor (§§ 168–169) and the withdrawal right (§ 152); and § 171 makes almost all of them
  ***halbzwingend*** — variable in the policyholder's favour only. Kapitel 6 (§§ 172–177) does the same for *Berufsunfähigkeit*.
- The **DeckRV** (*Deckungsrückstellungsverordnung*, 18 April 2016) is made under **§ 88 Abs. 3 VAG** and fixes the
  *Rechnungsgrundlagen* of the statutory *Deckungsrückstellung*: the *Höchstrechnungszins* (§ 2), the *Höchstzillmersatz* (§ 4)
  and the *Referenzzins* that generates the *Zinszusatzreserve* (§ 5 Abs. 3).
- The **MindZV** (*Mindestzuführungsverordnung*, 18 April 2016) is made under **§ 145 VAG** and turns § 139's "put it in the
  RfB" and § 140's "use it only for policyholders" into an arithmetic floor: at least **90 %** of the investment result net of
  the *Rechnungszinsen*, **90 %** of the risk result and **50 %** of the remaining result, less the *Direktgutschrift*, computed
  separately for *Alt-* and *Neubestand*, and floored at zero.

**What each contributes to a cash flow model.** Read alone, none of the four gives a modeller a projection. Read together they
do, and each supplies a different kind of quantity:

| Instrument | Kind of rule | What the model gets from it |
|---|---|---|
| **VVG** [R22–R31] | contractual, one-way mandatory | the *benefits and options that must exist*: the surrender-value floor, the paid-up right, the profit-participation entitlement, the suicide window, the BU definition and the *Nachprüfung* notice period |
| **DeckRV** [R14–R17] | reserving arithmetic | the *ceilings that shape the tariff*: the discount rate a guarantee may be priced at, the acquisition cost that may be zillmered, the reserve that low rates force |
| **VAG** [R5–R13] | supervisory | the *constraints on the insurer's discretion*: adequacy of premiums, equal treatment, the RfB ring fence, the actuary's proposal, the *Bewertungsreserven* test |
| **MindZV / RfBV** [R18][R19] | distribution arithmetic | the *floor under the discretionary declaration*, expressed on the three result sources a German P&L is decomposed into |

The join is tighter than a list suggests, and three joins in particular are where a delib model lives:

1. **§ 138 VAG → § 2 DeckRV → the guarantee.** Premiums must be adequate to form adequate *Deckungsrückstellungen*; the DeckRV
   caps the rate at which those may be discounted; therefore the *Höchstrechnungszins* caps what a new tariff may guarantee. The
   rate has been **1.00 % since 1 January 2025** [R15], the first increase in about thirty years, and it stays with a contract
   for its whole term — which is why a German book is a stack of cohorts at 4.00 %, 3.25 %, 2.75 %, 2.25 %, 1.75 %, 1.25 %, 0.90
   %, 0.25 % and now 1.00 % [R15].
2. **§ 153 Abs. 3 VVG → § 139 Abs. 3/4 VAG → MindZV §§ 11–12.** The contract entitles the policyholder to *half* the
   *Bewertungsreserven* attributed to it; the VAG then removes from the fixed-income pool any *Sicherungsbedarf* arising from
   contracts with interest guarantees; the MindZV defines the reference rate — a **single month-end ten-year zero-coupon Euro
   swap rate** — and the fifteen-year look-forward against which a contract's highest applicable *Rechnungszins* is tested. In
   the low-rate decade that chain reduced the payable half to **zero** for many portfolios, and the BGH held the rule
   constitutional in 2018 [R36].
3. **§ 4 DeckRV ∥ § 169 Abs. 3 VVG.** The DeckRV governs what the insurer may **reserve** for acquisition costs (25 ‰ of the
   *Summe aller Prämien*, the statute's own phrase); § 169 governs what it must **pay** on surrender (the value on a five-year even spread of the charged
   costs). They are independent constraints and the tighter one binds. A model that applies only one of them has an early-
   duration surrender curve that is wrong in a way a German reviewer will see immediately.

**What sits outside the four.** The **statutory accounts** are HGB §§ 341–341o plus the **RechVersV**, whose *Formblatt 1*
replaces § 266 HGB for the balance sheet and whose § 28 Abs. 8 forces the RfB development, the *Schlussüberschussanteilfonds*
and the declared *Überschussanteile* per *Abrechnungsverband* into the published *Anhang* [R54] — which is the practical reason
a delib product document can cite a named insurer's declaration at all. The **BerVersV** carries the national supervisory
returns, including the *Zerlegung des Rohergebnisses nach Ergebnisquellen* on forms F.213.01 to F.219.01, which is the three-way
split the MindZV minima operate on [R54]. The **Solvency II layer** — Directive 2009/138/EG, Delegated Regulation (EU) 2015/35,
the 2025 review and the EIOPA curves [R1–R4] — reaches German life business through the VAG rather than directly, which is why
delib cites VAG sections throughout and directive articles only where the European layer is itself the point. The **guarantee**
is bounded at the bottom by the *Sicherungsfonds* and § 314 VAG [R12]: a supervisory power to cut guaranteed benefits by up to 5
% where the fund steps in, and an uncapped, asset-position-driven reduction where it does not. **No delib document describes a
German guarantee as unconditional.**

**And what delib does not model.** All ten models publish gross, undiscounted, best-estimate-style liability cash flows. The
Solvency II balance sheet, the SCR and MCR, the risk margin, the *Deckungsrückstellung*, the *Zinszusatzreserve*, the RfB stock
as a balance-sheet item and the IFRS 17 measurement are **cited, never specified**. Where a document needs a discount rate, an
asset return or a declared rate to make a worked example run, that number is `**[std]**` with a rationale, not a citation.

---

## Product key and product-relevance matrix

**Product key**, used in the `Products` line of every entry and as the matrix columns:

`KLV` kapitallebensversicherung · `RV` klassische_rentenversicherung · `FRV` fondsgebundene_rentenversicherung · `IDX`
indexpolice · `BAS` basisrente · `RIE` riester_rente · `SOF` sofortrente · `RLV` risikolebensversicherung · `BU`
berufsunfaehigkeit · `PFL` pflegerentenversicherung.

`x` = load-bearing for that product's specification, technical notes or model; `(x)` = qualified, conditional or background
relevance — the entry governs the product but does not shape its cash flows, or reaches it only through an option or a rider;
blank = not relevant.

| R# | Reference (short name) | KLV | RV | FRV | IDX | BAS | RIE | SOF | RLV | BU | PFL |
|----|------------------------|-----|----|-----|-----|-----|-----|-----|-----|----|-----|
| R1 | Richtlinie 2009/138/EG — Solvabilität II | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R2 | Delegierte Verordnung (EU) 2015/35 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R3 | Richtlinie (EU) 2025/2 — the Solvency II review | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R4 | EIOPA — RFR term structures, UFR, Volatilitätsanpassung | (x) | (x) | | (x) | (x) | (x) | (x) | | (x) | (x) |
| R5 | VAG 2016 and Anlage 1 — the Sparten | x | x | x | x | x | x | x | x | x | x |
| R6 | VAG §§ 74–110 and § 40 — balance sheet, SCR/MCR, SFCR | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R7 | VAG §§ 124–125 — Anlagegrundsätze, Anlagestock | x | x | x | x | x | x | x | (x) | (x) | (x) |
| R8 | VAG § 138 — Prämienkalkulation; Gleichbehandlung | x | x | (x) | x | x | x | x | x | x | x |
| R9 | VAG § 139 — Überschussbeteiligung; Sicherungsbedarf | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R10 | VAG §§ 140 and 145 — the RfB and its Verordnungen | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R11 | VAG §§ 141–143; Altbestand/Neubestand 1994 | x | x | x | x | x | x | x | x | x | x |
| R12 | VAG §§ 221–236 and § 314; Protektor | x | x | x | x | x | x | x | x | x | x |
| R13 | VAG §§ 351–353 — Übergangsmaßnahmen | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R14 | DeckRV and § 2 — the Höchstzinssatz provision | x | x | (x) | x | x | x | x | x | x | x |
| R15 | Höchstzinssatz rate history; Sechste VO 19.07.2024 | x | x | (x) | x | x | x | x | x | x | x |
| R16 | DeckRV § 4 — Höchstzillmersätze | x | x | x | x | x | x | | x | x | x |
| R17 | DeckRV § 5 Abs. 3 — Referenzzins, ZZR, Korridor | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R18 | MindZV — the 90/90/50 minima and §§ 11–13 | x | x | (x) | x | x | x | x | x | x | x |
| R19 | RfBV — the collective part of the RfB | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R20 | LVRG 2014 | x | x | (x) | x | x | x | (x) | x | x | x |
| R21 | BaFin — FinDAG, MaGo, Auslegungsentscheidungen | (x) | (x) | x | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R22 | VVG 2008 — the statute, Kapitel 5, § 171 | x | x | x | x | x | x | x | x | x | x |
| R23 | VVG §§ 8 and 152 — Widerruf | x | x | x | x | x | x | x | x | x | x |
| R24 | VVG § 153 — Überschussbeteiligung, Bewertungsreserven | x | x | x | x | x | x | x | (x) | (x) | (x) |
| R25 | VVG §§ 154–155 — Modellrechnung, Standmitteilung | x | x | (x) | x | x | x | (x) | | (x) | (x) |
| R26 | VVG §§ 150, 159–162 — consent, beneficiary, suicide | x | (x) | (x) | (x) | (x) | (x) | (x) | x | (x) | (x) |
| R27 | VVG § 163 — Prämien- und Leistungsänderung | (x) | (x) | | | | | | (x) | x | x |
| R28 | VVG §§ 165–170 — paid-up, surrender, Rückkaufswert | x | x | x | x | (x) | x | (x) | (x) | x | x |
| R29 | VVG §§ 172–177 — Berufsunfähigkeitsversicherung | (x) | (x) | | | (x) | | | (x) | x | (x) |
| R30 | VVG §§ 19, 21, 37, 38, 157, 158 | x | x | (x) | (x) | (x) | (x) | (x) | x | x | x |
| R31 | VVG §§ 6, 7, 1a, 7b, 7c, 214 and the VVG-InfoV | x | x | x | x | x | x | x | x | x | x |
| R32 | PRIIPs — VO (EU) 1286/2014 and the RTS | (x) | (x) | x | x | (x) | (x) | (x) | | | |
| R33 | IDD — RL (EU) 2016/97, transposition, § 34d GewO | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R34 | Unisex — EuGH C-236/09 and the AGG | x | x | x | x | x | x | x | x | x | x |
| R35 | BaFin Merkblatt 01/2023 — Wohlverhaltensaufsicht | x | x | x | x | (x) | (x) | (x) | | | |
| R36 | The BGH line of authority | x | x | x | x | (x) | x | (x) | (x) | (x) | x |
| R37 | GDV-Musterbedingungen; BU market practice | x | x | (x) | (x) | (x) | (x) | (x) | x | x | (x) |
| R38 | AltEinkG and the Drei-Schichten-Modell | x | x | x | x | x | x | x | (x) | (x) | (x) |
| R39 | EStG § 10 Abs. 1 Nr. 2 b and Abs. 3 — Basisrente | | | | | x | (x) | | (x) | (x) | |
| R40 | ZPO §§ 850b, 851c and 851d — Pfändungsschutz | (x) | (x) | (x) | | x | (x) | | | x | (x) |
| R41 | EStG § 22 Nr. 1 S. 3 a and § 55 EStDV | (x) | x | x | x | x | (x) | x | | x | (x) |
| R42 | EStG § 10a and §§ 79–99 — the Riester machinery | | | (x) | | (x) | x | | | | |
| R43 | AltZertG, BZSt, AltvPIBV and the PIA | | (x) | (x) | (x) | x | x | | | | |
| R44 | Altersvorsorge-Reformgesetz 2026; Altersvorsorgedepot | | (x) | (x) | | (x) | x | | | | |
| R45 | EStG § 20 Abs. 1 Nr. 6 — 12/62, Mindesttodesfallschutz | x | x | x | x | | (x) | (x) | (x) | | |
| R46 | ErbStG and SGB V §§ 226, 229, 240 | x | (x) | (x) | (x) | (x) | x | (x) | x | (x) | (x) |
| R47 | Rechnungsgrundlagen 1./2. Ordnung; the DAV tables | x | x | x | x | x | x | x | x | x | x |
| R48 | DAV 2008 T and its predecessors | x | (x) | (x) | (x) | (x) | (x) | | x | (x) | (x) |
| R49 | DAV 2004 R and DAV 2004 R-Bestand | (x) | x | x | x | x | x | x | | | (x) |
| R50 | DAV 1997 I / RI / TI | (x) | | | | | | | (x) | x | (x) |
| R51 | DAV 2008 P, § 15 SGB XI and the Pflegegrad break | (x) | (x) | | | | | | | (x) | x |
| R52 | Destatis — Perioden- und Kohortensterbetafeln, Pflege | x | x | x | x | x | x | x | x | x | x |
| R53 | The German life market in numbers | x | x | x | x | x | x | x | x | x | x |
| R54 | HGB §§ 341–341o, RechVersV, BerVersV | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R55 | IFRS 17 and the Variable Fee Approach | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R56 | DAV Fachgrundsätze and the Höchstrechnungszins recommendation | x | x | x | x | x | x | x | x | x | x |

**One row is deliberately absent from the matrix and is recorded here instead.** BaFin *Rundschreiben 11/2017 (VA)*, the
*Kapitalanlagerundschreiben*, and the **Anlageverordnung (AnlV)** it interprets apply to **small insurers under §§ 212–217 VAG
and to domestic Pensionskassen and Pensionsfonds** — **not** to the Solvency II life insurers that write the ten delib products,
which are governed by the qualitative § 124 VAG prudent person principle [R7]. German market writing routinely cites AnlV quotas
as if they bound all insurers; since 1 January 2016 they do not bind the large life insurers at all. The circular is discussed
inside R7 so that no delib author misapplies an AnlV quota, and it carries no id of its own.

---

## 1. Prudential — the European layer

The Solvency II layer reaches German life business **through the VAG**, not directly. That is why delib cites VAG sections
throughout and directive articles only where the European layer is itself the point. **No Solvency II article number in this
library was read from the instrument while it was drafted**: `eur-lex.europa.eu` was refused at the egress gateway, and the
article numbers below came from secondary summaries. The pass of 2026-08-30 reached EUR-Lex, and each entry's own `Retrieved:`
line says which of these articles was read there and which was not.

### R1. Richtlinie 2009/138/EG — Solvabilität II
- Publisher: European Parliament and Council (EUR-Lex); German mirrors at `lexparency.de` and `kpmg-lexlinks.de`
- Doc type: Level 1 directive (consolidated text)
- URL: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32009L0138 (returned by search); consolidated PDF
  https://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:02009L0138-20190113 (returned);
  https://lexparency.de/eu/32009L0138/ (returned)
- Retrieved: **yes** — the consolidated German text at
  https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=CELEX:02009L0138-20250117 (2.28 MB, current consolidated version
  17/01/2025), read **2026-08-30**. Artt. 37, 76, 77, 77a–77e and 101 were read in full. **Note the retrieval mechanic:** the
  `legal-content/.../TXT/?uri=CELEX:32009L0138` landing page serves only the recitals, and the `TXT/PDF/` form truncates at the
  sweep's byte cap; the ELI form `eur-lex.europa.eu/eli/<type>/<year>/<n>/oj/deu/pdfa1b` delivers the complete Official Journal text.
- Content: the directive Germany transposes into the VAG. The substance established from the summaries: **the value of technical
  provisions equals the sum of a best estimate and a risk margin, calculated separately**; the relevant risk-free yield curve
  for the best estimate is that of **Article 77(2)** — a reference independently confirmed by BaFin's own interpretive decision
  on capital-market models [R21] — and the **risk margin of Article 77(5)** is calculated excluding any capital add-on.
  **Article 76** appeared in the search results in the role of the article cited for the best-estimate-plus-risk-margin rule —
  **which the 2026-08-30 retrieval shows to be wrong: that rule is Article 77(1), and Article 76 is *Allgemeine Bestimmungen*.**
  For a delib model the operative point is the boundary: all ten models publish gross, undiscounted liability cash flows
  and stop short of the measurement this directive prescribes.
- Not established: **no article number here was read from the instrument itself** and all are therefore `[unverified]`. The
  three-pillar structure, the **99.5 % one-year VaR** confidence level and the directive's adoption date are commonly reported
  but were **not returned by any search in this sweep** and are `[unverified]`. One secondary source states that Solvency II
  stress scenarios are calibrated to a **0.5 % probability of occurrence**, which is consistent with the 99.5 % VaR but is a
  secondary restatement, not the directive.
- Read in the 2026-08-30 pass — **one correction and three resolutions.** **Correction:** the
  best-estimate-plus-risk-margin rule is **Article 77(1)** (*"Der Wert der versicherungstechnischen Rückstellungen hat der Summe aus
  einem „besten Schätzwert“ und einer Risikomarge ... zu entsprechen"*), **not Article 76**, which is *Allgemeine Bestimmungen* and
  states the transfer-value and market-consistency principles; the separate-calculation rule is Article 77(4). **Resolved:** the
  directive is *"vom 25. November 2009"*, ABl. L 335 vom 17.12.2009, S. 1–155; **Article 101(3)** fixes the SCR at *"dem Value-at-Risk
  der Basiseigenmittel ... zu einem Konfidenzniveau von 99,5 % über den Zeitraum eines Jahres"*; and **Article 37(5)** confirms that a
  *Kapitalaufschlag* is excluded from the Article 77(5) risk margin. Article 77(2) as the risk-free-curve reference is confirmed.
  Articles 77a–77e are the extrapolation, matching adjustment, its calculation, the volatility adjustment and EIOPA's technical
  information — the articles VAG §§ 80–83 transpose one for one [R6].
- Products: all ten (cited-not-specified).

### R2. Delegierte Verordnung (EU) 2015/35
- Publisher: European Commission (EUR-Lex); mirrors at `lexparency.de`, `gesetze.legal`, `umwelt-online.de`
- Doc type: Level 2 delegated regulation, directly applicable
- URL: https://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:32015R0035&from=DE (returned);
  https://lexparency.de/eu/32015R0035/ (returned); https://gesetze.legal/eu/vo_eu_2015_35 (returned)
- Retrieved: **yes** — the complete Official Journal text at
  https://eur-lex.europa.eu/eli/reg_del/2015/35/oj/deu/pdfa1b (PDF, 797 pp., ABl. L 12 vom 17.1.2015), read **2026-08-30**;
  Artt. 37, 38 and 39 read in full. **The URL this entry previously led with,
  `legal-content/DE/TXT/PDF/?uri=CELEX:32015R0035&from=DE`, answers 200 but truncates at 3 MB and the truncated PDF does not open —
  it is not a retrieval.** `lexparency.de` refused with a connection reset; `gesetze.legal/eu/vo_eu_2015_35` serves and its
  per-article pages (`/vo_eu_2015_35/39`) were used as a cross-check.
- Content: where the operative Solvency II detail lives, which is why a German modeller looking for contract boundaries, expense
  rules or standard-formula stresses reads this rather than the VAG. Established from summaries: **Art. 37** governs the
  calculation of the risk margin, which rests on the assumption that the **entire portfolio of obligations is transferred to
  another undertaking**; **Art. 38** defines that hypothetical *Referenzunternehmen*; **Art. 39** sets the *Kapitalkostensatz*.
  The instrument's own title carries its adoption date of **10 October 2014**.
- Not established **as at the original build; the first point is resolved by the 2026-08-30 pass below.** The 6 % cost-of-capital
  rate was not confirmed from any text at build time — the only support was the 2025 review's "reduced from 6 to 4.75 per cent"
  wording [R3] — and it **is now read from Art. 39 of the regulation itself**. **Still not established: Art. 18 (Vertragsgrenzen / contract boundaries)
  returned nothing** and its content is entirely `[unverified]`. The **life underwriting sub-modules (Art. 136 ff.)** —
  mortality, longevity, disability, lapse, mass lapse, expense, revision and catastrophe — and their calibrations, **including
  the 40 % mass-lapse shock**, were **not established**; the query that would have addressed them was cut by the exhausted
  budget. Only the *names* of the sub-modules are corroborated, from a secondary source listing longevity, disability, lapse and
  expenses as the material SCR drivers for German business. The publication date of **17 January 2015** was not returned in this
  sweep. Consequence for delib: **no cost-of-capital rate, no contract-boundary rule and no lapse or expense stress in this
  library rests on a retrieved text**, and any such figure in a product document is `**[std]**` or `[unverified]`.
- Read in the 2026-08-30 pass — **the 6 % is settled from the instrument.** Art. 39 in full:
  *"Es wird davon ausgegangen, dass der in Artikel 77 Absatz 5 der Richtlinie 2009/138/EG genannte Kapitalkostensatz 6 % beträgt."*
  Art. 37(1) gives the risk-margin formula $RM = CoC\cdot\sum_{t\ge0} SCR(t)/(1+r(t+1))^{t+1}$ with $SCR(t)$ the reference
  undertaking's SCR after $t$ years and $r(t+1)$ the basic risk-free rate, chosen in the reporting currency, and Art. 37(3) requires
  allocation to the Article 80 lines of business; Art. 38(1) sets the transfer assumption and provides that the reference undertaking
  *"hat vor der Übertragung weder Versicherungs- oder Rückversicherungsverpflichtungen noch Eigenmittel"*. The publication date
  **17 January 2015** is confirmed from the OJ page headers. **Art. 18 (Vertragsgrenzen) and the life underwriting sub-modules
  (Art. 136 ff.), including the mass-lapse shock, were still not read** — the document was opened but those articles were not, and
  they remain `[unverified]`.
- Products: all ten (cited-not-specified).

### R3. Richtlinie (EU) 2025/2 — the Solvency II review
- Publisher: European Parliament and Council, Official Journal; secondary analysis from BDO, KPMG, Deloitte, PwC, Meyerthole
  Siems Kohlruss and the AVÖ
- Doc type: amending directive
- URL:
  https://www.bdo.de/de-de/insights/weitere-veroffentlichungen/versicherungen/solvency-ii-reform-ab-2027-entlastung-durch-proportionalitaet
  (returned);
  https://klardenker.kpmg.de/financialservices-hub/regulatory-update/ueberarbeitete-solvency-ii-richtlinie-im-eu-amtsblatt-veroeffentlicht/
  (returned); https://aktuare.de/de/presse/pressemitteilungen/2682-pm-risikomarge-solvencyii.html (returned)
- Retrieved: **partly.** The **MSK commentary** at
  https://aktuare.de/de/presse/pressemitteilungen/2682-pm-risikomarge-solvencyii.html was read (HTML, 25 kB, **2026-08-30**);
  `bdo.de` refused with HTTP 403; the KPMG *klardenker* page serves. **The amending directive itself was not opened** — no attempt was
  made on `eur-lex.europa.eu/eli/dir/2025/2/oj/deu/pdfa1b` in this pass — so every date and number below is a consultancy's report of
  the instrument, not the instrument.
- Content: the amending directive from the 2019–2021 review, **dated 27 November 2024** and **published in the Official Journal
  on 8 January 2025**. **The new rules apply for the first time on 30 January 2027**, two years after entry into force, and
  Member States must transpose within those two years — so German transposition into the VAG is due before that date. What
  changes and matters to a liability model: the **Kapitalkostensatz underlying the risk margin falls from 6 % to 4.75 %**, with
  the next review of the rate at the earliest five years after entry into force; and an **exponential, time-dependent lambda
  factor** is to be introduced through the Level 2 regulation, reducing the level and the volatility of the risk margin for
  long-term business, with **no lower bound** and an effect on **projected years ≥ 28**. The net effect is a risk-margin
  reduction most beneficial to insurers with long-term business — which is exactly the German life book. Otherwise the reform
  combines targeted proportionality relief for small and non-complex undertakings with tightened qualitative requirements on
  governance, risk management, sustainability and crisis prevention.
- Not established: **a wording conflict across the summaries.** One states "das Inkrafttreten ist für den 30. Januar 2027
  vorgesehen"; another states the rules apply "zwei Jahre nach ihrem Inkrafttreten am 30. Januar 2027"; a third gives
  publication on 8 January 2025 and application from 30 January 2027. The consistent reading is entry into force twenty days
  after publication and first application 30 January 2027, but **the entry-into-force date itself was never stated by any search
  result** and is `[unverified]`. Only the **30 January 2027 first application** is safe to assert. The lambda formula, the
  proportionality thresholds and the macroprudential tools were not established.
- Products: all ten, forward-looking only. **No delib model implements a 2027 basis and none should be read as doing so.**

### R4. EIOPA — risk-free interest rate term structures, the UFR and the Volatilitätsanpassung
- Publisher: European Insurance and Occupational Pensions Authority; republished on `data.europa.eu`; secondary commentary from
  PwC, KPMG and addactis
- Doc type: data hub, technical documentation and news releases
- URL: https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en (returned);
  https://www.eiopa.europa.eu/eiopa-publishes-ultimate-forward-rate-ufr-2026-2025-03-31_en (returned);
  https://www.eiopa.europa.eu/eiopa-updates-reference-portfolios-used-calculate-volatility-adjustment-solvency-ii-risk-free-rate-2025-12-09_en
  (returned); the *Report on the Calculation of the UFR for 2026*, **EIOPA-BoS-25-114**, at
  https://www.eiopa.europa.eu/document/download/16f852f9-919d-49fe-a691-b9eb9e3285bd_en?filename=EIOPA-BoS-25-114-Report+on+the+Calculation+of+the+UFR+for+2026.pdf
  (returned)
- Retrieved: **yes** — EIOPA's landing page (HTML, 258 kB), the **UFR 2026 release of 31 March 2025** (HTML, 90 kB) and the
  **reference-portfolio update of 9 December 2025** (HTML, 93 kB), read **2026-08-30**. The monthly technical-information packages
  and the RFR Technical Documentation PDF were located on the page but **not opened**, so no curve point and no VA value was
  extracted.
- Content: EIOPA **publishes the relevant risk-free interest-rate term structures monthly**, and **§ 83 VAG makes their use
  binding on German undertakings** [R6] — which is the hook by which a European technical publication becomes German law.
  Established specifics: updated technical documentation published **24 September 2024**, taking effect **1 January 2025**, with
  the first calculation on that basis at the **end of January 2025**; the **UFR for the euro is 3.30 %, applicable from 1
  January 2026, unchanged from 2025**; the published packages carry the risk-free rates, the **volatility adjustment**, the
  matching-adjustment fundamental spreads and the UFR; and the **reference portfolios behind the volatility adjustment were
  updated on 9 December 2025**. A secondary commentary — not EIOPA — describes the curve as interpolated below a **Last Liquid
  Point of 20 years** and then extrapolated to the UFR over a **60-year horizon by the Smith–Wilson method**.
- Not established: **no German volatility-adjustment value, for any date, was established** — the query was cut by the exhausted
  budget; the one Germany-specific number any search returned was a **fundamental spread of 0 basis points on the German
  government bond in May 2016**, from a secondary summary, which is a different quantity and nearly a decade stale. **No numeric
  curve point was extracted.** The Smith–Wilson / LLP-20 / 60-year description rests on **one secondary source** and is
  `[unverified]` against EIOPA's own documentation. For delib: **no curve value is used in any model**; the models publish
  undiscounted cash flows and a reader wanting a market-consistent valuation applies a curve from this source. Any discount rate
  in a delib document is `**[std]**`.
- Read in the 2026-08-30 pass. *"Publication is done on a monthly basis"*, confirming the monthly cadence.
  The UFR release states: *"The UFR does not change for any of the relevant currencies compared to this year. This means an applicable
  UFR of 3.30% as of 1 January 2026 for the euro."* The VA update of 9 December 2025 says EIOPA *"will begin using these updated
  representative portfolios for the end-March 2026 VA calculation"*, published at the beginning of April 2026, with annual revisions
  under Article 11.1.3 of the RFR Technical Documentation. **Correction:** the technical documentation is **not** the 24 September
  2024 edition — the page lists 10 December 2024, 23 June 2025, 16 October 2025, 9 December 2025 and, most recently,
  **26 May 2026 (Solvency II Review)**.
- Products: all ten (discounting, cited-not-specified); most materially the long-duration guaranteed books — RV, SOF, BAS, RIE,
  KLV, IDX, PFL.

---

## 2. Prudential — the Versicherungsaufsichtsgesetz

The VAG 2016 is the German transposition of Solvency II and the single statute a German life model is held to. Its architecture
matters for citation: **Teil 1** carries the general prudential rules (valuation, technical provisions, own funds, SCR, MCR,
investments, the public solvency report); **Teil 2 Kapitel 3 Abschnitt 1** the *besondere Vorschriften* for life insurance (§§
138–145); **Teil 3** the *Sicherungsfonds* (§§ 221 ff.); **Teil 4** the supervisory powers including § 314; **Teil 8** the
transitional provisions (§§ 351–353). That layout is why a German product document cites §§ 138–141 for the contract-side
mechanics and §§ 74–88 for the balance sheet, and why the two rarely appear in the same paragraph.

### R5. VAG 2016 — the statute, its architecture and Anlage 1 (die Sparten)
- Publisher: Bundesministerium der Justiz / Bundesamt für Justiz, via `gesetze-im-internet.de`; mirrored by `dejure.org`,
  `buzer.de`, `lxgesetze.de`, `juraforum.de`, `anwalt.de`, `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`
- Doc type: federal statute (consolidated text) with annexes
- URL: https://www.gesetze-im-internet.de/vag_2016/BJNR043410015.html (returned); full text PDF
  https://www.gesetze-im-internet.de/vag_2016/VAG.pdf (returned); Anlage 1
  https://www.gesetze-im-internet.de/vag_2016/anlage_1.html (returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81**, read **2026-08-30**; **Anlage 1** and **§ 294** read in full. The
  `BJNR043410015.html` index page also serves (1.3 MB) and the `VAG.pdf` download serves (1.0 MB); the per-section HTML pages are
  frameset shells and `anlage_1.html` answered with a connection reset, which is why the XML is the citable route.
- Content: *Gesetz über die Beaufsichtigung der Versicherungsunternehmen*, in the version in force since **1 January 2016** —
  the Solvency II transposition. **Anlage 1** to the Act is the *Einteilung der Risiken nach Sparten*, and it decides which
  supervisory regime a product sits in and which undertakings must join the *Sicherungsfonds* [R12]. The life-relevant *Sparten*
  established from summaries: **19 Leben**, "soweit nicht unter den Nummern 20 bis 24 aufgeführt"; 20 Heirats- und
  Geburtenversicherung; **21 Fondsgebundene Lebensversicherung**; 22 Tontinengeschäfte; **23 Kapitalisierungsgeschäfte**,
  described as business in which, applying a mathematical procedure, premiums fixed in advance and the obligations assumed are
  fixed in duration and amount. The relevance to delib is direct: **eight of the ten products sit in Sparte 19**; the
  `fondsgebundene_rentenversicherung` sits in **Sparte 21** and therefore carries the separate *Anlagestock* rule of § 125 VAG
  [R7].
- Not established: the date of promulgation (1 April 2015 is the figure usually given) was **not returned by any search** and is
  `[unverified]`. A **Sparte 24** exists — the cross-reference "Nummern 20 bis 24" implies it — and is reported elsewhere as
  *Geschäfte der Verwaltung von Versorgungseinrichtungen*, but that title was not returned and is `[unverified]`. **§ 294 VAG as
  the general statement of supervisory objectives**, which German commentary usually cites, was not confirmed by any result and
  is `[unverified]`; BaFin's own page states the objective in prose without a section number [R21]. **The supervisory Sparte
  classification of a stand-alone *selbständige Berufsunfähigkeitsversicherung* and of a *Pflegerentenversicherung* — whether
  they are Sparte 19 business or fall to the health regime — was not established**; the query was cut by the exhausted budget,
  and it is an open question for BU and PFL.
- Read in the 2026-08-30 pass — **two resolutions.** **Anlage 1** reads *"19. Leben (soweit nicht unter den
  Nummern 20 bis 24 aufgeführt) 20. Heirats- und Geburtenversicherung 21. Fondsgebundene Lebensversicherung 22. Tontinengeschäfte
  23. Kapitalisierungsgeschäfte 24. Geschäfte der Verwaltung von Versorgungseinrichtungen 25. Pensionsfondsgeschäfte"* — so the
  Sparte 24 title is established and the list runs to 25, which the Nummer-19 exclusion does not reach. **§ 294 Abs. 1:**
  *"Hauptziel der Beaufsichtigung ist der Schutz der Versicherungsnehmer und der Begünstigten von Versicherungsleistungen."*, with
  Abs. 4 making the *Finanzaufsicht* watch over the *dauernde Erfüllbarkeit*. The statute's *Ausfertigung* is **1 April 2015**.
- Products: all ten.

### R6. VAG §§ 74–110, §§ 122–123 and § 40 — valuation, best estimate, risk margin, the LTG measures, SCR/MCR and the SFCR
- Publisher: Bundesamt für Justiz; mirrors at `dejure.org`, `buzer.de`, `lxgesetze.de`, `freirecht.de`, `juraforum.de`,
  `haufe.de`, `datenbank.nwb.de`, `sozialgesetzbuch-sgb.de`. Doc type: statutory sections.
- URL: https://www.gesetze-im-internet.de/vag_2016/__88.html ; https://dejure.org/gesetze/VAG/78.html ; .../82.html ;
  .../80.html ; .../96.html ; .../40.html ; https://freirecht.de/g/VAG:75 ; https://freirecht.de/g/VAG:100 ;
  https://www.haufe.de/id/norm/versicherungsaufsichtsgesetz-96-110-unterabschnitt-2-solvabilitaetskapitalanforderung-HI7709851.html
  (all returned). §§ 74 and 77 in the canonical `__74.html` / `__77.html` form `[unverified]`.
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81**, read **2026-08-30**; §§ 40, 74, 76, 77, 78, 80, 81, 82, 83, 88, 96, 122 and 123 read in full.
  `dejure.org/gesetze/VAG/78.html`, `freirecht.de/g/VAG:75` and `freirecht.de/g/VAG:100` also serve and were used as
  cross-checks; `gesetze-im-internet.de/vag_2016/__88.html` answered with a connection reset.
- Content: **§ 74** is the market-consistent valuation rule that makes the *Solvabilitätsübersicht* a different object from the
  HGB accounts: assets at the amount for which they could be exchanged, and liabilities at the amount for which they could be
  transferred or settled, **between knowledgeable, willing and independent business partners**, with — quoted from the summary —
  *"eine Anpassung der Bewertung zur Berücksichtigung der Bonität des Versicherungsunternehmens findet nicht statt"*, i.e. **no
  own-credit adjustment**. **§ 75** carries the § 74 Abs. 3 principles into the technical provisions. **§ 76**: their value is
  the **best estimate plus a risk margin**, calculated separately; **§ 77** defines the best estimate and **§ 78** the risk
  margin; **§ 79** carries the general calculation principles; **§ 83** obliges undertakings to use the technical information
  EIOPA publishes — **the hook by which the EIOPA curve, the volatility adjustment and the fundamental spreads become binding
  German law** [R4]; **§ 84** covers further matters. **§§ 80–82 are the long-term-guarantee measures.** § 82: **with the
  supervisor's approval** an undertaking may apply a ***Volatilitätsanpassung*** to the risk-free curve used for the best
  estimate under § 77. § 80: with approval, a ***Matching-Anpassung*** for a portfolio of life obligations including annuities
  from non-life contracts. **The two are mutually exclusive on the same obligations**, and matching is additionally excluded
  where the curve already carries a § 351 transitional [R13]. Their presence or absence moves a German solvency ratio by
  hundreds of percentage points, which is why **no delib document quotes one without saying whether it is *mit* or *ohne
  Volatilitätsanpassung und Übergangsmaßnahmen*** [R53]. **§ 88 matters most to delib, because it is the legal root of the
  DeckRV.** It places on the undertaking the burden of demonstrating the adequacy of its provisions, the suitability of its
  methods and the adequacy of its statistical data, and lets the supervisor order an increase where §§ 75–87 are not complied
  with. **§ 88 Abs. 3** empowers the Bundesministerium der Finanzen, in agreement with the Bundesministerium der Justiz und für
  Verbraucherschutz and observing the *Grundsätze ordnungsmäßiger Buchführung*, to fix by *Rechtsverordnung* **Höchstwerte für
  den Rechnungszins bei Versicherungsverträgen mit Zinsgarantie**, further requirements for the discount rates, and the
  actuarial bases and valuation methods for the *Deckungsrückstellung*. **That sentence is why the *Höchstrechnungszins* is a
  ministerial regulation rather than a supervisory circular, and why the DAV's annual recommendation is a recommendation and not
  a decision** [R14][R15][R56]. **§§ 96–110** are *Unterabschnitt 2 Solvabilitätskapitalanforderung*: § 96 allows a
  **Standardformel** or an **internes Modell**, with the supervisor able to order an internal model where the risk profile
  deviates materially from the standard formula's assumptions; § 100 sets out the *Basissolvabilitätskapitalanforderung*. The
  **MCR** is a separate Unterabschnitt of the same Kapitel, in force in Germany since **1 January 2016**, forming with the SCR a
  **two-tier ladder** whose lower rung marks an unacceptable risk level for policyholders. **§ 40** obliges publication of an
  annual **Bericht über Solvabilität und Finanzlage (SFCR)**, released by the *Vorstand* under § 40 Abs. 1 Satz 3 — the
  practical route to a named insurer's SCR ratio, technical provisions and transitional use.
- Not established: the text of **§ 74 Abs. 3** and of **§ 78** was not returned. **The MCR section numbers were not
  established**: §§ 122–124 is the range commonly cited, but § 124 is demonstrably *Anlagegrundsätze* [R7], so **delib cites the
  MCR by name, not by section**. **§ 234g VAG**, which surfaced in the same search, is the **Pensionsfonds** provision and is
  out of scope — recorded so no reader mistakes it for the life rule. The **MCR's absolute euro floors**, amended by the Sechste
  Verordnung of 19 July 2024 [R15], were **not established**. The Solvency II article numbers §§ 76–78 transpose are
  `[unverified]` [R1]. **No German volatility-adjustment value was established for any date**, and which German life insurers
  use the matching adjustment (reportedly none) was not established.
- Read in the 2026-08-30 pass — **the MCR sections are established and § 74 Abs. 3 is quotable.**
  **§ 122 *Bestimmung der Mindestkapitalanforderung; Verordnungsermächtigung*** and **§ 123 *Berechnungsturnus; Meldepflichten***
  are the MCR provisions, so delib may now cite them by section; § 124 begins the next Kapitel, which is why "§§ 122–124" was always
  going to fail. § 74 Abs. 3 Satz 2 verbatim: *"Eine Berichtigung der Bewertung, um die Bonität des Versicherungsunternehmens zu
  berücksichtigen, findet nicht statt."* — note the wording, which is not the *"eine Anpassung der Bewertung zur Berücksichtigung
  der Bonität ..."* form the earlier summary reproduced. § 78 Abs. 2 Satz 3 defers to any Commission cost-of-capital rate under
  Art. 86(d) of the directive, which is the 6 % of [R2]. § 88 Abs. 3 Satz 1 Nr. 1 empowers the BMF to fix *"bei
  Versicherungsverträgen mit Zinsgarantie einen oder mehrere Höchstwerte für den Rechnungszins"* — the recital the Sechste Verordnung
  cites [R15]. §§ 80 and 82 confirm the mutual exclusion of the matching and volatility adjustments in both directions.
- Products: all ten (cited-not-specified — the models publish the cash flows this block would be applied to, and perform no § 74
  valuation, no SCR and no MCR).

### R7. VAG §§ 124 and 125 — Anlagegrundsätze, Sicherungsvermögen and the Anlagestock
- Publisher: Bundesamt für Justiz; BaFin for the *Prudent-Person-Principle* topic page; mirrors at `buzer.de`, `lxgesetze.de`,
  `dejure.org`, `anwalt.de`, `lexetius.com`, `sozialgesetzbuch-sgb.de`; Gabler on *Anlagestock*. Doc type: statutory sections;
  supervisory topic page.
- URL: https://www.gesetze-im-internet.de/vag_2016/__124.html ; `__125.html` ;
  https://www.bafin.de/DE/Aufsicht/VersichererPensionsfonds/Kapitalanlagen/PrudentPersonPrinciple/prudent_person_principle_artikel.html
  ; https://www.versicherungsmagazin.de/lexikon/anlagestock-1944505.html ; and, kept outside the matrix, BaFin **Rundschreiben
  11/2017 (VA)** at
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Rundschreiben/2017/rs_1711_hinweise_anlage_sicherungsvermoegen_va.html
  (all returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81**, read **2026-08-30**; §§ 124 and 125 read in full. BaFin *Rundschreiben 11/2017 (VA)*
  also read (HTML, 298 kB). `gesetze-im-internet.de/vag_2016/__124.html` serves in full (9.7 kB); the BaFin *Prudent Person
  Principle* article page returns HTTP 404 and is dropped.
- Content: **§ 124** — since 1 January 2016 a Solvency II undertaking has **no quantitative investment limits**; the qualitative
  standard requires that all assets be invested so that the **security, quality, liquidity and profitability of the portfolio as
  a whole** are ensured and their location guarantees availability; that assets covering technical provisions be invested
  **appropriately to the nature and duration** of the liabilities; that they be invested in the interest of all policyholders in
  accordance with the disclosed investment policy; and that conflicts of interest resolve in policyholders' favour. **This is
  why a German life insurer's asset mix — and hence the *Kapitalanlageergebnis* that drives the *Überschussbeteiligung* [R18] —
  is not derivable from a rulebook, and why every asset-return assumption in delib is `**[std]**`.** **§ 125** — the
  ***Sicherungsvermögen*** is the ring-fenced pool covering policyholder claims: the *Vorstand* allocates to it during the year
  in line with the expected growth of the *Mindestumfang*; it is **administered separately** and held within the Member or
  Contracting States; and with approval **independent sections** may be formed. **The *Anlagestock***: for each *Anlageart* a
  **separate section of the Sicherungsvermögen** must be formed where life contracts provide benefits in units of an open fund
  under § 1 Abs. 4 KAGB, in shares issued by an investment company, in assets under § 2 Abs. 4 Investmentgesetz (as it stood to
  21 July 2013) excluding cash, or **directly linked to a share index or other reference value** — one summary placing this in
  **§ 125 Absatz 5**. That makes FRV structurally different from the general-account products (the unit fund is segregated, the
  policyholder bears its result, and the MindZV base differs [R21]) and supplies the statutory hook under which IDX sits. **The
  AnlV boundary**: BaFin *Rundschreiben 11/2017 (VA)* of **12 December 2017**, replacing the circular of **15 April 2011**,
  interprets the **Anlageverordnung 2016** and applies to **small insurers under §§ 212–217 VAG and to Pensionskassen and
  Pensionsfonds only** — **not** to the insurers writing the ten delib products. German market writing routinely cites AnlV
  quotas as if they bound all insurers; **since 1 January 2016 they do not bind the large life insurers at all.** One
  substantive point worth carrying: BaFin clarified that **zero- or negative-yielding investments may be admitted to the
  Sicherungsvermögen provided the profitability of the portfolio as a whole is ensured**.
- Not established: whether § 124 contains a derivatives or non-admitted-asset clause; **the Absatz numbering of the Anlagestock
  rule rests on one summary**; the *Mindestumfang* definition. **The AnlV's own content — the *Anlageformen*, the *Mischungs-*
  and *Streuungsquoten* — was not established and nothing in delib may state an AnlV quota.** Whether German index products are
  written inside an *Anlagestock* or in the general account was **not established** and is an open question for IDX.
- Read in the 2026-08-30 pass — **the Anlagestock Absatz is fixed and the IDX question is reframed.**
  The *Anlagestock* rule is **§ 125 Abs. 5**: *"Für jede Anlageart ist eine Abteilung des Sicherungsvermögens (Anlagestock) zu
  bilden"* where a life contract provides benefits in units of an open fund under § 1 Abs. 4 KAGB, in units issued by an investment
  company, in old § 2 Abs. 4 InvG assets, or binds them *"direkt an einen Aktienindex oder andere Bezugswerte"* (Nr. 4). **§ 125
  Abs. 2** defines the *Mindestumfang* as the sum of named balance-sheet items, so that gap closes too, and Abs. 4 requires separate
  administration and custody within the Member or Contracting States. **§ 124 Abs. 2 is the unit-linked carve-out**: Abs. 1 Nr. 5 to 8
  do not apply where the policyholder bears the investment risk, the provisions must be replicated by the units or by the units
  representing the reference value, and where such benefits carry a guarantee Nr. 5 to 8 apply again to the assets backing the
  additional provisions. **For IDX the statute supplies a test, not an answer:** an *Anlagestock* is required only where the linkage
  is *direct*, so whether a given German *Indexpolice* needs one turns on product design. § 124 fixes no quantitative limit anywhere.
- Products: FRV and IDX load-bearing; KLV, RV, BAS, RIE, SOF load-bearing on § 124 and the general *Sicherungsvermögen*; RLV,
  BU, PFL qualified.

### R8. VAG § 138 — Prämienkalkulation in der Lebensversicherung; Gleichbehandlung
- Publisher: Bundesamt für Justiz; mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`, `juraforum.de`,
  `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`, `haufe.de`, `lexsoft.de`
- Doc type: statutory section
- URL: https://www.gesetze-im-internet.de/vag_2016/__138.html (returned); https://dejure.org/gesetze/VAG/138.html (returned);
  https://lxgesetze.de/vag/138 (returned);
  https://www.juraforum.de/gesetze/vag/138-praemienkalkulation-in-der-lebensversicherung-gleichbehandlung (returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81**, read **2026-08-30**; § 138 read in full. `dejure.org/gesetze/VAG/138.html`,
  `lxgesetze.de/vag/138` and `juraforum.de` also serve; `gesetze-im-internet.de/vag_2016/__138.html` is a 4.4 kB frameset shell with
  no statutory text.
- Content: **Absatz 1** is the pricing-sufficiency rule and the reason a German tariff is priced on **prudent, not
  best-estimate, bases**: premiums in life insurance must be calculated *auf der Grundlage angemessener
  versicherungsmathematischer Annahmen* and set **high enough** that the undertaking can meet all its obligations and in
  particular form **adequate *Deckungsrückstellungen*** for the individual contracts. The undertaking's own financial position
  may be taken into account, but **funds not deriving from premium payments may not be used systematically and permanently** to
  support the tariff. That clause forbids permanent cross-subsidy of a loss-making tariff out of shareholder funds; it is why
  the first-order bases carry margins that later emerge as *Überschuss* [R47], and it is the statutory root of the *dauernde
  Erfüllbarkeit* standard that also appears in § 341e HGB [R54] and in BaFin's stated supervisory objective [R21]. **Absatz 2**
  is the equal-treatment rule, quoted by a search summary: *"Bei gleichen Voraussetzungen dürfen Prämien und Leistungen nur nach
  gleichen Grundsätzen bemessen werden."* This is the supervisory half of the fairness constraint on discretionary profit
  sharing. Search results establish that the **BGH, in a judgment of 18 September 2024, Az. IV ZR 436/22**, tied the supervisory
  equal-treatment principle of § 138 Abs. 2 VAG to the contractual entitlement of **§ 153 Abs. 2 VVG** [R24], under which
  policyholders must participate in surplus *nach einem verursachungsorientierten Verfahren*. Together they mean the German
  *Überschussbeteiligung* is **discretionary in level but not in method**: an insurer may set the declaration, but the split
  between *Abrechnungsverbände* must follow causation. Search summaries also record that § 138 contains an exception mechanism
  under which, when measures are taken, the policyholders' *Bestände* must be charged *verursachungsorientiert*, and that the
  provision addresses offsetting costs not covered by the premium calculation against surpluses from a more favourable risk or
  investment result.
- Not established: the number and content of the Absätze beyond 1 and 2. **Whether the *verursachungsorientiert* charging rule
  sits in § 138 or in § 140 is ambiguous across the two summaries and is `[unverified]`**; a delib document should attribute the
  causation principle to § 153 Abs. 2 VVG and § 138 Abs. 2 VAG **jointly**, as the BGH did, rather than to a single Absatz.
- Read in the 2026-08-30 pass — **one resolution and one correction.** **§ 138 has exactly two Absätze**,
  so the "Absätze beyond 1 and 2" caveat is closed. Abs. 1 verbatim: *"Die Prämien in der Lebensversicherung müssen unter
  Zugrundelegung angemessener versicherungsmathematischer Annahmen kalkuliert werden und so hoch sein, dass das
  Lebensversicherungsunternehmen allen seinen Verpflichtungen nachkommen und insbesondere für die einzelnen Verträge ausreichende
  Deckungsrückstellungen bilden kann. Hierbei kann der Finanzlage des Versicherungsunternehmens Rechnung getragen werden, ohne dass
  planmäßig und auf Dauer Mittel eingesetzt werden dürfen, die nicht aus Prämienzahlungen stammen."* Abs. 2 in full: *"Bei gleichen
  Voraussetzungen dürfen Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden."* **Correction:** the
  *verursachungsorientiert* rule is **not in § 138**; it is **§ 140 Abs. 1 Satz 3 VAG** and it is about charging RfB draw-downs back
  to the sub-portfolios that caused them, not a general surplus-allocation principle. The general causation principle is § 153 Abs. 2
  VVG [R24].
- Products: all ten; qualified only for FRV, whose investment result is the policyholder's, so that only the risk and cost
  results are shared.

### R9. VAG § 139 — Überschussbeteiligung and the Sicherungsbedarf test on Bewertungsreserven
- Publisher: Bundesamt für Justiz; mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`, `juraforum.de`,
  `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`, `lexsoft.de`, `gesatz.de`
- Doc type: statutory section
- URL: https://www.gesetze-im-internet.de/vag_2016/__139.html (returned); https://dejure.org/gesetze/VAG/139.html (returned);
  https://lxgesetze.de/vag/139 (returned); https://www.buzer.de/139_VAG.htm (returned);
  https://www.juraforum.de/gesetze/vag/139-ueberschussbeteiligung (returned); https://gesatz.de/link.aspx?lnk=31094 (returned,
  carrying the Abs. 3/4 text)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81**, read **2026-08-30**; § 139 read in full. `dejure.org/gesetze/VAG/139.html`,
  `buzer.de/139_VAG.htm`, `lxgesetze.de/vag/139` and `gesatz.de` also serve; the `gesetze-im-internet.de` per-section page is a
  6.0 kB frameset shell.
- Content: **Absatz 1**, quoted by a search summary: *"Die für die Überschussbeteiligung der Versicherten bestimmten Beträge
  sind, soweit sie den Versicherten nicht unmittelbar zugeteilt wurden, in der Bilanz in eine Rückstellung für
  Beitragsrückerstattung einzustellen."* This is the structural fact behind the whole German surplus chassis: **surplus
  earmarked for policyholders either goes out immediately as *Direktgutschrift* or into the RfB, and nowhere else.** A delib
  model of a profit-participating product must carry both a direct credit and an RfB stock, or it has not modelled the product.
  **Absatz 3** is the LVRG's *Bewertungsreserven* restriction [R20]: valuation reserves from **festverzinsliche Anlagen und
  Zinsabsicherungsgeschäfte**, held directly or indirectly, may be taken into account in policyholders' participation in
  valuation reserves **only to the extent that they exceed any *Sicherungsbedarf* aus Versicherungsverträgen mit
  Zinsgarantien**. Departing policyholders therefore share only in the excess. **Absatz 4** defines the test. Per the returned
  text: the *Sicherungsbedarf* from contracts with interest guarantees is the **sum of the Sicherungsbedarfe of those contracts
  whose applicable interest rate exceeds the applicable Euro interest-rate swap rate at the time the valuation reserves are
  determined**; and a single contract's *Sicherungsbedarf* is its **actuarially calculated interest obligation, computed using
  that reference rate, less the Deckungsrückstellung**. The mechanics of the reference rate and the fifteen-year look-forward
  are in MindZV §§ 11–12 [R18]. The practical consequence for delib: for a German contract written on a 3.25 % or 4.00 %
  *Höchstrechnungszins* [R15], the *Sicherungsbedarf* has for most of the last decade exceeded the fixed-income valuation
  reserves outright, so the *Bewertungsreserven* component of a maturity payout has often been **zero**. Any delib product
  document that models a *Bewertungsreserven* payment must say which side of this test it assumes, and the assumption is
  `**[std]**`.
- Not established: the full text of Absätze 2 and 5 onwards. The predecessor provision (**§ 56a VAG a.F.**), which most German
  commentary still names when describing the *Bewertungsreserven* rule, was **not confirmed by any search result** and is
  `[unverified]`. **A correction carried from the prudential sweep and stated here so it is not repeated:** § 139 VAG is
  *Überschussbeteiligung*, **not** the *Rückkaufswert* and **not** the Zillmerung cap; the *Rückkaufswert* is § 169 VVG [R28]
  and the *Höchstzillmersatz* is § 4 DeckRV [R16].
- Read in the 2026-08-30 pass. **§ 139 has exactly four Absätze**, so the "Absätze 2 and 5 onwards" caveat
  is closed and Abs. 2 is read: for *Versicherungsaktiengesellschaften* the *Vorstand* fixes the amounts with the *Aufsichtsrat*'s
  consent, amounts not owed as of right only so far as a **dividend of at least 4 per cent of the Grundkapital** can still be paid,
  and no balance-sheet profit may be distributed beyond a *Sicherungsbedarf*. Abs. 1, Abs. 3 and Abs. 4 are confirmed word for word,
  including *"deren maßgeblicher Rechnungszins über dem maßgeblichen Euro-Zinsswapsatz zum Zeitpunkt der Ermittlung der
  Bewertungsreserven (Bezugszins) liegt"*. **§ 56a VAG a.F. remains `[unverified]`** — the repealed statute is not part of the
  consolidated text.
- Products: KLV, RV, BAS, RIE, IDX, SOF load-bearing; RLV, BU, PFL qualified (the risk and cost results are shared, and the
  *Bewertungsreserven* rule reaches them only where the tariff carries a savings element); FRV qualified — see BaFin's
  interpretive decision on minimum allocation in unit-linked business [R21].

### R10. VAG §§ 140 and 145 — Rückstellung für Beitragsrückerstattung and the Verordnungsermächtigung
- Publisher: Bundesamt für Justiz; mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`, `haufe.de`, `sozialgesetzbuch-sgb.de`,
  `datenbank.nwb.de`
- Doc type: statutory sections
- URL: https://www.gesetze-im-internet.de/vag_2016/__140.html (returned); https://dejure.org/gesetze/VAG/140.html (returned);
  https://www.buzer.de/140_VAG.htm (returned); https://lxgesetze.de/vag/140 (returned);
  https://www.haufe.de/id/norm/versicherungsaufsichtsgesetz-140-rueckstellung-fuer-beitragsrueckerstattung-HI7710187_p140.html
  (returned); https://dejure.org/gesetze/VAG/145.html (returned); https://www.buzer.de/gesetz/11544/b28432.htm (returned, the
  Abschnitt 1 *Lebensversicherung* table of contents)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81**, read **2026-08-30**; §§ 140 and 145 read in full. `dejure.org/gesetze/VAG/140.html`,
  `buzer.de/140_VAG.htm`, `lxgesetze.de/vag/140`, `haufe.de` and `dejure.org/gesetze/VAG/145.html` also serve; the
  `gesetze-im-internet.de` per-section page is a 7.9 kB frameset shell.
- Content: **§ 140 — the use restriction.** Amounts allocated to the RfB may be used **only** for the *Überschussbeteiligung* of
  the insured, **including the participation in Bewertungsreserven prescribed by § 153 VVG** [R24]. That is a hard ring fence:
  RfB money cannot be released to shareholders. **The three escape hatches** — the number is corrected below from the statute —
  all require the supervisor's consent and are all confined to the part of the RfB **not** attributable to already-declared profit
  shares (*soweit sie nicht auf bereits festgelegte Überschussanteile entfällt*): the RfB may be drawn on **in the interest of the
  policyholders** (1) to avert an impending *Notstand*, (2) to offset **unforeseen losses from profit-participating contracts
  arising from general changes in circumstances**, and (3) to **increase the Deckungsrückstellung where the calculation bases must
  be adjusted because of an unforeseen and not merely temporary change in circumstances**. **Escape hatch (3) is the statutory
  route by which the German industry financed the *Zinszusatzreserve*
  out of the free RfB during the low-rate decade** [R17], and it is why a German life insurer's RfB stock and its ZZR stock move
  against each other. When such a measure is taken, the policyholders' *Bestände* are charged *verursachungsorientiert*.
  **Supervisory plans.** The supervisor may require a **Zuführungsplan** where the allocation to the RfB does not meet the
  minimum requirements (the MindZV, [R18]) and an **Ausschüttungsplan** where the *ungebundener* part of the RfB exceeds the
  maximum amount (the **MindZV § 13** cap, [R18]). **The collective part.** § 140 **Abs. 4** permits a life insurer to establish within
  the RfB **einen kollektiven Teil oder mehrere kollektive Teile**, assigned to all profit-participating contracts collectively
  rather than to a *Teilbestand*; the RfBV governs it [R19]. **§ 145 *Verordnungsermächtigung*** empowers the Bundesministerium
  der Finanzen to make regulations concerning the **Zuführung zur Rückstellung für Beitragsrückerstattung in der
  Lebensversicherung**. It is therefore the statutory root of the **MindZV** [R18] and, with § 140 Abs. 4, of the
  **RfBV** [R19] — the pair that turns § 139's "put it in the RfB" and § 140's "use it only for policyholders" into an
  arithmetic minimum. Recording the chain **§ 145 VAG → MindZV** correctly matters because delib product documents cite the
  MindZV percentages constantly and a reader needs to know why a ministry may set them.
- Not established: the distinction between ***gebundene*** and ***freie*** RfB — the vocabulary every German market commentary
  uses — is **not in the statutory text any search returned**; it emerges from § 28 RechVersV's *Schlussüberschussanteilfonds*
  and *festgelegte Überschussanteile* [R54] together with the RfBV's *ungebundene RfB* [R19], and delib defines the terms from
  those two instruments rather than from § 140. Whether the supervisor's consent under the escape hatches has ever been granted,
  and how often, was not established. The **precise wording of § 145 and the list of matters the regulation may cover were not
  established**, and whether § 145 also underpins the RfBV or the RfBV rests on § 140 alone is `[unverified]`. **A correction
  carried forward:** § 145 VAG is a *Verordnungsermächtigung*, **not** the *Sicherungsvermögen*; the *Sicherungsvermögen* is §
  125 VAG [R7].
- Read in the 2026-08-30 pass — **three corrections, all from the statutory text.** **(1) There are three
  escape hatches, not two.** § 140 Abs. 1 Satz 2 permits the RfB to be drawn on, in exceptional cases, with the supervisor's consent
  and in the policyholders' interest, to *"1. einen drohenden Notstand abzuwenden, 2. unvorhersehbare Verluste aus den
  überschussberechtigten Versicherungsverträgen auszugleichen, die auf allgemeine Änderungen der Verhältnisse zurückzuführen sind,
  oder 3. die Deckungsrückstellung zu erhöhen, wenn die Rechnungsgrundlagen auf Grund einer unvorhersehbaren und nicht nur
  vorübergehenden Änderung der Verhältnisse angepasst werden müssen"*, and Satz 3 adds *"Bei Maßnahmen nach Satz 2 Nummer 2 oder 3
  sind die Versichertenbestände verursachungsorientiert zu belasten."* **(2) The second plan is an *Ausschüttungsplan*, not a
  *Verteilungsplan*** (§ 140 Abs. 3 Nr. 2). **(3) The *kollektiver Teil* is § 140 Abs. 4**, not Abs. 1 Satz 2. **Resolved:** the term
  ***ungebunden*** is statutory — § 140 Abs. 2 Nr. 2 and Abs. 3 Nr. 2 — and the § 145 mapping is exact: **Abs. 1 → MindZV §§ 10–12,
  Abs. 2 → MindZV §§ 4–9, Abs. 3 → MindZV § 13, Abs. 4 → the certification wording, Abs. 6 (with § 140 Abs. 4) → RfBV.** **The cap on
  the *ungebundener Teil* is therefore MindZV § 13, not the RfBV** [R18] [R19].
- Products: KLV, RV, BAS, RIE, IDX, SOF load-bearing; RLV, BU, PFL, FRV qualified.

### R11. VAG §§ 141–143 — Verantwortlicher Aktuar, Treuhänder, Anzeigepflichten, and the deregulation of 29 July 1994
- Publisher: Bundesamt für Justiz; mirrors at `dejure.org`, `buzer.de`, `lxgesetze.de`, `juraforum.de`, `anwalt.de`,
  `lexetius.com`, `freirecht.de`, `datenbank.nwb.de`; for the deregulation, `de.wikipedia.org` and two Gabler
  *Versicherungslexikon* entries on `versicherungsmagazin.de`. Doc type: statutory sections; lexicon entries.
- URL: https://www.gesetze-im-internet.de/vag_2016/__142.html ; `__143.html` ; https://dejure.org/gesetze/VAG/141.html ;
  https://lxgesetze.de/vag/141 ; https://freirecht.de/g/VAG:128 ; https://de.wikipedia.org/wiki/Neubestand ;
  https://www.versicherungsmagazin.de/lexikon/altbestand-1944472.html (all returned); `__141.html` `[unverified canonical form]`
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81**, read **2026-08-30**; §§ 141, 142 and 143 read in full.
  `dejure.org/gesetze/VAG/141.html`, `lxgesetze.de/vag/141` and `freirecht.de/g/VAG:128` also serve, as do the
  *Altbestand*/*Neubestand* lexicon pages; the `gesetze-im-internet.de` per-section page for § 142 is a 4.3 kB frameset shell.
- Content: **§ 141 *Verantwortlicher Aktuar*.** Every life insurer must appoint one, *zuverlässig und fachlich geeignet*,
  **sufficient experience regularly assumed at three years' actuarial activity**, appointed and dismissed by the *Aufsichtsrat*.
  The duties that matter: an ***Erläuterungsbericht zur versicherungsmathematischen Bestätigung*** and an
  ***Angemessenheitsbericht*** go to the supervisor; the actuary **attends the Aufsichtsrat meeting on the annual accounts**;
  and the actuary **makes a proposal on the Überschussbeteiligung**, which the undertaking must **submit to the supervisor** and
  from which it may depart only on **written or electronic notification with reasons**. **That last item is the governance
  reason German declared rates cluster as tightly as the market data show** [R53]: the declaration is the board's, but it passes
  through a named actuary's written proposal. **§ 142** — for life contracts **concluded after 28 July 1994** where premiums can
  be changed for existing contracts, changes take effect only with an **unabhängiger Treuhänder**'s consent (§ 157 Abs. 1 and 2
  applying to the trustee), and the trustee step falls away where supervisory approval is required. It is the supervisory
  counterpart of § 163 VVG [R27]. (Separately, **§ 128** appoints a trustee guarding the *Sicherungsvermögen* *unter
  Mitverschluss*, and **§ 129** governs its securing.) **§ 143** is the German equivalent of a tariff filing: after
  authorisation the undertaking must **unverzüglich** notify the supervisor of the **Grundsätze für die Berechnung der Prämien
  und der Deckungsrückstellungen**, including the *verwendeten Rechnungsgrundlagen, mathematischen Formeln, kalkulatorischen
  Herleitungen und statistischen Nachweise*, and again whenever they change. **This is why a German tariff's first-order bases
  exist as a documented, supervisor-visible object — and equally why they are not public, which is the structural reason delib's
  decrement tables must be `**[std]**` proxies** [R47]. **The 29 July 1994 boundary.** German life business splits into
  ***Altbestand*** (before) and ***Neubestand*** (from). Until deregulation the AVB were part of a *genehmigungspflichtiger
  Geschäftsplan* approved by the Bundesaufsichtsamt für das Versicherungswesen; in the *Altbestand* that approved plan
  **continues to apply and changes still require approval**, while in the *Neubestand* contract design and premium calculation
  are **free within the statutory frame**. At deregulation **the entire RfB accumulated to 1994 was allocated exclusively to the
  Altbestand**, which is why insurers still run separate surplus accounts and why the MindZV computes the minimum **getrennt für
  Alt- und Neubestand** [R18]. **All ten delib products are Neubestand business and every product document says so** — a reader
  meeting a 4.00 % guarantee in a German data set is almost always looking at pre-2000 *Neubestand*.
- Not established: the text of the ***versicherungsmathematische Bestätigung*** was **not returned** and is `[unverified]`; its
  connection to §§ 341e–341h HGB is inferred [R54], not read. The one-day gap between § 142's "after **28** July 1994" and the
  deregulation date of **29** July 1994 is real in the sources and unexplained; both dates are given as found. § 157 VAG's
  content was not established, nor whether DAV standards bind the *Verantwortlicher Aktuar* as a matter of law [R56].
- Read in the 2026-08-30 pass. § 141 Abs. 1 Satz 4: *"Eine ausreichende Berufserfahrung ist regelmäßig
  anzunehmen, wenn eine mindestens dreijährige Tätigkeit als Versicherungsmathematiker nachgewiesen wird."*; Abs. 3 puts appointment
  and dismissal with the *Aufsichtsrat*; Abs. 5 Nr. 4 has the actuary propose the *Überschussbeteiligung* **to the Vorstand**, and
  **Abs. 6 Nr. 3** makes the *Vorstand* submit it to the supervisor and notify any departure, *"die Gründe für die Abweichung sind der
  Aufsichtsbehörde schriftlich oder elektronisch mitzuteilen"*. § 142 in full confirms the *"nach dem 28. Juli 1994 geschlossenen"*
  boundary and that the trustee step falls away where supervisory approval is needed. § 143 confirms the *Anzeigepflicht* wording.
  **The *Altbestand* definition is now available from a retrieved instrument**, though not from the VAG: **§ 2 Nr. 3 RfBV** ties it to
  § 336 VAG and Art. 16 § 2 Satz 2 of the Drittes Durchführungsgesetz/EWG zum VAG of 21 July 1994, extending it to contracts concluded
  between 1 January 1995 and 31 December 1997 that matched an *Altbestand* tariff and were settled with it until 12 April 2008 [R19].
  **Still `[unverified]`:** the claim that the whole pre-1994 RfB was allocated to the *Altbestand* at deregulation — market history,
  not statute.
- Products: all ten; § 143 load-bearing for every product's `sources.md` provenance discussion.

### R12. VAG §§ 221–236 and § 314, with Protektor — the Sicherungsfonds and the supervisor's crisis powers
- Publisher: Bundesamt für Justiz for the VAG and the two Verordnungen; Protektor Lebensversicherungs-AG; Wissenschaftliche
  Dienste des Deutschen Bundestages; mirrors at `dejure.org`, `buzer.de`, `lxgesetze.de`, `juraforum.de`, `rechtsportal.de`,
  `sozialgesetzbuch-sgb.de`. Doc type: statutory sections; the SichLVV and SichLVFinV; corporate and parliamentary documents.
- URL: https://www.gesetze-im-internet.de/vag_2016/__222.html ; https://dejure.org/gesetze/VAG/221.html ; .../226.html ;
  .../314.html ; https://www.gesetze-im-internet.de/sichlvv/BJNR117000006.html ;
  https://www.gesetze-im-internet.de/sichlvfinv_2016/BJNR082800016.html ;
  https://www.protektor-ag.de/de/sicherungsfonds/dokumente ;
  https://www.bundestag.de/resource/blob/412602/04b5e6635cb5cdea18c3b7bcd94dbcac/WD-4-256-12-pdf.pdf (all returned)
- Retrieved: **yes** for the VAG — canonical XML, **Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81**, read **2026-08-30**; §§ 221, 222, 226 and 314 read in full.
  `gesetze-im-internet.de/vag_2016/__222.html` serves in full (8.5 kB) and `dejure.org/gesetze/VAG/221.html` serves.
  **The SichLVV index page is a 6.1 kB shell**; the SichLVFinV serves (26 kB); the Protektor documents page serves (88 kB) but
  **no Protektor document was opened**, so the Mannheimer chronology remains `[unverified]`.
- Content: **§ 221 *Pflichtmitgliedschaft*.** Undertakings authorised to write the business of **Sparten 19 to 23 of Anlage 1**
  [R5] **must belong to a Sicherungsfonds** protecting the claims of policyholders, insured persons and beneficiaries.
  **Pensions- und Sterbekassen are excepted** — exactly the vehicles delib puts out of scope. **§ 222 — the five-per-cent
  haircut.** Where the fund's *Sicherungsvermögen* plus collectable *Sonderbeiträge* is insufficient to secure continuation of
  the contracts, **the supervisor may reduce the obligations under the life contracts by at most 5 per cent of the contractually
  guaranteed benefits**, and may issue orders to prevent an extraordinary increase in early terminations. **§ 226
  *Finanzierung*.** The **sum of the annual contributions** is **0.2 per mille of the sum of the members'
  versicherungstechnische Netto-Rückstellungen** measured **according to §§ 341e to 341h HGB** [R54] — the statutory accounts,
  not the Solvency II balance sheet; the fund's own *Sicherungsvermögen* **should not fall below 1 per mille** of that aggregate
  and **Sonderbeiträge** may be levied **up to 1 per mille**; individual contributions are set under the **SichLVFinV**.
  **Protektor** is the German life guarantee scheme: the statutory *Sicherungsfonds* whose **tasks and powers were transferred
  to it by the SichLVV**, with compulsory membership for life insurers and for branches writing life business in Germany. **The
  Mannheimer case is the only time it has been used and the chronology is established**: in **June 2003** Protektor received a
  commitment declaration for the transfer of the portfolio of the insolvency-threatened *Mannheimer Lebensversicherungs-AG*;
  negotiations concluded **18 September 2003**, notarised **26/27 September 2003**, with economic effect from **1 July 2003**;
  **BaFin approved the Bestandsübertragungsvertrag on 1 October 2003** and **138 Mannheimer employees became Protektor employees
  that day**. Protektor was then a **voluntary** industry vehicle; the **statutory** fund was created by VAG amendments of **15
  December 2004**. For delib, Protektor is the answer to "what happens if the insurer fails" in every product document, and the
  precedent is **a portfolio transferred and continued, not a payout**. **§ 314 *Zahlungsverbot; Herabsetzung von Leistungen***
  is the crisis power and the single most important qualification on the word "guarantee". **Abs. 1**: where an undertaking is
  **permanently unable to meet its obligations** but avoiding insolvency appears to be in the insured's interest, the supervisor
  may take the necessary measures and **temporarily prohibit all kinds of payments**, the summary naming
  **Versicherungsleistungen**, **Gewinnverteilungen** and, for life insurance, **den Rückkauf oder die Beleihung des
  Versicherungsscheins sowie Vorauszahlungen darauf** — so **a delib document modelling a surrender option says the option is
  suspendable by the supervisor**. **Abs. 2**: the supervisor may **reduce the obligations of a life insurer in accordance with
  its Vermögenslage**, the *Deckungsrückstellungen* being **reduced first and the Versicherungssummen then recomputed**, or the
  *Versicherungssummen* reduced directly where that is not possible; **the policyholder's duty to keep paying premiums at the
  previous level is unaffected**; and the supervisor **may proceed unequally where special circumstances justify it**. German
  life guarantees therefore sit under **two distinct write-down powers**: a **fund-level 5 % cap** under § 222 and an
  **uncapped, asset-position-driven reduction** under § 314. **No delib document describes a German guarantee as
  unconditional.**
- Not established: the three § 226 figures came from summaries of one query and **the repeated 1 ‰ may be an artefact of two
  Absätze using the same number, or of one summary conflating them**; both readings are recorded and the *Sonderbeitrag* figure
  is `[unverified]`. The fund's member count and asset stock, § 336 VAG's content and the exact date the statutory fund began
  operating were not established. **Whether § 314 has ever been applied to a German life insurer was not established**, and
  **the relationship between § 314 and the § 222 cap — which applies first, and whether the § 314 reduction is bounded — was not
  established and must not be asserted.** A draft **VSAAG** surfaced on the DAV site and would change the resolution framework;
  its content and status are `[unverified]`. **A correction carried forward:** § 146 VAG is **not** the Sicherungsfonds — it
  concerns substitutive Krankenversicherung, out of delib scope.
- Read in the 2026-08-30 pass — **one correction and several precisions.** **Correction:** the § 222
  five-per-cent step is a **duty, not a discretion** — § 222 Abs. 5: *"setzt die Aufsichtsbehörde bei Lebensversicherungsverträgen
  die Verpflichtungen aus den Verträgen um maximal 5 Prozent der vertraglich garantierten Leistungen herab"* — and the section is
  titled *Aufrechterhaltung der Versicherungsverträge*, its Abs. 2 ordering the whole portfolio transferred to the fund with
  *dingliche Wirkung*. § 221 confirms Sparten 19 bis 23 and the *Pensions- und Sterbekassen* exception. § 226 confirms the
  **0,2 Promille** annual contribution on the §§ 341e–341h HGB net technical provisions (Abs. 5 Satz 2), and adds the **1 Promille**
  target for the fund's assets (Abs. 4) and **1 Promille** maximum *Sonderbeiträge* (Abs. 5 Satz 5). § 314 Abs. 1 and Abs. 2 confirm
  both write-down powers verbatim, including *"Die Pflicht der Versicherungsnehmer, die Versicherungsentgelte in der bisherigen Höhe
  weiterzuzahlen, wird durch die Herabsetzung nicht berührt."* and the ability to proceed unequally; **Abs. 3** allows both powers to
  be confined to a *selbständige Abteilung des Sicherungsvermögens*.
- Products: all ten (the outer boundary of every guarantee in the library).

### R13. VAG §§ 351–353 — the Solvency II transitional measures and the 2024 recalculation
- Publisher: Bundesamt für Justiz; BaFin; mirrored by `dejure.org`, `buzer.de`, `rechtsportal.de`, `lexsoft.de`,
  `sozialgesetzbuch-sgb.de`
- Doc type: statutory sections; supervisory application pages; a BaFin *Fachartikel*
- URL: https://dejure.org/gesetze/VAG/351.html (returned); https://dejure.org/gesetze/VAG/352.html (returned);
  https://dejure.org/gesetze/VAG/353.html (returned); https://www.buzer.de/352_VAG.htm (returned);
  https://www.bafin.de/DE/Aufsicht/VersichererPensionsfonds/Antraege/Uebergangsmassnahmen/uebergangsmassnahmen_node.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2024/fa_bj_0702_Solvency_II_Uebergangsmassnahmen.html
  (returned — BaFin *Fachartikel* "Neu rechnen, bitte!")
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81**, read **2026-08-30**; §§ 351, 352 and 353 read in full.
  `dejure.org/gesetze/VAG/351.html`, `/352.html`, `/353.html` and `buzer.de/352_VAG.htm` serve, as do BaFin's
  *Übergangsmaßnahmen* pages and its *Neu rechnen, bitte!* article; the map-report 939 press release was read (HTML, 94 kB).
- Content: **§ 352** is the *Rückstellungstransitional*: a deduction that temporarily reduces technical provisions on the
  Solvency II balance sheet, and thereby raises eligible own funds, for business written before the regime began. **The maximum
  deductible portion falls linearly from 100 per cent in the year beginning 2016 to 0 per cent on 1 January 2032** — a
  sixteen-year run-off. **§ 351** is the parallel transitional on the risk-free rates. **§ 353**: an undertaking that determines
  it would not meet the SCR without the § 351 or § 352 transitional must, **within two months**, submit a plan setting out the
  gradual introduction of measures to raise eligible own funds or reduce the risk profile so that SCR compliance is restored
  **by the end of the transitional period**. **The 2024 recalculation is the single most consequential supervisory event in the
  German life market since the LVRG, and it is well corroborated.** In **Q2 2024** BaFin ordered life insurers to
  **recalculate** the *Rückstellungstransitional*, on the ground that the interest-rate rise which ended the low-rate phase from
  2022 had made the existing deduction amounts inappropriate: higher rates sharply reduced Solvency II technical provisions and
  hence raised own funds, while the SCR also fell. A BaFin spokesman is quoted to the effect that **for most companies the
  Rückstellungstransitional takes the value 0 after recalculation**. The effect on published ratios is in [R53]. For delib the
  discipline is simple: **no delib model implements a transitional**, and any German solvency ratio quoted in a delib document
  must state whether it is before or after the 2024 recalculation, because the two are not comparable.
- Not established: **the legal instrument by which BaFin "ordered" the recalculation** — a general administrative act,
  individual orders, or an interpretation of § 352 itself — was **not established**. How many undertakings held a § 351
  transitional as opposed to a § 352 one was not established. The exact wording of the § 352 linear formula was not read.
- Read in the 2026-08-30 pass — **the legal basis of the 2024 recalculation is established.** **§ 352
  Abs. 3**: the amounts used to compute the deduction *"dürfen mit Genehmigung oder müssen auf Verlangen der Aufsichtsbehörde alle
  24 Monate oder, wenn sich das Risikoprofil des Unternehmens wesentlich verändert, häufiger neu berechnet werden"* — so BaFin's
  order is an exercise of its *Verlangen* under § 352 Abs. 3, not a new power. The linear run-off is verbatim: *"Der maximal
  abzugsfähige Anteil sinkt am Ende jedes Kalenderjahres linear von 100 Prozent während des Jahres ab 2016 auf 0 Prozent am
  1. Januar 2032."*, with § 351 Abs. 2 Satz 2 identical for the rate transitional, the two mutually exclusive (§ 351 Abs. 4 Nr. 2,
  § 352 Abs. 5). § 353 Abs. 2 confirms the **two-month** plan deadline and Abs. 3 adds twelve-monthly progress reports and revocation
  where compliance becomes unrealistic. map-report confirms the market effect and notes that *"von der Aufsicht keine pauschale
  Abschaffung des Rückstellungstransitionals angeordnet"* wurde.
- Products: all ten (cited-not-specified).

---

## 3. Prudential — reserving, the Höchstrechnungszins and the Zinszusatzreserve

The DeckRV is made under § 88 Abs. 3 VAG [R6] and fixes the *Rechnungsgrundlagen* of the German statutory *Deckungsrückstellung*
— the HGB reserve of § 341f HGB [R54], **not** the Solvency II best estimate. This distinction is the axis of the whole German
reserving picture and every delib document keeps it: an insurer carries **two liability measures**, and the
*Überschussbeteiligung*, the *Zinszusatzreserve* and the § 139 VAG *Bewertungsreserven* test all run on the **HGB** side.

### R14. DeckRV — the reserving regulation and its § 2, the Höchstzinssatz
- Publisher: Bundesamt für Justiz; mirrored by `buzer.de`, `umwelt-online.de`, `jurawelt.com`, `gesatz.de`, `de.wikipedia.org`;
  BaFin for the FAQ that states the 2025 change
- Doc type: Rechtsverordnung of **18 April 2016**, and its § 2
- URL: https://www.gesetze-im-internet.de/deckrv_2016/BJNR076700016.html (returned); PDF
  https://www.gesetze-im-internet.de/deckrv_2016/DeckRV.pdf (returned); https://www.gesetze-im-internet.de/deckrv_2016/__2.html
  (returned); https://www.buzer.de/gesetz/12006/a198101.htm (returned);
  https://www.bafin.de/SharedDocs/FAQs/DE/VA/Pensionskassen/01_Frage.html (returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250**, read **2026-08-30**; §§ 1, 2, 3, 4, 5 and 5a read in full — the whole regulation.
  The `BJNR076700016.html` index page serves (20 kB) and `DeckRV.pdf` serves (58 kB); `buzer.de/gesetz/12006/a198101.htm` and BaFin's
  Pensionskassen FAQ were read as cross-checks; the `gesetze-im-internet.de/deckrv_2016/__2.html` per-section page is a 5.5 kB
  frameset shell.
- Content: *Verordnung über Rechnungsgrundlagen für die Deckungsrückstellungen*. The sections that matter to delib are **§ 2**
  (the *Höchstrechnungszins*), **§ 4** (*Höchstzillmersätze und versicherungsmathematische Berechnungsmethode*, [R16]) and **§
  5**, whose **Absatz 3** carries the *Referenzzins* that generates the *Zinszusatzreserve* [R17]. **§ 2 fixes the maximum
  interest rate at which a German life insurer may discount its statutory *Deckungsrückstellung* for contracts carrying an
  interest guarantee**, and therefore — through § 138 Abs. 1 VAG's requirement that premiums be adequate to fund that reserve
  [R8] — the maximum rate at which a new tariff may be priced. It is the *Garantiezins* of market language, although the two are
  not legally identical: § 2 caps the **reserving** rate; the guaranteed rate a policy carries is a tariff decision that may be
  lower. BaFin's FAQ title states the operative change in terms: *"Zum 1. Januar 2025 wird der Höchstrechnungszins in § 2 der
  Deckungsrückstellungsverordnung (DeckRV) von 0,25 Prozent auf 1,0 Prozent angehoben"* (Stand 09.09.2024) — quoted from the
  search result, not from BaFin. Two structural facts a delib document needs: the rate applies **to new business at the time of
  contract conclusion** and then **stays with the contract for its whole term**, which is why the German in-force book is a
  stack of cohorts [R15] and why the *Zinszusatzreserve* exists at all; and the same rate applies to Pensionskassen, which delib
  puts out of scope, so the FAQ is cited for the life rate only.
- Not established **as at the original build; all four points are resolved by the 2026-08-30 pass below.** The wording of § 2,
  whether it states a single rate or a rate plus qualifications, the reserving-versus-guarantee question, the publisher disagreement
  over the section title, and the section list were all open; the § 3 note — that a 60 %/85 % yield cap "must be the pre-2016
  regulation" — was **wrong**. **What remains open:** the historic **60 %** ceiling is not in the DeckRV 2016 at all; its home was
  the repealed Article 20 of Directive 2002/83/EC, which was not retrieved [R56].
- Read in the 2026-08-30 pass — **two corrections and the full section list.** **(1) The statute's term is
  *Höchstzinssatz*.** The § 2 heading is *"Höchstzinssatz"* and Abs. 1 Satz 1 reads *"... wird der Höchstzinssatz für die Berechnung
  der Deckungsrückstellungen auf 1 Prozent festgesetzt"*. `buzer.de` was right; BaFin, the BMF and the DAV use *Höchstrechnungszins*,
  which is the market name for the same rate. **(2) § 3 *Ausnahmen* is live law, not a pre-2016 residue** — the earlier note that an
  85 % yield cap "must be the pre-2016 regulation" is wrong. § 3 Abs. 1 caps the *Rechnungszins* for **single-premium contracts with a
  term up to eight years** at **85 per cent of the last month-end *Umlaufrendite der Anleihen der öffentlichen Hand*** of matching
  residual maturity, measured at the premium date; § 3 Abs. 2 applies the same 85 per cent cap to **annuity contracts without a
  surrender value**, for the eight years from annuity commencement and for the part of the reserve attributable to the annuity in
  payment, against the mean of the last month-end values for one-to-eight-year maturities. **That bears directly on `sofortrente` and
  on single-premium points in KLV and RV.** **Section list:** § 1 Geltungsbereich, § 2 Höchstzinssatz, § 3 Ausnahmen, § 4
  Höchstzillmersätze und versicherungsmathematische Berechnungsmethode, § 5 Versicherungsmathematische Rechnungsgrundlagen,
  § 5a Übergangsregelung, § 6 Inkrafttreten. § 2 Abs. 2 Satz 1 fixes the cohort rule; § 1 Abs. 2 confines the regulation to contracts
  without an approved tariff, i.e. the *Neubestand*.
- Products: all ten; qualified for FRV, where it bites on the *Rentenphase* and any guarantee component rather than on the unit
  fund.

### R15. The Höchstzinssatz / Höchstrechnungszins rate history and the Sechste Verordnung of 19 July 2024
- Publisher: Bundesministerium der Justiz / `recht.bund.de` for the BGBl; Bundesministerium der Finanzen for the
  Referentenentwurf; Deutsche Aktuarvereinigung for the fact sheet; VPV, Wikipedia, cecu.de, bavprofis.de and ihre-vorsorge.de
  for the rate table
- Doc type: amending Rechtsverordnung; professional fact sheet; secondary rate tables
- URL: https://www.recht.bund.de/bgbl/1/2024/250/VO.html (returned);
  https://aktuar.de/content/PDF/Fachwissen/H%C3%B6chstrechnungszins_in_der_Lebensversicherung.pdf (returned);
  https://de.wikipedia.org/wiki/H%C3%B6chstrechnungszins (returned);
  https://www.bundesfinanzministerium.de/Content/DE/Gesetzestexte/Gesetze_Gesetzesvorhaben/Abteilungen/Abteilung_VII/20_Legislaturperiode/2024-06-27-Sechste-VO-VAG/1-Referentenentwurf.pdf?__blob=publicationFile&v=2
  (returned)
- Retrieved: **yes** — the ***Regelungstext*** of the Sechste Verordnung at
  https://www.recht.bund.de/bgbl/1/2024/250/regelungstext.pdf?__blob=publicationFile&v=1 (PDF, 2 pp.), and the **DAV *Fachwissen*
  fact sheet** *Höchstrechnungszins in der Lebensversicherung* at
  https://aktuar.de/content/PDF/Fachwissen/H%C3%B6chstrechnungszins_in_der_Lebensversicherung.pdf (PDF, 2 pp.), both read
  **2026-08-30**. **The `VO.html` page carries only the metadata** — publication 24.07.2024, *Ausfertigung* 19.07.2024, FNA
  7631-11-5/-10/-12 — and the text is in the linked `regelungstext.pdf`. The BMF *Referentenentwurf* PDF returns HTTP 404 and is
  dropped. The Siebte (BGBl. 2024 I Nr. 414) and Achte (BGBl. 2025 I Nr. 31) Verordnung announcement pages serve.
- Content: **the full rate history**, as returned by the search summary of the rate table. Every figure carries its period:

  | Period | Höchstrechnungszins |
  |---|---|
  | 1987 – 06/1994 | **3.50 %** |
  | 07/1994 – 06/2000 | **4.00 %** |
  | 07/2000 – 2003 | **3.25 %** |
  | 2004 – 2006 | **2.75 %** |
  | 2007 – 2011 | **2.25 %** |
  | 2012 – 2014 | **1.75 %** |
  | 2015 – 2016 | **1.25 %** |
  | 2017 – 2021 | **0.90 %** |
  | 2022 – 2024 | **0.25 %** |
  | from 2025 | **1.00 %** |

Two facts about the table are load-bearing and separately corroborated: the **1994 move was an increase**, from 3.50 % to 4.00
%, and the summary states the rate "only increased in 1994 … and has only been reduced since then"; and the **2025 move to 1.00
% is the first increase in about thirty years**, described in the sources as the first since deregulation in 1994 [R11].
  **Both readings need one correction from the retrieved DAV table below: the 1987 step from 3,00 % to 3,50 % was also an increase**,
  so the series has three increases in total — 1987, 1994 and 2025 — and the 2025 move is the first in thirty and a half years,
  counting from July 1994. **The
instrument.** The Bundesministerium der Finanzen amended the DeckRV by the **Sechste Verordnung zur Änderung von Verordnungen
nach dem Versicherungsaufsichtsgesetz of 19 July 2024**, published as **BGBl. 2024 I Nr. 250**, setting the
*Höchstrechnungszins* at **1.00 % with effect from 1 January 2025**; the DeckRV amendment is Article 1 of that regulation, and a
**Referentenentwurf of 27 June 2024** is on the BMF site. The same regulation **updated the absolute floors for the
Mindestkapitalanforderung** following a European Commission notification. For delib the operative number for a new-business
tariff written today is **1.00 % (2025 onwards)**, and every model point representing an older cohort carries its cohort's rate;
all ten products' `**[std]**` guaranteed rates are anchored to this table.
- Not established: the precise **within-year effective dates** for the 2000, 2004, 2007, 2012, 2015, 2017 and 2022 steps were
  not established beyond the half-year granularity shown. The **MCR absolute floors** set by the Sechste Verordnung are
  `[unverified]` — no euro figure was returned. Two later instruments in the same series were located and **not investigated**:
  the **Siebte Verordnung** (`https://www.recht.bund.de/bgbl/1/2024/414/VO.html`, returned) and the **Achte Verordnung**
  (`https://www.recht.bund.de/bgbl/1/2025/31/VO.html`, returned); their content is `[unverified]` and either could have moved
  the rate again.
- Read in the 2026-08-30 pass — **the rate table and the amending instrument are both first-hand now.**
  The DAV fact sheet publishes the series from 1903: **1903–1922 3,50 %; 1923–1941 4,00 %; 1942–1986 3,00 %; 1987–06/1994 3,50 %;
  07/1994–06/2000 4,00 %; 07/2000–2003 3,25 %; 2004–2006 2,75 %; 2007–2011 2,25 %; 2012–2014 1,75 %; 2015–2016 1,25 %; 2017–2021
  0,90 %; 2022–2024 0,25 %; 2025 1,00 %** — every row previously carried is confirmed and three earlier cohorts are added. The
  Verordnung's Artikel 1: *"In § 2 Absatz 1 Satz 1 der Deckungsrückstellungsverordnung vom 18. April 2016 (BGBl. I S. 767), die
  zuletzt durch Artikel 1 der Verordnung vom 22. April 2021 (BGBl. I S. 842) geändert worden ist, wird die Angabe „0,25 Prozent“
  durch die Angabe „1 Prozent“ ersetzt."*; Artikel 4: *"Diese Verordnung tritt vorbehaltlich des Satzes 2 am 1. Januar 2025 in Kraft.
  Artikel 2 tritt am Tag nach der Verkündung in Kraft."* **The MCR absolute floors are established:** Artikel 2 raises § 1 Abs. 2
  KapAusstV from 2,5 to **2,7 Mio. Euro**, from 3,7 to **4 Mio. Euro** (twice), from 3,6 to **3,9 Mio. Euro** and from 1,2 to
  **1,3 Mio. Euro**. **Caveat on the source:** the DAV fact sheet as served is a mixed edition — its prose still says
  *"Aktuell liegt er bei 0,25 Prozent"* while its table already carries the 2025 row.
- Products: all ten.

### R16. DeckRV § 4 — Höchstzillmersätze
- Publisher: Bundesamt für Justiz; `buzer.de`; `haufe.de` (pre-2016 version under the same section number); secondary
  explanations at `verivox.de`, `ivwkoeln.web.th-koeln.de`, `versicherungsbote.de`, `versicherungs-wiki.de`
- Doc type: section of a Rechtsverordnung
- URL: https://www.gesetze-im-internet.de/deckrv_2016/__4.html (returned);
  https://www.verivox.de/lebensversicherung/themen/zillmerung/ (returned);
  https://ivwkoeln.web.th-koeln.de/versicherungslexikon/2015/08/11/zillmerung/ (returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250**, read **2026-08-30**; § 4 read in full. The
  `gesetze-im-internet.de/deckrv_2016/__4.html` per-section page is a 6.2 kB frameset shell; the *Zillmerung* lexicon pages at
  `verivox.de` and `ivwkoeln.web.th-koeln.de` serve and were used only as background.
- Content: *Zillmerung* is the mechanism by which an insurer offsets a contract's one-off acquisition costs against its first
  premiums, which is why a German endowment or annuity has a very low surrender value in its early years. **§ 4 DeckRV caps it:
  the *Zillmersatz* may not exceed 25 per mille (25 ‰, i.e. 2.5 %) of the *Beitragssumme***, the sum of all premiums payable
  under the contract. The claim for reimbursement of one-off acquisition costs may be covered individually, from the highest
  possible premium components up to the height of the *Zillmersatz*, **from the inception of the insurance**; and **the
  *Zillmersatz* an undertaking uses at the time of contract conclusion applies for the whole term**, so a pre-2015 contract
  keeps its 40 ‰ basis. **The 2015 cut**: the maximum was reduced from **40 ‰ to 25 ‰ with effect from 1 January 2015** by the
  LVRG [R20]; summaries state the pre-reform figure both as "40 Promille" and as "bis zu 4 Prozent", which are the same number.
  For delib this parameter sets the shape of the guaranteed surrender-value curve in the first years of every regular-premium
  product, and it **interacts with § 169 VVG's independent five-year-spread floor** [R28]: the DeckRV governs what the insurer
  may **reserve**, § 169 VVG governs what it must **pay**, and a delib model carrying a zillmerised reserve applies both
  separately, the tighter binding.
- Not established: **a real conflict in the summaries about what the percentage is a percentage of.** One rendering states the
  cap applies to premiums paid that are *not used for insurance coverage and administration cost coverage*; a second, closer to
  the DeckRV text, states that in the *Barwert der Prämien* no more than **2.5 % of premium components above the current value
  of the obligation** may be applied; a third states plainly "25 ‰ der Beitragssumme". **The plain reading is the one German
  market documents use and the one delib adopts, but the exact statutory base is not established**, and any restatement of the
  mechanism beyond "25 ‰ of the Beitragssumme" is `[unverified]`. Whether the cap applies to single-premium contracts, and how
  the *Beitragssumme* is defined for them, was not established. The statement that the § 169 five-year spread and the 25 ‰ cap
  are **independent constraints** is the compiler's inference; no source says so explicitly.
- Read in the 2026-08-30 pass — **the three-way conflict this entry recorded is resolved, because all
  three renderings are partial views of one sentence.** § 4 Abs. 1 in full: *"Im Wege der Zillmerung werden die Forderungen auf Ersatz
  der geleisteten, einmaligen Abschlusskosten einzelvertraglich bis zur Höhe des Zillmersatzes ab Versicherungsbeginn aus den
  höchstmöglichen Prämienteilen gedeckt, die nach den verwendeten Berechnungsgrundsätzen in dem Zeitraum, für den die Prämie gezahlt
  wird, weder für Leistungen im Versicherungsfall noch zur Deckung von Kosten für den Versicherungsbetrieb bestimmt sind. Der
  Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten."* — **note *Summe aller Prämien*, not *Beitragssumme***,
  which is the market term. Abs. 2 ties the uncovered part to the § 15 Abs. 1 RechVersV receivable and deducts it from the present
  value of future premiums; Abs. 3 carves out contracts where § 25 Abs. 2 RechVersV forces a higher reserve; **Abs. 4** fixes the
  cohort rule: *"Der von einem Versicherungsunternehmen zum Zeitpunkt des Vertragsabschlusses verwendete Zillmersatz ... gilt für die
  gesamte Laufzeit des Vertrages."* **Still `[unverified]`:** the 40 ‰ → 25 ‰ step and its 1 January 2015 date — the consolidated text
  shows only 25 ‰ and the amending instrument was not read.
- Products: every regular-premium product load-bearing — KLV, RV, BAS, RIE, FRV, IDX, RLV, BU, PFL. Not relevant to SOF, a
  single-premium payout annuity that is not zillmered in this sense.

### R17. DeckRV § 5 Abs. 3 — the Referenzzins, the Zinszusatzreserve and the Korridormethode
- Publisher: Bundesamt für Justiz; BaFin for the interpretive decision; `buzer.de`, `jurion.de`, `de.wikipedia.org`; technical
  commentary at `heistermannconsulting.de` and `msg-insurance-suite.com`; trade press (`cash-online.de`, Versicherungsbote,
  Pfefferminzia, GDV, Allianz Global Investors) for the quantum. Doc type: section of a Rechtsverordnung; a BaFin
  *Auslegungsentscheidung*; trade-press analysis.
- URL: https://www.gesetze-im-internet.de/deckrv_2016/__5.html ; https://www.buzer.de/gesetz/12006/a198104.htm ;
  https://www.bafin.de/SharedDocs/Downloads/DE/Auslegungsentscheidung/dl_ae_151204_projektion_referenzzins_va.html ;
  https://heistermannconsulting.de/referenzzinsatz-fuer-die-zzr-zum-31-12-2022-betraegt-157/ ;
  https://www.cash-online.de/a/zinszusatzreserve-korridormethode-bringt-zehn-milliarden-euro-entlastung-allein-2018-430796/ ;
  https://www.versicherungsbote.de/id/4939216/Zinszusatzreserve-2024-Milliarden-fliessen-zurueck---und-vieles-bleibt-offen/ (all
  returned)
- Retrieved: **yes** for the regulation — canonical XML, **Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250**, read **2026-08-30**; §§ 5 and 5a read in full. The
  `gesetze-im-internet.de/deckrv_2016/__5.html` per-section page does serve (8.3 kB), as does `buzer.de/gesetz/12006/a198104.htm`;
  **BaFin's *Auslegungsentscheidung* on the projection of the *Referenzzins* was read** (HTML, 82 kB).
  `heistermannconsulting.de` returns HTTP 404. **The ZZR quantum figures below come from trade press that was not re-opened in this
  pass and stay `[unverified]`.**
- Content: **What the ZZR is.** The ***Zinszusatzreserve*** is the additional German statutory reserve arising when the discount
  rate applicable under § 5 DeckRV must be reduced below a contract's tariff rate, producing a **higher *Deckungsrückstellung*
  than the tariff rate alone would give**. It is an **HGB** reserve, financed out of the result and, under § 140 VAG's second
  escape hatch, out of the free RfB [R10]. **How the *Referenzzins* is built.** It uses the **month-end zero-coupon Euro
  interest-rate swap rates at ten years published by the Deutsche Bundesbank under § 7 der Rückstellungsabzinsungsverordnung**:
  for each of the **nine preceding calendar years** the annual mean of month-end levels **rounded up to two decimals**, and for
  the current year the mean of the **first nine months**; for **2009 to 2013** the regulation **fixes the means by statute at
  3.81, 3.13, 3.15, 2.14 and 1.96 per cent**; the reference rate is the **arithmetic mean over the ten-year period**. **The
  Korridormethode.** The calculation was **newly regulated with effect from 23 October 2018**, published in BGBl. I of **22
  October 2018**: the current year's rate must lie **within a corridor around the previous year's**, limiting the annual change
  **in both directions**; the reform touched **only the reference rate**, not the ZZR calculation. **The 2018 counterfactual,
  corroborated twice**: under the old method the rate would have fallen from **2.21 % (2017)** to about **1.9 % in 2018**; under
  the corridor it fell only to **2.10 %**, worth **about ten billion euros of relief industry-wide for 2018**. The rate was
  **1.57 % at 31 December 2022 and 1.57 % in 2025**, reportedly **unchanged since 2021** — pinned flat for five years while
  market swap rates moved sharply. BaFin's *Auslegungsentscheidung* **Projektion des Referenzzinses gemäß § 5 Abs. 3 DeckRV**
  tells undertakings how to project it, which is what makes a multi-year ZZR projection auditable [R21]. **The ZZR in quantum**,
  all trade press and rating-agency reporting, **never a supervisory source**: the stock was about **€84 bn at the 2024
  balance-sheet date**, down from a **€96 bn peak at end-2021**; about **€8.5 bn was added in 2021**; **2022 and 2023** each saw
  reductions of **more than €3 bn**; **2024 was the first year since introduction in which insurers had to add nothing at all**,
  with about **€5 bn flowing back industry-wide** and releases among the **fifty largest summing to about €3.4 bn**; for
  **2025** a further **€4 bn** reduction, with capacity to release **around €5 bn a year in 2025 and 2026**. **The released
  funds reach policyholders through a higher *Überschussbeteiligung***, which is the mechanical link to the declared rates in
  [R53] and why German declarations have risen since 2023 although the reference rate is pinned. An earlier projection had the
  ZZR rising to **€225 bn**; that path was made obsolete by the 2022 rate rise and the corridor, and is recorded only so a
  reader can date it.
- Not established: **the width of the corridor** — no search gave the percentage-point or relative bound, and **any delib
  statement of it is `[unverified]`**; it is the single most important missing figure in the prudential layer. Whether the ZZR
  uses the same fifteen-year look-forward as MindZV § 12 [R18] was **not established** and the two must not be conflated; the
  rest of § 5 beyond Absatz 3 was not read. The **€5 bn and €3.4 bn 2024 figures are different cuts** (industry vs the fifty
  largest) that no source reconciles, as are the €4 bn realised and €5 bn capacity figures for 2025. Every ZZR figure quoted
  from this entry in a delib document is attributed to the trade press; the BaFin *Erstversicherungsstatistik* [R53] would carry
  the audited aggregate.
- Read in the 2026-08-30 pass — **the corridor is not a corridor, and this entry described it too
  loosely.** § 5 Abs. 3 builds the *Referenzzins* from the Bundesbank's month-end ten-year zero-coupon euro swap rates published under
  § 7 RückAbzinsV: the annual mean for each of the nine preceding calendar years, rounded up to two decimals, **with 2009 to 2013
  fixed by the regulation at 3,81, 3,13, 3,15, 2,14 und 1,96 Prozent**; the mean of the first nine months for the current year; and
  their sum divided by ten. Then **two** differences are formed, each rounded up: (1) that ten-year mean less last year's
  *Referenzzins*, and (2) **9 per cent of the current-year mean less 9 per cent of last year's *Referenzzins***. Satz 7: *"Haben die
  Differenzen aus Satz 6 Nummer 1 und 2 das gleiche Vorzeichen, ergibt sich der Referenzzins des Kalenderjahres dadurch, dass der
  Referenzzins des vorherigen Kalenderjahres um die Differenz, die den kleineren Absolutbetrag hat, angepasst wird."* Satz 8:
  *"Andernfalls bleibt der Referenzzins gegenüber dem vorherigen Kalenderjahr unverändert."* Satz 9: *"Der Referenzzins des
  Kalenderjahres 2017 beträgt 2,21 Prozent."* — **so the 2.21 % anchor is statutory, and the rate can stand still for years when the
  two signals disagree in sign.** § 5 Abs. 4 is the ZZR test itself, comparing the *Referenzzins* with *"dem höchsten in den nächsten
  15 Jahren für einen Vertrag maßgeblichen Rechnungszins"*; § 5a dates the corridor version from the financial year beginning after
  31 December 2017, i.e. the version in force from **23 October 2018**. § 5 Abs. 1 also supplies the prudence rule quoted at [R47]:
  *"Die Ableitung von Rechnungsgrundlagen auf der Basis eines besten Schätzwertes genügt nicht."*
- Products: KLV, RV, BAS, RIE, SOF, IDX load-bearing; BU and PFL qualified (annuities in payment carry a tariff rate and
  therefore a ZZR); RLV and FRV background. **Cited-not-specified: no delib model builds a ZZR.**

---

## 4. Prudential — the surplus regulations, the LVRG and the supervisor

### R18. MindZV — the minimum allocation to the RfB, and §§ 11–13
- Publisher: Bundesamt für Justiz; mirrors at `buzer.de`, `lxgesetze.de`, `freirecht.de`, `anwalt.de`, `gesetze.legal`,
  `de.wikipedia.org`. Doc type: Rechtsverordnung of **18 April 2016**, made under § 145 VAG [R10].
- URL: https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html ; `.../__4.html` ; `.../__6.html` ; `.../__11.html` ;
  https://www.buzer.de/gesetz/12013/a198221.htm ; https://lxgesetze.de/mindzv/11 ; https://freirecht.de/g/MindZV:11 (all
  returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688**, read
  **2026-08-30**; §§ 4, 6, 7, 8, 11, 12 and 13 read in full. The `BJNR083100016.html` index page serves (53 kB), as do
  `buzer.de/gesetz/12013/a198221.htm`, `lxgesetze.de/mindzv/11` and `freirecht.de/g/MindZV:11`.
- Content: *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung* — the arithmetic floor under the German
  *Überschussbeteiligung*, applying to life insurers **except Pensionskassen**, which have their own § 5. **The three result
  sources and their minimum shares.** **§ 6 *Kapitalanlageergebnis* — 90 %**: the minimum allocation from investment income for
  profit-participating contracts is **90 per cent of the Kapitalerträge to be credited under § 3 Abs. 1, less the
  Rechnungszinsen**, without reducing the externally financed provision component under § 3 Abs. 7 Satz 5 and without pro-rata
  interest on *Pensionsrückstellungen*. **The subtraction of the *Rechnungszinsen* is the crucial detail: the guarantee is
  funded first, and only the excess is shared 90/10.** **§ 7 *Risikoergebnis* — 90 %**, raised from 75 % by the LVRG with effect
  from **7 August 2014** [R20]. **§ 8 *Übriges Ergebnis* — 50 %**, the cost result. **§ 4 — assembly.** From the sum under § 6
  Abs. 1, § 7 and § 8 the ***Direktgutschrift*** attributable to profit-participating contracts is **deducted**, including
  *Schlusszahlungen* from *Bewertungsreserven* distributed as a direct credit; **Alt- and Neubestand are treated separately
  throughout** [R11]; and **a mathematically negative minimum allocation is replaced by zero**. Those two rules make the MindZV
  a **minimum transfer to the RfB, not a minimum payout**. **§§ 11–13 — the Sicherungsbedarf machinery** behind § 139 Abs. 3/4
  VAG [R9]. **§ 11**: the reference rate is the **zero-coupon Euro interest-rate swap rate published by the Deutsche Bundesbank
  under § 7 der Rückstellungsabzinsungsverordnung, at ten years, at the end of the month preceding the date on which the
  Bewertungsreserven are determined**. **Note the difference from the ZZR rate** [R17]: the ZZR uses a **ten-year average**
  damped by the corridor, the *Sicherungsbedarf* a **single month-end spot** rate. **They are different numbers from the same
  Bundesbank series, and confusing them is one of the standard errors in describing a German life balance sheet.** **§ 12**: the
  § 11 rate is compared with **the highest Rechnungszins applicable to the contract over the next fifteen years**, and where it
  is lower the contract generates a *Sicherungsbedarf*, locking that much of the fixed-income valuation reserves away from
  departing policyholders. The fifteen-year window is why the test bites hardest on annuity business: a deferred annuity
  guaranteeing 3.25 % in the *Rentenphase* keeps generating a *Sicherungsbedarf* long after a comparable endowment has matured.
  **Why this is the centre of the delib library.** Six of the ten products are profit-participating general-account contracts
  whose credited return is the guarantee plus a discretionary share of these three results, so any delib model of the surplus
  chassis represents at least the three result sources, the 90/90/50 floor, the direct-credit-versus-RfB split, and the fact
  that the floor binds on the **HGB** accounts.
- Not established: **§ 7 and § 8 were never returned in their own words** — the 90 % and 50 % come from two consistent summaries
  of § 4 and of the regulation as a whole. **§ 3's definition of the *zuzurechnende Kapitalerträge* — the base the 90 % bites on
  — was not established, and it is the number that actually matters for a projection.** § 2 (definitions, including
  *Direktgutschrift*) was not retrieved; whether the 50 % applies symmetrically to a negative cost result was not established.
  **§ 13 was not retrieved** and is `[unverified]`; the **valuation formula in § 12** was not returned; the
  *Rückstellungsabzinsungsverordnung* was not researched beyond the cross-reference.
- Read in the 2026-08-30 pass — **the 90 / 90 / 50 split, the assembly rule and the § 13 cap are all
  first-hand.** § 6 Abs. 1: *"90 Prozent der nach § 3 Absatz 1 anzurechnenden Kapitalerträge abzüglich der rechnungsmäßigen Zinsen"*,
  with two asymmetries this entry did not carry — a contractual share above 90 per cent **raises** the minimum (Satz 4), and where the
  creditable investment income falls short of the *rechnungsmäßige Zinsen* the minimum is **100 per cent** of the shortfall rather
  than zero (Sätze 5–6). § 7: 90 per cent of the *Risikoergebnis*; § 8: 50 per cent of the *übriges Ergebnis*; both floored at zero
  and computed separately for *Alt-* and *Neubestand*. § 4 Abs. 1 defines the three sources **by named lines and columns of
  *Nachweisung 213* of the BerVersV** and Abs. 2 deducts the *Direktgutschrift* and replaces a negative result by zero. § 11 confirms
  the *Bezugszins* as the ten-year zero-coupon euro swap rate *"am Ende desjenigen Monats ..., der dem Zeitpunkt der Ermittlung der
  Bewertungsreserven vorangeht"* — a **single month-end spot**, materially different from the ZZR's damped ten-year average [R17];
  § 12 confirms the fifteen-year comparison. **§ 13 is the cap on the *ungebundener Teil*, and it lives here, not in the RfBV**:
  the sum of the § 28 Abs. 8 Nr. 2 Buchst. h RechVersV *ungebundener Teil* and any part already fixed beyond the following year may
  not exceed **0,8 × SP + 2 × (FR + DG) + Max{0; (1 − DNZ / 0,05) × SP}**, with SP the KapAusstV capital requirement, FR next year's
  fixed declared shares, DG next year's expected *Direktgutschrift* and DNZ the three-year average net investment return.
- Products: KLV, RV, BAS, RIE, IDX, SOF load-bearing; RLV, BU, PFL load-bearing **on the risk result** — the 90 % share of the
  *Risikoergebnis* funds a German term, BU or Pflege tariff's *Beitragsrückerstattung*; FRV qualified [R21].

### R19. RfBV — the collective part of the Rückstellung für Beitragsrückerstattung
- Publisher: Bundesamt für Justiz; `dejure.org` for the BGBl citation; `jurawelt.com`; Bundesrat Drucksache 585/16 as
  background; BaFin for the interpretive decision on *Teilkollektivierung*
- Doc type: Rechtsverordnung, **BGBl. I 2015 S. 300**
- URL: https://www.gesetze-im-internet.de/rfbv/BJNR030000015.html (returned); https://www.gesetze-im-internet.de/rfbv/__3.html
  (returned); https://dejure.org/BGBl/2015/BGBl._I_S._300 (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ae_110419_mindestzufuehrung_rfb_va.html
  (returned)
- Retrieved: **yes** — canonical XML, **Stand: geändert durch Art. 1 V v. 19.7.2017 I 3037**, read
  **2026-08-30**; *Eingangsformel* and §§ 1–5 read in full — the whole regulation.
  `gesetze-im-internet.de/rfbv/BJNR030000015.html` answered with a connection reset and `/rfbv/__3.html` is a 6.7 kB shell, which is
  why the XML is the citable route; `dejure.org/BGBl/2015/BGBl._I_S._300` serves for the citation and BaFin's
  *Teilkollektivierung* interpretive decision was read (HTML, 89 kB).
- Content: implements § 140 Abs. 1 Satz 2 VAG [R10]. It applies to life insurers **except Sterbekassen and regulierte
  Pensionskassen**. **§ 2 — the cap on the *ungebundene* RfB.** On establishing a *kollektiver Teil*, the undertaking must set
  an ***Obergrenze* for the ungebundene Rückstellung für Beitragsrückerstattung of the *Teilbestände*, expressed as a
  percentage**; the percentage is **at least 100**, is **identical for all Teilbestände**, and **may be changed from the prior
  year only with the supervisor's consent**. Where a *Teilbestand*'s *ungebundene* RfB **exceeds** that ceiling and no
  *Rückführungen* into the *Teilbestände* take place at the balance-sheet date, **the excess is transferred to the kollektiver
  Teil**. **§ 3** requires an *Obergrenze* for the collective part itself, as a percentage of an amount. **Why it exists**: the
  collective part lets an insurer hold surplus committed to policyholders as a class but not yet attributed to any
  *Teilbestand*, which is what makes cross-cohort smoothing legally possible without breaching the § 138 Abs. 2 VAG equal
  treatment rule [R8]. BaFin's interpretive decision on the *Zusammenwirken von Mindestzuführung zur RfB und
  Teilkollektivierung* (**19 April 2011**) governs how the MindZV floor interacts with it [R21]. **Vocabulary for delib**: the
  statutory term is *ungebundene* RfB; German market writing says *freie RfB* for the same thing and *gebundene RfB* for the
  part already committed to declared shares and to the *Schlussüberschussanteilfonds* of § 28 RechVersV [R54].
- Not established: **the percentage base in § 3 was not established**; one summary of § 140 VAG describes the ceiling as "a
  percentage of declared profit shares and the expected expenses for declared Direktgutschriften, with a minimum percentage of
  100", which appears to describe **§ 2**, not § 3 — **the two are conflated in the summaries and the conflation is not
  resolved**. § 1 (*Geltungsbereich*) and any further sections were not retrieved. **Whether the German market actually uses the
  collective part, and how large it is, was not established.**
- Read in the 2026-08-30 pass — **the section attribution in this entry was off by one, and the percentage
  bases are now established.** **§ 2 is *Begriffsbestimmungen***; **§ 3 Abs. 2** sets the *Obergrenze* for the *ungebundene* RfB of
  the *Teilbestände* as a percentage **of the declared profit shares fixed for allocation in the following year plus the expected
  following-year cost of the declared *Direktgutschrift***, *"Der Prozentsatz beträgt mindestens 100, ist für alle Teilbestände
  identisch und darf gegenüber dem Vorjahr nur mit Zustimmung der Aufsichtsbehörde geändert werden."*; **§ 3 Abs. 3** sets the ceiling
  on the collective part as a percentage of the KapAusstV amount, *"Der Prozentsatz beträgt höchstens 60"*, with returns to the
  *Teilbestände* distributed by share of *Rohüberschuss* (with or without *Direktgutschrift*), or by another
  *verursachungsorientierter Verteilungsschlüssel* with consent, the same key for all. **The *Eingangsformel* shows the regulation was
  made under § 56b Abs. 2 Satz 2 VAG a.F.**, inserted by Art. 6 Nr. 6 of the Act of 3 April 2013, and it now operates on **§ 140
  Abs. 4 VAG**, not § 140 Abs. 1 Satz 2. § 2 also supplies the *Altbestand* / *Neubestand* / *Teilbestand* definitions [R11].
  **Still `[unverified]`:** whether the German market actually uses the collective part, and how large it is.
- Products: KLV, RV, BAS, RIE, IDX, SOF load-bearing for the surplus chassis; the other four qualified.

### R20. LVRG 2014 — the Lebensversicherungsreformgesetz
- Publisher: Bundesgesetzblatt / `dejure.org` for the citation; Deutscher Bundestag for the Drucksache and the plenary record;
  Gabler and Haufe for the summaries; DIA/ITA for the impact study
- Doc type: federal statute, **BGBl. I 2014 S. 1330**, of **1 August 2014**; Gesetzentwurf **BT-Drs. 18/1772** of 18 June 2014
- URL: https://dejure.org/BGBl/2014/BGBl._I_S._1330 (returned); https://dserver.bundestag.de/btd/18/017/1801772.pdf (returned);
  https://www.haufe.de/steuern/gesetzgebung-politik/aenderungen-im-ueberblick-das-neue-lebensversicherungsreformgesetz_168_265064.html
  (returned); https://wirtschaftslexikon.gabler.de/definition/lebensversicherungsreformgesetz-54407 (returned);
  https://www.dia-vorsorge.de/wp-content/uploads/2019/07/150519_DIA_Studie_final_LVRG.pdf (returned)
- Retrieved: **partly.** The **BGBl citation record** at `dejure.org/BGBl/2014/BGBl._I_S._1330` was read (HTML, 46 kB) and
  the **government bill BT-Drs. 18/1772 of 18.06.2014** at `dserver.bundestag.de/btd/18/017/1801772.pdf` was read (PDF, 40 pp.), both
  **2026-08-30**; the Haufe, Gabler and DIA commentaries also serve. **The Act's own *Regelungstext* was not retrieved** — dejure
  serves the citation record, and the consolidated statutes carry the result without naming the amending article.
- Content: *Gesetz zur Absicherung stabiler und fairer Leistungen für Lebensversicherte* — the reform that reshaped the German
  *Überschussbeteiligung* for the low-rate era. Three of its changes are load-bearing for delib. **(1) Bewertungsreserven
  restricted**: the distribution restriction applies **only to valuation reserves from festverzinsliche Wertpapiere**, and
  participation by departing policyholders is limited where an insurer's provisions are, at prevailing low rates, insufficient
  to fund the guarantees given to remaining policyholders — this is the *Sicherungsbedarf* test now in § 139 Abs. 3/4 VAG [R9]
  and MindZV §§ 11–12 [R18]. **(2) *Höchstzillmersatz* cut from 40 ‰ to 25 ‰** of the *Beitragssumme*, effective **1 January
  2015** [R16]. **(3) *Risikoüberschuss* share raised from 75 % to 90 %**, effective **7 August 2014**, now § 7 MindZV [R18] —
  the single change that most affects delib's biometric products, since a German term, BU or Pflege tariff's surplus is
  predominantly a risk surplus. Alongside them, **distributions to shareholders may be prohibited** where needed to secure the
  guaranteed benefits (an *Ausschüttungssperre*). The constitutionality of the LVRG's insertion into **§ 153 Abs. 3 Satz 3 VVG**
  was litigated and upheld [R36].
- Not established: the LVRG amended the **old** VAG (§ 56a a.F. and others) and **the mapping from those old sections onto the
  2016 VAG sections was not established**; delib cites the current sections and describes the LVRG as the reform that introduced
  the rules, not as the current legal source. Whether the LVRG also introduced a commission cap (*Provisionsdeckel*) — trade
  press in the results discusses one as a later, separate proposal — was **not established and is not asserted**.
- Read in the 2026-08-30 pass. The citation record gives *"Bundesgesetzblatt Jahrgang 2014 Teil I Nr. 38,
  ausgegeben am 06.08.2014, Seite 1330"* for the *"Gesetz zur Absicherung stabiler und fairer Leistungen für Lebensversicherte
  (Lebensversicherungsreformgesetz – LVRG) vom 01.08.2014"*. The bill states the three changes in its own words:
  *"insbesondere müssen die Versicherten künftig mit mindestens 90 Prozent (statt wie bislang 75 Prozent) an den Risikoüberschüssen
  beteiligt werden"*; *"Der Höchstzillmersatz für die bilanzielle Anrechnung von Abschlusskosten wird gesenkt"*; and
  *"Die Regelungen zur Beteiligung an den Bewertungsreserven werden dahingehend angepasst, dass die Ausschüttung von
  Bewertungsreserven an die ausscheidenden Versicherten begrenzt wird"*, its draft § 56a VAG a.F. text being word for word what
  § 139 Abs. 3 VAG now says. **The 7 August 2014 entry into force is confirmed from a different source in this pass** — the BGH press
  release on IV ZR 201/17 says *"in der Fassung des Lebensversicherungsreformgesetzes vom 1. August 2014, in Kraft getreten am
  7. August 2014"* [R36]. **Still `[unverified]`:** the 1 January 2015 date for the *Höchstzillmersatz*, the numeric 40 ‰ → 25 ‰ step
  (the bill says only that the rate is lowered), the mapping from the old VAG sections onto the 2016 VAG, and any *Provisionsdeckel*
  — the bill's summary mentions none.
- Products: all ten; most materially RLV, BU and PFL (the 90 % risk-result share) and KLV, RV, BAS, RIE (the
  *Bewertungsreserven* restriction and the Zillmerung cut).

### R21. BaFin — the FinDAG, the MaGo and the Auslegungsentscheidungen
- Publisher: Bundesamt für Justiz for the FinDAG; BaFin for the circulars, interpretive decisions and topic pages; Gabler, KPMG,
  Wavestone and Fincon as secondary. Doc type: federal statute; supervisory circular; a cluster of *Auslegungsentscheidungen*.
- URL: https://www.gesetze-im-internet.de/findag/BJNR131010002.html ;
  https://www.bafin.de/DE/die-bafin/ueber-die-bafin/aufgaben/versicherungsaufsicht/versicherungsaufsicht_node.html ;
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/EN/Rundschreiben/2017/rs_1702_mago_va_en.html ;
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Konsultation/2025/kon_05_2025_konsultation_ueberarbeitung_mago_va.html
  ; and the interpretive decisions at https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ under
  the slugs `ae_151204_wechselwirkung_ueberschussbeteiligung_neugeschaeft_va`, `ae_160610_beteiligung_an_bewertungsreserven`,
  `ae_091222_mzffglv_va`, `ae_110419_mindestzufuehrung_rfb_va`, `ae_161111_kapitalmarktmodelle_va`,
  `ae_160222_latente_steuern_auf_versicherungstechnische_rueckstellungen` (all returned)
- Retrieved: **partly.** The **FinDAG** (HTML, 265 kB), BaFin's **Auslegungsentscheidung index** (156 kB), the
  ***Zusammenwirken von Mindestzuführung zur RfB und Teilkollektivierung*** decision (89 kB), the ***Projektion des Referenzzinses
  gemäß § 5 Abs. 3 DeckRV*** decision (82 kB), the **MaGo consultation 05/2025** page (89 kB) and BaFin's *Versicherungsaufsicht*
  overview (93 kB) were all read **2026-08-30**. **The MaGo circular itself was not opened** — the English page cited here returns
  HTTP 404 — and **six of the eight Auslegungsentscheidungen were not opened individually.**
- Content: **The institution.** BaFin was created in **2002** by the *Finanzdienstleistungsaufsichtsgesetz of 22 May 2002*,
  merging the three predecessor *Bundesaufsichtsämter* into a single *Allfinanzaufsicht*; the merger was organisational and
  **created no new competences**. BaFin is under the *Rechts- und Fachaufsicht* of the Bundesministerium der Finanzen (§ 2
  FinDAG) and supervises under the KWG, the VAG and the WpHG. **The objective** is to ensure the **permanent fulfilment
  capability of insurance contracts** — the *dauernde Erfüllbarkeit* standard that also appears in § 341e HGB [R54] and § 138
  Abs. 1 VAG [R8] — with the protection of the insured; supervision splits into *Finanzaufsicht/Solvenzaufsicht*,
  *Rechtsaufsicht* and, in German usage, *Missstandsaufsicht*. **The MaGo.** *Rundschreiben 2/2017 (VA) — Mindestanforderungen
  an die Geschäftsorganisation von Versicherungsunternehmen* was **published 25 January 2017, in force 1 February 2017**. It
  **interprets the business-organisation provisions of the VAG and of Delegated Regulation (EU) 2015/35 and binds BaFin's own
  application of them**, covering *Aufbauorganisation*, internal guidelines, the Solvency II *Schlüsselfunktionen*, risk
  management, undertaking-specific stress tests and *Ausgliederung*. A **revised version was published 14 July 2025** after
  **Konsultation 05/2025** (opened 29 January 2025), its **Chapter 8** specifying group requirements. For delib the MaGo is why
  the ***versicherungsmathematische Funktion*** exists alongside the § 141 VAG *Verantwortlicher Aktuar* [R11] — **two distinct
  actuarial roles, which delib does not conflate.** **The Auslegungsentscheidungen** are BaFin's published statements of how it
  will apply a provision: not law, but binding on BaFin's own practice and carrying much of the operative detail the regulations
  leave open. Established, each from one or two sentences: (1) ***Wechselwirkungen zwischen Überschussbeteiligung und
  Neugeschäft*** (4 December 2015) — German life and health insurance is characterised by **collective mechanisms**, so new
  business can affect the existing portfolio's future *Überschussbeteiligung*. (2) ***Ausweis der Beteiligung an den
  Bewertungsreserven in der Standmitteilung*** (10 June 2016) — the annual statement must disclose the **full** allocation;
  showing only a guaranteed *Sockelbeteiligung* **is not sufficient**, because the policyholder could not otherwise obtain
  clarity as § 155 Satz 1 VVG requires [R25]. (3) ***Mindestzuführung in der fondsgebundenen Lebensversicherung*** (22 December
  2009) — **load-bearing for FRV**, whose investment result belongs to the policyholder and whose MindZV base is therefore not
  the general account's. (4) ***Zusammenwirken von Mindestzuführung zur RfB und Teilkollektivierung*** (19 April 2011) [R19].
  (5) ***Auswirkung von passiver Rückversicherung auf die Angemessenheit der Zuführung zur RfB*** — treaty design affects the
  minimum allocation but **must not inappropriately reduce policyholders' Überschussbeteiligung**. (6) ***Anforderungen an
  Kapitalmarktmodelle*** (11 November 2016) — calibration must be consistent with the risk-free curve used for the best estimate
  under **Art. 77(2) of Directive 2009/138/EC** [R1]. (7) ***Latente Steuern auf versicherungstechnische Rückstellungen*** (22
  February 2016). (8) ***Projektion des Referenzzinses gemäß § 5 Abs. 3 DeckRV*** [R17].
- Not established: **none of these documents was read.** Each is one or two sentences of summary; the operative wording,
  thresholds and worked examples are unknown, which makes the interpretive decisions **the weakest-evidenced supervisory
  material in this file relative to their importance**. The date of item (5) and a 2020 decision the summaries mention were not
  established, nor whether any has been withdrawn. The four Solvency II **Schlüsselfunktionen** are named only generically;
  their individual names and VAG sections were **not established**. Whether the 2025 MaGo revision is in force, or applies from
  a stated date, was not established.
- Read in the 2026-08-30 pass. The supervisory objective is now quoted from the statute rather than from
  BaFin's own pages: **§ 294 Abs. 1 VAG** makes the *Hauptziel* the protection of policyholders and beneficiaries and **§ 294 Abs. 4**
  puts the *dauernde Erfüllbarkeit* at the centre of the *Finanzaufsicht* [R5]. **Still `[unverified]`:** the MaGo's publication and
  in-force dates of 25 January and 1 February 2017 and the 14 July 2025 revision; and the content of the six unopened interpretive
  decisions, whose captions are kept as known references.
- Products: FRV load-bearing (item 3); KLV, RV, BAS, RIE, IDX, SOF for items 1, 2, 4, 5; all ten for the institutional context
  and items 6 and 7.

---

## 5. Contract law — the Versicherungsvertragsgesetz

German life contract law is a single statute whose **Kapitel 5 (§§ 150–171) is *halbzwingend***: §§ 152 Abs. 1 and 2, 153 to
155, 157, 158, 161 and 163 to 170 may not be varied to the policyholder's detriment (§ 171 VVG). That one sentence is why a
delib model may treat the surrender-value floor, the paid-up right, the suicide clause and the profit-participation entitlement
as **contractual facts rather than insurer choices**, and why the discretionary layer sits only where the statute leaves room.
This block carries the strongest search corroboration in the library: roughly 45 German-language queries, with six to ten
independent publishers returning each of §§ 8, 152, 153, 154, 155, 161, 163, 165, 168, 169, 171 and 172.

### R22. VVG 2008 — the statute, Kapitel 5 and § 171 (halbzwingende Vorschriften)
- Publisher: Bundesministerium der Justiz / Bundesamt für Justiz; mirrors at `dejure.org`, `buzer.de`, `lexetius.com`,
  `rewis.io`, `juraforum.de`, `lxgesetze.de`, `sozialgesetzbuch-sgb.de`. Doc type: federal statute of **23 November 2007**, in
  force from 1 January 2008.
- URL: https://www.gesetze-im-internet.de/vvg_2008/BJNR263110007.html (returned);
  https://www.gesetze-im-internet.de/vvg_2008/__170.html and `__171.html` (returned)
- Retrieved: **yes** — canonical XML, **VVG 2008, ausgefertigt 23. November 2007, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; §§ 170 and 171 read in full, and the whole of Kapitel 5 and
  Kapitel 6 across [R23]–[R29]. The `BJNR263110007.html` index page serves (421 kB) and `vvg_2008/anlage.html` serves (41 kB);
  `vvg_2008/__170.html` answered with a connection reset and most other per-section pages are 4–6 kB frameset shells, which is why
  the XML is the citable route throughout this block.
- Content: the VVG 2008 replaced the VVG of 1908 with effect from 1 January 2008. Structure, as confirmed repeatedly: **Teil 1**
  general provisions (§§ 1–73, including the advice and information duties §§ 6, 7, 7a–7d, the withdrawal right § 8,
  pre-contractual disclosure §§ 19–22, premium default §§ 33, 37, 38 and the intermediary rules §§ 59–68); **Teil 2** the
  individual branches, of which **Kapitel 5 Lebensversicherung** runs §§ 150–171 and **Kapitel 6
  Berufsunfähigkeitsversicherung** §§ 172–177; **Teil 3** final provisions including § 214. A *single* statute therefore
  supplies the death-cover rules, the savings-contract rules and the disability-income rules, and **§ 176 imports §§ 150–170
  into the BU chapter *entsprechend*** [R29]. **§ 171 Satz 1**, as read from the statute on 2026-08-30 — the
  summary version this entry carried gave "§ 152 Abs. 1 und 2": *"Von § 152 Absatz 1 **bis 4** und den §§ 153 bis 155, 157, 158, 161
  und 163 bis 170 kann nicht zum Nachteil des Versicherungsnehmers, der versicherten Person oder des Eintrittsberechtigten abgewichen
  werden."*, with Satz 2 permitting the Schrift- or Textform to be agreed for a § 165 conversion request and a § 168 termination.
  A *halbzwingende* provision may be varied in the policyholder's favour; a variation to their detriment is not void as such, but
  **the insurer may not rely on it**. Note what is **not** in the list: §§ 150, 151, 156, 159, 160, 162, **§ 152 Abs. 5** and § 171
  itself — so beneficiary designation, the consent rule and the first premium's due date are freely variable. **§ 170
  *Eintrittsrecht***: where the claim is attached or insolvency is opened over the policyholder's assets, the **namentlich
  bezeichnete Bezugsberechtigte** may, with the policyholder's consent, step into the contract, satisfying the executing
  creditors or the estate **up to the amount the policyholder could have demanded on termination**, i.e. up to the
  *Rückkaufswert*; where no beneficiary is named, the right belongs to the spouse or civil partner and children; the declaration
  may be made **only within one month**. **Two chapters have no VVG home at all, and this matters for delib**: there is no
  statutory chapter for *Pflegerentenversicherung* (reached, if at all, through § 177 Abs. 1, which is contested — [R29], [R36])
  and none for *indexgebundene* Rentenversicherung, which in law is a *fondsgebundene* or *klassische* contract with the index
  participation living entirely inside the *Überschussbeteiligung* of § 153 [R24].
- Not established: no consolidated-version date was confirmed; the "last amended by" line is **not established**. The **VVG
  a.F.** numbering — § 5a (Policenmodell), § 172 Abs. 2 (Bedingungsanpassung) and § 176 Abs. 3/4 (Rückkaufswert, Stornoabzug),
  all of which appear in the case law [R36] — was confirmed only through case-law summaries, not from a text. **§ 156 VVG was
  never searched.** Whether the § 170 one-month period is an *Ausschlussfrist* was not stated; the § 170 Absatz numbering is
  `[unverified]`.
- Read in the 2026-08-30 pass — **§ 171 was misquoted and is now exact.** *"Von § 152 Absatz 1 **bis 4** und
  den §§ 153 bis 155, 157, 158, 161 und 163 bis 170 kann nicht zum Nachteil des Versicherungsnehmers, **der versicherten Person oder
  des Eintrittsberechtigten** abgewichen werden. Für das Verlangen des Versicherungsnehmers auf Umwandlung nach § 165 und für seine
  Kündigung nach § 168 kann die Schrift- oder die Textform vereinbart werden."* The earlier version read "§ 152 Abs. 1 und 2" and
  named only the policyholder. What is **not** listed: §§ 150, 151, 156, 159, 160, 162 and **§ 152 Abs. 5**. § 170 confirms the
  *Eintrittsrecht*, the creditor-satisfaction ceiling at the termination value, the spouse/children fallback and the **one-month**
  notice running from knowledge of the attachment or the opening of insolvency. § 176 imports §§ 150–170 into the BU chapter
  *"soweit die Besonderheiten dieser Versicherung nicht entgegenstehen"*. **§ 160 exists and is now read** [R26]; **§ 156 was still
  not opened.**
- Products: all ten.

### R23. VVG §§ 8 and 152 — the 14-day and 30-day Widerrufsrechte
- Publisher: Bundesamt für Justiz; mirrors at `juraforum.de`, `buzer.de`, `rewis.io`, `lxgesetze.de`, `datenbank.nwb.de`,
  `haufe.de`, `dejure.org`, `freirecht.de`, `sozialgesetzbuch-sgb.de`, `gesetze-in-app.de`, `deutsche-versicherungsboerse.de`.
  Doc type: statutory sections plus the statutory *Anlage* (Muster für die Widerrufsbelehrung).
- URL: https://www.gesetze-im-internet.de/vvg_2008/__8.html (returned); https://www.gesetze-im-internet.de/vvg_2008/anlage.html
  (returned); https://www.gesetze-im-internet.de/vvg_2008/__152.html (returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; §§ 8 and 152 read in full. `vvg_2008/__8.html` serves in full
  (8.7 kB); `vvg_2008/__152.html` is a 5.8 kB shell.
- Content: **§ 8** — the policyholder may withdraw within **14 days**, in *Textform*, without reasons, and **timely dispatch
  suffices**. The period begins on conclusion but **does not begin** before the policyholder has received, in Textform, the
  *Versicherungsschein*, the contract terms including the AVB, and the information required by the VVG-InfoV [R31]. A summary
  reported the general cut-off as *"Das Widerrufsrecht erlischt spätestens zwölf Monate und 14 Tage nach dem Vertragsschluss"*.
  The **Anlage** is a statutory safe-harbour model whose blocks a summary reported as: the 14-day/no-reasons/Textform statement;
  the start-of-period block listing the *Versicherungsschein*, the AVB with *Tarifbestimmungen*, the *Widerrufsbelehrung*, the
  *Informationsblatt zu Versicherungsprodukten* and the further information of Abschnitt 2; the legal-consequences block; and a
  **30-day repayment deadline**. **§ 152 makes three deviations for life insurance**, each expressed as an *abweichend von*
  clause. **Abs. 1**: the period is **30 days**, and the right **lapses at the latest 24 months and 30 days after conclusion**.
  **Abs. 2**: where the withdrawal is effective the insurer owes the ***Rückkaufswert einschließlich der Überschussanteile nach
  § 169***; in the § 9 Satz 2 case it owes that or, if more favourable, **the premiums paid for the first year**. **Abs. 3**:
  the single or first premium falls due **immediately after the expiry of 30 days from receipt of the Versicherungsschein**.
  This is the single most model-relevant conduct rule in the German life chapter: **a withdrawal exercised after cover has begun
  is settled at the surrender value, not at premiums-paid**, so the § 169 floor [R28] reaches into the withdrawal window. For
  delib it fixes a **first-duration decrement legally distinct from lapse**: a withdrawal unwinds the contract, a surrender pays
  a *Rückkaufswert*, and a model that lumps the two into one lapse rate loses the distinction and should say so.
- Not established: **the Absatz structure of § 8 is partly contradictory across summaries** — the Muster is at Abs. 4 Satz 1
  (reliable, from the Anlage's own title), one summary puts the twelve-month long stop at Abs. 4 Satz 2, a third describes Abs.
  3 as the no-withdrawal list and Abs. 5 as the *Verordnungsermächtigung*; **the Absatz-to-rule mapping inside § 8 is
  `[unverified]`** while the substantive rules are corroborated. The content of **§ 9 VVG (Rückabwicklung)** was never searched.
  The *Fernabsatz* interaction is **not established**.
- Read in the 2026-08-30 pass — **the Absatz mapping inside § 152 was wrong.** **Abs. 2** applies where
  cover began before the end of the period **and** the § 9 Abs. 2 Satz 1 Nr. 1 condition is met: the insurer owes the premium part
  after receipt of the withdrawal **and** *"den Rückkaufswert einschließlich der Überschussanteile nach § 169"*. **Abs. 3 is the case
  where that condition is not met** — same premium part, plus the § 169 value *"oder, wenn dies für den Versicherungsnehmer günstiger
  ist, die für das erste Jahr gezahlten Prämien"*. **The due-date rule is Abs. 5**, not Abs. 3. Abs. 1 confirms the 30 days and the
  24-months-and-30-days long-stop; Abs. 4 disapplies § 9 Abs. 2 bis 4. § 8 Abs. 4 Satz 2 confirms *"zwölf Monate und 14 Tage nach dem
  Vertragsschluss"* **and Satz 3 disapplies it where the policyholder was never instructed** — the statutory root of the
  *Widerrufsjoker* [R36]. § 8 Abs. 2 adds that the period does not start before a PRIIPs or PEPP *Basisinformationsblatt* has been
  provided and puts the burden of proving receipt on the insurer. **Still `[unverified]`:** § 9 VVG, whose Abs. 2 Satz 1 Nr. 1
  condition switches between § 152 Abs. 2 and Abs. 3, was not opened.
- Products: all ten.

### R24. VVG § 153 — Überschussbeteiligung and the hälftige Beteiligung an den Bewertungsreserven
- Publisher: Bundesamt für Justiz; mirrors at `dejure.org`, `buzer.de`, `rewis.io`, `lxgesetze.de`, `juraforum.de`,
  `anwalt24.de`, `gesatz.de`, `sozialgesetzbuch-sgb.de`, `gesetze-in-app.de`. Doc type: statutory section.
- URL: https://www.gesetze-im-internet.de/vvg_2008/__153.html `[unverified canonical form]`;
  https://dejure.org/gesetze/VVG/153.html (returned); https://www.buzer.de/153_VVG.htm (returned);
  https://rewis.io/gesetze/vvg/p/153-vvg/ (returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; § 153 read in full. `dejure.org/gesetze/VVG/153.html`,
  `buzer.de/153_VVG.htm` and `rewis.io/gesetze/vvg/p/153-vvg/` also serve; `vvg_2008/__153.html` is a 4.9 kB shell.
- Content: the article the whole KLV/RV/IDX chassis hangs on. **(1) The entitlement.** The policyholder has a **right** to
  participate in the *Überschuss* and in the *Bewertungsreserven* **unless participation is excluded by express agreement**, and
  such an exclusion **can only be made for the whole of the profit participation** — there is no partial opt-out. This is the
  German counterpart to the French *participation aux bénéfices*, but it is an **individual contractual entitlement with a
  statutory default**, not a collective minimum computed from a regulated account. **(2) The method.** The insurer must operate
  the participation by a ***verursachungsorientiertes Verfahren***, or by *"andere vergleichbare angemessene
  Verteilungsgrundsätze"*. The statute names the principle and **does not prescribe the algorithm**, which is precisely why the
  three surplus sources (*Zinsüberschuss*, *Risikoüberschuss*, *Kostenüberschuss*) and their declared rates are
  insurer-discretionary inputs and every level in delib is `**[std]**` unless a *Tarifblatt* supplies it. The BGH tied this
  Absatz to § 138 Abs. 2 VAG in **IV ZR 436/22 of 18 September 2024** [R8]. **(3) Bewertungsreserven.** The insurer must
  **recompute them annually** and allocate them by a cause-oriented method; **on termination of the contract, half of the amount
  then determined is allocated and paid to the policyholder**, and earlier allocation may be agreed. **(4) The LVRG override.**
  § 153 Abs. 3 Satz 3, in the version given by the LVRG of 1 August 2014 in force 7 August 2014 [R20], preserves the supervisory
  rules securing permanent fulfilment — a summary named **§§ 89, 124 Abs. 1, § 139 Abs. 3 und 4, §§ 140 and 214 VAG** — with the
  effect that **Bewertungsreserven from fixed-interest securities and interest-rate hedging instruments count toward the
  policyholder's share only to the extent that they exceed a *Sicherungsbedarf*** [R9][R18]. In a low-rate environment this
  reduced the payable half to zero for many portfolios, and the BGH held the rule constitutional [R36]. **For delib**: the
  *Bewertungsreserven* leg is path- and balance-sheet-dependent in a way a gross liability cash flow model cannot reproduce, so
  the reference implementations model the declared *laufende Überschussbeteiligung* and the *Schlussüberschussanteil* explicitly
  and treat the *Bewertungsreserven* share as an explicitly excluded component, saying so.
- Not established: the **Absatz/Satz numbering** of the entitlement (Abs. 1) and the method (Abs. 2) was inferred from the
  ordering in the summaries and from the BGH's citation of "§ 153 Abs. 3 Satz 3"; **the Abs. 1 and Abs. 2 attributions are
  `[unverified]`**. The VAG cross-references in Satz 3 come from a **single summary** and are `[unverified]` as a list.
- Read in the 2026-08-30 pass — **the Abs. 1 / Abs. 2 attributions are confirmed, the Satz 3 cross-reference
  list is established, and Abs. 4 is new to this library.** Abs. 3 Satz 3 in the version now in force reserves *"die §§ 89, 124
  Absatz 1, § 139 Absatz 3 und 4 und die §§ 140 sowie 214 des Versicherungsaufsichtsgesetzes"*. **Abs. 4:** *"Bei
  Rentenversicherungen ist die Beendigung der Ansparphase der nach Absatz 3 Satz 2 maßgebliche Zeitpunkt."* — so for an annuity
  contract the half-share of *Bewertungsreserven* falls due **at the end of the accumulation phase**, which fixes the timing for RV,
  FRV, IDX, BAS and RIE. Abs. 2 Satz 2 also excludes the § 268 Abs. 8 HGB amounts. **Still `[unverified]`:** BGH IV ZR 436/22 of
  18 September 2024, which was not opened.
- Products: KLV, RV, FRV, IDX, BAS, RIE, SOF load-bearing; RLV, BU, PFL qualified.

### R25. VVG §§ 154 and 155 — Modellrechnung and Standmitteilung
- Publisher: Bundesamt für Justiz; mirrors at eight and nine hosts respectively; Gabler's *Versicherungslexikon*; a Haufe
  commentary section; BaFin's *Auslegungsentscheidung* [R21]; a Verbraucherzentrale Hamburg *Sonderuntersuchung
  Standmitteilung*. Doc type: statutory sections.
- URL: https://www.gesetze-im-internet.de/vvg_2008/__154.html (returned); https://www.gesetze-im-internet.de/vvg_2008/__155.html
  (returned); https://www.gesetze-im-internet.de/vvg-infov/__2.html (returned, for the three rates)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; §§ 154 and 155 read in full, with **§ 2 VVG-InfoV**
  (canonical XML, Stand: zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156) for the three rates.
  `gesetze-im-internet.de/vvg-infov/__2.html` serves in full (10 kB); the VVG per-section pages are shells.
- Content: **§ 154 *Modellrechnung*.** Where the insurer, in connection with the offer or conclusion of a life contract, makes
  **quantified statements about possible benefits beyond the contractually guaranteed benefits**, it must give the policyholder
  a *Modellrechnung* showing the possible *Ablaufleistung* computed **on the calculation bases used for the premium
  calculation** at **three different interest rates**. The duty does **not** apply to *Risikoversicherungen* nor to contracts
  providing benefits of the kind described in § 124 Abs. 2 Satz 2 VAG. The three rates are set by **§ 2 Abs. 3 VVG-InfoV**,
  quoted by a summary as: *"a) Der Höchstrechnungszinssatz, multipliziert mit 1,67; b) der Zinssatz nach a) zuzüglich eines
  Prozentpunkts und c) der Zinssatz nach a) abzüglich eines Prozentpunkts."* The insurer must state clearly that the
  *Modellrechnung* rests on fictitious assumptions and that **no contractual claim** derives from it. **Arithmetic consequence
  for delib, and it is sharp**: with a *Höchstrechnungszins* of **1.00 %** (new business from 2025, [R15]) the statutory triple
  is **1.67 % / 2.67 % / 0.67 %**. A delib `product-spec.md` reproducing a published *Modellrechnung* reproduces that triple,
  and a technical note projecting an illustrative surplus scenario either uses those rates or says explicitly that it does not
  and why. **§ 155 *Standmitteilung*.** For **profit-participating** insurance the insurer must inform the policyholder
  **annually in Textform** about the **current status of their claims including the profit participation**, and must **disclose
  to what extent that profit participation is guaranteed**. The reported content: the agreed benefit on the insured event plus
  profit participation at the key date; the agreed benefit plus **guaranteed** profit participation at maturity or annuity
  commencement assuming unchanged continuation; and further information on surrender values and premiums paid. A second limb is
  the interesting one: **where the insurer has made statements about the possible future development of the profit
  participation, it must inform the policyholder of deviations of the actual development from those statements** — a direct
  statutory link back to § 154, making the *Modellrechnung* a benchmark the insurer keeps reporting against. For delib this is
  not a cash flow: it is the reason **published Standmitteilung specimens are a legitimate `[S#]` source class** for declared
  surplus rates and for the guaranteed/non-guaranteed split.
- Not established: the current *Höchstrechnungszins* was **not established in the contract sweep** and is carried from [R15].
  The § 124 Abs. 2 Satz 2 VAG carve-out was reported by one summary only and its content is `[unverified]`. The **Satz numbering
  within § 155** is `[unverified]` except for "§ 155 Satz 1", which the BaFin decision cites; whether the *Standmitteilung* must
  show the *Rückkaufswert* as such differed in emphasis between summaries. The date and instrument of the *Jährliche
  Unterrichtung* → *Standmitteilung* rename (almost certainly the LVRG) is **not established**. One query explicitly sought
  published criticism of the 1.67 multiplier at a 1 % ceiling and returned **nothing**; the observation that the multiplier is
  now nearly inert is the compiler's inference, not a sourced claim.
- Read in the 2026-08-30 pass — **the § 124 Abs. 2 Satz 2 VAG carve-out is confirmed and the quotation of the
  three rates is corrected.** § 154 Abs. 1 Satz 2: *"Dies gilt nicht für Risikoversicherungen und Verträge, die Leistungen der in
  § 124 Absatz 2 Satz 2 des Versicherungsaufsichtsgesetzes bezeichneten Art vorsehen."* — **unit-linked and index-linked contracts owe
  no *Modellrechnung***. § 2 Abs. 3 VVG-InfoV in full: *"1. dem Höchstrechnungszinssatz, multipliziert mit 1,67, 2. dem Zinssatz nach
  Nummer 1 zuzüglich eines Prozentpunktes und 3. dem Zinssatz nach Nummer 1 abzüglich eines Prozentpunktes."* — numbered 1./2./3., and
  *Prozentpunktes*, where this entry previously carried a)/b)/c) and *Prozentpunkts*. § 155 now has **three Absätze and a five-item
  list in Abs. 1 Satz 3** — the claim benefit plus profit participation, the maturity benefit plus **guaranteed** profit participation
  on continuation and on a paid-up basis, **the payout on the policyholder's termination**, and **the sum of premiums paid** for
  contracts from 1 July 2018 — so BaFin's 2016 decision citing "§ 155 Satz 1" refers to what is now **§ 155 Abs. 1 Satz 1** [R21].
- Products: KLV, RV, IDX, BAS, RIE load-bearing; FRV, SOF, BU, PFL qualified; not relevant to RLV (a pure *Risikoversicherung*
  is outside § 154).

### R26. VVG §§ 150, 159, 160, 161 and 162 — Einwilligung, Bezugsberechtigung, Selbsttötung
- Publisher: Bundesamt für Justiz; mirrors at `buzer.de`, `lxgesetze.de`, `dejure.org`, `juraforum.de`, `datenbank.nwb.de`,
  `anwalt.de`, `sozialgesetzbuch-sgb.de`, `rechtsportal.de`; a Haufe commentary and a Universität des Saarlandes lecture PDF.
  Doc type: statutory sections.
- URL: https://www.gesetze-im-internet.de/vvg_2008/__150.html `[unverified canonical form]`;
  https://www.gesetze-im-internet.de/vvg_2008/__159.html and `__161.html`, `__162.html` (returned); `__160.html` `[unverified
  canonical form]` — **§ 160 was not returned at all**
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; §§ 150, 159, **160**, 161 and 162 read in full.
  The per-section pages for §§ 150 and 159 are 4.8 kB and 4.0 kB frameset shells.
- Content: **§ 150** — where a policy is taken out **on the death of another person** and the agreed benefit **exceeds the
  amount of ordinary funeral costs** (*gewöhnliche Beerdigungskosten*), the **written consent** of that person is required for
  validity. It does not apply to *betriebliche Altersversorgung*, which delib excludes anyway. Two refinements from the summary:
  where the life assured lacks or has limited legal capacity, or has a *Betreuer* with authority over personal affairs, the
  policyholder **may not represent** them in consenting; and where a parent insures a **minor child**, consent is required
  **only** if the insurer is also to pay on death **before age seven** and the benefit for that case exceeds ordinary funeral
  costs. For delib this is an **issue-rule constraint** rather than a cash flow, and the funeral- cost boundary is what makes
  *Sterbegeldversicherung* a distinct product in German law rather than a small RLV — which is why delib excludes it. **§ 159
  *Bezugsberechtigung*** — the policyholder is, in case of doubt, entitled **without the insurer's consent** to designate a
  third party as beneficiary and to substitute another. The timing rule is what matters: a **widerruflich** designated third
  party acquires the right **only on occurrence of the insured event**; an **unwiderruflich** designated third party acquires it
  **already on designation**. For delib this determines whether the death benefit forms part of the estate (it does not, where a
  beneficiary is designated) and whether the policyholder can still surrender — **an irrevocable designation removes the
  unilateral disposal, so a model point carrying one should not carry a surrender assumption.** **§ 161 *Selbsttötung*** — in
  *Todesfallversicherung* the insurer is **not liable if the insured person intentionally took their own life within three years
  of conclusion of the contract**, unless the act was committed **in a state excluding free determination of the will owing to a
  pathological mental disturbance**. **Abs. 2** allows the three-year period to be **extended by individual agreement**; § 171
  makes shortening in the insurer's favour impossible [R22]. **Abs. 3** — where the insurer is not liable it must nevertheless
  **pay the Rückkaufswert einschließlich der Überschussanteile nach § 169** [R28]. **§ 162** — the insurer is not liable where
  the policyholder intentionally and unlawfully brought about the death of the insured; and a third-party beneficiary's
  **designation is void** if that third party did so. **Model consequence for RLV and the death cover inside KLV**: the first
  three policy years carry a benefit that is the **surrender value rather than the sum assured for the suicide sub-cause of
  death** — a *duration-dependent benefit definition*, not a rate adjustment, and therefore a listed modeling pitfall even in a
  model that does not split the death decrement by cause.
- Not established: the statute uses the undefined standard *gewöhnliche Beerdigungskosten* and **no search result supplied a
  figure, benchmark or case law fixing it**; any euro threshold in a delib document is `**[std]**`. The age-seven rule was
  reported by one summary only. **§ 160 VVG was never returned by any search** and its content — the default interpretation
  rules for several beneficiaries and for an "Erben" designation — is **not established**. The presumption that a designation is
  revocable unless stated otherwise is implied by § 159's structure but was not stated by any summary and is `[unverified]`.
  Whether the three-year suicide clock restarts on reinstatement or on an increase in sum assured is the general understanding
  and is `[unverified]`; no summary gave typical AVB wording.
- Read in the 2026-08-30 pass — **§ 160 is retrieved and the gap this entry recorded is closed.**
  § 160 Abs. 1: several beneficiaries without stated shares take equally and a share not acquired accrues to the others; Abs. 2: a
  designation of the *Erben* means, in case of doubt, those called as heirs at the time of death in proportion to their shares, and
  *"Eine Ausschlagung der Erbschaft hat auf die Berechtigung keinen Einfluss"*; Abs. 3: a right not acquired falls to the
  policyholder; Abs. 4: the *Fiskus* as heir has no benefit right. **Three further precisions.** § 150 Abs. 2 excepts
  *betriebliche Altersversorgung* from the written-consent requirement, and **§ 150 Abs. 4** provides that where the supervisor has
  fixed a maximum for *gewöhnliche Beerdigungskosten* that maximum governs — **the statute names a mechanism, not a figure**, so any
  euro threshold in delib stays `[std]`. § 161 Abs. 2 allows the three-year suicide period to be extended **only *durch
  Einzelvereinbarung***, not in the AVB. § 162 Abs. 1 applies only where the policy is on another person's life.
- Products: RLV and KLV load-bearing; the other eight qualified.

### R27. VVG § 163 — Prämien- und Leistungsänderung
- Publisher: Bundesamt für Justiz; mirrors at ten hosts including two Haufe commentary sections and Gabler's
  *Beitragsanpassung*. Doc type: statutory section.
- URL: https://www.gesetze-im-internet.de/vvg_2008/__163.html (returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; § 163 read in full — four Absätze.
  `vvg_2008/__163.html` is a 5.6 kB frameset shell.
- Content: the insurer may adjust the agreed premium where **three cumulative conditions** are met: (1) the **Leistungsbedarf**
  has changed in a way that is **not merely temporary and was not foreseeable** relative to the calculation bases of the agreed
  premium; (2) the **newly set premium**, on the corrected bases, is **appropriate and necessary** to secure the permanent
  fulfilment of the benefit; and (3) an **unabhängiger Treuhänder** has reviewed and confirmed the bases and those conditions —
  the contractual counterpart of the supervisory trustee of § 142 VAG [R11]. Two limits: **the adjustment is excluded** to the
  extent the benefits were **insufficiently calculated at the original or a previous calculation and a diligent and
  conscientious actuary should have recognised this**, in particular on the statistical bases then available — i.e. **the
  insurer may not reprice its way out of its own mispricing**; and the trustee step falls away where the change requires
  supervisory approval. The article also permits a **reduction of the insurance benefit** on the same conditions as an
  alternative to raising the premium. **For delib**: this is why a German BU or Pflegerente premium is *not* unconditionally
  guaranteed even where it is level, and why the correct description of a BU or PFL premium is a ***Bruttobeitrag* with a
  *Zahlbeitrag* below it**, the gap being a discretionary surplus rebate withdrawable **without invoking § 163 at all** [R53]. A
  model that treats the *Zahlbeitrag* as guaranteed for the whole term is making a behavioural assumption and the notes must
  label it.
- Not established: whether § 163 reaches *kapitalbildende* premiums in practice, or is effectively confined to biometric covers,
  **was not settled by any summary**. The interaction with the *Zahlbeitrag*/*Bruttobeitrag* mechanism — which operates through
  § 153 rather than § 163 — is the compiler's synthesis and is `[unverified]` as to its legal characterisation. No trustee-
  appointment procedure or VAG cross-reference was returned.
- Read in the 2026-08-30 pass — **one correction and one addition.** **Correction: the benefit-reduction
  alternative is the *policyholder's* right** — § 163 Abs. 2 Satz 1: *"Der Versicherungsnehmer kann verlangen, dass an Stelle einer
  Erhöhung der Prämie nach Absatz 1 die Versicherungsleistung entsprechend herabgesetzt wird."* — and only *"Bei einer prämienfreien
  Versicherung"* is the **insurer** entitled to reduce (Satz 2). **Addition: § 163 Abs. 3 is a timing rule** — the re-set or the
  reduction *"werden zu Beginn des zweiten Monats wirksam, der auf die Mitteilung der Neufestsetzung oder der Herabsetzung und der
  hierfür maßgeblichen Gründe an den Versicherungsnehmer folgt"*, so a monthly model has a defined effective date and a minimum
  one-month lag. The three cumulative conditions and the mispricing bar are confirmed verbatim, and Abs. 4 confirms that the trustee
  step falls away where supervisory approval is required. **Still `[unverified]`:** whether § 163 bites on *kapitalbildende* premiums
  in practice — **the statute draws no branch line at all**, so this is a question about practice, not text.
- Products: BU and PFL load-bearing; KLV, RV, RLV qualified.

### R28. VVG §§ 165–170 — prämienfreie Versicherung, Kündigung, Rückkaufswert and the Stornoabzug
- Publisher: Bundesamt für Justiz; mirrors at `dejure.org`, `buzer.de`, `lxgesetze.de`, `lexetius.com`, `juraforum.de`,
  `datenbank.nwb.de`, `anwalt.de`, `fachanwalt.de`, `haufe.de`, `sozialgesetzbuch-sgb.de`, `bavheute.de`. Doc type: statutory
  sections.
- URL: https://www.gesetze-im-internet.de/vvg_2008/__165.html ; `__166.html` ; `__168.html` ; `__169.html` (returned);
  `__167.html` `[unverified canonical form]`
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; §§ 165, 166, 167, 168 and 169 read in full.
  `vvg_2008/__165.html` is a 4.5 kB shell and `vvg_2008/__170.html` answered with a connection reset.
- Content: **§ 165 *Prämienfreie Versicherung*.** The policyholder may **at any time, for the end of the current insurance
  period, demand conversion into a prämienfreie Versicherung**, provided the agreed ***Mindestversicherungsleistung*** is
  reached; if not, the insurer must **pay the Rückkaufswert including surplus shares under § 169**. The paid-up benefit is
  computed **by recognised actuarial rules, on the calculation bases of the premium calculation, on the basis of the
  Rückkaufswert under § 169 Abs. 3 to 5**, and **must be stated in the contract for each insurance year**. **§ 166**: where the
  **insurer** terminates, the insurance is **automatically converted to prämienfrei**; and in the § 38 Abs. 2 premium-default
  case [R30] the insurer owes **the benefit it would have owed had the contract been paid-up at the date of the claim**, a
  consequence the § 38 Abs. 1 notice must point out. **German lapse is therefore a three-way decrement** — surrender,
  *Beitragsfreistellung*, and premium-default conversion — the last two keeping the policy in force with a reduced benefit and a
  continuing expense loading. A delib model implementing only surrender says so and states what the paid-up path would do; one
  implementing *Beitragsfreistellung* anchors the paid-up sum to the **same § 169 value** the surrender path uses, or the two
  will not reconcile. **§ 167** lets the policyholder **at any time demand conversion into an insurance meeting § 851c Abs. 1
  ZPO** [R40], bearing the costs; commentary adds it confers **no power of disposal**, only a right to demand. **§ 168**: **Abs.
  1** — where *laufende Prämien* are payable the policyholder may terminate **at any time for the end of the current insurance
  period**; **Abs. 2** — for a risk where the **occurrence of the insurer's obligation is certain** the right exists **even on a
  single premium**; **Abs. 3** — the carve-out that defines the German pension products: Abs. 1 and 2 do **not** apply to a
  contract intended for old-age provision where realisation has been excluded, namely (a) a **Basisrentenvertrag certified under
  § 5a AltZertG** with *Verwertung* excluded under § 10 Abs. 1 Nr. 2 Satz 1 Buchst. b EStG [R39][R43], and (b) contracts where
  the parties **irrevocably excluded realisation before entry into retirement**, capped by § 12 Abs. 2 Nr. 3 SGB II, a limb
  dated by one summary to an amendment of **26 August 2022 in force 1 January 2023** (the *Bürgergeld-Gesetz*). **Model
  consequence, the sharpest product distinction in delib: BAS has no surrender value and no lapse-to-surrender decrement.** **§
  169 *Rückkaufswert*.** The base measure is the ***Deckungskapital*** computed by recognised actuarial rules **on the
  calculation bases of the premium calculation**, at the **end of the current insurance period**. **The floor — Abs. 3**, and the statutory
  wording read on 2026-08-30 differs from the summary this entry carried in three places: *"bei **einer** Kündigung des
  **Versicherungsverhältnisses jedoch** mindestens der Betrag des Deckungskapitals, **das** sich bei gleichmäßiger Verteilung der
  angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt"*, with **supervisory rules on maximum Zillmer
  rates remaining unaffected** [R16] — **a floor on the value, not a cap on the charge**. **Abs. 4 is narrower than this entry said:**
  the *Zeitwert* measure applies to *fondsgebundene Versicherungen* and other § 124 Abs. 2 Satz 2 VAG contracts *"soweit nicht der
  Versicherer eine bestimmte Leistung garantiert; im Übrigen gilt Absatz 3"*, the calculation principles to be stated in the
  contract — the trigger is the **product class**, not the absence of a fixed guarantee. **Abs. 5 — the Stornoabzug**, quoted: *"Der Versicherer ist zu einem Abzug von dem nach Absatz 3 oder 4 berechneten
  Betrag nur berechtigt, wenn er vereinbart, beziffert und angemessen ist"*, and *"Die Vereinbarung eines Abzugs für noch nicht
  getilgte Abschluss- und Vertriebskosten ist unwirksam"*, with the **burden of proof on the insurer**. The *Rückkaufswert* and
  the extent to which it is guaranteed must be **communicated before the policyholder makes the contract declaration**. A delib
  model carrying an acquisition charge implements the **five-year floor as a `max()` against the tariff surrender value** and is
  tested on points that surrender where the floor binds and where it does not.
- Not established: **the Absatz numbering for the § 169 base measure and for the disclosure duty is `[unverified]`** — only Abs.
  3 and Abs. 5 are corroborated by quoted text and Abs. 4 by the Abs. 5 cross-reference. **No market range for Stornoabzug
  levels was established**, so every percentage is `**[std]**` except the one concrete number the BGH Debeka decision puts in
  the record [R36]. The *vereinbarte Mindestversicherungsleistung* is **contractual, not statutory, and no market range was
  returned**, so every such threshold is `**[std]**`. Whether a paid-up conversion may carry its own *Abzug* separate from Abs.
  5 is **not established**; § 166's Absatz structure is `[unverified]`. **Whether § 168 Abs. 2 gives a single-premium immediate
  annuity in payment a termination right was not resolved** — the market answer is no, **no search confirmed it**, and it is
  `[unverified]`. The § 12 Abs. 2 Nr. 3 SGB II amounts are not established, and whether Abs. 3 limb (b) requires an irrevocable
  exclusion at inception was reported inconsistently. No conversion mechanics or cost figure for § 167 was returned.
- Read in the 2026-08-30 pass — **the block this library leans on hardest, and the pass changed it most.**
  **§ 169 Abs. 3 verbatim, because the summary quotation this entry carried got three words wrong:** *"Der Rückkaufswert ist das nach
  anerkannten Regeln der Versicherungsmathematik mit den Rechnungsgrundlagen der Prämienkalkulation zum Schluss der laufenden
  Versicherungsperiode berechnete Deckungskapital der Versicherung, bei einer Kündigung des Versicherungsverhältnisses jedoch
  mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf
  die ersten fünf Vertragsjahre ergibt; die aufsichtsrechtlichen Regelungen über Höchstzillmersätze bleiben unberührt."* **Abs. 3
  Satz 2 is the disclosure duty** (before the policyholder's declaration, detail left to the VVG-InfoV). **Abs. 4 is narrower than
  this entry said:** the *Zeitwert* measure applies to *fondsgebundene Versicherungen* and other § 124 Abs. 2 Satz 2 VAG contracts
  *"soweit nicht der Versicherer eine bestimmte Leistung garantiert; im Übrigen gilt Absatz 3"* — the trigger is the **product class**,
  not the absence of a fixed guarantee. **Abs. 5** confirms *"vereinbart, beziffert und angemessen"* and the ineffectiveness of a
  deduction for untilgte acquisition costs — **but contains no burden-of-proof rule**, which is case law and, in the GDV model
  conditions, an express clause [R37]. **Abs. 6 is new to this library:** the insurer may reduce the Abs. 3 amount *"angemessen ...
  soweit dies erforderlich ist, um eine Gefährdung der Belange der Versicherungsnehmer ... auszuschließen"*, *"jeweils auf ein Jahr
  befristet"*. **Abs. 7** is the surplus limb behind every *"Rückkaufswert einschließlich der Überschussanteile"* cross-reference.
  **§ 168 Abs. 2 answers the SOF question against the market convention:** *"Bei einer Versicherung, die Versicherungsschutz für ein
  Risiko bietet, bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist, steht das Kündigungsrecht dem Versicherungsnehmer
  auch dann zu, wenn die Prämie in einer einmaligen Zahlung besteht."*, and Abs. 3 carves out only certified *Basisrenten* and
  irrevocably restricted § 851c/§ 851d ZPO contracts. **This is reported, not acted on: no delib model is changed in this pass.**
  § 165 Abs. 2 confirms the paid-up computation *"unter Zugrundelegung des Rückkaufswertes nach § 169 Abs. 3 bis 5"* and the duty to
  state it for each insurance year; § 166 has four Absätze including a two-month employer-cover limb; § 167 puts the conversion costs
  on the policyholder.
- Products: KLV, RV, FRV, IDX, RIE, BU, PFL load-bearing; BAS qualified (§ 165 yes, §§ 168–169 no); SOF and RLV qualified.

### R29. VVG §§ 172–177 — Kapitel 6, Berufsunfähigkeitsversicherung
- Publisher: Bundesamt für Justiz; mirrors at `dejure.org`, `buzer.de`, `rewis.io`, `lxgesetze.de`, `juraforum.de`,
  `datenbank.nwb.de`, `rechtsportal.de`, `jurion.de`, `anwalt24.de`, `sozialgesetzbuch-sgb.de`, plus a Haufe chapter page. Doc
  type: statutory sections (§ 172 *Leistung des Versicherers*; § 173 *Anerkenntnis*; § 174 *Leistungsfreiheit*; § 175
  *Abweichende Vereinbarungen*; § 176 *Anzuwendende Vorschriften*; § 177 *Ähnliche Versicherungsverträge*).
- URL: https://www.gesetze-im-internet.de/vvg_2008/__172.html, `__176.html`, `__177.html` (returned); `__173.html`,
  `__174.html`, `__175.html` `[unverified canonical form]`
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; §§ 172, 173, 174, 175, 176 and 177 read in full — the whole
  chapter. `vvg_2008/__172.html` is a 4.3 kB shell; `swisslife.de` refused with HTTP 403.
- Content: **§ 172 Abs. 1** — the insurer is obliged to render the agreed benefits for a *Berufsunfähigkeit* that arose **after
  the start of the insurance**. **§ 172 Abs. 2 — the statutory definition**, quoted by the summary: *"Berufsunfähig ist, wer
  seinen zuletzt ausgeübten Beruf, so wie er ohne gesundheitliche Beeinträchtigung ausgestaltet war, infolge Krankheit,
  Körperverletzung oder mehr als altersentsprechendem Kräfteverfall ganz oder teilweise voraussichtlich auf Dauer nicht mehr
  ausüben kann."* Four elements matter for a model: the reference occupation is **the last occupation as it was structured
  before the impairment**; the causes are **illness, bodily injury or more-than-age-appropriate decline of strength**; the
  incapacity may be **whole or partial**; and the standard is ***voraussichtlich auf Dauer***. **§ 172 Abs. 3** permits the
  additional condition that the insured **does not and cannot pursue another activity** their training and abilities enable and
  which corresponds to their previous *Lebensstellung* — the statutory basis of the ***abstrakte Verweisung*** [R37]. **§ 173
  *Anerkenntnis***: after a claim the insurer must **declare in Textform whether it acknowledges its obligation**; the
  acknowledgement may be **time-limited only once** and is binding until the end of that period. **§ 174 *Leistungsfreiheit***:
  where the insurer establishes that the conditions of liability have ceased it is free of the obligation, but **cessation takes
  effect only after prior notice in Textform and only from the end of the third month following that notice** — the
  *Nachprüfung* mechanism. **§ 175**: §§ 173 and 174 may not be varied to the policyholder's detriment. **§ 176**, quoted: *"Die
  §§ 150 bis 170 sind auf die Berufsunfähigkeitsversicherung entsprechend anzuwenden, soweit die Besonderheiten dieser
  Versicherung nicht entgegenstehen."* **§ 177**, quoted: *"(1) Die §§ 173 bis 176 sind auf alle Versicherungsverträge, bei
  denen der Versicherer für eine dauerhafte Beeinträchtigung der Arbeitsfähigkeit eine Leistung verspricht, entsprechend
  anzuwenden. (2) Auf die Unfallversicherung sowie auf Krankenversicherungsverträge … ist Absatz 1 nicht anzuwenden."* **Model
  consequences for BU**: the **three-month notice** before benefits stop is a real monthly cash-flow item — a reactivation
  recognised in month *t* still pays through *t+3*; the **once-only time-limited acknowledgement** is why a claims-in-payment
  model needs a distinct "acknowledged" state; and § 176 is the authority for giving a BU model a *Rückkaufswert*, a
  *Beitragsfreistellung* and an *Überschussbeteiligung* at all.
- Not established: **the six-month prognosis and the 50 % degree thresholds that dominate the German market are not in § 172** —
  the statute says *voraussichtlich auf Dauer* and *ganz oder teilweise*; those are **AVB conventions** [R37]. **Whether § 177
  Abs. 1 reaches a *Pflegerentenversicherung* is contested and unresolved**: a trade headline returned by the § 177 query reads
  *"VVG-Regeln zu LV gelten bei Grundfähigkeits- und Schwere-Krankheiten-Policen nicht"*, which points against for
  non-work-capacity triggers. This is **the main open legal question for PFL**. § 172 Abs. 1's "after the start of the
  insurance" wording was reported by one summary only.
- Read in the 2026-08-30 pass. § 172 Abs. 2 is confirmed word for word against the summary this entry
  carried. **§ 177 Abs. 1 is the sentence that matters for PFL, and its wording does not obviously reach a *Pflegerente*:**
  *"Die §§ 173 bis 176 sind auf alle Versicherungsverträge, bei denen der Versicherer für eine dauerhafte Beeinträchtigung der
  Arbeitsfähigkeit eine Leistung verspricht, entsprechend anzuwenden."*, with Abs. 2 excluding accident insurance and health-insurance
  contracts covering that risk. A *Pflegerentenversicherung* pays on *Pflegebedürftigkeit*, not on impaired *Arbeitsfähigkeit* —
  so whether Kapitel 6 reaches it is a live question the text does not answer in the product's favour, and delib treats the PFL
  claims-process rules as AVB conventions [R51]. § 174 Abs. 2 confirms the **three-month** cessation lag and § 173 Abs. 2 the
  once-only time limitation of the *Anerkenntnis*; § 175 makes §§ 173 and 174 semi-mandatory.
- Products: BU load-bearing; PFL qualified and contested; KLV, RV, RLV, BAS qualified (rider forms).

### R30. VVG §§ 19, 21, 37, 38, 157 and 158 — Anzeigepflicht, Zahlungsverzug, Altersangabe, Gefahränderung
- Publisher: Bundesamt für Justiz; mirrors at `buzer.de`, `dejure.org`, `juraforum.de` and practitioner PDFs including a
  *Versicherer im Raum der Kirchen* leaflet and an Allrecht *VVG-Belehrung § 19* tariff document; a Bavarian consumer-portal
  page for §§ 37/38. Doc type: statutory sections plus two live market instruction texts.
- URL: https://www.gesetze-im-internet.de/vvg_2008/__19.html, `__37.html`, `__157.html`, `__158.html` (returned); `__38.html`
  `[unverified canonical form]`
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; §§ 19, 21, 37, 38, 157 and 158 read in full.
  `vvg_2008/__19.html` is a 5.8 kB shell.
- Content: **§ 19** — the policyholder must disclose, up to making the contract declaration, the risk circumstances known to
  them for which the insurer has **asked in Textform**. On breach the insurer may **rescind**; rescission is **excluded** where
  the breach was neither intentional nor grossly negligent, in which case the insurer may **terminate on one month's notice**;
  and the obligation to perform falls away where the breach was ***arglistig***. **The limitation period is not in § 19 but in § 21 Abs. 3**, under which the rights to
  rescind, terminate and adjust conferred by § 19 Abs. 2 to 4 **lapse five years after conclusion**, extended to **ten years**
  where the breach was intentional or fraudulent; the lapse does not apply to insured events occurring before the period
  expires. The section attribution is `[unverified]` — the search summaries gave the periods without naming the section. **§ 157** — where the **age of the insured person was
  misstated**, the insurer's benefit **changes in the ratio of the premium corresponding to the true age to the agreed
  premium**, and the right to rescind exists only if the insurer would not have concluded the contract at the true age. **§
  158** — an **increase in risk** counts as such **only where it has been expressly agreed to count as one**, in Textform, and
  can no longer be invoked once **five years** (ten on intent or fraud) have passed; a premium reduction can likewise be
  demanded only for an expressly agreed decrease. **§ 37** — if the single or first premium is unpaid the insurer may rescind,
  and is not liable if the insured event occurs while it is unpaid, **but only if** it drew attention to that consequence by a
  separate Textform notice or a conspicuous notice in the *Versicherungsschein*. **§ 38** — for a *Folgeprämie* the insurer may
  set a payment deadline at the policyholder's cost; the reported requirements for a valid *qualifizierte Mahnung* are
  **Textform**, an **itemised statement of arrears of premium, interest and costs**, and a **minimum period of two weeks**; the
  insurer is free of liability where the event occurs after expiry and the policyholder is in default. **§ 166 overrides the
  general § 38 consequence for life insurance**: cover does not simply cease, the contract converts to *prämienfrei* [R28].
  **Model consequences**: § 157's **pro-rata benefit adjustment** is a clean, implementable rule and a natural test for RLV and
  KLV; § 158's default — **no risk-increase consequence unless expressly agreed** — is why German life and BU contracts are
  *not* subject to a general occupation-change clause and why a delib BU model needs no mid-term reunderwriting state; and
  **German lapse is not instantaneous**: due date → qualified reminder with a **two-week** period → expiry → conversion to
  paid-up. A monthly model that applies a lapse decrement in the month of the missed premium is off by at least one month and
  applies the wrong benefit basis. The **five-year contestability window** is a real first-duration mortality and morbidity
  effect a model may fold into a select period, provided it says so.
- Not established: the § 19 Absatz numbering is the standard account but was **not confirmed Absatz by Absatz** and is
  `[unverified]`. Whether § 38 Abs. 3 also gives a right to terminate without notice after the deadline was **not returned**.
  **§ 23 VVG (Gefahrerhöhung)**, cross-referenced by § 158, and **§ 33 VVG (Fälligkeit)**, cross-referenced by § 152 Abs. 3,
  were never searched. Whether the ten-year period runs from conclusion or from the breach differed in emphasis between
  summaries. No search result addressed market practice on grace periods beyond the statutory two weeks.
- Read in the 2026-08-30 pass — **four resolutions and one attribution correction.** **(1)** The § 19 Absatz
  numbering is confirmed: Abs. 1 duty on Textform questions, Abs. 2 *Rücktritt*, Abs. 3 exclusion where neither intentional nor
  grossly negligent plus a one-month termination right, Abs. 4 exclusion where the insurer would have concluded anyway, Abs. 5 the
  separate Textform warning, **Abs. 6** a policyholder termination right without notice within one month where a contract change
  raises the premium *"um mehr als 10 Prozent"* or excludes the risk. **(2) The *arglistig* forfeiture is § 21 Abs. 2 Satz 2, not
  § 19.** **(3)** § 21 Abs. 3 in full: *"Die Rechte des Versicherers nach § 19 Abs. 2 bis 4 erlöschen nach Ablauf von fünf Jahren nach
  Vertragsschluss; dies gilt nicht für Versicherungsfälle, die vor Ablauf dieser Frist eingetreten sind. Hat der Versicherungsnehmer
  die Anzeigepflicht vorsätzlich oder arglistig verletzt, beläuft sich die Frist auf zehn Jahre."* — **both periods run from
  *Vertragsschluss***, and claims inside the window stay contestable afterwards; Abs. 1 adds a one-month written exercise deadline.
  **(4)** **§ 38 Abs. 3 does give a right to terminate without notice after expiry**, combinable with the deadline and defeated by
  payment within one month. § 157 and § 158 are confirmed verbatim, § 158 Abs. 2 adding five-year and ten-year limits on relying on a
  risk increase. **Still `[unverified]`:** §§ 23 and 33 VVG were not opened, and no retrieved document addresses grace-period market
  practice.
- Products: RLV, BU, PFL, KLV, RV load-bearing; the rest qualified.

---

## 6. Conduct, disclosure and distribution

### R31. VVG §§ 6, 7, 1a, 7b, 7c and 214, with the VVG-InfoV — advice, information, cost disclosure and Effektivkosten
- Publisher: Bundesamt für Justiz; mirrors at `dejure.org`, `juraforum.de`, `buzer.de`, `lxgesetze.de`, `datenbank.nwb.de`,
  `ra.de`, `freirecht.de`, `anwalt.de`, `sozialgesetzbuch-sgb.de`; three IHK guidance pages; Gabler; an **ifa Ulm** note on the
  Effektivkosten amendment; the Versicherungsombudsmann's *Wir über uns* PDF. Doc type: statutory sections and the
  *VVG-Informationspflichtenverordnung* of 18 December 2007.
- URL: https://www.gesetze-im-internet.de/vvg_2008/__6.html ; `__7.html` ; `__7b.html` ; `__7c.html` ; `__214.html` ;
  https://www.gesetze-im-internet.de/vvg-infov/BJNR300400007.html ; `.../__2.html` ; `.../__4.html` ;
  https://dejure.org/gesetze/VVG/1a.html (all returned)
- Retrieved: **yes** — canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read **2026-08-30**; §§ 1a, 6, 7, 7b, 7c and 214 read in full, with the
  **VVG-InfoV** (canonical XML, Stand: zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156), §§ 2 and 4 read in full.
  The VVG-InfoV index page serves (34 kB) and `vvg-infov/__2.html` serves in full; `dejure.org/gesetze/VVG/1a.html` serves.
- Content: **§ 6** — the insurer must **question and advise** so far as the offer or the policyholder's situation gives
  occasion, **state the reasons** and **document** it; the duty continues after conclusion where there is a recognisable
  occasion; the policyholder may **waive** it by a separate written declaration. **§ 7** — the contract terms including the AVB
  and the VVG-InfoV information must be communicated **in Textform and in good time before the policyholder makes the contract
  declaration**; § 7 Abs. 2 enables the VVG-InfoV. **§ 1a**, quoted from a summary: *"Der Versicherer muss bei seiner
  Vertriebstätigkeit … stets ehrlich, redlich und professionell in deren bestmöglichem Interesse handeln"*; **OLG Stuttgart
  rejected the argument that this obliges an insurer to adapt or redesign its own products** — the limit that keeps § 1a a
  conduct standard rather than a product-design mandate, and the counterweight to Merkblatt 01/2023 [R35]. **§ 7b** — for
  *Versicherungsanlageprodukte* within Art. 2 Abs. 1 Nr. 17 IDD, information on the **distribution** and on **all costs and
  charges** in good time, including whether a periodic suitability assessment will be provided and warnings on the risks. **§
  7c** — only products **geeignet** for the policyholder and matching their **risk tolerance and ability to bear losses** may be
  recommended, with *Angemessenheit* examined in every case. **§ 214** — a private body may be recognised as a
  *Schlichtungsstelle* under § 24 VSBG; the **Versicherungsombudsmann e.V.** has been recognised **since August 2016**. **The
  VVG-InfoV settles three things for delib.** **(a) Cost disclosure, § 2 Abs. 1 Nr. 1**: the **costs included in the premium**
  must be disclosed — *Abschlusskosten* as a **single total amount**, other included costs as a **percentage of the annual
  premium with the duration stated**, and the *Verwaltungskosten* **separately**; a further summary reports that the amounts
  under Nr. 1, 2, 4 and 5 **must be stated in euro**. **This is why a German *Produktinformationsblatt* can be read as a source
  of actual charge levels in a way a French *encadré* cannot**: the *encadré* discloses maxima, the German PIB the amounts in
  the premium. **(b) The three Modellrechnung rates, § 2 Abs. 3** [R25]. **(c) Effektivkosten**: for life contracts covering a
  risk whose occurrence is certain, the ***Minderung der Wertentwicklung durch Kosten in Prozentpunkten bis zum Beginn der
  Auszahlungsphase*** must be disclosed, introduced by the LVRG in 2014 and a general information duty from **January 2015**,
  with the third-layer calculation later aligned to the **total-cost-indicator method of Annex VI to Delegated Regulation (EU)
  2017/653** [R32] and exceptions for *Altersvorsorge-* and *Basisrentenverträge* [R43]. **(d) § 4**, now headed
  *Informationsblatt zu Versicherungsprodukten*, requires the sheet to follow **Commission Implementing Regulation (EU)
  2017/1469 of 11 August 2017**, with the sequence of information prescribed so products can be compared. **For delib the
  Effektivkosten figure is a validation target for a product's charge parameterisation, not an input** — reproducing it exactly
  needs the PRIIPs Annex VI algorithm and a specified holding period, neither of which delib implements.
- Not established: **§ 1 VVG-InfoV was never searched** and the full item list of § 2 Abs. 1 was not retrieved; the summaries
  **disagree on whether *Abschlusskosten* are disclosed only as a euro total or also as a percentage**; the date and instrument
  of the amendment moving third-layer Effektivkosten onto the PRIIPs method is **not established**, and the § 4 Abs. 5 Satz 3
  citation rests on one summary. **§ 6a VVG was never returned by a direct search** and its heading and content are **not
  established**; **§ 7d** was named once and is otherwise unestablished. **Art. 2 Abs. 1 Nr. 17 IDD's definition of
  *Versicherungsanlageprodukt* — which decides whether FRV and IDX are in scope and whether a guaranteed KLV is — was not
  retrieved and is the most consequential gap in this entry.** §§ 59–68 VVG were reached only through IHK summaries and the §
  60/§ 61 attributions are `[unverified]`.
- Read in the 2026-08-30 pass — **one correction and three additions.** **Correction: § 214 does not
  recognise the *Versicherungsombudsmann*.** It empowers the **Bundesamt für Justiz** to recognise privately organised bodies as
  *Schlichtungsstelle* on the § 24 VSBG conditions, requires them to answer every complaint and to report harmful business practices
  to BaFin. The *Versicherungsombudsmann* is recognised **under** § 214, and the "since August 2016" date is `[unverified]`.
  **Additions.** **§ 6 Abs. 6** disapplies the whole advice-and-documentation regime where a *Versicherungsmakler* arranges the
  contract. **§ 2 Abs. 6 VVG-InfoV** gives the Effektivkosten method — *"wie der Gesamtkostenindikator nach Anhang VI der Delegierten
  Verordnung (EU) 2017/653"* [R32], always on that Annex's pre-cost return, carrying its biometric cost component only where the
  product guarantees **at least a 90 per cent** participation in *Risikoüberschüsse* — **and Satz 4 excludes the whole method from
  *Altersvorsorgeverträge* and *Basisrentenverträge*** under §§ 1 and 2 AltZertG, which are governed by the AltvPIBV instead [R43].
  **§ 4 Abs. 3 VVG-InfoV** disapplies the IPID for PRIIPs *Versicherungsanlageprodukte* and for PEPP, so the IPID and the KID are
  alternatives. § 2 Abs. 1 Nr. 1 and Abs. 2 confirm the cost-disclosure structure and the euro requirement; § 2 Abs. 4 extends it to
  BU with the warning that the AVB's BU concept differs from the social-law one. § 1a Abs. 1 Satz 1 in full: *"Der Versicherer muss
  bei seiner Vertriebstätigkeit gegenüber Versicherungsnehmern stets ehrlich, redlich und professionell in deren bestmöglichem
  Interesse handeln."*
- Products: all ten. **No cash-flow consequence for any delib model** except through the charge parameterisation the
  Effektivkosten validate.

### R32. PRIIPs — Verordnung (EU) Nr. 1286/2014 and the delegated technical standards
- Publisher: European Parliament and Council; European Commission. Doc type: regulation plus Delegated Regulations **(EU)
  2017/653** of 8 March 2017 and **(EU) 2021/2268**.
- URL: https://eur-lex.europa.eu/legal-content/DE/ALL/?uri=CELEX:32017R0653 (returned);
  https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32021R2268 (returned);
  https://eur-lex.europa.eu/DE/legal-content/summary/key-information-about-investment-products.html (returned). **A direct
  EUR-Lex landing page for Regulation (EU) 1286/2014 itself was not returned by any search and is not established.**
- Retrieved: **yes** — the Official Journal texts at
  https://eur-lex.europa.eu/eli/reg/2014/1286/oj/deu/pdfa1b (Level 1, PDF, 23 pp.),
  https://eur-lex.europa.eu/eli/reg_del/2017/653/oj/deu/pdfa1b (the RTS, PDF, 52 pp., ABl. L 100 vom 12.4.2017) and
  https://eur-lex.europa.eu/eli/reg_del/2021/2268/oj/deu/pdfa1b (the amendment, PDF, 57 pp., ABl. L 455 I vom 20.12.2021), all read
  **2026-08-30**. The `legal-content/DE/ALL/?uri=CELEX:32017R0653` and `.../32021R2268` landing pages also serve.
- Content: Regulation 1286/2014 introduced a standardised ***Basisinformationsblatt* (KID)** for packaged retail investment
  products **and *Versicherungsanlageprodukte***. Uniform requirements apply to delivery of the KID for **all** insurance-based
  investment products, **regardless of whether the underlying investment options are themselves PRIIPs** — the rule that pulls a
  German *fondsgebundene Rentenversicherung* with a fund menu wholly into scope. **2017/653** lays down the RTS on presentation,
  content, review and revision; **2021/2268** amended them with application from **1 January 2023**. Two content elements are
  corroborated: the ***Gesamtrisikoindikator* (SRI)** with explanations **including a possible maximum loss**; and **four
  performance scenarios** under the 2021/2268 regime — **optimistic, moderate, pessimistic and stress**, the stress scenario
  showing significant adverse effects not captured by the pessimistic one. The **total cost indicator method of Annex VI** is
  the method German third-layer *Effektivkosten* are now aligned with [R31].
- Not established: the **SRI 1–7 scale** is asserted in the market but **no search summary returned the numbers 1 to 7**; the
  scale is `[unverified]`. The **recommended holding period** rule, the **RIY presentation**, the **cost tables at 1 year / half
  the RHP / RHP** and the **biometric-risk premium treatment** for insurance PRIIPs were all sought and **none was returned** —
  all **not established**. Whether a *klassische* endowment or an *Indexpolice* with a premium guarantee is a
  *Versicherungsanlageprodukt* turns on Art. 2 Abs. 1 Nr. 17 IDD, not retrieved [R31], so **the scope boundary for KLV, RV and
  IDX is open**.
- Read in the 2026-08-30 pass — **the SRI scale and the scenario names are established.** Art. 3(2)(a) of
  Delegated Regulation (EU) 2017/653: *"Höhe des mit dem PRIIP verbundenen Risikos in Form einer Risikoklasse unter Anwendung eines
  Gesamtrisikoindikators mit einer numerischen Skala von 1 bis 7"*, and Annex III supplies the wording *"Wir haben dieses Produkt auf
  einer Skala von 1 bis 7 in die Risikoklasse [1/2/3/4/5/6/7] eingestuft"*. Annex IV as replaced by (EU) 2021/2268, Nr. 1:
  *"a) optimistisches Szenario; b) mittleres Szenario; c) pessimistisches Szenario; d) Stressszenario."* — **mittleres**, not
  "moderates", and Nr. 3 adds a fifth element specific to insurance: *"Ein zusätzliches Szenario für Versicherungsanlageprodukte beruht
  auf dem ... mittleren Szenario, sofern die Wertentwicklung in Bezug auf die Rendite der Anlage relevant ist."*, with Nr. 4 requiring
  the minimum investment return to be shown. Level 1 Art. 8(3)(d) confirms the *Gesamtrisikoindikator*, the possible maximum loss and
  the performance scenarios as KID content, and the *Gesamtkostenindikator* of Annex VI is the method § 2 Abs. 6 VVG-InfoV points at
  [R31]. **Still `[unverified]`:** the recommended-holding-period rule, the cost tables at 1 year / half the RHP / RHP, and the
  biometric-risk premium treatment inside Annex VI — located but not read line by line.
- Products: FRV and IDX load-bearing; KLV, RV, BAS, RIE, SOF qualified.

### R33. IDD — Richtlinie (EU) 2016/97, the transposition act of 20 July 2017 and § 34d GewO
- Publisher: European Parliament and Council; Deutscher Bundestag / BGBl; Bundesamt für Justiz for the GewO. Doc type:
  directive; transposing federal statute; trade-licensing provision.
- URL: **not established** for the directive and the transposition act — **no search returned an EUR-Lex page for 2016/97 or a
  BGBl page for the transposition**, and **no statutory page for § 34d GewO was returned either**. Secondary sources returned:
  https://kanzlei-michaelis.de/umsetzung-der-eu-vermittlerrichtlinie-2016-97-idd-in-deutsches-recht/ ;
  https://www.bundestag.de/resource/blob/508714/jenssen.pdf ; three IHK pages on *Versicherungsvermittler*.
- Retrieved: **partly.** The **directive** at https://eur-lex.europa.eu/eli/dir/2016/97/oj/deu/pdfa1b was opened
  (PDF, 41 pp., read **2026-08-30**) and **its title, date and structure were read; its conduct articles were not.** **§ 34d GewO**
  was read in full from the canonical XML (**Stand: zuletzt geändert durch Art. 1 G v. 20.7.2026 I Nr. 215**). The Kanzlei Michaelis
  transposition account (155 kB) and the Bundestag Jenssen paper (PDF, 1.0 MB) also serve; the `jura.uni-bonn.de` PDF returns
  HTTP 404.
- Content: the IDD was transposed by the act of **20 July 2017**, in force **23 February 2018** with exceptions; because the
  European roll-out slipped, Member States were free to apply the directive from **1 October 2018** and several German
  provisions took effect then. The useful part is the architecture: the transposition spreads the directive across **three
  statutes** — **GewO** (licensing and conduct of intermediaries, § 34d), **VAG** (distribution, remuneration and a
  **prohibition on passing commission through to the customer**, the *Provisionsabgabeverbot*), and **VVG** (information duties,
  product assessment and standing notices, via §§ 1a, 6a, 7a, 7b, 7c and 7d, [R31]). **§ 34d GewO**: anyone acting as a
  *Versicherungsvermittler* or *Versicherungsberater* needs a trade licence, on four reported conditions — proof of
  ***Sachkunde*** (normally the IHK *Sachkundeprüfung*), *Zuverlässigkeit*, *geordnete Vermögensverhältnisse* and a
  ***Berufshaftpflichtversicherung***; and § 34d Abs. 9 Satz 2 requires **15 hours of continuing education per calendar year**.
  For delib this is background with **no cash-flow consequence**, but it is the reason a German product's acquisition cost is
  structurally a **commission to a § 34d intermediary that the customer cannot be rebated**, which in turn is why the
  *Abschlusskosten* disclosure [R31] and the Zillmerung case law [R36] are as prominent as they are.
- Not established: the directive's own article numbering, the **IPID** requirement, the **demands-and-needs test**, the
  **suitability and appropriateness** tests for IBIPs and the **remuneration and conflicts** provisions were **never read** and
  are `[unverified]` — exactly the gap frlib records for the DDA at its R32. The *Provisionsabgabeverbot*'s VAG paragraph number
  is **not established**. A professional-indemnity minimum of **1,564,610 euro per claim** was returned by a **single commercial
  training-provider page with no year attached**; it is `[unverified]` and **must not be reproduced in a delib document**. The §
  34d Abs. 9 Satz 2 citation rests on one source.
- Read in the 2026-08-30 pass. The instrument is ***Richtlinie (EU) 2016/97 des Europäischen Parlaments und
  des Rates vom 20. Januar 2016 über Versicherungsvertrieb (Neufassung)***. **§ 34d GewO's four conditions are refusal grounds**
  (Abs. 5 Satz 1): lack of *Zuverlässigkeit* (Nr. 1), *"ungeordnete Vermögensverhältnisse"* (Nr. 2), no
  *Berufshaftpflichtversicherung* or equivalent (Nr. 3), no IHK *Sachkunde* examination (Nr. 4). **The commission point becomes a
  citation:** § 34d Abs. 1 Satz 6 — *"Einem Versicherungsvermittler ist es untersagt, Versicherungsnehmern, versicherten Personen oder
  Bezugsberechtigten aus einem Versicherungsvertrag Sondervergütungen zu gewähren oder zu versprechen."* **Still `[unverified]`:** the
  **15 hours** of continuing education — § 34d Abs. 9 Satz 2 imposes the duty and § 34e empowers a regulation, but the hours are in
  the VersVermV, which was not retrieved; and the directive's article numbering, the IPID requirement, the demands-and-needs test and
  the IBIP suitability and remuneration provisions, none of which was read.
- Products: all ten, as conduct background only.

### R34. Unisex — EuGH C-236/09 (Test-Achats), and §§ 19, 20 and 33 AGG
- Publisher: Court of Justice of the European Union; Bundesministerium der Justiz for the AGG; Christian Armbrüster's monograph
  (Universität Bonn) and the Antidiskriminierungsstelle as secondary. Doc type: judgment; federal statute.
- URL: https://datenbank.nwb.de/Dokument/Anzeigen/443611/ (returned);
  https://www.jura.uni-bonn.de/fileadmin/Fachbereich_Rechtswissenschaft/Einrichtungen/Sonstige/Zentrum_fuer_Europaeisches_Wirtschaftsrecht/Schriftenreihe/heft192armbruester.pdf
  (returned); https://www.gesetze-im-internet.de/agg/__19.html and `__20.html` (returned)
- Retrieved: **yes** — the **judgment** as reproduced at `datenbank.nwb.de/Dokument/Anzeigen/443611/` (HTML,
  64 kB) and the **AGG** from the canonical XML (**Stand: zuletzt geändert durch Art. 15 G v. 22.12.2023 I Nr. 414**), §§ 19, 20 and
  33 read in full, both **2026-08-30**. `gesetze-im-internet.de/agg/__19.html` is a 5.8 kB frameset shell.
- Content: the ECJ held on **1 March 2011** in **C-236/09** that using sex as a risk factor in insurance is incompatible with
  equality between men and women under **Articles 21 and 23 of the Charter of Fundamental Rights**, and **invalidated the
  derogation in Article 5(2) of the Gender Directive with effect from 21 December 2012**. From that date sex may **no longer**
  lead to different premiums or benefits for **new** contracts; insurers must offer ***Unisex-Tarife***. On the German side, **§
  19 AGG** carries the civil-law non-discrimination prohibition and expressly names private insurance; **§ 20 AGG** permits
  objectively justified differential treatment; and **§ 20 Abs. 2 Satz 1 AGG — the provision that allowed sex-differentiated
  pricing where sex was a determining risk factor on relevant and accurate actuarial and statistical data — was repealed**.
  Surviving in § 20 Abs. 2 in every account: **costs connected with pregnancy and maternity may under no circumstances lead to
  different premiums or benefits**. **§ 33 Abs. 5 AGG** is the transitional: for insurance relationships concluded **before 21
  December 2012** sex-differentiated treatment remains permissible on the same conditions, **except** for pregnancy and
  maternity costs. **Model consequence, and it is a hard one: every delib model prices unisex.** An RLV, BU or PFL model point
  may carry a `sex` attribute for **decrement** purposes — the underlying DAV tables are sex-specific [R47] — but **must not**
  let sex enter the premium. The standard market resolution is a **portfolio sex-mix assumption** applied to the best-estimate
  decrements; that mix is a modeller's assumption and is `**[std]**`. Letting a sex field leak into pricing reproduces a tariff
  unlawful in Germany since 2012 and is a numbered pitfall.
- Not established: **the amending instrument and date for the § 20 Abs. 2 Satz 1 repeal are reported two ways** — "Bundestag and
  Bundesrat adopted the AGG amendment in late February 2013" versus "made by the *SEPA-Begleitgesetz*, published 3 April 2013,
  with retroactive effect from 21 December 2012". They are reconcilable but **neither is confirmed**; both are recorded. The
  Gender Directive's own number (**2004/113/EG**) was **not returned by any search** and is `[unverified]`. Whether German
  insurers were required to apply unisex to **increases** on pre-2012 contracts is **not established**. **No market sex-mix
  figure was returned**, so every blend weight in delib is `**[std]**` [R47].
- Read in the 2026-08-30 pass — **the Gender Directive's number is established and one AGG provision is new
  to this library.** The judgment names *"Art. 5 Abs. 2 der Richtlinie 2004/113/EG des Rates vom 13. Dezember 2004"* and holds it
  *"ab dem 21.12.2012 ungültig"* for incompatibility with Artt. 21 and 23 of the Charter. **§ 20 Abs. 2 Satz 1 is now the maternity
  rule** — *"Kosten im Zusammenhang mit Schwangerschaft und Mutterschaft dürfen auf keinen Fall zu unterschiedlichen Prämien oder
  Leistungen führen."* — confirming that the old sentence permitting sex-differentiated pricing is gone. **§ 20 Abs. 2 Satz 2 is the
  statutory permission for age-rated tariffs:** differential treatment on religion, disability, age or sexual identity in private
  insurance is lawful *"nur ..., wenn diese auf anerkannten Prinzipien risikoadäquater Kalkulation beruht, insbesondere auf einer
  versicherungsmathematisch ermittelten Risikobewertung unter Heranziehung statistischer Erhebungen"*. § 33 Abs. 5 preserves
  sex-differentiated treatment for pre-21 December 2012 relationships where sex is *"ein bestimmender Faktor"* on accurate actuarial
  data. **A structural signal on later changes, short of an answer:** §§ 33 Abs. 2, 3 and 4 each disapply their transitional to
  *"spätere Änderungen von Dauerschuldverhältnissen"* and **Abs. 5 does not** — but no authority on that reading was retrieved, so it
  stays `[unverified]`. **Also new:** § 1 Abs. 1 Nr. 2 AltZertG independently requires a certified Riester contract to provide
  *"eine lebenslange und unabhängig vom Geschlecht berechnete Altersversorgung"* [R43]. **Still `[unverified]`:** the amending
  instrument and date for the § 20 Abs. 2 repeal, reported two ways, both recorded.
- Products: all ten.

### R35. BaFin Merkblatt 01/2023 (VA) — Wohlverhaltensaufsicht and angemessener Kundennutzen
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht; a Bundestag Drucksache 20/14411 of 23 December 2024 and a Mannheim
  academic paper as secondary. Doc type: supervisory *Merkblatt* with an FAQ and a consultation draft.
- URL:
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Pressemitteilung/2023/pm_2023_05_08_Merkblatt_kapitalbildende_LV.html
  (returned); https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/FAQ/faq_wohlverhalten.html (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2024/bafin_fachartikel_wohlverhalten.html (returned)
- Retrieved: **yes** — the full *Merkblatt* text with its marginal numbers (HTML, 162 kB), BaFin's **FAQ** on it (85 kB)
  and its ***Kundennutzen im Fokus*** article (88 kB), all read **2026-08-30**. The 2023 press release page returns HTTP 404.
- Content: BaFin **consulted on 31 October 2022** and **published in May 2023** a *Merkblatt zu wohlverhaltensaufsichtlichen
  Aspekten bei kapitalbildenden Lebensversicherungsprodukten* setting out what it expects so that such products offer an
  ***angemessener Kundennutzen*** and distribution conflicts of interest are avoided. **Two supervisory tests are reported
  explicitly and both are quantitative in kind if not in level.** **Cost**: BaFin will particularly examine insurers whose
  **Effektivkosten** for *kapitalbildende* products are **very high in a sector comparison**, and insurers whose **expenses for
  insurance intermediaries are noticeably high**. **Return**: producers must **formulate a return target for the relevant target
  market**, and for a retirement product to have appropriate customer benefit it must be **likely to achieve a real investment
  success over its term — a return after costs above a justified inflation rate**. BaFin reports outcomes: **some products
  offering no appropriate customer benefit were taken off the market**, and **cost reductions in existing portfolios and
  retroactive compensation measures** were achieved. For delib this is the German *Value for Money* regime and it matters twice:
  a KLV, RV, FRV or IDX charge parameterisation should be **plausible against a sector Effektivkosten distribution** rather than
  merely internally consistent, because the supervisor now polices the level; and it explains why the German market moved to
  lower guarantees and lower acquisition costs after 2023 — context a product specification's market- role section needs.
- Not established: **no Effektivkosten threshold, sector benchmark or numerical test appears in any summary**; the "very high in
  sector comparison" standard is qualitative as reported. Whether the Merkblatt applies to **fondsgebundene** and
  **indexgebundene** products as well as classical ones is **not established** — the title says *kapitalbildende*, which
  conventionally includes unit-linked savings, but no summary confirmed it. The Merkblatt's **legal basis is contested**: the
  Mannheim paper is titled *"Wohlverhaltensaufsicht: Ihre Rechtsgrundlagen und Grenzen"* and the OLG Stuttgart ruling on § 1a
  VVG [R31] points the other way; the tension is real and **unresolved**. Whether the Merkblatt has been amended since 2023 is
  not established.
- Read in the 2026-08-30 pass — **the scope question is answered and one modality is corrected.** Footnote 2:
  *"Als kapitalbildende Lebensversicherungsprodukte werden hier (klassische und fondsgebundene) Lebensversicherungsprodukte mit
  Sparkomponente bezeichnet. Darunter fallen Versicherungsanlageprodukte sowie weitere Lebensversicherungsprodukte mit Sparkomponente
  (insbesondere ... Direktversicherungen sowie Altersvorsorgeverträge ...)"*, and the body addresses *"die fondsgebundene
  Lebensversicherung (einschließlich statische und dynamische Hybride)"* separately — **so the Merkblatt reaches KLV, RV, FRV, the
  hybrid shapes IDX belongs to, Riester and Basisrente.** **Correction:** the real-return test is a *sollten*, not a *müssen* —
  Rn. 15 says insurers *"sollten ... auch prüfen, ob die Angehörigen des Zielmarktes nicht nur eine positive Rendite nach Kosten,
  sondern auch eine positive Rendite nach Kosten und Inflation anstreben"* (*"realer Anlageerfolg"*, benchmarkable against the ECB's
  medium-term target). What is mandatory is the probability test: *"Ein angemessener Kundennutzen setzt voraus, dass das formulierte
  Renditeziel mit hinreichender Wahrscheinlichkeit erreicht wird. Dies ist im Rahmen der Produktprüfung mit geeigneten stochastischen
  Analysen zu prüfen."*, and where the target market is guarantee-oriented a return target may be dispensable. The *Effektivkosten*
  are named as *"eine geeignete Größe zur Messung der insgesamt anfallenden Kosten"*. **Still `[unverified]`, and the finding is that
  the document is deliberately non-numeric:** no Effektivkosten threshold, sector benchmark or numerical test appears anywhere in it;
  and the reported consultation and publication dates and BaFin's reported enforcement outcomes are not in the *Merkblatt* text.
- Products: KLV, RV, FRV, IDX load-bearing; RIE, BAS, SOF qualified.

---

## 7. The case law and the market's model conditions

### R36. The BGH line of authority on German life contracts
- Publisher: Bundesgerichtshof (press releases and case captions); the CJEU for the 2013 § 5a VVG ruling; secondary reporting
  from Haufe, LTO, beck-aktuell, Versicherungsbote, Verbraucherzentrale Hamburg and Baden-Württemberg, Bund der Versicherten,
  procontra, VdK and several law firms. Doc type: judgments, reached through official press releases and case captions.
- URL: https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2018/2018107.html ; .../2025/2025227.html ;
  .../2026/2026050.html ;
  http://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/document.py?Gericht=bgh&Art=pm&Datum=2013&nr=65268 (all returned)
- Retrieved: **one of the six lines.** The **BGH press release on IV ZR 201/17** was read in full (HTML, 36 kB,
  **2026-08-30**). **The other five lines were not retrieved:** no judgment text and no press release for them was opened, and the
  `juris` document server refused with HTTP 403. Their captions are kept as known references and every statement about them is
  `[unverified]`.
- Content: six lines of authority, each of which changes what a delib model must do. **(1) Zillmerung and the
  Mindestrückkaufswert.** **BGH 12 October 2005 — IV ZR 162/03** (with IV ZR 245/03): clauses setting off *Abschlusskosten*
  against the first premiums are an *unangemessene Benachteiligung* and **invalid**, for intransparency and for substantive
  unfairness. **BGH 25 July 2012 — IV ZR 201/10**: the same, plus clauses that fail to distinguish the *Rückkaufswert* under §
  176 Abs. 3 VVG a.F. from the *Stornoabzug* under § 176 Abs. 4 VVG a.F. are ineffective under § 307 Abs. 1 Satz 2 BGB. **BGH 11
  September 2013 — IV ZR 17/13 and IV ZR 114/13**: for contracts concluded **up to the end of 2007**, *ergänzende
  Vertragsauslegung* gives the policyholder a minimum that **may not fall below half of the ungezillmertes Deckungskapital** on
  the premium-calculation bases; the Court described this as continuing its case law on the **1994–2001** tariff generation and
  extending it to end-2007. **IV ZR 216/13** applies the floor, with reported worked figures of **15,694.12 € paid against
  29,587.75 € of premiums**. **Why this matters although delib models new business**: the *hälftig* floor and the
  five-year-spread floor of § 169 Abs. 3 VVG [R28] are **different rules for different vintages**, so an in-force pre-2008 model
  point carries the judicial floor and delib must not silently apply § 169 Abs. 3 to a pre-2008 issue year. **(2) The
  Widerrufsjoker.** Where the withdrawal instruction was defective the period never started. Its home is **§ 5a VVG a.F.**, the
  *Policenmodell*, in force **1 January 1995 – 31 December 2007**; the CJEU held it incompatible with Union law in **2013** and
  the **BGH decided the question fundamentally on 7 May 2014, IV ZR 76/11**. Bounded both ways by **BGH 15 March 2023 — IV ZR
  40/21** (an instruction omitting the required **form** is not a minor error; *Rückabwicklung* available) and **BGH — IV ZR
  268/21** (no joker where conduct is *treuwidrig*). A successful *Widerspruch* unwinds on **bereicherungsrechtlich** terms —
  premiums back plus *Nutzungen*, less risk cover consumed — **a different payout from either surrender or maturity. delib does
  not implement it**, and the notes say the pre-2008 book carries a legal option the model does not value. **(3)
  Bewertungsreserven.** **BGH 27 June 2018 — IV ZR 201/17**: **§ 153 Abs. 3 Satz 3 VVG in the LVRG version is not
  unconstitutional**, the legislature's stated reason being that a prolonged low-interest environment would threaten insurers'
  ability to deliver the guarantees promised. The claim was for *Bewertungsreserven* *aus abgetretenem Recht* after the maturity
  of a *kapitalbildende Lebensversicherung*. **For delib**: the statutory half is conditional on a portfolio-level test the
  model does not perform and the highest court has confirmed the insurer may reduce it to zero, so a KLV or RV model either
  excludes the component explicitly or carries it as a `**[std]**` scalar citing this decision. **(4) The Rentenfaktor.** **BGH
  10 December 2025 — IV ZR 34/25**: a clause in the AVB of a *fondsgebundene Rentenversicherung* (a Riester contract) letting
  the insurer **reduce the *Rentenfaktor* named in the *Versicherungsschein*** — the monthly annuity per **10,000 € of
  Vertragsguthaben** — **without a corresponding duty to restore it if circumstances improve** is **void** under **§ 308 Nr. 4
  BGB** and **§ 307 Abs. 1 Satz 1 BGB**. The principles are reported to reach **all** comparable clauses, and per the insurer's
  own reported statement contracts concluded **between July 2001 and June 2013** carry the clause while those from **July 2013**
  do not. **The single most model-relevant German decision of the last year**: the *garantierter Rentenfaktor* is a **hard
  guarantee** unless the AVB gives a **symmetric** adjustment right, so an FRV model annuitising at a fixed guaranteed factor
  implements the legally correct default rather than a simplification. **(5) The Stornoabzug.** **BGH 18 March 2026 — IV ZR
  184/24**, overturning **OLG Koblenz, 5 December 2024, 2 UKl 1/23**: a *kapitalmarktabhängiger Stornoabzug* does **not**
  infringe the *Bezifferung* requirement of § 169 Abs. 5 Satz 1 VVG and is not intransparent — the insurer may specify a
  ***Berechnungsverfahren*** rather than a concrete amount at conclusion. The clause: a deduction of **up to 15 % of the
  Deckungskapital**, depending on the **Null-Kupon-Euro-Zinsswapsatz with a ten-year term published by the Deutsche
  Bundesbank**, accepted as suitable to protect the insured community against *zinsinduzierte Stornierungen*. **The case was
  remitted on *Angemessenheit*, so that limb is open**; a delib model may implement a *Stornoabzug* of that shape citing this
  decision as the observed upper end while stating that the appropriateness of 15 % has not been decided. **(6) The Pflegestufe
  gap.** **BGH — IV ZR 126/23**, reported **30 April 2025**: the 2017 reform replaced three *Pflegestufen* with five
  *Pflegegrade*, older AVB still refer to *Pflegestufen*, and that is an **unintended Regelungslücke**; **Pflegegrad 2 may not
  automatically be equated with Pflegestufe I**, because the reform **materially widened** the definition of care need,
  particularly on mental and cognitive grounds. The insurer may not retreat to "no Pflegestufe was established"; an
  **individual** examination, if necessary medical, is in principle possible **independently of the care fund's classification**
  [R51].
- Not established: the date and Aktenzeichen of **IV ZR 73/13** (16 July 2014 is better supported but `[unverified]`); whether
  the 2005 and 2013 *hälftig* rules are one rule or two formulations; **no BGHZ citation** for the 2012 or 2013 decisions. **The
  CJEU reference for the 2013 § 5a ruling was never established** — commonly cited as *Endress*, C-209/12 of 19 December 2013,
  **not returned by any search**. The date of IV ZR 268/21 is not established, and the direction of the 2014 decision is
  reported inconsistently across headlines. For IV ZR 34/25, whether a **symmetric** clause survives is implied but not a stated
  holding, and **the remedy was not reported**; no *Rentenfaktor* figures were given. For IV ZR 184/24, **the functional form
  linking the swap rate to the percentage is not established**, nor whether the clause reaches *Beitragsfreistellung*. The 30
  April 2025 date for IV ZR 126/23 rests on a **single** summary.
- Read in the 2026-08-30 pass — **line (3) now carries the court's own words and a worked figure.** The Senate
  held *"dass die Neuregelung zur Beteiligung des Versicherungsnehmers an Bewertungsreserven ... gemäß § 153 Absatz 3 Satz 3 des
  Versicherungsvertragsgesetzes (VVG) in der Fassung des Lebensversicherungsreformgesetzes vom 1. August 2014, **in Kraft getreten am
  7. August 2014**, nicht verfassungswidrig ist"* — **which independently settles the LVRG's entry-into-force date** [R20]. The facts:
  a *kapitalbildende Lebensversicherung* of 1 September 1999 maturing 1 September 2014, pre-announced on 1 July 2014 at
  **50.274,17 €** including **2.821,35 €** of *Bewertungsreserven*, finally paid at **47.601,77 €** with only **148,95 €** of
  *Bewertungsreserven* after the insurer applied its *Sicherungsbedarf*. The press release also reproduces § 153 Abs. 3 Satz 3 in its
  then-current form, cross-referring to §§ 53c, 54 Abs. 1 und 2, 56a Abs. 3 und 4 und 81c Abs. 1 und 3 VAG a.F., where the provision
  now in force cites §§ 89, 124 Abs. 1, 139 Abs. 3 und 4, 140 und 214 VAG [R24]. **The BGH quashed and remitted**, the appellate court
  having made no findings on whether the ordinary conditions for the reduction were met — so the decision settles the constitutional
  question, not the case.
- Products: KLV, RV, FRV, IDX, RIE and PFL load-bearing; BAS, SOF, RLV, BU qualified.

### R37. GDV-Musterbedingungen and German Berufsunfähigkeit market practice
- Publisher: Gesamtverband der Deutschen Versicherer e.V.; insurer and broker sources (Swiss Life Deutschland, ERGO,
  Württembergische, NÜRNBERGER, CosmosDirekt) for the market practice; a C. H. Beck commentary on the GDV *Musterklauseln*
  (Büchner, 1. Auflage 2025) and a Haufe commentary section as secondary. Doc type: non-binding model conditions;
  market-practice evidence.
- URL: https://www.gdv.de/gdv/service/musterbedingungen (returned);
  https://www.gdv.de/resource/blob/6348/5827a5492cca6aa1147852c30f10247b/allgemeine-bedingungen-fuer-die-kapitalbildende-lebensversicherung-0-pdf-data.pdf
  (returned); https://www.swisslife.de/pk/versicherungen/berufsunfaehigkeitsversicherung/abstrakte-verweisung.html and four
  further insurer pages (returned)
- Retrieved: **yes** for the index and the endowment set. The **GDV *Musterbedingungen* index** (HTML, 94 kB) and
  the ***Allgemeine Bedingungen für die kapitalbildende Lebensversicherung*** (PDF, 20 pp., **Stand: 21.07.2025**) were read
  **2026-08-30**. **The BU model conditions were not opened**, only their titles from the index.
- Content: the GDV publishes ***unverbindliche Musterbedingungen*** — model conditions that are **non-binding** for insurers and
  whose use is **purely optional**. Two facts about the BU models are established: an earlier set was dated **28 April 2021**,
  and the current ones are **MB BUV 22** and **MB BUZ 22**, dated **15 November 2022** — MB BUV the standalone *selbständige*
  BU, MB BUZ the *Zusatzversicherung* rider form. The existence of a **2025 C. H. Beck commentary organised around the GDV
  *Musterklauseln*** is itself evidence that these models are the market's reference wording. **For delib the Musterbedingungen
  are the natural `[S#]` primary product source class** for a reference product — published, free, non-proprietary and the thing
  most insurers' AVB derive from — provided a product specification that follows them also says they are **non-binding** and
  that real AVB differ. **BU market practice above the statutory floor** [R29]. ***Verweisung***: under an ***abstrakte
  Verweisung*** the insured does not necessarily receive benefits merely because they cannot perform their last occupation,
  provided they **could theoretically** perform another activity; under a ***konkrete Verweisung*** the insurer examines whether
  the insured **actually performs** another activity corresponding to their previous *Lebensstellung*. The reported market
  position: **almost all new contracts waive the abstrakte Verweisung**, and nowadays almost all insurers waive it **even in
  their basic tariffs**, retaining the konkrete Verweisung. ***The thresholds***: a broker summary reports the practical test as
  being unable to perform the last occupation **for at least six months** at **50 percent or more**. **Both numbers are AVB
  conventions, not statute.** **Model consequences for BU, and these are the operative ones**: the benefit is a **binary step at
  50 %**, not a proportional payment, so a model must decide whether it projects incidence of ≥50 % incapacity or a graded
  state; the **six-month qualification** is a deferred period in cash-flow terms, so a monthly BU model needs an explicit
  *Karenzzeit* parameter and the worked example must show whether the first payment is in month 7 and whether it is backdated;
  and with the abstrakte Verweisung waived, **reactivation is driven only by konkrete Verweisung or recovery**, which materially
  raises expected claim duration relative to a tariff that retains abstract referral.
- Not established: **no clause text from any GDV model was retrieved.** The specific provisions a delib model needs — the
  *Rückkaufswert* clause, the *Beitragsfreistellung* clause and its *Mindestversicherungssumme*, the *Stornoabzug* clause, the
  BU six-month prognosis fiction and the *Verweisung* wording — are **all not established**, and this is the **largest single
  gap in the contract-law layer**. The date of the ALB model behind the two PDFs is not established, and whether the two blob
  URLs are two versions or a duplicate is not established. The **six months** and **50 percent** figures come from a **single
  broker summary**; they are ubiquitous in the German market but on this evidence they are `[unverified]`. **Whether the six
  months operates as a retroactive fiction (benefits backdated to the start of incapacity) or as a waiting period (benefits from
  month 7) was not addressed by any summary, and the two produce materially different cash flows** — this is the most important
  unresolved parameter for BU. No source gave a market range for *Leistungsdauer*, *Karenzzeit* options or
  *Nachversicherungsgarantien*.
- Read in the 2026-08-30 pass — **the largest gap this file recorded is closed: clause text has been
  retrieved.** The index states the status in the GDV's own words: *"Diese Bedingungen sowie die Muster-Standmitteilungen für
  Lebensversicherungen sind für die Versicherungsunternehmen unverbindlich. Die Verwendung ist rein fakultativ."* — and it lists the
  full life catalogue: four BU sets, the endowment set, five annuity sets plus three AltZertG variants, *Risikolebensversicherung*,
  *Restkreditlebensversicherung*, the *Hinterbliebenenrenten-Zusatzversicherung* forms, and **nine *Muster-Standmitteilungen*** — a
  source class this file had not recorded and one that maps directly onto § 155 VVG [R25]. **There is no model set for an
  *Indexpolice*.** From the endowment set: **§ 12 Abs. 3** reproduces § 169 Abs. 3 VVG and adds a refinement the statute lacks —
  *"Ist die vereinbarte Beitragszahlungsdauer kürzer als fünf Jahre, verteilen wir diese Kosten auf die Beitragszahlungsdauer."*;
  **§ 12 Abs. 4** is the *Abzug* clause and **leaves the level blank** — *"nehmen wir einen Abzug in Höhe von ...¹² vor"*, footnote 12
  *"Unternehmensindividuell zu ergänzen."* — justified by the change in the remaining portfolio's risk position and by compensation
  for collectively provided risk capital, with appropriateness *"im Zweifel von uns nachzuweisen"*, **which is where the
  burden-of-proof rule lives** [R28]; **§ 12 Abs. 5** carries § 169 Abs. 6 VVG; **§ 13** shows that a *Beitragsfreistellung* carries
  **its own separate *Abzug***, also blank; **§ 14 Abs. 2** states *"Wir wenden auf Ihren Vertrag das Verrechnungsverfahren nach § 4
  der Deckungsrückstellungsverordnung an"* with the amortised amount *"auf 2,5 % der von Ihnen während der Laufzeit des Vertrages zu
  zahlenden Beiträge beschränkt"* [R16]. **Corrections:** the "MB BUV 22 / MB BUZ 22, dated 15 November 2022" naming **does not appear
  on the GDV index**, which dates its life section 13.09.2022 and the endowment set 21.07.2025; the short names and the November date
  are dropped. **Still `[unverified]`:** all BU clause text, the *Verweisung* wording and the six-month / 50 % thresholds.
- Products: KLV, RV, RLV, BU load-bearing; the rest qualified.

---

## 8. Tax and the three-layer state-subsidised pension architecture

**Read the evidence warning first.** The tax sweep ran **zero successful searches** — the shared `WebSearch` budget was
exhausted before it opened, and both queries it issued were refused. Every entry in this section rests on one of two things:
**second-hand corroboration** inherited from the prudential and contract sweeps, named per entry, or **general knowledge of
German tax law**. The structural claims — which provision carries which rule, what the mechanic is — are stated plainly because
they are well established and because hedging every clause would destroy the section's usefulness. **But every figure, effective
date, percentage and paragraph number in this section is `[unverified]` unless the entry names a sweep that corroborated it, and
downstream documents must carry that tag through.** Where a number is load-bearing for a model and cannot be confirmed, the
honest form is `**[std]**` with a rationale, **not** a `[REG-R#]` citation. The entries with real second-hand corroboration are
**R39** (the five prohibitions — two statutes, two sweeps), **R43** (the AltZertG § 1 criteria and the PIB/CRK regime — five
queries, two BZSt PDFs), **R44** (the 2026 reform — nine hosts, four official) and **R45** (§ 20 Abs. 1 Nr. 6 and the 50 %-Regel
— the KLV product sweep). Everything else is general knowledge.

### R38. AltEinkG — the Alterseinkünftegesetz and the Drei-Schichten-Modell
- Publisher: Deutscher Bundestag / Bundesrat; promulgated in the Bundesgesetzblatt Teil I. Doc type: *Änderungsgesetz* — its
  operative content lives in the EStG, so it has no standing `gesetze-im-internet.de` page.
- URL: **not established.** A BGBl citation commonly reported as *vom 5. Juli 2004, BGBl. I S. 1427* is `[unverified]` and is
  recorded as a lead, not a citation.
- Retrieved: **no for the act.** No BGBl text and no Bundestag drucksache for the AltEinkG was located or opened in
  this pass. **The two transitions it created were read**, from the EStG canonical XML, **Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197**, on **2026-08-30** — § 10 Abs. 3 at [R39] and
  § 22 Nr. 1 Satz 3 Buchst. a at [R41].
- Content: with effect from **1 January 2005** the act replaced *vorgelagerte* taxation of pensions with a ***nachgelagerte***
  system — qualifying contributions deducted during accumulation, the pension taxed as income in payment — and, because a
  wholesale switch would have doubly taxed the cohorts in the middle, introduced **two long linear transitions running in
  parallel**: a rising deductible percentage of Schicht-1 contributions [R39] and a rising taxable percentage keyed to the
  **year the pension starts** [R41]. Both are still running. The ***Drei-Schichten-Modell*** sorts retirement products by *what
  the state buys with the relief it gives*: **Schicht 1 — Basisversorgung** (gesetzliche Rentenversicherung, berufsständische
  Versorgungswerke, Alterssicherung der Landwirte, and the private **Basisrente**), contributions deductible under § 10 Abs. 1
  Nr. 2 EStG, benefits taxed on a cohort *Besteuerungsanteil*, the price of admission being that the product must look like a
  state pension; **Schicht 2 — kapitalgedeckte, staatlich geförderte Zusatzversorgung** (**Riester** and the *betriebliche
  Altersversorgung*), relief granted as a **direct payment into the contract** (the *Zulage*, a real cash flow) or as a
  *Sonderausgabenabzug*, benefits taxed **in full** under § 22 Nr. 5 EStG to the extent the contributions were subsidised;
  **Schicht 3 — private, ungeförderte Vorsorge** (KLV, RV, FRV, IDX, SOF), contributions not deductible as retirement provision
  at all, benefits lightly taxed under § 20 Abs. 1 Nr. 6 [R45] or on the *Ertragsanteil* [R41]. **For delib the layer is the
  first classifying attribute of every product**: it decides whether a state *Zulage* appears as an inflow, whether a surrender
  decrement is legally possible at all, and whether the payout documentation discusses a *Besteuerungsanteil* or an
  *Ertragsanteil*. The constitutional origin is the **BVerfG judgment of 6 March 2002 — 2 BvL 17/99** `[unverified]`, which gave
  the legislature until 1 January 2005 to end the unequal treatment of *Beamtenpensionen* and statutory pensions; that is why
  the transition is a constitutional remedy with a finite end rather than a policy dial.
- Not established: **the act's date, BGBl citation and article structure**; whether the act itself introduced the *Basisrente*
  label (the statutory term *Basisrentenvertrag* arrives in the AltZertG only later, [R43]); the **Rürup-Kommission**'s report
  and date; and **every element of the BVerfG citation** — docket number, date, deadline and constitutional article are general
  knowledge and `[unverified]`.
- Read in the 2026-08-30 pass — **one correction with consequences downstream.** **The
  contribution-deduction transition has ended.** § 10 Abs. 3 Satz 4 sets 76 per cent for 2013, Satz 6 raises it two points a year
  *"bis zum Kalenderjahr 2022; ab dem Kalenderjahr 2023 beträgt er 100 Prozent"* — so only **one** of the two long transitions is
  still running, the *Besteuerungsanteil* path of § 22, which reaches 100 per cent for the **2058** cohort [R41]. This entry
  previously said both were still running.
- Products: KLV, RV, FRV, IDX, BAS, RIE, SOF load-bearing as architecture; RLV, BU, PFL qualified.

### R39. EStG § 10 Abs. 1 Nr. 2 Buchst. b and § 10 Abs. 3 — the Basisrente deduction, the ceiling and the five prohibitions
- Publisher: Bundesministerium der Justiz; the BMF *Einkommensteuer-Handbuch* and a Frotscher/Geurts commentary on Haufe as
  secondary. Doc type: statutory section.
- URL: https://www.gesetze-im-internet.de/estg/__10.html — **returned in the contract sweep**, alongside the BMF
  *Einkommensteuer-Handbuch* and the Haufe commentary.
- Retrieved: **yes** — EStG canonical XML, **Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197**, read **2026-08-30**; § 10 Abs. 1 Nr. 2 and § 10 Abs. 3 read in full.
  `gesetze-im-internet.de/estg/__10.html` serves in full (41 kB).
- Content: **Buchst. a** covers the compulsory systems — statutory pension, *landwirtschaftliche Alterskassen* and
  *berufsständische Versorgungseinrichtungen*. delib does not model those, but they **consume the same ceiling a Basisrente
  contribution competes for**, which is the single most important behavioural fact about Basisrente demand. **Buchst. b**
  creates the private product: contributions to a contract that provides **exclusively** a **monthly, lifelong *Leibrente*** on
  the taxpayer's own life, commencing **not before completion of the 62nd year of age** (**60** for contracts concluded before 1
  January 2012), optionally with supplementary cover for *Berufsunfähigkeit*, *verminderte Erwerbsfähigkeit* and
  *Hinterbliebene*; and only if the claims are, in the words a sibling search summary returned, ***nicht vererblich, nicht
  übertragbar, nicht beleihbar, nicht veräußerbar und nicht kapitalisierbar***. **Each prohibition is a model instruction**:
  *nicht kapitalisierbar* removes the lump-sum option and any partial commutation; *nicht veräußerbar* removes the surrender
  value and the lapse-to-cash decrement; *nicht übertragbar* removes assignment; *nicht beleihbar* removes the policy loan; and
  *nicht vererblich* means that **on death before annuitisation the fund does not pass to the estate** — a Basisrente
  **without** a *Hinterbliebenenabsicherung* rider produces **no benefit at all** on pre-retirement death, which is why insurers
  sell the rider almost universally and why a delib BAS model must either carry it or say loudly that the base run assumes no
  death benefit. The permitted survivor class is narrow: spouse or registered partner, and children for as long as *Kindergeld*
  would be payable. **The ceiling, § 10 Abs. 3**, is not a fixed euro amount: since a reform reported as effective **1 January
  2015** it is the contribution that would be payable to the ***knappschaftliche Rentenversicherung*** on that scheme's own
  *Beitragsbemessungsgrenze*, **doubled for spouses assessed jointly**, and reduced by the employer's tax-free share of the
  statutory contribution and, for civil servants, by a *fiktiver Gesamtbeitrag*. The **deductible share phased in from 60 % in
  2005 by two percentage points a year**, and the **Jahressteuergesetz 2022 brought 100 % forward to 2023**. Candidate ceiling
  series, **every row `[unverified]`**, given with its arithmetic so it can be recomputed rather than believed: **2023** 107,400
  € × 24.7 % = **26,528 €**; **2024** 111,600 € × 24.7 % = **27,566 €**; **2025** 118,800 € × 24.7 % = **29,344 €**; **2026** a
  BBG of 124,800 € would give **30,826 €**. **For delib the deduction is not a cash flow of the contract** and no model computes
  it; it belongs in `product-spec.md` as the economic driver of premium behaviour, in particular the **year-end single-premium
  *Zuzahlung*** sized to the remaining headroom — so a BAS model that offers only a level regular premium models the wrong
  product.
- Not established: **the 24.7 % knappschaftliche rate, the 2015 switch, the pre-2015 flat 20,000 €, the 60 %/+2 pp phase-in
  path, the Jahressteuergesetz 2022 attribution, the *Satz* numbers within § 10 Abs. 3 and every BBG figure above are
  `[unverified]`** — none was corroborated by any search in this session. The **2026 BBG of 124,800 €** is a derived guess, not
  a figure. The reported **50 % limit on the share of the premium attributable to biometric riders** inside a Basisrente is
  `[unverified]` and its source (statute or BMF-Schreiben) is not established — it decides whether a BAS model may carry a large
  BU rider. Whether *Erwerbsminderungs-Basisrenten* are a separate *Produktgruppe* for transfer purposes is not established.
  Whether the **Öffnungsklausel** reaches a private Basisrente is **not established** and is material for high-contribution
  model points. **The whole ceiling series should be treated as `[std]` input candidates, not citations.**
- Read in the 2026-08-30 pass — **the five prohibitions are now a verbatim statutory quotation and the
  product shape is more detailed than this entry had it.** *"Die Ansprüche nach Buchstabe b dürfen nicht vererblich, nicht
  übertragbar, nicht beleihbar, nicht veräußerbar und nicht kapitalisierbar sein."* Doppelbuchst. aa requires *"nur die Zahlung einer
  monatlichen, auf das Leben des Steuerpflichtigen bezogenen lebenslangen Leibrente nicht vor Vollendung des 62. Lebensjahres"*, with
  optional BU, EMI and survivor cover, survivors being the spouse and *Kindergeld*-eligible children. **Two qualifications on
  *nicht kapitalisierbar*:** up to twelve monthly instalments may be paid together, and a *Kleinbetragsrente* under § 93 Abs. 3 EStG
  may be commuted, contracts at one provider being aggregated for that test; and *"Neben den genannten Auszahlungsformen darf kein
  weiterer Anspruch auf Auszahlungen bestehen."* **Doppelbuchst. bb is a second qualifying shape** — a stand-alone BU/EMI contract
  paying a lifelong monthly annuity for an insured event occurring up to completion of **age 67**, with benefit cessation on medically
  justified recovery and an age-dependent benefit permitted from age 55. **The ceiling, § 10 Abs. 3 Satz 1:** *"bis zu dem
  Höchstbeitrag zur knappschaftlichen Rentenversicherung, aufgerundet auf einen vollen Betrag in Euro"*, doubled for jointly assessed
  spouses. **Still `[unverified]`:** the age 60 for pre-2012 contracts — that transitional is in § 52, which was not read for this
  provision — and the euro value of the *Höchstbeitrag* for any year [R46].
- Products: BAS load-bearing; RIE, RLV, BU qualified — by contrast, for what is *not* deductible [R46].

### R40. ZPO §§ 850b and 851c — Pfändungsschutz and the shape it imposes on a Basisrente
- Publisher: Bundesamt für Justiz; two Brennecke practitioner articles, a Peter Lang monograph and a Prütting/Gehrlein
  commentary on Haufe as secondary. Doc type: statutory sections.
- URL: https://www.gesetze-im-internet.de/zpo/__850b.html and `__851c.html` (returned);
  https://www.buzer.de/gesetz/7030/al162722-0.htm (returned, the pre-2022 version of § 851c)
- Retrieved: **yes** — ZPO canonical XML, **Stand: zuletzt geändert Art. 2 G v. 22.12.2025 I Nr. 349**, read
  **2026-08-30**; §§ 850b, 851c and **851d** read in full. `gesetze-im-internet.de/zpo/__850b.html` is a 5.3 kB frameset shell;
  `buzer.de` serves the pre-2022 § 851c version, which is what the conflicting figures came from.
- Content: **§ 851c Abs. 1** — claims to benefits may be attached **only as earnings from employment** where **all** of the
  following hold: the benefit is granted **at regular intervals, for life, and not before the completion of the 60th year of
  age, or only on the occurrence of Berufsunfähigkeit**; the claims **may not be disposed of**; the **designation of third
  parties other than survivors as beneficiaries is excluded**; and **no capital payment other than on death has been agreed**.
  **§ 851c Abs. 2** — amounts saved in performance of such a contract to build an appropriate old-age provision are not
  attachable, subject to an **aggregate ceiling of 340,000 euro** and to annual limits. **§ 850b Abs. 1 Nr. 1** — pensions
  payable on account of injury to body or health, **including claims from a private Berufsunfähigkeitsversicherung**, are
  ***bedingt pfändbar***: attachable under the employment-earnings rules only if execution against other movable assets has not
  led and is not expected to lead to full satisfaction **and** attachment corresponds to *Billigkeit*. **Model consequence: BAS
  is defined by these conditions, not merely protected by them.** The four requirements of § 851c Abs. 1 are the same four
  features § 10 Abs. 1 Nr. 2 Buchst. b EStG demands [R39] and that § 168 Abs. 3 VVG makes non-terminable [R28]. Together —
  **three instruments, two research sweeps, one product description** — they mean a BAS model has **no surrender, no capital
  option except a death benefit, no third-party beneficiary except survivors, annuity commencement not before 60 in ZPO terms
  and not before 62 in tax terms, and no assignment**. That is a complete behavioural specification, and it is why BAS is the
  one delib product with **no lapse-to-cash decrement at all**. For BU, § 850b means a BU annuity in payment is conditionally
  attachable, which does not change the cash flow — and the notes should say so rather than leave the reader wondering.
- Not established: **the annual savings allowances of § 851c Abs. 2 are contradicted across summaries** — a **6,000 €/7,000 €**
  two-band ladder reported as current law "in effect since 1 January 2022" versus a **2,000 €–9,000 €** age-graded ladder
  reported as pre-2022. Both are recorded, **both `[unverified]` on the precise bands**; the 340,000 € aggregate is agreed. The
  amending instrument is reported only as "*geändert durch Artikel 1 G. v. 07.05.2021 BGBl. I S. 850*" in a URL title. **§ 851d
  ZPO** (the payout-phase counterpart) was named and never searched.
- Read in the 2026-08-30 pass — **the contested savings bands are settled.** § 851c Abs. 2 Satz 1: the amounts
  are unattachable so far as they do not annually exceed **6 000 Euro** for a debtor from 18 to the completed 27th year and
  **7 000 Euro** from 28 to the completed 67th, and do not exceed **340 000 Euro** in aggregate. **So the 6 000 / 7 000 two-band
  ladder is current law and the 2 000–9 000 age-graded ladder is the superseded version.** Two further rules: the amounts are re-set
  every fifth year on 1 July in the *Pfändungsfreigrenzenbekanntmachung*, and where the *Rückkaufwert* exceeds the unattachable amount
  **three tenths of the excess** are unattachable, except above three times 340 000 Euro. § 851c Abs. 1's four conditions are confirmed
  verbatim. **§ 851d**, new to this entry, makes monthly benefits from **tax-subsidised** retirement assets attachable *"wie
  Arbeitseinkommen"*. **Correction:** § 850b Abs. 1 Nr. 1 covers *"Renten, die wegen einer Verletzung des Körpers oder der Gesundheit
  zu entrichten sind"* and **does not name private *Berufsunfähigkeitsversicherung*** — that inclusion is case law and stays
  `[unverified]`. § 850b Abs. 1 Nr. 4 adds a figure: death-only life insurance claims are conditionally attachable where the sum
  assured does not exceed **5 400 Euro**.
- Products: BAS and BU load-bearing; RIE, KLV, RV, FRV, PFL qualified.

### R41. EStG § 22 Nr. 1 Satz 3 Buchst. a and § 55 EStDV — Besteuerungsanteil, Rentenfreibetrag and Ertragsanteil
- Publisher: Bundesministerium der Justiz. Doc type: statutory section plus the implementing regulation's § 55.
- URL: https://www.gesetze-im-internet.de/estg/__22.html and https://www.gesetze-im-internet.de/estdv_1955/__55.html — **both
  `[unverified canonical form]`**; the `/estg/__NN.html` pattern is evidenced by the sibling return of `__10.html`, the EStDV
  slug is a guess and is **the least reliable URL in this file**.
- Retrieved: **yes** — EStG canonical XML, **Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197** and EStDV 1955 canonical XML (**Stand: zuletzt geändert durch Art. 2 V v.
  19.12.2025 I Nr. 372**), read **2026-08-30**; § 22 Nr. 1 Satz 3 Buchst. a read in full **including both statutory tables**, and
  § 55 EStDV read in full **including its table**. Both per-section pages serve (48 kB and 21 kB). **This entry was previously a
  reconstruction with no corroboration at all.**
- Content: **Doppelbuchst. aa — the Schicht-1 rule.** Three mechanics, and the third is the one models and product documents get
  wrong. **(1) The *Besteuerungsanteil* is fixed by the year the pension starts, not by the year of receipt**, and one cohort
  table applies to the gesetzliche Rente, a Versorgungswerk pension and a private Basisrente alike. The reported path: **50 %
  for pensions beginning in or before 2005**, rising **two percentage points a year to 80 % for the 2020 cohort**, then **one
  point a year**, reaching 100 % with the 2040 cohort. **(2) The path was flattened in 2024**: the *Wachstumschancengesetz*
  reduced the annual step from 1 point to **0.5 point with effect from the 2023 cohort**, giving reported values of **82.5 %
  (2023), 83.0 % (2024), 83.5 % (2025), 84.0 % (2026)** and moving the 100 % endpoint to **2058**; the same act wound down the
  *Versorgungsfreibetrag* (§ 19 Abs. 2 EStG) and the *Altersentlastungsbetrag* (§ 24a EStG) on the same rhythm. **(3) The
  untaxed remainder is frozen in euro, for life.** The ***Rentenfreibetrag*** is computed **once**, in the year following the
  first full calendar year of receipt, as the euro amount not covered by the *Besteuerungsanteil*, and **stays at that euro
  amount for the whole duration** — so every subsequent increase, including every increase in the *Überschussrente*, is **fully
  taxable**. Illustration, figures illustrative only: a Basisrente of 12,000 € first paid in 2026 at 84.0 % has a
  *Rentenfreibetrag* of 1,920 € fixed for life; if surplus lifts the annuity to 15,000 € by 2040 the taxable amount is 13,080 €,
  i.e. **87.2 %**, not 84 %. **Doppelbuchst. bb — the Schicht-3 *Ertragsanteil*.** Only a fixed percentage of each payment,
  determined **once by the annuitant's completed age at annuity commencement and never changed**, is taxable; the remainder is a
  tax-free return of capital. The two anchors most often quoted, and the two this compiler would defend, are **age 65 → 18 %**
  and **age 60 → 22 %**; a fuller reported row (age → %) runs 50→30, 55→26, 60→22, 62→21, 63→20, 64→19, **65→18**, 67→17, 68→16,
  70→15, 72→13, 75→11, 80→8, 85→5. **The table is an actuarial artefact, not a policy dial** — a present-value split of a life
  annuity on an assumed interest rate reported to have been cut from **5.5 % to 3 %** in 2005 — and, unlike the
  *Rentenfreibetrag*, it is the **percentage** that is frozen, so surplus increases to a Schicht-3 annuity are taxed at the same
  light rate. **That asymmetry is the whole economic case for SOF** [R38]. **§ 55 EStDV** supplies a **second table keyed to the
  annuity's remaining term** for an ***abgekürzte Leibrente*** — which is what a *Berufsunfähigkeitsrente* from a *selbständige*
  BU contract is, taxed far more lightly than an equivalent lifelong annuity. **Where a BU annuity is written inside a
  Basisrente the treatment is different again**, falling into Schicht 1 and taxed on the *Besteuerungsanteil* — so the **same
  biometric benefit is taxed two different ways depending on the wrapper**, which a BU product specification must state.
- Not established: **the entire Besteuerungsanteil cohort table, the entire Ertragsanteil row and every row of the § 55 EStDV
  table are `[unverified]` reconstructions**, corroborated by no search result. The rule that the *Rentenfreibetrag* is fixed in
  the **second** year is general knowledge. Whether the *Ertragsanteil* age is the completed year at commencement or at the
  start of the calendar year is not established and would shift a boundary case by one row. Whether the table sits in the
  statute or an annex is not established. **delib publishes gross cash flows and computes no tax**; what the BAS, SOF and BU
  notes owe the reader is the statement that the *tax* profile of the published stream is **not flat**, and that any net-of-tax
  analysis must apply a **frozen euro allowance** in Schicht 1 and a **frozen percentage** in Schicht 3.
- Read in the 2026-08-30 pass — **both tables are now the statute's own.** **Besteuerungsanteil by year of
  *Rentenbeginn*:** bis 2005 **50,0**; 2006 52,0; 2007 54,0; 2008 56,0; 2009 58,0; 2010 **60,0**; 2011 62,0; 2012 64,0; 2013 66,0;
  2014 68,0; 2015 70,0; 2016 72,0; 2017 74,0; 2018 76,0; 2019 78,0; 2020 **80,0**; 2021 81,0; 2022 82,0; **2023 82,5** and half-point
  steps thereafter — 2024 83,0; 2025 83,5; 2026 84,0; … 2030 86,0; … — to **2058 100,0**. The reported shape, including the flattening
  from the 2023 cohort and the 2058 endpoint, is confirmed exactly; the attribution to the *Wachstumschancengesetz* is not in the
  consolidated text and stays `[unverified]`. **The *Rentenfreibetrag* mechanics are more qualified than this entry said:** Satz 5
  freezes the tax-free part *"ab dem Jahr, das dem Jahr des Rentenbeginns folgt, für die gesamte Laufzeit"*, but **Satz 6** adjusts it
  proportionally on a change in the annual amount and **Satz 7** provides *"Regelmäßige Anpassungen des Jahresbetrags der Rente führen
  nicht zu einer Neuberechnung und bleiben bei einer Neuberechnung außer Betracht."* — so "every increase is fully taxable" holds for
  *regelmäßige Anpassungen*, and whether a surplus-driven increase is one is `[unverified]`. **Ertragsanteil:** the table is keyed to
  the *"Bei Beginn der Rente **vollendetes Lebensjahr**"*, which answers the open question; it runs 59 % at ages 0–1 down to 1 % from
  97, with **65–66 → 18 %** and **60–61 → 22 %** confirmed and neighbours 62 → 21, 63 → 20, 64 → 19, 67 → 17, 68 → 16, 69–70 → 15.
  **§ 55 Abs. 2 EStDV** supplies the *abgekürzte Leibrenten* table keyed to the remaining term, 97 % at three years down to 2 % at 59,
  with a third column falling back to the § 22 age table.
- Products: RV, FRV, IDX, BAS, SOF, BU load-bearing; KLV, RIE, PFL qualified.

### R42. EStG § 10a and Abschnitt XI (§§ 79–99) — the Riester subsidy machinery
- Publisher: Bundesministerium der Justiz; the **Zentrale Zulagenstelle für Altersvermögen (ZfA)** at the Deutsche
  Rentenversicherung Bund as administering body. Doc type: statutory sections.
- URL: https://www.gesetze-im-internet.de/estg/__10a.html ; `__79.html` ; `__84.html` ; `__85.html` ; `__86.html` ; `__93.html`
  — **all `[unverified canonical form]`**; the contract sweep records explicitly that **no `/estg/__93.html` page was returned**
  by either of its two *Kleinbetragsrente* queries, twelve secondary hosts being returned instead.
- Retrieved: **yes** — EStG canonical XML, **Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197**, read **2026-08-30**; §§ 10a, 79, 82, 83, 84, 85, 86 and 93 read in full.
  `gesetze-im-internet.de/estg/__10a.html` serves in full (17 kB). **Every euro figure in this entry was previously
  `[unverified]`.**
- Content: **§ 10a — the deduction and the *Günstigerprüfung*.** Contributions to a certified *Altersvorsorgevertrag*, **plus
  the Zulagen credited to it**, are deductible as *Sonderausgaben* up to **2,100 € a year**, reportedly unchanged since 2008.
  The tax office computes both the tax saved and the *Zulagenanspruch* of its own motion and grants the better; if the deduction
  wins the taxpayer receives the **difference** as a reduction of assessed tax and **the Zulagen already paid stay in the
  contract**. **This split is the single most important thing a RIE model author must understand: only the Zulage is a contract
  cash flow; the Günstigerprüfung top-up is a personal tax refund and never touches the policy.** **§ 79 — entitlement.**
  *Unmittelbar Zulageberechtigte* are broadly those compulsorily insured in the statutory scheme plus *Beamte* and recipients of
  wage-replacement benefits; **the self-employed not compulsorily insured and berufsständisch pensioned professionals are
  excluded** — precisely the population Basisrente serves, so **the two subsidised products are complements addressed to
  different people, not competitors**. *Mittelbar Zulageberechtigte* are the spouse or partner of an entitled person holding
  their **own** certified contract, who since a change reported as effective **2012** must pay at least the ***Sockelbeitrag* of
  60 € a year** — producing a real contract type, **a 60 € annual premium receiving a 175 € Grundzulage**, whose omission would
  leave a RIE model point table missing an economically extreme part of the book. **§§ 83–85 — the Zulagen.** ***Grundzulage***
  **175 €** a year (reportedly since **2018**; 154 € from 2008 to 2017); ***Kinderzulage*** **185 €** per child receiving
  *Kindergeld*, or **300 €** where the child was **born on or after 1 January 2008**, credited by default to the **mother's**
  contract; a one-off ***Berufseinsteiger-Bonus*** of **200 €** where the entitled person has not completed their 25th year at
  the start of the first *Beitragsjahr*. **§ 86 — the *Mindesteigenbeitrag***: `min(4 % × previous year's beitragspflichtige
  Einnahmen, 2,100 €)` **less the *Zulagenanspruch***, floored at **60 €**. Three features drive behaviour: the **prior-year
  income base**, so keying the premium to current salary is wrong after any income step; the **subtraction of the Zulage**, so a
  two-child household on modest earnings owes only the floor; and — the real trap — **the Kürzung is proportional, not a
  cliff**, the Zulage being reduced **in the ratio of the contribution paid to the Mindesteigenbeitrag**, so a model treating it
  as all-or-nothing produces a discontinuity that does not exist. **The ZfA**: application is **through the provider**, normally
  once by a *Dauerzulagenantrag*; the ZfA checks entitlement against the pension scheme's own earnings and Kindergeld data and
  **pays to the provider**, who credits the contract; claims run up to **two years** back; and a later finding of no entitlement
  triggers a **reclaim**, so a RIE contract can carry a **negative Zulage cash flow**. **The Zulage for year *t* is typically
  credited in *t+1***, so an annual-step model must state its choice **in the processing order**; crediting in *t* overstates
  the fund and its interest. **§§ 93–94 — *schädliche Verwendung*.** Using subsidised capital other than as permitted —
  surrender, capital beyond the permitted 30 %, benefits before the earliest age, transfer to a non-certified vehicle — triggers
  repayment of the **Zulagen and the § 10a tax advantage**, withheld by the provider. **This is the behavioural heart of a RIE
  model**: the contract is legally terminable, unlike BAS, but terminating costs the entire subsidy history, so **the RIE lapse
  assumption should be materially below the RV/FRV assumption with this rule stated as the reason**; a lapse produces a
  *Rückkaufswert* **net of the Rückzahlungsbetrag**, a different quantity from the § 169 VVG value; and **a paid-up election is
  not *schädlich***, so the natural RIE decrement is *ruhend stellen*, not surrender. **§ 93 Abs. 3 — the *Kleinbetragsrente***:
  an annuity below a threshold expressed as a percentage of the ***monatliche Bezugsgröße nach § 18 SGB IV*** may be commuted at
  the start of the payout phase **without being *schädlich***, for **Riester and Basisrente alike**, reportedly at the reduced
  rate of § 34 EStG. **The threshold is contested**: **Account A** — 1 % of the monthly Bezugsgröße, **39.55 €/month** on a 2026
  figure of 3,955 €, with 1.5 % only from 2027; **Account B** — amended by the *Altersvorsorgereformgesetz* of 26 May 2026 so
  that **1.5 %** applies **from June 2026**, i.e. **59.33 €/month**. **They cannot both be right; delib picks one, tags it
  `**[std]**` and prints both.** For a small contract the commutation branch is the **modal outcome**, so both RIE and BAS need
  a commutation test at annuitisation and a model point that trips it. Two further exits that are **not** *schädlich* and are
  real decrements from an insurance-based book: the **Wohn-Riester** *Altersvorsorge-Eigenheimbetrag* (§ 92a) and
  *Tilgungsförderung* (§ 82 Abs. 1 Satz 1 Nr. 2), with deferred tax collected through a ***Wohnförderkonto*** rolled up at a
  notional **2 %** a year and taxed either successively to age 85 or in one sum with a **30 % discount**. delib implements
  neither; the RIE specification names them and notes that a real book's persistency is worse than a pure-lapse model suggests.
- Not established: **every figure above** — the 2,100 € ceiling and its freeze, the 175 / 185 / 300 / 200 / 60 € amounts and
  dates, the 4 % rate and its phase-in, the definition of *beitragspflichtige Einnahmen* for non-employees, the two-year window
  and the reclaim mechanism, the §§ 89–91 attributions, the composition of the *Rückzahlungsbetrag* and the whole § 94
  procedure, the § 34 treatment, the **2026 Bezugsgröße of 3,955 €/month** (two secondary sources, neither official, and
  unsettled as between the bundeseinheitliche and the West figure), and every Wohn-Riester parameter. **§ 93 EStG's statutory
  text was never returned by any sweep.**
- Read in the 2026-08-30 pass — **every figure is now statutory, and the contested *Kleinbetragsrente*
  threshold is settled.** § 10a Abs. 1 Satz 1: *"Altersvorsorgebeiträge (§ 82) zuzüglich der dafür nach Abschnitt XI zustehenden
  Zulage jährlich bis zu **2 100 Euro** als Sonderausgaben abziehen"*. § 84 Satz 1: *"diese beträgt ab dem Beitragsjahr 2018 jährlich
  **175 Euro**"*, Satz 2 adding *"einmalig **200 Euro**"* for those under 25 at the start of the *Beitragsjahr*. § 85 Abs. 1:
  **185 Euro** per child, **300 Euro** for a child born after 31 December 2007, allocated to the mother by default (Abs. 2). § 79
  Satz 2 Nr. 4: the *mittelbar* entitled spouse must pay **at least 60 Euro** into their own contract. § 86 Abs. 1 Satz 2: 4 per cent
  of the prior year's income *"jedoch nicht mehr als der in § 10a Absatz 1 Satz 1 genannte Höchstbetrag, vermindert um die Zulage nach
  den §§ 84 und 85"*, Satz 4 the **60 Euro** *Sockelbetrag*, and **Satz 6 settles the proportionality trap in one sentence:**
  *"Die Kürzung der Zulage ermittelt sich nach dem Verhältnis der Altersvorsorgebeiträge zum Mindesteigenbeitrag."* **§ 93 Abs. 3
  Satz 2 Nr. 1** defines a *Kleinbetragsrente* by **1,5 Prozent der monatlichen Bezugsgröße nach § 18 SGB IV**, and Nr. 2 adds an
  *Auszahlungsplan* variant **ab dem 1. Januar 2027 on the same 1,5 per cent** — **so 1.5 per cent is the rate in force now and the
  2027 date attaches to the payout-plan variant, not to the rate.** **§ 82 Abs. 1** defines *geförderte Altersvorsorgebeiträge* as
  contributions *"die der Zulageberechtigte ... leistet"*, which is the definition the *Beitragsgarantie* question at [R43] turns on.
  **Still `[unverified]`:** the euro *Bezugsgröße* for any year [R46], and the *t+1* Zulage crediting convention.
- Products: RIE load-bearing; FRV and BAS qualified.

### R43. AltZertG, the BZSt, the AltvPIBV and the Produktinformationsstelle Altersvorsorge
- Publisher: Bundesministerium der Justiz; **Bundeszentralamt für Steuern (BZSt)** as *Zertifizierungsstelle*; Bundesministerium
  der Finanzen; **Produktinformationsstelle Altersvorsorge gGmbH (PIA)**; a DAV article, a Springer *ZVersWiss* paper, an ifa
  Ulm note and Fraunhofer ITWM's ALMSIM page as secondary. Doc type: certification statute; regulation; standardised
  product-information regime.
- URL: https://www.gesetze-im-internet.de/altzertg/BJNR132200001.html and `.../__1.html`, `.../__7.html` (returned);
  https://www.buzer.de/gesetz/2399/a182166.htm (returned, § 2a *Kostenstruktur*);
  https://www.gesetze-im-internet.de/altvpibv/__5.html (returned);
  https://www.bzst.de/SharedDocs/Downloads/DE/Zertifizierungsstelle/Kommentar_AltZertG_201706.pdf?__blob=publicationFile&v=6
  (returned, the BZSt's own *Kommentar zum AltZertG*, June 2017); https://produktinformationsstelle.de/ and
  `.../chancen-risiko-klassen/` (returned);
  https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Weitere_Steuerthemen/Altersvorsorge/2019-03-14-Produktinformationsblatt-AltZertG-Muster-gemaess-AltvPIBV.pdf?__blob=publicationFile&v=4
  (returned, the BMF *Muster-Produktinformationsblatt* of 14 March 2019). `.../altzertg/__5a.html` is **`[unverified canonical
  form]`** and was **not** returned.
- Retrieved: **yes for the statute** — AltZertG canonical XML, **Stand: zuletzt geändert durch Art. 5 G v.
  25.10.2023 I Nr. 294**, with Artt. 5–7 G v. 26.5.2026 I Nr. 156 recorded as *textlich nachgewiesen, dokumentarisch noch nicht
  abschließend bearbeitet* [R44]; §§ 1, 2, 2a and 5a read in full, **2026-08-30**. The `BJNR132200001.html` index page serves
  (100 kB) and `buzer.de/gesetz/2399/a182166.htm` serves for § 2a. **Not retrieved:** the AltvPIBV beyond its section list
  (`altvpibv/__5.html` is a 7.5 kB shell), the **BZSt commentary PDF** (which does serve, 1.25 MB, but was not read), the
  **BMF *Muster*-PIB** (which does serve, 1.10 MB, but was not read) and any **PIA determination** (`produktinformationsstelle.de`
  serves, 36 kB, but no *Allgemeinverfügung* was opened).
- Content: Riester and Basisrente are **certified product categories under a statute of their own**, and certification is a
  *product* approval, not a *tax* ruling. The AltZertG defines what an *Altersvorsorgevertrag* (§ 1) and a *Basisrentenvertrag*
  (§ 5a) must contain; the **BZSt** issues the certificate — reported to have moved from BaFin to the BZSt on **1 July 2010** —
  and §§ 10a and 79 ff. EStG then hang the subsidy on it. **§ 1 fixes four features that are all model instructions.** **(a)
  *Beitragsgarantie* (§ 1 Abs. 1 Nr. 3):** the provider must guarantee that **at the beginning of the payout phase at least the
  paid-in *Altersvorsorgebeiträge* are available** for the payout phase, with **up to 20 % of total contributions** left out of
  account where they secure *Erwerbsminderung*, *Berufsunfähigkeit* or *Hinterbliebene*. This is a **100 % money-back guarantee
  at retirement**, and it is why a German Riester insurance contract is invested so conservatively and became hard to sell at a
  0.25 % *Höchstrechnungszins* [R15]. For a RIE model it is a **floor on the fund at annuitisation**, evaluated as `max(fund,
  sum(premiums) + sum(zulagen) − biometric_carve_out)`. **(b) Earliest payout: age 62** (60 for contracts before 2012), the same
  boundary as [R39] and [R45]. **(c) The payout shape (§ 1 Abs. 1 Nr. 4):** a **lebenslange Leibrente**, or an *Auszahlungsplan*
  followed by a **Teilkapitalverrentung from at the latest age 85**, with a **Teilkapitalauszahlung of up to 30 % of the
  available capital** available **at the beginning of the payout phase only**. **(d) Cost structure and switching:** § 2a
  enumerates the cost types that may be charged and requires the individual PIB to break them down by **§ 2a Satz 1 Nr. 1
  Buchst. a bis f** and **Nr. 2 Buchst. a bis c** — so **a certified product's charge structure is enumerated by statute and a
  RIE charge table can be built from published PIBs in a way a Schicht-3 charge table cannot**; § 1 Abs. 1 Nr. 8 is reported to
  require *Abschluss- und Vertriebskosten* to be spread over **at least five years**; and § 1 Abs. 1 Nr. 10 Buchst. b carries a
  ***Wechselrecht*** to transfer the *Altersvorsorgevermögen* to another certified contract, expressly **not** a *schädliche
  Verwendung*, on a reported **three months to the end of a quarter** notice, with a reported cap on the transferring provider's
  *Wechselkosten* (**150 €**) and acquisition costs chargeable by the receiving provider on **only 50 %** of the transferred
  capital. **The AltvPIBV and the PIA.** Since **1 January 2017** providers of Basisrente and Riester must use a **uniform,
  individual *Produktinformationsblatt***, introduced by the *Altersvorsorge-Verbesserungsgesetz* and governed by the AltvPIBV,
  delivered **in good time and at the latest before the customer's declaration of intent**, with **provable receipt**. It
  discloses ***Effektivkosten*** — reported as the difference **r\* − r_k**, the reduction in the achievable return caused by
  costs — computed **individually for each contract offer** under § 7 Abs. 1 AltZertG with § 9 Abs. 1 AltvPIBV, a stronger duty
  than the product-level VVG-InfoV figure [R31]; and it assigns the product to **one of five *Chancen-Risiko-Klassen*** under §
  5 AltvPIBV, **CRK 1** the least risky and least remunerative and **CRK 5** high opportunity and high risk, determined **by the
  PIA on behalf of the BMF** by examining the product for a *Modellkunde* **under various capital-market scenarios over a
  comparable savings period**. **This is a genuinely unusual feature of the German market with no counterpart in `uslib`,
  `uklib`, `jplib` or `frlib`: a public body assigns a risk class using a stochastic model the insurer does not control.**
  **delib does not implement the PIA simulation.** A RIE or BAS specification may **report** a published CRK and Effektivkosten
  as `[S#]` facts about the reference product and must say that reproducing either requires the PIA's scenario set, which is
  neither public nor in scope — exactly the "cited, not specified" boundary the library draws around discounting and capital.
- Not established: **the text of § 5a AltZertG was never retrieved by any sweep** — only its existence and its § 168 Abs. 3 VVG
  cross-reference [R28] are established; its conditions, its relationship to § 1 and whether it imposes cost-disclosure duties
  of its own are **not established**. The act's date (reported 26 June 2001), the **1 July 2010** BaFin→BZSt transfer, and the
  reported **1 January 2010** start of compulsory Basisrente certification are `[unverified]`. The **20 %** biometric carve-out
  rests on **one** summary. **Whether the *Beitragsgarantie* covers the *Zulagen* as well as the contributions is not settled**
  — one summary says yes, another implies it, the statutory text obtained does not decide it — and this is **the single most
  material unresolved ambiguity for a delib model**, since for a two-child model point it moves the guarantee floor by thousands
  of euro over thirty years; it must be a `**[std]**` choice with both readings printed. The **150 € Wechselkosten cap, the 50 %
  rule, the five-year spreading and the three-month notice are all `[unverified]`**. The **definitions of r\* and r_k and the
  CRK class boundaries are not established**; whether the PIA *Allgemeinverfügung* of 2022 is the operative determination is
  ambiguous; the BMF Muster PIB is dated 14 March 2019 and may have been superseded. Whether the PIB regime reaches Schicht-3
  products is not established — the sources describe it as *geförderte*-only.
- Read in the 2026-08-30 pass — **one correction and five confirmations.** **Correction: § 5a is not the
  definition of a *Basisrentenvertrag*.** It is a one-sentence procedural provision — *"Die Zertifizierungsstelle erteilt die
  Zertifizierung nach § 2 Abs. 3, wenn ihr die nach diesem Gesetz erforderlichen Angaben und Unterlagen vorliegen sowie die
  Vertragsbedingungen des Basisrentenvertrags dem § 2 Absatz 1 oder Absatz 1a sowie dem § 2a entsprechen und der Anbieter den
  Anforderungen des § 2 Absatz 2 entspricht."* **The substantive definition is § 2**, whose Abs. 1 simply incorporates § 10 Abs. 1
  Nr. 2 Buchst. b Doppelbuchst. aa EStG, and whose **Abs. 1a defines the Basisrente-Erwerbsminderung** with a twelve-month prognosis,
  six-hour and three-hour thresholds, at least half the benefit on partial incapacity, backdating capped at 36 months, interest-free
  premium deferral during claims assessment, and a waiver of the § 19 Abs. 3 Satz 2 and Abs. 4 VVG rights. **Confirmed:** the
  *Beitragsgarantie* of § 1 Abs. 1 Nr. 3 on *"die eingezahlten Altersvorsorgebeiträge"* with *"bis zu 20 Prozent der Gesamtbeiträge"*
  left out where used for biometric cover; **age 62** and the statutory unisex requirement in § 1 Abs. 1 Nr. 2; the payout shape of
  § 1 Abs. 1 Nr. 4 Buchst. a — lifelong annuity or *Auszahlungsplan* with *Teilkapitalverrentung* from at latest age 85, benefits that
  *"müssen während der gesamten Auszahlungsphase gleich bleiben oder steigen"*, up to twelve instalments combinable, a
  *Kleinbetragsrente* commutable with a **four-week** deferral right, and *"bis zu 30 Prozent des zu Beginn der Auszahlungsphase zur
  Verfügung stehenden Kapitals"* payable outside the monthly benefits; and the § 2a enumeration of permitted cost types, which applies
  to **both** contract types. **On the *Zulagen* question the pass narrows without closing:** § 1 Abs. 1 Nr. 3 guarantees
  *Altersvorsorgebeiträge*, and § 82 Abs. 1 EStG defines those as contributions *"die der Zulageberechtigte ... leistet"* [R42] —
  which on its face excludes the state *Zulagen* — but the AltZertG does not cross-refer to § 82 EStG and no authority was retrieved,
  so it stays the section's most material `[std]` choice. **Still `[unverified]`:** the act's date, the BaFin→BZSt transfer, the
  AltvPIBV's content, the CRK scale and boundaries, and the *Wechselkosten* cap.
- Products: RIE and BAS load-bearing; RV, FRV, IDX qualified for cost-disclosure contrast.

### R44. The Altersvorsorgereformgesetz 2026 and the Altersvorsorgedepot
- Publisher: Deutscher Bundestag / Bundesrat / Bundesministerium der Finanzen; Deutsche Rentenversicherung. Doc type: federal
  statute and its parliamentary papers.
- URL: https://dserver.bundestag.de/btd/21/040/2104088.pdf (returned, **BT-Drs. 21/4088,
  21. Wahlperiode, 11.02.2026**); https://www.bundestag.de/dokumente/textarchiv/2026/kw13-de-altersvorsorge-1156798 (returned,
      *Bundestag beschließt das Altersvorsorgedepot*);
      https://www.deutsche-rentenversicherung.de/DRV/DE/Ueber-uns-und-Presse/Presse/Meldungen/2026/260508-bundesrat-reform-private-altersvorsorge
      (returned); https://www.bundesfinanzministerium.de/Content/DE/FAQ/reform-der-privaten-altersvorsorge.html (returned);
      https://www.bundesregierung.de/breg-de/aktuelles/reform-private-altersvorsorge-2400072 (returned)
- Retrieved: **yes for the official explanatory material** — the **DRV release of 8 May 2026** (HTML, 148 kB), the
  **BMF FAQ** (313 kB), the **Bundesregierung Q&A** (123 kB), the **Bundestag text archive** entry (508 kB) and the **Bundestag
  drucksache 21/4088** (PDF, 1.25 MB), all read **2026-08-30**. **The Act's own text was not retrieved.**
- Content: **Riester is closed.** The **Bundesrat approved the *Altersvorsorgereformgesetz* on 8 May 2026**, so it entered into
  force on publication in the Bundesgesetzblatt, and **the new state-subsidised private provision starts on 1 January 2027**.
  From 2027 the Riester-Rente is **replaced by a new subsidised model**, described by the Federal Government as more flexible,
  cheaper and higher-yielding, whose central new vehicle the Bundestag's own text archive names the ***Altersvorsorgedepot***. A
  provider-side page discusses whether to let an existing Riester contract lie dormant or switch, which **implies
  grandfathering**. **This changes what a delib `riester_rente` model *is***: a model of a product **closed to new business from
  1 January 2027** with a very large in-force book whose contractual rights survive. That is worth building — a closed book is
  exactly what a liability cash flow model is for — but the `product-spec.md` must say it plainly rather than present the
  product as current, and it means the *Beitragsgarantie* of [R43] is a feature of the **legacy** contract.
- Not established: **the enactment date is contradictory** — one summary refers to an act "vom 26.05.2026" while these sources
  give Bundesrat consent on 8 May 2026; reconcilable (consent then promulgation) but **neither the BGBl citation nor the
  promulgation date is established**, and both are `[unverified]`. **The substance of the Altersvorsorgedepot — contribution
  limits, subsidy rates, whether the *Beitragsgarantie* survives, payout rules, whether insurance products remain eligible — was
  not established by any search.** Whether existing Riester contracts may be continued, must be frozen or may be transferred is
  **not established** beyond an inference from one provider page. The earlier stages (a BMF *Fokusgruppe private Altersvorsorge*
  reporting in 2023 and a lapsed 2024 *pAV-Reformgesetz* Referentenentwurf) and the reported design of a proportional subsidy
  are general knowledge and `[unverified]`. The **Frühstart-Rente** discussed in the same debate was never searched.
- Read in the 2026-08-30 pass — **the enactment contradiction is resolved, from two directions.** The DRV
  states *"Der Bundesrat hat am 8. Mai 2026 dem Gesetz zur Reform der steuerlich geförderten privaten Altersvorsorge
  (Altersvorsorge-Reformgesetz) zugestimmt"*, and **the consolidated statutes give the promulgation**: the VVG's `Stand` reads
  *"zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156"* and the AltZertG carries Artt. 5–7 of the same act — so the Bundesrat
  consented on **8 May 2026** and the Act is the **Gesetz vom 26. Mai 2026, BGBl. 2026 I Nr. 156**. The two dates were never in
  conflict. **The new regime's shape:** free choice between a lifelong annuity and an *Entnahmeplan*; products with an **80 % or a
  100 % *Beitragsgarantie*** or a standard product; ***Altersvorsorgedepots* without guarantees and without a lifelong payout**, with
  a **20-year payout phase from age 65** ending at 85; and eligibility extended to the **self-employed and members of
  *Versorgungswerke***. **The new subsidy formula:** a *Grundzulage* of **50 cent per euro up to 360 Euro**, then **25 cent per euro
  on a further 1 440 Euro**, so **up to 540 Euro**; a *Kinderzulage* of **1 Euro per euro up to 300 Euro per child**; and a
  *Sonderausgabenabzug* of at most **1 800 Euro plus the Zulagenanspruch**. **Grandfathering is explicit:** *"Bestehende
  Riester-Verträge laufen weiter! Es gibt einen Bestandsschutz für diese Verträge."*, with an optional switch by declaration and no
  clawback — but taking out a new contract alongside an old one applies the new rules to the old one automatically. **Still
  `[unverified]`:** the Act's text and article structure, and every transitional date beyond 1 January 2027.
- Products: RIE load-bearing; BAS, RV, FRV qualified.

### R45. EStG § 20 Abs. 1 Nr. 6 — the Unterschiedsbetrag, the 12/62 rule and the Mindesttodesfallschutz
- Publisher: Bundesministerium der Justiz; the BMF *Einkommensteuer-Handbuch* for the annex; NWB, IWW, Haufe, smartsteuer and
  Gonze & Schüttler as secondary. Doc type: statutory section plus administrative guidance.
- URL: https://esth.bundesfinanzministerium.de/esth/2024/C-Anhaenge/Anhang-22a/I/inhalt.html (returned);
  https://datenbank.nwb.de/Dokument/357065/ (returned);
  https://www.haufe.de/steuern/steuerwissen-tipps/nach-dem-31122004-abgeschlossene-lebensversicherungen_170_448252.html
  (returned);
  https://www.haufe.de/finance/haufe-finance-office-premium/kapitallebensversicherungen-einkommensteuer-312-mindesttodesfallschutz-bei-lebensversicherungen_idesk_PI20354_HI8459274.html
  (returned);
  https://www.iww.de/wvm/archiv/kapitallebensversicherungen-neuer-mindesttodesfallschutz-fuer-ab-dem-1-april-2009-abgeschlossene-vertraege-f14610
  (returned). The statutory page `https://www.gesetze-im-internet.de/estg/__20.html` is **`[unverified canonical form]`**.
- Retrieved: **yes** — EStG canonical XML, **Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197**, read **2026-08-30**; § 20 Abs. 1 Nr. 6 read in full (nine Sätze) together with the
  relevant sentences of § 52 Abs. 28. `gesetze-im-internet.de/estg/__20.html` serves in full (33 kB). The BMF handbook annex at
  `esth.bundesfinanzministerium.de` returns a Radware interstitial rather than the annex and is **not** a retrieval; the Haufe, IWW
  and NWB commentaries serve.
- Content: the tax rule that decides when a German endowment or unit-linked contract is cashed in, and therefore the shape of
  every Schicht-3 lapse assumption in delib. **The base**: the taxable amount is the ***Unterschiedsbetrag* between the
  *Versicherungsleistung* and the sum of the *Beiträge* paid on it** — a gain measure, taking no account of inflation. **The
  half-income rule**: where the benefit is paid **after completion of the 60th year of life** and **at least twelve years after
  conclusion**, **only half the *Unterschiedsbetrag*** is taxable; for contracts concluded **after 31 December 2011** the age is
  **62**. **The rate**: where the halving applies to a benefit accruing from 1 January 2009, the flat *Abgeltungsteuer* does
  **not** apply — **§ 32d Abs. 2 Nr. 2 EStG** puts the half amount into the **personal marginal rate**. **The
  Mindesttodesfallschutz**: a contract concluded from **1 April 2009** qualifies for the half-income treatment **only if the
  *Todesfallleistung* is at least 50 % of all premiums payable over the whole term**; failing the test the earnings are taxed
  **in full under the Abgeltungsteuer with no halving**. **What this does to a model**: it creates a **duration-12 and age-60/62
  double threshold** that policyholders wait for, so a KLV, RV, FRV or IDX lapse assumption that is flat in duration has ignored
  the strongest single driver of German surrender behaviour — surrenders are suppressed approaching duration 12 and spike at it,
  and again at the age threshold. The effect is directly analogous to the eight-year threshold that drives French *assurance
  vie* behaviour, and **delib models it the same way frlib does — as a duration-dependent lapse shape with the threshold named
  and the level `**[std]**`**. The rule reaches RV, FRV and IDX too, because a deferred annuity whose *Kapitalwahlrecht* is
  exercised for cash is taxed here while the same contract annuitised is taxed on the *Ertragsanteil* [R41] — **the
  annuitise-or-commute election is therefore a tax election**, and a model treating it as a fixed take-up rate says that the
  rate stands in for a tax comparison it does not perform. And the 50 %-Regel is a **model-point design constraint**: a KLV, FRV
  or IDX representative product must carry a death benefit above the floor, and a point with a very short term or a very high
  single premium relative to the sum assured may breach it — **a model point that would fail the German tax test is not
  representative of a real sold contract.**
- Not established: the § 52 locus for the age-62 rule (§ 52 has been renumbered repeatedly); whether the twelve years run from
  *Vertragsschluss* or from the first premium; the treatment of late *Zuzahlungen*; the *Satz* number carrying the
  Mindesttodesfallschutz and its introducing act (reported as the *Jahressteuergesetz 2009*); a reported **second condition**
  that on death the agreed benefit must exceed the *Deckungskapital* or *Zeitwert* by at least **10 %** — the summary attached
  the words "after five years", which does not parse as a rule, so **the 10 % figure is recorded and its base, time profile and
  qualifier are `[unverified]`**; and whether the 50 % is measured against premiums *payable* or *paid* for a contract that
  lapses early. The **pre-2005 cohort's qualifying conditions** — a twelve-year term, a five-year minimum premium-paying period
  and a minimum death cover as a percentage of the *Beitragssumme* — **were not established by any search result, are
  `[unverified]`, and are not asserted anywhere in delib**; what can be said is that for contracts concluded before 1 January
  2005 the *rechnungsmäßige und außerrechnungsmäßige Zinsen* were entirely free of income tax on maturity, which is why an
  *Altvertrag* has an almost nil lapse rate and why a KLV document must say the reference model does not represent that cohort.
  The **Abgeltungsteuer** rate of 25 % plus the 5.5 % *Solidaritätszuschlag* and 8/9 % *Kirchensteuer*, the § 43 withholding
  mechanism and the *Sparer-Pauschbetrag* are all `[unverified]`. The **InvStG *Teilfreistellung*** reported at **15 %** of
  gains attributable to equity-fund units inside a *fondsgebundene* contract, giving a composite taxable share of about **42.5
  %**, is **general knowledge throughout, uncorroborated, and the weakest claim in this section**; an FRV specification may name
  it only with the tag.
- Read in the 2026-08-30 pass — **the twelve-year start point, the 60→62 transitional and the second limb of
  the *Mindesttodesfallschutz* are all resolved.** Satz 2: *"Wird die Versicherungsleistung nach Vollendung des 60. Lebensjahres des
  Steuerpflichtigen und nach Ablauf von zwölf Jahren **seit dem Vertragsabschluss** ausgezahlt, ist die Hälfte des
  Unterschiedsbetrags anzusetzen."* — **so the twelve years run from *Vertragsschluss***. **§ 52 Abs. 28 Satz 7:** *"§ 20 Absatz 1
  Nummer 6 Satz 2 ist für Vertragsabschlüsse nach dem 31. Dezember 2011 mit der Maßgabe anzuwenden, dass die Versicherungsleistung
  nach Vollendung des 62. Lebensjahres des Steuerpflichtigen ausgezahlt wird."* — 12/60 for 2005–2011 contracts, 12/62 from 2012.
  **Satz 6 is a two-limbed cumulative test**, and the "reported second condition" this entry could not parse is limb (b): Satz 2 is
  disapplied where **(a)** the death benefit is *"weniger als 50 Prozent der Summe der für die gesamte Vertragsdauer zu zahlenden
  Beiträge"* **and (b)** it does not exceed the *Deckungskapital* or *Zeitwert* *"spätestens fünf Jahre nach Vertragsabschluss ... um
  mindestens 10 Prozent"* of the *Deckungskapital*, the *Zeitwert* or the premiums paid, that 10 per cent being allowed to fall to
  zero in equal annual steps. **§ 52 Abs. 28 Satz 8** dates Satz 6 to contracts *"die nach dem 31. März 2009 abgeschlossen werden"*.
  **Two sentences new to this entry:** Satz 5 treats a *vermögensverwaltender Versicherungsvertrag* as transparent, and **Satz 9**
  makes **15 per cent of the *Unterschiedsbetrag* tax-free for *fondsgebundene Lebensversicherungen*** so far as it stems from
  *Investmenterträge*. **Still `[unverified]`:** the § 32d Abs. 2 Nr. 2 interaction, which was not read.
- Products: KLV, RV, FRV, IDX load-bearing; RIE, SOF, RLV qualified. **All delib benefit cash flows are gross of
  *Kapitalertragsteuer*, *Solidaritätszuschlag* and *Kirchensteuer*; the models compute no tax and no withholding**, and every
  Schicht-3 `technical-notes.md` says so in one line.

### R46. ErbStG and SGB V §§ 226, 229 and 240 — death benefits and contributions on an annuity in payment
- Publisher: Bundesministerium der Justiz; the GKV-Spitzenverband for the *Beitragsverfahrens- grundsätze Selbstzahler*; the
  Bundesministerium für Arbeit und Soziales for the annual *Sozialversicherungsrechengrößen*. Doc type: statutory sections; an
  annual Rechtsverordnung.
- URL: **not established** for any of them. `https://www.gesetze-im-internet.de/erbstg_1974/__3.html` and
  `https://www.gesetze-im-internet.de/sgb_5/__229.html` are **`[unverified canonical form]`** and the ErbStG slug is itself a
  guess.
- Retrieved: **yes** — ErbStG canonical XML (**Stand: zuletzt geändert durch Art. 10 G v. 22.6.2026 I Nr. 192**),
  § 3 read in full, and **SGB V**, fetched and indexed in this pass (canonical XML, **Stand: zuletzt geändert durch Art. 1 G v.
  26.6.2026 I Nr. 195**), §§ 226, 229 and 240 read in full, both **2026-08-30**. `gesetze-im-internet.de/erbstg_1974/__3.html` serves
  (8.5 kB); `sgb_5/__229.html` is a 6.9 kB frameset shell, which is why the XML is the citable route.
- Content: **Germany has no insurance-specific death-benefit tax regime.** Unlike France, where CGI arts. 990 I and 757 B carve
  life insurance out of ordinary succession, a German *Todesfallleistung* paid to a named beneficiary is simply an ***Erwerb von
  Todes wegen*** under § 3 Abs. 1 Nr. 4 ErbStG — a benefit acquired under a contract for the benefit of a third party — and
  falls into ordinary inheritance tax at the beneficiary's own *Steuerklasse* and *Freibetrag*. Reported *persönliche
  Freibeträge* (§ 16): **500,000 €** spouse or registered partner, **400,000 €** child, **200,000 €** grandchild, **100,000 €**
  parent on death, **20,000 €** in *Steuerklassen* II and III; reported rate bands (§ 19): class I **7–30 %**, II **15–43 %**,
  III **30–50 %**; a *Versorgungsfreibetrag* (§ 17) of **256,000 €** for a surviving spouse. **Two structuring facts the German
  market actually uses** and that change who a model's beneficiary is: the ***Über-Kreuz-Versicherung***, where
  *Versicherungsnehmer* and *versicherte Person* are different people — spouses each owning a policy on the other's life — so
  that death triggers a payment to a *surviving policyholder* rather than an acquisition from a deceased one and **no
  inheritance tax arises**, which is standard advice for couples buying RLV cover and means a real RLV book contains a large
  share of cross-owned policies; and the **gift limb**, under which granting an *unwiderrufliches Bezugsrecht* during life is a
  *Schenkung* under § 7 ErbStG at the time of the grant [R26]. **Social insurance is the asymmetry that can reverse the tax
  argument.** § 229 SGB V makes certain retirement incomes ***Versorgungsbezüge***, contributory in the *Krankenversicherung der
  Rentner* and the *soziale Pflegeversicherung* at the **full rate borne entirely by the pensioner** — reported as an
  *allgemeiner Beitragssatz* of **14.6 %** plus the fund's *Zusatzbeitrag*, and **3.6 %** (2025) for care insurance with a **0.6
  %** surcharge for the childless — and the class covers **betriebliche Altersversorgung** in all five *Durchführungswege*.
  **What is not a Versorgungsbezug is the point**: a **private Riester annuity**, a **Basisrente** and **every Schicht-3
  annuity** (RV, FRV, IDX, SOF) attract **no health or long-term-care contribution at all** for a compulsorily insured
  pensioner. § 226 Abs. 2 SGB V grants a ***Freibetrag*** in the health insurance for benefits that *are* caught, reported as
  **one twentieth of the monthly Bezugsgröße** — **187.25 €/month in 2025** and **197.75 €/month in 2026** — with only a
  *Freigrenze* of the same amount in the care insurance. **But § 240 SGB V reverses the result for *freiwillig versicherte*
  members**, for whom **the whole of the member's economic capacity** is contributory, expressly including private annuities:
  the same SOF annuity that costs a compulsorily insured pensioner nothing costs a voluntarily insured one roughly **19 %** of
  every payment. **The self-employed — the core Basisrente market and a large part of the private annuity market — are
  overwhelmingly freiwillig or privately insured**, so the exposed population is precisely the one buying the products, and a
  SOF, RV or BAS specification discussing net-of-tax attractiveness must carry the qualification. Three delib parameters hang
  off one annual regulation, the *Sozialversicherungsrechengrößen-Verordnung*: the Basisrente ceiling [R39], the
  *Kleinbetragsrente* threshold [R42] and this *Freibetrag* — so **delib carries them as `**[std]**` parameters in one place,
  with the year stated, and every product document references that one place**.
- Not established: **all figures, all paragraph attributions, the ErbStG URL slug, the *Versorgungsfreibetrag* mechanics and the
  § 240 scope.** Whether a **Basisrente Hinterbliebenenrente** is caught by the ErbStG or exempted as a *Versorgungsbezug* is
  **not established** and is a real question given [R39]'s *nicht vererblich* condition. **Whether a Pflegerente or a BU annuity
  in payment is a *Versorgungsbezug* is not established.** The taxation of a **Pflegerente** itself is genuinely open, with two
  incompatible readings current — **not taxable at all** (compensation for care costs, falling under no *Einkunftsart*, the
  standard statement for *Pflegetagegeld*) versus ***Ertragsanteil*** taxation as a *Leibrente* [R41]. The distinction matters
  because the first makes the benefit worth more per euro of premium than any other benefit in delib. **The PFL
  `product-spec.md` states both readings, cites neither, and says the model publishes gross benefits and takes no position** —
  which costs nothing, because delib computes no tax anywhere. Likewise **not established**: whether a
  *Pflegerentenversicherung* premium is a *sonstige Vorsorgeaufwendung* under § 10 Abs. 4 EStG, where a
  *Risikolebensversicherung* and a *selbständige* BU premium sit within a joint annual ceiling reported at **2,800 €** for the
  self-employed and **1,900 €** for employees — a ceiling that basic health and care contributions alone normally exhaust, so
  that **a German risk-protection premium is in practice not deductible at all**, the exact opposite of the Schicht-1 position
  and the reason the market sells **BU cover inside a Basisrente**.
- Read in the 2026-08-30 pass — **three claims confirmed, two corrected, one base established.**
  **Confirmed:** § 3 Abs. 1 Nr. 4 ErbStG covers *"jeder Vermögensvorteil, der auf Grund eines vom Erblasser geschlossenen Vertrags bei
  dessen Tode von einem Dritten unmittelbar erworben wird"*. § 229 Abs. 1 lists the five *Versorgungsbezüge* classes and excludes
  *"Leistungen aus Altersvorsorgevermögen im Sinne des § 92 des Einkommensteuergesetzes"* from the bAV class, so a private Riester
  annuity, a Basisrente and every Schicht-3 annuity are outside it. **§ 226 Abs. 2 gives the *Freibetrag* base this entry could not
  state:** contributions are payable only where the monthly total exceeds *"ein Zwanzigstel der monatlichen Bezugsgröße nach § 18 des
  Vierten Buches"*, and a *Freibetrag* of the same one-twentieth is then deducted from the § 229 Abs. 1 Satz 1 Nr. 5 income.
  **Corrections. (1)** A ***Versorgungswerk*** pension **is** a *Versorgungsbezug* — § 229 Abs. 1 Nr. 3, *"Renten der Versicherungs-
  und Versorgungseinrichtungen, die für Angehörige bestimmter Berufe errichtet sind"* — so the Schicht-1 exemption does not extend to
  the compulsory professional schemes. **(2) § 240 does not itself name private annuities**; it requires that
  *"die Beitragsbelastung die gesamte wirtschaftliche Leistungsfähigkeit des freiwilligen Mitglieds berücksichtigt"*, and the express
  inclusion is in the GKV-Spitzenverband's *Beitragsverfahrensgrundsätze Selbstzahler*, which was not retrieved. **The "full rate borne
  entirely by the pensioner" claim is § 248 SGB V, which was not read, and is dropped from this entry.** **Still `[unverified]`:**
  § 7 ErbStG, § 248 SGB V, the *Über-Kreuz-Versicherung* and gift structuring practices, and the 2026 monthly *Bezugsgröße*.
- Products: KLV, RLV and RIE load-bearing; the rest qualified.

---

## 9. Biometric bases and market statistics

**Read the evidence warning first.** The biometric sweep also ran **zero successful searches**; both queries it issued were
refused for budget. **No value from any DAV table is known to this library, at any age, for any of the five tables**, and none
may appear anywhere in delib attributed to one. The market aggregates in R53 are second-hand from the prudential sweep and carry
its caveats. The DAV tables are **proprietary and are not shipped**; every decrement CSV in delib is a `**[std]**` proxy,
anchored so the product's own worked example reproduces exactly, and each product's `sources.md` names the DAV table the proxy
stands in for and says what a replacement must preserve.

### R47. Rechnungsgrundlagen erster und zweiter Ordnung, and the DAV as owner of the tables
- Publisher: Deutsche Aktuarvereinigung e.V. (DAV); the concept itself is carried by § 138 VAG [R8], § 2 DeckRV [R14], § 341f
  HGB [R54] and the DAV *Fachgrundsätze* [R56]. Doc type: market terminology and professional practice, not a document.
- URL: `https://aktuar.de/` — the host and the path shapes `content/PDF/Fachwissen/` and `de/newsroom/detail/` were **returned
  in the prudential sweep**; **no table-specific path is established**.
- Retrieved: **the DAV website yes, the tables no.** `aktuar.de` was browsed on **2026-08-30** — the home page
  (HTML, 130 kB), the *Wissen* index and the *Regularien* page — and **no page offering or describing any of the five tables was
  found.** This is not a network limitation: the site serves, and the DAV distributes its tables to members and licensees.
  **The prudence rule behind the two-basis structure was retrieved** from § 5 Abs. 1 DeckRV and § 138 Abs. 1 VAG.
- Content: the DAV occupies a position with **no equivalent in frlib, uklib or uslib**: it is at once the professional body
  whose members sign the statutory certifications [R11], the standard-setter whose *Fachgrundsätze* bind them [R56], **the body
  that derives and owns the market's biometric tables**, and the body that makes the annual *Höchstrechnungszins* recommendation
  [R56]. In France the mortality tables are homologated by *arrêté* and printed in the *Code des assurances* annexe, so a
  modeller can read them; in Germany the equivalent tables are a **members' deliverable of a private association**. That single
  institutional difference is why this section is shaped the way it is: **every table citation in delib is a citation to a
  document the library has not read and cannot ship.** **The mechanic that does not depend on having a PDF open.** German life
  actuarial practice runs **two parallel sets of assumptions** over the same contract. ***Rechnungsgrundlagen erster Ordnung***
  are the pricing and reserving bases — the *Rechnungszins* capped by the *Höchstrechnungszins*, a biometric table carrying
  explicit safety margins, and cost loadings. They are deliberately **prudent**, which is a statutory requirement [R8], and they
  determine the *Bruttobeitrag* and the *Deckungsrückstellung*. ***Rechnungsgrundlagen zweiter Ordnung*** are the best-estimate
  assumptions and determine what actually happens. **The *Sicherheitszuschlag* is the wedge between them, and its direction
  depends on which way the risk runs**: for a **death benefit** prudence means assuming mortality **higher** than expected; for
  a **survival benefit or annuity** it means **lower** mortality **and a stronger assumed improvement trend**, so a generational
  annuity table carries safety in **two dimensions** and a proxy reproducing only the level is not a proxy for the table; for
  **disability incidence** it means **higher** incidence and **lower** reactivation; for **care** it means higher incidence,
  longer duration in care and lower mortality of care recipients. **The wedge is not waste — it is the profit-sharing engine**:
  its systematic release as experience emerges is the *Risikoüberschuss*, one of the three *Überschussquellen* fed into the RfB
  and distributed under the MindZV [R10][R18]. **A delib model that projects only best-estimate cash flows must still know the
  first-order basis**, because that is what fixes the *Bruttobeitrag* and the guaranteed benefits — the numbers the contract
  states — while the second-order basis drives the projection. The technical notes' three-way assumption split is this
  distinction wearing different clothes. The most visible market artefact of the wedge is the **Bruttobeitrag/Zahlbeitrag gap in
  Berufsunfähigkeit** [R37][R50]. **An insurer may use its own table.** German practice permits *Rechnungsgrundlagen* derived
  from the undertaking's own portfolio experience where the data suffices, provided the derivation is documented and § 138 VAG's
  prudence requirement is met; the DAV table is a **market default and benchmark, not a legal mandate**. That is a real
  difference from France, where art. A. 335-1 *C. ass.* enumerates the permitted kinds of table and floors experience-table
  annuity rates at the homologated table; **no German analogue of that explicit floor was established, and its existence or
  absence is an open question.**
- Not established: **the size of the DAV's safety loading on any table**, as a percentage, an age-dependent function or a
  separate tabulation, **for any of the five tables**. Whether the DAV publishes both orders of each table or only the
  first-order table with a derivation report is **not established**, though market practice speaks of "1. Ordnung" and "2.
  Ordnung" tabulations. **The DAV's licence terms — member-only, licensed to insurers, licensed to software vendors — were not
  established at all**, and this is the highest-value single question for the next sweep: it is the fact that would tell a delib
  user how to obtain the real table lawfully. The DAV's seat, founding year and membership are `[unverified]`. **The derivations
  of the German market tables have historically been published in the peer-reviewed actuarial literature — the *Blätter der
  DGVFM*, continued from 2010 as the *European Actuarial Journal* — even though the tables themselves are not freely
  available**, which is the right place to send a reader who wants to improve on a delib proxy; but **no specific derivation
  paper was identified for any of the five tables**, and volume numbers, years, authors and titles are all **not established**.
- Read in the 2026-08-30 pass — **the prudence requirement is now a regulation, not a convention.** § 5 Abs. 1
  DeckRV [R17]: *"Die Ableitung von Rechnungsgrundlagen auf der Basis eines besten Schätzwertes genügt nicht. Die Abschätzung künftiger
  Verhältnisse muss eine nachteilige Abweichung der relevanten Faktoren von den getroffenen, aus den Statistiken abgeleiteten Annahmen
  beinhalten."*, with § 138 Abs. 1 VAG requiring *angemessene versicherungsmathematische Annahmen* [R8] and § 143 VAG making the
  insurer's own choice supervisor-visible but not public [R11]. **Neither instrument names a table**, which is what makes the DAV
  tables a market default rather than a legal mandate. **Everything about the tables themselves remains unretrieved**, per
  [R48]–[R51].
- Products: all ten.

### R48. DAV 2008 T and its predecessors — the death-benefit mortality basis
- Publisher: Deutsche Aktuarvereinigung e.V., 2008 `[unverified]`. Doc type: proprietary actuarial table. **Not public, not
  redistributable; delib ships no version of it.**
- URL: **not established.**
- Retrieved: **no — DAV 2008 T is not published.** `aktuar.de` serves and was browsed on **2026-08-30** (home page, *Wissen*
  index, *Regularien*); no page offers or describes the table. The obstacle is the DAV's distribution model, not network access, and
  it did not change in this pass.
- Content: the market-standard first-order mortality basis for **German death-benefit business** — *Risikolebensversicherung*,
  the death component of a *Kapitallebensversicherung*, death cover in a deferred annuity's accumulation phase, and the
  *Beitragsrückgewähr* death benefit of a BAS or RIE contract. It succeeded **DAV 1994 T** and is understood to derive from
  pooled German insured-lives experience rather than population data — the substantive difference from a Destatis table [R52],
  since insured lives are **selected** and their mortality is materially lighter than the general population's at the working
  ages term cover lives at. Structural features a `**[std]**` proxy must reproduce, each `[unverified]`: **sex-specific base
  tables** (raw material even though a tariff may not price on sex since 2012, [R34]); a **smoker/non-smoker split**, which
  German term insurers use heavily and which produces the roughly two-to-one premium spread in the RLV market; **selection
  factors** for the first years after underwriting, medical selection putting $q_x$ in policy years 1–5 substantially below the
  ultimate rate; and **no projected mortality improvement**, because for death cover improvement is favourable to the insurer,
  so a prudent first-order basis does not project it. **That is the exact opposite of DAV 2004 R [R49], and it is why a single
  "German mortality table" does not exist: the direction of prudence forks by product.** Model consequences: an RLV model built
  on a population table without a selection adjustment **overstates claims by a wide margin at issue ages 25–45**, so the RLV
  proxy is documented as insured-lives-shaped with its anchor stated; and where a KLV carries both a death and a survival
  benefit, **using one table for both is a numbered pitfall**, since the prudent basis for the death leg is not the prudent
  basis for the survival leg. **The in-force cohorts** were priced on **DAV 1994 T** (pre-2008) or **ADSt 1986** and older
  (pre-1994) `[unverified]`; delib's treatment is stated identically in every affected product — **the model point carries its
  cohort's *Höchstrechnungszins* [R15] and a single `[std]` decrement proxy is used across all cohorts**, with the notes saying
  explicitly that cohort-specific first-order mortality is not modelled and why: the guaranteed benefits of an in-force point
  are given data on the model point row, so the table that produced them need not be re-derived.
- Not established: the publication year (2008 is inferred from the name), the data window, the age range, whether
  smoker/non-smoker and selection tables are part of the published set, the size of the loading, and whether a first- and
  second-order pair is distributed — **all not established**. Names, dates and publishers of DAV 1994 T, ADSt 1986 and the older
  tables are `[unverified]`, as are the cut-over dates between them. **No $q_x$ value at any age is known to this library and
  none may appear anywhere in delib attributed to this table.**
- Products: RLV and KLV load-bearing; the others qualified; not relevant to SOF.

### R49. DAV 2004 R and DAV 2004 R-Bestand — the generational annuity tables
- Publisher: Deutsche Aktuarvereinigung e.V., 2004 `[unverified]`. Doc type: proprietary actuarial tables. **Not public, not
  redistributable; delib ships no version of them.**
- URL: **not established.**
- Retrieved: **no — DAV 2004 R is not published.** `aktuar.de` serves and was browsed on **2026-08-30** (home page, *Wissen*
  index, *Regularien*); no page offers or describes the table. The obstacle is the DAV's distribution model, not network access, and
  it did not change in this pass.
- Content: the market-standard first-order basis for **every German annuity promise** — RV and SOF directly, and FRV, IDX, BAS
  and RIE through annuitisation of the accumulated fund. Its defining property is that it is a ***Generationentafel***: a
  two-dimensional basis $q(x,\tau)$ in attained age and calendar year, **not a period table**. That is the one structural fact a
  delib annuity model must reproduce, and reproducing it is not optional — **a period-table proxy priced at a 40-year-old's
  annuitisation in 2055 understates the liability by a margin that dwarfs every other assumption in the model**. The
  construction, as the German market describes it and `[unverified]` in every detail: a **Basistafel** of second-order mortality
  for a stated base year, sex-specific; a ***Trendfunktion*** supplying age-dependent annual improvement rates; and safety
  loadings applied to **both** the level and the trend. The trend is not constant over time — the German construction uses a
  **Starttrend** fitted to recent experience **converging to a weaker Zieltrend** over a transition period, so **a proxy
  applying one flat improvement rate forever is qualitatively wrong in long deferrals**. For single-premium immediate annuities
  buyers self-select for good health and the table is understood to carry ***Selektionsfaktoren*** reducing mortality in the
  first years — the mirror image of the underwriting selection in DAV 2008 T, running the same direction for the opposite
  reason, and **a SOF model that ignores it understates the annuity cost**. **DAV 2004 R-Bestand** is the variant for the
  *Deckungsrückstellung* of annuities **already in force**, as distinct from pricing new business: when DAV 2004 R was
  introduced it revealed that the book priced on DAV 1994 R was reserved on mortality that had proved far too heavy, and the
  strengthening (*Nachreservierung*) was permitted to be financed over a transition period rather than in one balance sheet.
  **Modelling consequences**: every delib annuity model needs **two indices** on the mortality cells, with the calendar year
  stated as `issue_year + t`; the `**[std]**` proxy must be **generational**, built as a base table times a cumulative
  improvement factor with its improvement parameters documented as `[std]` and anchored to Destatis's own generational tables
  [R52], which are the free and redistributable analogue; and the guaranteed *Rentenfaktor* of an FRV or IDX contract is the
  arithmetic image of this table plus the guaranteed rate, so a model publishing a `[std]` *Rentenfaktor* **and** a `[std]`
  annuity table must state whether the two are consistent and, if not, which is authoritative.
- Not established: the base year, the age range, the trend function's form, the transition length, the loading structure, the
  selection period and the smoker treatment are **all not established**; nor is whether the table is distributed as a
  first-order/second-order pair. The length and legal basis of the *Nachreservierung* transition, and whether BaFin prescribed
  or merely permitted it, are not established; the existence, name and date of a **DAV 1994 R** predecessor are `[unverified]`.
  ***"DAV 2004 R-B20" has two incompatible readings*** — a table applying the trend for a **twenty-year horizon**, or something
  else entirely (a *Bestand* table with a 20 % loading, or a 2020 valuation table) — and **neither can be excluded**; any delib
  document naming it must say only that it is an in-force annuity variant of the DAV 2004 R family and stop there. **No $q_x$,
  no improvement rate and no annuity factor may be attributed to this table anywhere in delib.**
- Products: RV, SOF, FRV, IDX, BAS, RIE load-bearing; KLV and PFL qualified.

### R50. DAV 1997 I / RI / TI — the Berufsunfähigkeit decrement family
- Publisher: Deutsche Aktuarvereinigung e.V., 1997 `[unverified]`. Doc type: proprietary actuarial tables. **Not public, not
  redistributable; delib ships no version of them.**
- URL: **not established.**
- Retrieved: **no — the DAV 1997 family is not published.** `aktuar.de` serves and was browsed on **2026-08-30** (home page, *Wissen*
  index, *Regularien*); no page offers or describes the table. The obstacle is the DAV's distribution model, not network access, and
  it did not change in this pass.
- Content: **a correction to the commissioning brief, recorded as a question rather than a correction.** The brief names "DAV
  1997 I and DAV 1997 TI (Eintritts- und Reaktivierungswahrscheinlichkeiten)". On this compiler's understanding that pairing is
  incomplete: a German BU model needs **three** decrements and the market names a family of **three** tables — **I** for
  *Invalidisierung* (incidence), **RI** for *Reaktivierung*, and **TI** for the *Sterbewahrscheinlichkeiten der Invaliden*.
  Reading "TI" as the reactivation table would leave disabled-life mortality unspecified, which no multi-state BU model can do.
  **This is `[unverified]` and is recorded as a question for the next sweep**, but a delib document should not repeat the
  two-table pairing without checking. **The multi-state structure the tables serve.** A BU model is a three-state process —
  *aktiv* → *invalide* → *tot*, with a return arc *invalide* → *aktiv* — needing, per age and sex: $i_x$ (incidence), $q_x^{aa}$
  (active-life mortality, from DAV 2008 T or its predecessor, [R48]), $q_x^{ii}$ (disabled-life mortality, materially heavier
  than active mortality especially in the first year after disablement) and $r_x$ (reactivation, concentrated in the first two
  years of a claim and near zero thereafter). **This is the most data-hungry product in delib and the one whose `[std]` proxies
  carry the least support.** **The age of the basis is itself a finding**: these tables date from 1997 and rest on older
  experience, while German BU claims experience has shifted decisively — the causes mix has moved towards psychiatric diagnoses
  and the statutory *Berufsunfähigkeitsrente* was abolished for cohorts born from 1961, changing both the insured population and
  its incentives. A thirty-year-old first-order basis with a heavy safety loading is **why the German BU market runs a large and
  persistent *Bruttobeitrag*/*Zahlbeitrag* gap** [R37]. **Modelling consequences**: the BU model must publish an **explicit
  reactivation assumption** — setting it to zero is a choice with a large, one-directional effect that must be argued, not
  defaulted; **disabled-life mortality must be separate from active-life mortality**, using one rate for both being a numbered
  pitfall; and the six-month qualification and the 50 % degree threshold are **AVB conventions, not table properties** [R37] —
  the tables give probabilities of a *state*, and the contract decides when that state pays.
- Not established: the three-table structure, the names **RI** and **TI**, the publication year, the data window, whether the
  tables distinguish **occupational classes** (*Berufsgruppen* rating is the dominant premium driver in the German BU market and
  must come from somewhere, but the DAV 1997 family is not obviously it), and the size of the loadings — **all not
  established**. Whether a table exists for *Erwerbsunfähigkeit* as distinct from *Berufsunfähigkeit* is not established. **A
  table designated "DAV 1998 E" could not be characterised at all**: two incompatible readings of the letter are available —
  *Erlebensfall*, a survival-benefit table, and *Erwerbsunfähigkeit* — and neither can be preferred on the available evidence,
  so **no delib document may cite DAV 1998 E.** **No incidence rate at any age may be attributed to DAV 1997 I anywhere in
  delib.**
- Products: BU load-bearing; RLV, KLV and PFL qualified.

### R51. DAV 2008 P, § 15 SGB XI and the Pflegegrad break
- Publisher: Deutsche Aktuarvereinigung e.V., 2008 `[unverified]`, for the table; Bundesministerium der Justiz for SGB XI. Doc
  type: proprietary actuarial table; statutory sections.
- URL: table **not established**; https://dejure.org/gesetze/SGB_XI/15.html (returned in the contract sweep);
  `https://www.gesetze-im-internet.de/sgb_11/__37.html` and `__43.html` `[unverified canonical form]`.
- Retrieved: **the statute yes, the table no.** **SGB XI** canonical XML (**Stand: zuletzt geändert durch Art. 2c G
  v. 24.7.2026 I Nr. 228**), §§ 15, 36, 37 and 43 read in full, **2026-08-30**; `dejure.org/gesetze/SGB_XI/15.html` and
  `gesetze-im-internet.de/sgb_11/__37.html` also serve. **DAV 2008 P is not published**, as at [R48].
- Content: **DAV 2008 P** is the market-standard first-order basis for private long-term-care business —
  *Pflegerentenversicherung*, and in the health sector *Pflegetagegeld* and *Pflegekosten* cover, which delib treats as out of
  scope. It is understood to supply, by age and sex, **transition probabilities into care**, **mortality of people in care** and
  **transitions between care levels** `[unverified]`. **The finding that matters most is a mismatch, not a number.** A table
  published in 2008 is necessarily defined on the **three *Pflegestufen*** of the pre-2017 social care insurance. The *Zweites
  Pflegestärkungsgesetz* replaced them on **1 January 2017** with the **five *Pflegegrade*** of § 15 SGB XI, assessed by a
  points-based *Begutachtungsinstrument* that deliberately **widened** the definition of care need, particularly on cognitive
  and mental grounds — and the BGH has **refused to map the two scales** [R36]. **If the courts will not map the grades, a
  modeller may not silently do so either.** Therefore, for delib's PFL product: the model **states which trigger scale it
  implements** — *Pflegegrade*, an ADL points system, or a combination — and **any incidence proxy calibrated to Pflegegrade
  data is explicitly not a proxy for DAV 2008 P**, because the two are defined on different state spaces separated by a
  definitional break that raised measured prevalence. **The social scheme is the benchmark the private product is sold
  against**: it pays *Pflegegeld* (cash where care is given informally), *Pflegesachleistung* (in kind) and *vollstationäre
  Pflege* (a fixed contribution to residential care), with **Pflegegrad 1 receiving none of the three**, only the monthly
  *Entlastungsbetrag*; the amounts rise steeply with grade and are capped and partly in kind, which is why **the private
  *Pflegerente* — uncapped cash, paid irrespective of setting — is the product's entire selling proposition** and why its
  benefit is modelled as an annuity rather than a reimbursement. The private benefit ladder is conventionally a **percentage of
  the full *Pflegerente* per Pflegegrad**, and **no market standard was established**, so it is `**[std]**` in delib unless a
  *Tarifblatt* supplies it. Since 2022 the care-related *Eigenanteil* in residential care is reduced by ***Leistungszuschläge*
  rising with the duration of residence** (§ 43c SGB XI), **so the funding gap a private *Pflegerente* is sized to fill is
  largest in the first year of residential care** — a feature with a direct modelling implication for the sum insured.
- Not established: **whether DAV 2008 P is defined on Pflegestufen (the reasoned inference) or was reissued on Pflegegrade is
  not established, and this is the most consequential unresolved question for PFL** — if a post-2017 revision exists, the whole
  caveat changes shape. The data source, age range, state space, loading structure and whether reactivation out of a care level
  is modelled are **all not established**; whether an earlier *DAV 1998 P* exists is not established. **The § 15 SGB XI point
  bands separating grades 1 to 5 were sought and not returned in the contract sweep either, and remain unknown** — without them
  the PFL grade ladder cannot be grounded in anything but `[std]`. **No SGB XI euro amount was established** — no *Pflegegeld*,
  no *Pflegesachleistung*, no § 43 residential contribution, no *Eigenanteil*, no *Leistungszuschlag* percentage — and **no
  delib document may quote one without confirming it**; magnitudes in circulation from general knowledge are recorded nowhere in
  this library as figures. The § numbers other than § 15 are `[unverified]`. The subsidised **Pflege-Bahr** product (§ 127 SGB
  XI `[unverified]`, from 1 January 2013, a €5 monthly *Zulage* on a €10 own contribution with **no health underwriting**) is
  recorded as **out of scope but instructive**: it is the clearest illustration in the German market of anti-selection risk, so
  **delib's PFL incidence assumption is an underwritten-lives assumption and is not transferable to a guaranteed-issue tariff**;
  every Pflege-Bahr parameter here is `[unverified]`.
- Read in the 2026-08-30 pass — **the statutory side of the Pflegegrad break is now quantified.** § 15 Abs. 2
  weights the six modules ***Mobilität* 10 %**, ***kognitive und kommunikative Fähigkeiten sowie Verhaltensweisen und psychische
  Problemlagen* together 15 %**, ***Selbstversorgung* 40 %**, ***Bewältigung von ... krankheits- oder therapiebedingten Anforderungen*
  20 %** and ***Gestaltung des Alltagslebens und sozialer Kontakte* 15 %**, modules 2 and 3 contributing **one** weighted score, the
  higher. § 15 Abs. 3 maps the total: **Pflegegrad 1 ab 12,5 bis unter 27; 2 ab 27 bis unter 47,5; 3 ab 47,5 bis unter 70; 4 ab 70 bis
  unter 90; 5 ab 90 bis 100**, with Abs. 4 allowing grade 5 below 90 in *besondere Bedarfskonstellationen*. **The social benefit
  ladder is read rather than described:** § 37 Abs. 1 *Pflegegeld* per month **347 € (PG 2), 599 € (3), 800 € (4), 990 € (5)**;
  § 43 Abs. 2 *vollstationär* **805 €, 1 319 €, 1 855 €, 2 096 €**; and §§ 36, 37 and 43 all open at *"Pflegebedürftige der Pflegegrade
  2 bis 5"*, confirming that **Pflegegrad 1 receives none of the three**. A points instrument weighting cognition at 15 % and self-care
  at 40 % is a **different state space** from the three *Pflegestufen*, not a rescaling. **Still `[unverified]`:** everything about
  DAV 2008 P, and the *Zweites Pflegestärkungsgesetz* as the amending instrument — the consolidated text shows the result.
- Products: PFL load-bearing; BU, KLV and RV qualified.

### R52. Destatis — Periodensterbetafeln, Kohortensterbetafeln, Pflegestatistik and the reuse licence
- Publisher: Statistisches Bundesamt (Destatis), Wiesbaden; the *Datenlizenz Deutschland* is issued by the German administration
  `[unverified]`. Doc type: official statistical publications and datasets.
- URL: **not established** for any of them; no Destatis path was returned to any sweep.
- Retrieved: **yes for the methodology and headline results**, and the URLs are now established where this entry had
  none. Destatis's *Entwicklung der Lebenserwartung* page
  (`destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/sterbetafel.html`, 86 kB), its
  *Kohortensterbetafeln* page (`.../kohortensterbetafeln.html`, 90 kB) and its *Impressum* were read **2026-08-30**. The tables
  themselves — `.../Publikationen/Downloads-Sterbefaelle/statistischer-bericht-sterbetafeln-5126207237005.xlsx` and
  `.../statistischer-bericht-kohortensterbetafeln-5126101239005.xlsx` — were **located but not opened**, so **no $q_x$ value is
  quoted anywhere**. The *Pflegestatistik* was not opened.
- Content: the **free, redistributable, population-level German mortality basis**, and therefore the raw material behind every
  `**[std]**` decrement CSV delib ships — exactly the role INSEE plays in frlib. **Two distinct products, and confusing them is
  a real error**: the *Sterbetafel 20xx/20yy* is a **period table** computed annually from three years of deaths and population,
  giving $q_x$ and $e_x$ by single year of age and sex; the *Allgemeine Sterbetafel* is computed once per census cycle on
  census-corrected denominators, is the more accurate, and is the one usually used as a base table. **Why a population table is
  the wrong shape**: insured lives are selected, so population mortality is heavier than insured mortality at the ages term and
  endowment business lives at, and lighter than annuitant mortality is light — **it sits between the two insured populations and
  matches neither**. A delib proxy built from it therefore carries an explicit, `[std]`-tagged adjustment with a stated
  direction: **downward for a term or endowment death leg** (medical selection) and **downward again and generationally for an
  annuity** (voluntary anti-selection plus improvement). **The *Generationensterbetafeln für Deutschland* are the single most
  useful public document in this section**: cohort life tables built from historical German mortality plus a projected
  improvement, normally in more than one variant distinguished by the strength of assumed improvement — **exactly the structure
  DAV 2004 R has** [R49], and therefore the right public basis for delib's `[std]` generational annuity proxy, built as
  $q(x,\tau)=q_{\text{base}}(x)\cdot\prod(1-\lambda(x))$ over the calendar years from the base year, with $\lambda(x)$ a `[std]`
  age-dependent improvement rate anchored so the worked example reproduces exactly and documented as a **simplification** of the
  Starttrend/Zieltrend structure rather than a replication of it. What it does **not** supply is the annuitant selection effect
  and the first-order safety loading; both stay `[std]` adjustments layered on top. The ***Pflegestatistik*** is the **only
  public German prevalence data for long-term care** and therefore the calibration target for every `[std]` PFL incidence
  assumption: it counts *Pflegebedürftige* recognised by the social scheme by **Pflegegrad 1 to 5**, by age and sex, and by care
  setting. **The series contains a definitional break at the 2017 reform that is not a change in the underlying risk** [R51], so
  any delib document quoting a prevalence trend says so and no incidence proxy is calibrated across the break. **The licence
  question and why delib's position does not depend on it**: German official statistics are understood to be released under a
  permissive attribution licence (*Datenlizenz Deutschland – Namensnennung*) permitting commercial reuse, redistribution and
  modification with attribution — the same assumption frlib records as `[unverified]` for INSEE. **delib's ruling is safe under
  either answer**: the shipped CSVs are **constructed, anchored, documented `[std]` proxies**, not reproductions of any
  published series, each carrying a `provenance` column naming what it stands in for, so the library's position does not turn on
  resolving the licence. **It does depend on never shipping a DAV table**, which is not a licence question at all.
- Not established: the exact edition names and reference periods, the exact life-expectancy values (recent German period tables
  are understood to give **about 78 years for men and about 83 for women** `[unverified]`, and **no figure from this entry may
  be quoted to more precision than that**), the age ranges, the publication dates and the tabulation form. For the generational
  tables: the cohort range, the number and names of the variants, the projection horizon and whether they are machine-readable —
  **none of the commonly cited framing could be confirmed and none may be stated**. For the Pflegestatistik: **no figure was
  corroborated**, including the widely cited headline of around **5.7 million** *Pflegebedürftige* on the 2023 reference date,
  the grade percentages, the home/institution split and the periodicity; whether it covers privately insured care recipients was
  not established and materially affects its use as a denominator. The licence name, version and attribution wording are **not
  established**. The *koordinierte Bevölkerungsvorausberechnung* — the right citation for any statement about the direction of
  German longevity — has an **unestablished current edition, base year and variant set**. **HMD** (long, methodologically
  consistent historical series, the right basis for fitting an improvement trend, requiring registration and carrying its own
  terms) and **Eurostat** are recorded as the other free routes; their coverage and licence terms are not established.
- Read in the 2026-08-30 pass — **the vocabulary this entry used was Destatis's older one, and the licence
  question is answered.** Destatis publishes ***Periodensterbetafeln*** — three calendar years of deaths and population,
  *"eine Momentaufnahme der Sterblichkeitsverhältnisse der gesamten Bevölkerung"* with no future assumption, the current edition being
  the **Sterbetafel 2023/2025** — and ***Kohortensterbetafeln***, **not *Generationensterbetafeln***. The cohort tables rest on
  projections *"in Anlehnung an die Annahmen zur Entwicklung der Lebenserwartung der 15. koordinierten Bevölkerungsvorausberechnung"*
  and come in **two variants, Variante 1 on the low and Variante 2 on the high life-expectancy assumption** — the same
  two-dimensional, multi-variant shape DAV 2004 R has [R49]. Two anchors for a proxy's level: on the Sterbetafel 2023/2025 a
  65-year-old man has **18,0** further years and a woman **21,1**; the 2023 birth cohort is projected at roughly **81 to 90 years for
  boys and 85 to 93 for girls** depending on variant. **The licence:** Destatis's *Impressum* states for GENESIS-Online
  *"© Statistisches Bundesamt (Destatis), 2026 — Datenlizenz Deutschland – Namensnennung – Version 2.0"*, an attribution licence.
  **Still `[unverified]`:** every $q_x$ value, and the *Pflegestatistik*'s 2017 definitional break.
- Products: all ten (the base of every `[std]` proxy).

### R53. The German life market in numbers — GDV, BaFin, Assekurata, Map-Report, Morgen & Morgen and Franke und Bornberg
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e.V.; BaFin; Assekurata Assekuranz Rating-Agentur GmbH; Franke
  und Bornberg GmbH / map-report; MORGEN & MORGEN GmbH. Doc type: statistical compendia, supervisory statistics, rating-agency
  surveys and claims-practice studies.
- URL:
  https://www.gdv.de/resource/blob/180978/b8ae8eb0b1bf4b15e7cc3354bc231af9/die-deutsche-lebensversicherung-in-zahlen-2024-publikation-pdf-data.pdf
  ; https://www.bafin.de/SharedDocs/Downloads/DE/Statistik/Erstversicherer/neu/dl_st_24_erstvu_lv_va.html ;
  https://www.assekurata-rating.de/2026/01/29/ueberschussdeklaration/ ;
  https://www.franke-bornberg.de/blog/map-report-verwaltungskostenquote-2023-lebensversicherer ;
  https://www.franke-bornberg.de/fb-news/pressemitteilungen/map-report-939-solvabilitaet-im-vergleich-2015-bis-2024 (all
  returned)
- Retrieved: **yes**, and one cited URL is dead. The **GDV *Die deutsche Lebensversicherung in Zahlen 2025***
  (PDF, reporting business year 2024) at
  `gdv.de/resource/blob/188374/dde4d81192e583ac43e7e80a84aa6ac6/die-deutsche-lebensversicherung-in-zahlen-2025-publikation-pdf-data.pdf`,
  the **2024 edition** (reporting 2023) at blob/180978, **Assekurata's *Überschussdeklaration 2026*** of 29.01.2026 (HTML, 194 kB),
  **map-report 939** (94 kB) and the map-report ***Verwaltungskostenquote*** article (102 kB) were all read **2026-08-30**.
  **`bafin.de/.../dl_st_24_erstvu_lv_va.html` returns HTTP 404**, so the BaFin life-segment figure of €90.4 bn is dropped.
- Content: **Volumes, 2024, GDV basis** (Lebensversicherer, Pensionskassen and Pensionsfonds together): premium income **+2.8 %
  to €94.6 bn**; *laufende Beiträge* **€66.3 bn**, roughly flat; *Einmalbeitragsgeschäft* about **+10 % to €28 bn**; composition
  **63.9 % / 29.5 % / 6.7 %** (laufende / Einmal / Zusatzversicherungen); **contract count −1.4 % to 80.3 m** — **the level is wrong
  and is corrected to 84.3 m by the 2026-08-30 pass below**; new business
  *laufender Beitrag* **€6.6 bn (+2.8 %)** and *Einmalbeitragsgeschäft* **+10.8 % to €27.2 bn**. The operative reading is the
  **Einmalbeitrag shift**: single premium is now roughly 30 % of income and growing an order of magnitude faster than regular
  premium, which is why SOF is a live product and why KLV and RV model point tables include single-premium points. **Volumes,
  2024, BaFin basis**: life-segment *verdiente Bruttobeiträge* **€90.4 bn**. **The GDV and BaFin figures measure different
  populations on different bases and must never appear in the same table in delib.** **The GDV taxonomy** is the vocabulary any
  German market figure comes in `[unverified]`: *Kapitalversicherungen* → KLV, *Risikoversicherungen* → RLV,
  *Rentenversicherungen* → RV and SOF, *fondsgebundene* → FRV, *sonstige Lebensversicherungen* (where index business sits and is
  **not separately visible**), the excluded *Kollektiv-* and bAV lines, and *Zusatzversicherungen* (BU as a **rider**, while
  delib models the *selbständige* form). Riester and Basisrente **cut across** the taxonomy and are reported separately.
  **Declared rates.** For **2025**, average *laufende Verzinsung* **2.53 % Klassik / 2.58 % Neue Klassik**. For **2026** the
  sources give **2.6–2.7 %**, **2.87 %** and **2.54 %** — three incompatible averages. Highest declared rates named: **Inter
  3.40 %**, **Provinzial 3.25 %**. **The *laufende Verzinsung* is the *Garantieverzinsung* plus the *laufende
  Zinsüberschussbeteiligung***, so a declared 2.5 % on a 1.0 % guarantee implies a 1.5 pp surplus credit and **a delib model
  must never add the declared rate on top of the guarantee** — a numbered pitfall for every general-account product.
  *Gesamtverzinsung* adds the *Schlussüberschussanteil* and the *Bewertungsreserven* share. **Cost ratios, 2024.**
  *Verwaltungskostenquote* **2.4 %** on one measurement and **2.19 %** on another, against **2.5 % for 2023**, with a market
  spread **from under 2 % to over 4 %**; the two use different denominators (*gebuchte* versus *verdiente Bruttobeiträge*).
  **The 2024 solvency reset** [R13]: the life industry's SCR ratio **including** transitionals was **340.3 % at end-2024 against
  663.6 % at end-2023**, a fall of about **323 percentage points driven by the recalculation rather than by economics**; **three
  life insurers failed to reach 100 % without Hilfs- und Übergangsmaßnahmen at 31 December 2024**; base ratios **excluding**
  transitionals stayed largely stable — the recalculation removed an accounting cushion, not capital. Named 2024 outliers
  **without volatility adjustment and without transitionals**: highest **LVM 730.1 %** and **LV 1871 715.7 %**; lowest
  **Concordia Oeco 27.6 %**, **LPV 35.5 %**, **Öffentliche Oldenburg 59.6 %**. BaFin's *Erstversicherungsstatistik* is published
  as Excel with a separate life volume, the **2024 Tabellenteil on 17 November 2025**, and is the aggregate a delib document
  should prefer over trade press. **The survey houses** supply what no statutory source does: Assekurata's annual
  *Überschussdeklaration* and its *Marktstudie zu Überschussbeteiligungen und Garantien* track the declared rates and the shift
  from full *Beitragsgarantie* through "Neue Klassik" partial guarantees to levels below 100 % of premiums — the premise of
  delib's IDX product; *map-report* draws insurer-level series from the statutory accounts [R54], the only route to a cost or
  lapse figure defined identically across insurers, and gives the **spread** as well as the average, which is what a `**[std]**`
  parameter needs; and MORGEN & MORGEN and Franke und Bornberg publish the two standard **BU claims-practice** studies reporting
  the *Anerkennungsquote*, the declinature grounds (dominantly *Anzeigepflichtverletzung* under § 19 VVG [R30]), the *Vergleich*
  share, processing time and average age at claim. **The BU consequence is specific**: a model paying every incident claim in
  full is modelling a 100 % acceptance rate, so **delib's BU incidence assumption is `**[std]**` net of declinature, stated as
  such**, with a pitfall recorded that applying a gross incidence table *and* an acceptance ratio double-counts.
- Not established: the disagreements above are recorded and **none is resolved** — 2026 declared rate three ways;
  *Verwaltungskostenquote* 2.4 % vs 2.19 %; *Einmalbeiträge* €28 bn (total) vs €27.2 bn (new business); the end-2024 SCR ratio
  with transitionals **340.3 % vs 484 %**. **No Abschlusskostenquote figure at all**, the only anchor being the 25 ‰
  *Höchstzillmersatz* [R16], a **cap not an observation**. **No Stornoquote value for any year**, and **no duration-shaped lapse
  curve exists publicly for any German product** — the GDV rate is published on **two bases (contract count, and sum insured or
  premium)** giving materially different answers, so a delib lapse assumption is a `**[std]**` duration-shaped curve anchored on
  its duration-weighted average. **No product-level GDV split** and **no Riester or Basisrente contract count**, on any basis,
  in any year. **No *Rentenfaktor* and no *Effektivkosten* value**, guaranteed or current, from any insurer, in any year,
  although both are published per contract by law [R31][R43] — the two most consequential missing numbers in the library. **No
  BU figure**: no causes percentage (the *ordering* — psychiatric, musculoskeletal, cancer — is robust; the shares are not), no
  *Anerkennungsquote*, no average BU-Rente, no *Berufsgruppen* differential, no Brutto/Zahlbeitrag ratio, no
  *Erwerbsminderungsrente* amount or threshold. **IDX is statistically invisible** — no public series isolates index-linked
  business, which is itself a finding the IDX documentation must state. Nothing in the BaFin statistics themselves was read; the
  number of German life insurers and the aggregate *Deckungsrückstellung* were not established.
- Read in the 2026-08-30 pass — **one figure was wrong, and two ranges replace three disputed averages.**
  **Correction: the contract stock at end-2024 is 84,3 Mio. Verträge** (start of 2024: 85,5 Mio.), a fall of 1.4 per cent — this entry
  gave the correct percentage against the wrong level of 80.3 m. The other 2024 volumes are confirmed and sharpened: premium income
  **+2,8 % auf 94,6 Mrd. €**, *Einmalbeitrag* **+9,8 % auf 28,3 Mrd. €**, *laufende Beiträge* **66,3 Mrd. €**, benefits paid
  **+2,8 % auf 101,8 Mrd. €**, new-business sum insured from 323 to about **329 Mrd. €**, more than **46 Mio.** annuity contracts,
  **8,8 Mio.** *Direktversicherungen* and **9,7 Mio. Riester-Verträge (−3,5 %)** with Riester new business down **26,0 %** — the
  numbers behind [R44]. **Declared rates:** Assekurata publishes the *laufende Verzinsung* **per insurer** for 2024–2026 and states
  *"Diese setzt sich aus der Garantieverzinsung und der laufenden Zinsüberschussbeteiligung zusammen."*, confirming the
  never-add-on-top rule. The 2026 column runs from about **2,10 %** to **3,50 %** — Allianz 2,70 (2,80), Axa 3,00, EUROPA 2,90 (3,20),
  Continentale 2,60 (2,90), Alte Leipziger 2,40 (2,50), Gothaer 2,45 (2,70) — and **that observed range, not an average, is what a
  `[std]` credited-rate parameter should be argued against**; the three conflicting averages this entry carried were not retrieved and
  are dropped. **Cost ratios: the spread given here was far too narrow.** map-report reports the industry *Verwaltungskostenquote* at
  **2,46 % for 2023** against **2,34 % for 2022**, with a per-insurer range from **0,79 %** (Europa) to **11,29 %** (Targo) — an
  order of magnitude, not "under 2 % to over 4 %". **Solvency:** 340,3 % including transitionals at end-2024 against 663,6 % at
  end-2023, base ratio **308,6 %**, three insurers below 100 % without *Hilfs- und Übergangsmaßnahmen*, per-insurer spread 103,9 % to
  716,4 %, transitionals running out in 2032. **Still `[unverified]`:** the BU claims-practice studies, neither of which was opened.
- Products: all ten (market context, and the observed ranges behind every `[std]` choice).

---

## 10. Accounting and professional standards

### R54. HGB §§ 341–341o, RechVersV and BerVersV — the German statutory accounts and supervisory returns
- Publisher: Bundesamt für Justiz; BaFin for the BerVersV *Begründung*; mirrored by `dejure.org`, `buzer.de`, `freirecht.de`,
  `juraforum.de`, `ra.de`, `gesatz.de`, `lxgesetze.de`, `haufe.de`, `anwalt.de`, `datenbank.nwb.de`, `de.wikipedia.org`. Doc
  type: statute and two Rechtsverordnungen.
- URL: https://dejure.org/gesetze/HGB/341f.html and `/341e.html` (returned); https://www.gesatz.de/link.aspx?lnk=17400
  (returned, §§ 341f–341h); https://www.gesetze-im-internet.de/rechversv/BJNR337800994.html, `.../formblatt_1.html`,
  `.../__28.html` (returned); https://www.gesetze-im-internet.de/berversv_2017/BJNR285800017.html (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Aufsichtsrecht/Verordnung/begruendung_berversv_va.html (returned)
- Retrieved: **mostly.** The **HGB** (canonical XML, **Stand: zuletzt geändert durch Art. 4 G v. 4.2.2026 I Nr. 33**),
  §§ 341e and 341f read in full, and the **RechVersV** (canonical XML, **Stand: zuletzt geändert durch Art. 69 G v. 10.8.2021 I
  3436**), §§ 15, 25 and 28 read in full, both **2026-08-30**; `dejure.org/gesetze/HGB/341f.html` and `gesatz.de` also serve.
  **The BerVersV was retrieved only as its table of contents** — the index page serves (515 kB) and confirms § 10 as *Zusätzliche
  formgebundene Erläuterungen der Lebensversicherungsunternehmen*, but **its Anlagen, where the *Nachweisungen* live, were not
  opened.** BaFin's *Begründung zur Versicherungsberichterstattungs-Verordnung* serves (112 kB) and was not read.
- Content: **§ 341e — the standard of prudence.** Insurers must form technical provisions **to the extent necessary according to
  reasonable commercial judgement (*nach vernünftiger kaufmännischer Beurteilung*) to ensure the *dauernde Erfüllbarkeit* of the
  obligations** — the same standard § 138 Abs. 1 VAG imposes on premiums [R8] and BaFin states as its supervisory objective
  [R21], and the reason the German statutory reserve is deliberately conservative rather than best-estimate. **§ 341f — the
  *Deckungsrückstellung*.** One must be formed for obligations from **life insurance and from insurance business conducted in
  the manner of life insurance** — the hook that brings a *Pflegerente* or a stand-alone BU annuity inside the same reserving
  rule — at the amount of its ***versicherungsmathematisch berechneter Wert***, **including profit shares already allocated**
  but **excluding *verzinslich angesammelte Überschussanteile***, and **after deducting the actuarially calculated present value
  of future premiums**: the **prospective method**. Where a prospective calculation is not possible, the **retrospective
  method** on accumulated income and expenses applies. **§ 341h** covers the *Schwankungsrückstellung*, a non-life instrument
  noted only for completeness. **The RechVersV** is the statutory-accounts rulebook: insurers use **Formblatt 1 instead of § 266
  HGB** for the balance sheet and **Formblatt 3** for the life/health profit and loss account, both following the
  ***Nettoprinzip*** with reinsurers' shares openly deducted. **§ 28 gives the German surplus system its published anatomy**:
  within the RfB a ***Schlussüberschussanteilfonds*** is formed for *Schlussüberschussanteile*, *Schlusszahlungen*,
  *Gewinnrenten* and the minimum participation in *Bewertungsreserven*, per the applicable *Deklaration*, and the RfB may be
  used only for those purposes. **§ 28 Abs. 8 is the disclosure that makes the chassis auditable from outside**: the *Anhang*
  must give, in tabular form, the **development of the RfB** (*Anfangsbestand*, *Zuführungen*, *Entnahmen*, *Endbestand*); the
  portions attributable to its components **including the Schlussüberschussanteilfonds**; for **individual
  *Abrechnungsverbände*** the ***festgelegte Überschussanteile*** and where applicable the ***Ansammlungszinssatz***, with the
  *Zuteilungsjahr* stated; and the **procedures used to calculate the Schlussüberschussanteilfonds together with the chosen
  actuarial assumptions**. **This is the single most useful published source on a named insurer's surplus system**, and the
  reason a delib product document can cite a declared *Überschussanteilsatz* at all. **The BerVersV** governs what an insurer
  files with BaFin **beyond** the Solvency II templates — the national, HGB-based returns: life insurers must additionally
  prepare *formgebundene Erläuterungen* including the ***Zerlegung des Rohergebnisses nach Ergebnisquellen*** under
  **Nachweisungen 213 bis 219**, filed as forms **F.213.01 to F.219.01**. That is the **source-of-earnings split** —
  *Kapitalanlageergebnis*, *Risikoergebnis*, *übriges Ergebnis* — which is exactly the three-way split the MindZV's 90/90/50
  minima operate on [R18]; and the MindZV cross-refers into these forms by **named cell**, its § 5 identifying inputs as the
  amount in "**Formblatt 200 Seite 7 Zeile 10 Spalte 04**" and "**Formblatt 200 Seite 7 Zeile 12 Spalte 03**". **A German
  minimum allocation is therefore computed from named cells of a named supervisory form**, which is unusually concrete and is
  worth saying in a delib technical note. **delib computes none of this**: no model produces a *Deckungsrückstellung*, an RfB
  stock or a P&L, and the accounting layer is cited, never specified.
- Not established: the exact boundary of §§ 341–341o and which sections cover the *Anhang* and *Lagebericht*; § 341g was not
  retrieved; **the precise HGB treatment of *verzinslich angesammelte Überschussanteile* — which balance-sheet line they sit on
  — was not established, and it matters for any delib product with an accumulation option**. **The line structure of Formblatt 1
  was not established**, so where the *Deckungsrückstellung*, the RfB and the *Anlagestock* sit on a German balance sheet is
  unknown. Whether the RfB's *gebundene*/*ungebundene* split appears in § 28 or only in the RfBV was not established; the
  definition of *Abrechnungsverband* was not retrieved. **The contents of Nachweisungen 213–219 were not established**, only
  that the forms exist and carry the decomposition; and **the MindZV cell references quoted above are from the Pensionskassen
  section (§ 5), not from § 4, and must not be assumed to be the same for life insurers**. Whether the returns are public was
  not established (they are generally understood not to be). The RechVersV's own dates — **8 November 1994, BGBl. I S. 3378**,
  last amended **10 August 2021, BGBl. I S. 3436** — were returned by the search summaries and are recorded as such.
- Read in the 2026-08-30 pass. § 341e Abs. 1 Satz 1 verbatim: *"Versicherungsunternehmen haben
  versicherungstechnische Rückstellungen auch insoweit zu bilden, wie dies nach vernünftiger kaufmännischer Beurteilung notwendig ist,
  um die dauernde Erfüllbarkeit der Verpflichtungen aus den Versicherungsverträgen sicherzustellen."*, Satz 2 subordinating it to the
  supervisory rules on the *Rechnungsgrundlagen einschließlich des dafür anzusetzenden Rechnungszinsfußes*. § 341f Abs. 1 gives the
  prospective method in the statute's own words, and **§ 341f Abs. 2 is the ZZR root:** *"Bei der Bildung der Deckungsrückstellung
  sind auch gegenüber den Versicherten eingegangene Zinssatzverpflichtungen zu berücksichtigen, sofern die derzeitigen oder zu
  erwartenden Erträge der Vermögenswerte des Unternehmens für die Deckung dieser Verpflichtungen nicht ausreichen."* [R17].
  **Two RechVersV sections close loops elsewhere:** **§ 25 Abs. 1** requires *"angemessene Sicherheitszuschläge"* and permits
  Zillmerung, and **§ 25 Abs. 2** raises the reserve to the guaranteed *Rückkaufswert* where § 341f HGB would give less — **which is
  where the § 169 Abs. 3 VVG floor enters the balance sheet** [R28] and what DeckRV § 4 Abs. 3 refers back to [R16]; **§ 15 Abs. 1**
  defines the receivable DeckRV § 4 Abs. 2 caps. **§ 28 Abs. 8 Nr. 2 is now read item by item**, its Buchstabe h defining
  *"den ungebundenen Teil (Rückstellung für Beitragsrückerstattung ohne die Buchstaben a bis g)"* — the definition the RfBV and
  MindZV § 13 both borrow [R18] [R19] — with (e)–(g) the three *Schlussüberschussanteilfonds* tranches, Nr. 3 the per-*Abrechnungs­
  verband* declared shares and *Ansammlungszinssatz*, and Nr. 4 the *Schlussüberschussanteilfonds* method and bases. **Still
  `[unverified]` at that level of detail:** the *Nachweisungen 213–219* and the F.213.01–F.219.01 form names, **though the substance is
  confirmed from the other side**, MindZV § 4 Abs. 1 defining the three result sources by named lines and columns of *Nachweisung 213*
  [R18].
- Products: all ten as the source of published insurer data; load-bearing for KLV, RV, BAS, RIE, IDX and SOF.

### R55. IFRS 17 — Versicherungsverträge and the Variable Fee Approach
- Publisher: IASB; European Commission for the endorsement regulation; **DRSC** for the German project page; Haufe and Deloitte
  as commentary; the DAV for actuarial application material. Doc type: accounting standard, endorsed into EU law by **Verordnung
  (EU) 2021/2036**.
- URL: https://www.drsc.de/projekte/insurance-contracts/ (returned);
  https://www.deloitte.com/de/de/services/audit-assurance/perspectives/versicherungsvertraege-ifrs-17.html (returned);
  https://www.haufe.de/id/kommentar/joerg-baetgepeter-wollmerthans-juergen-kirschpeter-oser-2-variable-fee-approach-vfa-HI16462224.html
  (returned)
- Retrieved: **the commentary yes, the standard no.** The DRSC project page (HTML, 485 kB), the Deloitte overview
  (326 kB) and the Haufe VFA commentary (152 kB) were read **2026-08-30**. **IFRS 17 itself is IFRS Foundation copyright and is not
  freely served; the EU endorsement regulation was not opened either.**
- Content: the EU published **Verordnung (EU) 2021/2036 in November 2021**, taking IFRS 17 into EU law; the application date had
  been **deferred by one year to 1 January 2023**, and the standard applies **for financial years beginning on or after 1
  January 2023**. **Scope**: insurance contracts, reinsurance contracts and **investment contracts with discretionary
  participation features** (*Kapitalanlageverträge mit ermessensabhängiger Überschussbeteiligung*) — the last category matters
  in Germany because it catches savings vehicles that are not insurance in the risk-transfer sense. **The Variable Fee
  Approach** is an adaptation of the building-block approach for contracts with **direct participation features** and is
  **mandatory** for them: it explicitly reflects the value development of the underlying items, and the difference between the
  value computed at the first step and the value the actuaries compute at the second is **recorded in the Contractual Service
  Margin** — which is what "variable fee" names. Under the VFA, **investment returns on the underlying portfolio no longer hit
  the income statement immediately; they flow through the CSM, which is released progressively.** German life contracts
  qualifying for the VFA typically include the **HGB gross-surplus participation** — i.e. **the *Überschussbeteiligung* chassis
  of [R9], [R10] and [R18] is precisely what makes them direct-participating.** For delib IFRS 17 is **cited, never specified**:
  no model produces a CSM, a risk adjustment or a fulfilment cash flow, and the models produce gross liability cash flows that
  an IFRS 17 measurement would take as one input.
- Not established: the CSM, the risk adjustment, the coverage units and the transition approaches beyond the sentences above.
  Which German life insurers report under IFRS 17 (only listed groups do; solo German statutory accounts remain HGB) was **not
  established**. **Whether Riester and Basisrente contracts qualify as direct-participating was not established.** The
  endorsement regulation appears in one summary as "Verordnung (EG) Nr. 2021/2036" and in another as "Verordnung (EU)
  2021/2036"; **EU** is correct for a 2021 instrument and the "EG" rendering is treated as a transcription error, but **that
  judgment is inference**.
- Read in the 2026-08-30 pass — **and the pass *removed* a date this entry asserted.** The DRSC project page as
  served is **out of date**: it still gives the original first application *"für Geschäftsjahre, die am oder nach dem 1. Januar 2021
  beginnen"* and reports the deferral as *"um ein Jahr auf 2022"*. **So the 1 January 2023 application date and *Verordnung (EU)
  2021/2036* as the endorsement instrument were not confirmed by anything retrieved here and are now `[unverified]`.** What is
  confirmed is the standard's issue date of **18 May 2017** and the VFA's scope, in the Haufe commentary's words: *"Der Variable Fee
  Approach findet ausschließlich auf solche Versicherungsverträge Anwendung, die durch eine direkte Überschussbeteiligung ...
  gekennzeichnet sind"* and *"Der VFA ist verpflichtend für die im Standard spezifizierten Versicherungsverträge mit direkter
  Überschussbeteiligung anzusetzen"*, reinsurance being excluded and measured under the general model or the PAA.
- Products: all ten (qualified — group reporting context).

### R56. DAV Fachgrundsätze and the annual Höchstrechnungszins recommendation
- Publisher: Deutsche Aktuarvereinigung e.V.; PwC Deutschland *Insurance News* and Versicherungsmagazin as secondary reporters.
  Doc type: professional standards; annual recommendation and its supporting *Zinsbericht*.
- URL:
  https://aktuar.de/de/newsroom/detail/dav-empfiehlt-auch-fuer-2027-einen-hoechstrechnungszins-fuer-lebensversicherungs-neuvertraege-in-hoehe-von-10-prozent/
  (returned); https://aktuar.de/content/PDF/News/Pressemeldungen/2025_11_26_DAV_PM_H%C3%B6chstrechnungszins.pdf (returned);
  https://aktuar.de/content/PDF/Fachwissen/2024-11-22_Zinsbericht_f%C3%BCr_2026.pdf (returned);
  https://blogs.pwc.de/de/insurance-news/article/252092/dav-empfiehlt-beibehaltung-des-hoechstrechnungszinses-in-der-lebensversicherung-bei-1-0-prozent-fuer-2027
  (returned). **No URL for the *Fachgrundsätze* index or for any individual standard was returned.**
- Retrieved: **yes** — the newsroom item (HTML, 51 kB), the **DAV press release of 26.11.2025**
  (`aktuar.de/content/PDF/News/Pressemeldungen/2025_11_26_DAV_PM_H%C3%B6chstrechnungszins.pdf`, PDF, 3 pp.), the ***Fachwissen* fact
  sheet** *Höchstrechnungszins in der Lebensversicherung* (PDF, 2 pp.) and the DAV ***Regularien*** page, all read **2026-08-30**.
  The ***Zinsbericht für 2026*** (PDF, 551 kB) serves but **was not read**; the PwC commentary serves.
- Content: **The recommendation and its method.** The *Höchstrechnungszins* is set by the Bundesministerium der Finanzen as the
  DeckRV's *Verordnungsgeber* [R14]; **the DAV submits an annual proposal**, and **the ministry has in the past mostly followed
  it** — a soft-law channel with no statutory anchoring any search result identified, so delib describes it as **practice rather
  than law**. The method: the DAV runs **model calculations on a representative *Neuanlageportfolio***; scenarios for the
  development of returns are **weighted stochastically**; a **five-year average** damps short-term fluctuations; and a
  ***Sicherheitsabschlag* of 40 %** is applied to the smoothed return. The 40 % haircut is the residue of the statutory **60 %
  ceiling** that bound the German rate from the mid-1990s until Solvency II — derived from **Article 17 of the Third Life
  Directive of 1992**, carried forward as **Article 20 of Directive 2002/83/EC**, under which the reserving rate could not
  exceed **60 % of the rate on bonds issued by the State in whose currency the contract is denominated**, in the German
  application 60 % of the average yield on **ten-year government bonds**. **That rule was repealed without replacement when
  Solvency II took effect on 1 January 2016**, which is why the current German rate rests on a ministerial judgment informed by
  an actuarial recommendation rather than on a formula. The DAV recommended the increase from **0.25 % to 1.00 % for 2025**,
  which the ministry adopted [R15], then recommended **keeping 1.0 % for 2026** and again **1.0 % for 2027** (press release of
  **26 November 2025**), stating that one percent can be stably maintained in the medium term. **The asymmetry that matters for
  delib**: the interest haircut is **documented and quantified at 40 %**; the biometric haircuts [R47] are **neither, for any of
  the five tables**, and the reference library must not present the two legs of the *Rechnungsgrundlagen* as equally supported.
  **The professional standards.** The German actuarial standards system is understood to be a three-tier hierarchy of binding
  instruments — *Grundsätze*, *Richtlinien* and *Hinweise*, together the ***Fachgrundsätze***, binding on DAV members through
  the association's conduct rules — plus non-binding ***Ergebnisberichte*** `[unverified]` throughout. The mechanism that
  matters for a cash flow model is the chain from standard to tariff: § 138 VAG requires prudent actuarial assumptions [R8] and
  § 2 DeckRV requires prudently chosen bases [R14], and **neither instrument names a table**. The gap between "prudent" and
  "this specific $q_x$" is closed by the *Verantwortlicher Aktuar* under § 141 VAG [R11] exercising professional judgement under
  DAV standards, and in practice by using the DAV table appropriate to the product. **A German biometric basis is therefore soft
  law with hard consequences**: no statute mandates DAV 2008 T, and yet essentially every German term tariff is priced on it or
  on an insurer table justified against it. **The delib convention that follows**: cite the **named document or nothing** — a
  delib document that cites "a DAV standard" without saying which tier it belongs to is making a claim it cannot support. And
  the modelling consequence belongs in every product's technical notes: the model's decrement table is a **modeller's
  assumption, not a contractual term**, sitting in assumption class (c) behavioural for a BU incidence rate but in class (a)
  contractual for a *Rentenversicherung*, whose tariff table is fixed at inception and whose guaranteed *Rentenfaktor* is its
  arithmetic image. Getting that split wrong is a category error.
- Not established: **a direct conflict on the historic formula.** One summary states the ceiling as *"60 % der
  durchschnittlichen Rendite zehnjähriger deutscher Staatsanleihen"*; another states the German rate could amount to only *"85
  Prozent der gemittelten monatlichen Umlaufrendite von Anleihen der öffentlichen Hand"* under **§ 3 DeckRV**. These are
  **different bases and different percentages**. The 60 % figure is corroborated by the EU-directive lineage and by the DAV's
  own 40 %-haircut framing and is the one delib uses; **the 85 % figure is recorded and left unresolved, and any use of it must
  be marked `[unverified]`.** The contents of the DAV *Zinsbericht* — the portfolio composition, the scenario set, the resulting
  smoothed return — were not read. Whether the ministry has ever departed from a DAV recommendation, and when, was not
  established. **The exact names of the standards tiers, whether *Hinweise* bind at all, the mechanism by which the DAV's rules
  bind, and the title of any individual *Fachgrundsatz* are all not established**, nor is whether BaFin has ever endorsed a DAV
  standard by circular — which would convert soft law into a supervisory expectation. Whether a **successor** to DAV 2008 T, DAV
  2004 R, DAV 1997 I or DAV 2008 P has been published **is not known**, so **delib's formulation everywhere is "the DAV table
  conventionally used for this product is X"** — a statement about market convention that survives a successor being published —
  rather than "the current DAV table is X", which does not.
- Read in the 2026-08-30 pass — **the method and the professional-standards definition are now the DAV's own
  words, and one asserted hierarchy is withdrawn.** On the method: *"Die abschließende Entscheidung über den Höchstrechnungszins
  obliegt dem Bundesministerium für Finanzen durch eine Änderung der Deckungsrückstellungsverordnung."*; a representative
  new-money portfolio is modelled with the equity and property leg valued *"analog zum Vorgehen der Produktinformationsstelle
  Altersvorsorge (PIA)"* [R43]; *"Zur weiteren Glättung wird außerdem das arithmetische Mittel dieser Renditen über die vergangenen
  fünf Jahre gebildet."*; *"Zusätzlich wird ein 40-prozentiger Abschlag als Sicherheitspuffer eingerechnet, so wie ihn der Gesetzgeber
  bis zur Einführung von Solvency II verlangt hat."*; **and a floor this entry did not carry** — *"auch in Tiefzinsphasen [muss] der
  Sicherheitsabschlag immer mindestens 0,4 Prozentpunkte betragen."* The 2027 recommendation is confirmed from the press release of
  26 November 2025. **On the standards:** the *Regularien* page defines *Fachgrundsätze* as publications of DAV and IVS which, with
  the *Standesregeln*, lay down the principles of proper practice, characterised by addressing actuarial technical questions, being of
  fundamental and practice-relevant importance, being **legitimated by a *Feststellungsverfahren* open to all members** and being
  **secured by a *Disziplinarverfahren***, and expressly distinguishes them from non-binding ***Ergebnisberichte***.
  **The three-tier *Grundsätze / Richtlinien / Hinweise* naming this entry asserted does not appear there and is withdrawn to
  `[unverified]`.** **Still `[unverified]`:** Article 17 of the Third Life Directive and Article 20 of Directive 2002/83/EC, the
  source of the 60 % ceiling, neither of which was retrieved.
- Products: all ten.

---

## Gaps and caveats register

This section is the most reliable part of the file and should be read before any other. It records four things: what no search
could establish, where results disagreed, which figures are vintage-sensitive, and which material is proprietary and therefore
not shippable.

### A. The retrieval limit as the file was built, kept because it governs how everything above was written

Points 1 to 4 are the position on **2026-08-29** and are left in the words they were written in; point 5 records what the pass
of 2026-08-30 did to them, and it is point 5 and the per-entry `Retrieved:` lines that describe the file as it now stands.

1. **No document cited in this file had been retrieved.** Direct HTTP egress was blocked by an organisation network policy;
   `WebFetch` and `curl` were refused with HTTP 403 at the egress gateway for every external host. `gesetze-im-internet.de`,
   `bafin.de`, `aktuar.de`, `gdv.de`, `bundesfinanzministerium.de`, `destatis.de`, `dejure.org`, `eur-lex.europa.eu` and
   `de.wikipedia.org` were all tried and all refused. Every entry rested on **search-result summaries**, and every German phrase
   in quotation marks was a quotation **of a summary**, not of an instrument.
2. **The session's 200-call `WebSearch` budget was exhausted mid-build.** The prudential sweep (~35 German queries) and the
   contract sweep (~45) ran while search was available and record, per fact, what a search corroborated. **The tax sweep and the
   biometric sweep each ran zero successful searches**, and the query issued while compiling this file was likewise refused.
   R38–R53 are therefore materially weaker than R1–R37 and the file says so per entry.
3. **Grading, so a downstream author can calibrate.** Statutory *titles and section numbers* are strongly corroborated (five to
   ten independent publishers). Statutory *substance* summarised by one to three of them is moderately corroborated. Trade-press
   figures are frequently single-source. Anything with no search behind it is general knowledge and is tagged.
4. **The most useful method note for the next sweep**, recorded because it is cheap and it worked: every
   `gesetze-im-internet.de` section page follows `https://www.gesetze-im-internet.de/<lawslug>/__<section>.html`, and searching
   for `"§ NNN <Gesetz>" <Stichwort>` reliably returns that page plus four to eight independent mirrors whose snippets together
   reconstruct most of a section's substance. It works **poorly** for regulations with short sections (MindZV §§ 7–8, RfBV § 3)
   and **not at all** for BaFin circulars and interpretive decisions, whose pages return a title and one sentence — those need
   retrieval, not search.

5. **Superseded on 2026-08-30, and left standing above as the record of how the file was built.** Points 1 to 4 describe the
   build of 2026-08-29. In the pass of **2026-08-30** the network policy no longer applied and every entry was tried again: each
   now carries a `Retrieved:` line saying what was read, with the law's `Stand` for statutes and the edition for publications.
   **Forty-three of the fifty-six read `yes`, four read `no` ([R38], [R48], [R49], [R50]) and nine are partial.** **Where an entry
   quotes German in the `Read in the 2026-08-30 pass` bullet, that quotation is from the instrument**; where it quotes German
   elsewhere, the older caveat holds and it is a quotation of a summary. The `Retrieval conditions` header at the head of this
   file now carries both halves — how the library was built and what the pass established — and **the per-entry `Retrieved:`
   lines remain authoritative on any entry the two describe differently**.

### B. What no search could establish, in priority order

**Restated on 2026-08-30.** Eleven of the twenty-two items below were closed by the retrieval pass; each says so and names what
closed it. The rest stand, with a sharper reason than "no search returned it".

1. **CLOSED 2026-08-30 — and the question was wrongly framed.** There is **no corridor width** in § 5 Abs. 3 DeckRV [R17]. The
   rule forms two differences — the ten-year mean less last year's *Referenzzins*, and 9 per cent of the current-year mean less
   9 per cent of last year's — and adjusts by **the smaller in absolute value where the signs agree**, leaving the rate
   **unchanged where they disagree**. There is no bound to find, and § 5 Abs. 3 Satz 9 anchors the recursion at **2,21 Prozent for
   2017**.
2. **CLOSED 2026-08-30 for the endowment set.** The GDV *Allgemeine Bedingungen für die kapitalbildende Lebensversicherung*
   (Stand 21.07.2025) were read [R37]: the *Rückkaufswert* clause (§ 12 Abs. 3), the *Abzug* clause (§ 12 Abs. 4, **level left
   blank, "Unternehmensindividuell zu ergänzen"**), the § 169 Abs. 6 reduction (§ 12 Abs. 5), the surplus components (§ 12
   Abs. 6), the *Beitragsfreistellung* clause with **its own separate *Abzug*** (§ 13) and the cost clause (§ 14 Abs. 2).
   **Still open for BU:** the *Verweisung* and six-month clauses — the BU model conditions were not opened.
3. **OPEN.** Whether the BU six-month rule is a retroactive fiction or a waiting period ([R37]). The two produce materially
   different monthly cash flows and the choice is currently `**[std]**`.
4. **CLOSED 2026-08-30.** § 15 Abs. 3 SGB XI [R51]: **Pflegegrad 1 ab 12,5 bis unter 27; 2 ab 27 bis unter 47,5; 3 ab 47,5 bis
   unter 70; 4 ab 70 bis unter 90; 5 ab 90 bis 100** Gesamtpunkte, with § 15 Abs. 2 giving the module weights 10 / 15 / 40 / 20 /
   15 per cent and modules 2 and 3 contributing only the higher of the two.
5. **NARROWED, not closed.** § 1 Abs. 1 Nr. 3 AltZertG guarantees *"die eingezahlten Altersvorsorgebeiträge"*, and § 82 Abs. 1
   EStG defines *Altersvorsorgebeiträge* as contributions *"die der Zulageberechtigte ... leistet"* [R42] [R43] — which on its face
   excludes the state *Zulagen*. **But the AltZertG does not cross-refer to § 82 EStG and no authority was retrieved**, so this
   stays the section's most material `[std]` choice. For a two-child model point it moves the guarantee floor by thousands of euro
   over thirty years.
6. **The two consolidated BMF-Schreiben** on *Rentenbesteuerung* and on the *Riester/bAV* subsidy. They are the operative
   authority for [R39], [R41] and [R42] and would resolve more of the tax section than any other two documents; **neither's
   title, date, reference number nor URL is established** and none is guessed.
7. **PARTLY CLOSED 2026-08-30.** **The 6 % cost-of-capital rate is read from Art. 39 of the regulation** [R2] —
   *"Es wird davon ausgegangen, dass der in Artikel 77 Absatz 5 der Richtlinie 2009/138/EG genannte Kapitalkostensatz 6 % beträgt."*
   — as are the Art. 37 formula and the Art. 38 reference-undertaking assumptions. **Still open:** Art. 18 (Vertragsgrenzen) and
   the life-underwriting sub-modules of Art. 136 ff. including the mass-lapse shock; the document was opened, those articles were
   not read.
8. **CLOSED 2026-08-30.** The MCR provisions are **§ 122 *Bestimmung der Mindestkapitalanforderung; Verordnungsermächtigung*** and
   **§ 123 *Berechnungsturnus; Meldepflichten*** VAG [R6]; the absolute euro floors are in § 1 Abs. 2 KapAusstV as amended by
   Artikel 2 of the Sechste Verordnung [R15] — **2,7 / 4 / 4 / 3,9 / 1,3 Mio. Euro** from 25 July 2024.
9. **OPEN by choice.** No EIOPA curve value and no German volatility adjustment for any date was extracted ([R4]) — the monthly
   packages are Excel workbooks and delib takes no curve point from them. The euro **UFR of 3.30 % from 1 January 2026** is
   confirmed from EIOPA's release of 31 March 2025.
10. **CLOSED 2026-08-30, and it corrects an assumption.** § 5a AltZertG is read [R43] and is **purely procedural**; the
    substantive *Basisrentenvertrag* definition is **§ 2**, with § 2 Abs. 1a defining the Basisrente-Erwerbsminderung.
11. **CLOSED 2026-08-30.** § 93 EStG is read [R42], including Abs. 3's *Kleinbetragsrente* definition at **1,5 Prozent der
    monatlichen Bezugsgröße**.
12. **§ 160 VVG CLOSED 2026-08-30** — its four default rules are read [R26]. **§ 156 VVG still not opened** ([R22]).
13. **The EuGH reference for the 2013 § 5a VVG ruling** ([R36]) — commonly cited as *Endress*, C-209/12 of 19 December 2013, but
    **no search returned the case number**; carry it as `[unverified]` or omit it.
14. **Art. 2 Abs. 1 Nr. 17 IDD's definition of *Versicherungsanlageprodukt*** ([R31], [R32]) — it decides whether KLV, RV and
    IDX are PRIIPs products at all.
15. **PARTLY CLOSED 2026-08-30.** The **SRI 1–7 scale** is read from Art. 3(2)(a) of Delegated Regulation (EU) 2017/653 and the
    **four performance scenarios** — *optimistisches, mittleres, pessimistisches, Stressszenario*, plus an additional scenario for
    insurance-based products — from Annex IV as replaced by (EU) 2021/2268 [R32]; **the full item list of § 2 Abs. 1 VVG-InfoV** is
    read, as are § 2 Abs. 3, Abs. 4 and Abs. 6 and § 4 [R31]. **Still open:** the RIY presentation, the cost tables and the
    biometric-premium treatment inside Annex VI; **VVG-InfoV § 1**; and **§§ 6a and 7d VVG**.
16. **The Anlageverordnung's own content** ([R7]) — the *Anlageformen* and the *Mischungs-* and *Streuungsquoten*. **Nothing in
    delib may state an AnlV quota.**
17. **The supervisory *Sparte* classification of a stand-alone SBU and of a Pflegerente** ([R5]) — whether they are *Sparte* 19
    business or fall to the health regime.
18. **PARTLY CLOSED 2026-08-30.** The **BerVersV *Nachweisungen* are still not read** — only the regulation's table of contents
    was retrieved — but **MindZV § 4 Abs. 1 names the *Nachweisung 213* lines and columns for each of the three result sources**
    [R18], so the substance is established from the other side. **§ 28 Abs. 8 RechVersV is read item by item** [R54].
    **Still open:** the line structure of RechVersV *Formblatt 1*, and the wording of the *versicherungsmathematische Bestätigung*
    ([R11]).
19. **PARTLY CLOSED 2026-08-30.** **Two of the eight BaFin *Auslegungsentscheidungen* were read** — *Zusammenwirken von
    Mindestzuführung zur RfB und Teilkollektivierung* and *Projektion des Referenzzinses gemäß § 5 Abs. 3 DeckRV* — as was the
    index page and the *Merkblatt 01/2023* in full [R21] [R35]. **The other six were not opened**, and neither was the MaGo
    circular itself.
20. **The DAV's licence terms** ([R47]) — so delib cannot even tell a user how to obtain the real table lawfully. The
    highest-value single question for the next sweep.
21. **The AltvPIBV's own citation, the CRK class boundaries and the definitions of r\* and r_k** ([R43]); **the
    Altersvorsorgedepot product definition** ([R44]).
22. **PARTLY CLOSED 2026-08-30.** The Siebte (BGBl. 2024 I Nr. 414) and Achte (BGBl. 2025 I Nr. 31) Verordnung announcement
    pages serve, and **neither moved the rate**: the DeckRV's own `Stand` is still *"zuletzt geändert durch Art. 1 V v. 19.7.2024
    I Nr. 250"* and § 2 Abs. 1 Satz 1 still reads 1 Prozent [R14] [R15]. **The draft VSAAG was not investigated** ([R12]).

### C. Where results disagreed — **restated on 2026-08-30**, ten of eighteen resolved

1. **RESOLVED by replacement, not by choosing.** Assekurata publishes the *laufende Verzinsung* **per insurer**, and the 2026
   column runs from about **2,10 %** to **3,50 %** ([R53]). The three disputed averages were not retrieved and are dropped; a
   `[std]` credited rate should be argued against the **observed range**.
2. **RESOLVED against both figures.** map-report gives the industry *Verwaltungskostenquote* as **2,46 % for 2023** (2022:
   2,34 %) with a per-insurer range from **0,79 %** to **11,29 %** ([R53]). Neither 2.4 % nor 2.19 % was retrieved, and the
   spread is an order of magnitude, not the narrow band this register assumed.
3. **PARTLY RESOLVED.** map-report 939 gives **340,3 %** including transitionals at end-2024 against **663,6 %** at end-2023 and
   a **base ratio of 308,6 %** ([R53]). The "484 %" cut was not retrieved and is dropped.
4. **RESOLVED by dropping the BaFin figure.** The BaFin download 404s ([R53]); only the GDV basis is cited, and the two must
   still never be mixed.
5. **RESOLVED.** § 226 VAG read in full ([R12]): the **0,2 Promille** annual contribution is Abs. 5 Satz 2, the **1 Promille**
   target for the fund's assets is Abs. 4, and the **1 Promille** *Sonderbeitrag* ceiling is Abs. 5 Satz 5. The repetition is
   real, not an artefact.
6. **RESOLVED, and none of the three renderings was quite right.** § 4 Abs. 1 Satz 2 DeckRV: *"Der Zillmersatz darf 25 Promille
   der **Summe aller Prämien** nicht überschreiten."* ([R16]) — *Beitragssumme* is the market term, not the statute's.
7. **PARTLY RESOLVED, and the framing was wrong.** The **85 % cap is live law**: § 3 Abs. 1 and Abs. 2 DeckRV 2016 apply it to
   short single-premium contracts and to annuities in payment without a surrender value ([R14]). **The 60 % ceiling is not in the
   DeckRV at all** and its EU lineage was not retrieved ([R56]).
8. **RESOLVED.** § 2 RfBV is *Begriffsbestimmungen*; **§ 3 Abs. 2** carries the *Teilbestand* ceiling on a base of next year's
   declared shares plus expected *Direktgutschrift*, minimum 100 per cent, and **§ 3 Abs. 3** the collective ceiling as a
   percentage of the KapAusstV amount, **maximum 60 per cent** ([R19]).
9. **RESOLVED against the 1 per cent reading.** § 93 Abs. 3 Satz 2 Nr. 1 EStG defines a *Kleinbetragsrente* by **1,5 Prozent der
   monatlichen Bezugsgröße nach § 18 SGB IV**, and Nr. 2 adds an *Auszahlungsplan* variant **from 1 January 2027 on the same
   1,5 per cent** ([R42]) — **the 2027 date attaches to the payout-plan variant, not to the rate.**
10. **RESOLVED.** The Bundesrat consented on **8 May 2026** and the act is the **Gesetz vom 26. Mai 2026, BGBl. 2026 I Nr. 156**,
    which the VVG's and the AltZertG's own `Stand` lines name ([R44]).
11. **RESOLVED.** § 851c Abs. 2 Satz 1 Nr. 1 ZPO: **6 000 Euro** from 18 to the completed 27th year and **7 000 Euro** from 28 to
    the completed 67th, aggregate **340 000 Euro** ([R40]). The age-graded ladder is the superseded version.
12. **OPEN.** The § 20 Abs. 2 Satz 1 AGG repeal — "late February 2013" versus the *SEPA-Begleitgesetz* of 3 April 2013 with
    retroactive effect from 21 December 2012 ([R34]). The consolidated text shows only the result; both readings recorded.
13. **RESOLVED.** The Absatz structures of §§ 8, 152 and 169 VVG are read ([R23], [R28]), and **two were wrong**: the § 152
    due-date rule is **Abs. 5**, not Abs. 3, and the § 169 *Zeitwert* trigger in **Abs. 4** is the product class, not the absence
    of a fixed guarantee.
14. **NARROWED.** § 177 Abs. 1 VVG applies §§ 173–176 *"auf alle Versicherungsverträge, bei denen der Versicherer für eine
    **dauerhafte Beeinträchtigung der Arbeitsfähigkeit** eine Leistung verspricht"* ([R29]). A *Pflegerente* pays on
    *Pflegebedürftigkeit*, so **the wording points against**, but no authority was retrieved. **Still the main open legal question
    for PFL.**
15. **OPEN.** Whether a Pflegerente is taxable at all ([R46]) — not taxable versus *Ertragsanteil*. Neither reading was tested
    against a retrieved source in this pass.
16. **RESOLVED, and neither branch was right.** The *verursachungsorientiert* rule is **§ 140 Abs. 1 Satz 3 VAG** and it governs
    **charging RfB draw-downs back to the sub-portfolios that caused them**, not surplus allocation ([R8], [R10]). The general
    causation principle for surplus is **§ 153 Abs. 2 VVG** ([R24]), and the RfBV adds a *verursachungsorientierter
    Verteilungsschlüssel* for returns out of the collective part ([R19]).
17. **OPEN, and it will stay open.** "DAV 2004 R-B20" has two incompatible readings ([R49]); "DAV 1998 E" could not be
    characterised at all ([R50]) and **no delib document may cite it**; and the DAV 1997 family may be two tables or three
    ([R50]). **The DAV publishes nothing that would settle any of them.**
18. **WITHDRAWN rather than resolved.** The IFRS 17 endorsement regulation number **and the 1 January 2023 application date are
    now both `[unverified]`** ([R55]): the DRSC project page as served on 2026-08-30 is out of date, still giving the original
    1 January 2021 date and a deferral *"um ein Jahr auf 2022"*, and the endorsement regulation was not opened.

### D. Which figures are vintage-sensitive

Every figure in this file carries its year. These are the ones that will go stale first, and a delib document quoting them
without the year is wrong within months:

- **The *Höchstzinssatz* / *Höchstrechnungszins*** ([R14], [R15]): **1 Prozent from 1 January 2025**, fixed by § 2 Abs. 1 Satz 1
  DeckRV as amended by the Sechste Verordnung of 19 July 2024, and recommended unchanged by the DAV for 2026 and 2027. The rate
  history is a **cohort stack** — the DAV's own table now sits at [R15] — and a model point must carry its cohort's rate, not
  today's.
- **The ZZR *Referenzzins*** ([R17]): the **construction** is statutory and read, including the 2017 anchor of **2,21 Prozent**;
  the **current level of 1.57 %**, reported unchanged since 2021, and the ZZR stock (€84 bn at end-2024 from a €96 bn peak at
  end-2021) are **trade-press figures that were not re-opened in this pass** and stay `[unverified]`.
- **The declared *laufende Verzinsung*** ([R53]): Assekurata's **per-insurer** 2026 column runs from about **2,10 %** to
  **3,50 %**; the averages this register previously carried were not retrieved and are dropped.
- **The 2024 solvency reset** ([R13], [R53]): **340.3 % including transitionals at end-2024 against 663.6 % at end-2023.** Pre-
  and post-recalculation ratios are **not comparable** and a delib document must say which it quotes.
- **The euro UFR** ([R4]): **3.30 % applicable from 1 January 2026**.
- **The Solvency II cost-of-capital rate** ([R2], [R3]): **6 %, now read from Art. 39 of Delegated Regulation (EU) 2015/35**,
  falling to **4.75 %** under the 2025 review, first applying **30 January 2027** — that last figure and date being a consultancy's
  report, not the instrument. **No delib model implements a 2027 basis.**
- **The *Sozialversicherungsrechengrößen*** ([R39], [R42], [R46]): the Basisrente ceiling, the *Kleinbetragsrente* threshold and
  the *Versorgungsbezüge* Freibetrag all move annually off one regulation, so delib carries them as `**[std]**` parameters **in
  one place with the year stated** and every product document references that one place.
- **Riester's closure** ([R44]): new business ends **1 January 2027** under the **Altersvorsorge-Reformgesetz vom 26. Mai 2026,
  BGBl. 2026 I Nr. 156**, to which the Bundesrat consented on 8 May 2026. Existing contracts carry *Bestandsschutz*. A delib RIE
  model is a model of a **closed** product and its specification says so.
- **The Höchstzillmersatz** ([R16]): **25 Promille der Summe aller Prämien**, statutory in § 4 Abs. 1 Satz 2 DeckRV; the
  40 ‰ predecessor and its 1 January 2015 replacement date are **`[unverified]`** — the consolidated text shows only the current
  figure. § 4 Abs. 4 fixes the rate in force at conclusion for the whole term.
- **The unisex boundary** ([R34]): **21 December 2012**. Contracts before it may still be sex-rated; delib models none of them.

### E. What is proprietary and therefore not shippable

1. **The five DAV tables — DAV 2008 T, DAV 2004 R, DAV 2004 R-Bestand, DAV 1997 I / RI / TI and DAV 2008 P — are the property of
   the Deutsche Aktuarvereinigung, are distributed to members and licensees rather than published, and are not redistributed
   anywhere in delib** ([R47]–[R51]). The library cites them **by name**, states **what a replacement must preserve** — level,
   sex split, smoker split, selection period, trend structure, first- versus second-order — and ships `**[std]**` proxies
   instead, anchored so that each product's worked example reproduces exactly. **No $q_x$, no incidence rate, no improvement
   rate and no annuity factor anywhere in this library is attributed to a DAV table.**
2. **No value from any DAV table is known to this library**, and the 2026-08-30 pass did not change that: `aktuar.de` serves and
   was browsed, and it publishes no table. So there is no route in this session to validating a proxy against
   the real basis. That is the defining limitation of delib's biometric layer and it is stated in `index.md`, in every
   `sources.md` header and in every `_research/<slug>.md` header.
3. **An insurer's own *Rechnungsgrundlagen* are not public.** § 143 VAG makes them a documented, supervisor-visible object
   ([R11]) and precisely for that reason they are filed, not published.
4. **The PIA's stochastic scenario set** behind the *Chancen-Risiko-Klassen* and the individual *Effektivkosten* is not public
   ([R43]); delib reports a published CRK or Effektivkosten as an `[S#]` fact and does not reproduce the computation.
5. **The BerVersV supervisory returns** ([R54]) are generally understood not to be public, which is why the *Zerlegung des
   Rohergebnisses* reaches delib only through the RechVersV § 28 *Anhang* disclosures and through rating-agency series built on
   them.
6. **Destatis material is different and is the reason the proxies are buildable, and the licence question is now answered.**
   Destatis's *Impressum*, read 2026-08-30, states for GENESIS-Online *"© Statistisches Bundesamt (Destatis), 2026 —
   Datenlizenz Deutschland – Namensnennung – Version 2.0"* ([R52]) — reuse with attribution. delib's position never depended on it,
   because the shipped CSVs are **constructed proxies with a `provenance` column**, not reproductions of any published series.

### F. Two structural observations to carry into the product documents

1. **The regulation constrains the floor, not the offer.** Almost every number a German policy actually shows a customer — the
   credited rate, the charges, the *Rentenfaktor*, the *Stornoabzug*, the *Zahlbeitrag* — is set by the insurer inside a
   statutory envelope, and almost none of it is published per insurer. That is why delib's parameter tables are
   `**[std]**`-heavy, and why **each `[std]` footnote should point at the specific provision that bounds it**: the 25 ‰ cap for
   acquisition costs [R16], the 90/90/50 floor for the declaration [R18], the five-year spread for the surrender value [R28],
   the *Beitragsgarantie* for a Riester fund [R43].
2. **The German surplus system is a three-lever machine, and a model that pulls one lever has not modelled the product.** The
   insurer chooses the **declaration**, the **split between *Direktgutschrift* and RfB**, and the **release from the RfB and the
   *Schlussüberschussanteilfonds*** — subject to the MindZV minimum and the MindZV § 13 ceiling on the *ungebundener Teil* [R18],
   the RfB ring fence and its three escape hatches [R10], the RfBV ceilings on the *Teilbestände* and on the collective part [R19]
   and the § 139 VAG *Bewertungsreserven* test [R9]. A delib model that credits a rate without representing the RfB has modelled a
   French *fonds en euros* with German vocabulary, not a German contract.

### G. What this file is not

It carries **no `S#` primary product sources**. No *Allgemeine Versicherungsbedingungen*, no *Produktinformationsblatt*, no
*Basisinformationsblatt*, no *Verbraucherinformation* and no *Tarifblatt* is cited here; those belong in the ten per-product
research files and are cited there. What is written above about *variation across insurers* is therefore the **latitude the
regulation leaves** plus what the market aggregates say about how that latitude is used — never a statement about a named
carrier's contract.
