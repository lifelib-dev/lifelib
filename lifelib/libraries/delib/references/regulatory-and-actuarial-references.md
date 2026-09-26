# Regulatory and Actuarial References — German Life Insurance

**Status:** Draft, 2026-08-29.

Curated reference library for the Germany section of the reference-product library. It covers the prudential layer (Solvabilität II as
transposed into the *Versicherungsaufsichtsgesetz*, the statutory *Deckungsrückstellung* and the *Zinszusatzreserve*), the surplus
regulations that put an arithmetic floor under the *Überschussbeteiligung*, the contract law of the *Versicherungsvertragsgesetz*,
conduct and disclosure, the case law and the market's model conditions, the tax architecture of the *Drei-Schichten-Modell*, the
biometric bases and market statistics, and the accounting and professional standards that the ten reference cash-flow-model
implementations rely on.

**The ten products this page serves**, by slug: `kapitallebensversicherung`, `klassische_rentenversicherung`,
`fondsgebundene_rentenversicherung`, `indexpolice`, `basisrente`, `riester_rente`, `sofortrente`, `risikolebensversicherung`,
`berufsunfaehigkeit`, `pflegerentenversicherung`.

Product folders cite entries on this page as **[REG-R#]** (e.g., `[REG-R1]`); the **R1–R56 numbering below is frozen — do not renumber
and do not reuse a number**, because product documentation cites against it and a renumbering silently changes what every one of those
citations means. Unused ids are simply omitted downstream, leaving gaps, and each product's `sources.md` records which ids are absent
and why. Within this page, plain `[R#]` refers to the same entries. All URLs accessed **2026-08-29**.

**Citation discipline.** `[S#]` marks a fact from a primary product document listed in a product's own `sources.md`; `[R#]` a fact
from a product-specific regulatory or actuarial reference in that same file; `[REG-R#]` a fact from this page. **[std]** marks a
standardization introduced for the reference implementation — a parameter or convention chosen where sources vary, are proprietary or
are silent, each carrying a rationale and, where one could be established, the observed range across insurers. **[unverified]** marks
a claim from general knowledge or a secondary source that **no retrieved document confirms**. The hard rule the library runs on: **every
quantitative parameter is either source-tagged or marked [std]. No number anywhere in `delib` is untagged.**

---

## Retrieval conditions — read this before relying on a single line below

This section is stated first, in full, and prominently, because a reader needs it before using a single citation below — and because
**the statement that used to stand here has been overtaken**. `delib` was drafted with no document retrieval at all, and this page
said so on its first screen. The citations have since been **re-verified against the primary documents**, and **44 of the 56 entries
below now open with `Retrieved: yes`**: the document was fetched, opened and read, and the entry's own line records what was read, in
what format and how much of it. The twelve that do not are named at the end of this section, each with its reason. **The per-entry
`Retrieved:` lines are the authority for any single claim; this section only summarises them.**

**1. How this page was drafted, and why that stays on the record.** `delib` was built under a **default-deny network policy that
blocked all egress**. `WebFetch` and `curl` were refused with **HTTP 403 at the egress gateway** for every host outside a short
package-registry allowlist, and the hosts that matter for German life insurance — `gesetze-im-internet.de`, `bafin.de`, `aktuar.de`,
`gdv.de`, `bundesfinanzministerium.de`, `destatis.de`, `dejure.org`, `eur-lex.europa.eu` — were tried and refused without exception.
Not one statutory text, not one BaFin circular, not one DAV table, not one BGH judgment and not one statistical release was opened
while this page was written. The only research channel was `WebSearch`, which returns titles, URLs and a search-engine summary of the
matched pages rather than the pages, and **its 200-call budget was exhausted during the build**: roughly 35 German-language queries
went to the prudential and supervisory sweep, roughly 45 to contract law and conduct, the remainder to the ten per-product sweeps, and
**the tax sweep and the biometric sweep each ran zero successful searches**. The first draft of this page therefore rested on **the
authoring model's own knowledge of German insurance law and practice**, disciplined by the `[std]` and `[unverified]` tags and
corroborated where it could be by those secondary summaries. That account is kept here, and stays kept, because **it is this page's
provenance**: it is why `[std]` carries so much of the library's arithmetic, why the tax and biometric blocks began weaker than the
rest, and what the re-verification was verifying against. It is no longer a description of how to read the page.

**2. What the re-verification established.** The egress policy has since been lifted, and the citations were re-verified against the
primary documents in the pass of **2026-08-30**.

- **The fifteen German instruments this page cites were read as canonical XML from `gesetze-im-internet.de`, with each law's amendment
  status (`Stand`) recorded** on the entry that cites it: VAG, VVG, VVG-InfoV, DeckRV, MindZV, RfBV, RechVersV, HGB, EStG, EStDV,
  AltZertG, ZPO, ErbStG, SGB V and SGB XI — with § 34d GewO and the AGG read the same way alongside them. The `Stand` is written out
  in each entry, so that a reader can tell which vintage of the statute the entry is a statement about.
- **The European instruments were read as Official Journal text**: the consolidated German Solvabilität II directive [R1], the
  Delegated Regulation as a 797-page PDF [R2], the PRIIPs regulation with its two delegated acts as three PDFs [R32], and the IDD as
  a 41-page PDF (R33).
- **The supervisory, professional, statistical and market material was read as the publications themselves**: BaFin's *Merkblatt*
  01/2023 (VA) in full with its marginal numbers [R35], the DAV press release and *Fachwissen* fact sheet behind the
  *Höchstrechnungszins* [R56], the GDV endowment *Musterbedingungen* as a 20-page PDF, *Stand 21.07.2025* [R37], Destatis's
  methodology and headline results [R52], and the GDV, Assekurata and map-report market publications [R53].
- Across `delib` as a whole the same pass **checked 950 statutory section references and found 950 of them correct**, and retrieved
  insurer *AVB*, *Verbraucherinformationen* and *Produktinformationsblätter* as PDFs for the ten product corpora. **Library-wide, 501
  of `delib`'s 805 source entries — 62 % — now read `Retrieved: yes`.** This page, at **44 of 56**, is the best-covered part of the
  library, for the plain reason that statutes are served in canonical form and insurer documents mostly are not.

**What a `Retrieved:` line means.** `Retrieved: yes` means **the document was opened and the passage the entry rests on was read** —
not that the whole document was read, and not that everything in the entry is in it; the line names the sections that were read. An
entry that is not `Retrieved: yes` is **a pointer rather than a certificate**: it names the instrument a claim should be checked
against without asserting that anyone checked it, and it is marked as one. Treat a claim on this page as sound where its entry says
`Retrieved: yes`, and as provisional where it does not.

**The re-verification changed things — it did not merely confirm the draft.** § 138 VAG turns out to have no Absätze beyond 1 and 2,
and the *verursachungsorientiert* charging rule turns out not to be in § 138 at all but in § 140 Abs. 1 Satz 3 VAG [R8] [R10]; the
average declared rates this page reported for 2025 and 2026 were **not retrieved and have been dropped**, replaced by the observed
per-insurer range [R53]; the administration-cost spread the page gave was far too narrow and has been replaced by map-report's own
distribution [R53]; and the largest gap the page recorded — that no clause text from the GDV *Musterbedingungen* had ever been read —
is closed [R37]. Each entry states its own corrections under **Resolved in this pass** and its residue under **Still unverified**.

What follows from all of that, exactly:

- **Quotation is first-hand wherever the entry says the document was opened.** A German sentence in quotation marks under a
  `Retrieved: yes` entry is quoted from the instrument or the publication itself, not from a summary of it. The claims that still rest
  on a search-result summary say so where they sit — the clearest is the BGH decision of 18 September 2024 (IV ZR 436/22) tying § 138
  Abs. 2 VAG to § 153 Abs. 2 VVG, which was **not** retrieved and stays `[unverified]` [R8].
- **No URL on this page is fabricated, and the URLs have now been exercised.** Where a cited URL does not serve, the entry says so and
  the URL is replaced or the claim withdrawn: BaFin's life-statistics download returns **HTTP 404** [R53], the English MaGo page
  returns **HTTP 404** [R21], and the `juris` document server refused the BGH judgments with **HTTP 403** [R36]. The
  `[unverified canonical form]` marker the draft used for `gesetze-im-internet.de` section URLs it had never followed **no longer
  appears on any entry**: the text behind those URLs was read from the canonical XML the same host serves.
- **`[unverified]` now means something narrower, and is used precisely rather than generously.** It marks a specific paragraph number,
  effective date, monetary amount, percentage or market figure that **no retrieved document confirms** — it is no longer the standing
  condition of the whole page. Where it survives, the entry names what would settle it: an amending act visible only as a consolidated
  text's footnote, an administrative determination not opened, a judgment not served.
- **The five domains of this page are still not equally supported and must not be read as if they were.** Prudential and supervisory
  (R1–R21) stands at **18 of 21** entries retrieved; contract law and conduct (R22–R37) at **14 of 16**; tax and the three layers
  (R38–R46) at **8 of 9** — the block that was written on zero successful searches is the most changed on the page, its statutes now
  read in full, including both § 22 EStG tables and the § 55 EStDV table; accounting and professional standards (R54–R56) at **2 of
  3**; and biometric bases and market statistics (R47–R53) at **2 of 7**. **The biometric block is the weak one, and network access
  cannot fix it** — see the structural warning below.
- **Where a figure is needed by a reference implementation and cannot be confirmed, the honest form downstream is still a [std]
  parameter** with a stated rationale and an argued plausible range — not a [REG-R#] citation. A `[std]` number is honest; a wrong
  `[REG-R#]` number is not. In several places this pass **widened** such a range rather than replacing it with a citation [R53].

**3. The twelve entries that are not `Retrieved: yes`.** Seven of them record that **the instrument the entry is named for was not
opened at all**.

| Entry | What was not retrieved, and why |
|---|---|
| **R3** — Richtlinie (EU) 2025/2 | The amending directive itself was not opened on EUR-Lex in this pass. What the entry reports is an actuarial consultancy's commentary, which *was* read in full — a statement about what a commentator says of the instrument, not about what the instrument says. |
| **R36** — the BGH line of authority | **One of the six lines** was retrieved: the press release on IV ZR 201/17. For the other five, no judgment text and no press release was opened, and the `juris` document server refused with **HTTP 403**. They are kept as known references with their captions. |
| **R38** — AltEinkG | No BGBl text and no Bundestag drucksache for the Act was located. The two transitions it created were read instead from the EStG canonical XML, at R39 and R41. |
| **R48** — DAV 2008 T | **Not published.** This is not a network limit: `aktuar.de` serves and was opened; the DAV distributes its tables to members and licensees. |
| **R49** — DAV 2004 R and DAV 2004 R-Bestand | Not published, and for the same reason — the DAV's distribution model, not a network limit. |
| **R50** — DAV 1997 I / RI / TI | Not published, for the same reason. |
| **R55** — IFRS 17 | IFRS Foundation copyright: the standard is not freely served, and the EU endorsement regulation was not opened either. Three commentaries were read in its place. |

**Five more record that the entry's principal document was opened while a named part of it was not.** **R20** — the LVRG's BGBl
citation record and the government bill (BT-Drs. 18/1772) were read; the Act's own *Regelungstext* was not, because dejure serves the
citation record and not the text. **R21** — five BaFin documents were opened; the MaGo circular itself was not. **R33** — the IDD was
opened as a document and § 34d GewO read in full from the canonical XML, but the directive's conduct articles were not read line by
line. **R47** — the DAV site was opened; no DAV table, and no document describing a table's construction, was retrieved, because none
is published. **R51** — §§ 15, 36, 37 and 43 SGB XI were read in full; DAV 2008 P itself is not published.

**And seven entries that do open with `Retrieved: yes` still name a component that was not read**: the BU model conditions behind R37,
the AltvPIBV and the BMF *Muster*-Produktinformationsblatt behind R43, the Act's own text behind R44, Destatis's `.xlsx` tables behind
R52, BaFin's own life statistics behind R53, the BerVersV beyond its table of contents behind R54, and the DAV *Zinsbericht für 2026*
behind R56. **Read the entry, not this summary, before relying on a specific line.**

**One structural warning that governs the whole biometric section.** The five tables at the centre of German life pricing — **DAV 2008
T**, **DAV 2004 R**, **DAV 2004 R-Bestand**, **DAV 1997 I / RI / TI** and **DAV 2008 P** — are the property of the Deutsche
Aktuarvereinigung, are distributed to members and licensees rather than published, and are **not redistributable**. `delib` ships
**none of them** and quotes **no $q_x$, no incidence rate, no improvement rate and no annuity factor from any of them**. Every
decrement CSV in the library is a **[std]** proxy, anchored so that the product's own worked example reproduces exactly. That is the
same posture `frlib` took towards TH 00-02 and TGH05, and it is not a workaround: it is the only lawful and honest way to ship a
public reference library against a proprietary basis.

---

**Regulatory architecture in one line:** BaFin supervises German life insurers under Solvabilität II as transposed into the **VAG**,
and there is no second national supervisor — conduct and prudential supervision sit inside one authority — while the **VVG** carries
the contract law in a *separate statute with a different addressee*, and the arithmetic of the guarantee and the surplus is delegated
to two ministerial regulations, the **DeckRV** (the *Höchstrechnungszins*, the *Höchstzillmersatz*, the *Referenzzins* behind the
*Zinszusatzreserve*) and the **MindZV** (the 90 / 90 / 50 minimum allocation to the *Rückstellung für Beitragsrückerstattung*); which
is why a German model reads four instruments where a French model reads one code.

**Ten German terms carry the whole library** and are used untranslated after first use, because several have no English equivalent and
two are routinely mistranslated.

***Überschussbeteiligung*** — the policyholder's participation in the insurer's surplus. It is **not** the French *participation aux
bénéfices* and must never be rendered that way in a comparative sentence: the French version is a collective statutory minimum
computed from a regulated account, the German one an **individual contractual entitlement** (§ 153 VVG, [R24]) with a **statutory
minimum transfer to a reserve** on top (the MindZV, [R18]). ***Deckungs- rückstellung*** — the German statutory (HGB) reserve,
prospective, computed on the *Rechnungsgrundlagen* of the premium calculation (§ 341f HGB, [R54]; DeckRV, [R14]). It is **not** the
Solvency II best estimate, and the whole German picture depends on keeping the two apart: an insurer carries **two liability
measures**, and the *Überschussbeteiligung*, the *Zinszusatzreserve* and the *Bewertungsreserven* test all run on the **HGB** side.
***Rückkaufswert*** — the surrender value (§ 169 VVG, [R28]), floored at the *Deckungskapital* that results from spreading the charged
acquisition and distribution costs evenly over the first five contract years. ***Zillmerung*** — offsetting a contract's one-off
acquisition costs against its first premiums, the *Zillmersatz* capped by § 4 Abs. 1 Satz 2 DeckRV at **25 Promille der Summe aller
Prämien** — the *Beitragssumme* of market language ([R16]). ***Höchstzinssatz*** — the maximum rate at which the
*Deckungsrückstellung* may be discounted, **the statute's own term**, fixed at 1 Prozent by § 2 Abs. 1 Satz 1 DeckRV ([R14]);
***Höchstrechnungszins*** is the same rate under the name BaFin, the BMF and the DAV use, and delib writes *Höchstzinssatz* when
citing § 2 and *Höchstrechnungszins* when reporting the market ([R15]). Neither is the *Garantiezins*: § 2 caps the **reserving**
rate, while the rate a policy guarantees is a tariff decision that may be lower — a distinction the DAV states in terms ([R56]). ***Zinszusatzreserve*** — the additional HGB reserve that arises when
the § 5 Abs. 3 DeckRV *Referenzzins* falls below a contract's tariff rate ([R17]); it exists in no other jurisdiction in this
repository. ***Rentenfaktor*** — euros of monthly annuity per €10,000 of accumulated capital, the number that converts a unit-linked
or index account value into an annuity; the BGH struck down asymmetric unilateral reduction clauses in 2025 ([R36]).
***Beitragsgarantie*** — a guarantee that at least the contributions paid are available at the start of the payout phase, statutory
for a certified Riester contract ([R43]). ***Berufsunfähigkeit*** — inability to pursue **the last occupation as it was structured
before the impairment** (§ 172 Abs. 2 VVG, [R29]); it is *not* "disability" in the general-labour-market sense, and the statutory
scheme's *Erwerbsminderung* is that other thing. ***Pflegegrad*** — one of the five care levels of § 15 SGB XI, which replaced the
three *Pflegestufen* on 1 January 2017 ([R51]); the replacement is a **definitional break**, not a change in the underlying risk, and
the BGH has refused to map the two scales ([R36]).

Four more terms recur throughout. ***laufende Verzinsung*** is the declared annual credited rate and equals the *Garantieverzinsung*
**plus** the *laufende Zinsüberschussbeteiligung* — **not** a surplus rate on top of the guarantee; adding the two is the commonest
arithmetic error in describing a German contract and is a numbered pitfall in every affected product ([R53]). ***Direktgutschrift***
is surplus credited immediately rather than parked in the RfB, and is **deducted** from the MindZV minimum, which is why the MindZV is
a minimum *transfer*, not a minimum *payout* ([R18]). ***Bruttobeitrag*** and ***Zahlbeitrag*** are the tariff premium and the premium
actually collected after surplus is applied as a *Beitragsverrechnung*; the gap is large and persistent in *Berufsunfähigkeit* and the
*Zahlbeitrag* is **not guaranteed** ([R37], [R53]). ***Altbestand*** / ***Neubestand*** are contracts concluded before / from **29
July 1994**, the deregulation date ([R11]); **all ten delib products are Neubestand business**.

**Scope note on capital.** The SCR and the MCR exist under Solvabilität II [R1] [R2] as transposed by §§ 96–110 VAG [R6], and the
German statutory balance sheet carries its own *Deckungsrückstellung* and *Zinszusatzreserve* [R14] [R17] [R54] — but this library
treats the capital layer as **cited-not-specified**. The reference models produce **gross, undiscounted, best-estimate-style liability
cash flows and stop short of the discounting**. The Solvency II balance sheet, the SCR and MCR, the risk margin, the
*Deckungsrückstellung*, the *Zinszusatzreserve*, the RfB as a balance-sheet stock and the IFRS 17 measurement are referenced, never
specified. **The cost-of-capital rate is now read from the instrument — 6 per cent, Art. 39 of Delegated Regulation (EU) 2015/35
[R2] — but no risk-free curve value and no volatility-adjustment value was extracted from any EIOPA package [R4]**, so **any discount
rate, asset return or declared rate in a product document is `**[std]**`** with a rationale rather than a citation.

---

## Product-relevance matrix

`x` = load-bearing for that product's specification, technical notes or model; `(x)` = qualified, conditional or background relevance
— the entry governs the product but does not shape its cash flows, or reaches it only through an option or a rider; blank = not
relevant.

**Column key.** `KLV` = kapitallebensversicherung · `RV` = klassische_rentenversicherung · `FRV` = fondsgebundene_rentenversicherung ·
`IDX` = indexpolice · `BAS` = basisrente · `RIE` = riester_rente · `SOF` = sofortrente · `RLV` = risikolebensversicherung · `BU` =
berufsunfaehigkeit · `PFL` = pflegerentenversicherung.

| R# | Reference (short name) | KLV | RV | FRV | IDX | BAS | RIE | SOF | RLV | BU | PFL |
|----|------------------------|-----|----|-----|-----|-----|-----|-----|-----|----|-----|
| R1 | Richtlinie 2009/138/EG — Solvabilität II | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R2 | Delegierte Verordnung (EU) 2015/35 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R3 | Richtlinie (EU) 2025/2 — the Solvency II review | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R4 | EIOPA — RFR term structures, UFR, Volatilitätsanpassung | (x) | (x) | | (x) | (x) | (x) | (x) | | (x) | (x) |
| R5 | VAG 2016 and Anlage 1 — the Sparten | x | x | x | x | x | x | x | x | x | x |
| R6 | VAG §§ 74–110, 122–123 and § 40 — balance sheet, SCR/MCR, SFCR | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
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
| R17 | DeckRV § 5 Abs. 3 und 4 — Referenzzins, ZZR, Korridor | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R18 | MindZV — the 90/90/50 minima, §§ 11–12 and the § 13 cap | x | x | (x) | x | x | x | x | x | x | x |
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
| R31 | VVG §§ 1a, 6, 7, 7b, 7c, 214 and the VVG-InfoV | x | x | x | x | x | x | x | x | x | x |
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
| R56 | DAV Fachgrundsätze; the Höchstrechnungszins recommendation | x | x | x | x | x | x | x | x | x | x |

**One instrument is deliberately absent from the matrix and is recorded here instead.** BaFin *Rundschreiben 11/2017 (VA)*, the
*Kapitalanlagerundschreiben*, and the **Anlageverordnung (AnlV)** it interprets apply to **small insurers under §§ 212–217 VAG and to
domestic Pensionskassen and Pensionsfonds** — **not** to the Solvency II life insurers that write the ten delib products, which are
governed by the qualitative § 124 VAG prudent person principle [R7]. German market writing routinely cites AnlV quotas as if they
bound all insurers; since 1 January 2016 they do not bind the large life insurers at all. The circular is discussed inside R7 so that
no delib author misapplies an AnlV quota, and it carries no id of its own.

---

## 1. Prudential — the European layer

The Solvency II layer reaches German life business **through the VAG**, not directly. That is why this page cites VAG sections
throughout and directive articles only where the European layer is itself the point. **The Solvency II article numbers on this page
have now been read from the instruments themselves**: EUR-Lex serves, and the directive and the Delegated Regulation were both
opened in the German language version (see the per-entry `Retrieved` lines). One retrieval mechanic is worth recording, because it
is the difference between a citation and a landing page: `eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:...` truncates at
the sweep's byte cap and the truncated PDF will not open, whereas the ELI form
`eur-lex.europa.eu/eli/<type>/<year>/<number>/oj/deu/pdfa1b` delivers the complete Official Journal text.

(delib-reg-r1)=

### R1. Richtlinie 2009/138/EG — Solvabilität II

- **Publisher:** European Parliament and Council (EUR-Lex)
- **URL:** https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=CELEX:02009L0138-20250117 (the consolidated German text; the
  landing page https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32009L0138 also serves but returns only the recitals)
- **Accessed:** 2026-08-30
- **Retrieved:** yes (consolidated German HTML, 2.28 MB, current consolidated version 17/01/2025, read 2026-08-30; Artt. 37, 76, 77,
  77a–77e and 101 read in full)
- **Used for:** the valuation architecture behind the VAG's §§ 74–88 [R6] and the confidence level behind the SCR.
- **Annotation:** *Richtlinie 2009/138/EG des Europäischen Parlaments und des Rates vom **25. November 2009** betreffend die Aufnahme
  und Ausübung der Versicherungs- und der Rückversicherungstätigkeit (Solvabilität II) (Neufassung)*, **ABl. L 335 vom 17.12.2009,
  S. 1–155**; the version read here is the consolidated text as at **17 January 2025**. The Level 1 directive Germany transposes into
  the VAG, and therefore the instrument behind every valuation rule a German modeller actually reads as a VAG section.
  **What the articles say, read from the text.** **Article 76** is *Allgemeine Bestimmungen*: technical provisions must be held for
  all obligations, and their value is *"dem aktuellen Betrag, den Versicherungs- oder Rückversicherungsunternehmen zahlen müssten,
  wenn sie ihre Versicherungs- und Rückversicherungsverpflichtungen unverzüglich auf ein anderes Versicherungs- oder
  Rückversicherungsunternehmen übertragen würden"* — a transfer value, calculated market-consistently and *"auf vorsichtige,
  verlässliche und objektive Art und Weise"*. **The best-estimate-plus-risk-margin rule is Article 77(1)**, not Article 76:
  *"Der Wert der versicherungstechnischen Rückstellungen hat der Summe aus einem „besten Schätzwert“ und einer Risikomarge wie in
  Absatz 2 und 3 erläutert zu entsprechen."* **Article 77(2)** defines the best estimate as the probability-weighted average of future
  cash flows discounted on *"der maßgeblichen risikofreien Zinskurve"* — the reference BaFin's interpretive decision on capital-market
  models also uses [R21]. **Article 77(4)** carries the separate-calculation rule and its replicating-portfolio exception.
  **Article 77(5)** is the risk-margin cost-of-capital article: the rate must be the same for all undertakings and is reviewed
  periodically; **the directive does not state a number** — the 6 % is Level 2 [R2]. **Article 37(5)** confirms that a *Kapitalaufschlag*
  imposed for governance deficiencies is excluded from the Article 77(5) risk margin. **Article 101(3)** fixes the calibration:
  the SCR *"entspricht dem Value-at-Risk der Basiseigenmittel eines Versicherungs- oder Rückversicherungsunternehmens zu einem
  Konfidenzniveau von **99,5 %** über den Zeitraum eines Jahres"*, and Article 101(4) lists the six risk categories. **Articles 77a to
  77e** carry the extrapolation of the risk-free curve, the *Matching-Anpassung*, its calculation, the *Volatilitätsanpassung* and the
  technical information EIOPA must publish — the articles VAG §§ 80–83 transpose one for one [R6] [R4]. Governs the valuation basis of
  all ten delib products, which produce the gross best-estimate cash flows and stop short of the measurement the directive prescribes.
  **Corrected in this pass:** an earlier version of this entry attributed the best-estimate-plus-risk-margin rule to Article 76; the
  instrument puts it in Article 77(1). The **99.5 % one-year VaR** and the **25 November 2009** adoption date, previously carried as
  `[unverified]`, are confirmed above. **Still unverified:** nothing in this entry.

(delib-reg-r2)=

### R2. Delegierte Verordnung (EU) 2015/35

- **Publisher:** European Commission (EUR-Lex)
- **URL:** https://eur-lex.europa.eu/eli/reg_del/2015/35/oj/deu/pdfa1b (the complete Official Journal text). The form previously
  cited here, `.../legal-content/DE/TXT/PDF/?uri=CELEX:32015R0035&from=DE`, answers 200 but the body truncates at 3 MB and the
  truncated PDF does not open — it is not a retrieval and has been replaced.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (PDF, 797 pp., OJ L 12 of 17.1.2015, read 2026-08-30; Artt. 37, 38 and 39 read in full)
- **Used for:** the risk-margin construction and the cost-of-capital rate.
- **Annotation:** The Level 2 implementing measures, **dated 10 October 2014** and published at **ABl. L 12 vom 17.1.2015**, directly
  applicable without national transposition, and where the operative Solvency II detail lives — which is why a German modeller
  looking for contract boundaries, expense rules or standard-formula stresses reads this rather than the VAG.
  **Read from the text.** **Art. 37 *Berechnung der Risikomarge*** gives the formula
  $RM = CoC\cdot\sum_{t\ge 0} SCR(t)/(1+r(t+1))^{t+1}$, where $SCR(t)$ is the reference undertaking's SCR after $t$ years and
  $r(t+1)$ the basic risk-free rate for maturity $t+1$, chosen in the reporting currency; Art. 37(3) requires the total risk margin to
  be allocated to the Article 80 lines of business. **Art. 38 *Referenzunternehmen*** sets the transfer assumption: the whole portfolio
  of the original undertaking is taken over by another undertaking, which *"hat vor der Übertragung weder Versicherungs- oder
  Rückversicherungsverpflichtungen noch Eigenmittel"*, and life and non-life portfolios are assumed transferred to two different
  reference undertakings where the original undertaking writes both. **Art. 39 *Kapitalkostensatz*** is one sentence, quoted in full:
  *"Es wird davon ausgegangen, dass der in Artikel 77 Absatz 5 der Richtlinie 2009/138/EG genannte Kapitalkostensatz 6 % beträgt."*
  **The 6 % is therefore established from the instrument**, and the entry no longer rests on the 2025 review's "reduced from 6 to
  4.75 per cent" wording [R3]. **Still unverified:** the contract-boundary, expense and standard-formula articles were not read —
  they are outside what any delib model implements, and no delib document states a figure from them.

(delib-reg-r3)=

### R3. Richtlinie (EU) 2025/2 — the Solvency II review

- **Publisher:** Meyerthole Siems Kohlruss (MSK), reproduced on `aktuare.de`, for the commentary; European Parliament and Council for
  the instrument
- **URL:** https://aktuare.de/de/presse/pressemitteilungen/2682-pm-risikomarge-solvencyii.html
- **Accessed:** 2026-08-30
- **Retrieved:** the **commentary** yes (HTML, 25 kB, read 2026-08-30); **the directive itself, no** — no attempt was made to open
  Richtlinie (EU) 2025/2 on EUR-Lex in this pass, so every statement below about the amending directive is a statement about what an
  actuarial consultancy reports of it, not about what the instrument says
- **Used for:** the direction of travel on the risk margin, and the warning that a German solvency ratio quoted today sits under a
  regime that changes in 2027.
- **Annotation:** The amending directive from the 2019–2021 review, reported as **dated 27 November 2024** and **published in the
  Official Journal on 8 January 2025**, with **first application on 30 January 2027** and a two-year transposition deadline, so German
  transposition into the VAG is due before that date. Two changes matter to a liability model: the **Kapitalkostensatz underlying the
  risk margin falls from 6 % to 4.75 %** — the 6 % starting point is now established from Art. 39 of Delegated Regulation (EU) 2015/35
  [R2] — and an **exponential, time-dependent lambda factor** is to be introduced through the Level 2 regulation, reducing the level
  and volatility of the risk margin for long-term business, with **no lower bound** and an effect on **projected years ≥ 28** — a
  reduction most beneficial to insurers with long-term business, which is exactly the German life book. Otherwise the reform combines
  proportionality relief for small and non-complex undertakings with tightened qualitative requirements on governance, risk management
  and sustainability. **Still unverified, and the reason is now specific rather than general:** every date and every number in this
  entry comes from one consultancy note; the entry-into-force date is not stated there either, so only the 30 January 2027 first
  application is safe to assert. A reader who needs the amending directive should open it at
  `https://eur-lex.europa.eu/eli/dir/2025/2/oj/deu/pdfa1b`, which this pass did not do.

(delib-reg-r4)=

### R4. EIOPA — risk-free interest rate term structures, the UFR and the Volatilitätsanpassung

- **Publisher:** EIOPA
- **URL:** https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en, with
  https://www.eiopa.europa.eu/eiopa-publishes-ultimate-forward-rate-ufr-2026-2025-03-31_en for the UFR and
  https://www.eiopa.europa.eu/eiopa-updates-reference-portfolios-used-calculate-volatility-adjustment-solvency-ii-risk-free-rate-2025-12-09_en
  for the volatility-adjustment portfolios
- **Accessed:** 2026-08-30
- **Retrieved:** yes (three HTML pages, 258 kB / 90 kB / 93 kB, read 2026-08-30)
- **Used for:** the fact that the curve is a monthly EIOPA publication made binding by § 83 VAG, and the euro UFR level.
- **Annotation:** EIOPA **publishes the relevant risk-free interest-rate term structures monthly** — the landing page states
  *"Publication is done on a monthly basis"* and lists the monthly technical-information packages by year — and **§ 83 VAG makes
  their use binding on German undertakings** [R6], which is the hook by which a European technical publication becomes German law and
  the reason delib cites a VAG section for a European curve. **The UFR:** EIOPA's release of **31 March 2025** states that
  *"The UFR does not change for any of the relevant currencies compared to this year. This means an applicable UFR of **3.30%** as of
  **1 January 2026** for the euro."* **The volatility adjustment:** EIOPA updated the representative portfolios behind it on
  **9 December 2025**, will first use them for the **end-March 2026 VA calculation** published at the beginning of April 2026, and
  revises them annually, the next revision scheduled for end-2026 under Article 11.1.3 of the RFR Technical Documentation.
  **Corrected in this pass:** the technical documentation is not the 24 September 2024 edition — the landing page lists later versions
  of 10 December 2024, 23 June 2025, 16 October 2025, 9 December 2025 and, most recently, **26 May 2026 (Solvency II Review)**.
  **Still unverified:** the Last Liquid Point of 20 years and the Smith–Wilson extrapolation to the UFR over a 60-year horizon are
  **described in the RFR Technical Documentation PDF, which this pass did not open**, so they remain `[unverified]`; and **no numeric
  curve point and no German volatility-adjustment value was extracted for any date** — the monthly packages are Excel workbooks and
  delib takes no curve point from them.

---

## 2. Prudential — the Versicherungsaufsichtsgesetz---

## 2. Prudential — the Versicherungsaufsichtsgesetz

The VAG 2016 is the German transposition of Solvency II and the single statute a German life model is held to. Its architecture
matters for citation: **Teil 1** carries the general prudential rules (valuation, technical provisions, own funds, SCR, MCR,
investments, the public solvency report); **Teil 2 Kapitel 3 Abschnitt 1** the *besondere Vorschriften* for life insurance (§§
138–145); **Teil 3** the *Sicherungsfonds* (§§ 221 ff.); **Teil 4** the supervisory powers including § 314; **Teil 8** the
transitional provisions (§§ 351–353). That layout is why a German product document cites §§ 138–141 for the contract-side mechanics
and §§ 74–88 for the balance sheet, and why the two rarely appear in the same paragraph.

(delib-reg-r5)=

### R5. VAG 2016 — the statute, its architecture and Anlage 1 (die Sparten)

- **Publisher:** Bundesamt für Justiz via `gesetze-im-internet.de`
- **URL:** https://www.gesetze-im-internet.de/vag_2016/BJNR043410015.html (human-facing); the text was read from the canonical XML at
  https://www.gesetze-im-internet.de/vag_2016/xml.zip
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; Anlage 1 and § 294 read in full, read 2026-08-30)
- **Used for:** the *Sparten* classification that decides which supervisory regime a product sits in, and the statutory statement of
  the supervisory objective.
- **Annotation:** *Gesetz über die Beaufsichtigung der Versicherungsunternehmen*, **ausgefertigt 1. April 2015**, in force since
  1 January 2016 — the Solvency II transposition. **Anlage 1** is the *Einteilung der Risiken nach Sparten*, and it decides which
  supervisory regime a product sits in and which undertakings must join the *Sicherungsfonds* [R12]. The life-relevant *Sparten*,
  now read from the annex itself: **19 Leben** *"(soweit nicht unter den Nummern 20 bis 24 aufgeführt)"*; **20** Heirats- und
  Geburtenversicherung; **21 Fondsgebundene Lebensversicherung**; **22** Tontinengeschäfte; **23 Kapitalisierungsgeschäfte**;
  **24 Geschäfte der Verwaltung von Versorgungseinrichtungen**; and the list continues to **25 Pensionsfondsgeschäfte**, which the
  Nummer-19 exclusion does *not* reach. The relevance to delib is direct: **eight of the ten products sit in Sparte 19**;
  `fondsgebundene_rentenversicherung` sits in **Sparte 21** and therefore carries the separate *Anlagestock* rule of § 125 Abs. 5 VAG
  [R7]. **The supervisory objective, now quoted rather than inferred** — § 294 Abs. 1 VAG: *"Hauptziel der Beaufsichtigung ist der
  Schutz der Versicherungsnehmer und der Begünstigten von Versicherungsleistungen."* § 294 Abs. 4 adds the *Finanzaufsicht* limb, which
  must watch over *"die dauernde Erfüllbarkeit der Verpflichtungen aus den Versicherungen"* — the standard that reappears in § 138
  Abs. 1 VAG [R8] and § 341e HGB [R54]. **Resolved in this pass:** the Sparte 24 title, and § 294 as the general statement of
  supervisory objectives, both previously `[unverified]`. **Still unverified:** the date of promulgation of the *Anlage* itself is not
  separately stated; the statute's own *Ausfertigung* is 1 April 2015 and its consolidated `Stand` is recorded above.

(delib-reg-r6)=

### R6. VAG §§ 74–110, §§ 122–123 and § 40 — valuation, best estimate, risk margin, the LTG measures, SCR/MCR and the SFCR

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__88.html (human-facing; the per-section HTML page is a frameset shell and on
  the sweep answered with a connection reset). Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; §§ 40, 74, 76, 77, 78, 80, 81, 82, 83, 88, 96, 122 and 123 read in full, read
  2026-08-30)
- **Used for:** the two-liability-measure distinction, the statutory root of the DeckRV, and the LTG measures a quoted German solvency
  ratio depends on.
- **Annotation:** The block that makes the German *Solvabilitätsübersicht* a different object from the HGB accounts. **§ 74** is the
  market-consistent valuation rule — assets at the amount at which they *"zwischen sachverständigen, vertragswilligen und voneinander
  unabhängigen Geschäftspartnern getauscht werden könnten"*, liabilities at the amount at which they could be transferred or settled
  between the same parties, and, § 74 Abs. 3 Satz 2 verbatim: *"Eine Berichtigung der Bewertung, um die Bonität des
  Versicherungsunternehmens zu berücksichtigen, findet nicht statt."* — i.e. **no own-credit adjustment**. **§ 76 Abs. 1** makes
  technical provisions the sum of the best estimate under § 77 and the risk margin under § 78, *"getrennt zu berechnen"*; **§ 77**
  defines the best estimate as the probability-weighted average of future cash flows on the relevant risk-free curve, computed gross
  of reinsurance recoverables; **§ 78** defines the risk margin and, in Abs. 2 Satz 3, defers to any cost-of-capital rate the
  Commission fixes under Art. 86(d) of the directive — which it has, at 6 % [R2]. **§ 83** obliges undertakings to use the technical
  information EIOPA publishes for the best estimate, the matching adjustment and the volatility adjustment — the hook that makes the
  EIOPA curve binding German law [R4]. **§§ 80–82 are the long-term-guarantee measures**: § 80 the ***Matching-Anpassung*** on
  approval, with nine cumulative conditions including that the contracts *"führen nicht zu künftigen Prämienzahlungen"* and carry no
  policyholder options beyond a surrender option capped at the value of the assigned assets; § 81 its calculation; § 82 the
  ***Volatilitätsanpassung***, also on approval. **They are mutually exclusive on the same obligations** — § 80 Abs. 3 forbids the
  matching adjustment where the curve already carries a volatility adjustment under § 82 or the § 351 transitional, and § 82 Abs. 2
  forbids the volatility adjustment where a matching adjustment applies. Their presence moves a German solvency ratio by hundreds of
  percentage points, which is why **no delib document quotes a ratio without saying whether it is *mit* or *ohne
  Volatilitätsanpassung und Übergangsmaßnahmen*** [R53]. **§ 88 matters most to delib, because it is the legal root of the DeckRV.**
  § 88 Abs. 3 Satz 1 empowers the Bundesministerium der Finanzen, in agreement with the Bundesministerium der Justiz, to fix by
  *Rechtsverordnung* for the calculation of the *Deckungsrückstellung* — Nr. 1 — *"bei Versicherungsverträgen mit Zinsgarantie einen
  oder mehrere Höchstwerte für den Rechnungszins"*, and further Nr. 2 the discounting inputs of § 341f Abs. 2 HGB, Nr. 3 the
  *Höchstbeträge für die Zillmerung* and Nr. 4 the actuarial bases and valuation methods. The Sechste Verordnung of 19 July 2024 cites
  exactly this empowerment [R15]. **That is why the *Höchstzinssatz* is a ministerial regulation rather than a supervisory circular,
  and why the DAV's annual recommendation is a recommendation and not a decision** [R14] [R15] [R56]. **§ 96** allows the SCR to be
  determined by a *Standardformel* or an *internes Modell*, and lets the supervisor order an internal model where the risk profile
  deviates materially from the standard formula's assumptions; §§ 96–110 carry the SCR, with **Anlage 3** giving the standard-formula
  structure. **The MCR sections are now established: § 122 *Bestimmung der Mindestkapitalanforderung; Verordnungsermächtigung*** —
  the MCR being *"der Betrag anrechnungsfähiger Basiseigenmittel, unterhalb dessen die Versicherungsnehmer und Anspruchsberechtigten
  bei einer Fortführung der Geschäftstätigkeit einem unannehmbaren Risikoniveau ausgesetzt sind"*, its level fixed by ministerial
  regulation (the *Kapitalausstattungs-Verordnung*) — **and § 123 *Berechnungsturnus; Meldepflichten***. **§ 40** obliges publication
  of an annual **Solvabilitäts- und Finanzbericht** within 14 weeks of the year end (20 weeks at group level), and § 40 Abs. 3
  requires the effect of setting the matching and volatility adjustments to zero to be quantified — the practical route to a named
  insurer's SCR ratio, its transitional use and its LTG dependence. **Resolved in this pass:** § 74 Abs. 3 and § 78 were read; the
  MCR section numbers are **§§ 122–123**, so delib may now cite them, and the earlier note that "§§ 122–124 is commonly cited but
  § 124 is demonstrably *Anlagegrundsätze*" is explained — § 124 begins the *next* Kapitel. **Still unverified:** nothing in this
  entry; §§ 84–87, 89–95 and 97–110 were not read line by line and no delib document states anything from them.

(delib-reg-r7)=

### R7. VAG §§ 124 and 125 — Anlagegrundsätze, Sicherungsvermögen and the Anlagestock

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__124.html (human-facing); text read from the canonical XML
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; §§ 124 and 125 read in full, read 2026-08-30). The BaFin *Rundschreiben 11/2017 (VA)*
  was also opened (HTML, 298 kB) for the AnlV boundary.
- **Used for:** the absence of a quantitative asset rulebook (which is why every asset-return assumption in delib is `[std]`) and the
  *Anlagestock* rule that separates FRV and IDX from the general-account products.
- **Annotation:** **§ 124 *Anlagegrundsätze*** states the *Grundsatz der unternehmerischen Vorsicht* in eight numbered requirements
  and **fixes no quantitative limit at all**: assets must be invested so that *"Sicherheit, Qualität, Liquidität und Rentabilität des
  Portfolios als Ganzes sichergestellt werden"* (Abs. 1 Nr. 2), assets covering technical provisions additionally *"in einer der Art
  und Laufzeit der ... Verbindlichkeiten des Unternehmens angemessenen Weise"* (Nr. 3), conflicts of interest must resolve in
  policyholders' favour (Nr. 4), derivatives are permitted only for risk reduction or efficient portfolio management (Nr. 5), and
  Nr. 7 and 8 require appropriate mixing and spreading without naming a ratio. **This is why a German life insurer's asset mix — and
  hence the *Kapitalanlageergebnis* that drives the *Überschussbeteiligung* [R18] — is not derivable from a rulebook, and why every
  asset-return assumption in delib is `[std]`.** **§ 124 Abs. 2 is the unit-linked carve-out and is load-bearing for FRV and IDX:**
  Nr. 5 to 8 of Abs. 1 do **not** apply to life contracts where the policyholder bears the investment risk; instead the technical
  provisions must be replicated *"so genau wie möglich"* by the relevant units (Satz 2 Nr. 1) or, where benefits are bound
  *"direkt an einen Aktienindex oder an einen anderen ... Referenzwert"*, by the units representing that reference value (Satz 2
  Nr. 2); and **where such benefits include a guarantee, Abs. 1 Nr. 5 to 8 apply again to the assets backing the additional technical
  provisions** (Satz 2 Nr. 3). **§ 125 *Sicherungsvermögen*** — the ring-fenced pool covering policyholder claims. Abs. 2 defines its
  *Mindestumfang* as the sum of the balance-sheet values of the *Beitragsüberträge*, the *Deckungsrückstellung*, the reserves for
  outstanding claims and surrenders, for non-profit-related premium refunds and for unused premiums from dormant contracts, the part
  of the RfB attributable to declared but not yet allocated profit shares, liabilities to policyholders and premiums to be refunded —
  gross of reinsurance. Abs. 4: it *"ist gesondert von jedem anderen Vermögen zu verwalten und im Gebiet der Mitglied- oder
  Vertragsstaaten aufzubewahren"*. Abs. 6 allows *selbständige Abteilungen* on approval. **The *Anlagestock* is § 125 Abs. 5**, and
  the Absatz number is now established: *"Für jede Anlageart ist eine Abteilung des Sicherungsvermögens (Anlagestock) zu bilden"*
  where life contracts provide benefits in units of an open investment fund under § 1 Abs. 4 KAGB (Nr. 1), in units issued by an
  investment company (Nr. 2), in assets under the old § 2 Abs. 4 InvG (Nr. 3), or **bind them *"direkt an einen Aktienindex oder
  andere Bezugswerte"* (Nr. 4)**. That makes FRV structurally different from the general-account products — the unit fund is
  segregated, the policyholder bears its result, and the MindZV base differs [R21]. **For IDX the statute supplies the test rather
  than the answer:** an *Anlagestock* is required where the benefit is bound *directly* to the index, so whether a particular German
  *Indexpolice* sits in one turns on whether its index participation is a direct linkage or, as the market usually builds it, an
  option purchased in the general account financed out of the annual surplus. **That is a product-design question, not an open
  statutory one, and the reference implementation states which shape it models.** **The AnlV boundary**, recorded so no delib author
  misapplies it: BaFin *Rundschreiben 11/2017 (VA)* of **12 December 2017** interprets the **Anlageverordnung** and applies to small
  insurers under §§ 212–217 VAG and to Pensionskassen and Pensionsfonds only — **not** to the insurers writing the ten delib products.
  **Resolved in this pass:** the Absatz numbering of the Anlagestock rule (§ 125 Abs. 5), the *Mindestumfang* definition (§ 125
  Abs. 2), and the IDX classification question, which the statute answers as a test. **Still unverified:** **the AnlV's own content —
  the *Anlageformen* and the *Mischungs-* und *Streuungsquoten* — was not read and nothing in delib may state an AnlV quota.**

(delib-reg-r8)=

### R8. VAG § 138 — Prämienkalkulation in der Lebensversicherung; Gleichbehandlung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__138.html (human-facing; the per-section page is a 4.4 kB frameset shell with
  no statutory text). Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; § 138 read in full — it has exactly two Absätze — read 2026-08-30)
- **Used for:** the prudent-pricing rule behind the first-order bases, and the equal-treatment rule behind the surplus allocation.
- **Annotation:** **Absatz 1**, quoted in full because it is the root of the whole first-order/second-order distinction [R47]:
  *"Die Prämien in der Lebensversicherung müssen unter Zugrundelegung angemessener versicherungsmathematischer Annahmen kalkuliert
  werden und so hoch sein, dass das Lebensversicherungsunternehmen allen seinen Verpflichtungen nachkommen und insbesondere für die
  einzelnen Verträge ausreichende Deckungsrückstellungen bilden kann. Hierbei kann der Finanzlage des Versicherungsunternehmens
  Rechnung getragen werden, ohne dass planmäßig und auf Dauer Mittel eingesetzt werden dürfen, die nicht aus Prämienzahlungen
  stammen."* That clause forbids permanent cross-subsidy of a loss-making tariff out of shareholder funds; it is why the first-order
  bases carry margins that later emerge as *Überschuss* [R47], and it is the statutory root of the *dauernde Erfüllbarkeit* standard
  that reappears in § 341e HGB [R54] and in § 294 Abs. 4 VAG [R5] [R21]. **Absatz 2** is the equal-treatment rule, and the whole of
  it: *"Bei gleichen Voraussetzungen dürfen Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden."* Search results
  established that the **BGH, on 18 September 2024, Az. IV ZR 436/22**, tied § 138 Abs. 2 VAG to the contractual entitlement of
  **§ 153 Abs. 2 VVG** [R24]; **that decision was not retrieved in this pass and the citation remains `[unverified]`**. Together they
  mean the German *Überschussbeteiligung* is **discretionary in level but not in method**: an insurer may set the declaration, but the
  split between *Abrechnungsverbände* must follow causation. **Resolved in this pass, and it is a correction.** § 138 has **no Absätze
  beyond 1 and 2**, so the earlier "the Absätze beyond 1 and 2" caveat falls away. And the ***verursachungsorientiert*** charging rule
  is **not in § 138 at all**: it is **§ 140 Abs. 1 Satz 3 VAG** — *"Bei Maßnahmen nach Satz 2 Nummer 2 oder 3 sind die
  Versichertenbestände verursachungsorientiert zu belasten."* — and it is a rule about **charging the RfB draw-downs of § 140 Abs. 1
  Satz 2 Nr. 2 and 3 back to the sub-portfolios that caused them**, not a general causation principle for surplus allocation. The
  general causation principle for surplus is **§ 153 Abs. 2 VVG** [R24], and the RfBV adds a *verursachungsorientierter
  Verteilungsschlüssel* for returns out of the collective part [R19]. delib should therefore attribute the causation principle to
  § 153 Abs. 2 VVG, and use § 140 Abs. 1 Satz 3 VAG only for the loss-charging case. **Still unverified:** the BGH decision of
  18 September 2024 (IV ZR 436/22) — named in the earlier sweep, not opened here.

(delib-reg-r9)=

### R9. VAG § 139 — Überschussbeteiligung and the Sicherungsbedarf test on Bewertungsreserven

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__139.html (human-facing; the per-section page is a 6.0 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; § 139 read in full — it has exactly four Absätze — read 2026-08-30)
- **Used for:** the direct-credit-or-RfB structure every profit-participating delib model must carry, and the *Sicherungsbedarf* test.
- **Annotation:** **Absatz 1**, verbatim: *"Die für die Überschussbeteiligung der Versicherten bestimmten Beträge sind, soweit sie den
  Versicherten nicht unmittelbar zugeteilt wurden, in der Bilanz in eine Rückstellung für Beitragsrückerstattung einzustellen."*
  This is the structural fact behind the whole German surplus chassis: **surplus earmarked for policyholders either goes out
  immediately as *Direktgutschrift* or into the RfB, and nowhere else.** A delib model of a profit-participating product must carry
  both a direct credit and an RfB stock, or it has not modelled the product. **Absatz 2**, now read: for *Versicherungsaktiengesell­
  schaften* the *Vorstand* fixes the amounts to be set aside with the *Aufsichtsrat*'s consent, but amounts not owed as of right may
  be earmarked for the *Überschussbeteiligung* only so far as a **dividend of at least 4 per cent of the *Grundkapital*** can still be
  distributed out of the remaining balance-sheet profit — and no balance-sheet profit may be distributed beyond any *Sicherungsbedarf*
  under Absatz 4. **Absatz 3** is the LVRG's *Bewertungsreserven* restriction [R20]: valuation reserves *"aus direkt oder indirekt vom
  Versicherungsunternehmen gehaltenen festverzinslichen Anlagen und Zinsabsicherungsgeschäften"* count toward the § 153 VVG
  participation **only in so far as they exceed any *Sicherungsbedarf* aus den Versicherungsverträgen mit Zinsgarantie**. **Absatz 4**
  defines the test: the *Sicherungsbedarf* is the sum over contracts *"deren maßgeblicher Rechnungszins über dem maßgeblichen
  Euro-Zinsswapsatz zum Zeitpunkt der Ermittlung der Bewertungsreserven (Bezugszins) liegt"*, a single contract's being *"die
  versicherungsmathematisch unter Berücksichtigung des Bezugszinses bewertete Zinssatzverpflichtung des Versicherungsvertrags,
  vermindert um die Deckungsrückstellung"*; the reference rate is MindZV § 11 and the fifteen-year look-forward MindZV § 12 [R18].
  **The practical consequence for delib:** for a contract written on a 3.25 % or 4.00 % *Höchstzinssatz* [R15] the *Sicherungsbedarf*
  has for most of the last decade exceeded the fixed-income valuation reserves outright, so the *Bewertungsreserven* component of a
  maturity payout has often been **zero**. Any delib document that models such a payment must say which side of the test it assumes,
  and the assumption is `[std]`. **Resolved in this pass:** Absatz 2 is read, and **there is no Absatz 5** — § 139 ends at Absatz 4,
  so the earlier "Absätze 2 and 5 onwards" caveat is closed. **Still unverified:** the predecessor **§ 56a VAG a.F.**, which most
  German commentary still names — the repealed statute is not part of the consolidated VAG 2016 text and was not retrieved.

(delib-reg-r10)=

### R10. VAG §§ 140 and 145 — Rückstellung für Beitragsrückerstattung and the Verordnungsermächtigung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__140.html (human-facing; the per-section page is a 7.9 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; §§ 140 and 145 read in full, read 2026-08-30)
- **Used for:** the RfB ring fence, the escape hatches that financed the ZZR, and the chain from § 145 to the MindZV and the RfBV.
- **Annotation:** **§ 140 Abs. 1 Satz 1 — the use restriction.** Amounts allocated to the RfB *"dürfen nur für die
  Überschussbeteiligung der Versicherten einschließlich der durch § 153 des Versicherungsvertragsgesetzes vorgeschriebenen Beteiligung
  an den Bewertungsreserven verwendet werden"* [R24]. That is a hard ring fence: RfB money cannot be released to shareholders.
  **Three escape hatches, not two** — a correction this pass makes. § 140 Abs. 1 Satz 2 allows the RfB, *"soweit sie nicht auf bereits
  festgelegte Überschussanteile entfällt"*, to be drawn on **in Ausnahmefällen, with the supervisor's consent, in the policyholders'
  interest** in order to: **(1)** *"einen drohenden Notstand abzuwenden"*; **(2)** *"unvorhersehbare Verluste aus den
  überschussberechtigten Versicherungsverträgen auszugleichen, die auf allgemeine Änderungen der Verhältnisse zurückzuführen sind"*;
  or **(3)** *"die Deckungsrückstellung zu erhöhen, wenn die Rechnungsgrundlagen auf Grund einer unvorhersehbaren und nicht nur
  vorübergehenden Änderung der Verhältnisse angepasst werden müssen"*. Satz 3 then requires that, for measures under Nr. 2 or 3,
  *"die Versichertenbestände verursachungsorientiert zu belasten"* sind [R8]. **Escape hatch (3) is the statutory route by which the
  German industry financed the *Zinszusatzreserve* out of the free RfB during the low-rate decade** [R17], and it is why a German life
  insurer's RfB stock and its ZZR stock move against each other. **§ 140 Abs. 2** defines the *Missstand* — an inadequate allocation
  to, or inadequate use of, the RfB — and pins both to ministerial regulations: an allocation short of the minimum fixed under
  **§ 145 Abs. 2**, or an *"ungebundener Teil der Rückstellung für Beitragsrückerstattung"* exceeding the maximum fixed under
  **§ 145 Abs. 3**. **§ 140 Abs. 3** gives the supervisor the two plans, and the second one is **not** called a *Verteilungsplan*:
  a ***Zuführungsplan*** where the allocation falls short, and an ***Ausschüttungsplan*** where the *ungebundener Teil* exceeds the
  cap. **§ 140 Abs. 4 — not Abs. 1 Satz 2 — permits a *kollektiver Teil* of the RfB**, or several, *"der beziehungsweise die den
  überschussberechtigten Verträgen insgesamt zugeordnet ist beziehungsweise sind"* [R19]. **§ 145 *Verordnungsermächtigung*** is the
  statutory root of both regulations, and the mapping is now exact: **§ 145 Abs. 2 → MindZV §§ 4–9** (the minimum allocation in
  dependence on investment income, the risk result and the other results) [R18]; **§ 145 Abs. 3 → MindZV § 13** (the *Höchstbetrag des
  ungebundenen Teils*); **§ 145 Abs. 1 → MindZV §§ 10–12** (the assets in scope, the Euro swap rate and the valuation method for the
  interest obligation); **§ 145 Abs. 6, with § 140 Abs. 4 → RfBV** (the collective part) [R19]; and § 145 Abs. 4 the wording of the
  actuarial certification. Recording the chain correctly matters because delib product documents cite the MindZV percentages
  constantly. **Corrected in this pass, all three from the statutory text:** the escape hatches are **three**, not two; the plan under
  Abs. 3 Nr. 2 is an ***Ausschüttungsplan***; and the *kollektiver Teil* is **§ 140 Abs. 4**. **Also corrected:** the cap on the
  *ungebundener Teil* is **MindZV § 13**, not the RfBV — the RfBV caps the *collective* part and the *Teilbestand* ceilings [R19].
  **Resolved:** the term ***ungebunden*** **is statutory** — it appears in § 140 Abs. 2 Nr. 2 and Abs. 3 Nr. 2 VAG and is defined by
  reference to § 28 Abs. 8 Nr. 2 Buchst. h RechVersV [R54]; what remains market vocabulary is the *gebunden* / *frei* pairing, and
  delib defines those from the RechVersV components.

(delib-reg-r11)=

### R11. VAG §§ 141–143 — Verantwortlicher Aktuar, Treuhänder, Anzeigepflichten, and the deregulation of 29 July 1994

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__142.html (human-facing; the per-section page is a 4.3 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; §§ 141, 142 and 143 read in full, read 2026-08-30)
- **Used for:** the governance reason declared rates cluster, and the reason a German tariff's first-order bases are documented but
  not public.
- **Annotation:** **§ 141 *Verantwortlicher Aktuar in der Lebensversicherung*.** Every life insurer must appoint one; he must be
  *zuverlässig und fachlich geeignet*, and § 141 Abs. 1 Satz 4 fixes the experience test verbatim: *"Eine ausreichende
  Berufserfahrung ist regelmäßig anzunehmen, wenn eine mindestens dreijährige Tätigkeit als Versicherungsmathematiker nachgewiesen
  wird."* Abs. 3: he is appointed and dismissed by the *Aufsichtsrat*. Abs. 5 lists his duties — Nr. 1 to ensure that the premiums and
  the *Deckungsrückstellungen* comply with § 138 VAG, § 341f HGB and the regulation made under § 88 Abs. 3 VAG, *"dabei muss er die
  Finanzlage des Unternehmens insbesondere daraufhin überprüfen, ob die dauernde Erfüllbarkeit ... jederzeit gewährleistet ist"*;
  Nr. 2 the *versicherungsmathematische Bestätigung* under the balance sheet with an *Erläuterungsbericht* to the *Vorstand*; Nr. 3
  the duty to escalate to the supervisor; and **Nr. 4 the proposal on the Überschussbeteiligung**, which he submits *to the Vorstand*
  with a report on why it is appropriate. Abs. 6 then closes the loop to the supervisor: the *Vorstand* must lay the
  *Erläuterungsbericht* and the *Angemessenheitsbericht* before the supervisor, and must submit the actuary's proposal *unverzüglich*
  and notify the supervisor if it intends to depart from it — *"die Gründe für die Abweichung sind der Aufsichtsbehörde schriftlich
  oder elektronisch mitzuteilen"*. **That last item is the governance reason German declared rates cluster as tightly as the market
  data show** [R53]. **§ 142 *Treuhänder in der Lebensversicherung***, quoted in full because it is short and the date matters:
  *"Soweit bei den nach dem 28. Juli 1994 geschlossenen Lebensversicherungsverträgen die Prämien mit Wirkung für bestehende
  Versicherungsverträge geändert werden können, dürfen entsprechende Änderungen erst in Kraft gesetzt werden, nachdem ihnen ein
  unabhängiger Treuhänder zugestimmt hat."* The trustee step falls away where the change needs supervisory approval — the supervisory
  counterpart of § 163 Abs. 4 VVG [R27]. **§ 143 *Besondere Anzeigepflichten in der Lebensversicherung*** is the German equivalent of
  a tariff filing: after authorisation the undertaking must *"unverzüglich der Aufsichtsbehörde die Grundsätze für die Berechnung der
  Prämien und Deckungsrückstellungen einschließlich der verwendeten Rechnungsgrundlagen, mathematischen Formeln, kalkulatorischen
  Herleitungen und statistischen Nachweise unter deren Beifügung anzuzeigen"*, and again whenever they change. **This is why a German
  tariff's first-order bases exist as a documented, supervisor-visible object — and equally why they are not public, which is the
  structural reason delib's decrement tables must be `[std]` proxies** [R47]. **The 29 July 1994 boundary.** German life business
  splits into ***Altbestand*** and ***Neubestand***; § 142 draws the line at contracts concluded after 28 July 1994, and the RfBV's
  own definition (§ 2 Nr. 3 RfBV, retrieved) ties the *Altbestand* to § 336 VAG and to Art. 16 § 2 Satz 2 of the Drittes
  Durchführungsgesetz/EWG zum VAG of 21 July 1994, extending it to contracts concluded between 1 January 1995 and 31 December 1997
  that matched an *Altbestand* tariff and were settled jointly with it until 12 April 2008 [R19]. Until deregulation the AVB were part
  of a *genehmigungspflichtiger Geschäftsplan*; in the *Altbestand* that plan **continues to apply and changes still require
  approval**, while in the *Neubestand* contract design and premium calculation are **free within the statutory frame**, which is why
  the MindZV computes the minimum **getrennt für Alt- und Neubestand** [R18]. **Still unverified:** the claim that at deregulation
  *the entire RfB accumulated to 1994 was allocated exclusively to the Altbestand* is not in any retrieved instrument and is
  **[unverified]** — it is market history, not statute.

(delib-reg-r12)=

### R12. VAG §§ 221–236 and § 314, with Protektor — the Sicherungsfonds and the supervisor's crisis powers

- **Publisher:** Bundesamt für Justiz for the VAG and the SichLVV/SichLVFinV
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__222.html (human-facing); text read from the canonical XML
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; §§ 221, 222, 226 and 314 read in full, read 2026-08-30)
- **Used for:** the outer boundary of every guarantee in the library, and the two distinct statutory write-down powers.
- **Annotation:** **§ 221 *Pflichtmitgliedschaft*:** undertakings authorised to write **Sparten 19 bis 23 of Anlage 1** [R5], or
  substitutive health insurance under § 146, **must belong to a Sicherungsfonds** — *"mit Ausnahme der Pensions- und Sterbekassen"*,
  exactly the vehicles delib puts out of scope; Pensionskassen may join voluntarily (Abs. 2). **§ 222 — and the section is titled
  *Aufrechterhaltung der Versicherungsverträge*, not "the haircut".** Where the supervisor finds the § 314 Abs. 1 conditions met it
  informs the fund (Abs. 1) and, where necessary to protect policyholders, **orders the transfer of the entire portfolio, with the
  assets covering it, to the fund** (Abs. 2), the order carrying *dingliche Wirkung* and the rights and duties passing to the fund
  (Abs. 3). **The five-per-cent limb is Abs. 5, and it is mandatory, not discretionary:** where the fund's *Sicherungsvermögen* plus
  collectable *Sonderbeiträge* is insufficient to secure continuation of the contracts, *"setzt die Aufsichtsbehörde bei
  Lebensversicherungsverträgen die Verpflichtungen aus den Verträgen um maximal 5 Prozent der vertraglich garantierten Leistungen
  herab"*, and it may additionally order measures to prevent an extraordinary rise in early terminations. Abs. 6 lets the fund
  transfer the book on to authorised insurers and adapt the AVB with an independent trustee's confirmation; Abs. 7: the transferring
  undertaking's authorisation lapses. **§ 226 *Finanzierung*:** the fund's assets *"soll 1 Promille"* of the members' *versicherungs­
  technische Netto-Rückstellungen im Sinne der §§ 341e bis 341h des Handelsgesetzbuchs* not fall below (Abs. 4) [R54]; the **annual
  contributions of all members of the life fund sum to 0,2 Promille** of the same base (Abs. 5 Satz 2); and **Sonderbeiträge of up to
  1 Promille** may be levied where needed (Abs. 5 Satz 5). Note the base: the **statutory accounts, not the Solvency II balance
  sheet.** **Protektor Lebensversicherungs-AG** carries the statutory fund's tasks, transferred by the SichLVV; the Mannheimer case is
  reported as the only time it has been used, with a commitment declaration in June 2003, negotiations concluded 18 September 2003 and
  BaFin's approval of the *Bestandsübertragungsvertrag* on 1 October 2003 — **all of that is `[unverified]`: no Protektor document was
  opened in this pass**, and the statutory fund's own creation date is likewise not established from a retrieved instrument.
  **§ 314 *Zahlungsverbot; Herabsetzung von Leistungen*** is the crisis power and the single most important qualification on the word
  "guarantee". **Abs. 1:** where the undertaking *"dauerhaft nicht mehr imstande ist, seine Verpflichtungen zu erfüllen, die Vermeidung
  des Insolvenzverfahrens aber zum Besten der Versicherten geboten erscheint"*, the supervisor may order what is needed, and —
  verbatim — *"Alle Arten von Zahlungen, besonders Versicherungsleistungen, Gewinnverteilungen und bei Lebensversicherungen der
  Rückkauf oder die Beleihung des Versicherungsscheins sowie Vorauszahlungen darauf, können zeitweilig verboten werden."* So **a delib
  document modelling a surrender option says the option is suspendable by the supervisor.** **Abs. 2:** on the same condition the
  supervisor may *"die Verpflichtungen eines Lebensversicherungsunternehmens aus seinen Versicherungen dem Vermögensstand entsprechend
  herabsetzen"*, **may proceed unequally where special circumstances justify it**, must reduce the *Deckungsrückstellungen* first and
  recompute the *Versicherungssummen* afterwards, and — the sting — *"Die Pflicht der Versicherungsnehmer, die Versicherungsentgelte
  in der bisherigen Höhe weiterzuzahlen, wird durch die Herabsetzung nicht berührt."* **Abs. 3** allows both powers to be confined to
  a *selbständige Abteilung des Sicherungsvermögens* (§ 125 Abs. 6) [R7]. German life guarantees therefore sit under **two distinct
  write-down powers**: a fund-level 5 % reduction the supervisor must make, and an uncapped, asset-position-driven reduction it may
  make. **Corrected in this pass:** the § 222 haircut is expressed as a duty (*"setzt ... herab"*), not a discretion.

(delib-reg-r13)=

### R13. VAG §§ 351–353 — the Solvency II transitional measures and the 2024 recalculation

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__352.html (human-facing; `dejure.org/gesetze/VAG/352.html` also serves).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; §§ 351, 352 and 353 read in full, read 2026-08-30). The map-report 939 press release
  (HTML, 94 kB) was opened for the market effect.
- **Used for:** the run-off profile of the transitional and the reason a German solvency ratio is not comparable across 2024.
- **Annotation:** **§ 352 *Versicherungstechnische Rückstellungen*** is the *Rückstellungstransitional*: with the supervisor's
  approval a temporary deduction from technical provisions, applicable at the level of homogeneous risk groups, equal to a share of
  the difference between the provisions computed under § 75 at 1 January 2016 and those computed under the pre-2016 HGB and VAG rules.
  The run-off, now read verbatim: *"Der maximal abzugsfähige Anteil sinkt am Ende jedes Kalenderjahres linear von 100 Prozent während
  des Jahres ab 2016 auf 0 Prozent am 1. Januar 2032."* **§ 351** is the parallel transitional on the risk-free rates, with the same
  linear decline to 0 per cent on 1 January 2032, and **the two are mutually exclusive** (§ 351 Abs. 4 Nr. 2, § 352 Abs. 5).
  **§ 353:** an undertaking that would not meet the SCR without either transitional must, **within two months of that finding**,
  submit a plan for the phased introduction of measures restoring compliance by the end of the transitional period, and report on
  progress every twelve months; if the progress report shows compliance is unrealistic, the supervisor **revokes the approval**.
  **The 2024 recalculation, and its legal basis is now established.** § 352 Abs. 3 provides that the amounts used to compute the
  deduction *"dürfen mit Genehmigung oder müssen auf Verlangen der Aufsichtsbehörde alle 24 Monate oder, wenn sich das Risikoprofil
  des Unternehmens wesentlich verändert, häufiger neu berechnet werden"* — **so BaFin's Q2 2024 order to recalculate is an exercise of
  the supervisor's *Verlangen* under § 352 Abs. 3, not a general administrative act inventing a new power.** The market effect is in
  [R53]: the industry SCR ratio including transitionals fell from **663.6 % at end-2023 to 340.3 % at end-2024**, while the base ratio
  excluding transitionals was **308.6 %**, some 32 percentage points below — i.e. the recalculation removed an accounting cushion, not
  capital; map-report notes explicitly that *"von der Aufsicht keine pauschale Abschaffung des Rückstellungstransitionals angeordnet"*
  wurde. For delib the discipline is simple: **no delib model implements a transitional**, and any German solvency ratio quoted in a
  delib document must state whether it is before or after the 2024 recalculation. **Resolved in this pass:** the legal instrument
  behind the recalculation (§ 352 Abs. 3 VAG) and the exact wording of the § 352 linear formula, both previously `[unverified]`.

---

## 3. Prudential — reserving---

## 3. Prudential — reserving, the Höchstrechnungszins and the Zinszusatzreserve

The DeckRV is made under § 88 Abs. 3 VAG [R6] and fixes the *Rechnungsgrundlagen* of the German statutory *Deckungsrückstellung* — the
HGB reserve of § 341f HGB [R54], **not** the Solvency II best estimate. This distinction is the axis of the whole German reserving
picture and every delib document keeps it: an insurer carries **two liability measures**, and the *Überschussbeteiligung*, the
*Zinszusatzreserve* and the § 139 VAG *Bewertungsreserven* test all run on the **HGB** side.

(delib-reg-r14)=

### R14. DeckRV — the reserving regulation and its § 2, the Höchstzinssatz

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/deckrv_2016/BJNR076700016.html (human-facing); text read from the canonical XML at
  https://www.gesetze-im-internet.de/deckrv_2016/xml.zip
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250; §§ 1, 2, 3, 4, 5 and 5a read in full, read 2026-08-30). BaFin's
  Pensionskassen FAQ (HTML, 57 kB) was also opened.
- **Used for:** the maximum reserving rate every delib guarantee is anchored to, and the exceptions that bear on single-premium and
  annuity business.
- **Annotation:** *Verordnung über Rechnungsgrundlagen für die Deckungsrückstellungen*, **vom 18. April 2016 (BGBl. I S. 767)**, made
  under § 88 Abs. 3 Satz 1 Nr. 1 VAG [R6]. **§ 1** applies it to life insurers including Pensionskassen but excluding Sterbekassen, to
  accident insurers writing *Versicherungen mit Rückgewähr der Prämien*, and to insurers paying annuities out of liability and motor
  business — and only to *"Verträge, denen keine aufsichtsbehördlich genehmigten Tarife zugrunde liegen"*, i.e. the *Neubestand*
  [R11]. **The whole section list is now established: § 1 Geltungsbereich, § 2 Höchstzinssatz, § 3 Ausnahmen, § 4 Höchstzillmersätze
  und versicherungsmathematische Berechnungsmethode, § 5 Versicherungsmathematische Rechnungsgrundlagen, § 5a Übergangsregelung,
  § 6 Inkrafttreten.** **§ 2 Abs. 1 Satz 1, verbatim:** *"Bei Versicherungsverträgen mit Zinsgarantie, die auf Euro oder die nationale
  Währungseinheit eines an der Europäischen Wirtschafts- und Währungsunion teilnehmenden Mitgliedstaates lauten, wird der
  Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf 1 Prozent festgesetzt."* For other currencies BaFin fixes the rate
  (Satz 2). **§ 2 Abs. 2 Satz 1 fixes the cohort rule:** *"Bei Versicherungsverträgen mit Zinsgarantie gilt der von einem
  Versicherungsunternehmen zum Zeitpunkt des Vertragsabschlusses verwendete Rechnungszins für die Berechnung der
  Deckungsrückstellung für die gesamte Laufzeit des Vertrages."* — which is why the German in-force book is a stack of cohorts [R15]
  and why the ZZR exists at all. Abs. 2 also permits the original contract's rate on an internal *Versorgungsausgleich* split, and
  leaves § 5 Abs. 3 and 4 (the ZZR) untouched; Abs. 3 lets Pensionskassen use a uniform rate not exceeding the current
  *Höchstzinssatz* for a tariff generation, reduced in stages with the supervisor's consent. **§ 2 caps the *reserving* rate**, and
  the rate a policy guarantees is a tariff decision that may be lower — which the DAV states in terms [R56] and which § 88 Abs. 3
  Satz 1 Nr. 1 VAG confirms by empowering *Höchstwerte für den Rechnungszins*, not for the guarantee.
  **Two corrections this pass makes, both from the text.** **(1) The statute's own term is *Höchstzinssatz*.** The § 2 heading is
  *"Höchstzinssatz"* and the operative sentence says *Höchstzinssatz*; ***Höchstrechnungszins* is the market term**, used by the DAV
  [R56], by BaFin — whose FAQ headline reads *"Zum 1. Januar 2025 wird der Höchstrechnungszins in § 2 der
  Deckungsrückstellungsverordnung (DeckRV) von 0,25 Prozent auf 1,0 Prozent angehoben"* — and by the BMF. `buzer.de` was right and
  this page was wrong. **delib writes *Höchstzinssatz* when quoting or citing § 2 DeckRV, and *Höchstrechnungszins* when reporting the
  market and the DAV, saying once which is which.** **(2) § 3 *Ausnahmen* is live law, not a pre-2016 residue.** The earlier note that
  a summary attributing an 85 % yield cap to § 3 DeckRV "must be the pre-2016 regulation and must not be carried forward" is wrong.
  § 3 Abs. 1 provides that for **single-premium contracts with a term of up to eight years** in euro the applicable *Rechnungszins*
  may not exceed **85 per cent of the last month-end value of the *Umlaufrenditen der Anleihen der öffentlichen Hand* with a residual
  maturity matching the policy term**, taken from the Bundesbank's *Kapitalmarktstatistik*, measured at the date the premium is paid.
  § 3 Abs. 2 applies the same 85 per cent cap to **annuity contracts without a surrender value**, from the start of the annuity, for
  the following eight years and for the part of the *Deckungsrückstellung* attributable to the annuity in payment, against the
  arithmetic mean of the last month-end values for residual maturities of one to eight years, measured at annuity commencement.
  **That is directly relevant to `sofortrente` and to any single-premium point in KLV or RV**, and it is reported here without any
  change to a model: see the report note under §5 of the upgrade rules. **Still unverified:** the 60 % figure that used to accompany
  the 85 % in older commentary is **not** in the DeckRV 2016 — its home was the repealed Article 20 of Directive 2002/83/EC [R56],
  which this pass did not retrieve.

(delib-reg-r15)=

### R15. The Höchstzinssatz / Höchstrechnungszins rate history and the Sechste Verordnung of 19 July 2024

- **Publisher:** `recht.bund.de` for the Bundesgesetzblatt; Deutsche Aktuarvereinigung for the rate history
- **URL:** https://www.recht.bund.de/bgbl/1/2024/250/VO.html (the announcement page) with
  https://www.recht.bund.de/bgbl/1/2024/250/regelungstext.pdf?__blob=publicationFile&v=1 (the *Regelungstext* itself), and
  https://aktuar.de/content/PDF/Fachwissen/H%C3%B6chstrechnungszins_in_der_Lebensversicherung.pdf for the table
- **Accessed:** 2026-08-30
- **Retrieved:** yes — **the amending regulation** (PDF, 2 pp., BGBl. 2024 I Nr. 250, ausgegeben 24. Juli 2024, read 2026-08-30) and
  **the DAV fact sheet** (PDF, 2 pp., read 2026-08-30). The `VO.html` page carries only the metadata; the text is in the linked
  `regelungstext.pdf`.
- **Used for:** the cohort rate table every delib model point is anchored to, and the instrument that set the current rate.
- **Annotation:** **A word on the name before the numbers.** The statute's term is ***Höchstzinssatz*** (§ 2 DeckRV, [R14]);
  ***Höchstrechnungszins*** is the market term the DAV, BaFin and the BMF use, and it is the name of the table below. They denote the
  same rate. Neither is the ***Garantiezins***: the DAV fact sheet is explicit — *"Umgangssprachlich wird der Höchstrechnungszins oft
  mit dem Garantiezins gleichgesetzt. Dabei handelt es sich hierbei um verschiedene Werte!"* — the *Garantiezins* being what the
  insurer actually promises, and the reserving rate being capped by, and in practice historically equal to, the *Höchstrechnungszins*.
  **The rate history, now read from the DAV's own fact sheet** rather than reconstructed. The DAV publishes the series from 1903, the
  values to 1986 supplied by the GDV:

  | Period | Rate | Period | Rate |
  |---|---|---|---|
  | 1903–1922 | 3.50 % | 2004–2006 | 2.75 % |
  | 1923–1941 | 4.00 % | 2007–2011 | 2.25 % |
  | 1942–1986 | 3.00 % | 2012–2014 | 1.75 % |
  | 1987–06/1994 | 3.50 % | 2015–2016 | 1.25 % |
  | 07/1994–06/2000 | 4.00 % | 2017–2021 | 0.90 % |
  | 07/2000–2003 | 3.25 % | 2022–2024 | 0.25 % |
  |  |  | **2025** | **1.00 %** |

  Every row the previous version of this entry carried is confirmed, and the series is extended back three cohorts. **A German
  in-force book is a stack of these cohorts and every delib model point carries its cohort's rate rather than today's**, because
  § 2 Abs. 2 Satz 1 DeckRV fixes the rate for the whole term at conclusion [R14]. Two structural readings hold, and the extended series
  sharpens the second one. The **1994 move was an increase**, from 3.50 % to 4.00 %; so was the **1987 move**, from 3.00 % to 3.50 %,
  which the earlier version of this table did not reach — so the series has **three** increases in total, in 1987, 1994 and 2025, and
  is otherwise monotonically falling from 1994. The **2025 move to 1.00 % is therefore the first increase in thirty and a half
  years**, counting from July 1994. **The instrument.** The *Bundesministerium der Finanzen* amended the DeckRV by the ***Sechste
  Verordnung zur Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz vom 19. Juli 2024***, **BGBl. 2024 I Nr. 250,
  ausgegeben zu Bonn am 24. Juli 2024**. Its Artikel 1 is one sentence: *"In § 2 Absatz 1 Satz 1 der Deckungsrückstellungsverordnung
  vom 18. April 2016 (BGBl. I S. 767), die zuletzt durch Artikel 1 der Verordnung vom 22. April 2021 (BGBl. I S. 842) geändert worden
  ist, wird die Angabe „0,25 Prozent“ durch die Angabe „1 Prozent“ ersetzt."* Artikel 4: *"Diese Verordnung tritt vorbehaltlich des
  Satzes 2 am 1. Januar 2025 in Kraft. Artikel 2 tritt am Tag nach der Verkündung in Kraft."* The empowerment recited is § 88 Abs. 3
  Satz 1 Nr. 1 VAG [R6]. **The same regulation updated the absolute floors under the *Kapitalausstattungs-Verordnung*, and the euro
  figures are now on the record** — Artikel 2 raises § 1 Abs. 2 KapAusstV from 2.5 to **2.7 Mio. Euro** (Nr. 1), from 3.7 to
  **4 Mio. Euro** (Nrn. 2 and 3), from 3.6 to **3.9 Mio. Euro** (Nr. 4) and from 1.2 to **1.3 Mio. Euro** (Nr. 5), with effect from
  the day after promulgation, i.e. 25 July 2024. Artikel 3 makes the parallel 0,25 → 1 Prozent change in § 22 Abs. 1 Satz 3
  PFAV for Pensionsfonds. **For delib the operative number for a new-business tariff written today is 1.00 %**, and all ten products'
  `[std]` guaranteed rates are anchored to this table. **Resolved in this pass:** the BGBl citation and promulgation date, the exact
  amending words, the entry-into-force date, and the MCR absolute floors — all previously `[unverified]`. **Still unverified:** the
  precise within-year effective dates for the 2004, 2007, 2012, 2015, 2017 and 2022 steps. The DAV table gives them as whole calendar
  years, which implies a 1 January effect, and the 2025 step is proved to take effect on 1 January by the BGBl text above; but only
  the 1994 and 2000 steps are shown mid-year in the source, and delib does not assert a day for the others. **Note also:** the DAV
  fact sheet as retrieved is the edition written while the 2025 change was still a recommendation — its prose says *"Aktuell liegt er
  bei 0,25 Prozent"* while its table already carries the 2025 row, so the table has been updated and the surrounding text has not.

(delib-reg-r16)=

### R16. DeckRV § 4 — Höchstzillmersätze

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/deckrv_2016/__4.html (human-facing; the per-section page is a 6.2 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250; § 4 read in full, read 2026-08-30)
- **Used for:** the shape of the guaranteed surrender-value curve in the first years of every regular-premium delib product.
- **Annotation:** *Zillmerung* is the mechanism by which an insurer offsets a contract's one-off acquisition costs against its first
  premiums, and it is why a German endowment or annuity has a very low surrender value in its early years. **§ 4 Abs. 1, verbatim,
  because the three renderings this page previously carried in conflict are all partial views of one sentence:** *"Im Wege der
  Zillmerung werden die Forderungen auf Ersatz der geleisteten, einmaligen Abschlusskosten einzelvertraglich bis zur Höhe des
  Zillmersatzes ab Versicherungsbeginn aus den höchstmöglichen Prämienteilen gedeckt, die nach den verwendeten Berechnungsgrundsätzen
  in dem Zeitraum, für den die Prämie gezahlt wird, weder für Leistungen im Versicherungsfall noch zur Deckung von Kosten für den
  Versicherungsbetrieb bestimmt sind. Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten."* Reading it back
  against the three summaries: the cap is on the *Zillmersatz*; it is **25 ‰ (2.5 %) of the *Summe aller Prämien*** — the statute's
  own words, not *Beitragssumme*, which is the market term for the same quantity; the recovery is **einzelvertraglich**, **from
  *Versicherungsbeginn***, and out of **exactly those premium parts not needed for benefits or for administration**. All three
  renderings are reconciled and the conflict is closed. **§ 4 Abs. 2** ties the mechanism to the accounts: those premium parts, to the
  extent they have not yet covered the acquisition costs up to the *Zillmersatz* and therefore equal the receivable capitalisable
  under § 15 Abs. 1 RechVersV [R54], are deducted from the present value of future premiums in the individual
  *Deckungsrückstellung*. **§ 4 Abs. 3** carves out contracts where the statutory surrender values force a *Deckungsrückstellung*
  higher than § 341f HGB would give (§ 25 Abs. 2 RechVersV): there the *höchstmögliche Prämienteile* are those not needed to build the
  increased reserve — **the point at which § 169 VVG's floor and the DeckRV meet inside the reserve** [R28]. **§ 4 Abs. 4** fixes the
  cohort rule for the *Zillmersatz* exactly as § 2 Abs. 2 does for the rate: *"Der von einem Versicherungsunternehmen zum Zeitpunkt
  des Vertragsabschlusses verwendete Zillmersatz für die Berechnung der Deckungsrückstellung gilt für die gesamte Laufzeit des
  Vertrages."* — so a pre-2015 contract keeps its 40 ‰ basis. **The 2015 cut** from **40 ‰ to 25 ‰ with effect from 1 January 2015**
  is attributed to the LVRG [R20] and remains `[unverified]`: the current consolidated DeckRV shows only the 25 ‰ in force, and the
  amending instrument was not retrieved. For delib this parameter sets the shape of the guaranteed surrender-value curve in the first
  years of every regular-premium product, and it **interacts with § 169 Abs. 3 VVG's independent five-year-spread floor** [R28]: the
  DeckRV governs what the insurer may **reserve**, § 169 VVG what it must **pay**, and a model carrying a zillmerised reserve applies
  both separately, the tighter binding.

(delib-reg-r17)=

### R17. DeckRV § 5 Abs. 3 und 4 — the Referenzzins, the Zinszusatzreserve and the Korridormethode

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/deckrv_2016/__5.html (this per-section page does serve, 8.3 kB); text read from the
  canonical XML
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250; §§ 5 and 5a read in full, read 2026-08-30). BaFin's *Auslegungsentscheidung*
  on the projection of the *Referenzzins* (HTML, 82 kB) was also opened.
- **Used for:** the ZZR mechanism and the reference-rate construction that distinguishes it from the § 139 VAG test.
- **Annotation:** The ***Zinszusatzreserve*** is the additional German statutory reserve that arises under **§ 5 Abs. 4 DeckRV** when
  the *Referenzzins* falls below a contract's applicable *Rechnungszins*, producing a **higher *Deckungsrückstellung* than the tariff
  rate alone would give. It is an **HGB** reserve, rooted in **§ 341f Abs. 2 HGB** — which requires interest obligations to be taken
  into account where current or expected asset returns do not cover them [R54] — financed out of the result and, under § 140 Abs. 1
  Satz 2 Nr. 3 VAG, out of the free RfB [R10]; it exists in no other jurisdiction in this repository.
  **How the *Referenzzins* is built, now read from § 5 Abs. 3 rather than summarised.** The inputs are *"die von der Deutschen
  Bundesbank gemäß § 7 der Rückstellungsabzinsungsverordnung veröffentlichten Monatsendstände derjenigen Null-Kupon-Euro-Zinsswapsätze,
  die eine Laufzeit von 10 Jahren haben"*. For each of the **nine preceding calendar years** the annual mean of month-end levels is
  taken, **rounded up to two decimals**, with the years **2009 to 2013 fixed by the regulation itself at 3,81, 3,13, 3,15, 2,14 und
  1,96 Prozent**; for the current year the mean of the **first nine months** is taken on the same rounding. The sum of the nine annual
  means and the current-year mean is divided by ten (Satz 5). **The corridor is not a band around last year's rate — it is a
  two-signal damping rule, and this page previously described it loosely.** Satz 6 forms two differences, each rounded up to two
  decimals: **(1)** the ten-year mean of Satz 5 **less last year's *Referenzzins***; **(2)** **9 per cent of the current-year mean of
  Satz 4 less 9 per cent of last year's *Referenzzins***. Satz 7: *"Haben die Differenzen aus Satz 6 Nummer 1 und 2 das gleiche
  Vorzeichen, ergibt sich der Referenzzins des Kalenderjahres dadurch, dass der Referenzzins des vorherigen Kalenderjahres um die
  Differenz, die den kleineren Absolutbetrag hat, angepasst wird."* Satz 8: *"Andernfalls bleibt der Referenzzins gegenüber dem
  vorherigen Kalenderjahr unverändert."* And Satz 9 anchors the recursion in statute: *"Der Referenzzins des Kalenderjahres 2017
  beträgt 2,21 Prozent."* **That is why the rate can sit still for years while market swap rates move: when the long-run mean and the
  current-year signal point in opposite directions the rate does not move at all.** § 5a fixes the start date: the corridor version of
  § 5 Abs. 3 and 4 *"in der ab dem 23. Oktober 2018 geltenden Fassung ist erstmals für das Geschäftsjahr anzuwenden, das nach dem
  31. Dezember 2017 begonnen hat"*. **The ZZR test itself is § 5 Abs. 4**, and it is the reason the corridor matters: at each
  balance-sheet date the *Referenzzins* of the calendar year in which the financial year began is compared with *"dem höchsten in den
  nächsten 15 Jahren für einen Vertrag maßgeblichen Rechnungszins"*; where it is lower, the individual *Deckungsrückstellung* is
  computed on the **minimum of the applicable rate and the *Referenzzins* for each of the next fifteen years** and on the applicable
  rate thereafter. **Note the deliberate parallel with, and difference from, MindZV §§ 11–12** [R18]: the ZZR uses a **ten-year
  average damped by the corridor**, the *Sicherungsbedarf* test uses a **single month-end spot**, and both then run the same
  fifteen-year comparison. Confusing the two rates is one of the standard errors in describing a German life balance sheet.
  **The 2018 counterfactual and the quantum** — under the old method the rate would have fallen from 2.21 % (2017) to about 1.9 %,
  where under the corridor it fell only to 2.10 %, worth about ten billion euros of relief industry-wide for 2018; the rate is
  reported as 1.57 % at 31 December 2022 and unchanged into 2025; the ZZR stock is reported at about €84 bn at the 2024
  balance-sheet date from a €96 bn peak at end-2021, with 2024 the first year requiring no addition and about €5 bn flowing back.
  **All of that remains `[unverified]`: it is trade press, no supervisory source states it, and this pass retrieved none of it.**
  What the pass does establish is the mechanism above and the statutory 2017 anchor of 2.21 %. **The released funds reach
  policyholders through a higher *Überschussbeteiligung***, the mechanical link to the declared rates in [R53].

---

## 4. Prudential — the surplus regulations---

## 4. Prudential — the surplus regulations, the LVRG and the supervisor

(delib-reg-r18)=

### R18. MindZV — the minimum allocation to the RfB, §§ 11–13 and the § 13 cap

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html (human-facing); text read from the canonical XML
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688; §§ 4, 6, 7, 8, 11, 12 and 13 read in
  full, read 2026-08-30)
- **Used for:** the 90/90/50 arithmetic floor under the German *Überschussbeteiligung*, and the *Sicherungsbedarf* machinery.
- **Annotation:** *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*, **vom 18. April 2016**, made under
  § 145 Abs. 1 to 3 VAG [R10] — the arithmetic floor under the German *Überschussbeteiligung*, and the whole section list runs
  §§ 1–17 plus two Anlagen. **The three result sources and their minimum shares, now read.**
  **§ 6 Abs. 1 — *Kapitalanlageergebnis*, 90 %:** the minimum allocation *"beträgt 90 Prozent der nach § 3 Absatz 1 anzurechnenden
  Kapitalerträge abzüglich der rechnungsmäßigen Zinsen"* (net of the externally financed reserve part and of interest on pension
  provisions). **The subtraction of the *Rechnungszinsen* is the crucial detail: the guarantee is funded first, and only the excess is
  shared 90/10.** Two asymmetries the earlier version of this entry did not carry: where the contract promises **more than 90 %** of
  the creditable investment income, *"ist die Mindestzuführung entsprechend zu erhöhen"* (Satz 4); and where the result is negative
  **because the creditable investment income falls short of the *Rechnungszinsen***, the minimum allocation is **100 per cent** of
  that shortfall rather than zero (Sätze 5 and 6) — i.e. an investment shortfall must be made good in full, it is not shared.
  § 6 Abs. 2 sets a separate 90 % minimum for the collective part of the RfB under § 140 Abs. 4 VAG [R19].
  **§ 7 — *Risikoergebnis*, 90 %**, raised from 75 % by the LVRG with effect from 7 August 2014 [R20] — the percentage is read from
  the regulation, the amending date remains `[unverified]`. **§ 8 — *Übriges Ergebnis*, 50 %**, the cost result. Both floor a
  negative result at zero and treat *Alt-* and *Neubestand* separately.
  **§ 4 — assembly:** the three sources are defined by **named cells of *Nachweisung 213* of the BerVersV** [R54] — Kapitalanlage­
  ergebnis from Zeilen 07 and 08, Risikoergebnis from Zeilen 04, 05, 12 and 13, übriges Ergebnis from Zeilen 06, 09, 10, 11, 14 and
  15. From their sum the ***Direktgutschrift*** attributable to profit-participating contracts is **deducted**, including final
  payments on the *Bewertungsreserven* participation where paid as a direct credit; *Alt-* and *Neubestand* are computed separately;
  and *"Ergibt sich rechnerisch eine negative Mindestzuführung zur Rückstellung für Beitragsrückerstattung, wird sie durch Null
  ersetzt."* Those rules make the MindZV a **minimum transfer to the RfB, not a minimum payout**.
  **§§ 11–12 — the *Sicherungsbedarf* machinery** behind § 139 Abs. 3 und 4 VAG [R9]. **§ 11**, verbatim: the *Bezugszins* is
  *"der von der Deutschen Bundesbank gemäß § 7 der Rückstellungsabzinsungsverordnung veröffentlichte Null-Kupon-Euro-Zinsswapsatz mit
  einer Laufzeit von zehn Jahren am Ende desjenigen Monats ..., der dem Zeitpunkt der Ermittlung der Bewertungsreserven vorangeht"* —
  **a single month-end spot, and note the difference from the ZZR rate** [R17], which is a ten-year average damped by the corridor:
  different numbers from the same Bundesbank series, and **confusing them is one of the standard errors in describing a German life
  balance sheet**. **§ 12:** that rate is compared with *"dem höchsten in den nächsten 15 Jahren für einen Vertrag maßgeblichen
  Rechnungszins"*; where it is lower the interest obligation is valued on the minimum of the two for fifteen years and on the
  applicable rate thereafter, *"im Übrigen ... dieselben Berechnungs- und Bewertungsansätze wie bei der Deckungsrückstellung"*; the
  fifteen-year window is why the test bites hardest on annuity business.
  **§ 13 — the cap on the *ungebundener Teil* of the RfB, and it lives here, not in the RfBV** [R19]. The sum of the *ungebundener
  Teil* within the meaning of § 28 Abs. 8 Nr. 2 Buchst. h RechVersV [R54] and any part already fixed beyond the following year may not
  exceed **0,8 × SP + 2 × (FR + DG) + Max{0; (1 − DNZ / 0,05) × SP}**, where SP is the capital requirement under §§ 9–14 KapAusstV
  (§ 17 for Pensionskassen), FR the fixed part of the RfB attributable to next year's declared shares, DG next year's expected direct
  credit, and DNZ the average net investment return of the last three financial years. That is the cap § 140 Abs. 2 Nr. 2 and Abs. 3
  Nr. 2 VAG police with an *Ausschüttungsplan* [R10]. **Why this entry is the centre of the library:** six of the ten products are
  profit-participating general-account contracts whose credited return is the guarantee plus a discretionary share of these three
  results, so any delib model of the surplus chassis represents at least the three result sources, the 90/90/50 floor, the
  direct-credit-versus-RfB split, and the fact that the floor binds on the **HGB** accounts. **Resolved in this pass:** all three
  percentages, the § 4 assembly rule, the § 11 and § 12 wording, and the location and formula of the *ungebunden* cap.
  **Still unverified:** the LVRG's 7 August 2014 effective date for the 75 → 90 % change.

(delib-reg-r19)=

### R19. RfBV — the collective part of the Rückstellung für Beitragsrückerstattung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/rfbv/BJNR030000015.html (human-facing; the sweep hit a connection reset on this host
  page). Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: geändert durch Art. 1 V v. 19.7.2017 I 3037; Eingangsformel and §§ 1–5 read in full — the
  whole regulation — read 2026-08-30)
- **Used for:** the collective-RfB mechanism that makes cross-cohort smoothing lawful, and the ceilings that bound it.
- **Annotation:** *Verordnung über den kollektiven Teil der Rückstellung für Beitragsrückerstattung*, **ausgefertigt 10. März 2015**,
  **BGBl. I 2015 S. 300**, made under **§ 56b Abs. 2 Satz 2 VAG a.F.** (its *Eingangsformel*, inserted by Art. 6 Nr. 6 of the Act of
  3 April 2013) and now operating on **§ 140 Abs. 4 VAG** [R10]. It applies to life insurers **except *Sterbekassen* and *regulierte
  Pensionskassen* im Sinne von § 233 Abs. 1 oder 2 VAG** (§ 1). The regulation has **five sections**, and the section attribution in
  the earlier version of this entry was off by one — a correction this pass makes. **§ 2 is *Begriffsbestimmungen***, and it is more
  useful than a definitions section usually is: it defines the *ungebundene RfB* by reference to § 28 Abs. 8 Nr. 2 Buchst. h RechVersV
  [R54], and it defines ***Altbestand***, ***Neubestand*** and ***Teilbestand*** — a *Teilbestand* being one of the *Bestandsgruppen*
  of the *Neubestand* named in Anlage 1 Abschnitt D BerVersV, or one of the *Abrechnungsverbände* of the *Altbestand* fixed in the
  approved *Geschäftsplan* [R11].
  **§ 3 carries both ceilings.** **§ 3 Abs. 2 — the ceiling on the *ungebundene* RfB of the *Teilbestände*:** on establishing a
  collective part the undertaking must fix an ***Obergrenze*** expressed as a **percentage of the declared profit shares fixed for
  allocation in the following year plus the expected cost in the following year of the declared *Direktgutschrift* of the
  *Teilbestände*** — that is the percentage base the earlier version could not establish. *"Der Prozentsatz beträgt mindestens 100,
  ist für alle Teilbestände identisch und darf gegenüber dem Vorjahr nur mit Zustimmung der Aufsichtsbehörde geändert werden."*
  Where a *Teilbestand*'s *ungebundene* RfB exceeds the ceiling and no *Rückführungen* take place at the balance-sheet date, the
  excess is transferred to the collective part. **§ 3 Abs. 3 — the ceiling on the collective part itself:** a percentage of the
  capital requirement under §§ 9–14 KapAusstV (§ 17 for Pensionskassen), and *"Der Prozentsatz beträgt **höchstens 60**"*, again
  changeable only with the supervisor's consent. Where the collective part exceeds it, the excess must be returned to the
  *Teilbestände* at the following balance-sheet date; earlier returns are possible with consent. **The distribution key is
  prescribed:** the share of each *Teilbestand* in the *Rohüberschuss*, or in the *Rohüberschuss ohne Direktgutschrift*, in each case
  only where positive; another ***verursachungsorientierter Verteilungsschlüssel*** is possible with the supervisor's consent; and
  the same key must be used for all *Teilbestände*. **§ 3 Abs. 1** provides that collective parts *"können nur durch Rückführung ...
  aufgelöst werden"*, and **§ 3 Abs. 4** allows returns to individual *Teilbestände* with financing deficits, with consent.
  **§ 4** requires contractual obligations that stand in the way of an allocation to the collective part to be respected, and applies
  § 3 separately after a portfolio transfer; **§ 5** is the transitional for financial years beginning before 1 January 2016.
  **Why it exists:** the collective part lets an insurer hold surplus committed to policyholders as a class but not yet attributed to
  any *Teilbestand*, which is what makes cross-cohort smoothing legally possible without breaching § 138 Abs. 2 VAG [R8]; BaFin's
  interpretive decision of 19 April 2011 governs how the MindZV floor interacts with it [R21]. **Vocabulary for delib:** the statutory
  term is ***ungebundene*** RfB — used in the RfBV, in § 140 VAG and in MindZV § 13, and defined by § 28 Abs. 8 Nr. 2 Buchst. h
  RechVersV as *"den ungebundenen Teil (Rückstellung für Beitragsrückerstattung ohne die Buchstaben a bis g)"*; German market writing
  says *freie RfB* for the same thing and *gebundene RfB* for the a-to-g components — declared but unallocated current and final
  shares, the minimum *Bewertungsreserven* amounts, and the three tranches of the *Schlussüberschussanteilfonds* [R54].
  **Corrected in this pass:** the *Teilbestand* ceiling is § 3 Abs. 2 and the collective ceiling § 3 Abs. 3 (the earlier text put them
  in §§ 2 and 3); the RfBV implements **§ 140 Abs. 4** VAG, not § 140 Abs. 1 Satz 2; and **the cap on the *ungebundener Teil* of the
  RfB as a whole is MindZV § 13, not the RfBV** [R18]. **Resolved:** the percentage bases in § 3, and the whole section list.
  **Still unverified:** **whether the German market actually uses the collective part, and how large it is** — that is a market fact
  no instrument states and no retrieved document reports. Load-bearing for the surplus chassis of KLV, RV, BAS, RIE, IDX and SOF.

(delib-reg-r20)=

### R20. LVRG 2014 — the Lebensversicherungsreformgesetz

- **Publisher:** Bundesgesetzblatt, via `dejure.org` for the citation; Deutscher Bundestag for the government bill
- **URL:** https://dejure.org/BGBl/2014/BGBl._I_S._1330 with https://dserver.bundestag.de/btd/18/017/1801772.pdf
- **Accessed:** 2026-08-30
- **Retrieved:** the **BGBl citation record** yes (HTML, 46 kB, read 2026-08-30) and the **government bill** yes (PDF, 40 pp.,
  BT-Drs. 18/1772 of 18.06.2014, read 2026-08-30). **The Act's own text was not retrieved** — dejure serves the citation record, not
  the *Regelungstext*, and the consolidated statutes it amended carry the result without naming the amending article.
- **Used for:** the three changes that reshaped the German surplus chassis, and the reason delib cites the current sections rather
  than the LVRG.
- **Annotation:** *Gesetz zur Absicherung stabiler und fairer Leistungen für Lebensversicherte (Lebensversicherungsreformgesetz –
  LVRG)*, **vom 01.08.2014**, published in **Bundesgesetzblatt Jahrgang 2014 Teil I Nr. 38, ausgegeben am 06.08.2014, Seite 1330** —
  the citation record now read rather than reported. The bill is **BT-Drs. 18/1772 of 18 June 2014**, and its own summary of the
  reform is the cleanest statement of what the Act did: the problem is that *"Ein lang anhaltendes Niedrigzinsumfeld würde mittel- bis
  langfristig die Fähigkeit der privaten Lebensversicherungsunternehmen bedrohen, die den Versicherten zugesagten Zinsgarantien zu
  erbringen"*, and the answers are, verbatim from the bill: **(1)** *"insbesondere müssen die Versicherten künftig mit mindestens
  90 Prozent (statt wie bislang 75 Prozent) an den Risikoüberschüssen beteiligt werden"* — now § 7 MindZV [R18], **the single change
  that most affects delib's biometric products**, since a German term, BU or Pflege tariff's surplus is predominantly a risk surplus;
  **(2)** *"Der Höchstzillmersatz für die bilanzielle Anrechnung von Abschlusskosten wird gesenkt. Hierdurch soll Druck auf die
  Versicherungen ausgeübt werden, die Abschlusskosten zu senken."* — now § 4 Abs. 1 Satz 2 DeckRV at 25 ‰ [R16]; and **(3)**
  *"Die Regelungen zur Beteiligung an den Bewertungsreserven werden dahingehend angepasst, dass die Ausschüttung von
  Bewertungsreserven an die ausscheidenden Versicherten begrenzt wird, soweit dies zur Sicherung der den Bestandskunden zugesagten
  Garantien"* erforderlich ist — the *Sicherungsbedarf* test the bill drafts as § 56a VAG a.F. and which now sits in § 139 Abs. 3
  und 4 VAG [R9] with MindZV §§ 11–12 [R18]; the bill's draft wording of the *Bewertungsreserven* restriction is word for word what
  § 139 Abs. 3 VAG now says. Alongside them the bill strengthens supervisory powers and raises cost transparency, its own
  *Erfüllungsaufwand* estimate naming *"die Information der Versicherungsnehmer über die Abschlussprovision (§ 61 Absatz 3 Satz 1
  VVG)"* as the largest new information duty. The constitutionality of the LVRG's insertion into § 153 Abs. 3 Satz 3 VVG was litigated
  and upheld [R36]. **Still unverified:** the **effective dates** — 7 August 2014 for the risk-surplus share and 1 January 2015 for
  the *Höchstzillmersatz* — are not stated in the bill's summary and the Act's own *Inkrafttreten* article was not read; the numeric
  40 ‰ → 25 ‰ step is likewise not in the bill's summary, which says only that the rate is lowered. The LVRG amended the **old** VAG
  (§ 56a a.F. and others) and **the mapping from those sections onto the 2016 VAG is not established from a retrieved instrument**,
  so delib cites the current sections and describes the LVRG as the reform that introduced the rules, not as the current legal source.
  **Whether the LVRG also introduced a commission cap (*Provisionsdeckel*) is not established and is not asserted** — the bill's
  summary does not mention one.

(delib-reg-r21)=

### R21. BaFin — the FinDAG, the MaGo and the Auslegungsentscheidungen

- **Publisher:** Bundesamt für Justiz for the FinDAG; BaFin for the rest
- **URL:** https://www.gesetze-im-internet.de/findag/BJNR131010002.html, with
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ for the index,
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ae_110419_mindestzufuehrung_rfb_va.html and
  https://www.bafin.de/SharedDocs/Downloads/DE/Auslegungsentscheidung/dl_ae_151204_projektion_referenzzins_va.html
- **Accessed:** 2026-08-30
- **Retrieved:** partly. The **FinDAG** yes (HTML, 265 kB); the **Auslegungsentscheidung index** yes (HTML, 156 kB); the
  ***Zusammenwirken von Mindestzuführung zur RfB und Teilkollektivierung*** yes (HTML, 89 kB); the ***Projektion des Referenzzinses
  gemäß § 5 Abs. 3 DeckRV*** yes (HTML, 82 kB); the **MaGo consultation page** yes (HTML, 89 kB). **The MaGo circular itself,
  no** — the English page cited in `_research` returns HTTP 404 and the German circular was not opened; and **the other six
  Auslegungsentscheidungen listed below were not opened individually**.
- **Used for:** the institutional frame, the two distinct actuarial roles, and the interpretive decisions delib's surplus and FRV
  entries lean on.
- **Annotation:** **The institution.** BaFin was created in 2002 by the *Finanzdienstleistungsaufsichtsgesetz*, merging the three
  predecessor *Bundesaufsichtsämter* into a single *Allfinanzaufsicht*; it sits under the *Rechts- und Fachaufsicht* of the
  Bundesministerium der Finanzen (§ 2 FinDAG) and supervises under the KWG, the VAG and the WpHG. **The supervisory objective is now
  quoted from the VAG rather than paraphrased from BaFin's own pages** — § 294 Abs. 1 VAG makes the *Hauptziel der Beaufsichtigung*
  the protection of policyholders and beneficiaries, and § 294 Abs. 4 makes the *Finanzaufsicht* watch over the *dauernde
  Erfüllbarkeit* of the obligations [R5], the same standard that appears in § 341e HGB [R54] and § 138 Abs. 1 VAG [R8]. There is
  **no second national insurance supervisor**: Germany runs conduct and prudential supervision inside one authority. **The MaGo.**
  *Rundschreiben 2/2017 (VA) — Mindestanforderungen an die Geschäftsorganisation von Versicherungsunternehmen* interprets the
  business-organisation provisions of the VAG and of Delegated Regulation (EU) 2015/35 and binds BaFin's own application of them; a
  **revision was consulted on as Konsultation 05/2025**, whose page was retrieved. For delib the MaGo is why the
  ***versicherungsmathematische Funktion*** exists alongside the § 141 VAG *Verantwortlicher Aktuar* [R11] — **two distinct actuarial
  roles, which delib does not conflate.** **The publication and in-force dates of 25 January and 1 February 2017 and the 14 July 2025
  revision date remain `[unverified]`: the circular was not opened.** **The Auslegungsentscheidungen** are BaFin's published
  statements of how it will apply a provision: not law, but binding on BaFin's own practice and carrying much of the operative detail
  the regulations leave open. Two were read in this pass — **(4) *Zusammenwirken von Mindestzuführung zur RfB und
  Teilkollektivierung* (19 April 2011)** [R19] and **(8) *Projektion des Referenzzinses gemäß § 5 Abs. 3 DeckRV*** [R17]. The
  remaining six are listed here as known references, each **`[unverified]` as to content because it was not opened**: (1)
  *Wechselwirkungen zwischen Überschussbeteiligung und Neugeschäft* (4 December 2015); (2) *Ausweis der Beteiligung an den
  Bewertungsreserven in der Standmitteilung* (10 June 2016), reported to require the **full** allocation to be disclosed, a guaranteed
  *Sockelbeteiligung* alone not sufficing for what is now § 155 Abs. 1 Satz 1 VVG [R25]; (3) *Mindestzuführung in der fondsgebundenen
  Lebensversicherung* (22 December 2009), **load-bearing for FRV**, whose MindZV base is not the general account's; (5) *Auswirkung
  von passiver Rückversicherung auf die Angemessenheit der Zuführung zur RfB*; (6) *Anforderungen an Kapitalmarktmodelle*
  (11 November 2016), reported to require calibration consistent with the risk-free curve of **Art. 77(2)** of Directive
  2009/138/EG — an article now read at [R1]; and (7) *Latente Steuern auf versicherungstechnische Rückstellungen*
  (22 February 2016).

---

## 5. Contract law---

## 5. Contract law — the Versicherungsvertragsgesetz

German life contract law is a single statute whose **Kapitel 5 (§§ 150–171) is *halbzwingend***: **§ 152 Absatz 1 bis 4** and
**§§ 153 bis 155, 157, 158, 161 und 163 bis 170** may not be varied to the detriment of the policyholder, the insured person or the
*Eintrittsberechtigter* (§ 171 Satz 1 VVG). That one sentence is why a delib model may treat the surrender-value floor, the paid-up
right, the suicide clause and the profit-participation entitlement as **contractual facts rather than insurer choices**, and why the
discretionary layer sits only where the statute leaves room. **Every section in this block has now been read from the canonical
statutory XML**, which is why the entries below quote the statute rather than a summary of it; the whole block runs on one `Stand`,
recorded once here: **VVG 2008, ausgefertigt 23. November 2007, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read
2026-08-30.

(delib-reg-r22)=

### R22. VVG 2008 — the statute, Kapitel 5 and § 171 (halbzwingende Vorschriften)

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/BJNR263110007.html (human-facing); text read from the canonical XML at
  https://www.gesetze-im-internet.de/vvg_2008/xml.zip
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; §§ 170 and 171 read in full, and the whole of Kapitel 5 and 6 across [R23]–[R29], read
  2026-08-30)
- **Used for:** the semi-mandatory boundary that decides which contract terms a delib model may treat as fixed.
- **Annotation:** The VVG 2008, **ausgefertigt 23. November 2007**, replaced the VVG of 1908 with effect from 1 January 2008.
  **Teil 1** carries the general provisions (§§ 1–73: advice and information §§ 6, 6a, 7, 7a–7d; withdrawal § 8; pre-contractual
  disclosure §§ 19–22; premium default §§ 33, 37, 38); **Teil 2** the branches, of which **Kapitel 5 Lebensversicherung** runs
  §§ 150–171 and **Kapitel 6 Berufsunfähigkeitsversicherung** §§ 172–177; **Teil 3** the final provisions including § 214. A single
  statute therefore supplies the death-cover, savings-contract and disability-income rules, and **§ 176 imports §§ 150–170 into the BU
  chapter *entsprechend, soweit die Besonderheiten dieser Versicherung nicht entgegenstehen*** [R29].
  **§ 171 *Abweichende Vereinbarungen*, quoted in full, and it corrects what this page previously said:** *"Von § 152 Absatz 1 bis 4
  und den §§ 153 bis 155, 157, 158, 161 und 163 bis 170 kann nicht zum Nachteil des Versicherungsnehmers, der versicherten Person oder
  des Eintrittsberechtigten abgewichen werden. Für das Verlangen des Versicherungsnehmers auf Umwandlung nach § 165 und für seine
  Kündigung nach § 168 kann die Schrift- oder die Textform vereinbart werden."* The earlier version read *"§ 152 Abs. 1 und 2"*; the
  statute says **Absatz 1 bis 4**, and it protects three classes of person, not one. A *halbzwingende* provision may be varied in the
  policyholder's favour; a detrimental variation is not void as such, but **the insurer may not rely on it**. Note what is **not**
  listed: §§ 150, 151, 156, 159, 160, 162 and **§ 152 Abs. 5** — so beneficiary designation, the consent rule and the due date of the
  first premium are freely variable. **§ 170 *Eintrittsrecht*:** on *Arrest*, *Zwangsvollstreckung* or the opening of insolvency
  proceedings over the policyholder's estate, a **named** beneficiary may, with the policyholder's consent, step into the contract,
  satisfying the creditors or the insolvency estate *"bis zur Höhe des Betrags, dessen Zahlung der Versicherungsnehmer im Fall der
  Kündigung des Versicherungsverhältnisses vom Versicherer verlangen könnte"*; where no beneficiary is named the same right belongs to
  the spouse or *Lebenspartner* and the children (Abs. 2); and the entry is made by notice to the insurer **within one month** of the
  beneficiary learning of the attachment or of the opening of insolvency (Abs. 3). **Two chapters have no VVG home at all, and this
  matters for delib:** there is no statutory chapter for *Pflegerentenversicherung* — reached, if at all, through § 177 Abs. 1, whose
  wording is now read at [R29] and is about *"eine dauerhafte Beeinträchtigung der Arbeitsfähigkeit"*, not about *Pflegebedürftigkeit*
  — and none for *indexgebundene* Rentenversicherung, which in law is a *fondsgebundene* or *klassische* contract with the index
  participation living entirely inside § 153 [R24]. **Resolved in this pass:** the § 171 list, the § 170 mechanics and the fact that
  **§ 156 and § 160 exist and are not semi-mandatory** — § 160 is read at [R26]. **Still unverified:** the **VVG a.F.** numbering
  (§ 5a, § 176 Abs. 3/4), which is corroborated only through case-law summaries [R36] — the repealed statute is not part of the
  consolidated text. Load-bearing for all ten products.

(delib-reg-r23)=

### R23. VVG §§ 8 and 152 — the 14-day and 30-day Widerrufsrechte

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__8.html (this per-section page does serve, 8.7 kB); text read from the
  canonical XML
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; §§ 8 and 152 read in full, read 2026-08-30)
- **Used for:** the first-duration decrement that is legally distinct from lapse, and the settlement basis on withdrawal.
- **Annotation:** **§ 8 Abs. 1** — the policyholder may withdraw the contract declaration **within 14 days**, in *Textform*, without
  reasons, and *"zur Fristwahrung genügt die rechtzeitige Absendung"*. **§ 8 Abs. 2:** the period begins with the conclusion of the
  contract, but **not before** the policyholder has received in *Textform* the *Versicherungsschein*, the contract terms including the
  AVB and the VVG-InfoV information [R31], **and** a compliant instruction on the withdrawal right; for products needing a PRIIPs or
  PEPP *Basisinformationsblatt* [R32] it does not begin before that has been provided either, and **the burden of proving receipt is
  on the insurer**. **§ 8 Abs. 4 Satz 2:** *"Das Widerrufsrecht erlischt spätestens zwölf Monate und 14 Tage nach dem
  Vertragsschluss."* — but Satz 3 disapplies that long-stop where the policyholder was never instructed under Abs. 2 Satz 2 Nr. 2,
  which is the statutory root of the *Widerrufsjoker* [R36]. Abs. 3 lists four exclusions (terms under a month, provisional cover,
  Pensionskassen contracts based on employment terms, and large risks).
  **§ 152 makes five deviations for life insurance, and the Absatz mapping in the earlier version of this entry was wrong.**
  **Abs. 1:** the period is **30 days** and the right lapses at the latest **24 Monate und 30 Tage** after conclusion.
  **Abs. 2:** where cover began before the end of the period **and the § 9 Abs. 2 Satz 1 Nr. 1 condition is met**, the insurer owes
  (1) the part of the premiums attributable to the time after receipt of the withdrawal **and** (2) *"den Rückkaufswert einschließlich
  der Überschussanteile nach § 169"*. **Abs. 3 — not the due-date rule, as this page previously said — covers the case where that
  condition is *not* met:** the insurer then owes the same premium part and *"den Rückkaufswert einschließlich der Überschussanteile
  nach § 169 oder, wenn dies für den Versicherungsnehmer günstiger ist, die für das erste Jahr gezahlten Prämien"*. **Abs. 4**
  disapplies § 9 Abs. 2 bis 4. **Abs. 5 is the due-date rule:** *"Abweichend von § 33 Abs. 1 ist die einmalige oder die erste Prämie
  unverzüglich nach Ablauf von 30 Tagen nach Zugang des Versicherungsscheins zu zahlen."* This is the most model-relevant conduct rule
  in the German life chapter: **a withdrawal exercised after cover has begun is settled at the surrender value, not at premiums paid,
  except where the first-year-premium comparison in Abs. 3 is more favourable** — so the § 169 floor [R28] reaches into the withdrawal
  window. For delib it fixes a **first-duration decrement legally distinct from lapse**, and a model that lumps the two into one lapse
  rate must say so. **Resolved in this pass:** the whole Absatz-to-rule mapping inside §§ 8 and 152, previously `[unverified]`, and
  the twelve-month long-stop's exception. **Still unverified:** **§ 9 VVG (*Rechtsfolgen des Widerrufs*) was not opened**, so the
  content of the § 9 Abs. 2 Satz 1 Nr. 1 condition that switches between § 152 Abs. 2 and Abs. 3 is named but not read, and the
  *Fernabsatz* interaction through § 356a BGB (§ 8 Abs. 1 Satz 3) is likewise not established.

(delib-reg-r24)=

### R24. VVG § 153 — Überschussbeteiligung and the hälftige Beteiligung an den Bewertungsreserven

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__153.html (human-facing; the per-section page is a 4.9 kB frameset shell —
  `dejure.org/gesetze/VVG/153.html` also serves). Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; § 153 read in full — four Absätze — read 2026-08-30)
- **Used for:** the entitlement, the method and the timing of the *Bewertungsreserven* half-share.
- **Annotation:** The article the whole KLV / RV / IDX chassis hangs on, and the German counterpart to the French *participation aux
  bénéfices* — but **an individual contractual entitlement with a statutory default, not a collective minimum computed from a
  regulated account**. **Abs. 1 — the entitlement, verbatim:** *"Dem Versicherungsnehmer steht eine Beteiligung an dem Überschuss und
  an den Bewertungsreserven (Überschussbeteiligung) zu, es sei denn, die Überschussbeteiligung ist durch ausdrückliche Vereinbarung
  ausgeschlossen; die Überschussbeteiligung kann nur insgesamt ausgeschlossen werden."* There is no partial opt-out. **Abs. 2 — the
  method:** *"Der Versicherer hat die Beteiligung an dem Überschuss nach einem verursachungsorientierten Verfahren durchzuführen;
  andere vergleichbare angemessene Verteilungsgrundsätze können vereinbart werden."*, with Satz 2 excluding the § 268 Abs. 8 HGB
  amounts. The statute names the principle and **does not prescribe the algorithm**, which is precisely why the three surplus sources
  (*Zinsüberschuss*, *Risikoüberschuss*, *Kostenüberschuss*) and their declared rates are insurer-discretionary and **every level in
  delib is `[std]` unless a *Tarifblatt* supplies it**. **Abs. 3 — Bewertungsreserven:** *"Der Versicherer hat die Bewertungsreserven
  jährlich neu zu ermitteln und nach einem verursachungsorientierten Verfahren rechnerisch zuzuordnen. Bei der Beendigung des Vertrags
  wird der für diesen Zeitpunkt zu ermittelnde Betrag zur Hälfte zugeteilt und an den Versicherungsnehmer ausgezahlt; eine frühere
  Zuteilung kann vereinbart werden."* **Abs. 3 Satz 3 is the LVRG override [R20], and its VAG cross-references are now established
  exactly rather than carried as an unverified list:** the supervisory rules securing *dauernde Erfüllbarkeit* remain unaffected,
  *"insbesondere die §§ 89, 124 Absatz 1, § 139 Absatz 3 und 4 und die §§ 140 sowie 214 des Versicherungsaufsichtsgesetzes"* — with
  the effect that *Bewertungsreserven* from fixed-interest assets and hedges count toward the policyholder's share only so far as they
  exceed a *Sicherungsbedarf* [R9] [R18]; in a low-rate environment this reduced the payable half to zero for many portfolios, and the
  BGH held the rule constitutional [R36].
  **Abs. 4 is new to this page and is directly model-relevant:** *"Bei Rentenversicherungen ist die Beendigung der Ansparphase der
  nach Absatz 3 Satz 2 maßgebliche Zeitpunkt."* — for an annuity contract the half-share of *Bewertungsreserven* falls due at **the
  end of the accumulation phase**, not at the end of the contract. That fixes the timing for RV, FRV, IDX, BAS and RIE and removes an
  ambiguity a deferred-annuity model would otherwise have to invent.
  **For delib:** the *Bewertungsreserven* leg is path- and balance-sheet-dependent in a way a gross liability cash flow model cannot
  reproduce, so the reference implementations model the declared *laufende Überschussbeteiligung* and the *Schlussüberschussanteil*
  explicitly and treat the *Bewertungsreserven* share as an explicitly excluded component, saying so. **Resolved in this pass:** the
  Abs. 1 and Abs. 2 attributions, the Satz numbering, the VAG cross-reference list, and the annuity timing rule of Abs. 4.
  **Still unverified:** the BGH decision **IV ZR 436/22 of 18 September 2024** tying Abs. 2 to § 138 Abs. 2 VAG [R8], which was not
  opened in this pass.

(delib-reg-r25)=

### R25. VVG §§ 154 and 155 — Modellrechnung and Standmitteilung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__154.html (human-facing; the per-section page is a 4.4 kB frameset shell).
  Text read from the canonical XML, with § 2 VVG-InfoV for the three rates.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; §§ 154 and 155 read in full, and § 2 VVG-InfoV, Stand: zuletzt geändert durch Art. 13 G v.
  26.5.2026 I Nr. 156, read 2026-08-30)
- **Used for:** the statutory illustration rates a product spec must reproduce, and the annual statement that makes declared rates a
  citable `[S#]` source class.
- **Annotation:** **§ 154 *Modellrechnung*, Abs. 1:** where the insurer makes *"bezifferte Angaben zur Höhe von möglichen Leistungen
  über die vertraglich garantierten Leistungen hinaus"*, it must give the policyholder a *Modellrechnung* showing the possible
  *Ablaufleistung* *"unter Zugrundelegung der Rechnungsgrundlagen für die Prämienkalkulation mit drei verschiedenen Zinssätzen"*.
  **The carve-out is now confirmed and it is wider than "Risikoversicherungen":** *"Dies gilt nicht für Risikoversicherungen und
  Verträge, die Leistungen der in § 124 Absatz 2 Satz 2 des Versicherungsaufsichtsgesetzes bezeichneten Art vorsehen."* — i.e.
  **unit-linked and index-linked contracts owe no *Modellrechnung* at all** [R7], which resolves what this page previously carried as
  a one-summary claim and is load-bearing for FRV and IDX. Abs. 2 requires the insurer to state clearly that the model calculation is
  a computation on fictitious assumptions from which no contractual claim follows.
  **The three rates are § 2 Abs. 3 VVG-InfoV, quoted exactly** — the earlier version of this entry lettered them a)/b)/c) and wrote
  *Prozentpunkts*; the regulation numbers them and writes *Prozentpunktes*: *"Die vom Versicherer zu übermittelnde Modellrechnung im
  Sinne von § 154 Abs. 1 des Versicherungsvertragsgesetzes ist mit folgenden Zinssätzen darzustellen: 1. dem Höchstrechnungszinssatz,
  multipliziert mit 1,67, 2. dem Zinssatz nach Nummer 1 zuzüglich eines Prozentpunktes und 3. dem Zinssatz nach Nummer 1 abzüglich
  eines Prozentpunktes."* **The arithmetic consequence for delib is sharp:** at a *Höchstzinssatz* of **1.00 %** [R15] the statutory
  triple is **1.67 % / 2.67 % / 0.67 %**, so a `product-spec.md` reproducing a published *Modellrechnung* reproduces that triple, and
  a technical note projecting an illustrative surplus scenario either uses those rates or says explicitly that it does not and why.
  **§ 155 *Standmitteilung*.** Abs. 1 Satz 1: for profit-participating insurance the insurer must inform the policyholder **annually
  in Textform** *"über den aktuellen Stand seiner Ansprüche unter Einbeziehung der Überschussbeteiligung"*, and Satz 2 requires it to
  state *"inwieweit diese Überschussbeteiligung garantiert ist"*. **Abs. 1 Satz 3 then enumerates five items, which the earlier
  version of this entry did not have:** (1) the agreed benefit on a claim plus profit participation at the stated reference date;
  (2) the agreed benefit plus **guaranteed** profit participation at maturity or annuity commencement assuming the contract continues
  unchanged; (3) the same **assuming the contract is made paid-up**; (4) **the payout amount on the policyholder's termination**; and
  (5) **the sum of premiums paid**, for contracts concluded from **1 July 2018** (obtainable on request otherwise). Abs. 3 is the
  second limb: where the insurer has made quantified statements about the future development of the profit participation, it must
  point out deviations of the actual development from them — making the *Modellrechnung* a benchmark it keeps reporting against.
  For delib this is not a cash flow: it is the reason **published Standmitteilung specimens are a legitimate `[S#]` source class** for
  declared surplus rates and for the guaranteed/non-guaranteed split — and items (2), (3) and (4) map one for one onto what a delib
  model produces. **Resolved in this pass:** the § 124 Abs. 2 Satz 2 VAG carve-out, and the Satz numbering within § 155 — the
  provision now has Absätze, so BaFin's 2016 interpretive decision citing "§ 155 Satz 1" refers to what is now **§ 155 Abs. 1 Satz 1**
  [R21], the numbered list having been added with effect for contracts from 1 July 2018. **Still unverified:** the instrument that
  renamed the *Jährliche Unterrichtung* to *Standmitteilung*.

(delib-reg-r26)=

### R26. VVG §§ 150, 159, 160, 161 and 162 — Einwilligung, Bezugsberechtigung, Selbsttötung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__159.html (human-facing; the per-section page is a 4.0 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; §§ 150, 159, 160, 161 and 162 read in full, read 2026-08-30)
- **Used for:** the issue rules, the beneficiary defaults and the three-year suicide clause that make a duration-dependent death
  benefit.
- **Annotation:** **§ 150 *Versicherte Person*.** Abs. 2: where a policy is taken out **on the death of another person** and the
  agreed benefit **exceeds *"den Betrag der gewöhnlichen Beerdigungskosten"***, that person's **written consent** is required for
  validity — *"dies gilt nicht bei Lebensversicherungen im Bereich der betrieblichen Altersversorgung"*, an exception this page did
  not previously carry; and the policyholder may not represent the other person in giving that consent. Abs. 3: where a parent insures
  a **minor child**, consent is required only where the insurer is also to pay on death **before completion of the seventh year of
  life** above that threshold. **Abs. 4 answers the threshold question the earlier version left open, without giving a number:**
  *"Soweit die Aufsichtsbehörde einen bestimmten Höchstbetrag für die gewöhnlichen Beerdigungskosten festgesetzt hat, ist dieser
  maßgebend."* — the ceiling is a supervisory determination, not a statutory figure, which is why **no euro threshold appears in the
  statute and any figure in a delib document is `[std]`.** The funeral-cost boundary is what makes *Sterbegeldversicherung* a distinct
  product in German law rather than a small RLV — which is why delib excludes it. **§ 159 *Bezugsberechtigung*** — Abs. 1: the
  policyholder may, in case of doubt, designate and substitute a beneficiary **without the insurer's consent**; Abs. 2: a
  **widerruflich** designated third party *"erwirbt das Recht auf die Leistung des Versicherers erst mit dem Eintritt des
  Versicherungsfalles"*; Abs. 3: an **unwiderruflich** designated one *"bereits mit der Bezeichnung als Bezugsberechtigter"* — so
  **an irrevocable designation removes the unilateral disposal and a model point carrying one should not carry a surrender
  assumption**. **§ 160 *Auslegung der Bezugsberechtigung* is now retrieved**, and its four default rules close the gap the earlier
  version recorded: several beneficiaries without stated shares take **equally**, and a share not acquired **accrues to the others**
  (Abs. 1); a designation of the policyholder's *Erben* means, in case of doubt, **those called as heirs at the time of death, in
  proportion to their shares of the estate**, and *"Eine Ausschlagung der Erbschaft hat auf die Berechtigung keinen Einfluss"*
  (Abs. 2); a right not acquired by the third party falls to the policyholder (Abs. 3); and the *Fiskus* as heir gets **no** benefit
  right (Abs. 4). **§ 161 *Selbsttötung*** — Abs. 1: in *Todesfallversicherung* the insurer is not liable where the insured person
  *"sich vor Ablauf von drei Jahren nach Abschluss des Versicherungsvertrags vorsätzlich selbst getötet hat"*, unless the act was
  committed *"in einem die freie Willensbestimmung ausschließenden Zustand krankhafter Störung der Geistestätigkeit"*; Abs. 2: the
  period **may be extended, but only *durch Einzelvereinbarung*** — not in the AVB, a restriction this page did not previously carry;
  Abs. 3: where the insurer is not liable it must nevertheless pay *"den Rückkaufswert einschließlich der Überschussanteile nach
  § 169"* [R28]. **§ 162 *Tötung durch Leistungsberechtigten*** — Abs. 1 releases the insurer where the **policyholder** intentionally
  and unlawfully brings about the death of **another** insured person, and Abs. 2 treats a **beneficiary's** designation as not made
  where the beneficiary does so. **Model consequence for RLV and the death cover inside KLV:** the first three policy years carry a
  benefit that is the **surrender value rather than the sum assured for the suicide sub-cause of death** — a *duration-dependent
  benefit definition*, not a rate adjustment, and therefore a listed modeling pitfall even in a model that does not split the death
  decrement by cause. **Resolved in this pass:** the age-seven rule, the *bAV* exception, the Einzelvereinbarung restriction, and the
  whole of § 160. **Still unverified:** **no figure or supervisory determination fixing *gewöhnliche Beerdigungskosten* was
  retrieved** — § 150 Abs. 4 names the mechanism, and BaFin's determination under it was not opened — so any euro threshold in a delib
  document remains `[std]`.

(delib-reg-r27)=

### R27. VVG § 163 — Prämien- und Leistungsänderung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__163.html (human-facing; the per-section page is a 5.6 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; § 163 read in full — four Absätze — read 2026-08-30)
- **Used for:** the reason a German BU or Pflegerente premium is not unconditionally guaranteed, and the timing of a re-set.
- **Annotation:** **Abs. 1 — three cumulative conditions, confirmed word for word.** The insurer may re-fix the agreed premium where
  **(1)** *"sich der Leistungsbedarf nicht nur vorübergehend und nicht voraussehbar gegenüber den Rechnungsgrundlagen der vereinbarten
  Prämie geändert hat"*; **(2)** the newly fixed premium on the corrected bases *"angemessen und erforderlich ist, um die dauernde
  Erfüllbarkeit der Versicherungsleistung zu gewährleisten"*; and **(3)** *"ein unabhängiger Treuhänder die Rechnungsgrundlagen und
  die Voraussetzungen der Nummern 1 und 2 überprüft und bestätigt hat"* — the contractual counterpart of the supervisory trustee of
  § 142 VAG [R11]. **The mispricing bar, Abs. 1 Satz 2:** a re-set is excluded *"insoweit ..., als die Versicherungsleistungen zum
  Zeitpunkt der Erst- oder Neukalkulation unzureichend kalkuliert waren und ein ordentlicher und gewissenhafter Aktuar dies
  insbesondere anhand der zu diesem Zeitpunkt verfügbaren statistischen Kalkulationsgrundlagen hätte erkennen müssen"* — **the insurer
  may not reprice its way out of its own mispricing.**
  **Abs. 2 corrects what this page previously said.** The benefit-reduction alternative is **the policyholder's right, not the
  insurer's**: *"Der Versicherungsnehmer kann verlangen, dass an Stelle einer Erhöhung der Prämie nach Absatz 1 die
  Versicherungsleistung entsprechend herabgesetzt wird."* Only *"bei einer prämienfreien Versicherung"* is the **insurer** entitled to
  reduce the benefit on the Abs. 1 conditions. **Abs. 3 is new to this page and is a cash-flow timing rule:** the re-set or the
  reduction *"werden zu Beginn des zweiten Monats wirksam, der auf die Mitteilung der Neufestsetzung oder der Herabsetzung und der
  hierfür maßgeblichen Gründe an den Versicherungsnehmer folgt"* — so a monthly model implementing a re-pricing event has a defined
  effective date and a minimum one-month notice lag. **Abs. 4:** the trustee step falls away where the change requires supervisory
  approval. **For delib:** this is why a German BU or Pflegerente premium is *not* unconditionally guaranteed even where it is level,
  and why the correct description is a ***Bruttobeitrag* with a *Zahlbeitrag* below it**, the gap being a discretionary surplus rebate
  withdrawable **without invoking § 163 at all** [R53]; a model that treats the *Zahlbeitrag* as guaranteed for the whole term is
  making a behavioural assumption and the notes must label it as one. **Still unverified:** whether § 163 reaches *kapitalbildende*
  premiums in practice, or is effectively confined to biometric covers — **the statute draws no branch line at all, so this is a
  question about practice, not text, and no retrieved document settles it**; and the legal characterisation of the *Zahlbeitrag*
  mechanism as operating through § 153 rather than § 163 remains the compiler's synthesis.

(delib-reg-r28)=

### R28. VVG §§ 165–170 — prämienfreie Versicherung, Kündigung, Rückkaufswert and the Stornoabzug

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__165.html (human-facing; the per-section page is a 4.5 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; §§ 165, 166, 167, 168 and 169 read in full, read 2026-08-30)
- **Used for:** the surrender-value floor, the paid-up path, and the termination carve-out that defines BAS.
- **Annotation:** The most model-relevant entry in the contract layer, and the one this pass changed most.
  **§ 165 *Prämienfreie Versicherung*:** Abs. 1 — the policyholder may *"jederzeit für den Schluss der laufenden Versicherungsperiode
  die Umwandlung der Versicherung in eine prämienfreie Versicherung verlangen, sofern die dafür vereinbarte Mindestversicherungs­
  leistung erreicht wird"*; if it is not reached the insurer pays *"den auf die Versicherung entfallenden Rückkaufswert
  einschließlich der Überschussanteile nach § 169"*. Abs. 2: the paid-up benefit is computed *"nach anerkannten Regeln der
  Versicherungsmathematik mit den Rechnungsgrundlagen der Prämienkalkulation unter Zugrundelegung des Rückkaufswertes nach § 169
  Abs. 3 bis 5"* and **must be stated in the contract for each insurance year**. Abs. 3: it is computed for the end of the current
  insurance period taking premium arrears into account, and the surplus entitlements are unaffected.
  **§ 166 *Kündigung des Versicherers*:** Abs. 1 — where the **insurer** terminates, *"wandelt sich mit der Kündigung die Versicherung
  in eine prämienfreie Versicherung um"*, and § 165 applies to the conversion. Abs. 2 — in the § 38 Abs. 2 premium-default case [R30]
  the insurer owes the benefit it would have owed had the contract converted at the date of the claim. Abs. 3 requires the § 38 Abs. 1
  reminder to point out the coming conversion; Abs. 4 adds an employer-arranged-cover limb with a **two-month** minimum period and a
  § 212 continuation notice. **German lapse is therefore a three-way decrement** — surrender, *Beitragsfreistellung*, and
  premium-default conversion — the last two keeping the policy in force with a reduced benefit and a continuing expense loading.
  A delib model implementing only surrender says so and states what the paid-up path would do; one implementing *Beitragsfreistellung*
  anchors the paid-up sum to the **same § 169 Abs. 3 bis 5 value** the surrender path uses, or the two will not reconcile.
  **§ 167** lets the policyholder demand conversion into an insurance meeting **§ 851c Abs. 1 ZPO** [R40], *"die Kosten der Umwandlung
  hat der Versicherungsnehmer zu tragen"*.
  **§ 168 *Kündigung des Versicherungsnehmers*:** Abs. 1 — where *laufende Prämien* are payable the policyholder may terminate at any
  time for the end of the current insurance period. **Abs. 2, verbatim, because it bears directly on SOF:** *"Bei einer Versicherung,
  die Versicherungsschutz für ein Risiko bietet, bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist, steht das
  Kündigungsrecht dem Versicherungsnehmer auch dann zu, wenn die Prämie in einer einmaligen Zahlung besteht."* **Abs. 3 — the
  carve-out that defines the German pension products:** Abs. 1 and 2 do **not** apply to a retirement-provision contract where
  **(1)** the parties have excluded realisation of the claims under § 10 Abs. 1 Nr. 2 Satz 1 Buchst. b EStG in a *Basisrentenvertrag*
  certified under **§ 5a AltZertG** [R39] [R43], or **(2)** so far as they have irrevocably excluded realisation and that exclusion is
  necessary to obtain the *Pfändungsschutz* of **§ 851c or § 851d ZPO** [R40]. **Model consequence, the sharpest product distinction
  in delib: BAS has no surrender value and no lapse-to-surrender decrement.** **And a finding this pass records rather than acts on:**
  the earlier version of this entry said the market answer for a single-premium immediate annuity in payment is that no termination
  right exists but that no source confirmed it. **The statute now read says the opposite on its face** — § 168 Abs. 2 grants the
  right for a single-premium contract covering a risk whose occurrence is certain, and § 168 Abs. 3 carves out only certified
  *Basisrenten* and irrevocably-restricted *Pfändungsschutz* contracts. A *Sofortrente* sold as an ordinary Schicht-3 annuity falls in
  neither carve-out. This is flagged, not fixed: **no delib model is changed in this pass**, and SOF's specification is reported as
  resting on a market convention the statute does not obviously support.
  **§ 169 *Rückkaufswert*, and the whole section is now read.** **Abs. 1** — payable where a contract covering a certain risk is
  ended by the policyholder's termination or by the insurer's *Rücktritt* or *Anfechtung*. **Abs. 2** — payable only so far as it does
  not exceed the benefit that would be due on a claim at the date of termination, the excess being applied to a paid-up insurance; on
  *Rücktritt* or *Anfechtung* the full amount is payable. **Abs. 3 is the base measure and the five-year floor, quoted exactly — the
  version this page previously carried was a summary's paraphrase and got three words wrong:** *"Der Rückkaufswert ist das nach
  anerkannten Regeln der Versicherungsmathematik mit den Rechnungsgrundlagen der Prämienkalkulation zum Schluss der laufenden
  Versicherungsperiode berechnete Deckungskapital der Versicherung, bei einer Kündigung des Versicherungsverhältnisses jedoch
  mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf
  die ersten fünf Vertragsjahre ergibt; die aufsichtsrechtlichen Regelungen über Höchstzillmersätze bleiben unberührt."* [R16] — **a
  floor on the value, not a cap on the charge.** **Abs. 3 Satz 2 is the disclosure duty**, whose location this page could not
  previously fix: the *Rückkaufswert* and the extent to which it is guaranteed must be communicated **before the policyholder makes
  the contract declaration**, the detail being left to the VVG-InfoV [R31]. **Abs. 4 is narrower than this page said:** the *Zeitwert*
  measure applies **to *fondsgebundene Versicherungen* and other contracts providing benefits of the § 124 Abs. 2 Satz 2 VAG kind**
  [R7] *"soweit nicht der Versicherer eine bestimmte Leistung garantiert; im Übrigen gilt Absatz 3"*, and the calculation principles
  must be stated in the contract — so the trigger is **the product class, not the absence of a fixed guarantee**, and FRV and IDX are
  the products it reaches. **Abs. 5 — the *Stornoabzug*:** *"Der Versicherer ist zu einem Abzug von dem nach Absatz 3 oder 4
  berechneten Betrag nur berechtigt, wenn er vereinbart, beziffert und angemessen ist. Die Vereinbarung eines Abzugs für noch nicht
  getilgte Abschluss- und Vertriebskosten ist unwirksam."* **The burden of proof on the insurer is *not* in the statute** and is
  removed from this entry as a statutory claim — it is case law [R36] and is `[unverified]` here. **Abs. 6 is new to this page and is
  a second statutory haircut:** the insurer may reduce the Abs. 3 amount *"angemessen ... soweit dies erforderlich ist, um eine
  Gefährdung der Belange der Versicherungsnehmer, insbesondere durch eine Gefährdung der dauernden Erfüllbarkeit ..., auszuschließen"*,
  and *"Die Herabsetzung ist jeweils auf ein Jahr befristet."* — a one-year, renewable reduction distinct from the Abs. 5 deduction and
  from the § 314 VAG power [R12]. **Abs. 7 is the surplus limb every "Rückkaufswert einschließlich der Überschussanteile"
  cross-reference points at:** in addition to the Abs. 3–6 amount the insurer must pay the profit shares already allocated, so far as
  not already included, **and** the *Schlussüberschussanteil* provided for in the AVB for the case of termination, § 153 Abs. 3 Satz 2
  remaining unaffected. A delib model carrying an acquisition charge implements the **five-year floor as a `max()` against the tariff
  surrender value** and is tested on points that surrender where the floor binds and where it does not.
  **Resolved in this pass:** the Absatz numbering for the base measure (Abs. 3), the disclosure duty (Abs. 3 Satz 2) and the *Zeitwert*
  trigger (Abs. 4); § 166's Absatz structure; the existence of the Abs. 6 reduction power and the Abs. 7 surplus add-on; and the
  § 168 Abs. 2 single-premium question, answered against the market convention. **Still unverified:** whether a paid-up conversion may
  carry an *Abzug* of its own separate from Abs. 5 — § 165 Abs. 2 routes the calculation through § 169 Abs. 3 bis 5, which suggests it
  may, but no authority was read; **no market range for *Stornoabzug* levels and none for the *vereinbarte Mindestversicherungs­
  leistung* was retrieved**, so every such percentage and threshold is `[std]` apart from the one figure the BGH Debeka decision puts
  in the record [R36].

(delib-reg-r29)=

### R29. VVG §§ 172–177 — Kapitel 6, Berufsunfähigkeitsversicherung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__172.html (human-facing; the per-section page is a 4.3 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; §§ 172, 173, 174, 175, 176 and 177 read in full — the whole chapter — read 2026-08-30)
- **Used for:** the statutory BU definition, the *Nachprüfung* notice period, and the reach of Kapitel 6 into other products.
- **Annotation:** **§ 172 Abs. 1** — the insurer must render the agreed benefits *"für eine nach Beginn der Versicherung eingetretene
  Berufsunfähigkeit"*. **§ 172 Abs. 2 — the statutory definition, quoted in full:** *"Berufsunfähig ist, wer seinen zuletzt
  ausgeübten Beruf, so wie er ohne gesundheitliche Beeinträchtigung ausgestaltet war, infolge Krankheit, Körperverletzung oder mehr
  als altersentsprechendem Kräfteverfall ganz oder teilweise voraussichtlich auf Dauer nicht mehr ausüben kann."* Four elements matter
  for a model: the reference occupation is **the last occupation as it was structured before the impairment**; the causes are illness,
  bodily injury or more-than-age-appropriate decline of strength; the incapacity may be **whole or partial**; and the standard is
  ***voraussichtlich auf Dauer***. **§ 172 Abs. 3** permits the additional condition *"dass die versicherte Person auch keine andere
  Tätigkeit ausübt oder ausüben kann, die zu übernehmen sie auf Grund ihrer Ausbildung und Fähigkeiten in der Lage ist und die ihrer
  bisherigen Lebensstellung entspricht"* — the statutory basis of the ***abstrakte Verweisung*** [R37]. **§ 173 *Anerkenntnis*:** the
  insurer must state in *Textform* whether it acknowledges its obligation, and Abs. 2: *"Das Anerkenntnis darf nur einmal zeitlich
  begrenzt werden. Es ist bis zum Ablauf der Frist bindend."* **§ 174 *Leistungsfreiheit*:** where the conditions of liability have
  ceased, the insurer is released only if it has set the change out to the policyholder in *Textform* (Abs. 1), and *"frühestens mit
  dem Ablauf des dritten Monats nach Zugang der Erklärung"* (Abs. 2) — the *Nachprüfung* mechanism. **§ 175** makes §§ 173 and 174
  semi-mandatory. **§ 176:** *"Die §§ 150 bis 170 sind auf die Berufsunfähigkeitsversicherung entsprechend anzuwenden, soweit die
  Besonderheiten dieser Versicherung nicht entgegenstehen."* **§ 177 *Ähnliche Versicherungsverträge*, and the wording matters for
  PFL:** Abs. 1 applies §§ 173 bis 176 *"auf alle Versicherungsverträge, bei denen der Versicherer für eine dauerhafte
  Beeinträchtigung der Arbeitsfähigkeit eine Leistung verspricht"*, and Abs. 2 excludes accident insurance and health-insurance
  contracts covering the impairment-of-working-capacity risk. **A *Pflegerentenversicherung* pays on *Pflegebedürftigkeit*, not on an
  impairment of *Arbeitsfähigkeit*, so whether § 177 Abs. 1 reaches it at all is a live question the statutory text does not resolve
  in the product's favour** — which is why delib treats the PFL claims-process rules as AVB conventions rather than statutory ones
  [R51]. **Model consequences for BU:** the **three-month notice** is a real monthly cash-flow item — a reactivation recognised in
  month *t* still pays through *t+3*; the **once-only time-limited acknowledgement** is why a claims-in-payment model needs a distinct
  "acknowledged" state; and § 176 is the authority for giving a BU model a *Rückkaufswert*, a *Beitragsfreistellung* and an
  *Überschussbeteiligung* at all. **Still unverified:** nothing in this entry.

(delib-reg-r30)=

### R30. VVG §§ 19, 21, 37, 38, 157 and 158 — Anzeigepflicht, Zahlungsverzug, Altersangabe, Gefahränderung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__19.html (human-facing; the per-section page is a 5.8 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; §§ 19, 21, 37, 38, 157 and 158 read in full, read 2026-08-30)
- **Used for:** the contestability window a select period stands in for, and the fact that German lapse is not instantaneous.
- **Annotation:** **§ 19 *Anzeigepflicht*, and the Absatz structure is now confirmed rather than assumed.** Abs. 1: the policyholder
  must disclose, up to the making of his contract declaration, the risk circumstances known to him which are material and *"nach denen
  der Versicherer in Textform gefragt hat"*, and also answer such questions asked between his declaration and acceptance. Abs. 2: on
  breach the insurer may **rescind**. Abs. 3: rescission is **excluded** where the breach was *"weder vorsätzlich noch grob
  fahrlässig"*, in which case the insurer may terminate on **one month's** notice. Abs. 4: rescission for gross negligence and the
  Abs. 3 termination right are both excluded where the insurer would have concluded anyway, if on other terms, which then become part
  of the contract retroactively. Abs. 5: all of these rights require a **separate Textform warning** about the consequences, and are
  excluded where the insurer knew. **Abs. 6 carries a number worth having:** where a contract change under Abs. 4 raises the premium
  *"um mehr als 10 Prozent"* or excludes cover for the undisclosed circumstance, the policyholder may terminate **without notice
  within one month** of the insurer's notification. **§ 21 carries the exercise rules and the periods, and the section attribution
  this page previously marked `[unverified]` is confirmed.** Abs. 1: the insurer must assert its § 19 Abs. 2 bis 4 rights **in writing
  within one month** of learning of the breach. Abs. 2: on rescission after a claim the insurer is not liable **unless** the breach
  concerned a circumstance causal neither for the claim nor for the extent of the obligation — *"Hat der Versicherungsnehmer die
  Anzeigepflicht arglistig verletzt, ist der Versicherer nicht zur Leistung verpflichtet."*, which is where the *arglistig* rule
  actually lives, not in § 19. **Abs. 3, verbatim:** *"Die Rechte des Versicherers nach § 19 Abs. 2 bis 4 erlöschen nach Ablauf von
  fünf Jahren nach Vertragsschluss; dies gilt nicht für Versicherungsfälle, die vor Ablauf dieser Frist eingetreten sind. Hat der
  Versicherungsnehmer die Anzeigepflicht vorsätzlich oder arglistig verletzt, beläuft sich die Frist auf zehn Jahre."* — so **both
  periods run from *Vertragsschluss***, which answers the question this page left open, and claims occurring inside the window stay
  contestable afterwards. **§ 157 *Unrichtige Altersangabe*, in full:** *"Ist das Alter der versicherten Person unrichtig angegeben
  worden, verändert sich die Leistung des Versicherers nach dem Verhältnis, in welchem die dem wirklichen Alter entsprechende Prämie
  zu der vereinbarten Prämie steht."*, with rescission available only where the insurer would not have concluded at the correct age.
  **§ 158 *Gefahränderung*:** Abs. 1 — *"Als Erhöhung der Gefahr gilt nur eine solche Änderung der Gefahrumstände, die nach
  ausdrücklicher Vereinbarung als Gefahrerhöhung angesehen werden soll; die Vereinbarung bedarf der Textform."*; Abs. 2 — a risk
  increase can no longer be relied on **five years** after it occurred, **ten** where § 23 was breached intentionally or fraudulently;
  Abs. 3 — the § 41 premium-reduction right likewise requires an express *Gefahrminderung* agreement. **§ 37** — Abs. 1 gives the
  insurer a right of *Rücktritt* while the first premium is unpaid; Abs. 2 releases it from a claim arising while the first premium is
  unpaid, but only where the policyholder is responsible **and** the insurer gave a separate Textform notice or a conspicuous notice
  in the *Versicherungsschein*. **§ 38** — Abs. 1: for a *Folgeprämie* the insurer may set a payment period at the policyholder's cost
  in *Textform*, *"die mindestens zwei Wochen betragen muss"*, effective only if it itemises the arrears of premium, interest and
  costs and states the Abs. 2 and 3 consequences. Abs. 2: no liability for a claim after expiry while the policyholder is in default.
  **Abs. 3 answers the question this page left open: yes, the insurer may terminate without notice after expiry**, may combine the
  termination with the period so that it takes effect on expiry, and the termination becomes ineffective if the policyholder pays
  within one month. **But § 166 overrides the general § 38 consequence for life insurance**: cover does not simply cease, the contract
  converts to *prämienfrei* [R28]. **Model consequences:** § 157's pro-rata benefit adjustment is a clean, implementable rule and a
  natural test for RLV and KLV; § 158's default — **no risk-increase consequence unless expressly agreed** — is why German life and BU
  contracts carry no general occupation-change clause and why a delib BU model needs no mid-term reunderwriting state; and **German
  lapse is not instantaneous**: due date → qualified reminder with a two-week period → expiry → conversion to paid-up, so a monthly
  model applying a lapse decrement in the month of the missed premium is off by at least one month and applies the wrong benefit
  basis. The **five-year contestability window of § 21 Abs. 3** is a real first-duration mortality and morbidity effect a model may
  fold into a select period, provided it says so. **Resolved in this pass:** the § 19 Absatz numbering, the location of the *arglistig*
  rule (§ 21 Abs. 2 Satz 2), the § 38 Abs. 3 termination right, and the start date of the ten-year period. **Still unverified:**
  **§ 23 VVG (*Gefahrerhöhung*)**, cross-referenced by § 158 Abs. 2, and **§ 33 VVG (*Fälligkeit*)**, cross-referenced by § 152 Abs. 5,
  were not opened; and no retrieved document addresses market practice on grace periods beyond the statutory two weeks.

---

## 6. Conduct, disclosure and distribution---

## 6. Conduct, disclosure and distribution

(delib-reg-r31)=

### R31. VVG §§ 1a, 6, 7, 7b, 7c and 214, with the VVG-InfoV — advice, information, cost disclosure and Effektivkosten

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__6.html (human-facing; the per-section page is a 5.8 kB frameset shell) and
  https://www.gesetze-im-internet.de/vvg-infov/BJNR300400007.html. Text read from the canonical XML of both.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (VVG canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, §§ 1a, 6, 7, 7b, 7c and 214 read in full; VVG-InfoV canonical XML, Stand: zuletzt
  geändert durch Art. 13 G v. 26.5.2026 I Nr. 156, §§ 2 and 4 read in full; read 2026-08-30)
- **Used for:** the German cost-disclosure regime that makes a *Produktinformationsblatt* a usable `[S#]` charge source, and the
  Effektivkosten figure delib validates against.
- **Annotation:** **§ 6 *Beratung des Versicherungsnehmers*** — Abs. 1: the insurer must question and advise so far as the difficulty
  of assessing the cover or the policyholder's own situation gives occasion, *"auch unter Berücksichtigung eines angemessenen
  Verhältnisses zwischen Beratungsaufwand und der vom Versicherungsnehmer zu zahlenden Prämien"*, must state the reasons for each
  recommendation, and must document it. Abs. 4 extends the duty into the running contract; Abs. 5 makes breach a damages claim; and
  **Abs. 6 is a limit this page did not carry: §§ 6 Abs. 1–5 do not apply at all where the contract is arranged by a
  *Versicherungsmakler*** — the broker's own duties take over. **§ 7 *Information des Versicherungsnehmers*** — Abs. 1: the contract
  terms including the AVB and the VVG-InfoV information must be communicated *"rechtzeitig vor Abgabe von dessen Vertragserklärung
  ... in Textform"*, clearly and comprehensibly; Abs. 2 is the empowerment for the VVG-InfoV and names, for life insurance,
  information on the expected benefits, their determination and calculation, the *Modellrechnung*, the acquisition and administration
  costs offset against premiums, and other costs. **§ 1a *Vertriebstätigkeit des Versicherers*, Abs. 1 Satz 1, now quoted in full:**
  *"Der Versicherer muss bei seiner Vertriebstätigkeit gegenüber Versicherungsnehmern stets ehrlich, redlich und professionell in
  deren bestmöglichem Interesse handeln."*, with Abs. 1 Satz 2 defining *Vertriebstätigkeit* to include advice, contract preparation,
  conclusion and participation in administration and performance, and Abs. 3 requiring all distribution information including
  advertising to be *"redlich und eindeutig"* and not misleading. **OLG Stuttgart is reported to have rejected the argument that this
  obliges an insurer to adapt or redesign its own products** — the limit that keeps § 1a a conduct standard rather than a
  product-design mandate, and the counterweight to Merkblatt 01/2023 [R35]; **that decision was not retrieved and remains
  `[unverified]`.** **§ 7b** requires, for *Versicherungsanlageprodukte* within the meaning of Art. 2(1)(17) IDD, appropriate
  information on the distribution and on *"sämtliche Kosten und Gebühren rechtzeitig vor Abschluss des Vertrags"*, aggregated, with
  the total cost and its cumulative effect on the investment return made comprehensible, an itemisation on request, and a repeat at
  least annually during the term. **§ 7c** requires the insurer to ask about knowledge and experience, financial circumstances
  including loss-bearing capacity, and investment objectives including risk tolerance, and to recommend only products *"die für diesen
  geeignet sind"*.
  **§ 214 corrects a claim this page previously made.** § 214 does **not** recognise the *Versicherungsombudsmann e.V.*; it empowers
  the **Bundesamt für Justiz** to recognise privately organised bodies as *Schlichtungsstelle* for consumer insurance disputes and for
  intermediary disputes, on the conditions of § 24 VSBG, and requires recognised bodies to answer every complaint and to inform BaFin
  of business practices that may materially harm many consumers. The *Versicherungsombudsmann* is recognised **under** § 214, not
  **by** it, and the "since August 2016" date is `[unverified]` — no recognition instrument was retrieved.
  **The VVG-InfoV settles three things for delib, all now read.** **(a) Cost disclosure, § 2 Abs. 1 Nr. 1:** the costs included in
  the premium must be disclosed — *"die einkalkulierten Abschlusskosten als einheitlicher Gesamtbetrag und die übrigen einkalkulierten
  Kosten als Anteil der Jahresprämie unter Angabe der jeweiligen Laufzeit"*, with the *Verwaltungskosten* shown **additionally and
  separately** on the same basis; § 2 Abs. 1 Nr. 2 adds other and occasion-driven costs, Nr. 4 the *Rückkaufswerte* and Nr. 5 the
  paid-up minimum and benefits, and **§ 2 Abs. 2 requires the Nr. 1, 2, 4 and 5 figures in euro**. **This is why a German
  *Produktinformationsblatt* can be read as a source of actual charge levels in a way a French *encadré* cannot**: the *encadré*
  discloses maxima, the German PIB the amounts in the premium. **(b) The three Modellrechnung rates, § 2 Abs. 3** [R25].
  **(c) Effektivkosten, § 2 Abs. 1 Nr. 9:** for life contracts *"die Versicherungsschutz für ein Risiko bieten, bei dem der Eintritt
  der Verpflichtung des Versicherers gewiss ist"*, the insurer must disclose *"die Minderung der Wertentwicklung durch Kosten in
  Prozentpunkten (Effektivkosten) bis zum Beginn der Auszahlungsphase"*. **§ 2 Abs. 6 gives the method and two limits this page did
  not have.** The Effektivkosten are computed *"wie der Gesamtkostenindikator nach Anhang VI der Delegierten Verordnung (EU) 2017/653"*
  [R32] on the offered contract's own parameters, except that the pre-cost annual return of that Annex is always used and that the
  Annex's biometric-risk cost component is carried over **only where the underlying product guarantees at least a 90 per cent
  participation in *Risikoüberschüsse***. And **Satz 4 excludes the whole method from *Altersvorsorgeverträge* and
  *Basisrentenverträge* under §§ 1 and 2 AltZertG** — so RIE and BAS are governed by the AltvPIBV's own individual Effektivkosten
  instead [R43], and the two figures are not interchangeable. **(d) § 4** requires the *Informationsblatt zu Versicherungsprodukten*
  to follow **Durchführungsverordnung (EU) 2017/1469**, adds a euro cost block for products outside Annex I of Directive 2009/138/EG,
  and **§ 4 Abs. 3 disapplies it for PRIIPs *Versicherungsanlageprodukte* and for PEPP** — the IPID and the PRIIPs KID are
  alternatives, not cumulative. **§ 2 Abs. 4** applies the whole cost regime to *Berufsunfähigkeitsversicherung* and adds the warning
  that the AVB's BU concept differs from the social-law and *Krankentagegeld* concepts [R29] [R37].
  **For delib the Effektivkosten figure is a validation target for a product's charge parameterisation, not an input** — reproducing
  it exactly needs the PRIIPs Annex VI algorithm and a specified holding period, neither of which delib implements.
  **Resolved in this pass:** every VVG-InfoV citation above, the § 214 mischaracterisation, the § 6 Abs. 6 broker exception and the
  AltZertG carve-out from the Effektivkosten method. **Still unverified:** the OLG Stuttgart decision, the *Versicherungsombudsmann*
  recognition date, and the claim that the Effektivkosten duty was introduced by the LVRG with effect from January 2015 [R20].

(delib-reg-r32)=

### R32. PRIIPs — Verordnung (EU) Nr. 1286/2014 and the delegated technical standards

- **Publisher:** European Parliament and Council; European Commission for the RTS
- **URL:** https://eur-lex.europa.eu/eli/reg/2014/1286/oj/deu/pdfa1b (Level 1),
  https://eur-lex.europa.eu/eli/reg_del/2017/653/oj/deu/pdfa1b (the RTS) and
  https://eur-lex.europa.eu/eli/reg_del/2021/2268/oj/deu/pdfa1b (the 2021 amendment)
- **Accessed:** 2026-08-30
- **Retrieved:** yes (three PDFs, 23 pp. / 52 pp. / 57 pp., German Official Journal texts, read 2026-08-30)
- **Used for:** the KID content elements a German *fondsgebundene* or *indexgebundene* contract must publish, and the Annex VI method
  the German *Effektivkosten* figure is aligned with.
- **Annotation:** **Verordnung (EU) Nr. 1286/2014 des Europäischen Parlaments und des Rates vom 26. November 2014 über
  Basisinformationsblätter für verpackte Anlageprodukte für Kleinanleger und Versicherungsanlageprodukte (PRIIP)**, ABl. L 352 vom
  9.12.2014, introduced a standardised ***Basisinformationsblatt* (KID)** for packaged retail investment products **and
  *Versicherungsanlageprodukte***, which pulls a German *fondsgebundene Rentenversicherung* with a fund menu into scope.
  **Art. 8(3)(d) is the risk-and-return section, read from the regulation:** it requires (i) *"einen Gesamtrisikoindikator, ergänzt
  durch eine erläuternde Beschreibung dieses Indikators und seiner Hauptbeschränkungen"*; (ii) **the possible maximum loss of invested
  capital**, including whether the retail investor can lose all of it, whether further liabilities can arise, and whether a capital
  protection applies and from when; (iii) *"geeignete Performanceszenarien und die ihnen zugrunde liegenden Annahmen"*; (iv) any
  built-in performance caps; and (v) a statement that the investor's national tax law affects the actual payout.
  **The 1–7 scale is now established from the RTS.** Delegated Regulation **(EU) 2017/653 of 8 March 2017**, ABl. L 100 vom 12.4.2017,
  Art. 3(2)(a) requires *"Höhe des mit dem PRIIP verbundenen Risikos in Form einer Risikoklasse unter Anwendung eines
  Gesamtrisikoindikators mit einer numerischen Skala von 1 bis 7"*, and its Annex III supplies the wording — *"Wir haben dieses Produkt
  auf einer Skala von 1 bis 7 in die Risikoklasse [1/2/3/4/5/6/7] eingestuft, wobei [1 der niedrigsten/ ... /7 der höchsten]
  Risikoklasse entspricht."*
  **The four performance scenarios are likewise now established, and their German names are not the ones this page used.** Annex IV as
  replaced by Delegated Regulation **(EU) 2021/2268**, ABl. L 455 I vom 20.12.2021, applicable from **1 January 2023**, Nr. 1: *"a)
  optimistisches Szenario; b) mittleres Szenario; c) pessimistisches Szenario; d) Stressszenario."* — **mittleres**, not "moderates".
  Nr. 2 defines the stress scenario as showing significant adverse effects not captured by the pessimistic one, and **Nr. 3 adds a
  fifth element specific to insurance: *"Ein zusätzliches Szenario für Versicherungsanlageprodukte beruht auf dem ... mittleren
  Szenario, sofern die Wertentwicklung in Bezug auf die Rendite der Anlage relevant ist."*** Nr. 4 requires the minimum investment
  return to be shown, disregarding issuer default. **The *Gesamtkostenindikator* of Annex VI**, presented in the "Kosten im
  Zeitverlauf" table as a reduction in yield, is the method German third-layer *Effektivkosten* are aligned with by § 2 Abs. 6
  VVG-InfoV [R31] — which is why an FRV or IDX charge parameterisation can be validated against a published *Effektivkosten* figure
  but not reproduced without the Annex VI algorithm.
  **Resolved in this pass:** the SRI 1–7 scale, the four scenario names and the insurance-specific fifth scenario, all previously
  `[unverified]`. **Still unverified:** the recommended-holding-period rule, the cost tables at 1 year / half the RHP / RHP, and the
  biometric-risk premium treatment inside Annex VI — the Annexes were located but not read line by line, and no delib document states
  a figure from them.

(delib-reg-r33)=

### R33. IDD — Richtlinie (EU) 2016/97, the transposition act of 20 July 2017 and § 34d GewO

- **Publisher:** European Parliament and Council for the directive; Bundesamt für Justiz for the GewO
- **URL:** https://eur-lex.europa.eu/eli/dir/2016/97/oj/deu/pdfa1b for the directive;
  https://www.gesetze-im-internet.de/gewo/__34d.html for § 34d GewO (text read from the canonical XML);
  https://kanzlei-michaelis.de/umsetzung-der-eu-vermittlerrichtlinie-2016-97-idd-in-deutsches-recht/ for the transposition account
- **Accessed:** 2026-08-30
- **Retrieved:** the **directive** yes as a document (PDF, 41 pp., German Official Journal text, read 2026-08-30) — **its title,
  date and structure were read; its conduct articles were not read line by line**; **§ 34d GewO** yes (canonical XML, Stand: zuletzt
  geändert durch Art. 1 G v. 20.7.2026 I Nr. 215, read 2026-08-30); the transposition account yes (HTML, 155 kB)
- **Used for:** the licensing conditions behind German acquisition cost, and the *Sondervergütungsverbot* that makes commission
  non-rebatable.
- **Annotation:** ***Richtlinie (EU) 2016/97 des Europäischen Parlaments und des Rates vom 20. Januar 2016 über Versicherungsvertrieb
  (Neufassung)*** — the date is now read from the instrument. It was transposed by the act of **20 July 2017**, reported as in force
  **23 February 2018** with exceptions, Member States being free to apply the directive from **1 October 2018**; those German dates are
  from the secondary account and remain `[unverified]`. The useful part is the architecture: the transposition spreads the directive
  across **three statutes** — **GewO** (licensing and conduct of intermediaries, § 34d), **VAG** (distribution, remuneration and the
  *Provisionsabgabeverbot*), and **VVG** (information duties and product assessment, via §§ 1a, 6a, 7a, 7b, 7c and 7d, [R31]).
  **§ 34d GewO, now read.** Abs. 1: a *Versicherungsvermittler* — *Versicherungsvertreter* or *Versicherungsmakler* — needs a licence
  from the competent *Industrie- und Handelskammer*, and the licence must say which of the two it is. **Abs. 5 gives the four
  conditions, and they are refusal grounds rather than positive requirements:** the licence must be refused where the applicant lacks
  ***Zuverlässigkeit*** (Nr. 1), lives *"in ungeordneten Vermögensverhältnissen"* (Nr. 2), cannot show a
  ***Berufshaftpflichtversicherung*** or equivalent guarantee (Nr. 3), or has not passed the IHK examination proving the
  ***Sachkunde*** (Nr. 4). **The commission point this page makes is now a statutory citation rather than an inference:** § 34d Abs. 1
  Satz 6 provides that *"Einem Versicherungsvermittler ist es untersagt, Versicherungsnehmern, versicherten Personen oder
  Bezugsberechtigten aus einem Versicherungsvertrag Sondervergütungen zu gewähren oder zu versprechen."* — **so a German product's
  acquisition cost is structurally a commission to a § 34d intermediary that the customer cannot be rebated**, which is why the
  *Abschlusskosten* disclosure [R31] and the Zillmerung case law [R36] are as prominent as they are. Abs. 2 separates the
  *Versicherungsberater*, who may be paid only by the client and must pass on any insurer inducement under § 48c VAG; Abs. 3 forbids
  holding both licences. For delib this is background with **no cash-flow consequence** beyond the commission point above.
  **Still unverified:** the **15 hours of continuing education per calendar year** — § 34d Abs. 9 Satz 2 GewO imposes a
  *Weiterbildungspflicht* and § 34e GewO empowers a regulation to set its scope, but the hours are fixed by the
  *Versicherungsvermittlungsverordnung*, which this pass did not retrieve; and the directive's article numbering, the **IPID**
  requirement, the demands-and-needs test, the suitability and appropriateness tests for IBIPs and the remuneration and conflicts
  provisions, **which were not read** even though the instrument was opened — exactly the gap frlib records for the DDA at its R32.

(delib-reg-r34)=

### R34. Unisex — EuGH C-236/09 (Test-Achats), and §§ 19, 20 and 33 AGG

- **Publisher:** Court of Justice of the European Union, via the NWB case database; Bundesamt für Justiz for the AGG
- **URL:** https://datenbank.nwb.de/Dokument/Anzeigen/443611/ for the judgment;
  https://www.gesetze-im-internet.de/agg/__19.html for the AGG (human-facing; that per-section page is a 5.8 kB frameset shell,
  so the text was read from the canonical XML)
- **Accessed:** 2026-08-30
- **Retrieved:** yes — the **judgment** as reproduced by NWB (HTML, 64 kB, read 2026-08-30) and the **AGG** (canonical XML,
  Stand: zuletzt geändert durch Art. 15 G v. 22.12.2023 I Nr. 414; §§ 19, 20 and 33 read in full, read 2026-08-30)
- **Used for:** the rule that no delib model may price on sex, and the rule that it may price on age.
- **Annotation:** The ECJ held on **1 March 2011** in **C-236/09** that maintaining sex-differentiated tariffs indefinitely, and the
  derogation permitting it, is incompatible with equality between men and women under **Articles 21 and 23 of the Charter of
  Fundamental Rights**, and that **Art. 5 Abs. 2 der Richtlinie 2004/113/EG des Rates vom 13. Dezember 2004** is *"ab dem 21.12.2012
  ungültig"*. **The Gender Directive's number, previously not established, is 2004/113/EG** — read here from the judgment's own
  recitation. From that date sex may no longer lead to different premiums or benefits for **new** contracts; insurers must offer
  ***Unisex-Tarife***.
  **On the German side, all three AGG sections are now read.** **§ 19 Abs. 1 Nr. 2** carries the civil-law non-discrimination
  prohibition and **expressly names private insurance** — a *Benachteiligung* on grounds of race or ethnic origin, sex, religion,
  disability, age or sexual identity is impermissible in the formation, performance and termination of civil obligations *"die ... eine
  privatrechtliche Versicherung zum Gegenstand haben"*. **§ 20 Abs. 1** permits differential treatment on religion, disability, age,
  sexual identity or sex where there is a *sachlicher Grund*. **§ 20 Abs. 2 Satz 1 is now the pregnancy rule, which confirms that the
  old first sentence was repealed:** *"Kosten im Zusammenhang mit Schwangerschaft und Mutterschaft dürfen auf keinen Fall zu
  unterschiedlichen Prämien oder Leistungen führen."* — the provision that once allowed sex-differentiated pricing on actuarial data is
  simply gone from the consolidated text. **§ 20 Abs. 2 Satz 2 is load-bearing for delib and this page did not carry it:**
  differential treatment on **religion, disability, age or sexual identity** in private insurance *"ist ... nur zulässig, wenn diese
  auf anerkannten Prinzipien risikoadäquater Kalkulation beruht, insbesondere auf einer versicherungsmathematisch ermittelten
  Risikobewertung unter Heranziehung statistischer Erhebungen"* — **that is the statutory permission for age-rated tariffs**, and it is
  why every delib product prices on age and none prices on sex. **§ 33 Abs. 5** preserves sex-differentiated treatment for insurance
  relationships *"die vor dem 21. Dezember 2012 begründet werden"*, but only where sex *"bei einer auf relevanten und genauen
  versicherungsmathematischen und statistischen Daten beruhenden Risikobewertung ein bestimmender Faktor ist"*, and repeats the
  maternity rule. **On the question of later changes to pre-2012 contracts** the statute gives a structural signal rather than an
  answer: §§ 33 Abs. 2, 3 and 4 each carry an express sentence disapplying the transitional to *"spätere Änderungen von
  Dauerschuldverhältnissen"*, and **Abs. 5 does not** — but no authority on that reading was retrieved, so the point stays
  `[unverified]`.
  **Model consequence, and it is a hard one: every delib model prices unisex.** An RLV, BU or PFL model point may carry a `sex`
  attribute for **decrement** purposes — the underlying DAV tables are sex-specific [R47] — but **must not** let sex enter the
  premium. The standard market resolution is a **portfolio sex-mix assumption** applied to the best-estimate decrements; that mix is a
  modeller's assumption and is `[std]`. Letting a sex field leak into pricing reproduces a tariff unlawful in Germany since 2012 and is
  a numbered pitfall. **A second statutory unisex rule, for the subsidised products:** § 1 Abs. 1 Nr. 2 AltZertG requires a certified
  *Altersvorsorgevertrag* to provide *"eine lebenslange und unabhängig vom Geschlecht berechnete Altersversorgung"* [R43] — so Riester
  has been unisex by product law, not only by discrimination law. **Resolved in this pass:** the Gender Directive's number, the
  substance of the § 20 Abs. 2 repeal, the § 33 Abs. 5 wording, and the age-pricing permission. **Still unverified:** the amending
  instrument and date for the § 20 Abs. 2 Satz 1 repeal, **reported two ways** — a Bundestag/Bundesrat AGG amendment in late February
  2013, or the *SEPA-Begleitgesetz* published 3 April 2013 with retroactive effect from 21 December 2012 — the consolidated text shows
  only the result and both readings are recorded rather than one chosen; and **no market sex-mix figure was retrieved**, so every
  blend weight in delib is `[std]` [R47].

(delib-reg-r35)=

### R35. BaFin Merkblatt 01/2023 (VA) — Wohlverhaltensaufsicht and angemessener Kundennutzen

- **Publisher:** Bundesanstalt für Finanzdienstleistungsaufsicht
- **URL:** https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html
- **Accessed:** 2026-08-30
- **Retrieved:** yes (HTML, 162 kB, the full *Merkblatt* text with its marginal numbers, read 2026-08-30). BaFin's FAQ on the
  *Merkblatt* (HTML, 85 kB) and its *Kundennutzen im Fokus* article (HTML, 88 kB) were also opened.
- **Used for:** the German Value-for-Money regime, and the fact that it polices the *level* of charges rather than only their
  disclosure.
- **Annotation:** *Merkblatt 01/2023 (VA) zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden Lebensversicherungsprodukten*
  sets out what BaFin expects so that such products offer an ***angemessener Kundennutzen*** and distribution conflicts of interest are
  avoided. **The scope question this page previously left open is answered in the document's own footnote 2:** *"Als kapitalbildende
  Lebensversicherungsprodukte werden hier (klassische und fondsgebundene) Lebensversicherungsprodukte mit Sparkomponente bezeichnet.
  Darunter fallen Versicherungsanlageprodukte sowie weitere Lebensversicherungsprodukte mit Sparkomponente (insbesondere ...
  Direktversicherungen sowie Altersvorsorgeverträge ...)"*, and the body repeatedly addresses *"die fondsgebundene Lebensversicherung
  (einschließlich statische und dynamische Hybride)"* separately. **So the Merkblatt reaches KLV, RV, FRV and the hybrid shapes IDX
  belongs to, and reaches Riester and Basisrente as well.**
  **Two supervisory tests, both quantitative in kind if not in level.** **Return, Rn. 15:** insurers must formulate *Renditeziele*
  consistent with their target market's expectations, and *"sollten ... auch prüfen, ob die Angehörigen des Zielmarktes nicht nur eine
  positive Rendite nach Kosten, sondern auch eine positive Rendite nach Kosten und Inflation anstreben"* — a *"realer Anlageerfolg"*,
  for long-term contracts benchmarkable against the ECB's medium-term inflation target. **Note the modality: the real-return test is a
  *sollten*, not a *müssen*** — this page previously stated it as a requirement. What *is* mandatory is the probability test:
  *"Ein angemessener Kundennutzen setzt voraus, dass das formulierte Renditeziel mit hinreichender Wahrscheinlichkeit erreicht wird.
  Dies ist im Rahmen der Produktprüfung mit geeigneten stochastischen Analysen zu prüfen."* And where the target market is defined by
  the value of a guarantee, formulating a return target may be dispensable altogether. **Cost:** the Merkblatt names the
  ***Effektivkosten***, computed on the method of § 2 Abs. 6 VVG-InfoV [R31], as *"eine geeignete Größe zur Messung der insgesamt
  anfallenden Kosten eines kapitalbildenden Lebensversicherungsproduktes"*, and reasons that the risk of an inadequate or negative
  return rises with cost, cost being the variable the producer controls where the return is largely exogenous.
  **For delib this is the German *Value for Money* regime and it matters twice:** a KLV, RV, FRV or IDX charge parameterisation should
  be **plausible against a sector Effektivkosten distribution** rather than merely internally consistent, because the supervisor now
  polices the level; and it explains why the German market moved to lower guarantees and lower acquisition costs after 2023 — context
  a product specification's market-role section needs. **Resolved in this pass:** the scope question, the exact modality of the two
  tests, and the requirement of a stochastic check. **Still unverified:** **no Effektivkosten threshold, sector benchmark or numerical
  test appears anywhere in the Merkblatt** — the document is deliberately non-numeric, which is itself the finding; and the reported
  consultation date of 31 October 2022, the May 2023 publication, and BaFin's reported outcomes (products withdrawn, cost reductions in
  existing portfolios, retroactive compensation) are not stated in the *Merkblatt* text and remain `[unverified]` here.

---

## 7. The case law---

## 7. The case law and the market's model conditions

(delib-reg-r36)=

### R36. The BGH line of authority on German life contracts

- **Publisher:** Bundesgerichtshof (press releases and case captions)
- **URL:** https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2018/2018107.html
- **Accessed:** 2026-08-30
- **Retrieved:** **one of the six lines.** The **BGH press release on IV ZR 201/17** was opened in full (HTML, 36 kB, read
  2026-08-30) and line (3) below now rests on it. **The other five lines were not retrieved**: no judgment text and no press release
  for them was opened in this pass, and the `juris` document server refused with HTTP 403. They are kept as known references with
  their captions, and every statement about them is `[unverified]`.
- **Used for:** the vintage-dependent surrender-value floors, and the constitutional standing of the *Sicherungsbedarf* test.
- **Annotation:** Six lines of authority**(1) Zillmerung and the
  Mindestrückkaufswert.** **BGH 12 October 2005 — IV ZR 162/03**: clauses setting off *Abschlusskosten* against the first premiums are
  an *unangemessene Benachteiligung* and **invalid**. **BGH 25 July 2012 — IV ZR 201/10**: the same, plus clauses failing to
  distinguish the *Rückkaufswert* under § 176 Abs. 3 VVG a.F. from the *Stornoabzug* under Abs. 4 are ineffective under § 307 Abs. 1
  Satz 2 BGB. **BGH 11 September 2013 — IV ZR 17/13 and IV ZR 114/13**: for contracts concluded **up to the end of 2007**, *ergänzende
  Vertragsauslegung* gives a minimum that **may not fall below half of the ungezillmertes Deckungskapital**; **IV ZR 216/13** applies
  the floor, with reported worked figures of **15,694.12 € paid against 29,587.75 € of premiums**. **Why this matters although delib
  models new business:** the *hälftig* floor and the five-year-spread floor of § 169 Abs. 3 VVG [R28] are **different rules for
  different vintages**, so **delib must not silently apply § 169 Abs. 3 to a pre-2008 issue year**. **(2) The Widerrufsjoker.** Where
  the withdrawal instruction was defective the period never started; its home is **§ 5a VVG a.F.**, the *Policenmodell*, in force 1
  January 1995 – 31 December 2007, held incompatible with Union law by the CJEU in **2013** and decided fundamentally by the **BGH on
  7 May 2014, IV ZR 76/11**, bounded by **IV ZR 40/21** (15 March 2023) and **IV ZR 268/21**. A successful *Widerspruch* unwinds on
  **bereicherungsrechtlich** terms — premiums back plus *Nutzungen*, less risk cover consumed — **a different payout from either
  surrender or maturity; delib does not implement it**, and the notes say the pre-2008 book carries a legal option the model does not
  value. **(3) Bewertungsreserven — the one line retrieved, and it now carries a worked figure.** **BGH, Urteil vom 27. Juni 2018 —
  IV ZR 201/17**: the IV. Zivilsenat held *"dass die Neuregelung zur Beteiligung des Versicherungsnehmers an Bewertungsreserven
  (sog. stille Reserven) in der Lebensversicherung gemäß § 153 Absatz 3 Satz 3 des Versicherungsvertragsgesetzes (VVG) in der Fassung
  des Lebensversicherungsreformgesetzes vom 1. August 2014, in Kraft getreten am 7. August 2014, nicht verfassungswidrig ist"* —
  which **also settles the LVRG's entry-into-force date at 7 August 2014** [R20]. The reasoning: the new rule is more precise than its
  predecessor, is not an impermissible retroactivity, and sits inside a package that also raised the policyholders' share of the risk
  surplus and cut the *Höchstsatz für die bilanzielle Anrechnung von Abschlusskosten*, and that lets a balance-sheet profit reach
  shareholders only above the *Sicherungsbedarf*. **The facts quantify the effect, and no other retrieved source does:** a
  *kapitalbildende Lebensversicherung* running from 1 September 1999 to 1 September 2014 was pre-announced on 1 July 2014 at a
  maturity benefit of **50.274,17 €**, of which **2.821,35 €** was the *Bewertungsreserven* share; the final benefit notified on
  22 August 2014 was **47.601,77 €**, the insurer applying its *Sicherungsbedarf* so that only **148,95 €** of the
  *Bewertungsreserven* remained — a reduction of about 95 per cent of that component within seven weeks. **Note also** that the press
  release reproduces § 153 Abs. 3 Satz 3 as it stood for that case, cross-referring to §§ 53c, 54 Abs. 1 und 2, 56a Abs. 3 und 4 und
  81c Abs. 1 und 3 VAG a.F., where the provision now in force cross-refers to §§ 89, 124 Abs. 1, 139 Abs. 3 und 4, 140 und 214 VAG
  [R24] — the substance is the same and the section numbers moved with the 2016 VAG. And the BGH **quashed and remitted** because the
  appellate court had made no findings on whether the ordinary statutory conditions for the reduction were met, so the decision
  settles the constitutional question, not the case. **For delib:** the statutory half is conditional on a portfolio-level test the
  model does not perform and the highest court has confirmed the insurer may reduce it to near zero, so a KLV or RV model either
  excludes the component explicitly or carries it as a `**[std]**` scalar citing this decision. **(4) The Rentenfaktor.** **BGH 10 December 2025 — IV ZR
  34/25**: a clause in the AVB of a *fondsgebundene Rentenversicherung* letting the insurer **reduce the *Rentenfaktor* named in the
  Versicherungsschein** — the monthly annuity per **10,000 € of Vertragsguthaben** — **without a corresponding duty to restore it if
  circumstances improve** is **void** under **§ 308 Nr. 4 BGB** and **§ 307 Abs. 1 Satz 1 BGB**, the principles reportedly reaching
  all comparable clauses. **The single most model-relevant German decision of the last year:** the *garantierter Rentenfaktor* is a
  **hard guarantee** unless the AVB gives a **symmetric** adjustment right, so an FRV model annuitising at a fixed guaranteed factor
  implements the legally correct default rather than a simplification. **(5) The Stornoabzug.** **BGH 18 March 2026 — IV ZR 184/24**,
  overturning OLG Koblenz 2 UKl 1/23: a *kapitalmarktabhängiger Stornoabzug* does **not** infringe the *Bezifferung* requirement of §
  169 Abs. 5 Satz 1 VVG — the insurer may specify a ***Berechnungsverfahren*** rather than a concrete amount at conclusion. The
  clause: a deduction of **up to 15 % of the Deckungskapital**, depending on the **Null-Kupon-Euro-Zinsswapsatz with a ten-year term
  published by the Deutsche Bundesbank**, accepted as suitable to protect the insured community against *zinsinduzierte
  Stornierungen*. **The case was remitted on *Angemessenheit*, so that limb is open**; a delib model may implement a *Stornoabzug* of
  that shape citing this decision as the observed upper end while stating that the appropriateness of 15 % has not been decided. **(6)
  The Pflegestufe gap.** **BGH — IV ZR 126/23**, reported 30 April 2025: older AVB still refer to *Pflegestufen* and that is an
  **unintended Regelungslücke**; **Pflegegrad 2 may not automatically be equated with Pflegestufe I**, because the 2017 reform
  **materially widened** the definition of care need [R51].

(delib-reg-r37)=

### R37. GDV-Musterbedingungen and German Berufsunfähigkeit market practice

- **Publisher:** Gesamtverband der Deutschen Versicherer e.V.
- **URL:** https://www.gdv.de/gdv/service/musterbedingungen for the index and
  https://www.gdv.de/resource/blob/6348/5827a5492cca6aa1147852c30f10247b/allgemeine-bedingungen-fuer-die-kapitalbildende-lebensversicherung-0-pdf-data.pdf
  for the endowment model conditions
- **Accessed:** 2026-08-30
- **Retrieved:** yes — the **index page** (HTML, 94 kB) and the ***Allgemeine Bedingungen für die kapitalbildende
  Lebensversicherung*** (PDF, 20 pp., **Stand: 21.07.2025**), read 2026-08-30. **The BU model conditions themselves were not
  opened**, only their titles from the index.
- **Used for:** the `[S#]` clause source class for KLV, RV, FRV, RLV and BAS, and the AVB conventions a BU model must state.
- **Annotation:** The GDV publishes ***unverbindliche Musterbedingungen*** and says so on the page itself: *"Bei den hier
  aufgeführten Versicherungsbedingungen handelt es sich um Musterbedingungen des Gesamtverbandes der Deutschen Versicherungswirtschaft
  (GDV). Diese Bedingungen sowie die Muster-Standmitteilungen für Lebensversicherungen sind für die Versicherungsunternehmen
  unverbindlich. Die Verwendung ist rein fakultativ. Abweichende Bedingungen und Musterstandmitteilungen können vereinbart werden."*
  **The life catalogue is now enumerated from the index rather than reported**, and it covers eight of the ten delib products
  directly: *Allgemeine Bedingungen für die kapitalbildende Lebensversicherung*; *für die Risikolebensversicherung*; *für die
  Rentenversicherung mit aufgeschobener Rentenzahlung*; *mit sofort beginnender Rentenzahlung*; *für die fondsgebundene
  Rentenversicherung*; *für die Rentenversicherung gemäß § 10 Absatz 1 Nr. 2 Buchstabe b Doppelbuchstabe aa EStG (Basisrente-Alter)*;
  three AltZertG (Riester) variants including a *fondsgebundene* one and one with immediate annuity; four BU sets —
  *Berufsunfähigkeitsversicherung*, *Berufsunfähigkeits-Zusatzversicherung*, a *Basisrente-Alter* BUZ and one with
  *Arbeitsunfähigkeit* cover; the *Hinterbliebenenrenten-Zusatzversicherung* forms; and — a source class this page did not previously
  record — **nine *Muster-Standmitteilungen***, one each for Riester classic and hybrid, Basisrente classic and with BUZ, unit-linked
  and classical annuity, endowment, and annuity with BUZ [R25]. **There is no model set for an *Indexpolice***, which is consistent
  with IDX having no statutory chapter of its own [R22].
  **The largest gap this page recorded is now closed: clause text has been retrieved.** From the endowment model conditions, edition
  **21.07.2025** — **§ 12 Abs. 3, the *Rückkaufswert* clause:** *"Der Rückkaufswert ist nach § 169 des Versicherungsvertragsgesetzes
  (VVG) das nach anerkannten Regeln der Versicherungsmathematik mit den Rechnungsgrundlagen der Beitragskalkulation zum Schluss der
  laufenden Versicherungsperiode berechnete Deckungskapital des Vertrages. Bei einem Vertrag mit laufender Beitragszahlung ist der
  Rückkaufswert mindestens jedoch der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss-
  und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt."* — **with a refinement the statute does not contain:** *"Ist die
  vereinbarte Beitragszahlungsdauer kürzer als fünf Jahre, verteilen wir diese Kosten auf die Beitragszahlungsdauer."*
  **§ 12 Abs. 4, the *Abzug* clause, and the answer to "what is the market level" is that the model conditions do not state one:**
  the text reads *"Von dem nach Absatz 3 ermittelten Wert nehmen wir einen Abzug in Höhe von ...¹² vor"*, and footnote 12 says
  ***"Unternehmensindividuell zu ergänzen."*** The justification offered is *"weil mit ihm die Veränderung der Risikolage des
  verbleibenden Versichertenbestandes ausgeglichen wird"* plus compensation for collectively provided risk capital, with the
  appropriateness *"im Zweifel von uns nachzuweisen"* — **which is where the burden-of-proof rule this page previously attributed to
  § 169 Abs. 5 VVG actually appears: in the model clause, not in the statute** [R28]. **§ 12 Abs. 5** carries the § 169 Abs. 6 VVG
  one-year reduction verbatim, and **§ 12 Abs. 6** the surplus add-on of § 169 Abs. 7. **§ 13 answers the other open question in
  [R28]: a paid-up conversion does carry its own separate *Abzug*** — the paid-up sum is computed *"unter Zugrundelegung des
  Rückkaufswertes nach § 12 Absatz 3"* and then reduced by arrears *"außerdem nehmen wir einen Abzug in Höhe von ...¹⁸ vor"*,
  again left blank for the insurer, on the same appropriateness test; and § 13 Abs. 3 warns in bold that in the early years only the
  five-year minimum is available. **§ 14 Abs. 2 states the charge mechanics in the insurer's own voice:** *"Wir wenden auf Ihren
  Vertrag das Verrechnungsverfahren nach § 4 der Deckungsrückstellungsverordnung an"*, the amount so amortised being *"nach der
  Deckungsrückstellungsverordnung auf 2,5 % der von Ihnen während der Laufzeit des Vertrages zu zahlenden Beiträge beschränkt"* [R16].
  **For delib the Musterbedingungen are the natural `[S#]` primary product source class** for a reference product — published, free,
  non-proprietary and the thing most insurers' AVB derive from — provided a product specification that follows them also says they are
  **non-binding** and that real AVB differ, **and that the numeric slots are blank in the model and therefore `[std]` in delib.**
  **BU market practice above the statutory floor** [R29]. Under an ***abstrakte Verweisung*** the insured does not necessarily receive
  benefits merely because they cannot perform their last occupation, provided they **could theoretically** perform another activity;
  under a ***konkrete Verweisung*** the insurer examines whether the insured **actually performs** another activity corresponding to
  their previous *Lebensstellung*. The reported market position — **almost all new contracts waive the abstrakte Verweisung** — and
  the reported practical test — unable to perform the last occupation **for at least six months** at **50 per cent or more** — are
  **AVB conventions, not statute, and remain `[unverified]`: the BU model conditions were not opened in this pass.**
  **Model consequences for BU, and these are the operative ones:** the benefit is a **binary step at 50 %**, not a proportional
  payment, so a model must decide whether it projects incidence of ≥50 % incapacity or a graded state; the **six-month qualification**
  is a deferred period in cash-flow terms, so a monthly BU model needs an explicit *Karenzzeit* parameter and the worked example must
  show whether the first payment is in month 7 and whether it is backdated; and with the abstrakte Verweisung waived, **reactivation is
  driven only by konkrete Verweisung or recovery**, which materially raises expected claim duration. **Resolved in this pass:** the
  non-binding status quoted from the source, the full life catalogue, the existence of the *Muster-Standmitteilungen*, and the
  *Rückkaufswert*, *Abzug*, *Beitragsfreistellung* and cost clauses for KLV. **Still unverified:** the BU clause text, including the
  *Verweisung* wording and the six-month/50 % thresholds; the earlier "MB BUV 22 / MB BUZ 22, dated 15 November 2022" naming, which
  **does not appear on the GDV index page** — the page dates its life section 13.09.2022 and the endowment set 21.07.2025, so the
  short names and the November date are dropped as unverified; and **whether the six months operates as a retroactive fiction or as a
  waiting period**, so the choice is currently `**[std]**`.

---

## 8. Tax and the three-layer---

## 8. Tax and the three-layer state-subsidised pension architecture

**This section was the weakest in the library and is now the most changed.** It was written with **zero successful searches**; the
statutes it depends on have now been read in full from the canonical XML, and the tables it reconstructed from general knowledge have
been replaced by the statutory tables themselves. The instruments read for this section, each once, with the `Stand` that applies to
every entry below unless an entry says otherwise:

| Instrument | Stand |
|---|---|
| **EStG** | Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197 |
| **EStDV 1955** | Stand: zuletzt geändert durch Art. 2 V v. 19.12.2025 I Nr. 372 |
| **ZPO** | Stand: zuletzt geändert Art. 2 G v. 22.12.2025 I Nr. 349 |
| **AltZertG** | Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294, with Art. 5–7 G v. 26.5.2026 I Nr. 156 recorded as *textlich nachgewiesen, dokumentarisch noch nicht abschließend bearbeitet* |
| **ErbStG** | Stand: zuletzt geändert durch Art. 10 G v. 22.6.2026 I Nr. 192 |
| **SGB V** | Stand: zuletzt geändert durch Art. 1 G v. 26.6.2026 I Nr. 195 |

**What remains unverified is now specific, not blanket:** the *names and dates of amending acts* (the consolidated text shows the
result, not the instrument), the *administrative* material (BMF-Schreiben, the BZSt commentary, the PIA determinations), and the
*market* facts. Each entry says which. **delib computes no tax anywhere**: all benefit cash flows are gross of *Kapitalertragsteuer*,
*Solidaritätszuschlag* and *Kirchensteuer*.

(delib-reg-r38)=

### R38. AltEinkG — the Alterseinkünftegesetz and the Drei-Schichten-Modell

- **Publisher:** Deutscher Bundestag / Bundesrat for the act; Bundesamt für Justiz for the resulting EStG provisions
- **URL:** **not established for the act itself.** A BGBl citation commonly reported as *vom 5. Juli 2004, BGBl. I S. 1427* is
  `[unverified]` and is recorded as a lead, not a citation. The provisions it created were read at
  https://www.gesetze-im-internet.de/estg/__10.html and https://www.gesetze-im-internet.de/estg/__22.html
- **Accessed:** 2026-08-30
- **Retrieved:** **no for the act** — no BGBl text and no Bundestag drucksache for the AltEinkG was opened in this pass; **yes for
  the two transitions it created**, read from the EStG canonical XML (Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30) at [R39] and [R41]
- **Used for:** the layer classification that is the first attribute of every delib product.
- **Annotation:** With effect from **1 January 2005** the act replaced *vorgelagerte* taxation of pensions with a ***nachgelagerte***
  system — qualifying contributions deducted during accumulation, the pension taxed as income in payment — and introduced **two long
  linear transitions**. **One of them has ended, and this page said both were still running.** The **contribution-deduction
  transition** of § 10 Abs. 3 Sätze 4 und 6 EStG ran from 76 per cent in 2013, rising two percentage points a year, and
  *"ab dem Kalenderjahr 2023 beträgt er 100 Prozent"* — **it is complete** [R39]. The **taxation transition** of § 22 Nr. 1 Satz 3
  Buchst. a Doppelbuchst. aa EStG, keyed to the year the pension starts, is still running and reaches 100 per cent for the **2058**
  cohort [R41]. The ***Drei-Schichten-Modell*** sorts retirement products by *what the state buys with the relief it gives*:
  **Schicht 1 — Basisversorgung** (the statutory scheme, *Versorgungswerke* and the private **Basisrente**), contributions deductible
  under § 10 Abs. 1 Nr. 2 EStG, benefits taxed on a cohort *Besteuerungsanteil*, the price of admission being that the product must
  look like a state pension; **Schicht 2 — kapitalgedeckte, staatlich geförderte Zusatzversorgung** (**Riester** and the *betriebliche
  Altersversorgung*), relief granted as a **direct payment into the contract** (the *Zulage*, a real cash flow) or as a
  *Sonderausgabenabzug*; **Schicht 3 — private, ungeförderte Vorsorge** (KLV, RV, FRV, IDX, SOF), contributions not deductible as
  retirement provision at all, benefits lightly taxed under § 20 Abs. 1 Nr. 6 [R45] or on the *Ertragsanteil* [R41]. **For delib the
  layer is the first classifying attribute of every product**: it decides whether a state *Zulage* appears as an inflow, whether a
  surrender decrement is legally possible at all, and whether the payout documentation discusses a *Besteuerungsanteil* or an
  *Ertragsanteil*. **Corrected in this pass:** the claim that both transitions are still running. **Still unverified:** the act's
  date, BGBl citation and article structure; whether the act itself introduced the *Basisrente* label; and **every element of the
  constitutional origin** — the BVerfG judgment of 6 March 2002, 2 BvL 17/99, its docket number, date and deadline are general
  knowledge and no document was opened for them.

(delib-reg-r39)=

### R39. EStG § 10 Abs. 1 Nr. 2 Buchst. b and § 10 Abs. 3 — the Basisrente deduction, the ceiling and the five prohibitions

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://www.gesetze-im-internet.de/estg/__10.html (this per-section page does serve, 41 kB); text read from the canonical
  XML
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197; § 10 Abs. 1 Nr. 2 and § 10 Abs. 3 read in full, read 2026-08-30)
- **Used for:** the five prohibitions that define the BAS product shape, and the deduction ceiling that drives BAS premium behaviour.
- **Annotation:** **Buchst. a** covers the compulsory systems — statutory pension insurance, the *landwirtschaftliche Alterskasse* and
  *berufsständische Versorgungseinrichtungen* providing comparable benefits — which delib does not model but which **consume the same
  ceiling a Basisrente contribution competes for**, the single most important behavioural fact about Basisrente demand.
  **Buchst. b Doppelbuchst. aa creates the private product, and the words are now the statute's:** contributions *"zum Aufbau einer
  eigenen kapitalgedeckten Altersversorgung, wenn der Vertrag nur die Zahlung einer monatlichen, auf das Leben des Steuerpflichtigen
  bezogenen lebenslangen Leibrente nicht vor Vollendung des **62.** Lebensjahres oder zusätzlich die ergänzende Absicherung des
  Eintritts der Berufsunfähigkeit (Berufsunfähigkeitsrente), der verminderten Erwerbsfähigkeit (Erwerbsminderungsrente) oder von
  Hinterbliebenen (Hinterbliebenenrente) vorsieht"*; *Hinterbliebene* are the spouse and the children for whom the taxpayer has a
  *Kindergeld* or § 32 Abs. 6 entitlement, and a *Waisenrente* may run only while the § 32 conditions hold.
  **Buchst. b Doppelbuchst. bb is a second product shape this page did not carry**, and it matters for BU: a stand-alone contract
  insuring *Berufsunfähigkeit* or *verminderte Erwerbsfähigkeit* qualifies where it provides **only** a monthly lifelong annuity on
  the taxpayer's life *"für einen Versicherungsfall, der bis zur Vollendung des 67. Lebensjahres eingetreten ist"*; benefit cessation
  on a medically justified recovery may be agreed; and the annuity level may depend on the age at the insured event once the taxpayer
  has completed age 55.
  **The five prohibitions, now a verbatim statutory quotation rather than a summary's reproduction:** *"Die Ansprüche nach Buchstabe b
  dürfen nicht vererblich, nicht übertragbar, nicht beleihbar, nicht veräußerbar und nicht kapitalisierbar sein."* **Each prohibition
  is a model instruction:** *nicht kapitalisierbar* removes the lump-sum option and any partial commutation; *nicht veräußerbar*
  removes the surrender value and the lapse-to-cash decrement; *nicht übertragbar* removes assignment; *nicht beleihbar* removes the
  policy loan; and *nicht vererblich* means that **on death before annuitisation the fund does not pass to the estate** — a Basisrente
  **without** a *Hinterbliebenenabsicherung* rider produces **no benefit at all** on pre-retirement death, which is why insurers sell
  the rider almost universally and why a delib BAS model must either carry it or say loudly that the base run assumes no death
  benefit. **Two qualifications on *nicht kapitalisierbar* that this page did not have**, from the two following sentences:
  *"Anbieter und Steuerpflichtiger können vereinbaren, dass bis zu zwölf Monatsleistungen in einer Auszahlung zusammengefasst werden
  oder eine Kleinbetragsrente im Sinne von § 93 Absatz 3 Satz 2 oder 4 abgefunden wird"* [R42], and for the *Kleinbetragsrente* test
  **all of the taxpayer's contracts at one provider are aggregated**, separately per Doppelbuchstabe. A final sentence closes the
  shape: *"Neben den genannten Auszahlungsformen darf kein weiterer Anspruch auf Auszahlungen bestehen."*
  **The ceiling, § 10 Abs. 3, is not a fixed euro amount and the statute's phrasing is tighter than this page's:**
  *"Vorsorgeaufwendungen nach Absatz 1 Nummer 2 sind bis zu dem Höchstbeitrag zur knappschaftlichen Rentenversicherung, aufgerundet
  auf einen vollen Betrag in Euro, zu berücksichtigen. Bei zusammenveranlagten Ehegatten verdoppelt sich der Höchstbetrag."*
  **And the deductible percentage transition is over:** Satz 4 sets 76 per cent for 2013 and Satz 6 raises it by two points a year
  *"bis zum Kalenderjahr 2022; ab dem Kalenderjahr 2023 beträgt er 100 Prozent"* — so the earlier description of a reform "reported as
  effective 1 January 2015" is replaced by the statutory path, and **[R38] is corrected accordingly**. **For delib the deduction is
  not a cash flow of the contract** and no model computes it; it belongs in `product-spec.md` as the economic driver of premium
  behaviour, in particular the **year-end single-premium *Zuzahlung*** sized to the remaining headroom — so a BAS model that offers
  only a level regular premium models the wrong product. **Resolved in this pass:** the five prohibitions as a statutory quotation,
  the age 62, the ceiling formula and the end of the deduction transition. **Still unverified:** the **age 60 for contracts concluded
  before 1 January 2012** — that transitional is not in the consolidated § 10 text and its § 52 home was not read; and the euro value
  of the *Höchstbeitrag zur knappschaftlichen Rentenversicherung* for any year, which comes from the annual
  *Sozialversicherungsrechengrößen-Verordnung* [R46] and was not retrieved, so any euro ceiling in a delib document is `[std]` with
  the year stated.

(delib-reg-r40)=

### R40. ZPO §§ 850b, 851c and 851d — Pfändungsschutz and the shape it imposes on a Basisrente

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/zpo/__850b.html (human-facing; the per-section page is a 5.3 kB frameset shell).
  Text read from the canonical XML.
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert Art. 2 G v. 22.12.2025 I Nr. 349; §§ 850b, 851c and 851d read in full,
  read 2026-08-30)
- **Used for:** the four conditions that, with § 10 EStG and § 168 Abs. 3 VVG, fully specify BAS behaviour.
- **Annotation:** **§ 851c Abs. 1 — the four conditions, verbatim.** Claims to benefits granted under contracts *"dürfen nur wie
  Arbeitseinkommen gepfändet werden, wenn 1. die Leistung in regelmäßigen Zeitabständen lebenslang und nicht vor Vollendung des
  60. Lebensjahres oder nur bei Eintritt der Berufsunfähigkeit gewährt wird, 2. über die Ansprüche aus dem Vertrag nicht verfügt werden
  darf, 3. die Bestimmung von Dritten mit Ausnahme von Hinterbliebenen als Berechtigte ausgeschlossen ist und 4. die Zahlung einer
  Kapitalleistung, ausgenommen eine Zahlung für den Todesfall, nicht vereinbart wurde."*
  **§ 851c Abs. 2 — and the contested bands are now settled.** Amounts saved to build an appropriate retirement provision under such a
  contract are unattachable so far as they do not annually exceed **6 000 Euro for a debtor from 18 to the completed 27th year of
  life** and **7 000 Euro from 28 to the completed 67th year**, and so far as they do not exceed an aggregate of **340 000 Euro**.
  **So the 6,000/7,000 two-band ladder is current law and the 2,000–9,000 age-graded ladder is the superseded version** — the conflict
  this page recorded is resolved against the older reading. Two further rules the page did not carry: the amounts are re-set every
  fifth year on 1 July in the *Pfändungsfreigrenzenbekanntmachung*; and where the *Rückkaufwert* exceeds the unattachable amount,
  **three tenths of the excess** are unattachable too, except for the part exceeding three times 340 000 Euro.
  **§ 850b Abs. 1 Nr. 1** makes *"Renten, die wegen einer Verletzung des Körpers oder der Gesundheit zu entrichten sind"*
  ***bedingt pfändbar*** — attachable only under Abs. 2, where execution against other movable property has failed or will fail and
  attachment is equitable. **The statute does not name private *Berufsunfähigkeitsversicherung***; that inclusion is case law and
  commentary and is `[unverified]` here. **§ 850b Abs. 1 Nr. 4 carries a figure worth having for RLV and Sterbegeld:** claims from
  life insurances *"die nur auf den Todesfall des Versicherungsnehmers abgeschlossen sind"* are conditionally attachable where the sum
  assured does not exceed **5 400 Euro**. **§ 851d**, new to this page, provides that monthly benefits from **tax-subsidised**
  retirement assets — a lifelong annuity or an AltZertG *Auszahlungsplan* — are attachable **like earnings from employment**, which is
  the Riester counterpart of § 851c.
  **Model consequence: BAS is defined by these conditions, not merely protected by them.** The four requirements of § 851c Abs. 1 are
  the same four features § 10 Abs. 1 Nr. 2 Buchst. b EStG demands [R39] and that § 168 Abs. 3 VVG makes non-terminable [R28].
  Together — **three instruments, all now read** — they mean a BAS model has **no surrender, no capital option except a death benefit,
  no third-party beneficiary except survivors, annuity commencement not before 60 in ZPO terms and not before 62 in tax terms, and no
  assignment**. That is a complete behavioural specification, and it is why BAS is the one delib product with **no lapse-to-cash
  decrement at all**. For BU, § 850b means a BU annuity in payment is conditionally attachable, which does not change the cash flow —
  and the notes should say so rather than leave the reader wondering. **Resolved in this pass:** the § 851c Abs. 2 bands.
  **Still unverified:** the inclusion of private BU annuities in § 850b Abs. 1 Nr. 1, which rests on authority not retrieved here.

(delib-reg-r41)=

### R41. EStG § 22 Nr. 1 Satz 3 Buchst. a and § 55 EStDV — Besteuerungsanteil, Rentenfreibetrag and Ertragsanteil

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://www.gesetze-im-internet.de/estg/__22.html and https://www.gesetze-im-internet.de/estdv_1955/__55.html (both
  per-section pages serve); text read from the canonical XML of both
- **Accessed:** 2026-08-30
- **Retrieved:** yes (EStG canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, § 22 Nr. 1 Satz 3 Buchst. a read in full **including both statutory tables**; EStDV
  canonical XML, Stand: zuletzt geändert durch Art. 2 V v. 19.12.2025 I Nr. 372, § 55 read in full **including its table**; read
  2026-08-30)
- **Used for:** the cohort taxation of a Basisrente in payment and the *Ertragsanteil* of a Schicht-3 annuity — the asymmetry that is
  the economic case for SOF.
- **Annotation:** **This entry was previously a reconstruction with no corroboration at all. Both tables are now the statute's own.**
  **Doppelbuchst. aa — the Schicht-1 rule.** It applies to benefits from the statutory scheme, the *landwirtschaftliche Alterskasse*,
  the *berufsständische Versorgungseinrichtungen* **and *"Rentenversicherungen im Sinne des § 10 Absatz 1 Nummer 2 Buchstabe b"*** —
  i.e. one table for the state pension, a *Versorgungswerk* pension and a private Basisrente alike [R39]. **(1) The
  *Besteuerungsanteil* is fixed by the year the pension starts:** *"Der der Besteuerung unterliegende Anteil ist nach dem Jahr des
  Rentenbeginns und dem in diesem Jahr maßgebenden Prozentsatz aus der nachstehenden Tabelle zu entnehmen"*, the base being the
  *Jahresbetrag der Rente*. The statutory table, read in full: **bis 2005 → 50,0 %**, then 52,0 (2006), 54,0, 56,0, 58,0, 60,0 (2010),
  62,0, 64,0, 66,0, 68,0, 70,0 (2015), 72,0, 74,0, 76,0, 78,0, **80,0 (2020)**, 81,0 (2021), 82,0 (2022), then **half-point steps** —
  82,5 (2023), 83,0, 83,5, **84,0 (2026)**, 84,5, 85,0, 85,5, 86,0 (2030) … rising to **100,0 for the 2058 cohort**. **The reported
  shape is confirmed exactly**, including the flattening to a 0.5-point step from the **2023** cohort and the 2058 endpoint; the
  attribution of that flattening to the *Wachstumschancengesetz* is not in the consolidated text and remains `[unverified]`.
  **(2) The untaxed remainder is frozen in euro, and the statute is more precise than "for life".** Satz 4: the difference between the
  annual amount and the taxable part is the *steuerfreier Teil der Rente*; Satz 5: *"Dieser gilt ab dem Jahr, das dem Jahr des
  Rentenbeginns folgt, für die gesamte Laufzeit des Rentenbezugs."* **But Satz 6 and 7 qualify it in a way this page did not carry:**
  on a **change** in the annual amount the tax-free part is adjusted *"in dem Verhältnis ... in dem der veränderte Jahresbetrag der
  Rente zum Jahresbetrag der Rente steht, der der Ermittlung des steuerfreien Teils der Rente zugrunde liegt"* — **but**
  *"Regelmäßige Anpassungen des Jahresbetrags der Rente führen nicht zu einer Neuberechnung und bleiben bei einer Neuberechnung außer
  Betracht."* So the claim that **every increase, including every increase in the *Überschussrente*, is fully taxable** holds for
  *regelmäßige Anpassungen* and only for those; whether a surplus-driven increase in a private Basisrente is a *regelmäßige Anpassung*
  is a question the text does not answer and is `[unverified]`. Satz 8 adds a successor-annuity rule and Satz 9 attributes the
  annuity for the month of death to the deceased.
  **Doppelbuchst. bb — the Schicht-3 *Ertragsanteil*, and its table too is now the statute's.** The *Ertrag des Rentenrechts* is
  *"für die gesamte Dauer des Rentenbezugs der Unterschiedsbetrag zwischen dem Jahresbetrag der Rente und dem Betrag, der sich bei
  gleichmäßiger Verteilung des Kapitalwerts der Rente auf ihre voraussichtliche Laufzeit ergibt"* — a present-value split, an
  actuarial artefact rather than a policy dial. The table is keyed to *"Bei Beginn der Rente **vollendetes Lebensjahr** des
  Rentenberechtigten"*, **which answers the question this page left open: it is the completed year of life at annuity commencement,
  not at the start of the calendar year.** The two anchors most often quoted are confirmed: **65 bis 66 → 18 %** and **60 bis 61 →
  22 %**; the table runs from 59 % at ages 0–1 down to 1 % from age 97, with the neighbouring rows 62 → 21, 63 → 20, 64 → 19, 67 → 17,
  68 → 16, 69–70 → 15. Unlike the *Rentenfreibetrag*, **it is the percentage that is frozen**, so surplus increases to a Schicht-3
  annuity are taxed at the same light rate. **That asymmetry is the whole economic case for SOF** [R38].
  **§ 55 EStDV** supplies the special cases § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb Satz 5 delegates: Abs. 1 for annuities
  beginning before 1 January 1955 and for annuities on another person's or on several lives (the eldest where the right ends on the
  first death, the youngest where it ends on the last), and **Abs. 2 for ***abgekürzte Leibrenten*** — *"Der Ertrag der Leibrenten,
  die auf eine bestimmte Zeit beschränkt sind (abgekürzte Leibrenten), ist nach der Lebenserwartung unter Berücksichtigung der
  zeitlichen Begrenzung zu ermitteln."* — with a table keyed to the **remaining term in years**, from 97 % at a three-year term down
  to 2 % at 59 years, subject to a third column that falls back to the § 22 age table where the annuitant had completed a stated age
  at commencement. **That is what a *Berufsunfähigkeitsrente* from a *selbständige* BU contract is**, while a BU annuity written
  inside a Basisrente falls into Schicht 1 instead — so **the same biometric benefit is taxed two different ways depending on the
  wrapper**. **Resolved in this pass:** both statutory tables in full, the *Rentenfreibetrag* mechanics and its two qualifications,
  and the *Ertragsanteil* age definition. **Still unverified:** the amending act behind the 2023 flattening; and whether a
  surplus-driven increase counts as a *regelmäßige Anpassung* under Satz 7.

(delib-reg-r42)=

### R42. EStG § 10a and Abschnitt XI (§§ 79–99) — the Riester subsidy machinery

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://www.gesetze-im-internet.de/estg/__10a.html (this per-section page serves, 17 kB); text read from the canonical XML
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197; §§ 10a, 79, 82, 83, 84, 85, 86 and 93 read in full, read 2026-08-30)
- **Used for:** the Zulage cash flows a RIE model carries, the *Mindesteigenbeitrag* that drives them, and the commutation threshold.
- **Annotation:** **This entry previously had no corroboration and every euro figure carried `[unverified]`. All of them are now read
  from the statute.** **§ 10a Abs. 1 Satz 1 — the deduction and the *Günstigerprüfung*:** those compulsorily insured in the domestic
  statutory pension scheme *"können Altersvorsorgebeiträge (§ 82) zuzüglich der dafür nach Abschnitt XI zustehenden Zulage jährlich bis
  zu **2 100 Euro** als Sonderausgaben abziehen"*, and the same applies to the listed *Beamte* and equivalent groups. The tax office
  computes both the tax saved and the *Zulagenanspruch* and grants the better. **This split is the single most important thing a RIE
  model author must understand: only the Zulage is a contract cash flow; the Günstigerprüfung top-up is a personal tax refund and never
  touches the policy.** **§ 82 Abs. 1** defines *geförderte Altersvorsorgebeiträge* as the contributions and repayment instalments
  *"die der Zulageberechtigte (§ 79) bis zum Beginn der Auszahlungsphase zugunsten eines auf seinen Namen lautenden Vertrags leistet,
  der nach § 5 des Altersvorsorgeverträge-Zertifizierungsgesetzes zertifiziert ist"* — **the contributions the saver pays, which is why
  the *Beitragsgarantie* question at [R43] turns on whether the *Zulagen* are within that definition.**
  **§ 79 — entitlement.** Those named in § 10a Abs. 1, and — *mittelbare Zulageberechtigung* — the other spouse where the couple are
  not permanently separated, both are resident in the EU/EEA, **a contract in the other spouse's own name exists**, the other spouse
  *"hat zugunsten des Altersvorsorgevertrags ... im jeweiligen Beitragsjahr mindestens **60 Euro** geleistet"*, and that contract's
  payout phase has not begun. **The self-employed not compulsorily insured are excluded** — precisely the population Basisrente serves,
  so **the two subsidised products are complements addressed to different people, not competitors**. The 60-euro floor produces a real
  contract type, **a 60 € annual premium receiving a 175 € Grundzulage**, whose omission would leave a RIE model point table missing an
  economically extreme part of the book.
  **§§ 83–85 — the Zulagen, all confirmed.** § 83: the *Altersvorsorgezulage* is the sum of a *Grundzulage* (§ 84) and a *Kinderzulage*
  (§ 85). **§ 84: *"Jeder Zulageberechtigte erhält eine Grundzulage; diese beträgt ab dem Beitragsjahr 2018 jährlich 175 Euro."***, and
  the *Berufseinsteiger-Bonus* is § 84 Satz 2, not a section of its own: for those who have **not completed age 25** at the start of
  the *Beitragsjahr* the *Grundzulage* rises *"um einmalig 200 Euro"*, granted for the first *Beitragsjahr* beginning after
  31 December 2007 for which a *Zulage* is claimed. **§ 85 Abs. 1:** *"Die Kinderzulage beträgt für jedes Kind, für das gegenüber dem
  Zulageberechtigten Kindergeld festgesetzt wird, jährlich **185 Euro**. Für ein nach dem 31. Dezember 2007 geborenes Kind erhöht sich
  die Kinderzulage nach Satz 1 auf **300 Euro**."* § 85 Abs. 2 allocates it **to the mother** for married opposite-sex parents, to the
  father on joint application.
  **§ 86 — the *Mindesteigenbeitrag*, and the formula is now the statute's.** Abs. 1 Satz 2: it is *"jährlich 4 Prozent der Summe der
  in dem dem Kalenderjahr vorangegangenen Kalenderjahr ... erzielten beitragspflichtigen Einnahmen"* and equivalent items,
  *"jedoch nicht mehr als der in § 10a Absatz 1 Satz 1 genannte Höchstbetrag, vermindert um die Zulage nach den §§ 84 und 85"* — i.e.
  `min(4 % × previous year's income, 2 100 €) − Zulagenanspruch`. Satz 4: *"Als Sockelbetrag sind ab dem Jahr 2005 jährlich 60 Euro zu
  leisten."*, and Satz 5 makes the *Sockelbetrag* the minimum where it exceeds the computed amount. **Satz 6 settles the trap this
  page identified, in seven words:** *"Die Kürzung der Zulage ermittelt sich nach dem Verhältnis der Altersvorsorgebeiträge zum
  Mindesteigenbeitrag."* — **proportional, not a cliff**, so a model treating it as all-or-nothing produces a discontinuity that does
  not exist. The **prior-year income base** and the **subtraction of the Zulage** are both in Satz 2. **The Zulage for year *t* is
  typically credited in *t+1***, so an annual-step model must state its choice in the processing order; that timing is administrative
  practice and remains `[unverified]`.
  **§§ 93–94 — *schädliche Verwendung*.** § 93 Abs. 1: paying out subsidised retirement capital otherwise than on the AltZertG's
  permitted terms triggers repayment of the *Zulagen* and of the separately assessed § 10a advantage (the *Rückzahlungsbetrag*).
  **This is the behavioural heart of a RIE model**: the contract is legally terminable, unlike BAS, but terminating costs the entire
  subsidy history, so **the RIE lapse assumption should be materially below the RV/FRV assumption with this rule stated as the
  reason**; a lapse produces a *Rückkaufswert* **net of the Rückzahlungsbetrag**, a different quantity from the § 169 VVG value; and
  **a paid-up election is not *schädlich***, so the natural RIE decrement is *ruhend stellen*, not surrender.
  **§ 93 Abs. 3 — the *Kleinbetragsrente*, and the contested threshold is now settled against the 1 per cent reading.**
  *"Auszahlungen zur Abfindung einer Kleinbetragsrente zu Beginn der Auszahlungsphase gelten nicht als schädliche Verwendung."*, and a
  *Kleinbetragsrente* is **(Nr. 1)** an annuity which, on a level annuitisation of the whole capital available at the start of the
  payout phase, gives a monthly amount not exceeding ***1,5 Prozent der monatlichen Bezugsgröße nach § 18 des Vierten Buches
  Sozialgesetzbuch***, or **(Nr. 2)**, from **1 January 2027**, a monthly amount from an AltZertG *Auszahlungsplan* on the same
  1.5 per cent test. **So 1.5 per cent is the rate in force now; the 2027 date attaches to the payout-plan variant, not to the rate.**
  Satz 3 aggregates all the saver's subsidised contracts at one provider for the test, and Satz 4 extends the rule to a
  *Versorgungsausgleich* after the payout phase begins. For a small contract the commutation branch is the **modal outcome**, so both
  RIE and BAS need a commutation test at annuitisation and a model point that trips it [R39].
  **Resolved in this pass:** the 2,100 €, 175 €, 200 €, 185 €, 300 € and 60 € figures, the § 86 formula and its proportional
  reduction, and the *Kleinbetragsrente* threshold. **Still unverified:** the euro value of the *monatliche Bezugsgröße* for any year
  — it comes from the annual *Sozialversicherungsrechengrößen-Verordnung*, which was not retrieved [R46], so the euro threshold in a
  delib document is `[std]` with the year stated; and the *t+1* crediting convention.

(delib-reg-r43)=

### R43. AltZertG, the BZSt, the AltvPIBV and the Produktinformationsstelle Altersvorsorge

- **Publisher:** Bundesministerium der Justiz for the AltZertG and the AltvPIBV
- **URL:** https://www.gesetze-im-internet.de/altzertg/BJNR132200001.html (human-facing); text read from the canonical XML
- **Accessed:** 2026-08-30
- **Retrieved:** yes for the statute (canonical XML, Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294, with the 26.5.2026 amendments recorded as *textlich nachgewiesen,
  dokumentarisch noch nicht abschließend bearbeitet* [R44]; §§ 1, 2, 2a and 5a read in full, read 2026-08-30). **The AltvPIBV was not
  read** beyond its section list, the **BMF *Muster*-PIB** was not opened, and **no PIA determination was opened**.
- **Used for:** the *Beitragsgarantie* floor, the payout shape and the enumerated cost structure a RIE or BAS model implements.
- **Annotation:** Riester and Basisrente are **certified product categories under a statute of their own**, and certification is a
  *product* approval, not a *tax* ruling: the AltZertG defines what an *Altersvorsorgevertrag* (**§ 1**) and a *Basisrentenvertrag*
  (**§ 2**) must contain, the **BZSt** issues the certificate, and §§ 10a and 79 ff. EStG then hang the subsidy on it.
  **A correction first: § 5a is not the definition of a *Basisrentenvertrag*.** It is one sentence and it is purely procedural —
  *"Die Zertifizierungsstelle erteilt die Zertifizierung nach § 2 Abs. 3, wenn ihr die nach diesem Gesetz erforderlichen Angaben und
  Unterlagen vorliegen sowie die Vertragsbedingungen des Basisrentenvertrags dem § 2 Absatz 1 oder Absatz 1a sowie dem § 2a
  entsprechen und der Anbieter den Anforderungen des § 2 Absatz 2 entspricht."* **The substantive definition is § 2**, and § 2 Abs. 1
  simply incorporates the tax test: a *Basisrentenvertrag* is an agreement in German *"die die Voraussetzungen des § 10 Absatz 1
  Nummer 2 Buchstabe b Doppelbuchstabe aa des Einkommensteuergesetzes erfüllt"* [R39]. **§ 2 Abs. 1a defines the Basisrente-Erwerbs­
  minderung** and adds conditions no delib entry previously carried: partial incapacity must be recognised where a doctor forecasts at
  least twelve months' inability to work six hours a day on the general labour market, full incapacity at three hours, with at least
  half the insured benefit on partial and the full benefit on full incapacity; benefits run from the calendar month in which the
  incapacity arose where the claim is made within 36 months, and otherwise from 36 months before the claim; premiums must be deferred
  interest-free while a claim is decided; and the provider must waive the § 19 Abs. 3 Satz 2 and § 19 Abs. 4 VVG rights [R30] where
  the disclosure duty was breached without fault.
  **§ 1 Abs. 1 fixes the Riester features that are model instructions, all now read.** **(a) *Beitragsgarantie* (§ 1 Abs. 1 Nr. 3):**
  the provider must promise *"dass zu Beginn der Auszahlungsphase zumindest die eingezahlten Altersvorsorgebeiträge für die
  Auszahlungsphase zur Verfügung stehen und für die Leistungserbringung genutzt werden"*, and where premium parts are used for
  *Erwerbsminderung*, *Dienstunfähigkeit* or *Hinterbliebenenabsicherung*, ***"sind bis zu 20 Prozent der Gesamtbeiträge in diesem
  Zusammenhang nicht zu berücksichtigen"*** — **the 20 % carve-out is confirmed from the statute.** This is a **100 % money-back
  guarantee at retirement**, and it is why a German Riester insurance contract is invested so conservatively and became hard to sell
  at a 0.25 % *Höchstzinssatz* [R15]. **(b) Earliest payout: age 62** — § 1 Abs. 1 Nr. 2 requires *"eine lebenslange und unabhängig
  vom Geschlecht berechnete Altersversorgung"* payable *"nicht vor Vollendung des 62. Lebensjahres"* or from the start of a statutory
  pension, the same boundary as [R39] and [R45], **and the unisex requirement is a product-law rule independent of the AGG** [R34].
  **(c) The payout shape (§ 1 Abs. 1 Nr. 4 Buchst. a):** a **lebenslange Leibrente**, or instalments under an *Auszahlungsplan*
  *"mit einer anschließenden Teilkapitalverrentung ab spätestens dem 85. Lebensjahr"*; *"die Leistungen müssen während der gesamten
  Auszahlungsphase gleich bleiben oder steigen"* — **a non-decreasing constraint a delib annuity model must respect**; up to twelve
  monthly instalments may be combined into one payment; a *Kleinbetragsrente* may be commuted under § 93 Abs. 3 EStG [R42], with the
  saver entitled to defer the start of the payout phase to 1 January of the following year within **four weeks** of being told that
  the payout will take that form; and *"bis zu 30 Prozent des zu Beginn der Auszahlungsphase zur Verfügung stehenden Kapitals kann an
  den Vertragspartner außerhalb der monatlichen Leistungen ausgezahlt werden"* — **the 30 % lump sum is confirmed.**
  **(d) Cost structure, § 2a**, whose heading is *Kostenstruktur* and which applies to **both** contract types: *"Ein
  Altersvorsorgevertrag oder ein Basisrentenvertrag darf ausschließlich die nachfolgend genannten Kostenarten vorsehen"* — annual or
  monthly euro amounts; a percentage of the accumulated capital; a percentage of the agreed *Bausparsumme* or loan; a percentage of
  contributions or repayments paid or agreed; a percentage of the *Wohnförderkonto*; and from the start of the payout phase a
  percentage of the benefit paid — plus three occasion-driven charges only, for termination with transfer or payout, for a § 92a EStG
  housing use, and for *Versorgungsausgleich* work. **So a certified product's charge structure is enumerated by statute and a RIE
  charge table can be built from published PIBs in a way a Schicht-3 charge table cannot.**
  **The AltvPIBV and the PIA.** Providers of Basisrente and Riester must use a **uniform, individual *Produktinformationsblatt***,
  delivered before the customer's declaration of intent, disclosing ***Effektivkosten*** computed **individually for each contract
  offer** — a stronger duty than the product-level VVG-InfoV figure, which § 2 Abs. 6 Satz 4 VVG-InfoV expressly disapplies to these
  contracts [R31] — and assigning the product to **one of five *Chancen-Risiko-Klassen***, determined **by the PIA on behalf of the
  BMF**. **This is a genuinely unusual feature of the German market with no counterpart in `uslib`, `uklib`, `jplib` or `frlib`: a
  public body assigns a risk class using a stochastic model the insurer does not control.** **delib does not implement the PIA
  simulation**; a RIE or BAS specification may **report** a published CRK and Effektivkosten as `[S#]` facts and must say that
  reproducing either requires the PIA's scenario set, which is neither public nor in scope. **The 1 January 2017 start date, the
  five-class scale and the CRK 1-to-5 ordering are `[unverified]`: the AltvPIBV text and the PIA determinations were not read.**
  **Resolved in this pass:** § 5a's actual content and the correction of the § 2 / § 5a attribution; the 20 % carve-out; the 30 % lump
  sum; the age 62 and the statutory unisex rule; the non-decreasing payout constraint; and the § 2a cost enumeration.
  **On the *Beitragsgarantie* and the *Zulagen*, the pass narrows the question without closing it.** § 1 Abs. 1 Nr. 3 guarantees
  *"die eingezahlten Altersvorsorgebeiträge"*, and **§ 82 Abs. 1 EStG defines *Altersvorsorgebeiträge* as contributions and repayments
  *"die der Zulageberechtigte ... leistet"*** [R42] — which on its face excludes the state *Zulagen*, since the state pays those. But
  the AltZertG does not itself cross-refer to § 82 EStG, and no authority resolving the point was retrieved. **It therefore remains
  the single most material unresolved ambiguity here for a delib model** — for a two-child model point it moves the guarantee floor by
  thousands of euro over thirty years — so RIE keeps it as a `[std]` choice and prints both readings, now with the statutory wording
  and the § 82 definition beside them. **Still unverified:** the act's date (reported 26 June 2001), the **1 July 2010** BaFin→BZSt
  transfer, the reported **1 January 2010** start of compulsory *Basisrente* certification, the **150 € *Wechselkosten* cap**, the
  50 % rule, the five-year spreading and the three-month notice, the **definitions of r\* and r_k and the CRK class boundaries**,
  whether the PIA *Allgemeinverfügung* of 2022 is the operative determination, and whether the BMF *Muster*-PIB of 14 March 2019 has
  been superseded.

(delib-reg-r44)=

### R44. The Altersvorsorge-Reformgesetz 2026 and the Altersvorsorgedepot

- **Publisher:** Deutsche Rentenversicherung Bund; Bundesministerium der Finanzen; Deutscher Bundestag
- **URL:** https://www.deutsche-rentenversicherung.de/DRV/DE/Ueber-uns-und-Presse/Presse/Meldungen/2026/260508-bundesrat-reform-private-altersvorsorge,
  with https://www.bundesfinanzministerium.de/Content/DE/FAQ/reform-der-privaten-altersvorsorge.html and
  https://dserver.bundestag.de/btd/21/040/2104088.pdf
- **Accessed:** 2026-08-30
- **Retrieved:** yes for the official explanatory material — the **DRV release** (HTML, 148 kB), the **BMF FAQ** (HTML, 313 kB), the
  **Bundesregierung Q&A** (HTML, 123 kB), the **Bundestag text archive** (HTML, 508 kB) and the **Bundestag drucksache** (PDF,
  1.25 MB), read 2026-08-30. **The Act's own text was not retrieved.**
- **Used for:** the fact that `riester_rente` is a closed-book model, and the shape of what replaces it.
- **Annotation:** **Riester is closed to new business, and the enactment contradiction this page recorded is now resolved.** The DRV
  states that *"Der Bundesrat hat am 8. Mai 2026 dem Gesetz zur Reform der steuerlich geförderten privaten Altersvorsorge
  (Altersvorsorge-Reformgesetz) zugestimmt"*, and **the consolidated statutes give the promulgation: the VVG's `Stand` records
  *"zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156"* and the AltZertG carries Art. 5, 6 and 7 of the same act** — so the
  Bundesrat consented on **8 May 2026** and the Act is the ***Gesetz vom 26. Mai 2026, BGBl. 2026 I Nr. 156***. The two dates were
  never in conflict; they are the consent and the promulgation. **From 2027 the Riester-Rente is replaced by a new subsidised model**,
  and the DRV sets out its shape: free choice between a lifelong annuity and an *Entnahmeplan*; certified products with an
  **80 per cent or a 100 per cent *Beitragsgarantie*** or a standard product; ***Altersvorsorgedepots* without guarantees and without
  a lifelong payout**, with a **20-year payout phase from age 65** ending at age 85; and eligibility extended for the first time to
  the **self-employed and to members of *berufsständische Versorgungswerke***. **The new subsidy formula, which is not the old one:**
  a *Grundzulage* of **50 cent per euro of own contribution up to a maximum of 360 Euro**, then **25 cent per euro on a further
  1 440 Euro**, so **up to 540 Euro a year**; a *Kinderzulage* of **1 Euro per euro of own contribution up to 300 Euro per child**;
  and a *Sonderausgabenabzug* of at most **1 800 Euro plus the Zulagenanspruch**. Against that, the legacy regime the delib model
  implements is 175 / 185 / 300 Euro on a 4 %-of-prior-year-income *Mindesteigenbeitrag* capped at 2 100 Euro [R42].
  **Grandfathering is explicit:** *"Bestehende Riester-Verträge laufen weiter! Es gibt einen Bestandsschutz für diese Verträge."*,
  with an optional switch into the new subsidy by declaration and no repayment of past subsidy; but a saver who takes out a new
  contract alongside an old one has the new rules applied to the old one automatically.
  **This changes what a delib `riester_rente` model *is***: a model of a product **closed to new business from 1 January 2027** with a
  very large in-force book whose contractual rights survive. That is worth building — a closed book is exactly what a liability cash
  flow model is for — but the `product-spec.md` must say it plainly rather than present the product as current, and it means the
  *Beitragsgarantie* of [R43] is a feature of the **legacy** contract. **Still unverified:** the Act's own text and article structure,
  and every date inside the transition beyond 1 January 2027 — all of the above is official explanatory material, not the instrument.

(delib-reg-r45)=

### R45. EStG § 20 Abs. 1 Nr. 6 — the Unterschiedsbetrag, the 12/62 rule and the Mindesttodesfallschutz

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://www.gesetze-im-internet.de/estg/__20.html (this per-section page serves, 33 kB); text read from the canonical XML,
  with § 52 Abs. 28 for the transitional dates
- **Accessed:** 2026-08-30
- **Retrieved:** yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197; § 20 Abs. 1 Nr. 6 read in full — nine Sätze — and the relevant § 52 Abs. 28 sentences,
  read 2026-08-30)
- **Used for:** the duration and age thresholds that shape every Schicht-3 lapse assumption in delib.
- **Annotation:** The tax rule that decides when a German endowment or unit-linked contract is cashed in. **The base, Satz 1:** the
  taxable amount is *"der Unterschiedsbetrag zwischen der Versicherungsleistung und der Summe der auf sie entrichteten Beiträge
  (Erträge) im Erlebensfall oder bei Rückkauf des Vertrags"*, for annuity contracts with a *Kapitalwahlrecht* so far as the lifelong
  annuity is not chosen and paid, and for *Kapitalversicherungen mit Sparanteil*, **where the contract was concluded after
  31 December 2004** — a gain measure taking no account of inflation. **Satz 4 extends Sätze 1 bis 3 to *fondsgebundene
  Lebensversicherungen* and to annuity contracts without a *Kapitalwahlrecht***, so FRV and IDX are inside the rule.
  **The half-income rule, Satz 2:** *"Wird die Versicherungsleistung nach Vollendung des 60. Lebensjahres des Steuerpflichtigen und
  nach Ablauf von zwölf Jahren seit dem Vertragsabschluss ausgezahlt, ist die Hälfte des Unterschiedsbetrags anzusetzen."* — and
  **§ 52 Abs. 28 Satz 7 supplies the tightening:** *"§ 20 Absatz 1 Nummer 6 Satz 2 ist für Vertragsabschlüsse nach dem 31. Dezember
  2011 mit der Maßgabe anzuwenden, dass die Versicherungsleistung nach Vollendung des 62. Lebensjahres des Steuerpflichtigen
  ausgezahlt wird."* **So the rule is 12/60 for 2005–2011 contracts and 12/62 from 2012, and the twelve years run from
  *Vertragsschluss*** — which answers the question this page left open. **The rate:** where the halving applies to a benefit accruing
  from 1 January 2009 the flat *Abgeltungsteuer* does not apply and **§ 32d Abs. 2 Nr. 2 EStG** puts the half amount into the personal
  marginal rate; **that cross-reference was not read in this pass and is `[unverified]`.**
  **The *Mindesttodesfallschutz*, Satz 6, and it is a two-limbed cumulative test — the "reported second condition" this page could not
  parse is limb (b).** Satz 2 does **not** apply if **(a)** in a *Kapitallebensversicherungsvertrag* with an agreed level ongoing
  premium *"die vereinbarte Leistung bei Eintritt des versicherten Risikos weniger als 50 Prozent der Summe der für die gesamte
  Vertragsdauer zu zahlenden Beiträge beträgt"* **and (b)** *"die vereinbarte Leistung bei Eintritt des versicherten Risikos das
  Deckungskapital oder den Zeitwert der Versicherung spätestens fünf Jahre nach Vertragsabschluss nicht um mindestens 10 Prozent des
  Deckungskapitals, des Zeitwerts oder der Summe der gezahlten Beiträge übersteigt"*, that 10 per cent being allowed to fall to zero
  in equal annual steps to the end of the term. **§ 52 Abs. 28 Satz 8 dates it:** Satz 6 in the version of the Act of 19 December 2008
  applies *"für alle Versicherungsverträge ..., die nach dem 31. März 2009 abgeschlossen werden"* — confirming the 1 April 2009
  boundary. Failing the test the earnings are taxed **in full**.
  **Two further sentences this page did not carry.** **Satz 5** treats a *vermögensverwaltender Versicherungsvertrag* — one with
  separately managed, contract-specific assets not confined to publicly distributed funds or index trackers, where the beneficial
  owner may direct sales and reinvestment — as transparent, attributing the insurer's income to him and disapplying Sätze 1 bis 4.
  **Satz 9 is a number for FRV:** *"Bei fondsgebundenen Lebensversicherungen sind 15 Prozent des Unterschiedsbetrages steuerfrei ...,
  soweit der Unterschiedsbetrag aus Investmenterträgen stammt"*.
  **What this does to a model:** it creates a **duration-12 and age-60/62 double threshold** that policyholders wait for, so a KLV,
  RV, FRV or IDX lapse assumption that is flat in duration has ignored the strongest single driver of German surrender behaviour —
  surrenders are suppressed approaching duration 12 and spike at it, and again at the age threshold. The effect is directly analogous
  to the eight-year threshold that drives French *assurance vie* behaviour, and **delib models it the same way frlib does — as a
  duration-dependent lapse shape with the threshold named and the level `[std]`**. The rule reaches RV, FRV and IDX too, because a
  deferred annuity whose *Kapitalwahlrecht* is exercised for cash is taxed here while the same contract annuitised is taxed on the
  *Ertragsanteil* [R41] — **the annuitise-or-commute election is therefore a tax election**, and a model treating it as a fixed
  take-up rate says that the rate stands in for a tax comparison it does not perform. And the 50 %-Regel is a **model-point design
  constraint**: **a model point that would fail the German tax test is not representative of a real sold contract.**
  **Resolved in this pass:** the twelve years running from *Vertragsschluss*, the 60→62 transitional and its date, the second limb of
  the *Mindesttodesfallschutz*, and the 1 April 2009 boundary. **Still unverified:** the § 32d Abs. 2 Nr. 2 interaction; and the
  **pre-2005 cohort's qualifying conditions**, which **are not asserted anywhere in delib** — what can be said is that for contracts
  concluded before 1 January 2005 the *rechnungsmäßige und außerrechnungsmäßige Zinsen* were entirely free of income tax on maturity,
  which is why an *Altvertrag* has an almost nil lapse rate and why a KLV document must say the reference model does not represent
  that cohort.

(delib-reg-r46)=

### R46. ErbStG and SGB V §§ 226, 229 and 240 — death benefits and contributions on an annuity in payment

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://www.gesetze-im-internet.de/erbstg_1974/__3.html (this per-section page serves, 8.5 kB) and
  https://www.gesetze-im-internet.de/sgb_5/ ; text read from the canonical XML of both
- **Accessed:** 2026-08-30
- **Retrieved:** yes (ErbStG canonical XML, Stand: zuletzt geändert durch Art. 10 G v. 22.6.2026 I Nr. 192, § 3 read in full;
  SGB V canonical XML, Stand: zuletzt geändert durch Art. 1 G v. 26.6.2026 I Nr. 195, §§ 226, 229 and 240 read in full; read
  2026-08-30)
- **Used for:** the classification of a German death benefit, and the social-insurance asymmetry between the product layers.
- **Annotation:** **Germany has no insurance-specific death-benefit tax regime, and the provision is now quoted.** Unlike France, where
  CGI arts. 990 I and 757 B carve life insurance out of ordinary succession, a German *Todesfallleistung* paid to a named beneficiary
  is simply an ***Erwerb von Todes wegen*** under **§ 3 Abs. 1 Nr. 4 ErbStG** — *"jeder Vermögensvorteil, der auf Grund eines vom
  Erblasser geschlossenen Vertrags bei dessen Tode von einem Dritten unmittelbar erworben wird"* — and falls into ordinary inheritance
  tax at the beneficiary's own *Steuerklasse* and *Freibetrag*. **Two structuring facts the German market actually uses**, and they
  change who a model's beneficiary is: the ***Über-Kreuz-Versicherung***, where *Versicherungsnehmer* and *versicherte Person* are
  different people — spouses each owning a policy on the other's life — so that death triggers a payment to a *surviving
  policyholder* rather than an acquisition from a deceased one and **no inheritance tax arises**, which is standard advice for couples
  buying RLV cover and means a real RLV book contains a large share of cross-owned policies; and the **gift limb**, under which
  granting an *unwiderrufliches Bezugsrecht* during life is a *Schenkung* under § 7 ErbStG at the time of the grant [R26].
  **Both of those are `[unverified]`: § 3 Abs. 1 Nr. 4 was read, § 7 was not, and neither structuring practice is stated in any
  retrieved instrument.**
  **Social insurance is the asymmetry that can reverse the tax argument, and the three SGB V sections are now read.**
  **§ 229 Abs. 1** defines ***Versorgungsbezüge*** as income *"soweit sie wegen einer Einschränkung der Erwerbsfähigkeit oder zur
  Alters- oder Hinterbliebenenversorgung erzielt werden"* in five closed classes: public-service pensions (Nr. 1), parliamentary
  pensions (Nr. 2), **pensions of the *Versorgungswerke* — *"Renten der Versicherungs- und Versorgungseinrichtungen, die für
  Angehörige bestimmter Berufe errichtet sind"* (Nr. 3)**, farmers' pensions (Nr. 4) and **betriebliche Altersversorgung including the
  public-sector supplementary schemes (Nr. 5)**, from which *"Leistungen aus Altersvorsorgevermögen im Sinne des § 92 des
  Einkommensteuergesetzes"* and post-employment benefits from the member's own non-employer-funded premiums are expressly excluded.
  **What is not a Versorgungsbezug is the point**: a **private Riester annuity**, a **private Basisrente** and **every Schicht-3
  annuity** (RV, FRV, IDX, SOF) are in none of the five classes — but **a *Versorgungswerk* pension is**, which this page did not say,
  so the Schicht-1 exemption does not extend to the compulsory professional schemes. **§ 226 Abs. 2 gives the *Freibetrag* whose base
  this page could not previously state:** contributions on *Versorgungsbezüge* and *Arbeitseinkommen* are payable only where the
  monthly total exceeds ***ein Zwanzigstel der monatlichen Bezugsgröße nach § 18 des Vierten Buches***, and where it does, a
  *Freibetrag* of the same one-twentieth is deducted from the § 229 Abs. 1 Satz 1 Nr. 5 income, capped at that income.
  **§ 240 Abs. 1** provides for voluntary members that the *Spitzenverband Bund der Krankenkassen* fixes the basis uniformly and that
  *"die Beitragsbelastung die gesamte wirtschaftliche Leistungsfähigkeit des freiwilligen Mitglieds berücksichtigt"*, with Abs. 2
  setting a floor at what a comparable employed member would pay. **The statute does not itself name private annuities**; their express
  inclusion is in the *Beitragsverfahrensgrundsätze Selbstzahler* of the GKV-Spitzenverband, which was not retrieved, so that step is
  `[unverified]` — but the *gesamte wirtschaftliche Leistungsfähigkeit* standard is the statutory hook, and **the self-employed, the
  core Basisrente market and a large part of the private annuity market, are overwhelmingly freiwillig or privately insured**, so the
  exposed population is precisely the one buying the products. **The claim that Versorgungsbezüge are contributory "at the full rate
  borne entirely by the pensioner" is not in §§ 226, 229 or 240** — that rule is § 248 SGB V, which was not read, and the claim is
  removed from this entry.
  Three delib parameters hang off one annual regulation, the *Sozialversicherungsrechengrößen-Verordnung*: the Basisrente ceiling
  [R39], the *Kleinbetragsrente* threshold [R42] and the § 226 *Freibetrag* — so **delib carries them as `[std]` parameters in one
  place, with the year stated, and every product document references that one place**. **Still unverified:** the 2026 monthly
  *Bezugsgröße* of 3 955 €, which the earlier contract sweep recorded from two secondary sources and which **no official document
  retrieved here confirms**; § 7 ErbStG; § 248 SGB V; and the two ErbStG structuring practices.

---

## 9. Biometric bases---

## 9. Biometric bases and market statistics

**Read the warning first, because this section did not improve as much as the others.** Network access has changed nothing about the
central fact: **the five DAV tables are members' deliverables of a private association, are not published, and were not retrieved.**
**No value from any DAV table is known to this library, at any age, for any of the five tables**, and none may appear anywhere in
delib attributed to one. What did change is that the **public** material behind the `[std]` proxies — Destatis's period and cohort
tables [R52] — is now retrieved, and that the market aggregates in R53 now come from the publications themselves rather than from
reports of them.
Every decrement CSV in delib is a `**[std]**` proxy, anchored so the product's own worked example reproduces exactly, and each
product's `sources.md` names the DAV table the proxy stands in for and says what a replacement must preserve.

(delib-reg-r47)=

### R47. Rechnungsgrundlagen erster und zweiter Ordnung, and the DAV as owner of the tables

- **Publisher:** Deutsche Aktuarvereinigung e.V. (DAV)
- **URL:** https://aktuar.de/ and https://aktuar.de/de/wissen/regularien/
- **Accessed:** 2026-08-30
- **Retrieved:** the **DAV site** yes (home page HTML, 130 kB; *Regularien* page, read 2026-08-30). **No DAV table, and no DAV
  document describing a table's construction, was retrieved** — none is published.
- **Used for:** the two-basis structure every delib technical note's assumption split rests on.
- **Annotation:** The DAV occupies a position with **no equivalent in frlib, uklib or uslib**: it is at once the professional body
  whose members sign the statutory certifications [R11], the standard-setter whose *Fachgrundsätze* bind them [R56], **the body that
  derives and owns the market's biometric tables**, and the body that makes the annual *Höchstrechnungszins* recommendation [R56].
  In France the mortality tables are homologated by *arrêté* and printed in the *Code des assurances* annexe, so a modeller can read
  them; in Germany the equivalent tables are a **members' deliverable of a private association**. That single institutional
  difference is why this section is shaped the way it is: **every table citation in delib is a citation to a document the library has
  not read and cannot ship — and, unlike every other section of this page, that did not change when the network opened.**
  **The mechanic that does not depend on having a PDF open.** German life actuarial practice runs **two parallel sets of assumptions**
  over the same contract. ***Rechnungsgrundlagen erster Ordnung*** are the pricing and reserving bases — the *Rechnungszins* capped by
  § 2 DeckRV [R14], a biometric table carrying explicit safety margins, and cost loadings; they are deliberately **prudent**, which is
  a statutory requirement — § 138 Abs. 1 VAG demands *angemessene versicherungsmathematische Annahmen* [R8] and § 5 Abs. 1 DeckRV goes
  further, in words now read: *"Die Ableitung von Rechnungsgrundlagen auf der Basis eines besten Schätzwertes genügt nicht. Die
  Abschätzung künftiger Verhältnisse muss eine nachteilige Abweichung der relevanten Faktoren von den getroffenen, aus den Statistiken
  abgeleiteten Annahmen beinhalten."* [R17] — **so the prudence margin is not convention, it is a regulation** — and they determine the
  *Bruttobeitrag* and the *Deckungsrückstellung*. ***Rechnungsgrundlagen zweiter Ordnung*** are the best-estimate assumptions and
  determine what actually happens. **The *Sicherheitszuschlag* is the wedge between them, and its direction depends on which way the
  risk runs**: for a **death benefit** prudence means assuming mortality **higher** than expected; for a **survival benefit or
  annuity** it means **lower** mortality **and a stronger assumed improvement trend**, so a generational annuity table carries safety
  in **two dimensions** and a proxy reproducing only the level is not a proxy for the table; for **disability** it means higher
  incidence and lower reactivation; for **care**, higher incidence, longer duration in care and lower mortality of care recipients.
  **The wedge is not waste — it is the profit-sharing engine**: its systematic release as experience emerges is the *Risikoüberschuss*,
  one of the three *Überschussquellen* fed into the RfB and distributed under the MindZV [R10] [R18]. **A delib model that projects
  only best-estimate cash flows must still know the first-order basis**, because that is what fixes the *Bruttobeitrag* and the
  guaranteed benefits — the numbers the contract states — while the second-order basis drives the projection; the technical notes'
  three-way assumption split is this distinction wearing different clothes. **An insurer may use its own table**, because neither
  § 138 VAG nor § 5 DeckRV names one — so the DAV table is a **market default and benchmark, not a legal mandate**, and § 143 VAG makes
  the insurer's own choice a matter for the supervisor rather than the public [R11]. **Still unverified:** everything about the tables
  themselves, per [R48] to [R51].

(delib-reg-r48)=

### R48. DAV 2008 T and its predecessors — the death-benefit mortality basis

- **Publisher:** Deutsche Aktuarvereinigung e.V., 2008 `[unverified]`. Proprietary actuarial table. **Not public, not redistributable;
  delib ships no version
- **URL:** **not established.** The DAV website was browsed in this pass (`aktuar.de`, its *Wissen* and *Regularien* sections): it
  publishes press releases, *Fachinformationen* and the *Höchstrechnungszins* fact sheet, and **no page offering or describing DAV
  2008 T was found**.
- **Accessed:** 2026-08-30
- **Retrieved:** **no — the table is not published.** This is not a network limitation: `aktuar.de` serves, and was opened; the DAV
  distributes its tables to members and licensees. The table's *name* remains corroborated only at one remove.
- **Used for:** naming the basis a delib `[std]` proxy stands in for, and nothing else.
- **Annotation:** The market-standard first-order mortality basisfor **German death-benefit business** — *Risikolebensversicherung*,
  the death component of a *Kapitallebensversicherung*, death cover in a deferred annuity's accumulation phase, and the
  *Beitragsrückgewähr* death benefit of a BAS or RIE contract. It succeeded **DAV 1994 T** and is understood to derive from pooled
  German insured-lives experience rather than population data — the substantive difference from a Destatis table [R52], since insured
  lives are **selected** and their mortality is materially lighter than the general population's at the working ages term cover lives
  at. Structural features a `**[std]**` proxy must reproduce, each `[unverified]`: **sex-specific base tables** (raw material even
  though a tariff may not price on sex since 2012, [R34]); a **smoker/non-smoker split**, which German term insurers use heavily and
  which produces the roughly two-to-one premium spread in the RLV market; **selection factors** for the first years after
  underwriting; and **no projected mortality improvement**, because for death cover improvement is favourable to the insurer, so a
  prudent first-order basis does not project it. **That is the exact opposite of DAV 2004 R [R49], and it is why a single "German
  mortality table" does not exist: the direction of prudence forks by product.** Model consequences: an RLV model built on a
  population table without a selection adjustment **overstates claims by a wide margin at issue ages 25–45**, so the RLV proxy is
  documented as insured-lives-shaped with its anchor stated; and where a KLV carries both a death and a survival benefit, **using one
  table for both is a numbered pitfall**. **Unverified:** the publication year (2008 is inferred from the name), the data window, the
  age range, whether smoker/non-smoker and selection tables are part of the published set, the size of the loading, and whether a
  first- and second-order pair is distributed — **all not established**, as are the names and dates of DAV 1994 T and ADSt 1986.

(delib-reg-r49)=

### R49. DAV 2004 R and DAV 2004 R-Bestand — the generational annuity tables

- **Publisher:** Deutsche Aktuarvereinigung e.V., 2004 `[unverified]`. Proprietary actuarial tables. **Not public, not
  redistributable; delib ships no version
- **URL:** **not established.** As at [R48], `aktuar.de` was browsed in this pass and carries no page offering or describing
  DAV 2004 R.
- **Accessed:** 2026-08-30
- **Retrieved:** **no — the tables are not published**, and the reason is the DAV's distribution model, not a network limit.
- **Used for:** naming the basis a delib `[std]` generational proxy stands in for, and fixing the structure that proxy must have.
- **Annotation:** The market-standard first-order basisfor **every German annuity promise** — RV and SOF directly, and FRV, IDX, BAS
  and RIE through annuitisation of the accumulated fund. Its defining property is that it is a ***Generationentafel***: a
  two-dimensional basis $q(x,\\tau)$ in attained age and calendar year, **not a period table**. That is the one structural fact a
  delib annuity model must reproduce, and reproducing it is not optional — **a period-table proxy priced at a 40-year-old's
  annuitisation in 2055 understates the liability by a margin that dwarfs every other assumption in the model**. The construction, as
  the German market describes it and `[unverified]` in every detail: a **Basistafel** of second-order mortality for a stated base
  year, sex-specific; a ***Trendfunktion*** supplying age-dependent annual improvement rates; and safety loadings applied to **both**
  the level and the trend. The trend is not constant over time — the German construction uses a **Starttrend** fitted to recent
  experience **converging to a weaker Zieltrend** — so **a proxy applying one flat improvement rate forever is qualitatively wrong in
  long deferrals**. For single-premium immediate annuities buyers self-select for good health and the table is understood to carry
  ***Selektionsfaktoren***, the mirror image of the underwriting selection in DAV 2008 T, running the same direction for the opposite
  reason; **a SOF model that ignores it understates the annuity cost**. **DAV 2004 R-Bestand** is the variant for the
  *Deckungsrückstellung* of annuities **already in force**: when DAV 2004 R was introduced it revealed that the book priced on DAV
  1994 R was reserved on mortality that had proved far too heavy, and the strengthening (*Nachreservierung*) was permitted to be
  financed over a transition period. **Modelling consequences:** every delib annuity model needs **two indices** on the mortality
  cells, with the calendar year stated as `issue_year + t`; the `**[std]**` proxy must be **generational**, built as a base table
  times a cumulative improvement factor anchored to Destatis's own generational tables [R52], which are the free and redistributable
  analogue; and the guaranteed *Rentenfaktor* of an FRV or IDX contract is the arithmetic image of this table plus the guaranteed
  rate, so a model publishing a `[std]` *Rentenfaktor* **and** a `[std]` annuity table must state whether the two are consistent and,
  if not, which is authoritative.

(delib-reg-r50)=

### R50. DAV 1997 I / RI / TI — the Berufsunfähigkeit decrement family

- **Publisher:** Deutsche Aktuarvereinigung e.V., 1997 `[unverified]`. Proprietary actuarial tables. **Not public, not
  redistributable; delib ships no version
- **URL:** **not established.** As at [R48] and [R49].
- **Accessed:** 2026-08-30
- **Retrieved:** **no — the tables are not published.**
- **Used for:** naming the family a delib BU `[std]` proxy stands in for, and recording that its naming is itself uncertain.
- **Annotation:** **The naming is recorded here as a question, not a settled fact, and this pass did not settle it.**A German BU model needs **three** decrements and
  the market names a family of **three** tables — **I** for *Invalidisierung* (incidence), **RI** for *Reaktivierung*, and **TI** for
  the *Sterbewahrscheinlichkeiten der Invaliden*. Reading "TI" as the reactivation table would leave disabled-life mortality
  unspecified, which no multi-state BU model can do; the three-table reading is `[unverified]`, and **a delib document should not
  repeat a two-table pairing without checking.** **The multi-state structure the tables serve.** A BU model is a three-state process —
  *aktiv* → *invalide* → *tot*, with a return arc *invalide* → *aktiv* — needing, per age and sex: $i_x$ (incidence), $q_x^{aa}$
  (active-life mortality, from DAV 2008 T or its predecessor, [R48]), $q_x^{ii}$ (disabled-life mortality, materially heavier than
  active mortality especially in the first year after disablement) and $r_x$ (reactivation, concentrated in the first two years of a
  claim and near zero thereafter). **This is the most data-hungry product in delib and the one whose `[std]` proxies carry the least
  support.** **The age of the basis is itself a finding:** these tables date from 1997 and rest on older experience, while German BU
  claims experience has shifted decisively — the causes mix has moved towards psychiatric diagnoses and the statutory
  *Berufsunfähigkeitsrente* was abolished for cohorts born from 1961, changing both the insured population and its incentives. A
  thirty-year-old first-order basis with a heavy safety loading is **why the German BU market runs a large and persistent
  *Bruttobeitrag*/*Zahlbeitrag* gap** [R37]. **Modelling consequences:** the BU model must publish an **explicit reactivation
  assumption** — setting it to zero is a choice with a large, one-directional effect that must be argued, not defaulted;
  **disabled-life mortality must be separate from active-life mortality**, using one rate for both being a numbered pitfall; and the
  six-month qualification and the 50 % degree threshold are **AVB conventions, not table properties** [R37].

(delib-reg-r51)=

### R51. DAV 2008 P, § 15 SGB XI and the Pflegegrad break

- **Publisher:** Deutsche Aktuarvereinigung e.V. for the table; Bundesamt für Justiz for the SGB XI
- **URL:** https://www.gesetze-im-internet.de/sgb_11/__15.html for the statute (text read from the canonical XML); **not established**
  for the table
- **Accessed:** 2026-08-30
- **Retrieved:** the **statute** yes (canonical XML, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228; §§ 15, 36, 37 and
  43 read in full, read 2026-08-30). **The table, no — DAV 2008 P is not published**, as at [R48].
- **Used for:** the trigger scale a PFL model must declare, and the social benefit ladder the private product is sold against.
- **Annotation:** **DAV 2008 P** is the market-standard first-order basis for private long-term-care business —
  *Pflegerentenversicherung*, and in the health sector *Pflegetagegeld* and *Pflegekosten* cover, which delib treats as out of scope.
  It is understood to supply, by age and sex, **transition probabilities into care**, **mortality of people in care** and
  **transitions between care levels** `[unverified]`.
  **The finding that matters most is a mismatch, not a number, and the statutory side of it is now read in full.** A table published
  in 2008 is necessarily defined on the **three *Pflegestufen*** of the pre-2017 social care insurance. The *Zweites
  Pflegestärkungsgesetz* replaced them on **1 January 2017** with the **five *Pflegegrade*** of § 15 SGB XI, and the statute's own
  machinery shows how different the new scale is. § 15 Abs. 2: the *Begutachtungsinstrument* has **six modules** matching the six areas
  of § 14 Abs. 2, weighted ***Mobilität* 10 %**, ***kognitive und kommunikative Fähigkeiten sowie Verhaltensweisen und psychische
  Problemlagen* together 15 %**, ***Selbstversorgung* 40 %**, ***Bewältigung von und selbständiger Umgang mit krankheits- oder
  therapiebedingten Anforderungen und Belastungen* 20 %** and ***Gestaltung des Alltagslebens und sozialer Kontakte* 15 %**; modules 2
  and 3 contribute **one** weighted score, the higher of the two, not both. § 15 Abs. 3 then maps the total: **Pflegegrad 1 from 12,5
  to under 27 points; Pflegegrad 2 from 27 to under 47,5; Pflegegrad 3 from 47,5 to under 70; Pflegegrad 4 from 70 to under 90;
  Pflegegrad 5 from 90 to 100**, with Abs. 4 allowing Pflegegrad 5 below 90 points in *besondere Bedarfskonstellationen*. **A points
  instrument weighting cognition and behaviour at 15 % and self-care at 40 % is not the old *Pflegestufen* scale rescaled — it is a
  different state space**, and the BGH has **refused to map the two** [R36]. **If the courts will not map the grades, a modeller may
  not silently do so either.** Therefore, for delib's PFL product: the model **states which trigger scale it implements** —
  *Pflegegrade*, an ADL points system, or a combination — and **any incidence proxy calibrated to Pflegegrade data is explicitly not a
  proxy for DAV 2008 P**, because the two are defined on different state spaces separated by a definitional break that raised measured
  prevalence.
  **The social scheme is the benchmark the private product is sold against, and its amounts are now read rather than described.**
  § 37 Abs. 1 — *Pflegegeld* per calendar month: **347 € (Pflegegrad 2), 599 € (3), 800 € (4), 990 € (5)**. § 43 Abs. 2 — the
  *vollstationär* contribution per calendar month: **805 € (2), 1 319 € (3), 1 855 € (4), 2 096 € (5)**. § 36 Abs. 1 — *Pflegesach­
  leistung* likewise runs from Pflegegrad 2. **Pflegegrad 1 receives none of the three**, which the sections confirm by opening each
  entitlement at *"Pflegebedürftige der Pflegegrade 2 bis 5"*. The amounts rise steeply with grade and are capped and partly in kind,
  which is why **the private *Pflegerente* — uncapped cash, paid irrespective of setting — is the product's entire selling
  proposition** and why its benefit is modelled as an annuity rather than a reimbursement. **These euro figures are the version of
  SGB XI in force at the `Stand` above and change with amending acts; a delib document quoting one states the `Stand`.**
  The private benefit ladder is conventionally a **percentage of the full *Pflegerente* per Pflegegrad**, and **no market standard was
  retrieved**, so it is `**[std]**` in delib unless a *Tarifblatt* supplies it. **Resolved in this pass:** the § 15 module weights and
  point boundaries, and the social benefit amounts. **Still unverified:** everything about DAV 2008 P, and the *Zweites
  Pflegestärkungsgesetz* as the amending instrument and 1 January 2017 as its date — the consolidated SGB XI shows the result, not the
  instrument.

(delib-reg-r52)=

### R52. Destatis — Periodensterbetafeln, Kohortensterbetafeln, Pflegestatistik and the reuse licence

- **Publisher:** Statistisches Bundesamt (Destatis), Wiesbaden
- **URL:** https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/sterbetafel.html and
  .../kohortensterbetafeln.html, with the downloads
  `.../Publikationen/Downloads-Sterbefaelle/statistischer-bericht-sterbetafeln-5126207237005.xlsx` and
  `.../statistischer-bericht-kohortensterbetafeln-5126101239005.xlsx`, and https://www.destatis.de/DE/Service/Impressum/_inhalt.html
  for the licence
- **Accessed:** 2026-08-30
- **Retrieved:** yes for the **methodology and headline results** (three HTML pages, 86 kB / 90 kB / the *Impressum*, read
  2026-08-30). **The `.xlsx` tables themselves were located but not opened**, so no $q_x$ value is quoted here.
- **Used for:** the free, redistributable population basis behind every `[std]` decrement CSV delib ships, and the licence that makes
  that lawful.
- **Annotation:** The **free, redistributable, population-level German mortality basis** — exactly the role INSEE plays in frlib.
  **Two distinct products, and the vocabulary this page used was Destatis's older one.** Destatis publishes ***Periodensterbetafeln***
  — computed from three calendar years of deaths and population, *"eine Momentaufnahme der Sterblichkeitsverhältnisse der gesamten
  Bevölkerung"*, containing **no assumption about future development**, the current edition being the **Sterbetafel 2023/2025** — and
  ***Kohortensterbetafeln***, not *Generationensterbetafeln*, which is the name the earlier version of this entry used. The cohort
  tables *"weisen den spezifischen Sterblichkeitsverlauf und die Lebenserwartung eines Geburtsjahrgangs auf"* and, for cohorts still
  alive, rest on projected mortality *"in Anlehnung an die Annahmen zur Entwicklung der Lebenserwartung der 15. koordinierten
  Bevölkerungsvorausberechnung"*, published in **two variants — Variante 1 on the low and Variante 2 on the high life-expectancy
  assumption** — a spread Destatis publishes precisely so that a user need not pick a single trend. **That two-variant, projected
  structure is exactly the structure DAV 2004 R has** [R49], and it is why the cohort tables are the right public basis for delib's
  `[std]` generational annuity proxy. From the period side, two anchors that give a proxy its level: on the Sterbetafel 2023/2025 a
  65-year-old man has a further life expectancy of **18.0 years** and a woman of **21.1 years**; life expectancy at birth in the
  2023/2025 period is back slightly above the pre-pandemic 2017/2019 level. From the cohort side, the 2023 birth cohort is projected
  to reach roughly **81 to 90 years for boys and 85 to 93 for girls** depending on variant — the width of that range being the honest
  measure of what a single flat improvement rate hides.
  **Why a population table is the wrong shape:** insured lives are selected, so population mortality is heavier than insured mortality
  at the ages term and endowment business lives at, and lighter than annuitant mortality is light — **it sits between the two insured
  populations and matches neither**. A delib proxy built from it therefore carries an explicit, `[std]`-tagged adjustment with a
  stated direction: **downward for a term or endowment death leg** (medical selection) and **downward again and generationally for an
  annuity** (voluntary anti-selection plus improvement), built as
  $q(x,\tau)=q_{\text{base}}(x)\cdot\prod(1-\lambda(x))$ over the calendar years from the base year, with $\lambda(x)$ a `[std]`
  age-dependent improvement rate anchored so the worked example reproduces exactly and documented as a **simplification** of the
  Starttrend/Zieltrend structure rather than a replication of it.
  The ***Pflegestatistik*** is the **only public German prevalence data for long-term care** and therefore the calibration target for
  every `[std]` PFL incidence assumption; **the series contains a definitional break at the 2017 reform that is not a change in the
  underlying risk** [R51], so any delib document quoting a prevalence trend says so and **no incidence proxy is calibrated across the
  break**. That break claim is `[unverified]` here: the *Pflegestatistik* itself was not opened in this pass.
  **The licence question is now answered rather than assumed.** Destatis's own *Impressum* states, for the GENESIS-Online database:
  *"© Statistisches Bundesamt (Destatis), 2026 — Datenlizenz Deutschland – Namensnennung – Version 2.0"* — an attribution licence, so
  reuse with attribution is permitted. **delib's position does not depend on it anyway**, because the shipped CSVs are **constructed,
  anchored, documented `[std]` proxies**, not reproductions of any published series, each carrying a `provenance` column naming what it
  stands in for. **It does depend on never shipping a DAV table**, which is not a licence question at all.
  **Resolved in this pass:** the correct Destatis vocabulary, the two-variant cohort structure, the current period-table edition and
  two headline anchors, and the reuse licence. **Still unverified:** every $q_x$ value — the workbooks were located but not opened —
  and the *Pflegestatistik*'s 2017 break.

(delib-reg-r53)=

### R53. The German life market in numbers — GDV, Assekurata, map-report, Morgen & Morgen and Franke und Bornberg

- **Publisher:** Gesamtverband der Deutschen Versicherungswirtschaft e.V.; Assekurata Rating-Agentur; Franke und Bornberg / map-report
- **URL:** https://www.gdv.de/resource/blob/188374/dde4d81192e583ac43e7e80a84aa6ac6/die-deutsche-lebensversicherung-in-zahlen-2025-publikation-pdf-data.pdf,
  https://www.assekurata-rating.de/2026/01/29/ueberschussdeklaration/,
  https://www.franke-bornberg.de/fb-news/pressemitteilungen/map-report-939-solvabilitaet-im-vergleich-2015-bis-2024 and
  https://www.franke-bornberg.de/blog/map-report-verwaltungskostenquote-2023-lebensversicherer.
  **The URL this entry previously carried — `bafin.de/.../dl_st_24_erstvu_lv_va.html` — returns HTTP 404 and has been replaced.**
- **Accessed:** 2026-08-30
- **Retrieved:** yes (GDV *Die deutsche Lebensversicherung in Zahlen 2025*, PDF, reporting business year 2024; Assekurata
  *Überschussdeklaration 2026* of 29.01.2026, HTML, 194 kB; map-report 939 press release, HTML, 94 kB; map-report
  *Verwaltungskostenquote* article, HTML, 102 kB; read 2026-08-30). **BaFin's own life statistics were not retrieved: the cited
  download 404s.**
- **Used for:** the market aggregates a product spec's market-role section quotes, and the observed ranges a `[std]` parameter needs.
- **Annotation:** **Volumes, business year 2024, GDV basis** (Lebensversicherer, Pensionskassen and Pensionsfonds together), read from
  the 2025 edition of *Die deutsche Lebensversicherung in Zahlen*: premium income **+2.8 % to €94.6 bn**; ***Einmalbeitrag* +9.8 % to
  €28.3 bn**; *laufende Beiträge* **€66.3 bn**, nearly unchanged; benefits paid **+2.8 % to €101.8 bn**, about €279 m a day;
  new-business sum insured **+1.9 % from €323 bn to about €329 bn**. **The contract count in this entry was wrong and is corrected:**
  the stock at end-2024 was **84.3 m contracts** (start of 2024: 85.5 m), a fall of 1.4 per cent — the earlier text gave the correct
  percentage against the wrong level of 80.3 m. Of those, **more than 46 m are Rentenversicherungen** and **8.8 m
  Direktversicherungen**; **Riester stands at 9.7 m contracts at end-2024, down 3.5 %, with life insurers' Riester new business down
  26.0 % in the year** — the numbers behind [R44]'s closure. The operative reading is still the **Einmalbeitrag shift**: single
  premium is now roughly 30 per cent of income and growing far faster than regular premium, which is why SOF is a live product and why
  KLV and RV model point tables include single-premium points. **The GDV taxonomy** is the vocabulary any German market figure comes
  in: *Kapitalversicherungen* → KLV, *Risikoversicherungen* → RLV, *Rentenversicherungen* → RV and SOF, *fondsgebundene* → FRV,
  *sonstige Lebensversicherungen* (where index business sits and is **not separately visible**), and *Zusatzversicherungen* (BU as a
  **rider**, while delib models the *selbständige* form); Riester and Basisrente **cut across** it. **The BaFin life-segment figure of
  €90.4 bn *verdiente Bruttobeiträge* is dropped from this entry**, because the source 404s and the two bases must never appear in the
  same table anyway.
  **Declared rates — this entry now carries a distribution rather than three disputed averages.** Assekurata's *Überschussdeklaration
  2026* publishes the ***laufende Verzinsung*** of classical private annuities **per insurer** for 2024, 2025 and 2026, with the *Neue
  Klassik* value in brackets where one exists, and states the composition in terms this page had asserted: *"Diese setzt sich aus der
  Garantieverzinsung und der laufenden Zinsüberschussbeteiligung zusammen."* — **so a delib model must never add the declared rate on
  top of the guarantee**, a numbered pitfall for every general-account product. The 2026 column runs from about **2.10 %** at the low
  end to **3.50 %** at the high, with large names in between — Allianz **2.70** (2.80), Axa **3.00**, EUROPA **2.90** (3.20),
  Continentale **2.60** (2.90), Alte Leipziger **2.40** (2.50), Gothaer **2.45** (2.70) — and several insurers raising the rate
  between 2025 and 2026. **That observed range, not an average, is what a `[std]` credited-rate parameter should be argued against.**
  The averages this page previously reported (2.53 % / 2.58 % for 2025, and three conflicting 2026 figures) were **not retrieved and
  are dropped**; Assekurata also notes that for *Neue Klassik* *"kann der Garantiezins unterschiedlich sein"*, so bracketed values are
  not comparable across insurers without knowing the guarantee.
  **Cost ratios — and the spread this page gave was far too narrow.** map-report reports the industry ***Verwaltungskostenquote*** at
  **2.46 % for 2023** against **2.34 % for 2022**, i.e. rising, with a per-insurer range from **0.79 %** (Europa, a direct writer) to
  **11.29 %** (Targo) — not "from under 2 % to over 4 %". Direct writers and the largest insurers sit at the bottom of the
  distribution. **A `[std]` administration-cost parameter should therefore be argued against a distribution with an order-of-magnitude
  spread and a stated distribution channel, not against a market average.**
  **The 2024 solvency reset** [R13], read from map-report 939: the life industry's SCR ratio **including** transitionals was
  **340.3 % at end-2024 against 663.6 % at end-2023**, a fall of about 323 percentage points driven by BaFin's ordered recalculation
  of the *Rückstellungstransitional* rather than by economics; the **base ratio excluding transitionals was 308.6 %**, only about
  32 points lower, where in 2023 the gap had been 342.9 points — the recalculation removed an accounting cushion, not capital.
  **Three life insurers failed to reach 100 % without Hilfs- und Übergangsmaßnahmen at 31 December 2024**, against 21 at the first
  Solvency II reporting date for 2016; the per-insurer spread at end-2024 ran from **103.9 %** (Concordia Oeco) to **716.4 %**
  (LV 1871). map-report also records that the transitionals **run out in 2032**, which § 352 Abs. 2 VAG confirms [R13].
  **The survey houses** supply what no statutory source does: Assekurata's annual *Überschussdeklaration* tracks the declared rates
  and the shift from full *Beitragsgarantie* through "Neue Klassik" partial guarantees to levels below 100 % of premiums — the premise
  of delib's IDX product; *map-report* draws insurer-level series from the statutory accounts [R54] and gives the **spread** as well as
  the average, which is what a `**[std]**` parameter needs; and MORGEN & MORGEN and Franke und Bornberg publish the two standard **BU
  claims-practice** studies, **neither of which was opened in this pass**. **The BU consequence is specific and remains
  `[unverified]` in its level:** a model paying every incident claim in full is modelling a 100 % acceptance rate, so **delib's BU
  incidence assumption is `[std]` net of declinature, stated as such**, with a pitfall recorded that applying a gross incidence table
  *and* an acceptance ratio double-counts.

---

## 10. Accounting and professional standards

(delib-reg-r54)=

### R54. HGB §§ 341–341o, RechVersV and BerVersV — the German statutory accounts and supervisory returns

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/hgb/__341f.html (human-facing; that per-section page is a 5.0 kB frameset shell —
  `dejure.org/gesetze/HGB/341f.html` also serves), https://www.gesetze-im-internet.de/rechversv/BJNR337800994.html and
  https://www.gesetze-im-internet.de/berversv_2017/BJNR285800017.html; the HGB and RechVersV texts were read from the canonical XML
- **Accessed:** 2026-08-30
- **Retrieved:** yes for the **HGB** (canonical XML, Stand: zuletzt geändert durch Art. 4 G v. 4.2.2026 I Nr. 33; §§ 341e and 341f
  read in full) and for the **RechVersV** (canonical XML, Stand: zuletzt geändert durch Art. 69 G v. 10.8.2021 I 3436; §§ 15, 25 and
  28 read in full), read 2026-08-30. **The BerVersV was retrieved only as its table of contents** — the index page carries the section
  list, and **its Anlagen, where the *Nachweisungen* live, were not opened.**
- **Used for:** the prudence standard behind the German statutory reserve, the prospective method, and the published anatomy of the
  surplus system.
- **Annotation:** **§ 341e — the standard of prudence, quoted.** *"Versicherungsunternehmen haben versicherungstechnische
  Rückstellungen auch insoweit zu bilden, wie dies nach vernünftiger kaufmännischer Beurteilung notwendig ist, um die dauernde
  Erfüllbarkeit der Verpflichtungen aus den Versicherungsverträgen sicherzustellen."* — the same standard § 138 Abs. 1 VAG imposes on
  premiums [R8] and § 294 Abs. 4 VAG makes the supervisory objective [R5] [R21], and the reason the German statutory reserve is
  deliberately conservative rather than best-estimate. § 341e Abs. 1 Satz 2 then subordinates it to the supervisory rules on the
  *Rechnungsgrundlagen* **including the *Rechnungszinsfuß*** — the hook through which the DeckRV binds the HGB accounts — and Satz 3
  requires valuation at the balance-sheet date's conditions **without § 253 Abs. 2 discounting**.
  **§ 341f — the *Deckungsrückstellung*, and the prospective method is now the statute's own words.** One must be formed for
  obligations *"aus dem Lebensversicherungs- und dem nach Art der Lebensversicherung betriebenen Versicherungsgeschäft"* — the hook
  that brings a *Pflegerente* or a stand-alone BU annuity inside the same reserving rule — *"in Höhe ihres versicherungsmathematisch
  errechneten Wertes einschließlich bereits zugeteilter Überschußanteile mit Ausnahme der verzinslich angesammelten Überschußanteile
  und nach Abzug des versicherungsmathematisch ermittelten Barwerts der künftigen Beiträge (prospektive Methode)"*, with a
  retrospective fallback where a prospective calculation is not possible. **§ 341f Abs. 2 is the statutory root of the
  Zinszusatzreserve**, and it is short enough to quote: *"Bei der Bildung der Deckungsrückstellung sind auch gegenüber den Versicherten
  eingegangene Zinssatzverpflichtungen zu berücksichtigen, sofern die derzeitigen oder zu erwartenden Erträge der Vermögenswerte des
  Unternehmens für die Deckung dieser Verpflichtungen nicht ausreichen."* — which is exactly the calculation § 5 Abs. 3 DeckRV then
  parameterises with the *Referenzzins* [R17].
  **The RechVersV** is the statutory-accounts rulebook: insurers use **Formblatt 1 instead of § 266 HGB** for the balance sheet and
  **Formblatt 3** for the life/health profit and loss account, both following the ***Nettoprinzip***. Two of its sections close loops
  elsewhere on this page. **§ 25 Abs. 1** requires *"angemessene Sicherheitszuschläge"* in the *Deckungsrückstellung* and permits
  one-off acquisition costs to be recognised by an appropriate actuarial method, *"insbesondere dem Zillmerungsverfahren"*; **§ 25
  Abs. 2** provides that where the § 341f HGB reserve falls below the contractually or statutorily guaranteed *Rückkaufswert*, **it is
  raised to that value**, and the same for a paid-up benefit — **which is where the § 169 Abs. 3 VVG floor enters the balance sheet**
  [R28], and what DeckRV § 4 Abs. 3 then refers back to [R16]. **§ 15 Abs. 1** defines the *noch nicht fällige Ansprüche* receivable
  that DeckRV § 4 Abs. 2 caps.
  **§ 28 gives the German surplus system its published anatomy, and § 28 Abs. 8 Nr. 2 is now read item by item.** The *Anhang* must
  give, in tabular form: the **development of the RfB** (opening, additions, withdrawals, closing); and the parts attributable to
  **(a)** declared but unallocated current profit shares, **(b)** declared but unallocated final shares and final payments, **(c)**
  declared but unallocated minimum *Bewertungsreserven* amounts, **(d)** other declared but unallocated *Bewertungsreserven* amounts,
  **(e)–(g)** the three tranches of the ***Schlussüberschussanteilfonds*** — for *Gewinnrenten*, for final shares and payments, and for
  the minimum *Bewertungsreserven* participation — and **(h)** *"den ungebundenen Teil (Rückstellung für Beitragsrückerstattung ohne
  die Buchstaben a bis g)"*, **which is the definition the RfBV and MindZV § 13 both borrow** [R18] [R19]. Nr. 3 requires, **for each
  *Abrechnungsverband* or *Bestandsgruppe*, the declared profit shares and where applicable the *Ansammlungszinssatz* with the year of
  allocation**, and Nr. 4 *"die Verfahren zur Berechnung des Schlussüberschussanteilfonds sowie die gewählten Rechnungsgrundlagen"*.
  **This is the single most useful published source on a named insurer's surplus system**, and the reason a delib product document can
  cite a declared *Überschussanteilsatz* at all.
  **The BerVersV** governs the national, HGB-based returns beyond the Solvency II templates; its section list confirms *"Zusätzliche
  formgebundene Erläuterungen der Lebensversicherungsunternehmen"* as § 10. **That the life returns carry a *Zerlegung des
  Rohergebnisses nach Ergebnisquellen* under *Nachweisungen 213 bis 219*, filed as forms F.213.01 to F.219.01, was not read from the
  BerVersV itself and is `[unverified]` at that level of detail** — but **the substance is confirmed from the other side**: MindZV § 4
  Abs. 1 defines the *Kapitalanlageergebnis*, the *Risikoergebnis* and the *übrige Ergebnis* by **named lines and columns of
  *Nachweisung 213* of the BerVersV**, and MindZV §§ 6 and 13 cite *Nachweisung 219* and *Formblatt 200* the same way [R18].
  **A German minimum allocation is therefore computed from named cells of a named supervisory form**, which is unusually concrete and
  worth saying in a delib technical note. **delib computes none of this:** no model produces a *Deckungsrückstellung*, an RfB stock or
  a P&L, and the accounting layer is cited, never specified.

(delib-reg-r55)=

### R55. IFRS 17 — Versicherungsverträge and the Variable Fee Approach

- **Publisher:** IASB; DRSC and Haufe for the German commentary
- **URL:** https://www.drsc.de/projekte/insurance-contracts/ and
  https://www.haufe.de/id/kommentar/joerg-baetgepeter-wollmerthans-juergen-kirschpeter-oser-2-variable-fee-approach-vfa-HI16462224.html
- **Accessed:** 2026-08-30
- **Retrieved:** the **commentary** yes (DRSC project page, HTML, 485 kB; Haufe VFA commentary, HTML, 152 kB; Deloitte overview,
  HTML, 326 kB; read 2026-08-30). **The standard itself was not retrieved** — IFRS 17 is IFRS Foundation copyright and is not freely
  served; the EU endorsement regulation was not opened either.
- **Used for:** naming the measurement framework a delib cash flow would feed, and nothing more.
- **Annotation:** IFRS 17 *Versicherungsverträge* was issued by the IASB on **18 May 2017**, replacing the interim standard IFRS 4.
  **Scope:** insurance contracts, reinsurance contracts and **investment contracts with discretionary participation features** — the
  last category matters in Germany because it catches savings vehicles that are not insurance in the risk-transfer sense.
  **The Variable Fee Approach**, in the German commentary's words, *"findet ausschließlich auf solche Versicherungsverträge Anwendung,
  die durch eine direkte Überschussbeteiligung ... gekennzeichnet sind"*, and *"Der VFA ist verpflichtend für die im Standard
  spezifizierten Versicherungsverträge mit direkter Überschussbeteiligung anzusetzen"*, reinsurance being excluded and measured under
  the general model or the premium allocation approach. It is an adaptation of the building-block approach that explicitly reflects the
  value development of the underlying items, the difference being recorded in the **Contractual Service Margin** — which is what
  "variable fee" names. Under the VFA, **investment returns on the underlying portfolio no longer hit the income statement
  immediately; they flow through the CSM, which is released progressively.** German life contracts qualifying for the VFA typically
  include the HGB gross-surplus participation — i.e. **the *Überschussbeteiligung* chassis of [R9], [R10] and [R18] is precisely what
  makes them direct-participating.** For delib IFRS 17 is **cited, never specified**: no model produces a CSM, a risk adjustment or a
  fulfilment cash flow, and the models produce gross liability cash flows that an IFRS 17 measurement would take as one input.
  **A dating caveat this pass turned up and this entry now records.** The DRSC project page as served on 2026-08-30 is **out of
  date**: it still states the original first-application date of *"Geschäftsjahre, die am oder nach dem 1. Januar 2021 beginnen"* and
  reports the deferral as being *"um ein Jahr auf 2022"*. **The 1 January 2023 application date and *Verordnung (EU) 2021/2036* as the
  endorsement instrument were therefore not confirmed by anything retrieved here and remain `[unverified]`** — the earlier version of
  this entry stated both as fact. **Still unverified:** in addition to the dates, the CSM, the risk adjustment, the coverage units and
  the transition approaches beyond the sentences above; which German life insurers report under IFRS 17 (only listed groups do; solo
  German statutory accounts remain HGB); and **whether Riester and Basisrente contracts qualify as direct-participating**.

(delib-reg-r56)=

### R56. DAV Fachgrundsätze and the annual Höchstrechnungszins recommendation

- **Publisher:** Deutsche Aktuarvereinigung e.V.
- **URL:**
  https://aktuar.de/de/newsroom/detail/dav-empfiehlt-auch-fuer-2027-einen-hoechstrechnungszins-fuer-lebensversicherungs-neuvertraege-in-hoehe-von-10-prozent/,
  with https://aktuar.de/content/PDF/News/Pressemeldungen/2025_11_26_DAV_PM_H%C3%B6chstrechnungszins.pdf,
  https://aktuar.de/content/PDF/Fachwissen/H%C3%B6chstrechnungszins_in_der_Lebensversicherung.pdf and
  https://aktuar.de/de/wissen/regularien/
- **Accessed:** 2026-08-30
- **Retrieved:** yes (the newsroom item, HTML, 51 kB; the **press release of 26.11.2025**, PDF, 3 pp.; the ***Fachwissen* fact sheet
  *Höchstrechnungszins in der Lebensversicherung***, PDF, 2 pp.; and the DAV *Regularien* page; read 2026-08-30). The
  ***Zinsbericht für 2026*** (PDF, 551 kB) was located but not read.
- **Used for:** the method behind the annual recommendation, and the asymmetry between the interest haircut and the biometric ones.
- **Annotation:** **The recommendation and its method, now read from the DAV rather than reported.** The *Höchstrechnungszins* is set
  by the Bundesministerium der Finanzen as the DeckRV's *Verordnungsgeber*, which the DAV states in terms: *"Die abschließende
  Entscheidung über den Höchstrechnungszins obliegt dem Bundesministerium für Finanzen durch eine Änderung der
  Deckungsrückstellungsverordnung."* [R14] The DAV submits an annual proposal — *"Spätestens zu Beginn eines Jahres prüft die Deutsche
  Aktuarvereinigung, inwieweit der jeweils aktuell gültige Höchstrechnungszins in der Lebensversicherung auch für das Folgejahr noch
  angemessen ist."* — and the ministry has in the past mostly followed it, **a soft-law channel with no statutory anchoring any
  retrieved document identifies**, so delib describes it as **practice rather than law**.
  **The method, in the DAV's own description:** a representative new-money portfolio of a life insurer with a conservative investment
  strategy is modelled — government, government-guaranteed, covered and corporate bonds plus a small allocation to equities and
  property, the latter valued *"analog zum Vorgehen der Produktinformationsstelle Altersvorsorge (PIA)"* [R43]; average returns are
  projected under various interest scenarios; ***"Zur weiteren Glättung wird außerdem das arithmetische Mittel dieser Renditen über
  die vergangenen fünf Jahre gebildet."***; and ***"Zusätzlich wird ein 40-prozentiger Abschlag als Sicherheitspuffer eingerechnet, so
  wie ihn der Gesetzgeber bis zur Einführung von Solvency II verlangt hat."***, with a floor: *"auch in Tiefzinsphasen [muss] der
  Sicherheitsabschlag immer mindestens 0,4 Prozentpunkte betragen."* — **a minimum absolute haircut this page did not previously
  carry.** The DAV also states plainly that undertakings may use less: *"ist der Höchstrechnungszins das Maximum, das Unternehmen zur
  Berechnung ihrer Rückstellungen annehmen dürfen"* [R14].
  **The 40 per cent haircut is the residue of the statutory 60 % ceiling** that bound the German rate from the mid-1990s until
  Solvency II, derived from Article 17 of the Third Life Directive of 1992 and carried forward as Article 20 of Directive
  2002/83/EC, under which the reserving rate could not exceed 60 % of the rate on bonds issued by the State in whose currency the
  contract is denominated, and repealed without replacement when Solvency II took effect. **Those two directive articles were not
  retrieved in this pass and remain `[unverified]`**; what the DAV does confirm is that the 40 per cent discount is the survival of a
  requirement *"wie ihn der Gesetzgeber bis zur Einführung von Solvency II verlangt hat"*.
  **The recommendations.** The DAV recommended the increase from 0.25 % to 1.00 % for 2025, which the ministry adopted [R15], then
  recommended keeping 1.0 % for 2026, and on **26 November 2025** recommended **1.0 % for 2027** as well: *"Die Deutsche
  Aktuarvereinigung e.V. (DAV) empfiehlt, den seit Januar 2025 gültigen Höchstrechnungszins für Neuverträge in der Lebensversicherung
  in Höhe von 1,0 Prozent auch für das Jahr 2027 beizubehalten."*, on the ground that ten-year euro swap rates ran well above 2 % in
  2025 and that the model portfolio's projected average returns lie durably above 1.0 %.
  **The asymmetry that matters for delib:** the interest haircut is **documented and quantified at 40 % with a 0.4-point floor**; the
  biometric haircuts [R47] are **neither, for any of the five tables**, and this library must not present the two legs of the
  *Rechnungsgrundlagen* as equally supported.
  **The professional standards, now described in the DAV's own words rather than assumed.** The *Regularien* page defines
  ***Fachgrundsätze*** as publications of DAV and IVS which, together with the *Standesregeln*, lay down the principles of proper
  professional practice, and which are characterised by four features: they address actuarial technical questions; they are of
  fundamental and practice-relevant importance; **they are professionally legitimated by a *Feststellungsverfahren* open to all
  members**; and **their proper use is secured by a *Disziplinarverfahren***. They are expressly to be distinguished from
  ***Ergebnisberichte***, which individual DAV committees produce for information and discussion and which carry no such force.
  **The three-tier *Grundsätze / Richtlinien / Hinweise* naming this page previously asserted does not appear on that page and stays
  `[unverified]`.** The mechanism that matters for a cash flow model is the chain from standard to tariff: § 138 VAG requires
  *angemessene versicherungsmathematische Annahmen* [R8], § 5 Abs. 1 DeckRV forbids a pure best-estimate derivation [R47], and
  **neither instrument names a table**; the gap between "prudent" and "this specific $q_x$" is closed by the *Verantwortlicher Aktuar*
  under § 141 Abs. 5 Nr. 1 VAG [R11] exercising professional judgement, subject to the DAV's disciplinary process.
  **A German biometric basis is therefore soft law with hard consequences:** no statute mandates DAV 2008 T, and yet essentially every
  German term tariff is priced on it or on an insurer table justified against it. **The delib convention that follows:** cite the
  **named document or nothing** — a delib document that cites "a DAV standard" without saying which one is making a claim it cannot
  support.

---

### The two liability measures one projection feeds

A German life insurer values the same book twice, on two different bases, and both valuations consume the same per-policy projection
of premiums, claims, expenses and discretionary benefits. Keeping them apart is the single discipline this page exists to enforce.

**The HGB *Deckungsrückstellung*.** A prospective, deliberately prudent reserve computed on the *Rechnungsgrundlagen erster Ordnung*
of the premium calculation — the contract's own *Rechnungszins*, capped at conclusion by § 2 DeckRV [R14] [R15], and a first-order
biometric table [R47] — formed to the extent necessary to ensure *dauernde Erfüllbarkeit* [R54], increased by the *Zinszusatzreserve*
where the § 5 Abs. 3 DeckRV *Referenzzins* falls below the tariff rate [R17], and reduced by the actuarial present value of future
premiums. **This is the balance sheet the German surplus system actually operates on:** the MindZV 90/90/50 minimum allocation [R18],
the RfB ring fence and its three escape hatches [R10], the MindZV § 13 ceiling on the *ungebundene* part and the RfBV ceilings on the
*Teilbestände* and on the collective part [R18] [R19], and the § 139 VAG *Sicherungsbedarf* test on *Bewertungsreserven* [R9] are all
computed on the HGB accounts — which is why
a document describing a German contract must name the HGB measure even though no delib model computes it.

**The Solvency II *Solvabilitätsübersicht*.** A market-consistent balance sheet under §§ 74–88 VAG [R6], transposing Directive
2009/138/EG [R1] and elaborated by Delegated Regulation (EU) 2015/35 [R2], on which technical provisions are a **best estimate**
discounted at the EIOPA risk-free term structure [R4] plus a **risk margin**, with the long-term-guarantee measures and the §§ 351–353
transitionals [R13] sitting on top. **The cost-of-capital rate has now been read from the instrument** — 6 per cent, Art. 39 of
Delegated Regulation (EU) 2015/35 [R2] — and so have the risk-margin formula, the reference-undertaking assumption and the 99.5 %
one-year calibration [R1]. **Contract boundaries and the standard-formula shocks were not read**, so those remain `**[std]**` in this
library, and the SCR and MCR layers are cited-not-specified — though the MCR now has section numbers, §§ 122–123 VAG [R6]. **IFRS 17** [R55] is a third measure but a group-reporting one: German solo statutory accounts remain HGB, and no
delib model produces a CSM.

**What this library computes: none of them.** The delib models publish gross best-estimate-style liability cash flows per model point,
income-positive, undiscounted, on a declared annual or monthly grid. The discounting, the margins, the *Deckungsrückstellung*
recursion, the *Zinszusatzreserve*, the RfB stock and the CSM layer belong to a layer above — which is the only honest way to serve
two statutory bases and one international standard from a single projection, and the reason every product document says so in its own
scope note.

**And one last time, because it governs every line above.** **The retrieval position has changed, and each entry now states its own.**
Forty-four of the fifty-six entries were opened and read in the pass of **2026-08-30** and say so on a `Retrieved:` line that records
what was read — the canonical statutory XML with the law's `Stand` for the fifteen German instruments, the Official Journal text for
the European ones, and the publication itself for BaFin, the DAV, the GDV, Destatis and the survey houses. **Twelve entries fall short
of that**, each with a specific reason rather than a blanket one: three are a flat `no` — R48, R49 and R50, because the DAV tables
they name are not published at all — and the other nine say exactly what was missing, from the Solvency II review directive and the
IFRS 17 standard, through five of the six BGH lines and the AltEinkG's own text, to the MaGo circular and the LVRG's *Regelungstext*.
**Where an entry still carries `[unverified]`, it now says precisely why**, and the distinction between "not retrievable",
"retrievable but not opened in this pass" and "opened and silent on the point" is drawn per claim rather than asserted page-wide.

**The `Retrieval conditions` section at the head of this page now carries that position instead of the drafting-time one**, and the
two agree: 44 of 56, with the twelve named and a reason given for each. The drafting conditions are kept there as provenance — this
library was first written under blocked egress and an exhausted search budget, and that is part of what it is — but they no longer
describe how to read it. And the standing advice survives the change unaltered: **re-verify against the instrument before relying on
anything here** — a citation tells you what to check, and this pass has made the checking possible rather than made it unnecessary.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-reg-r1
[R10]: #delib-reg-r10
[R11]: #delib-reg-r11
[R12]: #delib-reg-r12
[R13]: #delib-reg-r13
[R14]: #delib-reg-r14
[R15]: #delib-reg-r15
[R16]: #delib-reg-r16
[R17]: #delib-reg-r17
[R18]: #delib-reg-r18
[R19]: #delib-reg-r19
[R2]: #delib-reg-r2
[R20]: #delib-reg-r20
[R21]: #delib-reg-r21
[R22]: #delib-reg-r22
[R23]: #delib-reg-r23
[R24]: #delib-reg-r24
[R25]: #delib-reg-r25
[R26]: #delib-reg-r26
[R27]: #delib-reg-r27
[R28]: #delib-reg-r28
[R29]: #delib-reg-r29
[R3]: #delib-reg-r3
[R30]: #delib-reg-r30
[R31]: #delib-reg-r31
[R32]: #delib-reg-r32
[R34]: #delib-reg-r34
[R35]: #delib-reg-r35
[R36]: #delib-reg-r36
[R37]: #delib-reg-r37
[R38]: #delib-reg-r38
[R39]: #delib-reg-r39
[R4]: #delib-reg-r4
[R40]: #delib-reg-r40
[R41]: #delib-reg-r41
[R42]: #delib-reg-r42
[R43]: #delib-reg-r43
[R44]: #delib-reg-r44
[R45]: #delib-reg-r45
[R46]: #delib-reg-r46
[R47]: #delib-reg-r47
[R48]: #delib-reg-r48
[R49]: #delib-reg-r49
[R5]: #delib-reg-r5
[R51]: #delib-reg-r51
[R52]: #delib-reg-r52
[R53]: #delib-reg-r53
[R54]: #delib-reg-r54
[R55]: #delib-reg-r55
[R56]: #delib-reg-r56
[R6]: #delib-reg-r6
[R7]: #delib-reg-r7
[R8]: #delib-reg-r8
[R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
