# Risikolebensversicherung (term life) — research notes (Germany)

Research notes for the German individual *Risikolebensversicherung* (RLV) — the pure protection
contract that pays a *Todesfallleistung* (death benefit) equal to the agreed *Versicherungssumme* if
the *versicherte Person* dies inside the *Versicherungsdauer*, and pays **nothing at all** otherwise.
It is the German market's cheapest and structurally simplest life contract, and the only one of the
ten delib products with no accumulation phase, no *Erlebensfallleistung* and, in the ordinary case,
no *Rückkaufswert*.

**In scope.** The individual, privately written, *selbständige* (standalone) term assurance on one or
two lives, with a **level *Bruttobeitrag*** over the whole *Beitragszahlungsdauer*, an
*Überschussbeteiligung* applied as ***Beitragsverrechnung*** so that the customer pays a
***Zahlbeitrag*** materially below the *Bruttobeitrag*, a *Versicherungssumme* that is **konstant**,
**linear fallend** or **annuitätisch fallend**, medical underwriting through *Gesundheitsfragen* with
*Raucher*/*Nichtraucher* differentiation and *Risikozuschläge*, the three-year *Selbsttötung* window
of § 161 VVG, and a *Nachversicherungsgarantie* on named life events. The single-life form and the
*verbundene Leben* form (two lives, one payment on the first death) are one chassis parameterised by
the number of lives. The *Über-Kreuz-Versicherung* — the same cover arranged so that each partner
insures the other's life and is his own *Bezugsberechtigter* — is a **contracting structure**, not a
different product, and is covered because it changes the tax outcome and nothing else.

**Out of scope, and said so where it matters.**

- *Restschuldversicherung* / *Restkreditversicherung* — the single-premium, bank-sold, loan-linked
  group cover. It shares the falling sum insured of the *annuitätisch fallende* RLV and nothing else:
  *Gruppenversicherung* sold through the lender, underwritten by a health declaration or not at all,
  with its own charge structure and mis-selling history. Where this file names a falling sum, it means
  a **standalone** RLV whose schedule shadows a loan.
- *Sterbegeldversicherung* — small-sum whole-of-life funeral cover with a *Wartezeit* and no
  *Gesundheitsprüfung*; it builds a *Deckungskapital* and carries a *Rückkaufswert*.
- *Risikolebensversicherung mit Beitragsrückgewähr* — the variant returning premiums on survival; it
  has a savings element by construction and is economically a *Kapitallebensversicherung* (delib
  product 1) with an unequal death and survival sum.
- The *Berufsunfähigkeits-* and *Unfalltod-Zusatzversicherung* riders commonly attached to an RLV; the
  standalone *Berufsunfähigkeitsversicherung* is delib product 9, and the rider forms are described
  here as options and not modelled.
- *Betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung* and
  *Kollektivverträge*; and Austrian and Swiss *Risikoversicherung* documents, to which the VVG, DeckRV,
  MindZV and ErbStG do not apply.

These notes are the **citation ground truth** for the delib `risikolebensversicherung` product
documents — `product-spec.md`, `technical-notes.md`, `model.md` and `sources.md`. Source ids
**S1..S17** and **R1..R23** below are **frozen — never renumber**; unused ids are simply omitted
downstream, leaving gaps, and `sources.md` records which are absent and why.

Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

Stated in the same terms as every other delib document, and in two halves: the two limits the
research was **done** under on 2026-08-29, and what the **re-verification** of 2026-08-30 established.
A reader who picks up only this file must learn both from this file.

**No document named here had been retrieved when it was written.** Direct HTTP egress from the build
environment was blocked by an organisation network policy: `WebFetch` and `curl` were refused
(HTTP 403 at the egress gateway) for every host outside a short package-registry allowlist. The hosts that matter for this product were
tried and refused — `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `buzer.de`, `destatis.de` and `de.wikipedia.org`. Not one
AVB PDF, *Produktinformationsblatt*, *Verbraucherinformation*, statutory text or comparison-portal
rate table was opened.

**The session's `WebSearch` budget was already exhausted before this product's research began.** The
session shares a hard cap of 200 calls; it was reached during the research for the two products
written earlier — `kapitallebensversicherung` and `klassische_rentenversicherung` — and **zero
searches were available for `risikolebensversicherung`**. Every attempt returns the budget-exhausted
message. That is materially worse than the position of the two sibling files, which at least had
search-result summaries, and worse again than `frlib/_research/temporaire-deces.md`, where the French
*notices d'information* were downloaded and read in full.

**What this file therefore was as drafted.** A statement of German term-assurance law, product
structure and market practice written from the authoring model's own knowledge, disciplined in three
ways:

1. **Documents were named as known references, not as evidence.** Each `S#` and `R#` entry names a
   document that **exists and is the right kind of document** for the claim beside it. Each carried
   `Retrieved: no — direct HTTP egress blocked; no search corroboration (session search budget
   exhausted)` unless it inherited corroboration through point 2. **This is the rule the
   re-verification changed**, and the paragraph after this list says how far. **No document number, edition date,
   page count or *Bundesgesetzblatt* citation is stated unless inherited**; where a URL is unknown the
   entry says `URL: not established`, and a canonical form given from confident knowledge is marked
   `[unverified]`.
2. **One inherited evidentiary spine.** Several instruments this product turns on — §§ 161, 169, 165
   and 19 VVG, the MindZV, the DeckRV, VAG § 139 and the DAV 2008 T *Richtlinie* — **were
   search-corroborated for the two sibling products while budget remained**, and their findings are
   recorded in `delib/_research/kapitallebensversicherung.md` and
   `delib/_research/klassische_rentenversicherung.md`. Where a fact here rests on that, the entry says
   **"inherited corroboration"** and names the sibling file and its source id. This is a real, if
   second-hand, chain and it is the strongest evidence in this file. Everything not so marked has
   **no** corroboration.
3. **Numbers become `[std]`, not citations.** Where the mechanic is certain and the level is not — the
   *Brutto*/*Zahlbeitrag* ratio, the *Sicherheitszuschlag*, the *Ratenzahlungszuschlag*, the
   *Stornoquote*, the premium rates themselves — this file ships a **`[std]` parameter with a stated
   rationale and an argued plausible range**, and puts the missing figure in the gaps register. A
   `[std]` number is honest; a guessed `[S7]` number is not, and there are none here.

**`[unverified]` keeps its normal meaning and is used generously**: any specific paragraph number,
effective date, monetary amount, percentage, price point or market figure that no search confirmed. It
is **not** applied to the general shape of a well-established mechanic — that would drown the signal —
but the moment a claim becomes specific and numeric it carries either an inherited corroboration, a
retrieval, or the tag.

**The re-verification of 2026-08-30.** The policy was lifted and the citations were checked against
the primary documents. Library-wide, all fifteen German instruments delib cites were read as canonical
XML from `gesetze-im-internet.de` with each law's amendment `Stand` recorded, 950 statutory section
references were checked and 950 were correct, and insurer AVB, *Verbraucherinformationen* and
*Produktinformationsblätter* were retrieved as PDFs and read; **501 of the library's 805 source
entries, 62 %, now read `Retrieved: yes`.** In this file the pass reached **23 of the 40 entries
below, and those 23 now carry their own `Retrieved:` line: 22 say yes and one says no ([R12])**. They
are the statutory spine — VVG, VVG-InfoV, MindZV, DeckRV, VAG, AGG, EStG, ErbStG, HGB and VersStG,
each read as canonical XML at a recorded `Stand`, with the load-bearing rules now quoted exactly in
German — and the GDV model wordings and carrier AVB at [S1] to [S5]. The other seventeen entries carry
no per-entry line, nothing was opened for them, and the drafted status above still governs them:
[S6]–[S17] are the carrier and comparison material, and [R18]–[R20], [R22] and [R23] the DAV,
rating-agency and statistical material.

**What an entry now means.** A **`Retrieved: yes`** line means the document was opened and the passage
the entry rests on was read, at the `Stand` or edition the line records. Where there is a
`Retrieved: no` line or no line at all, the citation is still **a pointer rather than a certificate**:
it names the instrument a claim must be checked against and does not assert that anyone checked it.
Note the one trap the pass exposed: the `.../<slug>/__<n>.html` addresses printed below are
**human-facing links only** — they answer 200 with a frameset of a few kilobytes and no statutory text
— so a section cited only through one of them is not retrieved. **The re-verification changed things**:
paragraph numbering is no longer `[unverified]` for any provision that was read, and where a reading
corrected an entry the entry says so. What it did not reach is the whole **quantitative** side — no
rate card, no *Produktinformationsblatt*, no price point, no DAV table — so every `[std]` level in
this file stands exactly where it did.

**What is not in this file, and would be in a properly researched one**: no insurer's AVB text, no
*Produktinformationsblatt*, no published *Bruttobeitrag* / *Zahlbeitrag* pair, no comparison-portal
price point, no *Nachversicherungsgarantie* event list from a wording, no smoker/non-smoker price ratio
from a rate card, no GDV statistic for the *Risikoversicherung* segment. Each is a numbered gap below.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. Tables and headings are in
English; the prose is English about German products.

| Term | Gloss |
|---|---|
| *Risikolebensversicherung* (RLV), *Risikoversicherung* | Term assurance: death cover for a fixed period, no survival benefit |
| *Todesfallleistung* / *Versicherungssumme* (VS) | The death benefit / the sum insured; *konstant*, *linear fallend* or *annuitätisch fallend* |
| *Versicherungsdauer* / *Beitragszahlungsdauer* / *Eintrittsalter* / *Endalter* | Cover period / premium-paying period / age at entry / age at which cover ends |
| *Bruttobeitrag*, *Tarifbeitrag* | The tariff premium: the **guaranteed maximum** the policyholder can ever be asked to pay |
| *Zahlbeitrag*, *Nettobeitrag* (consumer sense) | The premium billed = *Bruttobeitrag* less the *Beitragsverrechnung*. **Not guaranteed** |
| *Nettoprämie* (actuarial sense) | The risk premium before expense loadings — **a different quantity** from the consumer *Nettobeitrag* (mechanic 4) |
| *Nettotarif*, *Honorartarif* (distribution sense) | A commission-free tariff sold through fee-based advice. **A third, unrelated sense of "netto"** |
| *Beitragsverrechnung*, *Sofortverrechnung* | The *Überschussverwendung* form that nets declared surplus against the *Bruttobeitrag* |
| *Überschussbeteiligung* / *Überschussanteile* / *Deklaration* | The statutory entitlement to share in surplus (§ 153 VVG) / the amounts allocated / the annual declaration of rates |
| *Risikoüberschuss* / *Kostenüberschuss* / *Zinsüberschuss* / RfB | Mortality / expense / interest surplus — here the first dominates and the third is negligible / the provision holding surplus before allocation |
| *Rechnungsgrundlagen erster / zweiter Ordnung*, *Sicherheitszuschlag* | First-order (prudent, tariff and reserving) and second-order (best-estimate) bases / the prudential margin between them |
| *Rechnungszins* / *Höchstrechnungszins* | The technical interest rate / its statutory maximum for new business |
| *Deckungsrückstellung* / *Deckungskapital* / *Zillmerung* / *Höchstzillmersatz* | The balance-sheet provision / one contract's reserve / financing acquisition costs through it / the statutory cap on the amount so financed |
| *Rückkaufswert* / *Beitragsfreistellung*, *prämienfreie Versicherung* | Surrender value, **absent on the ordinary RLV** (mechanic 11) / making the contract paid-up, and the *beitragsfreie Versicherungssumme* that results |
| *Gesundheitsprüfung* / *Gesundheitsfragen* / *Vorvertragliche Anzeigepflicht* | Medical underwriting / the health questions asked / the applicant's pre-contractual duty of disclosure (§ 19 VVG) |
| *Risikozuschlag* / *Leistungsausschluss* / *Berufsgruppe* / *Raucher*, *Nichtraucher* | Extra-mortality loading / an individually agreed exclusion / occupation rating class / smoker, non-smoker |
| *Nachversicherungsgarantie* / *Dynamik* | The right to raise the sum insured on a named life event **without a new *Gesundheitsprüfung*** / automatic annual escalation of sum and premium, with a right of *Widerspruch* |
| *Verbundene Leben* / *Über-Kreuz-Versicherung* | Two *versicherte Personen* on one contract, one payment on the first death / the cross-contracting structure in which each partner insures the other's life and is his own beneficiary |
| *Versicherungsnehmer* (VN) / *versicherte Person* (vP) / *Bezugsberechtigter* | Policyholder / life insured / beneficiary — routinely three different roles here |
| *Selbsttötung* / *Kriegsklausel* | Suicide (§ 161 VVG) / the war clause restricting the benefit where death is connected with war |
| *Vorläufiger Versicherungsschutz* / *Wartezeit* / *Restschuldabsicherung* | Provisional cover between application and acceptance / waiting period, **normally absent on an RLV** / cover shaped to a loan's outstanding balance |
| *Erbschaftsteuer* / *Freibetrag* / *Steuerklasse* / *Erwerb von Todes wegen* | Inheritance tax / personal allowance / relationship class / the charging concept the *Über-Kreuz* structure avoids |
| *Stornoquote* / AVB / *Verbraucherinformation* / *Produktinformationsblatt* (PIB) | Lapse rate / policy conditions / consumer information pack / short pre-contractual product summary |

---
## Primary sources

**The blanket retrieval status this section once declared no longer holds in full.** As drafted,
every entry carried **Retrieved: no — direct HTTP egress blocked in the build environment; no search
corroboration (the session `WebSearch` budget was exhausted before this product's research began)**,
stated once here rather than repeated seventeen times. **Five of the seventeen were opened on
2026-08-30** — the two GDV model wordings [S1] [S2] and the carrier documents at [S3], [S4] and [S5]
— and each of those five now carries its **own** `Retrieved:` line with the edition it was read at.
The other twelve carry no line, nothing was opened for them, and the status above is still theirs.
Where an entry inherits corroboration from a sibling delib research file, the entry says so.

Order: GDV model wordings (S1–S2), carrier documents (S3–S13), then secondary consumer, comparison
and rating material (S14–S17). **Every carrier named below sells a *Risikolebensversicherung* in
Germany; that much is asserted from knowledge. Nothing about the content of any particular wording is
asserted, because nothing was read.**

### S1 — GDV, "Allgemeine Bedingungen für die Risikolebensversicherung" (*Musterbedingungen*)

- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. Doc type: *Musterbedingungen*
  — model AVB published by the industry association for members to adopt, adapt or ignore
- URL: `https://www.gdv.de/resource/blob/6324/13d86b44ff6f4d6800e9ddeb7bc17476/allgemeine-bedingungen-fur-die-risikolebensversicherung-data.pdf`, reached from the index at
  `https://www.gdv.de/gdv/service/musterbedingungen`. **Its own title is *Allgemeine Bedingungen für
  die Risikolebensversicherung***, not "für die Risikoversicherung"
- **Retrieved: yes** — PDF, 18 pp., **Stand: 21.07.2025**, read 2026-08-30
- Content — what this document is, and what weight an `[S1]` tag carries:
  - The GDV maintains model conditions for the main German life lines and the *Risikoversicherung* is
    one of them. The model wordings address the customer in the second person with question-headed
    sections ("Welche Leistungen erbringen wir?"), the style adopted for post-2008-VVG wordings
    [inherited: `kapitallebensversicherung.md` S1].
  - The disclaimer is on the first line of the document, verbatim: "Diese Bedingungen sind für die
    Versicherer unverbindlich; ihre Verwendung ist rein fakultativ. Abweichende Bedingungen können
    vereinbart werden." **An `[S1]`-tagged fact is a market template, weaker evidence about any
    carrier than the same fact taken from that carrier's own AVB** — which is why every clause below
    is cited beside [S3] or [S4] where those carry it too.
  - **The article text is now established.** Four clauses carry weight downstream. **§ 5 Abs. 3**:
    "Wenn unsere Leistungspflicht durch eine Änderung des Vertrages erweitert wird oder der Vertrag
    wiederhergestellt wird, beginnt die Dreijahresfrist bezüglich des geänderten oder
    wiederhergestellten Teils neu" — gap 9, closed. **§ 13 Abs. 4 and Abs. 8**: *Kündigung* converts
    the contract into a *beitragsfreie Versicherung*, and where the paid-up sum fails a carrier-set
    minimum the policyholder receives "den Rückkaufswert entsprechend § 169 des
    Versicherungsvertragsgesetzes (VVG)", less an *Abzug* — **which contradicts this file's claim
    that a German RLV pays nothing on termination**. **§ 14 Abs. 2–3**: the § 4 DeckRV
    *Verrechnungsverfahren* at 2,5 %, with "die restlichen Abschluss- und Vertriebskosten ... über
    die gesamte Beitragszahlungsdauer verteilt" — so 25 ‰ bounds the zillmered part, not the whole α;
    footnote 28 adds that the clause belongs in a wording only "bei der Verwendung des
    Zillmerverfahrens". **§ 2 Abs. 2–3**: surplus allocated *verursachungsorientiert* by
    ***Bestandsgruppe*** and ***Gewinnverband***.

### S2 — GDV, *Produktinformationsblatt* pattern for the *Risikoversicherung*

- Publisher: GDV. Doc type: model *Produktinformationsblatt* (PIB). **The name has moved on**: since
  the IDD implementation the document § 4 VVG-InfoV requires is the ***Informationsblatt zu
  Versicherungsprodukten*** (IPID, Durchführungsverordnung (EU) 2017/1469) [R17]. **The GDV publishes
  no model PIB for this line** — its *Musterbedingungen* index carries model *Bedingungen* and
  *Standmitteilungen* only
- URL: carrier specimens stand in its place —
  `https://www.cosmosdirekt.de/resource/blob/15750/ce3439de3bbf09d3d5fee7889a3cd235/vib-crc-risikolebensversicherung-data.pdf`
  and
  `https://www.cosmosdirekt.de/resource/blob/89394/91ebf9428a54446bc0e61e17723c3332/pib-risiko-lebensversicherung-data.pdf`
- **Retrieved: yes** — PDF, 2 pp., *Muster-VIB CR_CRC (12.20)*; PDF, 5 pp., *PIB_CRB/CRCB_Berechnung
  (01.2018)*; both read 2026-08-30
- Content: **the inference was right and the document delivers more than expected.** It does state the
  ***Bruttobeitrag* and the *Zahlbeitrag* side by side**, and it also states the charges, because
  § 2 Abs. 1 Nr. 1 and § 4 Abs. 2 VVG-InfoV require them in euro. For a model case of **Eintrittsalter
  41, Vertragsdauer 19 Jahre, Bankkaufmann, Versicherungssumme 100 000 €**:

  | Edition | Tariff | *Tarifbeitrag* / month | *Zahlbeitrag* year 1 | ratio | α, euro | α, % of *Tarifbeitragssumme* |
  |---|---|---|---|---|---|---|
  | Muster-VIB (12.20) | CRB2 Basis | 18,21 € | 8,20 € | 0,4503 | 99,98 € | 2,41 % |
  | Muster-VIB (12.20) | CRCB2 Comfort | 23,68 € | 10,66 € | 0,4502 | 129,97 € | 2,41 % |
  | PIB (01.2018) | CRB2 Basis | 19,75 € | 8,89 € | 0,4501 | — | — |
  | PIB (01.2018) | CRCB2 Comfort | 25,68 € | 11,55 € | 0,4498 | — | — |

  Other annual costs 48,52 € (Basis) and 63,08 € (Comfort), of which 35,20 € and 45,76 €
  *Verwaltungskosten*, taken over the 19-year premium term; paid-up administration 1,50 € per 100 €
  of paid-up sum insured. **The ratio is the same to three decimals across two tariffs and two
  editions** — § 138 VAG's *Gleichbehandlung* visible in the numbers. Gap 1 and gap 8 close for this
  carrier; **no figure here is promoted to a model parameter** (gap 3 closed as to the field list).

### S3 — CosmosDirekt (Cosmos Lebensversicherungs-AG), *Risikolebensversicherung*

- Doc type: *Allgemeine Bedingungen für die Risiko-Lebensversicherung* and *Besondere Bedingungen*.
  The `LA <number> <letter>` convention held: the term-assurance codes are **LA 803 A** and
  **LA 804 A**
- URL: `https://www.cosmosdirekt.de/resource/blob/7944/7b400325610aa816ee0ed2e1deda323d/allgemeine-bedingungen-risikoversicherung-la-803-a--data.pdf`
  and `https://www.cosmosdirekt.de/resource/blob/611396/6d70b9698c9fc73321e55cb81a98c9e1/besondere-bedingungen-fuer-die-risiko-lebensversicherung-la-804-a--data.pdf`,
  from the carrier's library at `https://www.cosmosdirekt.de/services/vertragsservice/vertragsservice-versicherungsbedingungen/`
- **Retrieved: yes** — PDF, 11 pp., **LA 803 A (04.26)**; PDF, 6 pp., **LA 804 A (04.26)**; read
  2026-08-30
- Content: the primary carrier wording of this product. **§ 3 Abs. 2 b** states the central mechanic:
  "Die Überschussanteile (Sofortrabatt) werden **in Prozent des Bruttobeitrags** festgesetzt und mit
  den laufenden Beiträgen verrechnet." **§ 3 Abs. 1 a** gives the MindZV percentages (90 / 50 / 90)
  and says the premiums leave "keine oder allenfalls geringfügige Beträge" for capital, so **no
  *Bewertungsreserven* arise at all** (Abs. 1 c). **§ 2** gives the *Selbsttötung* clock with its
  per-increment restart, the *Kriegsklausel* as an **exclusion** (not a *Deckungskapital*
  substitution), the ABC clause gated on 1 000 lives and a *Treuhänder*, and a terrorism exclusion.
  **§ 13** gives the *Nachversicherungsgarantie* in full (gap 7). **§ 15** gives the paid-up right on
  a constant sum insured with a 300 € minimum, its impossibility on a falling sum insured, and
  *Kündigung* "zum Ende des laufenden Monats" with "kein Rückkaufswert". **§ 16** applies § 4 DeckRV
  at 2,5 % and spreads the remainder. **§ 18** gives the twelve-month smoker qualifying period and
  treats a later switch as a *Gefahrerhöhung* (gap 22). And the *Rechnungsgrundlagen* preamble states
  a ***Rechnungszins* of 0,25 Prozent** and "einer unternehmenseigenen Sterbetafel auf Basis der
  DAV 2008T" — **the model prices at the 1,00 % DeckRV ceiling instead**. The direct-channel spread
  argument remains structural, and the spread stays `[std]` (mechanic 5).

### S4 — Hannoversche Lebensversicherung AG (VHV group), *Risikolebensversicherung*

- Doc type: *Bedingungen und Informationen — Risikoversicherung*, a pack containing the *Allgemeine
  Bedingungen für die Risikoversicherung / **T25***, the BUZ and UZ riders, *Steuer-Informationen*, a
  *Lexikon* and the *Merkblatt zur Anzeigepflichtverletzung*
- URL: `https://www.hannoversche.de/dam/risiko/bedingungen/bedingungen-risikolebensversicherung-aktuell.pdf`
- **Retrieved: yes** — PDF, 32 pp., document 700.0005.35, **Stand 09/2025**, read 2026-08-30
- Content: the second carrier wording, and the one that disproves this file's strongest claim.
  **§ 20 Abs. 3 b** corroborates S3 independently — the *Jahresgewinnanteil* is "in Prozent des
  **Tarifbeitrags**" and credited as a *Sofortgutschrift* — and Abs. 4 adds that it "kann auch **Null
  Euro** betragen". **§ 19** is the [S1] *Selbsttötung* clause word for word, restart included.
  **§ 13** is the problem: *Kündigung* "zum Ende des laufenden Monats" **converts the contract into a
  *beitragsfreie Versicherung*** (minimum 2 500 €), and below that minimum "wird das Deckungskapital
  abzüglich des oben beschriebenen Abzugs ausgezahlt und der Vertrag erlischt" — the *Abzug* being
  **60 % des Deckungskapitals** — with a *Rückkaufswerte* table annexed to the *Versicherungsschein*
  for every tariff **except T3 and T4**, the falling-sum tariffs that build no *Deckungskapital*.
  **So a German term assurance can carry a surrender value**, and the "no cash value, market-wide"
  claim in this file is wrong as to design, right as to magnitude. It also cites § 88 VAG and
  §§ 341e, 341f HGB as the *Deckungsrückstellung* basis, which is [R21] from the contract side.

### S5 — HUK-COBURG / HUK24, *Risikolebensversicherung* and the *Überschussbeteiligung* guide

- Doc type: insurer guide page **about term assurance specifically**, plus the product pages. URL:
  `https://www.huk24.de/risikolebensversicherung/ratgeber-lebensversicherung/ueberschussbeteiligung`
- **Retrieved: yes** — HTML, ~66 kB, read 2026-08-30
- Content — a carrier's own account of the *Überschussbeteiligung* **in this product**, not in the
  endowment:
  - The page is titled "Überschussbeteiligung der Risikolebensversicherung", so the carrier itself
    treats surplus participation as a **central feature of term assurance**. That alone contradicts
    the intuition an Anglophone modeller brings to a "term life" product.
  - **Correction to the inherited note.** The sibling entry recorded a **four-component surplus
    vocabulary** — *Zins-*, *Risiko-*, *Kosten-* und *übrige Überschüsse* — and this file carried it
    forward to the term product. **The page uses no such vocabulary.** It names **three** factors:
    the capital-market result, the insurer's cost structure and the number of deaths — which is the
    MindZV three [R9] and the three [S1], [S3] and [S4] all use. The four-component form belongs to
    the endowment file and has been removed from the product documents here.
  - **What the page does establish, and it is better.** The two surplus forms used on this line:
    "In der Praxis bieten Versicherer bei Risikolebensversicherungen für die Überschussbeteiligung
    wiederum meist eines von zwei Modellen an: den **Todesfallbonus** und den **Sofortrabatt**" —
    and [S1], [S3] and [S4] all carry exactly that pair, *Sofortrabatt* while premiums are paid and
    *Todesfallbonus* once paid up. And the asymmetry, stated by the carrier: the *Tarifbeitrag* "ist
    der **maximal zu leistende Versicherungsbeitrag**", and where surplus falls "steigt der Beitrag
    für den Versicherten höchstens bis zu dieser Höhe an".
  - **No rate, no *Beitragsverrechnung* percentage and no spread ratio is on this page**; those come
    from [S2] instead.

### S6 — Debeka Lebensversicherungsverein a. G., *Bedingungswerk* for the *Risikoversicherung*

- Doc type: *Bedingungswerk* (Debeka's name for its AVB booklets), in the carrier's public
  *Vertragsgrundlagen* library. URL: **not established.** The library's path pattern is
  `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/<code>.pdf`,
  established from the sibling research where three endowment wordings were located under it
  [inherited: `kapitallebensversicherung.md` S3–S6]. **The term-assurance code is not established and
  no path is guessed**
- Content: recorded because Debeka is the largest German life mutual by contract count and its
  *Vertragsgrundlagen* library is one of the few carrier document sets that is fully public and
  indexed by product family. Two inherited cautions transfer directly: Debeka maintains **several
  parallel wordings of different vintages within one product family**, and its *Überschussbeteiligung*
  clause numbering is **tariff-dependent**, so any specific section number is `[unverified]`
  [inherited: `kapitallebensversicherung.md` S3–S6]. **No Debeka term-assurance figure is asserted.**

### S7 — Dialog Lebensversicherungs-AG (Generali group), *Risikolebensversicherung*

- Doc type: AVB, *Verbraucherinformation*, broker-facing tariff material. URL: **not established**
- Content: named because Dialog positions itself as the German market's **specialist term-life carrier
  for the broker channel** — a monoline whose whole book is biometric risk. That matters in one
  specific way: a monoline's *Risikoergebnis* is its entire technical result, so the MindZV minimum
  allocation from the *Risikoergebnis* [R9] binds its surplus policy directly rather than competing
  with an investment result. **The positioning is asserted from knowledge; no wording, tariff, rate,
  *Berufsgruppen* table or surplus declaration is asserted** (gap 5).

### S8 — Allianz Lebensversicherungs-AG, *Risikolebensversicherung*

- Doc type: AVB, *Produktinformationsblatt*, product page. URL: **not established**
- Content: the market leader by premium income and the natural reference for the **narrow-spread** end
  of the *Brutto*/*Zahlbeitrag* distribution — a large composite with tied-agent and broker
  distribution has less room to net surplus against the tariff premium than a direct writer. **That is
  a structural argument, not an observation** (gap 1). One inherited fact bears on the family of
  Allianz life wordings: a declared *laufende Verzinsung* for 2026 of **2.70 %** on the classic book,
  above the market average [inherited: `kapitallebensversicherung.md` S11] — a **savings-side** rate,
  of no direct use here, where the *Zinsüberschuss* is negligible (mechanic 6).

### S9 — R+V Lebensversicherung AG, *Risikolebensversicherung*

- Doc type: AVB, *Produktinformationsblatt*, product page. URL: **not established**
- Content: one of the largest German life carriers and the cooperative-bank-channel comparator.
  **Nothing about its wording, rating structure or surplus declaration is asserted.**

### S10 — NÜRNBERGER Lebensversicherung AG, *Risikolebensversicherung*

- Doc type: AVB, *Verbraucherinformation*. URL: **not established.** The carrier's tariff-code
  convention is visible in the sibling research, which recorded an annuity wording headed "…nach Tarif
  NIR3301" [inherited: `klassische_rentenversicherung.md` S9]; **the term-assurance code is not
  established**
- Content: a broker-channel carrier with a long biometric-risk book. Recorded for the variations table
  only; **no parameter is asserted.**

### S11 — LV 1871 (Lebensversicherung von 1871 a. G.), *Risikolebensversicherung*

- Doc type: AVB, *Produktinformationsblatt*. URL: **not established**
- Content: a mutual with broker distribution whose range emphasises *Nachversicherungsgarantien* and
  occupational differentiation. **The emphasis is asserted from market knowledge; no event list, age
  cap, increase cap or *Berufsgruppen* table is asserted** (gap 7).

### S12 — Continentale Lebensversicherung a. G. and Europa Lebensversicherung AG, *Risikolebensversicherung*

- Doc type: AVB, *Produktinformationsblatt*, product pages. URL: **not established**
- Content: recorded as a **single entry deliberately**, because the pair is the clearest German
  instance of one group running a broker-channel carrier and a low-cost direct carrier side by side in
  the same product. If a *Brutto*/*Zahlbeitrag* comparison were ever made from public documents, this
  pair is where the channel effect would be visible with underwriting and reserving basis held
  constant. **No such comparison was made and no figure is asserted** (gap 5).

### S13 — Further carriers selling a *Risikolebensversicherung* in Germany (located as products, not as documents)

- Publishers: Alte Leipziger; Volkswohl Bund; Swiss Life Deutschland; Zurich Deutscher Herold; ERGO
  Vorsorge; AXA; Barmenia; Württembergische; Gothaer; Die Stuttgarter; Baloise (Deutschland); uniVersa;
  DEVK; SIGNAL IDUNA; Provinzial; Generali Deutschland; HDI. Doc type: AVB and
  *Produktinformationsblätter*. URL: **not established for any of them**
- Content: **this entry asserts one thing only — that each of these carriers offers an individual
  *Risikolebensversicherung* in Germany.** It exists so the variations table can state honestly that a
  market of this breadth exists and that **none of it was sampled**. **No `[S13]` tag appears on any
  parameter anywhere in the delib library.** Two of these carriers appear in the sibling research with
  located documents in **other** product families — Zurich Deutscher Herold with an annuity
  *Verbraucherinformation* series [inherited: `klassische_rentenversicherung.md` S4–S7] and Gothaer
  with an endowment AVB [inherited: `kapitallebensversicherung.md` S7] — which establishes that their
  document libraries are public and nothing about their term-assurance wordings.

### S14 — Comparison portals: Check24, Verivox, Tarifcheck — **secondary**

- Doc type: price-comparison result pages and accompanying *Ratgeber* articles. URL: **not established**
  for the term-assurance pages. The sibling research recorded Verivox *Ratgeber* pages on
  `Kapitallebensversicherung`, `Überschussbeteiligung` and `Zillmerung` [inherited:
  `kapitallebensversicherung.md` S15], establishing that the portal publishes explanatory pages of this
  kind and nothing about its term-assurance pages
- Content: **this entry's central claim was wrong and is withdrawn.** It said the portals are "the only
  public source of German RLV price points". They are not. § 2 Abs. 1 Nr. 1 and § 4 Abs. 2 VVG-InfoV
  put the premium and the costs on the pre-contractual *Informationsblatt* in euro, and carriers
  publish ***Muster*** specimens of it — which is how gap 1 was closed, at [S2], without a portal.
  What survives is the narrower and still true point: **a comparison result is generated per query
  and is not a published document**, so no portal price point is recorded here (gap 1).

### S15 — Finanztip, "Risikolebensversicherung" — **secondary**

- Doc type: consumer guide article with a periodically refreshed carrier recommendation. URL: **not
  established.** The sibling research recorded Finanztip articles on `Überschussbeteiligung
  Lebensversicherung` and `Steuer auf Lebensversicherung` [inherited: `kapitallebensversicherung.md`
  S16], establishing coverage of the subject area and nothing about this article
- Content: Finanztip is the German consumer publication that most consistently makes the
  ***Brutto*/*Zahlbeitrag* distinction the headline of its term-life advice** — the standing
  recommendation being to compare the *Bruttobeitrag* and not only the *Zahlbeitrag*, because the second
  is what you pay and the first what you can be made to pay. **The existence of that editorial line is
  asserted from knowledge; no figure, ranking or spread statistic is asserted** (gap 1).

### S16 — Stiftung Warentest / *Finanztest*, term-life comparison tests — **secondary**

- Doc type: periodic comparison test of RLV tariffs, paywalled with a free summary. URL: **not
  established**
- Content: the market's most influential comparison test for this product, and its design is why it
  matters here: *Finanztest* rates on the ***Zahlbeitrag* for defined model customers** — a stated age,
  sum insured, term and smoking status — **and separately reports the *Bruttobeitrag***, so a published
  test is the one German document type that would supply exactly the paired figures this file lacks.
  **No edition, date, model-customer definition or premium figure is asserted** (gap 1).

### S17 — Franke und Bornberg, MORGEN & MORGEN, ASSEKURATA — **secondary**

- Doc type: tariff ratings (`FB-Unternehmensrating`, `M&M Rating Risikoleben`), market studies,
  *Bedingungsanalysen*. URL: **not established** for any term-life rating. The sibling research located
  Assekurata's "24. Marktstudie *Überschussbeteiligungen und Garantien 2026*" and Franke und Bornberg
  commentary on *Basisinformationsblätter* [inherited: `kapitallebensversicherung.md` R25, R27],
  establishing that these houses publish in this field and nothing about their term-life work
- Content: the houses whose published criteria drive German RLV product design. Two are load-bearing for
  a representative specification and are asserted from market knowledge, **not from any document**: the
  ***Brutto*/*Zahlbeitrag* spread is itself a rated criterion** — a wide spread is marked down, because
  it measures the insurer's unilateral headroom to raise the billed premium; and the
  ***Nachversicherungsgarantie* event list, caps and age limit are rated criteria**, which is why the
  market has converged on a recognisable list (mechanic 8). Both `[unverified]`, and neither is used as
  a numeric parameter anywhere.

---
## Regulatory and actuarial references

**Retrieval status, revised.** The statutes below were read from the **canonical XML** each
instrument publishes at `gesetze-im-internet.de/<slug>/xml.zip`, which carries the law's `Stand`;
each entry now records the `Stand` it was read at. Sections read this way: **VVG** §§ 12, 19, 21, 22,
38, 150, 152, 153, 159, 161, 162, 163, 165, 166, 168, 169, 171 (Stand: zuletzt geändert durch Art. 12
G v. 26.5.2026 I Nr. 156); **MindZV** §§ 4, 6, 7, 8 (Art. 1 V v. 7.7.2020 I 1688); **DeckRV** §§ 1–5
(Art. 1 V v. 19.7.2024 I Nr. 250); **VAG** §§ 138, 140 (Art. 25 G v. 25.3.2026 I Nr. 81); **AGG**
§§ 19, 20, 33 (Art. 15 G v. 22.12.2023 I Nr. 414); **EStG** §§ 10, 20, 52 (Art. 7 G v. 29.6.2026 I
Nr. 197); **ErbStG** §§ 3, 15, 16, 19 (Art. 10 G v. 22.6.2026 I Nr. 192); **HGB** § 341f (Art. 4 G v.
4.2.2026 I Nr. 33); **VVG-InfoV** §§ 1, 2, 4 (Art. 13 G v. 26.5.2026 I Nr. 156). **VersStG 2021 § 4**
was read from its per-section HTML page, which serves text rather than a frameset.

Two things follow. First, the `.../<slug>/__<n>.html` addresses are kept as **human-facing links
only**: they answer 200 with a frameset of a few kilobytes and **no statutory text**, so a section
cited only through one of them is not retrieved. Second, where a rule is load-bearing the entry now
**quotes it exactly, in German**; everything else is still paraphrase, and what was not read is still
marked `[unverified]`. **Not retrieved and unchanged**: the RechVersV, the PRIIPs Regulation, the
Gender Directive and CJEU C-236/09 (the German implementation was read instead), the DAV papers'
substance (the files themselves are reachable), and every item at [R18]–[R20], [R22] and [R23].

### R1 — VVG § 161, *Selbsttötung*

- **Retrieved: yes** — canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30. Every clause below is confirmed verbatim. The one thing § 161 does **not** say is anything about increases: Abs. 1 runs the clock from *Abschluss des Versicherungsvertrags*, and the per-increment restart of gap 9 comes from the wordings [S1] [S3] [S4], not from the statute.
- Publisher: Bundesministerium der Justiz (Versicherungsvertragsgesetz 2008). URL:
  `https://www.gesetze-im-internet.de/vvg_2008/__161.html` — **returned by a search during the
  sibling research** [inherited: `kapitallebensversicherung.md` R4]
- **Inherited corroboration — the strongest single item in this file.** In an insurance **for the
  event of death** the insurer is ***leistungsfrei*** if the *versicherte Person* **intentionally
  takes her own life before three years have elapsed since conclusion of the contract**;
  **exception** where the act was committed **in a state excluding free determination of the will,
  caused by a *krankhafte Störung der Geistestätigkeit***; **the three-year period may be extended by
  individual agreement**, so it is a statutory minimum, extendable and by implication not
  shortenable; and **where the insurer is *leistungsfrei* it must nevertheless pay the
  *Rückkaufswert*, including *Überschussanteile*, under § 169**. Located in **Chapter 5** of the VVG.
- **Why it bites harder here than on an endowment.** On a *Kapitallebensversicherung* the
  substitution is soft — the *Rückkaufswert* after three years is a real sum. On a
  *Risikolebensversicherung* it is nil or nominal (mechanic 11), so the substitution is in economic
  substance **a forfeiture with a rounding error attached**. The model must carry the rule as a
  **benefit switch**, not as a decrement adjustment.
- Whether the three-year clock **restarts on an increase** of the sum insured, as the French one-year
  clock expressly does, is **not established from the statute**; German AVB practice is understood to
  restart it for the increment. `[unverified]` (gap 9).

### R2 — VVG § 169, *Rückkaufswert*

- **Retrieved: yes** — canonical XML, same Stand, read 2026-08-30. **Abs. 1's *gewiss* limitation is confirmed word for word** (gap 2). **But the inference that nothing is therefore ever paid is contradicted**: § 169 defines the *Rückkaufswert* and §§ 152 Abs. 2, 161 Abs. 3 and 165 Abs. 1 Satz 2 route a term contract to it; [S1] and [S4] pay it where the paid-up minimum fails, [S3] does not. Abs. 3's five-year spread and Abs. 5's *Abzug* test — including "Die Vereinbarung eines Abzugs für noch nicht getilgte Abschluss- und Vertriebskosten ist unwirksam" — are confirmed.

- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R2]
- **Inherited corroboration**: the section governs the surrender value payable on the policyholder's
  termination; **Abs. 3** provides the ***Mindestrückkaufswert***, computed on the basis that
  acquisition costs are spread over the **first five years**; the value is the *Deckungskapital*
  computed by recognised actuarial rules; a *Stornoabzug* may be deducted only where it is **agreed,
  reasonable and quantified in the contract** [inherited: `kapitallebensversicherung.md` R2, R22, R24].
- **The scope limitation that decides this product.** § 169 Abs. 1 confines the surrender-value duty
  to a life insurance whose insured event is **certain to occur** — the German formulation turns on
  whether the *Eintritt der Leistungspflicht* is *gewiss*. An endowment, an annuity and a
  whole-of-life cover satisfy it; **a *Risikolebensversicherung* does not**, because the insured may
  survive the term and the insurer may never owe anything. **The consequence is that no § 169 Abs. 1
  duty attaches to an RLV on *Kündigung*.** **That limitation is now read verbatim from the canonical
  XML and the tag is removed** (gap 2 closed). **What does not follow, and what this file wrongly
  said did, is that nothing is ever paid.** § 169 defines the *Rückkaufswert*; §§ 152 Abs. 2, 161
  Abs. 3 and 165 Abs. 1 Satz 2 route a term contract to it; and the market wordings pay it — [S1]
  § 13 Abs. 8 and [S4] § 13 convert the contract into a *beitragsfreie Versicherung* and pay the
  *Rückkaufswert*, less a *Stornoabzug*, where the paid-up sum fails a carrier-set minimum, only [S3]
  § 15 Abs. 10 paying nothing. **"Corroborated by uniform market practice" was wrong: the practice is
  not uniform.** The amount, however, is nil or nominal in all of them.

### R3 — VVG § 165, *Prämienfreie Versicherung* (*Beitragsfreistellung*)

- **Retrieved: yes** — canonical XML, same Stand, read 2026-08-30. **§ 165 carries no *gewiss* limitation of its own**, so the paid-up right is live on a term contract; Abs. 2 computes the paid-up benefit "unter Zugrundelegung des Rückkaufswertes nach § 169 Abs. 3 bis 5", which is where the *Stornoabzug* enters by reference. On the wordings the right is real on a constant sum insured (minimum 300 € at [S3], 2 500 € at [S4]) and impossible on a falling one, "kalkulationsbedingt kein Deckungskapital" [S3] § 15 Abs. 4.

- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R3]
- **Inherited corroboration**: the policyholder may **at any time, for the end of the current
  *Versicherungsperiode*, demand conversion into a *prämienfreie Versicherung***; the reduced benefit
  is computed by recognised actuarial rules; the insurer may make the same *Stornoabzug* as on
  surrender; and the right is subject to a **minimum-benefit test** — where the resulting
  *beitragsfreie Versicherungsleistung* would fall below an agreed minimum, the insurer pays the
  *Rückkaufswert* instead.
- **Effect here: the right exists in form and is empty in substance.** The *Deckungskapital* of a
  level-premium RLV is small and, after *Zillmerung*, zero or negative through much of the term
  (mechanic 10), so the paid-up sum fails the minimum test in most durations and the fallback is a
  payment of nil. Whether § 165 carries the same *gewiss* limitation as § 169 Abs. 1 was **not
  established** (gap 2); it makes no practical difference, both routes terminating in nil. What
  carriers offer instead — *Beitragsstundung*, a temporary *Ruhen*, a reduction of the sum insured —
  is `[unverified]` (gap 10).

### R4 — VVG §§ 19–22, *Vorvertragliche Anzeigepflicht* and *Anfechtung*

- **Retrieved: yes** for §§ 19, 21, 22 — canonical XML, same Stand, read 2026-08-30; § 20 was not read and is not relied on. The question-bounded duty ("nach denen der Versicherer in Textform gefragt hat"), the Abs. 5 warning requirement, § 21 Abs. 2's causation defence and § 21 Abs. 3's five/ten years are all confirmed. **Correction**: § 19 does not confer a right to accept on restricted terms — pre-contractual underwriting rests on freedom of contract; Abs. 4 Satz 2 gives the **retrospective** route after a breach. **Addition**: Abs. 6 gives a one-month termination right where such a change raises the premium by more than 10 %.

- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__19.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R5]; the `__20`, `__21`, `__22` forms
  are `[unverified]`
- **Inherited corroboration on § 19**: **Abs. 1 Satz 1** obliges the policyholder to disclose the
  *gefahrerhebliche Umstände* known to her **which the insurer has asked about in *Textform*** — **the
  duty is question-bounded**, with no free-standing duty to volunteer. The provision gives the insurer
  the right to put health questions and to decide whether to accept **with restrictions** or **only at
  an increased premium**. **Remedies**: on a breach the insurer may **adjust the contract
  retrospectively** — excluding the undisclosed risk, or raising the premium by a ***Risikozuschlag***
  — instead of refusing to perform, and for simple or gross negligence this is the usual outcome.
  **Time limits**: the adjust / terminate / rescind rights **lapse five years** after conclusion for
  negligent breach and **ten years** for **intentional or *arglistig*** breach.
- **Asserted, not inherited, and `[unverified]`**: that § 19 Abs. 5 conditions the remedies on the
  insurer having warned the applicant of the consequences in a separate *Textform* communication; that
  § 21 Abs. 2 defeats the remedy where the undisclosed circumstance caused neither the event nor the
  extent of the benefit; and that § 22 preserves ***Anfechtung wegen arglistiger Täuschung*** alongside
  them. On a term product these are the whole of the claims-risk story.

### R5 — VVG § 153, *Überschussbeteiligung*

- **Retrieved: yes** — canonical XML, same Stand, read 2026-08-30. Confirmed, with one new fact: exclusion of the *Überschussbeteiligung* requires an *ausdrückliche Vereinbarung* and "kann nur insgesamt" be done — an all-or-nothing switch, which is what `surplus_form = keine` implements. Both wordings open their surplus clause citing the section [S3] § 3, [S4] § 20 Abs. 1. **The *Bewertungsreserven* point is stronger than assumed**: on this product none arise at all, "daher entstehen dem Grunde nach keine Bewertungsreserven" [S3] § 3 Abs. 1 c.

- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R1]
- **Inherited corroboration**: the policyholder is **entitled to share in the surplus and in the
  *Bewertungsreserven***; participation may be excluded only by express agreement; the allocation must
  be ***verursachungsorientiert*** — attributed according to how the contract caused the surplus —
  under a procedure recognised by actuarial rules; **Abs. 3** governs the *Bewertungsreserven* share,
  allocated at least annually and payable on termination.
- **Why *verursachungsorientiert* is the load-bearing word here.** An RLV causes essentially **one**
  kind of surplus — the *Risikoüberschuss*. A cause-oriented allocation returns to the RLV book what
  the RLV book earned, and returns it as **a reduction of the premium**, there being no account to
  credit. German *Beitragsverrechnung* is § 153 operating on a product with no savings element
  (mechanic 5). Participation in *Bewertungsreserven* is **structurally negligible** here, because the
  attributable amount scales with a *Deckungsrückstellung* that is nil or nominal `[unverified]`.

### R6 — VVG § 163, *Prämien- und Leistungsänderung* (the *Treuhänder* clause)

- **Retrieved: yes** — canonical XML, same Stand, read 2026-08-30. **The entry's title was wrong**: the section is ***Prämien- und Leistungsänderung***. Abs. 1's three cumulative conditions turn on a change in the ***Leistungsbedarf***; Abs. 2 gives the policyholder a right to a benefit reduction instead; Abs. 4 drops the *Treuhänder* where supervisory approval is required. That the route is not used in practice on RLV *Bruttobeiträge* is still `[unverified]` — no retrieved document reports practice — but the premise is confirmed from the contract side: [S3] guarantees the *Bruttobeitrag* for the term and [S5] calls the *Tarifbeitrag* "der maximal zu leistende Versicherungsbeitrag".

- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` `[unverified]`. The sibling research
  recorded the section as governing premium and condition adjustment in life insurance and located
  market commentary on the *Treuhänderklausel* [inherited: `klassische_rentenversicherung.md` R3, R17,
  R18]
- The insurer may raise a life premium only on an **unforeseen and not merely temporary** change in
  the circumstances underlying the calculation, where the adjustment is necessary to safeguard
  permanent fulfilment, and where an **independent *Treuhänder*** confirms the bases; the policyholder
  may demand a corresponding benefit reduction instead.
- **The distinction that must not be blurred.** § 163 governs increases of the ***Bruttobeitrag***,
  and on a German RLV that route is essentially never used — the *Bruttobeitrag* is guaranteed for the
  term. What moves the customer's bill is the ***Überschussdeklaration***: cutting the
  *Beitragsverrechnung* raises the *Zahlbeitrag* toward the *Bruttobeitrag* with **no § 163 procedure,
  no *Treuhänder* and no policyholder remedy**, because no guaranteed term has changed. **This is the
  single most important legal fact about the German term-life premium** (mechanic 5). That § 163 is
  not used in practice on RLV *Bruttobeiträge* is `[unverified]`.

### R7 — VVG §§ 150, 159, 162 — *Versicherte Person*, *Bezugsberechtigung*, *Tötung durch Leistungsberechtigten*

- **Retrieved: yes** — canonical XML, same Stand, read 2026-08-30. § 150 Abs. 2's *schriftliche Einwilligung* above *gewöhnliche Beerdigungskosten* is confirmed verbatim, with an exception for *betriebliche Altersversorgung* and a special rule in Abs. 3 for a parent insuring a minor child. § 159 Abs. 2–3 fix when the beneficiary's right arises. **The entry's title for § 162 was wrong**: it is ***Tötung durch Leistungsberechtigten***; *Herbeiführung des Versicherungsfalles* is § 81.

- URLs: `.../vvg_2008/__150.html`, `__159.html`, `__162.html`, canonical forms, all `[unverified]`
- Asserted from knowledge, `[unverified]` throughout:
  - **§ 150** permits insurance on the life of another; where the benefit **exceeds ordinary funeral
    costs**, the ***schriftliche Einwilligung*** of that person is required. **This is the provision
    the *Über-Kreuz-Versicherung* runs on, and it also binds *verbundene Leben*** (mechanic 14).
  - **§ 159** governs the *Bezugsberechtigung*, revocable by default or ***unwiderruflich***; an
    irrevocable nomination vests the claim immediately and takes it out of the policyholder's
    disposal, with insolvency and tax consequences.
  - **§ 162** makes the insurer *leistungsfrei* where the **policyholder** intentionally and
    unlawfully brings about the death of the *versicherte Person*, and strips a **beneficiary** who
    does so of his entitlement.
- All three are structural on a product where *Versicherungsnehmer*, *versicherte Person* and
  *Bezugsberechtigter* are routinely three different people — the normal case here, not the exception.

### R8 — VVG § 152 (*Widerruf des Versicherungsnehmers*), § 166 (*Kündigung des Versicherers*), § 168 (*Kündigung des Versicherungsnehmers*)

- **Retrieved: yes** for §§ 12, 38, 152, 166, 168, 171 — canonical XML, same Stand, read 2026-08-30. **Two errors found.** § 166 is titled ***Kündigung des Versicherers*** and does not impose a demand procedure; it says only that the insurer's termination converts the contract into a *prämienfreie Versicherung*. The *Textform* demand is **§ 38 Abs. 1** and its minimum is **two weeks, not a month**. Confirmed: § 152 Abs. 1's 30 days; § 168 Abs. 1's termination at the end of the *Versicherungsperiode*, with § 12 making that period follow the *Zahlweise*; § 171's *halbzwingend* range. Worth recording: § 168 Abs. 2 confines the single-premium termination right to a *gewiss* risk. The carriers give more than the statute — termination "zum Ende des laufenden Monats" [S3] [S4].

- URLs: `.../vvg_2008/__152.html`, `__166.html`, `__168.html`, canonical forms, all `[unverified]`
- Asserted from knowledge, `[unverified]` throughout:
  - **§ 152** extends the general 14-day *Widerrufsfrist* of § 8 to **30 days** for life insurance.
  - **§ 166** governs non-payment of a *Folgeprämie* in life insurance, replacing the general § 38
    machinery: the *Zahlungsaufforderung* must be in *Textform*, must set a deadline of **at least one
    month** and must state the consequences; and the distinctive German step is that **the insurer's
    termination converts the contract into a *prämienfreie Versicherung*** rather than ending it —
    **unless** the paid-up benefit falls below the agreed minimum, when the contract ends.
  - **§ 168** gives the policyholder a right to terminate **at the end of each current
    *Versicherungsperiode*** on a running-premium contract; the period follows the *Zahlweise*, so a
    monthly-paying contract is terminable monthly.
- **Effect here.** § 166's paid-up conversion is the general German lapse path and on an RLV it
  **collapses into simple termination**, because the minimum test fails [R3]. A lapse is a pure exit:
  cover stops, nothing is paid, at most an unearned fraction of a prepaid premium is returned. So
  `claims_surr` is structurally zero, and § 168's period rule means exits are not concentrated at
  policy anniversaries.

### R9 — MindZV, *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*

- **Retrieved: yes** — canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688, read 2026-08-30. **§ 6 Abs. 1**, **§ 7**, **§ 8** carry the three percentages; gap 4 is closed and the section numbers may be cited. Each is floored at zero.

- URLs: `https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html` ·
  `https://www.buzer.de/gesetz/12013/a198221.htm` — both returned by a search during the sibling
  research [inherited: `kapitallebensversicherung.md` R6]
- **Inherited corroboration — the second load-bearing item in this file.** The minimum allocation to
  the *Rückstellung für Beitragsrückerstattung* is **90 % of the *Risikoergebnis*** attributable to
  *überschussberechtigte* contracts; **90 % of the *anzurechnende Kapitalerträge***, struck **after**
  deducting the *Aufwand für die Diskontierung der Deckungsrückstellung*, which is how the guaranteed
  interest is taken off the top before the policyholder's share; and **50 % of the *übriges
  Ergebnis***, which carries the expense result. An aggregate test combines the three, and the
  minimum is computed **separately for *Altbestand* and *Neubestand***.
- **Section attribution is not settled.** The sibling entry places the investment-result rule at § 6;
  the author's recollection places the investment result at § 4, the *Risikoergebnis* at § 5 and the
  *übriges Ergebnis* at § 6. **The three percentages are inherited and used; the section numbers are
  `[unverified]` and are cited nowhere in the delib library** (gap 4).
- **Why this regulation is the engine of the German term product.** An RLV has no meaningful
  investment result and a modest expense result; its technical outcome is almost entirely
  *Risikoergebnis*, and **90 % of that must go back to policyholders**. The insurer prices on a
  prudent first-order mortality basis, earns a large margin against a medically selected portfolio,
  and must return the overwhelming majority of it. *Beitragsverrechnung* is how it does so, and the
  width of the *Brutto*/*Zahlbeitrag* spread is to a first approximation **a direct function of how
  prudent the first-order basis is** (mechanic 5).

### R10 — DeckRV, *Deckungsrückstellungsverordnung* — *Höchstrechnungszins* and *Höchstzillmersatz*

- **Retrieved: yes** — canonical XML, Stand: zuletzt geändert durch Art. 1 V v. **19.7.2024** I Nr. 250, so the current rate is read at the instrument that set it; read 2026-08-30. § 2 Abs. 1 fixes the ***Höchstzinssatz*** at 1 %; § 4 Abs. 1 caps the *Zillmersatz* at "25 Promille der Summe aller Prämien" and applies to term business (gap 11, first half). **§ 5 Abs. 1 is new to this file and is load-bearing**: "Die Ableitung von Rechnungsgrundlagen auf der Basis eines besten Schätzwertes genügt nicht" — the statutory reason a *Sicherheitszuschlag* must exist. **A retrieved carrier prices its term tariff at a *Rechnungszins* of 0,25 %**, not at the ceiling [S3].

- URL: `https://www.buzer.de/gesetz/12006/index.htm` — returned by a search during the sibling
  research, which used it for the amendment history [inherited: `kapitallebensversicherung.md` R7]
- **Inherited corroboration**: the ***Höchstrechnungszins*** was raised **from 0,25 % to 1,00 % with
  effect from 1 January 2025**, three independent search results agreeing on the sequence **4 % in
  1994 → 0,25 % in 2022 → 1,00 % in 2025**, the 2025 move being the **first increase since 1994**. The
  ***Höchstzillmersatz*** may not exceed **25 ‰ of the *Beitragssumme***, cut **from 40 ‰** by the
  LVRG with effect from **1 January 2015**.
- **Effect here.** The *Rechnungszins* is close to irrelevant to an RLV — the *Deckungsrückstellung*
  is small and short-lived, so a 75-basis-point change moves the *Bruttobeitrag* very little. The
  *Höchstzillmersatz* is the opposite: 25 ‰ of the *Beitragssumme* of a term contract is a large
  number relative to that contract's tiny reserve, and it is why a *gezillmerte*
  *Risikolebensversicherung*'s *Deckungskapital* is **negative or nil for much of its term** (mechanic
  10). Whether the cap applies to a term product in the same way as to a savings contract was **not
  established** `[unverified]` (gap 11).

### R11 — VAG §§ 138–140 — *Gleichbehandlung*, *Überschussbeteiligung*, RfB

- **Retrieved: yes** for §§ 138 and 140 — canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81, read 2026-08-30; § 139 was not re-read. § 138 Abs. 2 in full: "Bei gleichen Voraussetzungen dürfen Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden." **The unit of "gleiche Voraussetzungen" is now known**: the *Bestandsgruppe* and, inside it, the *Gewinnverband* [S1] § 2 Abs. 2–3 — [S3] names *Bestandsgruppe 112*, [S4] *Bestandsgruppe G*. § 140 Abs. 1 confirms the RfB use restriction, which both wordings reproduce.

- URL: `https://dejure.org/gesetze/VAG/139.html` — returned by a search during the sibling research
  [inherited: `kapitallebensversicherung.md` R8]; the § 138 and § 140 forms are `[unverified]`
- **Inherited corroboration on § 139**: policyholders are **in principle to share in the
  *Bewertungsreserven* to the extent of one half**; participation by **exiting** policyholders is
  permitted **only to the extent that the *Bewertungsreserven* exceed the *Sicherungsbedarf*** arising
  from contracts with an interest guarantee; and *Sicherungsbedarf* is the sum, over contracts with an
  *überhöhter Rechnungszins*, of the actuarially valued interest obligation less the
  *Deckungsrückstellung*.
- **Asserted and `[unverified]`**: that § 138 imposes the ***Gleichbehandlungsgrundsatz*** — equal
  treatment of policyholders in equal circumstances in premium-setting and surplus allocation — and
  that § 140 governs the RfB, including withdrawals from it.
- **Effect here.** § 139's *Bewertungsreserven* mechanics are economically empty on this product
  [R5]. **§ 138 is the one that binds**: it is why an insurer declares **one *Beitragsverrechnung*
  rate per tariff generation and rating cell** rather than negotiating individual discounts, and
  therefore why the *Zahlbeitrag* can be modelled as a deterministic function of the *Bruttobeitrag*
  and a declared rate.

### R12 — DAV, "Herleitung der Sterbetafel DAV 2008 T für Lebensversicherungen mit Todesfallcharakter"

- **Retrieved: no**, on this file's own bar — all four addresses are live and were opened on 2026-08-30 (landing page ~53 kB; `20080708_DAV_2008_T.pdf` 1,09 MB; `2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf` 1,14 MB; `..._R_NR.pdf` 1,67 MB), **but their text was not read**, so everything below remains inherited corroboration. Reading them would close gaps 6 and 12. **One carrier-side corroboration is new**: [S3]'s AVB states its bases as "einer unternehmenseigenen Sterbetafel **auf Basis der DAV 2008T**", and DeckRV § 5 Abs. 1 now supplies the legal reason a *Sicherheitszuschlag* must exist [R10].


- Publisher: Deutsche Aktuarvereinigung e. V. Doc type: *DAV-Richtlinie* / *Fachgrundsatz*, with a
  2008 derivation paper and a 2022 restatement. URLs, all returned by a search during the sibling
  research [inherited: `kapitallebensversicherung.md` R14]:
  `https://aktuar.de/de/wissen/fachinformationen/detail/herleitung-der-sterbetafel-dav-2008-t-fuer-lebensversicherungen-mit-todesfallcharakter/` ·
  `https://aktuar.de/content/PDF/Fachwissen/20080708_DAV_2008_T.pdf` ·
  `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf` ·
  `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T_R_NR.pdf`
- **Inherited corroboration — the third load-bearing item, and *the* table for this product**:
  - The DAV *Arbeitsgruppe Biometrische Rechnungsgrundlagen* investigated mortality in life insurance
    **with *Todesfallcharakter*** over **2006 to 2008**, using **German insurers' own policy data**
    with **German population statistics**, compared against international developments.
  - After cleansing, the insured data covered **60 % of the German market in the
    *Kapitallebensversicherung* segment**; **the term-assurance figure was truncated in the search
    summary and is not established** (gap 12).
  - The *Richtlinie* **regulates the methodology for deriving mortality tables for reserving and the
    procedure for setting the *Sicherheitszuschläge***.
  - ***DAV 2008 T R*** and ***DAV 2008 T NR*** — smoker and non-smoker — are in principle **also
    suitable for premium calculation** differentiated by smoking status, **but not for policies
    written without a *Gesundheitsprüfung***.
  - **First adopted as a DAV-Richtlinie on 4 December 2008**; restated as a *Fachgrundsatz* dated
    **29 November 2022**. **The table values are not public and delib does not redistribute them.**
- **What this establishes for the model**: (i) the German first-order basis for a term product is
  DAV 2008 T with its smoker/non-smoker variants; (ii) the *Sicherheitszuschlag* is **part of the
  table's construction**, so first-order and second-order are two levels of one DAV framework and the
  model must publish both; (iii) the smoker split is **actuarially sanctioned for pricing**, which is
  why the market rates on it; (iv) it is **not** available without medical underwriting, which is why
  simplified-issue German death covers are aggregate-rated. **The magnitude of the loading was not
  established and is `[std]` here** (mechanic 15, gap 6).

### R13 — Unisex pricing: the EU Gender Directive, CJEU C-236/09 (*Test-Achats*), AGG § 20

- **Retrieved: yes** for the German implementation, AGG §§ 19, 20, 33 — canonical XML, Stand: zuletzt geändert durch Art. 15 G v. 22.12.2023 I Nr. 414, read 2026-08-30. **§ 33 Abs. 5 fixes the date in the German statute**: the derogation survives only for "Versicherungsverhältnisse, die **vor dem 21. Dezember 2012** begründet werden". § 20 Abs. 2 preserves a risk-adequate-calculation justification for religion, disability, age and sexual identity — **sex is absent from the list**. The Directive and CJEU C-236/09 were **not** retrieved; nothing is asserted from either.
- Publisher: Court of Justice of the European Union; Bundesministerium der Justiz. URL: **not
  established** for any of them
- Asserted from knowledge, `[unverified]` except the date: the judgment struck down the derogation
  permitting sex-differentiated insurance premiums with effect for contracts concluded **from
  21 December 2012**; German implementation runs through the amendment of **§ 20 AGG**. The frlib
  research reached the same cut-off independently from the French implementing article, which
  preserves the derogation only for contracts concluded "au plus tard le 20 décembre 2012"
  [`frlib` R10] — the closest thing to corroboration this entry has.
- **Effect here, larger than on any other delib product.** Female mortality at the ages a term
  contract is sold — 25 to 55 — is roughly **half** male mortality `[unverified]`, so a unisex tariff
  is a blend whose position depends entirely on the **assumed sex mix of the tariff's own new
  business**, a proprietary and periodically re-estimated number. **The DAV 2008 T variants are
  sex-distinct** [R12], so every German RLV tariff written since 2013 uses a **carrier-chosen mixing
  ratio that no source discloses**. The delib model carries a `[std]` 50/50 blend, and this is one of
  the largest single sources of unexplained spread between German carriers' rates.

### R14 — EStG § 20 Abs. 1 Nr. 6 and § 10 Abs. 1 Nr. 3a — income tax on the benefit, deductibility of the premium

- **Retrieved: yes** — canonical XML, Stand: neugefasst durch Bek. v. 8.10.2009 I 3366, 3862, zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30. Gaps 16 and 17 both close; see the register.

- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — returned by a search during the sibling
  research [inherited: `kapitallebensversicherung.md` R10]
- **Inherited corroboration**: § 20 Abs. 1 Nr. 6 taxes the ***Unterschiedsbetrag*** between the
  benefit and the premiums paid on a life insurance as investment income; the **half-income treatment
  (*Halbeinkünfteverfahren*)** applies where the contract has run at least **twelve years** and the
  benefit is paid after the policyholder's **62nd** birthday; a **BMF-Schreiben of 1 October 2009,
  IV C 1 - S 2252/07/0001** is the administrative guidance; and for contracts concluded from **1 April
  2009** a ***Mindesttodesfallschutz*** of **50 %** of the *Beitragssumme* is required for the
  favourable treatment [inherited: `kapitallebensversicherung.md` R10, R11, R12].
- **Why it matters that this section does *not* apply.** § 20 Abs. 1 Nr. 6 taxes the *Erlebensfall* —
  maturity or surrender — because that is where an *Unterschiedsbetrag* can arise. **A pure death
  benefit paid to a third party is not investment income of the policyholder and is not caught**, so
  the *Todesfallleistung* of an RLV is **free of Einkommensteuer** and the tax question moves entirely
  to the *Erbschaftsteuer* [R15]. The non-application is asserted and `[unverified]` (gap 16), though
  corroborated indirectly by the *Mindesttodesfallschutz* rule itself, which exists precisely to stop
  savings contracts dressing themselves as death covers to reach this section.
- ***Sonderausgaben***: RLV premiums fall among the *sonstige Vorsorgeaufwendungen* deductible under
  § 10 Abs. 1 Nr. 3a EStG, **within an annual ceiling in practice already exhausted by health and
  long-term-care contributions**, so the effective deduction for most taxpayers is **nil**. Both
  statements `[unverified]`; **no ceiling figure is stated in this file** (gap 17).

### R15 — ErbStG §§ 3, 15, 16, 19 — the *Erbschaftsteuer* treatment of the death benefit

- **Retrieved: yes** — canonical XML, Stand: neugefasst durch Bek. v. 27.2.1997 I 378, zuletzt geändert durch Art. 10 G v. 22.6.2026 I Nr. 192, read 2026-08-30. Gap 18 closes and every figure in it was right; see the register.

- URL: `https://www.gesetze-im-internet.de/erbstg_1974/` `[unverified]`; per-section forms **not
  established**
- Asserted from knowledge, `[unverified]` throughout:
  - **§ 3 Abs. 1 Nr. 4** brings within ***Erwerb von Todes wegen*** every asset acquired by a third
    party on the death of the deceased **by virtue of a contract concluded by the deceased**. A
    *Todesfallleistung* paid to a *Bezugsberechtigter* under a policy the deceased took out **on his
    own life and paid for himself** is the textbook case, and is **subject to *Erbschaftsteuer***.
  - **§ 15** sorts beneficiaries into three *Steuerklassen*: I (spouse, registered partner, children,
    grandchildren, parents on death), II (siblings, nieces and nephews, in-laws, divorced spouse),
    III (**everyone else, including an unmarried partner**).
  - **§ 16** sets the *Freibeträge*: **500,000 EUR** spouse or registered partner, **400,000 EUR** per
    child, **200,000 EUR** per grandchild, **100,000 EUR** parents and grandparents on a death
    acquisition, **20,000 EUR** in classes II and III. **Every figure is `[unverified]`** and is
    carried downstream as a `[std]` illustration (gap 18).
  - **§ 19** sets banded rates by class, beginning at **7 %** in class I and **30 %** in class III.
    `[unverified]`.
- **The arithmetic that drives German term-life contracting.** On the representative sum insured,
  **300 000 €**: paid to a **spouse**, the 500 000 € allowance absorbs it and the tax is nil; paid to
  an **unmarried partner**, the allowance is 20 000 €, the taxable acquisition 280 000 €, class III
  applies from 30 %, and the liability is on the order of **84 000 € — 28 % of the sum insured**. That
  comparison is why the *Über-Kreuz-Versicherung* exists (mechanic 14) and why a German term-life
  specification must document a contracting structure alongside the cash flows. **The arithmetic is
  arithmetic; its inputs are `[unverified]`.**

### R16 — VersStG 2021 § 4 Abs. 1 Nr. 5 — *Versicherungsteuer* exemption for life insurance

- **Retrieved: yes** — HTML, ~12 kB, read 2026-08-30. `versstg`, not `verststg`; the law is cited as **VersStG 2021** and the exempting limb is **§ 4 Abs. 1 Nr. 5 Buchst. a**. Gap 19 closes.

- URL: `https://www.gesetze-im-internet.de/verststg_1996/__4.html` `[unverified]`
- Asserted and `[unverified]`: the *Versicherungsteuer* — at a general rate of 19 % for most non-life
  lines — **does not apply to life insurance**, so a German RLV premium is billed **without insurance
  premium tax**, unlike a French *cotisation* quoted "TTC". The model carries **no premium-tax line**,
  recorded here so a reader does not conclude it was forgotten (gap 19).

### R17 — VVG-InfoV, and the PRIIP boundary for a pure protection product

- **Retrieved: yes** — canonical XML, Stand: zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156, read 2026-08-30. **Two claims confirmed and one overturned.** § 2 Abs. 1 Nr. 9 confines the *Effektivkosten* duty to a contract "bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist" — the same test as § 169 Abs. 1 — and § 4 Abs. 3 disapplies the *Informationsblatt* regime for PRIIPs. **But § 2 Abs. 1 Nr. 1 with Abs. 2, and § 4 Abs. 2 Satz 2, require the acquisition and administration costs to be disclosed to the applicant in euro**, so the charge levels are not "structurally undisclosed" (gap 8). The PRIIPs Regulation itself was **not** retrieved, so the exclusion of death-only contracts from its scope remains `[unverified]`.

- URL: `https://www.gesetze-im-internet.de/vvg-infov/` `[unverified]`. The sibling research recorded
  § 2 VVG-InfoV as the source of the pre-contractual information duties and of the *Effektivkosten*
  disclosure [inherited: `kapitallebensversicherung.md` R9]
- **The boundary this product sits on, asserted and `[unverified]`.** A ***Basisinformationsblatt***
  (PRIIP-KID) is required for a **packaged retail investment product** — one whose return is exposed
  to the performance of reference values or assets. A **pure *Risikolebensversicherung* has no
  investment component and is therefore not a PRIIP**, so none is produced for it; the applicable
  pre-contractual summary is the ***Produktinformationsblatt*** under the VVG-InfoV [S2].
- **Two consequences for delib.** (i) The brief's expectation of finding *Basisinformationsblätter*
  for this product is misplaced, and the gaps register records that rather than pretending the
  documents were merely unreachable. (ii) There is **no *Effektivkosten* figure for a term product**,
  because a reduction in yield presupposes a yield. **The absence of a published cost ratio is
  structural, not a research failure**, and it is a large part of why German term-life charge levels
  are invisible (gap 8).

### R18 — GDV, *Die deutsche Lebensversicherung in Zahlen* and the *Risikoversicherung* statistics

- URL: **not established** for the term-assurance breakdown. The sibling research located the GDV
  statistics landing page and the ten-year *Neugeschäft und Bestand* series [inherited:
  `kapitallebensversicherung.md` R20, R21]
- **Inherited corroboration**: the GDV publishes an annual statistical volume and a ten-year series
  broken down by product family; from it the sibling research took a whole-market ***Stornoquote* of
  2,72 % for 2024 and 2,56 % for 2023** on the main GDV measure — counting contracts terminated early,
  surrendered or made *beitragsfrei* as a percentage of the *Bestand* — and a second measure of
  **1,2 % for 2024** counting contracts and covering surrenders and other early terminations. **The
  two are not reconcilable from the evidence and both are recorded.**
- **What is *not* established is the whole of what this product needed**: the size of the German
  *Risikoversicherung* segment — contracts in force, new business, premium income, aggregate
  *versicherte Summe*, average sum insured, average premium — and any segment-specific lapse rate
  (gap 13). The whole-market *Stornoquote* is **deliberately not used** as a term-life assumption: a
  term contract's lapse is dominated by its first three durations and by the absence of any surrender
  value to lose, both of which push it above a book average weighted by long-dated savings contracts.

### R19 — BaFin supervisory material on life insurance conduct and product governance

- URL: **not established** for any term-life-specific item. The sibling research located BaFin's
  **Merkblatt 01/2023 (VA)** *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden
  Lebensversicherungsprodukten*, published **May 2023**, and the *Risiken im Fokus 2026* item on the
  cost of *kapitalbildende* products [inherited: `kapitallebensversicherung.md` R17, R18]
- **Inherited corroboration and its limit**: the *Merkblatt*'s subject is expressly
  ***kapitalbildende*** life products, and its concern is that costs be justified by customer value.
  **A pure *Risikolebensversicherung* is outside its stated subject matter.** Recorded so that a
  reader does not import an endowment-conduct standard into a term product; supervisory literature
  specific to German term assurance was **not located** (gap 14).

### R20 — Rating and analysis houses on German term-life tariff design

- Publisher: Franke und Bornberg; MORGEN & MORGEN; ASSEKURATA — the same corpus as S17, seen from the
  product side. URL: **not established**
- The reference class for two market-design facts no statute supplies: that the
  ***Brutto*/*Zahlbeitrag* spread is a rated criterion**, and that the ***Nachversicherungsgarantie*
  event list, caps and age limits are rated criteria**. Both `[unverified]` [S17]. **No rating,
  criterion weight or observed distribution is asserted.**

### R21 — HGB § 341f and RechVersV — statutory reserving for a term contract

- **Retrieved: yes** for HGB § 341f — canonical XML, Stand: zuletzt geändert durch Art. 4 G v. 4.2.2026 I Nr. 33, read 2026-08-30; the RechVersV was **not** read. **The entry over-attributed to § 341f**: Abs. 1 requires the prospective method and Abs. 2 the interest-guarantee test, and that is all. The premium bases with a prudent margin are DeckRV § 5 Abs. 1 [R10]; the administration-cost provision where the premium term is shorter than the cover term belongs to the RechVersV and stays `[unverified]`. [S4] gives the carrier-side chain: § 88 VAG and §§ 341e, 341f HGB with the regulations under them.

- URL: `https://www.gesetze-im-internet.de/hgb/__341f.html` `[unverified]`
- Asserted and `[unverified]`: § 341f requires the *Deckungsrückstellung* to be computed prospectively
  on the bases used to determine the premium, with a prudent margin, including a provision for future
  administration costs where the premium-paying period is shorter than the cover period; the RechVersV
  governs presentation. Whether a **negative** individual *Deckungsrückstellung* arising from
  *Zillmerung* must be floored at zero — the *Nullstellung* question — was **not established**, and it
  matters here because a *gezillmert* term contract sits below zero for a long stretch (gap 11).
- The delib posture, stated once in every product: **the models publish gross best-estimate-style
  liability cash flows, undiscounted. Discounting, the *Deckungsrückstellung*, Solvency II technical
  provisions and the SCR are referenced, never specified.** R21 is a pointer, not a model input.

### R22 — Solvency II and the German prudential layer

- Publisher: EIOPA; BaFin. URL: **not established.** A pointer only, on the same posture as R21: nothing
  product-specific for German term assurance was located, and **no capital, risk-margin or stress figure
  appears anywhere in the delib `risikolebensversicherung` documents.**

### R23 — German case law on *vorvertragliche Anzeigepflicht* and *Selbsttötung* in life insurance

- Publisher: Bundesgerichtshof and the *Oberlandesgerichte*. URL: **not established.** **No decision is
  cited by date or file number anywhere in this file, and none is invented**
- A known reference class, not a source. German term-life litigation clusters on two questions: whether
  the applicant's answers to the *Gesundheitsfragen* were complete and whether the insurer complied with
  the § 19 Abs. 5 warning requirement [R4]; and whether a *Selbsttötung* inside the three-year window
  was committed in a state excluding free will [R1]. The sibling research located BGH authority on
  adjacent life-insurance questions — the *Stornoabzug* *Bezifferung* requirement and the
  *Bewertungsreserven* judgment of **20 January 2021, IV ZR 318/19** [inherited:
  `kapitallebensversicherung.md` R22, R23] — establishing that the court decides this area regularly and
  nothing about term assurance. **No holding is asserted** (gap 20).

---
## Extracted facts, organised by mechanic

This is the section the `product-spec.md` and `technical-notes.md` are written from. It carries the
weight of the file, because it is the part that does not depend on having a PDF open. Every claim
carries an `[S#]` or `[R#]` tag, an inherited-corroboration note, `[unverified]`, or `[std]`.

### 1. Product structure and legal form

- A German *Risikolebensversicherung* is a **life insurance contract under Chapter 5 of the VVG**
  (*Lebensversicherung*, §§ 150–171), not accident or health business, even though it pays only on
  death. Every general life provision of that chapter applies unmodified — the 30-day *Widerrufsfrist*
  of § 152, the *Anzeigepflicht* of § 19, the *Selbsttötung* rule of § 161, the *Bezugsberechtigung* of
  § 159 [R1] [R4] [R7] [R8].
- It is **individual business** (*Einzelversicherung*) in delib scope: one contract, one
  *Versicherungsnehmer*, one or two *versicherte Personen*.
- **Three roles, routinely three different people.** The *Versicherungsnehmer* owns and pays; the
  *versicherte Person* is the life at risk; the *Bezugsberechtigter* receives the benefit. On a savings
  product these collapse into one or two people; on a term product they systematically do not, and
  **the tax outcome depends on which of them is which** [R7] [R15] (mechanic 14). Where the policyholder
  insures **another** life and the benefit exceeds ordinary funeral costs, that person's
  ***schriftliche Einwilligung*** is required [R7] `[unverified]` — the foundation of every *verbundene
  Leben* and *Über-Kreuz* arrangement.
- The product is ***überschussberechtigt*** as a matter of course, and the participation is the
  mechanism through which the customer's bill is set (mechanic 5) [R5] [R9] [S5]. A non-participating
  German term tariff is possible in law (§ 153 permits exclusion by express agreement [R5]) and is
  **not the market form**; none was located `[unverified]`.
- The documents delivered are the ***Allgemeine Versicherungsbedingungen***, the
  ***Verbraucherinformation*** pack and the ***Produktinformationsblatt*** [S2] [R17]. There is **no
  *Basisinformationsblatt***: a pure protection contract has no investment component and is not a PRIIP
  [R17] `[unverified]`. That is a **structural absence, not a missing document**.

### 2. The benefit

- **One benefit, one event.** The insurer pays the ***Versicherungssumme*** as a *Todesfallleistung* if
  the *versicherte Person* dies within the *Versicherungsdauer*; if she survives it, **nothing is paid
  and the contract simply ends** [R1] [R2] [S5] [S15]. No *Erlebensfallleistung*, no maturity value, no
  return of premium, no conversion right into a savings contract in the base design.
- The benefit is a **lump sum** paid to the *Bezugsberechtigter* directly and not through the estate
  where the nomination is effective [R7] — so the beneficiary is paid without waiting for probate and
  the sum is beyond the estate's creditors in the ordinary case `[unverified]`.
- Death **from any cause**, accident or illness alike, subject only to the short exclusion list of
  mechanic 13. **There is no *Wartezeit*** on a medically underwritten German RLV: cover attaches from
  the agreed *Versicherungsbeginn*, and the insurer's protection against anti-selection is the
  *Gesundheitsprüfung*, not a deferral of cover `[unverified]`. That contrasts with the German
  *Sterbegeldversicherung*, written without underwriting and therefore carrying a *Wartezeit*, and with
  France, where two of the eight carriers in the frlib corpus impose a *délai d'attente* of 3 or 12
  months where medical formalities are waived [`frlib` S6, S9].
- **No living benefits in the base design.** Options are bolted on (mechanic 8), but **there is no
  German equivalent of the French *PTIA* acceleration**, present in seven of eight French standalone
  contracts [`frlib` S1–S8]. **That absence is the second-largest structural difference between the
  German and French term products**, and it simplifies the model: one decrement, one benefit, no
  interlock to get wrong.

### 3. *Versicherungssumme* shapes

Three shapes are standard, and a German tariff normally offers all three on the same underwriting and
the same *Rechnungsgrundlagen*. All are `[unverified]` as to any carrier, asserted from market
knowledge, and structural rather than numeric.

- ***Konstante Versicherungssumme*** — the same sum throughout. The default and the majority form, used
  for family protection, where the need does not amortise.
- ***Linear fallende Versicherungssumme*** — the sum falls by a **fixed amount each year**, normally
  reaching zero or a stated residual at expiry. Cheap and simple, and a poor match to an annuity loan,
  whose balance falls slowly at first and quickly at the end while a linear schedule does the opposite.
- ***Annuitätisch fallende Versicherungssumme*** — the sum follows the **outstanding balance of an
  annuity loan** at a nominal rate agreed at issue. The *Darlehensabsicherung* form. The agreed rate is
  a **contractual schedule parameter, not the borrower's actual loan rate**: it is fixed at issue and
  does not follow the loan if it is refinanced, repaid early or rolled onto a new fixed rate. **No
  specific rate is asserted** (gap 15).
- **All three are one mechanic**: a schedule `S(t) = S(0) × f(t)` with `f(0) = 1`, driven by an external
  table — `f(t) = 1` constant, `f(t) = 1 − t/n` linear, and the outstanding-balance factor of an
  `n`-year annuity for the third. **A model that hard-codes a constant sum insured cannot represent two
  of the three shapes the German market actually sells**, which is why the delib model carries the
  schedule as a first-class input. Carriers price the falling shapes lower for the same initial sum
  **mechanically, not as a discount**; the model computes the reduction from the schedule. A fourth,
  **rising** shape is a different mechanic — the ***Dynamik*** (mechanic 8).

### 4. The premium: a level *Bruttobeitrag*, and three unrelated meanings of "netto"

- **The German term-life premium is level over the whole *Beitragszahlungsdauer***, struck at issue from
  the entry age and held there; it does **not** step up with attained age. This is the largest
  structural difference from the French *temporaire décès*, where every carrier in the frlib corpus
  whose basis is stated prices on an **annually revisable attained-age** basis and none prices level
  [`frlib` S1, S2, S3, S6, S7, S9, S10 and gap 1]. The German contract is the one an Anglo-American
  reader expects; the French one is not. Universality is `[unverified]` at carrier level but follows
  from the existence of a guaranteed *Bruttobeitrag* [R6] and from the *Zillmerung* regime [R10],
  neither of which makes sense on an annually repriced contract. An ***abgekürzte
  Beitragszahlungsdauer*** — premiums stopping before cover does — is offered by some tariffs
  `[unverified]`.
- **Three unrelated things are called "netto", and confusing them is the classic implementation error.**

| Term as used | Means | Where it appears |
|---|---|---|
| *Nettoprämie* / *Nettobeitrag* (**actuarial**) | The risk premium from the mortality and interest bases, **before** expense loadings; the *Bruttobeitrag* is this plus α, β and γ | Actuarial texts, DAV material, the sibling delib glossary |
| *Nettobeitrag* / *Zahlbeitrag* (**consumer**) | The premium billed = *Bruttobeitrag* **less** the *Beitragsverrechnung*. **The market's dominant usage for this product** | Insurer pages, *Produktinformationsblätter*, portals, consumer press [S5] [S14] [S15] [S16] |
| *Nettotarif* / *Honorartarif* (**distribution**) | A **commission-free** tariff sold through fee-based advice, the *Abschlussprovision* stripped out and charged as a fee | Broker and fee-adviser market `[unverified]` |

  The delib documents use ***Zahlbeitrag*** for the consumer sense throughout and reserve
  ***Nettoprämie*** for the actuarial sense, and say so once in each document. **The bare word
  "*Nettobeitrag*" is never used as a delib parameter name.**

### 5. *Bruttobeitrag* → *Zahlbeitrag*: the *Überschussbeteiligung* as *Beitragsverrechnung*

**This is the central mechanic of the German term product and the one an implementation gets wrong.**

- **The tariff premium is the *Bruttobeitrag*.** Computed on **first-order *Rechnungsgrundlagen*** — a
  prudent mortality table with *Sicherheitszuschläge* [R12], the *Rechnungszins* [R10] and the expense
  loadings — it is **what the contract guarantees**: the maximum the policyholder can ever be required
  to pay, unchanged over the term [R6].
- **The customer is billed the *Zahlbeitrag*.** The insurer declares an *Überschussanteil* and applies
  it as ***Beitragsverrechnung*** — netting it against the *Bruttobeitrag* before billing rather than
  crediting it to an account; also marketed as *Sofortverrechnung* or *Sofortrabatt*. So

  ```
  Zahlbeitrag(t) = Bruttobeitrag × (1 − v(t)),   0 ≤ v(t) < 1
  ```

  with `v(t)` the declared *Beitragsverrechnungssatz* for the year. The mechanic is corroborated in kind
  by a carrier's own guide page dedicated to the *Überschussbeteiligung* of this product [S5] and
  follows from § 153 VVG's requirement of a *verursachungsorientiert* allocation on a product with no
  reserve to credit [R5]. **The form and the name are asserted; no value of `v` is asserted anywhere in
  this file** (gap 1).
- **Only the *Bruttobeitrag* is guaranteed; the insurer may raise the *Zahlbeitrag* up to it.** The
  *Überschussbeteiligung* is declared **annually** and is not guaranteed for the future, and § 153 VVG
  confers an entitlement to *participate*, not to a level [R5]. A reduction of `v` raises the billed
  premium **without any § 163 procedure, without a *Treuhänder* and without a policyholder right of
  objection**, because no guaranteed term has moved [R6]. **This asymmetry is why the German market
  publishes both numbers, and why the spread is a rated criterion** [S17] [R20].
- **Why the spread is wide.** An RLV's technical result is almost entirely *Risikoergebnis*, and the
  MindZV obliges the insurer to allocate at least **90 %** of it to policyholders [R9]. So: the insurer
  prices on `q1 = (1 + m) · q2`, with `q2` the best estimate for a medically selected portfolio and `m`
  the aggregate *Sicherheitszuschlag* [R12]; actual claims run at roughly `q2`, giving a margin of
  `m/(1 + m)` of the *Bruttobeitrag*'s risk element; and **at least 90 % of that margin must go back**,
  with *Beitragsverrechnung* the only route available on a product with no account to credit. **A wide
  spread is therefore evidence of a prudent first-order basis, not of a generous insurer**, and a narrow
  one of a basis struck close to expected experience. Both readings are structurally sound and
  **neither is a quality judgement** — the nuance the consumer press tends to lose [S15] [S17].
- **The counter-intuitive consequence, and the most useful single result in this file.** Because 90 % of
  the extra margin is returned, **raising the prudence of the first-order basis moves the *Bruttobeitrag*
  a great deal and the *Zahlbeitrag* hardly at all.** Working the `[std]` calibration of mechanic 16
  through three levels of `m` at entry age 35, sum 300 000 €, 25-year term:

| Sicherheitszuschlag `m` | First-order / best-estimate | Bruttobeitrag p.a. | Zahlbeitrag p.a. | Zahl / Brutto |
|---|---|---|---|---|
| 1.00 | 2.00 | 1,180 EUR | 730 EUR | 0.62 |
| 1.25 | 2.25 | 1,316 EUR | 753 EUR | 0.57 |
| 1.50 | 2.50 | 1,451 EUR | 775 EUR | 0.53 |

  The *Bruttobeitrag* moves by **23 %** across that range; the *Zahlbeitrag* by **6 %**. All six figures
  are **[std]** constructions and are **not market observations**; the result they demonstrate is not a
  construction — it follows from the MindZV 90 % rule [R9], and it is why two German carriers can quote
  nearly identical *Zahlbeiträge* on very different *Bruttobeiträge*.
- **Modelling ruling.** The delib model **derives** the *Zahlbeitrag* from the first-order premium and
  the MindZV allocation rather than treating `v` as a free input, so the *Beitragsverrechnungssatz* is an
  **output of the surplus mechanic** — which is what it is in the real product. The model publishes
  **both premium streams**: a guaranteed `prem_gross` and a billed `prem_paid`, with `net_cf` built from
  the billed one and the guaranteed one available as the stress. **A model carrying only one premium
  stream cannot represent this product.**
- **The observed range of `Zahl / Brutto` across the German market could not be established** (gap 1).
  What can be said: it is **below 1 for essentially every participating tariff**; it is **wider in the
  direct channel than the tied-agent channel**, because less of the *Bruttobeitrag* is committed to
  acquisition costs [S3] [S12]; and a few tariffs are marketed on a deliberately **narrow** spread as a
  selling point [S17]. The representative design uses the derived **0.57**, tagged **[std]**.
  **One observation now exists against it**: a direct writer's published model case gives
  **0,450**, the same to three decimals across two tariffs and two editions [S2] — at the bottom of the
  argued 0,45–1,00 range, and wider than this design produces. **The design is unchanged**: one model
  case is not a market, and recalibrating would move the worked example and its golden tests.

### 6. Other *Überschussverwendung* forms

Four forms are used in the German market for a death-benefit contract. **Correction:** an earlier draft
attributed a four-component surplus vocabulary — *Zins-*, *Risiko-*, *Kosten-* und *übrige Überschüsse*
— to the carrier page at [S5]. The page uses no such vocabulary; it names **three** sources, as do
MindZV §§ 6–8 [R9] and all three retrieved wordings [S1] [S3] [S4]. **What [S5] does establish** is
that the German term market runs on two of the four forms below: "meist eines von zwei Modellen ... den
**Todesfallbonus** und den **Sofortrabatt**" — and every retrieved wording carries exactly that pair,
*Sofortrabatt* while premiums are paid and *Todesfallbonus* once paid up [S3] § 3 Abs. 2 b and d, [S4]
§ 20 Abs. 3 b. Prevalence beyond that pair is `[unverified]`.

| Form | Mechanic | Effect on the model |
|---|---|---|
| ***Beitragsverrechnung*** | Surplus netted against the *Bruttobeitrag*; the customer pays less | Reduces `prem_paid`; sum unchanged. **The base design** |
| ***Summenzuwachs*** / *Bonussumme* | Surplus buys additional **paid-up death cover**; the sum grows year by year | Raises the benefit; premium unchanged |
| ***Verzinsliche Ansammlung*** | Surplus accumulates with interest and is paid **in addition** on death | Creates an account value on a product that otherwise has none |
| ***Todesfallbonus*** | A declared bonus sum payable in addition on death | Raises the benefit only in the year of claim |

- **Sources of surplus, in order of size**: ***Risikoüberschuss*** first and by a wide margin;
  ***Kostenüberschuss*** second and modest; ***Zinsüberschuss*** third and negligible, the contract's
  *Deckungskapital* being small and short-lived [R9] [R10]. That ordering is the **mirror image of the
  endowment**, where the interest result dominates. The *Bewertungsreserven* share of § 153 Abs. 3 VVG
  and § 139 VAG is economically empty here for the same reason [R5] [R11] `[unverified]`.
- **The delib model implements *Beitragsverrechnung* only** and says so in `model.md`; *Summenzuwachs*
  is the one worth implementing next, being the only one that changes the benefit, not the premium.

### 7. *Zahlweise* and the *Ratenzahlungszuschlag*

- Premiums are payable **annually, half-yearly, quarterly or monthly** — annually in advance the
  actuarial base case, monthly by *SEPA-Lastschrift* the market's normal choice `[unverified]`.
- Paying other than annually attracts a ***Ratenzahlungszuschlag***: the German market convention is
  **2 % half-yearly, 3 % quarterly, 5 % monthly**, recorded in the sibling research as a convention with
  no carrier attribution. Carried here as **[std]** with that provenance, not as a citation (gap 21).
  Whether German carriers strike it on the *Bruttobeitrag* or the *Zahlbeitrag* — a few euros a year,
  but real for a model reproducing a *Produktinformationsblatt* figure — was **not established**
  `[unverified]`; the delib model applies it to the *Zahlbeitrag* and says so.
- The ***Versicherungsperiode*** follows the *Zahlweise*, and with it the policyholder's termination
  right under § 168 VVG [R8]: a monthly-paying contract is terminable monthly. **This is why German
  term-life lapse is not concentrated at policy anniversaries** the way an annual-mode book's is — a
  caution for any model assuming anniversary-only exits.
- **No *Versicherungsteuer***: life insurance is exempt [R16] `[unverified]`; no premium-tax line.

### 8. Options and guarantees

- ***Nachversicherungsgarantie*** — **the most important option on the product.** The policyholder may
  raise the *Versicherungssumme* **without a new *Gesundheitsprüfung*** on a named life event. The
  event families that recur across the German market, asserted from market knowledge and
  `[unverified]` in every particular (gap 7): marriage or entry into a *eingetragene
  Lebenspartnerschaft*; birth or adoption of a child; purchase of a property or drawing a loan secured
  on one; completion of training or of a degree and the start of employment; a substantial rise in
  income; taking up self-employment; divorce or the ending of a partnership; and the loss or reduction
  of other death cover, including an employer-provided one. The standard restrictions, likewise
  `[unverified]`: an **exercise window** after the event; a **cap per event** and a **cumulative cap**,
  expressed as a percentage of the original sum and/or an absolute amount; a **maximum age** beyond
  which the right lapses; and an **exclusion where the *versicherte Person* is already unable to work
  or is in treatment**. Some tariffs add an ***ereignisunabhängige Nachversicherung*** in the first
  years, exercisable without any event `[unverified]`.
  - **No event list, cap or age limit is asserted from any document** (gap 7). The option is
    specified with `[std]` parameters and is **off in the base run**.
  - **Why it matters actuarially**: an increase without underwriting is an increase in expected claims
    the increment's tariff does not reflect, bounded only by the trigger and the caps. It is also the
    point at which the § 161 three-year *Selbsttötung* clock is understood to restart for the
    increment [R1] `[unverified]` (gap 9).
- ***Dynamik*** (*Beitragsdynamik* / *Summendynamik*) — an agreed annual escalation of premium and sum
  insured together, without new underwriting, with a right of *Widerspruch* that typically lapses
  after a stated number of consecutive objections `[unverified]`. **Off in the base run.**
- ***Verlängerungsoption*** — extension at expiry without renewed underwriting, at the tariff then in
  force for the attained age. ***Umtauschoption*** — conversion into a *kapitalbildende
  Lebensversicherung* without a new *Gesundheitsprüfung*; historically common, now rare.
  ***Vorgezogene Todesfallleistung*** — early payment on medical evidence of terminal illness with a
  limited life expectancy; a growing German option and **not a *PTIA*-style disability acceleration**,
  the trigger being prognosis, not incapacity. ***Unfalltod-Zusatzversicherung*** (UZV) — an additional
  sum, commonly equal to the base sum, on accidental death within a stated period of the accident; the
  German analogue of the French *doublement accidentel*, present at five of eight carriers in the frlib
  corpus [`frlib` S1, S2, S6, S7, S9]. ***Berufsunfähigkeits-Zusatzversicherung*** (BUZ) and
  ***Beitragsbefreiung bei Berufsunfähigkeit*** — a disability rider and a waiver of premium, the
  standalone form being delib product 9. ***Vorläufiger Versicherungsschutz*** — provisional cover
  between application and acceptance, capped in amount and duration and sometimes limited to accidental
  causes; the analogue of the French *garantie provisoire* [`frlib` S2, S3]. All `[unverified]`, **none
  modelled**, and recorded so that a reader knows the omissions are deliberate.

### 9. Underwriting

- **The whole of German term-life risk selection is the *Gesundheitsprüfung***, and its legal frame is
  § 19 VVG: the applicant must disclose the *gefahrerhebliche Umstände* known to her **that the
  insurer has asked about in *Textform***, and nothing else — **the duty is question-bounded**
  [inherited: `kapitallebensversicherung.md` R5] [R4].
- ***Gesundheitsfragen*** typically cover outpatient treatment and consultations over a recent
  look-back period; inpatient treatment, operations and psychotherapy over a longer one; current
  complaints, medication and pending investigations; height and weight; and nicotine consumption.
  **The look-back periods are `[unverified]` and no figure is asserted** (gap 22). The insurer may
  escalate to an ***ärztliche Untersuchung***, a *Hausarztbericht*, blood tests or an ECG as the sum
  insured and entry age rise `[unverified]`. A ***vereinfachte Gesundheitsprüfung*** applies below a
  stated sum and full examination above a higher one; **no threshold is asserted** (gap 22). The
  corresponding French thresholds *are* published by two carriers — no medical formality below
  40 000 € and age 50, simplified underwriting to age 40 for up to 250 000 € [`frlib` S6, S3] — which
  shows the disclosure is possible and that the German market simply does not make it.
- ***Finanzielle Angemessenheit***: above a threshold the insurer also underwrites the financial
  justification for the sum — income, existing cover, the loan being protected — to bound
  over-insurance on a contract whose whole benefit falls due on death `[unverified]`.
- ***Raucher* / *Nichtraucher* — the largest single rating split after age.** A *Nichtraucher* is one
  who has consumed no nicotine-containing product for a stated qualifying period, with a duty to
  notify a resumption; carriers commonly allow reclassification once the period has been served in
  force. **The qualifying period is `[unverified]`**, commonly one or two years (gap 22). The split is
  **actuarially sanctioned**: the DAV publishes *DAV 2008 T R* and *DAV 2008 T NR* and states they are
  suitable for premium calculation differentiated by smoking status, **but not for policies written
  without a *Gesundheitsprüfung*** [R12].
  - **Price ratio.** The market's rule of thumb is that a smoker pays **roughly twice** a non-smoker's
    premium at the ages this product is sold. **No published ratio was obtained** (gap 1). The
    specification carries a **[std]** smoker/non-smoker **mortality** ratio of **2.20** at ages 30–55,
    which reproduces a **premium** ratio of about **2.0** once sum-related and per-policy expenses are
    added back (mechanic 16); the rationale is that the insured-lives smoker gap at working ages is
    consistently reported in the two-to-three range `[unverified]`.
- ***Berufsgruppen***: occupation is a rating factor but **far weaker here than on a
  *Berufsunfähigkeitsversicherung***. Most German RLV tariffs use a small number of classes, or none
  below a listed set of hazardous occupations — roofers, scaffolders, professional divers, explosives
  handlers, aircrew, deployed soldiers — which attract a *Risikozuschlag* or a decline `[unverified]`.
  **No class list, class count or loading is asserted** (gap 22).
- ***Risikozuschläge***: where the health evidence discloses an impairment the German outcome is
  normally a **premium loading expressed as a percentage of the risk premium**, not a benefit
  exclusion; life *Leistungsausschlüsse* are used sparingly, unlike in disability business. Hazardous
  **hobbies** — parachuting, technical diving, motorsport, mountaineering, combat sports — and extended
  stays in high-risk regions are handled the same way `[unverified]`. **No German carrier publishes a
  *Risikozuschlag* scale**, and neither does any French one [`frlib` mechanic 10]. The model carries a
  `rating_factor` on the mortality basis, **[std]** at 1.00 in the base run.
- ***Anzeigepflicht* remedies**, inherited [R4]: the insurer may **adjust the contract
  retrospectively** — writing in the *Risikozuschlag* or exclusion that would have applied — instead of
  refusing to perform, and for negligent breach this is the usual outcome; the rights **lapse after
  five years**, or **ten** for intentional or *arglistig* breach. **On a term contract these limits are
  the whole of the claims-risk story**: a claim in the first five years is exposed to the full remedy
  set, one after ten years essentially is not.
- **Underwriting outcomes** are the same four as everywhere: accept at standard rates; accept with a
  *Risikozuschlag* and/or an individually agreed exclusion, subject to the applicant's acceptance;
  defer; decline `[unverified]` [R4].

### 10. Charges, and the *Zillmerung* of a contract with almost no reserve

- **German carriers do not disclose their charge structure for this product**, and the absence is
  **structural**: no *Effektivkostenquote*, because a reduction in yield presupposes a yield; no
  *Basisinformationsblatt*, because the product is not a PRIIP; and the *Produktinformationsblatt*
  quotes premiums, not loadings [R17]. Every charge parameter in the delib specification is `[std]`
  (gap 8).
- The structure the *Bruttobeitrag* is built from is the standard German three-part one and its shape is
  not in doubt: ***Abschluss- und Vertriebskosten*** (α), expressed as a per-mille of the
  ***Beitragssumme***, with the ***Höchstzillmersatz*** capping the amount financed through the reserve
  at **25 ‰ of the *Beitragssumme***, cut from 40 ‰ by the LVRG with effect from 1 January 2015 [R10];
  and ***Verwaltungskosten*** (β and γ), normally split between a percentage of each premium and a
  per-policy or per-mille-of-sum annual amount `[unverified]`. **No level for any of them is public.**
- ***Zillmerung* on a term product is a peculiar thing.** The cap is a fraction of the
  ***Beitragssumme***, which for a 25-year contract is 25 times the annual premium — a large number.
  The contract's *Deckungskapital*, by contrast, is tiny, existing only because the level premium
  exceeds the rising natural risk premium early on (mechanic 11). **So the Zillmer charge is large
  relative to the reserve it is written into, and the *gezillmerte Deckungsrückstellung* of a term
  contract is negative for a long stretch and never becomes large.** Whether a negative individual
  reserve must be floored at zero — the *Nullstellung* question — was **not established** [R21]
  (gap 11).
- **The one charge consequence that reaches the cash flows**: acquisition cost is incurred at issue and
  recovered over the term, so an early lapse is a loss to the insurer. That is the economic reason lapse
  matters on a product with no surrender value, and why the model carries acquisition cost as a
  **year-0 outgo** rather than an annualised loading (mechanic 17).

### 11. No *Rückkaufswert* — why, and what actually happens on *Kündigung*

- **What every consumer source says.** Terminating a German RLV returns nothing: cover ends and the
  premiums paid stay with the insurer [S5] [S15]. The French market says the same about its own product
  — "les cotisations versées restent acquises à l'assureur", "le contrat ne comprend pas de faculté de
  rachat" [`frlib` S5, S9].
- **Why, precisely — two reasons, and only the second is legal:**
  1. **There is almost nothing to pay out.** An RLV has **no *Sparanteil*** in the endowment's sense: no
     part of the premium is set aside to build a sum that will certainly be paid. But it is **not** true
     that nothing accumulates. A level premium charged against a **rising** mortality rate necessarily
     overcharges early and undercharges late, and the difference is held as a *Deckungskapital* that
     builds, peaks near the middle of the term and **runs off to exactly zero at expiry**. On the
     `[std]` calibration of mechanic 16 that reserve peaks at a low single-digit percentage of the sum
     insured, and after *Zillmerung* (mechanic 10) it is **negative or nil through much of the term**.
     **Stating "there is no *Sparanteil*, therefore no reserve" is wrong, and a model built on it will
     fail its own closure check.** The correct statement is that the reserve exists, is small, is fully
     consumed by expiry, and is often negative on a *gezillmert* basis.
  2. **The statute does not require it to be paid out.** § 169 Abs. 1 VVG confines the surrender-value
     duty to a life insurance whose insured event is **certain to occur**; a term assurance's is not
     [R2]. **This scope limitation is `[unverified]` at the level of the statutory wording and is the
     most consequential such tag in this file** (gap 2); its practical result is not in doubt.
- **What happens on *Kündigung*.** The policyholder may terminate at the end of the current
  *Versicherungsperiode* [R8]; cover ends; **nothing is paid**; at most an unearned fraction of a
  prepaid premium is returned. On the model this is a **pure decrement with no benefit attached**, and
  `claims_surr` is **structurally zero** — worth asserting in a test rather than leaving to prose.
- **The *Beitragsfreistellung* question, answered.** § 165 VVG gives the right in form [R3]; on this
  product it is empty in substance, because the tiny or negative reserve buys a *beitragsfreie
  Versicherungssumme* that fails the minimum test in most durations, and the statutory fallback is
  payment of a nil *Rückkaufswert* [R3] [R2]. **The same collapse happens on the non-payment path**:
  § 166 VVG converts a lapsed life contract into a *prämienfreie Versicherung* rather than ending it —
  **unless** the paid-up benefit falls below the minimum, which here it does, so the contract simply
  ends [R8] `[unverified]`. Carriers answer the customer's real question with a *Beitragsstundung*, a
  temporary *Ruhen*, or a reduction of the sum insured `[unverified]` (gap 10).
- **Consequence for § 161.** The statutory substitution — *leistungsfrei*, but pay the *Rückkaufswert*
  [R1] — substitutes **nil**. So the German three-year rule, a softening on an endowment, is on a term
  contract **an exclusion in all but name** (mechanic 12).

### 12. *Selbsttötung* — § 161 VVG, and how it differs from the French rule

- **The German rule** [R1], inherited corroboration: the insurer is ***leistungsfrei*** where the
  *versicherte Person* **intentionally takes her own life before three years have elapsed since
  conclusion of the contract**; **unless** the act was committed **in a state excluding free
  determination of the will caused by a *krankhafte Störung der Geistestätigkeit***; the period **may be
  extended by agreement**; and where *leistungsfrei* the insurer must nevertheless **pay the
  *Rückkaufswert*, including *Überschussanteile*, under § 169**.
- **The French rule**, from the frlib research where the article was retrieved in full [`frlib` R1]:
  art. L. 132-7 of the Code des assurances makes the death cover "**de nul effet**" if the insured takes
  his own life **in the first year**, and **requires** cover from the second; on an increase the clock
  restarts **for the additional cover only**; and there is no surrender value to fall back on, art.
  L. 132-23 forbidding one on a temporaire décès [`frlib` R3].

| | Germany [R1] | France [`frlib` R1, R3] |
|---|---|---|
| Window | **Three years** from conclusion | **One year** from conclusion |
| Effect inside the window | Insurer *leistungsfrei*; **pays the *Rückkaufswert* instead** | Cover "de nul effet" — **nothing is paid** |
| What the substitution is worth on a term product | **Nil or nominal** — there is no surrender value (mechanic 11) | Nil by construction — the product may not have one |
| Extension by agreement | **Expressly permitted** | Not provided for; the statutory minimum is the rule |

- So the two systems reach **nearly the same economic answer by opposite routes**, and the German answer
  applies for **three times as long**. A modeller porting a French model to Germany who changes only the
  window length has got the mechanic right by accident; one porting the German model to France and
  keeping the *Rückkaufswert* substitution has introduced a benefit French law forbids.
- **The mental-illness exception is not a formality** — it is the ground on which German *Selbsttötung*
  claims are actually litigated [R23], so the rule is not a clean contractual switch. **A best-estimate
  cash-flow model cannot represent that**, and delib does not try: the rule is applied as a benefit
  switch over the first three policy years and the exception is a known simplification. **On an
  increase**, German AVB practice is understood to restart the clock **for the increment only**, as the
  French statute expressly does [`frlib` R1]; **`[unverified]` for Germany** (gap 9), and it matters
  because the *Nachversicherungsgarantie* makes increments routine (mechanic 8).

### 13. Exclusions — the *Kriegsklausel*, and how short the German list is

- **The German exclusion list is remarkably short.** Beyond the statutory *Selbsttötung* window [R1]
  and the statutory forfeitures of § 162 VVG [R7], a German RLV wording carries essentially one
  substantive exclusion — the ***Kriegsklausel*** — plus a nuclear / ABC clause. **There is no list of
  hazardous sports, no aviation exclusion, no alcohol or narcotics exclusion, no occupational
  exclusion and no pre-existing-condition exclusion in the ordinary German wording.** Hazardous
  activities are handled at **underwriting**, by a *Risikozuschlag* or an individually agreed
  exclusion, not by a standing clause (mechanic 9) `[unverified]`.
- **The contrast with France is stark.** The French *notices* retrieved for frlib carry exclusion lists
  running to a dozen or more heads — war, nuclear, riots and terrorism with active participation,
  intentional acts, alcohol above the Code de la route threshold, driving without a licence,
  non-prescribed narcotics, air sports, motor competition, solo ocean racing, diving below 20 metres,
  mountaineering above 3 000 metres, professional sport, pre-existing conditions, and occupational
  death for firefighters, military and police [`frlib` mechanic 9]. **A German wording covers all of
  that by pricing it.** The modelling consequence: the German product's claim rate is a mortality
  question, the French product's is partly a coverage question.
- **The *Kriegsklausel*, as the German market writes it**, `[unverified]` in every particular: where
  death is **causally connected with war or war-like events** the benefit is **restricted rather than
  excluded** — the wording pays the *Deckungskapital* or the value computed for the date of death
  instead of the *Versicherungssumme*, which on a term contract is **nil or nominal** (mechanic 11).
  The restriction standardly bites only where the *versicherte Person* took an ***aktive
  Beteiligung***, so **passive war risk — a civilian killed in a conflict he took no part in — remains
  covered**, which is the opposite of the drafting instinct an English-language reader brings to a war
  exclusion. Parallel restrictions apply to ***innere Unruhen*** with active participation and to
  death from ***ABC-Waffen*** and deliberately released nuclear energy. Some wordings carve **out** of
  the restriction a person abroad who is **overtaken** by war and does not participate.
- **§ 162 VVG's statutory forfeitures** sit alongside: the insurer is *leistungsfrei* where the
  **policyholder** intentionally and unlawfully brings about the death of the *versicherte Person*, and
  a **beneficiary** who does so loses his entitlement [R7] `[unverified]`.
- **Delib's treatment.** The base model applies **no exclusion decrement** beyond the § 161 window
  (mechanic 12). The *Kriegsklausel* is recorded in the specification and not modelled, and the reason
  is stated: it is a catastrophe-scenario clause, not a best-estimate one.

### 14. *Verbundene Leben* and the *Über-Kreuz-Versicherung*

Two different things that are routinely confused: the first is a **product form**, the second a
**contracting structure** with identical cover and a different tax outcome.

- ***Risikolebensversicherung auf verbundene Leben*** — **one contract, two *versicherte Personen***.
  The *Versicherungssumme* is paid **once, on the first death**, and the contract then **ends**,
  leaving the survivor with no cover. All `[unverified]` as to any carrier and asserted from market
  knowledge.
  - **Both lives are underwritten**, and both must give the § 150 written consent [R7].
  - **The premium is materially below the cost of two single contracts of the same sum**, because only
    one benefit is ever paid, and **above** one single contract, because the first-death rate exceeds
    either single rate. **No ratio is asserted** (gap 15); the model computes it from
    `q_first = q_A + q_B − q_A·q_B` under an independence assumption — itself a **[std]** choice that
    understates the true first-death rate for a couple sharing a household, a vehicle and a lifestyle.
  - **The separation problem.** On divorce the contract covers two people who no longer want a joint
    benefit and cannot simply halve it. Some carriers offer a **conversion right into two single
    contracts without a new *Gesundheitsprüfung***; where they do not, the only exit is termination
    with nothing back (mechanic 11) `[unverified]`. This is the standard consumer-press criticism.
  - **Modelling**: two lives, one benefit, one termination — a `lives = 2` variant on the same chassis
    with a first-death decrement, **off in the base run**.
- ***Über-Kreuz-Versicherung*** — **two contracts, crossed.** Partner A is *Versicherungsnehmer* and
  *Bezugsberechtigter* of a contract on **B's** life; B is *Versicherungsnehmer* and
  *Bezugsberechtigter* of a contract on **A's** life; each pays the premium on **his own** contract
  out of **his own** funds.
  - **The cover is identical to two ordinary single contracts.** Nothing about the benefit, premium,
    underwriting or cash flows changes, and **the model is indifferent to the structure** — worth
    saying so a reader does not go looking for a mechanic that is not there.
  - **The tax outcome is not identical, and that is the whole point.** Under the ordinary structure —
    A insures his own life and names B — the benefit is an ***Erwerb von Todes wegen*** under § 3
    Abs. 1 Nr. 4 ErbStG and is charged against B's *Freibetrag* [R15] `[unverified]`. Under the
    *Über-Kreuz* structure **A receives a payment under a contract A owns and paid for**; nothing
    passes from B's estate; there is **no *Erwerb von Todes wegen*** [R15] `[unverified]`.
  - **Two conditions it must actually satisfy**, both `[unverified]`: the premiums must be paid **from
    the surviving partner's own funds, verifiably** — a joint account fed by only one partner's income,
    or payment by the insured partner, exposes the arrangement to recharacterisation as a gift; and the
    **§ 150 written consent** of the insured partner is required [R7].
  - **Who needs it.** On a 300 000 € benefit: to a **spouse**, the 500 000 € *Freibetrag* absorbs it
    and the tax is nil; to an **unmarried partner**, the *Freibetrag* is 20 000 €, *Steuerklasse* III
    applies from 30 %, and the liability is on the order of **84 000 € — 28 % of the sum insured**
    `[unverified]` [R15]. **So the structure is close to compulsory for unmarried couples and close to
    pointless for married ones below the spousal allowance.** That is why the German market talks about
    it, and why the delib specification documents a contracting structure alongside the cash flows.

### 15. *Rechnungsgrundlagen*: DAV 2008 T, the *Sicherheitszuschläge*, and unisex

- **The mortality basis for a German term product is *DAV 2008 T***, with ***DAV 2008 T NR*** and
  ***DAV 2008 T R*** [R12], inherited corroboration: derived by the DAV *Arbeitsgruppe Biometrische
  Rechnungsgrundlagen* over **2006 to 2008** from German insurers' own policy data with German
  population statistics; the *Richtlinie* **regulates both the derivation methodology and the procedure
  for setting the *Sicherheitszuschläge***; the smoker and non-smoker variants are **suitable for
  premium calculation** but **not for policies written without a *Gesundheitsprüfung***; adopted
  **4 December 2008**, restated as a *Fachgrundsatz* dated **29 November 2022**.
- ***The table values are not public and delib does not redistribute them.*** The model ships a
  **[std] proxy** and states what a replacement must preserve: an age-graded death rate for medically
  selected lives, separable into smoker and non-smoker variants and into first-order and second-order
  levels.
- **The *Sicherheitszuschlag* is part of the table's construction, not a bolt-on.** The *Richtlinie*
  sets the **procedure** for determining it [R12]; the level is not public (gap 6), and it determines
  the *Brutto*/*Zahlbeitrag* spread almost by itself (mechanic 5). It exists to cover three named
  risks — ***Zufallsrisiko***, ***Änderungsrisiko*** and ***Irrtumsrisiko*** `[unverified]`.
- **Three structural reasons the effective first-order margin on a contract written today is large**,
  none of them a criticism of the insurer: the table was derived on **2006–2008** experience and German
  mortality has improved since, an 18-year drift on a table used for pricing today; it is applied to a
  **medically selected** portfolio in its early durations, where selection is strongest and the table's
  own selection allowance is generic; and the *Sicherheitszuschläge* are added on top of both.
  Together these make a first-order to second-order ratio **in the region of two** entirely plausible,
  which is what the observed spread implies (mechanic 5). **The ratio is `[std]`; the reasoning is not
  numeric.**
- ***Unisex*.** New business from **21 December 2012** may not rate on sex [R13]. But **DAV 2008 T is
  sex-distinct**, so every German unisex term tariff is a **blend of the male and female tables at a
  mixing ratio the carrier chooses from its own expected new-business mix** — proprietary, unpublished,
  periodically re-estimated `[unverified]`. Female mortality at the ages this product is sold is
  roughly half male `[unverified]`, so the ratio moves the tariff a great deal. **This is one of the
  largest single sources of unexplained rate spread between German carriers**, with no French analogue
  beyond the Institut des actuaires' 60 % / 40 % working-group mix [`frlib` R13]. The model uses a
  **[std]** 50/50 blend, stated as such.
- ***Rechnungszins***: at most the ***Höchstrechnungszins***, **1,00 % for new business from 1 January
  2025**, raised from 0,25 % and the first increase since 1994 [R10]. **On this product it barely
  matters** — the *Deckungskapital* is small and short-lived — a genuine difference from every other
  delib product, stated so a reader does not expect a *Zinszusatzreserve* discussion that does not
  apply. ***Lapse is not a pricing basis element***: German first-order bases are mortality, interest
  and expenses, and a *Stornowahrscheinlichkeit* is a second-order quantity used for projection and
  profit-testing, not for the tariff `[unverified]`.
- ***No German insurer publishes its own basis*** — not the table, the *Sicherheitszuschlag*, the A/E
  factor, the expense loading, the assumed unisex mix or the lapse assumption; the AVB say the
  calculation follows "die anerkannten Regeln der Versicherungsmathematik" and stop there
  `[unverified]`. **The same position frlib reached for France** [`frlib` gap 12], with one difference:
  a French carrier published a **complete attained-age gross rate card** [`frlib` S3], and **no German
  carrier publishes anything comparable** (gap 1).

### 16. Price points — what could not be established, and the `[std]` scale built instead

- **The brief asked for annual *Zahlbeiträge* at 100 000 € and 300 000 €, ages 30 and 40, non-smoker,
  from comparison portals, on the correct ground that these are the only public German price data for
  this product. They could not be obtained.** No German carrier publishes a rate card [S3]–[S13]; the
  *Produktinformationsblatt* quotes the applicant's own premium [S2]; and a portal result is generated
  per query rather than published [S14], so it is unreachable in any event. **The retrieval pass of
  2026-08-30 did not change this**: it opened the GDV model wordings and three carrier documents and
  found no rate card in any of them, and [S14] was not queried. **Not one price point appears in this
  file** (gap 1).
- **What is shipped instead is an explicit `[std]` construction**, given in full so that a reviewer can
  replace any part and re-derive the rest. **Every number below is `[std]`. None is a market
  observation, and none may be cited downstream as one.**

| Element | `[std]` value | Rationale |
|---|---|---|
| Best-estimate mortality `q2(x)` | `0.00030 x 1.095^(x-30)` p.a., unisex, non-smoker, medically selected | Gompertz proxy, anchored near 0.70 of an approximate German unisex population rate at ages 30–60 — the order of magnitude of a medically selected insured-lives table `[unverified]` |
| Smoker multiplier | 2.20 on `q2` | Mid-point of the two-to-three range reported for insured-lives smoker mortality at working ages `[unverified]` |
| Sicherheitszuschlag `m` | 1.25, so first-order `q1 = 2.25 x q2` | Calibrated so the derived Zahl/Brutto ratio lands near the market's "about half"; sensitivity tabulated in mechanic 5 |
| Rechnungszins | 0.00 % in this illustration | Set to zero so the arithmetic is reproducible with a calculator; the real 1.00 % [R10] moves the premium by well under 5 % on these terms |
| Acquisition cost | 25 permille of the Beitragssumme at issue | The Höchstzillmersatz ceiling [R10]; assumes a term tariff runs at the cap |
| Collection / premium-related admin | 5.0 % of each Bruttobeitrag | Placeholder; no German figure is public [R17] |
| Per-policy annual admin | 0.30 permille of the Versicherungssumme | Placeholder, expressed sum-related so it scales across the table |
| Surplus return | 90 % of the mortality margin | The MindZV minimum [R9]; modelling the statutory minimum is the conservative choice for the Zahlbeitrag |
| Lapse | none in this illustration | Deliberate: including it would change the level and obscure the mechanic |

- **Resulting `[std]` premium scale** — level annual premiums, unisex non-smoker, deaths at the end of
  the year, no lapse:

| Entry age | Term | Versicherungssumme | Bruttobeitrag p.a. | Zahlbeitrag p.a. | Zahl / Brutto | Brutto, permille of sum |
|---|---|---|---|---|---|---|
| 30 | 30 | 100,000 EUR | 386 EUR | 222 EUR | 0.58 | 3.86 |
| 30 | 30 | 300,000 EUR | 1,157 EUR | 667 EUR | 0.58 | 3.86 |
| 35 | 25 | 100,000 EUR | 439 EUR | 251 EUR | 0.57 | 4.39 |
| 35 | 25 | 300,000 EUR | 1,316 EUR | 753 EUR | 0.57 | 4.38 |
| 40 | 25 | 100,000 EUR | 664 EUR | 373 EUR | 0.56 | 6.64 |
| 40 | 25 | 300,000 EUR | 1,993 EUR | 1,117 EUR | 0.56 | 6.64 |

- **Smoker comparison at the anchor cell** (entry age 35, 300 000 €, 25 years): *Bruttobeitrag*
  2 777 € and *Zahlbeitrag* 1 539 €, a **smoker/non-smoker *Zahlbeitrag* ratio of 2.04** against a
  mortality ratio of 2.20 — the gap being the sum-related and per-policy expense elements, which do not
  scale with mortality. **All `[std]`.**
- **How to read these honestly.** They are internally consistent and reproduce three qualitative
  features the German market is known to have — a *Zahlbeitrag* near half the *Bruttobeitrag*, a smoker
  premium near double the non-smoker one, and a premium per unit sum rising steeply with entry age —
  but they are **not** evidence about any carrier, and against a live German comparison the constructed
  level would very likely sit **above the cheapest direct-written tariffs**, the construction running
  acquisition cost at the statutory ceiling and taking no credit for an expense surplus. **One
  published *Bruttobeitrag* / *Zahlbeitrag* pair at a known age, sum and term would pin `m` directly
  through the identity of mechanic 5 and everything else would follow — the highest-value missing datum
  in this file** (gap 1).

### 17. Decrements and policyholder behaviour

- **Two decrements only: death and lapse** — no disability acceleration, no surrender benefit, no
  paid-up state, no partial withdrawal; the simplest decrement structure of the ten delib products.
- **Lapse.** No *Risikoversicherung*-specific rate was established (gap 13). The inherited whole-market
  *Stornoquote* — **2,72 % (2024), 2,56 % (2023)** on the main GDV measure and **1,2 % (2024)** on a
  second, irreconcilable one [R18] — is a book average dominated by long-dated savings contracts and is
  **not used**. The `[std]` assumption is argued from three structural features instead: **there is
  nothing to lose by lapsing** — no surrender value, no accumulated bonus — so the financial friction
  that suppresses savings-contract lapse is absent; **the contract is terminable at the end of each
  *Versicherungsperiode***, monthly for a monthly-paying contract [R8], so exit is frictionless in time
  as well as in money; and **the need that motivated the purchase amortises** — a mortgage is repaid,
  children grow up — so lapse should **rise** in later durations, the opposite of the savings-product
  shape. Shipped: **6 % in policy year 1, 4 % in years 2 and 3, 3 % thereafter**, with an argued
  plausible range of **2 % to 8 %** in the early years. **No German figure supports any of it**
  (gap 13).
- **Anti-selective lapse.** Healthy lives can re-underwrite into a cheaper contract; impaired lives
  cannot, so the lapsing population is **healthier than the remaining one** and a term book's mortality
  drifts up relative to a table calibrated on the whole cohort. **Delib does not model selective
  lapse** — one basis for stayers and leavers — a known simplification and a listed pitfall.
- **The *Zahlbeitrag* is itself a lapse driver.** A cut in the *Beitragsverrechnung* raises the bill
  without any change the policyholder agreed to, and the remedy is to leave [R6] (mechanic 5). **A
  model that raises the *Zahlbeitrag* toward the *Bruttobeitrag* in a stress and leaves the lapse
  assumption unchanged is understating the stress.** A listed pitfall.
- **Premium cessation** at death and at the end of the *Beitragszahlungsdauer*, which may be shorter
  than the *Versicherungsdauer* (mechanic 4). The processing order must put premium collection before
  the death decrement in the year of death if the tariff collects in advance, and the model must say so.

### 18. Taxation

- **The *Todesfallleistung* is free of *Einkommensteuer*.** § 20 Abs. 1 Nr. 6 EStG taxes the
  *Unterschiedsbetrag* on a **survival or surrender** payment [R14]; a pure death benefit paid to a
  third party is not investment income of the policyholder and is **not caught** `[unverified]`
  (gap 16). The 12/62 rule, the *Halbeinkünfteverfahren* and the **50 % *Mindesttodesfallschutz***
  requirement for post-1 April 2009 contracts [R14] are rules about **savings** contracts, and the last
  exists precisely to stop savings contracts presenting themselves as death covers. **None applies to a
  pure RLV.**
- **The *Erbschaftsteuer* is the only tax that reaches this product**, and it reaches it hard for the
  wrong beneficiary [R15]: the benefit is an ***Erwerb von Todes wegen*** under § 3 Abs. 1 Nr. 4 ErbStG
  where the deceased concluded and paid for the contract on his own life; the *Freibetrag* depends on
  the relationship — **500 000 €** spouse or registered partner, **400 000 €** per child, **200 000 €**
  per grandchild, **20 000 €** in *Steuerklasse* III, which includes an **unmarried partner** — and the
  rate schedule begins at **7 %** in class I and **30 %** in class III. **Every one of those figures is
  `[unverified]`** (gap 18) and is carried downstream as a `[std]` illustration. **The planning response
  is the *Über-Kreuz-Versicherung*** (mechanic 14), which removes the benefit from the charge entirely
  by making the recipient the owner and payer.
- **Premiums**: *Sonderausgabenabzug* is available in principle under § 10 Abs. 1 Nr. 3a EStG among the
  *sonstige Vorsorgeaufwendungen*, and is worth **nothing** to most taxpayers because the annual ceiling
  is already consumed by health and long-term-care contributions [R14] `[unverified]` (gap 17). **No
  ceiling figure is stated in this file.**
- **No *Versicherungsteuer***: life insurance is exempt [R16] `[unverified]`, so the German premium
  bears no premium tax, unlike a French *cotisation* quoted "TTC" [`frlib` mechanic 13].
- **Nothing here is modelled**: the model publishes **gross** liability cash flows, and tax on the
  beneficiary is documented, not computed.

### 19. Market context

- **The size of the German *Risikoversicherung* segment was not established** — no contract count, new
  business, premium income, aggregate *versicherte Summe*, average sum insured or average premium
  [R18] (gap 13). This is the largest evidential hole in the file after the price points.
- Structural rather than statistical: a term contract's **premium** is tiny relative to its **sum
  insured**, so the segment is far larger measured by risk carried than by premium earned, and any
  ranking by premium income systematically understates it. Arithmetic, not an observation.
- **Distribution.** A genuinely three-channel market — tied agents and bank branches [S8] [S9],
  independent brokers [S7] [S10] [S11], direct writers [S3] [S4] [S12] — and the channel is visible in
  the ***Brutto*/*Zahlbeitrag* spread**, acquisition cost being the largest thing that differs between
  them (mechanic 5). **The Continentale / Europa pair is the cleanest natural experiment available**
  [S12], and **it was not sampled** (gap 5).
- **The comparison-portal layer is a market participant, not just an observer.** With no published rate
  card, the portals [S14] are where price competition happens, and a tariff's design is shaped by how
  it ranks in a portal's default query — a *Zahlbeitrag* query. **That is a plausible structural
  explanation for why the *Zahlbeitrag* is marketed and the *Bruttobeitrag* merely disclosed**, and it
  is `[unverified]`. The consumer-protection line runs the other way: compare the *Bruttobeitrag*,
  because that is what you can be made to pay [S15] [S16] [S17] [R20].

### 20. What a projection model needs, and what the corpus supplies

| Model input | Status | Tag |
|---|---|---|
| Benefit definition | established in full — sum insured on death inside the term, nothing otherwise | [R1] [R2] [S5] [S15] |
| Versicherungssumme shapes | three shapes established structurally; no schedule parameter established | mechanic 3, gap 15 |
| Premium form | level Bruttobeitrag over the term, established structurally | [R6] [R10], mechanic 4 |
| Bruttobeitrag / Zahlbeitrag mechanic | **established in kind** — Beitragsverrechnung, guaranteed gross, non-guaranteed billed | [R5] [R6] [R9] [S5] |
| Beitragsverrechnungssatz `v` | **not established at any level** | **[std]** 0.57, gap 1 |
| MindZV minimum allocation from the Risikoergebnis | established, 90 % | [R9] inherited |
| Mortality table family | established — DAV 2008 T, with R and NR variants, medically underwritten only | [R12] inherited |
| Mortality table values | **not public; not redistributed** | **[std]** proxy, mechanic 16 |
| Sicherheitszuschlag magnitude | **not established** | **[std]** m = 1.25, gap 6 |
| Unisex mixing ratio | mechanism established; carrier ratios proprietary | **[std]** 50/50, [R13] |
| Smoker / non-smoker mortality ratio | split established and actuarially sanctioned; **no ratio established** | **[std]** 2.20, gap 1 |
| Berufsgruppen structure | rating factor established; **no class list or loading established** | gap 22 |
| Risikozuschlag scale | mechanism established; **no scale is public in Germany or France** | **[std]** 1.00, mechanic 9 |
| Rechnungszins; Höchstzillmersatz | established — 1.00 % for new business from 2025 (immaterial here); 25 permille of the Beitragssumme | [R10] inherited |
| Acquisition and admin cost levels; Ratenzahlungszuschlag | **levels not established; disclosed per contract in euro under § 2 VVG-InfoV but never published as a rate card — one specimen gives α = 2,41 % of the *Tarifbeitragssumme* [S2]**; loading a market convention at 2 / 3 / 5 % | **[std]**, gaps 8 and 21 |
| Rückkaufswert; Beitragsfreistellung | **none** — established in substance, `[unverified]` in statutory wording; the paid-up right exists and collapses to nil | [R2] [R3] [R8], gap 2 |
| Selbsttötung window; clock on an increment | window established in full — three years, benefit substitution; **behaviour on an increment not established** | [R1] inherited, gap 9 |
| Kriegsklausel; Nachversicherungsgarantie parameters | shapes established structurally; **no wording, caps, window or age limit established** | mechanic 13, gap 7 |
| Lapse rate; premium rates; market size | **no term-specific figure of any kind anywhere** | **[std]** 6/4/3 % and the mechanic-16 scale, gaps 1 and 13 |
| Erbschaftsteuer parameters | charge established structurally; **every figure `[unverified]`** | [R15], gap 18 |

---

## Observed variation across insurers

**The honest headline, revised: two carriers were sampled, and the industry model wording.** The GDV
model conditions [S1], the Cosmos AVB and *Besondere Bedingungen* [S3] and the Hannoversche pack [S4]
were read in full, and Cosmos's premium and cost specimens [S2] with them. **Two carriers are not a
market**, and every range below is still argued rather than observed. frlib could put eight carriers side by side because
eight *notices d'information* were read; the sibling delib endowment file could put six side by side,
thinly, from search-result summaries. **This file can put none side by side.** What follows states what
a variations table would have contained and records that every cell is empty.

### Carrier coverage actually achieved

| Carrier | Sells an individual RLV | AVB located | Document content established | Any parameter established |
|---|---|---|---|---|
| CosmosDirekt [S3] | asserted | no | no | no |
| Hannoversche [S4] | asserted | no | no | no |
| HUK-COBURG / HUK24 [S5] | **yes** | no | **guide page retrieved** — the two surplus forms (*Todesfallbonus*, *Sofortrabatt*) and the *Tarifbeitrag* as billing ceiling; **no four-component vocabulary on it** | no |
| Debeka [S6] | asserted | no — library path pattern inherited only | no | no |
| Dialog [S7] | asserted | no | no | no |
| Allianz [S8] | asserted | no | no | no |
| R+V [S9] | asserted | no | no | no |
| NÜRNBERGER [S10] | asserted | no | no | no |
| LV 1871 [S11] | asserted | no | no | no |
| Continentale / Europa [S12] | asserted | no | no | no |
| Seventeen further carriers [S13] | asserted | no | no | no |

### Parameter ranges — what is argued, and what is observed

Every "range" below is **argued from structure or market knowledge**, not observed in a document. The
"who sits where" column is the point of a variations table, and it is empty throughout.

| Parameter | Range carried in the delib specification | Who sits where | Tag |
|---|---|---|---|
| Zahl / Brutto ratio | 0.45 to 1.00, representative 0.57 | **not established** | **[std]**, gap 1 |
| Sicherheitszuschlag `m` implied | 1.0 to 1.5 | **not established** | **[std]**, gap 6 |
| Smoker / non-smoker premium ratio | about 1.8 to 2.5 | **not established** | **[std]** 2.04 derived, gap 1 |
| Eintrittsalter | 18 to 65, some carriers to 70 or 75 | **not established** | **[std]**, gap 22 |
| Endalter | 75, with 80 and 85 offered | **not established** | **[std]**, gap 22 |
| Versicherungsdauer | 5 to 40 years | **not established** | **[std]**, gap 22 |
| Mindestversicherungssumme | 10,000 to 50,000 EUR | **not established** | **[std]**, gap 22 |
| Maximum sum without special underwriting | high six to low seven figures | **not established** | **[std]**, gap 22 |
| Vereinfachte Gesundheitsprüfung threshold | **not established at all** | **not established** | gap 22 |
| Berufsgruppen count | small, or none below a hazardous-occupation list | **not established** | gap 22 |
| Nachversicherung event list | nine recurring event families | **not established** | gap 7 |
| Nachversicherung cap, window and age limit | **not established at all** | **not established** | gap 7 |
| Ratenzahlungszuschlag | 2 % / 3 % / 5 % | market convention, no attribution | **[std]**, gap 21 |
| Rückkaufswert | none, market-wide | uniform | [R2], gap 2 |
| Selbsttötung window | three years, statutory minimum, extendable | statutory | [R1] |
| Versicherungssumme shapes offered | all three at most carriers | **not established** | mechanic 3 |
| Verbundene Leben offered | widely | **not established** | mechanic 14 |
| Lapse rate | 2 % to 8 % in early durations | **not established** | **[std]**, gap 13 |

### What the corpus supports as a representative design

A **composite**, not a copy of any carrier's tariff — it could not be otherwise, no carrier's tariff
having been read.

- **Single life, individual, participating *Risikolebensversicherung***, medically underwritten,
  *Neubestand* [R9] [R12].
- ***Konstante Versicherungssumme* of 300 000 €** as the base shape, with `linear fallend` and
  `annuitätisch fallend` as external schedule tables on the same chassis (mechanic 3). **[std]**;
  300 000 € is the sum at which the *Erbschaftsteuer* contrast of mechanic 14 becomes the decisive
  product-design fact.
- **Entry age 35, term 25 years, cover to age 60**, level *Bruttobeitrag* over the whole term
  (mechanic 4). **[std]**; long enough for the *Deckungskapital* to build and run off visibly, short
  enough to fit one worked-example table.
- ***Bruttobeitrag* on first-order bases** — a DAV 2008 T-shaped `[std]` proxy at `q1 = 2.25 x q2`,
  unisex 50/50, non-smoker, *Rechnungszins* 1,00 %, *gezillmert* at the 25 ‰ ceiling [R10] [R12] [R13].
- ***Zahlbeitrag* derived, not assumed**: the model computes the mortality margin against the
  second-order basis, returns the MindZV minimum of **90 %** of it as *Beitragsverrechnung*, and
  publishes **both** premium streams [R9] (mechanic 5). Derived ratio **0.57 [std]**.
- **No *Rückkaufswert*, no *beitragsfreie Versicherungssumme*, no maturity value.** Lapse is a pure
  decrement and `claims_surr` is structurally zero [R2] [R3] [R8] (mechanic 11).
- **Three-year *Selbsttötung* window** as a benefit switch paying the (nil) *Rückkaufswert* [R1]
  (mechanic 12); **no exclusion decrement** — the *Kriegsklausel* is documented, not modelled
  (mechanic 13).
- **Options off in the base run**: *Nachversicherungsgarantie*, *Dynamik*, *verbundene Leben*, UZV,
  BUZ, *vorgezogene Todesfallleistung* (mechanics 8, 14). **Lapse `[std]` at 6 % / 4 % / 3 %**, with
  selective lapse deliberately not modelled and recorded as a pitfall (mechanic 17).
- **Gross cash flows, undiscounted.** No *Deckungsrückstellung*, no Solvency II, no tax computation
  [R21] [R22].

---

## Gaps and caveats

1. ~~**No price point of any kind was obtained.**~~ **CLOSED for one carrier.** The gap said "one
   published *Bruttobeitrag* / *Zahlbeitrag* pair at a known age, sum and term would pin the
   *Sicherheitszuschlag* directly", and one was found: a carrier's *Muster-Informationsblatt* and
   *Produktinformationsblatt*, which § 2 Abs. 1 Nr. 1 and § 4 Abs. 2 VVG-InfoV require to carry the
   premium and the costs in euro. At **age 41, 19 years, 100 000 €**: *Tarifbeitrag* **18,21 €/month**
   against a first-year *Zahlbeitrag* of **8,20 €**, ratio **0,450**, and the same ratio to three
   decimals in three further specimens across two tariffs and two editions [S2]. No German carrier
   still publishes a **rate card** [S3]–[S13], and a portal result is still generated per query rather
   than published [S14]. **The premium scale of mechanic 16 is unchanged and remains a `[std]`
   construction** — one direct writer's model case is not a market — and the observed 0,450 is
   recorded as a check against it, sitting at the bottom of the argued 0,45–1,00 range.

2. **VERIFIED — and the conclusion drawn from it OVERTURNED.** § 169 Abs. 1 does confine the duty to
   a policy insuring "ein Risiko ..., bei dem der Eintritt der Verpflichtung des Versicherers **gewiss**
   ist", word for word, so no statutory surrender duty attaches on *Kündigung* [R2]; and § 165 carries
   **no** such limitation, so the paid-up right is live [R3]. **But the sentence "nothing is paid on
   *Kündigung* is corroborated by uniform market practice" is wrong.** The GDV model wording converts
   the contract into a *beitragsfreie Versicherung* on *Kündigung* and pays "den Rückkaufswert
   entsprechend § 169 des Versicherungsvertragsgesetzes (VVG)" where the paid-up sum fails a
   carrier-set minimum [S1] § 13 Abs. 4, Abs. 8; Hannoversche does the same at a 2 500 € minimum, less
   an *Abzug* of **60 % des Deckungskapitals**, with a *Rückkaufswerte* table annexed to the
   *Versicherungsschein* [S4] § 13; only Cosmos pays nothing [S3] § 15 Abs. 10. **The amount is nil or
   nominal in every wording — "keine oder nur geringe Mittel" [S1] [S3] — but the design is not
   uniform.** This is the most consequential finding of the provenance pass and the one open item that
   reaches the model: `claims_lapse = 0` is now carried as a best-estimate approximation, not as a
   structural identity.

3. ~~**No *Produktinformationsblatt* was located.**~~ **CLOSED.** Two carrier specimens were read
   [S2], and the field list inferred from purpose was right — with one correction of nomenclature: the
   document § 4 VVG-InfoV requires is the ***Informationsblatt zu Versicherungsprodukten*** (IPID);
   "Produktinformationsblatt" is the market's older name and survives in file naming. **No GDV model PIB
   exists** for this line; the association publishes model *Bedingungen* and *Standmitteilungen* only.

4. ~~**MindZV section numbering is unsettled.**~~ **CLOSED.** The three percentages sit in three
   consecutive sections of the canonical text: **§ 6 Abs. 1** — 90 % of the *anzurechnende
   Kapitalerträge* "abzüglich der rechnungsmäßigen Zinsen"; **§ 7** — "beträgt **90 Prozent** des ...
   Risikoergebnisses"; **§ 8** — 50 % of the *übriges Ergebnis*. § 4 Abs. 1 and § 7 Satz 2 confirm the
   separate *Alt-*/*Neubestand* computation, and each of the three is **floored at zero**, so the 90 %
   is a one-way minimum [R9]. Both carrier wordings state the same three percentages [S3] § 3 Abs. 1 a,
   [S4] § 20. **MindZV section numbers may now be cited.**

5. **The Continentale / Europa natural experiment was not run** [S12]: one group runs a broker-channel
   and a direct-channel carrier on the same product with the same underwriting and reserving basis — the
   cleanest available way to isolate the channel effect on the spread. Neither carrier's documents were
   reached, and the same applies to Dialog as a monoline comparator [S7].

6. **The magnitude of the DAV 2008 T *Sicherheitszuschlag* was not established.** The *Richtlinie*
   regulates the **procedure** for setting it [R12]; the level is not public. It determines the
   *Brutto*/*Zahlbeitrag* spread almost by itself (mechanic 5) and is shipped as **[std] `m = 1.25`**
   with its calibration and sensitivity stated in full.

7. ~~**No *Nachversicherungsgarantie* parameters were established.**~~ **CLOSED** by a carrier
   wording [S3] § 13. The event list: marriage; birth (multiple birth counting once) or adoption;
   financing from 50 000 €, purchase or start of construction of an owner-occupied home; first
   permanent employment after study or after vocational training; first chamber-regulated
   self-employment providing the main income; a permanent rise of at least 10 % in gross monthly basic
   pay; first crossing of the *Beitragsbemessungsgrenze*; exemption from statutory pension insurance as
   a self-employed craftsman. **Neither divorce nor loss of other cover is on it**, though both were in
   the guessed nine. Window **twelve months** from the event; per-event cap **20 % of the original sum
   insured, at most 50 000 €**, minimum 5 000 €; each event once, birth or adoption twice, **five
   occasions in all**; right ends **above age 50**, rests while the contract is not premium-paying, and
   is barred once a *schwere Krankheit* benefit is claimed. Increments are priced at the attained
   *rechnungsmäßiges Alter*, the recorded occupation, the remaining term and any agreed *Risikozuschlag*
   (Abs. 5). **`nvg_schedule.csv` is unchanged**: it is a mechanics demonstration, off in the base run,
   and its 1.2 / 1.4 steps sit inside the carrier's caps but assume full take-up of two events.

8. **WRONG as stated, and corrected.** There is indeed no *Effektivkostenquote* — and § 2 Abs. 1
   Nr. 9 VVG-InfoV gives the reason in terms, confining the duty to a contract "bei dem der Eintritt
   der Verpflichtung des Versicherers gewiss ist" — and no *Basisinformationsblatt*, the product not
   being a PRIIP [R17]. **But German term-life charge levels are not undisclosed.** § 2 Abs. 1 Nr. 1
   requires the *Abschlusskosten* as a single total and the other costs as a share of the annual
   premium, with the *Verwaltungskosten* separately again; § 2 Abs. 2 requires them **in Euro**; § 4
   Abs. 2 puts them on the *Informationsblatt* under "Prämie; Kosten"; and both wordings point the
   customer there [S1] § 14 Abs. 1, [S3] § 16 Abs. 1. What is missing is a **published rate card**.
   The specimen gives, for its model case, **99,98 € acquisition cost = 2,41 % of the
   *Tarifbeitragssumme***, other annual costs **48,52 €** of which **35,20 €** administration, and
   **1,50 € per 100 €** of paid-up sum while paid up [S2]. So the `[std]` α at the 25 ‰ ceiling is
   **close to right for this carrier and mis-typed**: DeckRV § 4 caps only the *zillmerbare* part, and
   both wordings spread "die restlichen Abschluss- und Vertriebskosten ... über die gesamte
   Beitragszahlungsdauer" [S1] § 14 Abs. 3, [S3] § 16 Abs. 3. **Every charge parameter stays [std]**
   (mechanic 16): one model case is not a market.

9. ~~**Whether the § 161 three-year clock restarts on an increase is not established.**~~ **CLOSED.**
   § 161 is silent — it runs from *Abschluss des Versicherungsvertrags* — but all three retrieved
   wordings say the same thing in near-identical words: "Wenn unsere Leistungspflicht durch eine
   Änderung des Vertrages erweitert wird oder der Vertrag wiederhergestellt wird, beginnt die
   Dreijahresfrist bezüglich des geänderten oder wiederhergestellten Teils neu" [S1] § 5 Abs. 3, [S3]
   § 2 Abs. 4, [S4] § 19 Abs. 3. **The model's per-increment restart is market practice**, and the
   French statute restarts its one-year clock the same way [`frlib` R1].

10. **What German carriers offer in place of *Beitragsfreistellung* was not established** [R3]:
    *Beitragsstundung*, a temporary *Ruhen* and a reduction of the sum insured are asserted from market
    knowledge and are `[unverified]`. The analysis that §§ 165 and 166 both collapse to nil on this
    product [R3] [R8] is structural and does not depend on the gap.

11. **Half closed.** DeckRV § 4 Abs. 1 reads "Der Zillmersatz darf **25 Promille der Summe aller
    Prämien** nicht überschreiten" and draws **no distinction between product types**; both [S1] § 14
    Abs. 2 and [S3] § 16 Abs. 2 apply "das Verrechnungsverfahren nach § 4 der
    Deckungsrückstellungsverordnung" to a term contract at 2,5 % — so the cap does reach a
    *Risikoversicherung* [R10]. Two refinements: § 4 Abs. 1 also caps the offset at the "höchstmöglichen
    Prämienteile", the parts needed neither for benefits nor for running costs, which binds harder on a
    term product; and [S1] footnote 28 records that the clause belongs in a wording only "bei der
    Verwendung des Zillmerverfahrens", so **Zillmerung is optional on this line**. The
    ***Nullstellung*** question is **still not established** — neither DeckRV § 4 nor HGB § 341f
    addresses it [R21] — and matters here because a *gezillmert* term contract sits below zero for a
    long stretch (mechanic 10). The model publishes no reserve, so neither reaches its cash flows.

12. **The DAV 2008 T data coverage for the term-assurance segment is not established.** The sibling
    research established coverage of **60 % of the German market in the *Kapitallebensversicherung*
    segment**; **the term-assurance figure was truncated in the search summary** [R12]. Since this is
    the table for **this** product, that is the one number of the two that mattered.

13. **The German *Risikoversicherung* market has no numbers in this file.** No contract count, new
    business, premium income, aggregate *versicherte Summe*, average sum insured, average premium and —
    most consequentially — **no segment-specific *Stornoquote*** [R18]. The inherited whole-market
    figures (**2,72 % / 2,56 %**, with a second irreconcilable measure at **1,2 %**) are a book average
    dominated by long-dated savings contracts and are **deliberately not used**. The delib lapse
    assumption is **[std] 6 % / 4 % / 3 %** on the structural argument of mechanic 17, range 2 % to 8 %,
    and **no German figure supports any of it.**

14. **No BaFin material specific to term assurance was located.** *Merkblatt* 01/2023 (VA) is expressly
    about ***kapitalbildende*** products and does not reach a pure protection contract [R19], so this
    file carries **no supervisory conduct standard** and a reader must not import the endowment one.

15. **Falling-sum schedule parameters were not established** (mechanic 3): the nominal rate a German
    *annuitätisch fallende* tariff amortises at, the residual sum at expiry, and the premium reduction
    relative to the constant shape. The model computes the reduction from the schedule, so the gap
    affects the **[std]** schedule table only. The same applies to the *verbundene Leben* premium
    relative to two single contracts.

16. ~~**The non-application of § 20 Abs. 1 Nr. 6 EStG is `[unverified]`.**~~ **CLOSED, and the section
    fails on both limbs.** Satz 1 taxes the *Unterschiedsbetrag* "**im Erlebensfall oder bei Rückkauf
    des Vertrags** bei Rentenversicherungen mit Kapitalwahlrecht ... und bei **Kapitalversicherungen
    mit Sparanteil**, wenn der Vertrag nach dem 31. Dezember 2004 abgeschlossen worden ist" [R14]. A
    pure *Risikolebensversicherung* pays on death, not on survival or surrender, and has no
    *Sparanteil*. The half-income rule of Satz 2 is confirmed at the 60th year, raised to the **62nd**
    by § 52 for contracts concluded after 31 December 2011; the **50 % *Mindesttodesfallschutz*** of
    Satz 6 is confirmed verbatim and applies, per § 52, to contracts concluded after **31 March 2009**.

17. ~~**The *Sonderausgaben* ceiling figures are deliberately omitted.**~~ **CLOSED, and the claim
    confirmed.** § 10 Abs. 1 Nr. 3a EStG names this product expressly, among contributions "zu
    **Risikoversicherungen, die nur für den Todesfall eine Leistung vorsehen**". § 10 Abs. 4 sets the
    combined ceiling for Nr. 3 and Nr. 3a at **2 800 Euro** a year, or **1 900 Euro** for a taxpayer
    whose health cover is wholly or partly paid for by another — most employees and pensioners — and
    Satz 4 settles the practical result: where the Nr. 3 health and long-term-care contributions already
    exceed the ceiling they are deducted in full and "ein Abzug von Vorsorgeaufwendungen im Sinne des
    Absatzes 1 Nummer 3a **scheidet aus**" [R14]. **The ceiling figures may now be stated.**

18. ~~**Every *Erbschaftsteuer* figure is `[unverified]`.**~~ **CLOSED, and every figure was right**
    [R15]. § 16 Abs. 1: 500 000 € spouse or *Lebenspartner*, 400 000 € children, 200 000 € grandchildren,
    100 000 € the rest of class I, 20 000 € classes II and III. § 15 Abs. 1: an unmarried partner falls
    in "alle übrigen Erwerber", class III. § 19 Abs. 1: 7 % at the foot of class I, 30 % flat to
    600 000 € in class III. § 3 Abs. 1 Nr. 4 catches the benefit without naming insurance — "jeder
    Vermögensvorteil, der auf Grund eines vom Erblasser geschlossenen Vertrags bei dessen Tode von einem
    Dritten unmittelbar erworben wird". **The 84 000 € illustration checks out to the euro**:
    (300 000 − 20 000) × 30 %. The figures remain `[std]` illustrations downstream and are never model
    parameters.

19. ~~**The *Versicherungsteuer* exemption's statutory location is `[unverified]`.**~~ **CLOSED, with
    the citation sharpened and a URL corrected.** The consolidated law is **VersStG 2021**, at
    `https://www.gesetze-im-internet.de/versstg/__4.html` — the `verststg_1996` slug this file carried
    is a typo and 404s. § 4 is titled *Ausnahmen von der Besteuerung*, and the exempting limb is
    **Abs. 1 Nr. 5 Buchst. a**: a contract creating claims to capital, annuity or other benefits "im
    **Fall des Todes**, des Erlebens oder des Alters". Satz 2 of that number matters for riders — the
    exemption "gilt nicht für die Unfallversicherung, die Haftpflichtversicherung und sonstige
    Sachversicherungen" [R16]. The model carries no premium-tax line and states why.

20. **No case law is cited by name anywhere in this file** [R23]. German term-life litigation clusters
    on the completeness of the *Gesundheitsfragen* answers, on the § 19 Abs. 5 warning requirement and
    on the mental-illness exception to § 161 — and **not one decision was located, so none is named and
    none is invented.**

21. **The *Ratenzahlungszuschlag* of 2 % / 3 % / 5 % is a market convention with no carrier
    attribution**, inherited from the sibling research. Whether German RLV carriers strike it on the
    *Bruttobeitrag* or the *Zahlbeitrag* was not established; the model applies it to the *Zahlbeitrag*
    and says so (mechanic 7).

22. **Partly closed — and the prediction that "a single retrieved AVB would close it almost entirely"
    was too optimistic.** Three AVBs were read and they settle **one** of the seven: the **smoker
    qualifying period is twelve months** before application, no smoking or vaping, nicotine-containing
    or not, with a parallel *Nicht-Nikotinkonsument* class — and, a fact the file did not have, the
    classification is **continuing**: a later switch is a *Gefahrerhöhung* the policyholder must notify,
    the insurer may charge a higher premium retroactively at an unchanged sum insured, and above a 10 %
    increase the policyholder may terminate within a month [S3] § 18. **Still not established**:
    health-question look-back periods, the medical-examination threshold, the simplified-question
    threshold, the *Berufsgruppen* count and loadings, the entry-age and cover-age envelopes, and the
    minimum and maximum sums insured (mechanic 9). All remain **[std]**. The reason the AVBs do not
    settle them is structural: those parameters live in the *Antrag* and the carrier's underwriting
    manual, not in the conditions.

23. **Comparison with the sister libraries, stated so the difference is not glossed.** `frlib`'s
    term-life file rests on eight *notices d'information* and five Légifrance articles **downloaded and
    read**. The two sibling delib files rest on search-result summaries. **This file rests on neither.**
    Its `[S#]` and `[R#]` tags point at documents that exist and were not opened; its
    inherited-corroboration notes are the only evidence in it that anyone checked anything; and its
    numbers are `[std]` constructions with their arithmetic shown. That is a weaker document than its
    siblings, it is weaker in a way visible on every page, and the alternative — a confident-looking
    file full of invented figures — would have been worse.
