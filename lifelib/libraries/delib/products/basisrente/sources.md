# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/basisrente.md` (the citation ground
truth for this product) and are **frozen — never renumber**. Unused sources are omitted, so the
numbering had a gap at **S12** (the GDV *Musterbedingungen* service index), which the drafting
session omitted because **whether the GDV publishes a Basisrente model condition set at all was
never established** (gap 5). **That gap is now closed and S12 is restored below**: the GDV
service index was retrieved on 2026-08-30 and it publishes a Basisrente *Musterbedingung*, a
Basisrente BUZ *Musterbedingung* and two Basisrente *Muster-Standmitteilungen*. All four were
retrieved in full. They are the spine this composite was written without, and several entries
below now rest on them. Every id — **S1–S16 and R1–R24** — appears below. Original access date
for all sources: **2026-08-29**; the retrieval pass recorded per entry ran on **2026-08-30**.
Cross-product [REG-R#] tags are listed in their own section at the end.

**Retrieval conditions — read this before relying on a single entry below.** They are the
conditions of house-rules section 3, and they are not what they were when this file was written:

1. **This file was drafted with no retrieval at all.** Direct HTTP egress from the build
   environment was blocked by an organisation network policy: `WebFetch` and `curl` were refused
   with HTTP 403 at the egress gateway for every host outside a short package-registry
   allowlist, and every host that matters here was tried and refused —
   `gesetze-im-internet.de` (EStG § 10 and § 22, AltZertG, ZPO § 851c, VVG, DeckRV),
   `bafin.de`, `gdv.de`, `aktuar.de`, `bundesfinanzministerium.de`, `bzst.de`, the authority
   that certifies *Basisrentenverträge*, and `de.wikipedia.org`. **There was no search channel
   either**: the session's `WebSearch` budget — a hard cap of 200 calls shared across all delib
   work — was **exhausted before this product was reached**, two sibling delib research files
   having consumed it. So the first draft of every entry below rested on the authoring model's
   own knowledge of German insurance law and practice, with no fetch, no search, no snippet and
   no summary behind it, disciplined by [std] and [unverified] tags rather than by a document.
2. **That policy has since been lifted and the citations were re-verified against the primary
   documents.** On **2026-08-30** the German statutes and regulations this product turns on were
   read as canonical XML at `gesetze-im-internet.de`, each with its amendment status (*Stand*)
   recorded on its entry and the sections it is cited for read; two carriers' *Allgemeine
   Versicherungsbedingungen*, the GDV *Musterbedingungen*, filled-in
   *Muster-Produktinformationsblätter*, the consolidated BMF-Schreiben, a BFH judgment and an
   independent *Effektivkosten* study were retrieved as PDF or HTML and read. The same pass
   across the whole library read all fifteen German instruments delib cites as canonical XML
   and checked 950 statutory section references, of which 950 were correct; **62 % of delib's
   source entries now say `Retrieved: yes`**.
3. **Where this file ends the pass.** Of the **forty** entries below — S1–S16 and R1–R24 —
   **twenty answer `Retrieved: yes`**, **seven** record part of what they cite as
   read and the rest as not, and **thirteen are still `Retrieved: no`**. Those thirteen name what
   happened, and none of them is a paywall or a subscription login: **four** are amending acts
   (R5, R6, R7, R8) that have no consolidated page of their own at `gesetze-im-internet.de`, and
   for three of the four the effect is read instead in the consolidated law; **one** is the DAV
   2004 R table [R17], which delib has never seen and which is not published free of charge;
   **five** are carrier document sets — an index whose links are injected by script and resolve
   to no PDF [S3], a host that answers HTTP 403 to this build environment [S8], two carriers of
   which nothing was opened [S6] [S10], and the residual list for which nothing was searched
   [S11]; and **three** are market and supervisory material — a BaFin document not found at the
   address recorded [R21], the GDV and BMF stock and new-business statistics, of which not one
   was opened, and rating pages that answer 200 with navigation and marketing copy and no rating
   table [R24].

**A `Retrieved: yes` entry is a certificate; a `Retrieved: no` entry is still a pointer.** Where
the line says yes, the document was opened and the passage the entry rests on was read, and the
edition, *Stand*, page count or quoted wording on the entry comes from the document itself. Where
it says no, an [R1] tag on a sentence about § 10 Abs. 1 Nr. 2 Buchst. b EStG means only *this is
the instrument that claim must be checked against*; it does not mean anyone read it, the URL is
either a canonical form offered and marked [unverified] or the entry says `URL: not established`,
and no document number, edition, page count or publication date has been invented anywhere in this
file. **The re-verification changed things, and the changes are on the entries themselves**: the
conversion basis of the guaranteed *Rentenfaktor* [S1] [R17], one carrier's product name [S4] and
the *Kleinbetragsrente* threshold [R23] are corrections to what the drafted text said, not
confirmations of it.

---

## Primary product sources

(delib-basisrente-s1)=

### S1 — Cosmos Lebensversicherungs-AG (CosmosDirekt), *Allgemeine Bedingungen* for the Basisrente — tariffs LA 1100 A, LA 1079 A, LA 936 A, LA 1099 A
- Publisher / doc type: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland; *Allgemeine Versicherungsbedingungen* for Basisrente tariffs, in the carrier's `LA nnnn A` house numbering
- URL: `https://www.cosmosdirekt.de/resource/blob/88924/af678e39611b9b44f5dfb3b0cebb895c/allgemeine-bedingungen-basisrente-la-1079-a--data.pdf` (LA 1079 A, the *klassisch* wording) and `https://www.cosmosdirekt.de/resource/blob/88926/1c398c12d5d98869dc0f23218bf20bf3/allgemeine-bedingungen-fondsgebundene-basisrente-la-1100-a--data.pdf` (LA 1100 A, the *fondsgebunden* wording). Two further Basisrente documents sit under the same `resource/blob` scheme and were retrieved with them: LA 1080 A (*Hinterbliebenen-Zusatzversicherung*, blob 89028) and the *Muster*-PIBs for both forms (blobs 89376 and 89378). **LA 936 A and LA 1099 A were not located and are not asserted to exist**
- Retrieved: **yes** (PDF, 7 pp. each, editions LA 1079 A (10.15) and LA 1100 A (10.15), read 2026-08-30). Both wordings were read in full, §§ 1, 2, 6, 7 and 8 closely
- Used for: **the most productive single source in this file.** It supplies, as read text rather than as inference: the **three premium forms** — LA 1079 A § 6 carries *Zuzahlungen* and premium adjustment, § 7 Abs. 2 the *Einmalbeitrag*, which the model's `prem_form` and `zuzahlung_pp` implement; the **tariff family** RBA/RBAE (no death benefit) beside RBH/RBHE (spouse or registered partner), where a death in the *Aufschubzeit* converts the *garantiertes Deckungskapital* into a lifelong survivor's annuity and never a lump sum, which is `claims_death` as a survivor's single premium; the absence of a capital option — "*Darüber hinaus erfolgen keine Auszahlungen. Ein Kapitalwahlrecht existiert nicht*" (§ 1 Abs. 11) — and of any *Rückkaufswert* on either a *Kündigung* or a *Beitragsfreistellung* (§ 7 Abs. 1 and 3); the **five-year spreading of acquisition costs**, "*Die bei der Beitragskalkulation in Ansatz gebrachten Abschluss- und Vertriebskosten verteilen wir in gleichmäßigen Jahresbeträgen mindestens auf die ersten fünf Vertragsjahre*" (§ 8 Abs. 1), which is `zill_spread_y = 5` (gap 8, closed); the **surplus shape** — a *Zins-Überschussanteil* in per cent of the *überschussberechtigtes Deckungskapital* and a *Grund-Überschussanteil* in ‰ of the *aufgelaufene Beitragssumme*, accumulated as a *Bonussumme* in the *Aufschubzeit*, with a *Schluss-Überschussanteil* and a *Bewertungsreserven*-share in per cent of the *Bonus-Deckungskapital* falling due only at the end of the *Aufschubzeit* (§ 2 Abs. 2 b–d), which closes gap 17's inference; the two payout-phase *Überschusssysteme*, *jährliche Rentensteigerung (dynamische Rente)* and *Zusatzrente (flexible Rente)* (§ 2 Abs. 2 e); and a **transfer to another provider free of charge on three months' notice** (§ 7 Abs. 7–11), which with [R18] closes gap 13.
  **It also contradicts the entry as it stood.** The conversion convention here is *not* an interest basis of 0 % p.a.: LA 1079 A § 1 Abs. 1 fixes the *garantierter Rentenfaktor* "*auf Grundlage einer anerkannten Sterbetafel (DAV 2004R) sowie des tariflichen Garantiesatzes (Rechnungszins) von 1,25 Prozent p. a.*" — the tariff's own *Rechnungszins*, which for an October 2015 wording is that year's *Höchstrechnungszins*. The 0 % figure was a Schicht-3 observation carried over from `_research/klassische_rentenversicherung.md` and it does **not** describe this carrier's Basisrente. The corrected statement is that the guaranteed factor is struck at inception on first-order DAV 2004 R at the **tariff's** *Rechnungszins*, which moves with the guarantee vintage [R16]

(delib-basisrente-s2)=

### S2 — Allianz Lebensversicherungs-AG, **BasisRente KomfortDynamik** — specimen *persönlicher Vorschlag*
- Publisher / doc type: Allianz Lebensversicherungs-AG; a distributed specimen quotation ("Berechnung BasisRente KomfortDyn") hosted by a broker rather than by the carrier, dated by its path to **February 2025** [unverified], together with the carrier's *Vorsorgekonzept KomfortDynamik* product page
- URL: product page `https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/`; the specimen at a broker path recorded in the research file
- Retrieved: **partly.** The product page: **yes** (HTML, ~531 kB, read 2026-08-30). The broker-hosted specimen quotation: **no** — the broker path recorded in the research file was not re-derivable and no substitute was found; both charge figures therefore remain uncorroborated
- Used for: three claims, of which the retrieved page settles one outright. First, **the layer is a tax wrapper around a common chassis** — the page sells one *Vorsorgekonzept* across PrivatRente, BasisRente and RiesterRente — which is the argument in `product-spec.md` for reusing the Schicht-3 chassis and in `model.md` for naming `RV_DE_S` as the sibling. Second, the hybrid asset form with selectable guarantee levels, **now confirmed verbatim**: "*Dafür stehen zum Rentenbeginn neben einem Garantieniveau von 80 % der eingezahlten Beiträge auch ein Garantieniveau von 60 % für noch höhere Chancen oder 90 % für noch höhere Sicherheit zur Verfügung*", with 100 % reserved by law to Riester — so the **60 / 80 / 90 % ladder with 80 % as the default is a read fact**, and the third row of the asset-form table no longer carries a tag. Third, the two charge figures — an ***Abschlussprovision* of 1 575 €** on the specimen and **total costs relative to the capital formed of at most 0,95 € per 100 €** — remain **[unverified]**, because the specimen itself was not reached; they are no longer the corpus's only charge anchor, since [S13] now supplies a filled-in *Muster*-PIB with an *Effektivkosten* figure and a full charge schedule

(delib-basisrente-s3)=

### S3 — Allianz Lebensversicherungs-AG, the **BasisRente** product family
- Publisher / doc type: Allianz Lebensversicherungs-AG; AVB, *Produktinformationsblätter* and *Verbraucherinformationen* for the carrier's Basisrente tariffs, marketed as BasisRente Klassik, BasisRente Perspektive and **BasisRente InvestFlex**
- URL: the carrier's *Muster*-PIB index for the family, `https://www.allianz.de/service/vorsorge/muster-produktinformation-allianz-basisrente/`
- Retrieved: **no** — the index page returns 200 with its document links injected by script, so no *Muster*-PIB PDF could be resolved from it; **no AVB, PIB or *Verbraucherinformation* of this carrier was opened.** The **product names are, however, no longer [unverified]**: *BasisRente InvestFlex*, in both a no-guarantee and an 80 %-*Beitragsgarantie* form, is named as an Allianz Basisrente tariff in the Fraunhofer ITWM study at [S16], and *BasisRente Perspektive* and the 60/80/90 % guarantee ladder are on the carrier's own pages at [S2]
- Used for: **the family's existence and its tariff names.** It appears in the variations table of `product-spec.md` as the second column's document set, and is named because Allianz is the largest German life writer, so its Basisrente wordings remain the most consequential documents this corpus has not opened. Every substantive Allianz claim in the product documents is sourced to [S2] or [S16] instead

(delib-basisrente-s4)=

### S4 — Alte Leipziger Lebensversicherung a. G., **AL_RoyalBasisRente** (Klassik and Fonds)
- Publisher / doc type: Alte Leipziger Lebensversicherung a. G., Oberursel; AVB, *Produktinformationsblatt*, *Verbraucherinformation*
- URL: `https://www.alte-leipziger.de/Allgemeine-Bedingungen-fondsgebundene-Basisrentenversicherung-pm2401.pdf`; the sibling wordings sit under the same flat scheme — `...-moderne-flexible-basisrente-pm2153.pdf` and `...-fondsgebundene-Basisrentenversicherung-mit-flexiblen-Garantien-pm2405.pdf`
- Retrieved: **yes** for pm 2401 (PDF, 21 pp., edition **pm 2401 – 06.2026**, read 2026-08-30); the other two wordings were located but only their identity was taken
- Used for: **the correction of this entry's own product name, and the carrier's tariff codes.** The retrieved wording is titled "*Allgemeine Bedingungen für die fondsgebundene Basisrente (Tarif FR70)*", and the Fraunhofer study at [S16] names the family ***ALfonds-Basis***, tariff **FR70** without a *Beitragsgarantie* and tariff **FR75** with an 80 % one. **"AL_RoyalBasisRente" is not the current market name and is withdrawn as a claim**; it is retained in the heading only because the id is frozen. The entry still carries the sentence in `product-spec.md` naming this carrier as a first target for a checker, because it is repeatedly placed at the top of independent Basisrente ratings [R24]

(delib-basisrente-s5)=

### S5 — NÜRNBERGER Lebensversicherung AG, **Basis-Rente** with **Berufsunfähigkeits-Zusatzversicherung**
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB for the Basisrente main contract and separate AVB for the BUZ rider; the carrier's *Muster*-PIB for the fund-linked Basisrente
- URL: `https://www.nuernberger.de/medien/4allportal/lv052_030_p.pdf` — the *Muster-Produktinformationsblatt* for the **NÜRNBERGER Fondsgebundene Basisrente**, certification number 006590, Stand 01.01.2025. The AVB for the Basisrente main contract and for the BUZ rider sit in the same `4allportal` scheme but **no Basisrente AVB document id was located**; the carrier's Schicht-3 wording GN331451 (tariff NIR3301) was retrieved and is *not* a Basisrente
- Retrieved: **the *Muster*-PIB yes** (PDF, 2 pp., Stand 01.01.2025, read 2026-08-30); **the AVB and the BUZ AVB no** — not located at any address on the carrier's own site
- Used for: **the corpus's first quantified Basisrente charge schedule and its first *Rentenfaktor* level**, both from the retrieved *Muster*-PIB, and both reported in full at [S13]. The tariff is **NFX3208T** [S16]. On the BUZ, this entry no longer carries gap 18: **a Basisrente BUZ wording has now been read** — not this carrier's, but the GDV *Musterbedingung* at [S12], whose § 9 Abs. 2 states the 50 % rule in contractual terms, "*Die Zusatzversicherung ist so gestaltet, dass stets mehr als 50 % der Beiträge auf Ihre Hauptversicherung entfallen*". That is the invariant `buz_prem_share < 0.50`, now cited rather than asserted. What remains unreached is **this carrier's own BUZ wording**, which would show how a principal *Berufsunfähigkeit* writer words the rule in practice

(delib-basisrente-s6)=

### S6 — Volkswohl Bund Lebensversicherung a. G., **Basisrente**
- Publisher / doc type: Volkswohl Bund Lebensversicherung a. G., Dortmund; AVB, *Produktinformationsblatt*
- URL: not established — the carrier's Basisrente pages were reached but no AVB or PIB PDF was resolved from them
- Retrieved: **no** — no AVB and no PIB of this carrier was opened. Its **tariff names are established at second hand**: the Fraunhofer study at [S16] names **BFR (FondsPur)** without a *Beitragsgarantie* and **BGR** with an 80 % one, and gives *Effektivkosten* for both
- Used for: **existence, tariff names, and one of the five carriers in the *Effektivkosten* comparison at [S16].** Named in the variations table of `product-spec.md` as a broker-channel carrier with a large Basisrente book [R24], the broker channel being where this product is sold

(delib-basisrente-s7)=

### S7 — LV 1871 (Lebensversicherung von 1871 a. G.), Basisrente
- Publisher / doc type: Lebensversicherung von 1871 a. G., München; AVB, *Produktinformationsblatt*; the current market name is ***MeinPlan Basisrente***
- URL: `https://www.lv1871.de/basisrente/` (product page); the carrier's PRIIPs *Basisinformationsblätter* index is at `https://www.lv1871.de/service/kundenservice/basisinformationsblaetter/`
- Retrieved: **the product page yes** (HTML, read 2026-08-30); **no AVB and no PIB.** The page names the tariff *MeinPlan Basisrente*, offers an ETF and fund line-up including *ETF-Portfolio Plus* and *Expertenpolice*, and advertises combination "*mit umfassendem Berufsunfähigkeitsschutz*" — so the **MeinPlan attribution is confirmed and the tag goes; "Golden Basic" is not on the current line-up and is withdrawn**
- Used for: the asset-form row of `product-spec.md` that names a ***fondsgebundene* Basisrente with an open fund and ETF universe and no *Beitragsgarantie***. The **form itself is no longer [unverified]**: [S16] computes *Effektivkosten* for a no-guarantee fund-linked Basisrente at five separate carriers, so the form is demonstrably a market staple. What stays [unverified] is the claim that it **dominates new business**, for which no figure exists anywhere in the corpus (gap 3)

(delib-basisrente-s8)=

### S8 — Swiss Life Deutschland, Basisrente (**Swiss Life Maximo** family)
- Publisher / doc type: Swiss Life AG, Niederlassung für Deutschland; AVB, *Produktinformationsblatt*
- URL: `https://www.swisslife.de/privatkunden/altersvorsorge/basisrente.html` — the obvious canonical form on the carrier's own site
- Retrieved: **no** — the carrier's host answers **HTTP 403** to this build environment on every path tried on 2026-08-30, so nothing of this carrier was opened and the entry is kept as a known reference. The **Maximo** product name accordingly stays [unverified]
- Used for: **nothing beyond existence.** Cited beside [S2] in the asset-form table of `product-spec.md` as a second large broker-channel writer of the hybrid form with a selectable guarantee level. That the hybrid form with a selectable guarantee level exists is now established at [S2] and [S16]; the attribution of it to *this* carrier is not

(delib-basisrente-s9)=

### S9 — Continentale Lebensversicherung AG, Basisrente (**Rente Invest Basis** family)
- Publisher / doc type: Continentale Lebensversicherung AG, Dortmund; AVB, *Produktinformationsblatt*
- URL: `https://www.continentale.de/basisrente`
- Retrieved: **the product page yes** (HTML, read 2026-08-30); **no AVB and no PIB.** The page offers "*drei Anspar-Wege*" — a *klassisch*, a hybrid and a fund-linked accumulation route to one guaranteed lifelong annuity — and names the fund-linked tariff ***BasisRente Invest***. The entry's product name is therefore corrected: it is **BasisRente Invest**, not "Rente Invest Basis", and the tag goes
- Used for: **existence, the corrected tariff name, and the three-accumulation-route structure**, which is the same *klassisch* / hybrid / *fondsgebunden* triple the asset-form table of `product-spec.md` sets out. Named in the variations table of `product-spec.md`

(delib-basisrente-s10)=

### S10 — Stuttgarter Lebensversicherung a. G., Basisrente
- Publisher / doc type: Stuttgarter Lebensversicherung a. G.; AVB, *Produktinformationsblatt*
- URL: not established — the carrier's Basisrente path was tried on 2026-08-30 and returned **HTTP 404**, and no replacement path was resolved
- Retrieved: **no** — nothing of this carrier was opened. Its Basisrente tariff **is** named at second hand in the Fraunhofer study at [S16], as ***BasisRente performance+***, in a no-guarantee and an 80 %-*Beitragsgarantie* form
- Used for: the single sentence in `product-spec.md` recording that **a fourth asset form — an index-linked Basisrente — is plausible from one carrier's tariff naming and was not established** (gap 12). **That naming is now weakened rather than confirmed**: the tariff the study observes is *performance+*, not *performance-safe*, and no *index-safe* Basisrente tariff was found at this carrier at all. The possibility of an index-linked Basisrente — the bridge to delib product 4 (`indexpolice`) — is therefore still open, but it no longer has even a tariff name behind it, and the documents continue to assert nothing

(delib-basisrente-s11)=

### S11 — The carriers for which nothing whatever was established
- Publisher / doc type: **Debeka**, **R+V**, **HDI**, **Gothaer**, **Zurich Deutscher Herold**, **ERGO**, **AXA**, **Generali / Dialog**, **Barmenia**, **Universa**, **Württembergische**, **Signal Iduna**, **Baloise**, **DEVK**, **Provinzial**, **HUK-Coburg**, **Hannoversche**, **CosmosDirekt** (beyond [S1]), **die Bayerische**, **Condor** — each writes, or has written, a Basisrente and therefore publishes AVB, a *Produktinformationsblatt* and a *Verbraucherinformation* for it
- URL: not established for any of them
- Retrieved: **no** — not one document of any carrier on this list was opened on 2026-08-30. None was individually searched for; the retrieval effort went to the carriers that [product-spec.md] actually cites
- Used for: **a statement of coverage rather than a fact.** It carries the sentence in `product-spec.md` that **twenty named German life writers whose Basisrente documents exist were not reached, and not one contributes a single fact** (gap 1). That sentence stands for these twenty. **Gap 1 as a whole no longer does**: two carriers' Basisrente wordings [S1] [S4], one carrier's filled-in *Muster*-PIB [S5] [S13] and the GDV model conditions [S12] have now been read, so the composite is no longer built without a single carrier document. One carrier not on this list — **WWK Lebensversicherung a. G.** — supplies the second retrieved *Muster*-PIB at [S13]

(delib-basisrente-s12)=

### S12 — GDV, *Musterbedingungen* and *Muster-Standmitteilungen* for the Basisrente
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V., Berlin; non-binding model conditions and model annual statements for the German life market ("*Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ*")
- URL: service index `https://www.gdv.de/gdv/service/musterbedingungen`, from which four Basisrente documents resolve under the `gdv.de/resource/blob/...` scheme: the **Basisrente AVB** (blob 6292), the **BUZ zur Basisrente** (blob 6330), the **Hinterbliebenenrenten-Zusatzversicherung zur Basisrente** (blob 6338) and the **Muster-Standmitteilungen** for a *Basisrentenversicherung (klassisch)* (blob 6314) and *(mit BUZ)* (blob 6310)
- Retrieved: **yes** — the index (HTML, ~94 kB), the Basisrente AVB (PDF, 18 pp., **Stand: 21.07.2025**), the BUZ AVB (PDF, 11 pp., **Stand: 15.11.2022**) and the *klassisch* Muster-Standmitteilung (PDF, 8 pp., 02.2017 form), all read 2026-08-30
- Used for: **this entry did not exist in the drafted file, because whether it existed at all was gap 5. It does exist, and it is now the spine of several other entries.** From the Basisrente AVB: the payout shape and the age floor (§ 1 Abs. 1); the combination of **up to twelve monthly annuities into one payment** where the monthly annuity is small (§ 1 Abs. 2), which closes gap 19; the ***Kleinbetragsrente* commutation right** and the fact that it is the **insurer's** right, not the policyholder's (§ 1 Abs. 3), reported at [R23]; the *Kündigung* that converts to a paid-up contract and pays no *Rückkaufswert*, with a single-premium contract simply continuing unchanged (§ 9), and **partial termination and partial premium-freezing above a minimum annuity** (§ 9 Abs. 2, § 10 Abs. 4); the paid-up annuity computed "*unter Zugrundelegung des Betrages des Deckungskapitals, das sich bei gleichmäßiger Verteilung der ... angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt*" (§ 10 Abs. 1), which closes gap 8; the **charge menu** of § 11, which is the closed list of AltZertG § 2a and includes the *Verrechnungsverfahren* of DeckRV § 4 capped at "*2,5 % der von Ihnen während der Laufzeit des Vertrages zu zahlenden Beiträge*"; and the annual-information field list of § 14, which is [S15]. From the BUZ AVB: the 50 % rule in contractual terms (§ 9 Abs. 2), the rider's termination with the main contract, and the rule that a BUZ *Rückkaufswert* is never paid out but raises the main contract's benefits (§ 9 Abs. 3) — the material gap 18 said had not been reached

(delib-basisrente-s13)=

### S13 — *Produktinformationsblatt* under § 7 AltZertG (the standardised PIB)
- Publisher / doc type: each provider, on a form and a computational method prescribed by law and administered by the **Produktinformationsstelle Altersvorsorge gGmbH (PIA)**, Kaiserslautern; the mandatory pre-sale document for a certified *Basisrentenvertrag*
- URL: there is no single URL — the *individual* PIB is quotation-specific and never public, but § 7 Abs. 4 AltZertG requires every provider to publish a ***Muster*-PIB** for assumed terms of **12, 20, 30 and 40 years** on its own website. Two were retrieved: NÜRNBERGER, `https://www.nuernberger.de/medien/4allportal/lv052_030_p.pdf`, and WWK, `https://www.wwk.de/medien/dokumente/produktinformationsblaetter/basisrente-invest-protect-50/fvg22_eb_lz20_50bg.pdf`
- Retrieved: **yes, two *Muster*-PIBs** (NÜRNBERGER, PDF, 2 pp., certification number 006590, Stand 01.01.2025; WWK, PDF, 2 pp., certification number 006421, Stand 03.01.2024), read 2026-08-30. **No *individual* PIB was obtained**, and none can be: it exists only inside a quotation
- Used for: **gap 2 and gap 7, both of which this entry can now answer.** The *Muster*-PIB is on the form and computational method of the AltvPIBV [R11], and it carries the ***Effektivkosten*** — the reduction in yield in percentage points — and a ***Chancen-Risiko-Klasse*** computed by PIA. **The CRK scale is 1 to 5**, CRK 1 the lowest; the *Effektivkosten* are computed against a reference gross return fixed by the CRK (2 / 3 / 4 / 5 / 6 % for CRK 1 to 5) and the benefit scenarios against four returns per CRK (for CRK 4: **−1 %, 2 %, 5 % and 6 %**) — all of it AltvPIBV §§ 5, 8 and 10, so gap 7 is closed.
  **The NÜRNBERGER sheet is the first quantified Basisrente in the delib corpus** and every figure below is read off it: a *Musterkunde* born 1988, contract from 01.01.2025, 30 years' accumulation to age 67, **100 € a month**, so 36 000 € paid; **CRK 4**; ***Effektivkosten* 1,77 percentage points** ("*Eine beispielhafte Wertentwicklung von 5,00 % wird durch die renditemindernden Größen von 1,77 Prozentpunkten auf eine Effektivrendite von 3,23 % verringert*"); *garantiertes Kapital für Verrentung* 18 000,00 €; **garantierte monatliche Altersleistung 44,89 €** at a **guaranteed *Rentenfaktor* of 24,94 € per 10 000 € of capital** — the first *Rentenfaktor* level anywhere in this corpus, which is gap 4; *Abschluss- und Vertriebskosten* **900,00 € = 2,50 % der vereinbarten Beiträge**, plus 2,50 % on each *Zuzahlung*; *Verwaltungskosten* of **7,00 % der eingezahlten Beiträge** and up to **3,80 % p.a. of the fund** (fund charges included; current burden 1,10 %); **1,50 % of the annuity p.a. in the payout phase**; *Versorgungsausgleich* up to 500,00 €; and "*Ein Anbieterwechsel ist bei diesem Produkt ausgeschlossen*". The WWK sheet, a 20-year single-premium contract with a 50 % *Beitragsgarantie*, is CRK 4 with *Effektivkosten* of **4,95 percentage points**, and likewise excludes an *Anbieterwechsel*.
  **Read the *Effektivkosten* on a *Muster*-PIB as a ceiling, not an expectation.** They are computed on the maximum permitted charge parameters, and the Fraunhofer ITWM study at [S16] puts the realistic figure for the same five carriers' fund-linked Basisrenten at **1 – 1,5 percentage points** against *Muster*-PIB figures of **3,0 – 4,6**. That distinction is the single most important thing this entry now carries

(delib-basisrente-s14)=

### S14 — *Basisinformationsblatt* (PRIIPs key information document)
- Publisher / doc type: each provider; the PRIIPs KID for an insurance-based investment product
- URL: not established for a *Basisrente*. A carrier's *Basisinformationsblatt* index was reached (`https://www.lv1871.de/service/kundenservice/basisinformationsblaetter/`) and one *Basisinformationsblatt* was retrieved in full — NÜRNBERGER `https://www.nuernberger.de/medien/4allportal/gn339322_p.pdf`, tariff NR3361DV, Stand 01.01.2026 — but **that document is a Schicht-3 contract with a *Kapitalwahlrecht*, not a Basisrente**
- Retrieved: **one specimen of the document type, yes; none for a Basisrente, no.** The retrieved specimen establishes the form — purpose statement, product type, recommended holding period, a **summary risk indicator on a scale of 1 to 7**, performance scenarios and a cost table — but it establishes nothing about a *Basisrentenvertrag*
- Used for: the record in `product-spec.md` that the document type exists and what it carries. **Gap 6 is narrowed but not closed.** What is now established, from § 7 Abs. 2 AltZertG [R11], is that the individual *Produktinformationsblatt* "*ersetzt das Informationsblatt zu Versicherungsprodukten nach § 4 der VVG-Informationspflichtenverordnung*" and that **no *Modellrechnung* under § 154 VVG is to be performed for a certified contract, and none may be attached** — so the AltZertG PIB does displace at least one neighbouring disclosure. Whether it also displaces the PRIIPs *Basisinformationsblatt* is **still not established**: no Basisrente KID was found at any carrier, which is consistent with the product being outside PRIIPs but does not prove it. Nothing downstream asserts either arrangement

(delib-basisrente-s15)=

### S15 — Annual statement to the policyholder (*jährliche Information*, § 7a AltZertG)
- Publisher / doc type: each provider; the statutory annual information for a certified contract
- URL: the statute itself, `https://www.gesetze-im-internet.de/altzertg/__7a.html`; the GDV *Muster-Standmitteilung* for a *Basisrentenversicherung (klassisch)* at [S12]
- Retrieved: **yes** — § 7a AltZertG as canonical XML (Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294), and the GDV *Muster-Standmitteilung* (PDF, 8 pp.), both read 2026-08-30. **The paragraph address § 7a is correct and the tag goes**
- Used for: one sentence in the regulatory-context section of `product-spec.md`, which can now name the fields instead of gesturing at them. § 7a Abs. 1 requires the provider to inform the contract partner annually of **(1)** the use made of the contributions paid, **(2)** the amount of capital built up, **(3)** the actual costs incurred in the past contribution year, **(4)** the investment return earned, and **(5)**, until the payout phase begins, the capital expected to be available at its start after costs, projected on the contributions actually paid and the *Wertentwicklungen* of the individual PIB — plus a statement on ethical, social and environmental considerations. The GDV model conditions restate that list at § 14 and add that the capital figure is a *Gesamtkapital* including allocated surplus, non-guaranteed *Schlussüberschüsse* and the non-guaranteed *Bewertungsreserven*-share. That is the same state-variable list `result_pols()` publishes, and it is now sourced

(delib-basisrente-s16)=

### S16 — Consumer, comparison and rating material
- Publisher / doc type: **Finanztip**, **Stiftung Warentest / Finanztest**, the **Verbraucherzentralen**, **Verivox**, **CHECK24**, **Handelsblatt** and the rating houses at [R24]; consumer guides, comparison-portal pages and product ratings — **secondary in every case**, and S-numbered in frlib's convention because they describe the product rather than regulate it. **One independent study is now added to this entry and is the only member of it that was read**: Fraunhofer-Institut für Techno- und Wirtschaftsmathematik ITWM, Kaiserslautern, *Studie – Reale Effektivkosten für ausgewählte Basisrentenprodukte*, 4 December 2023
- URL: `https://www.itwm.fraunhofer.de/content/dam/itwm/de/documents/PressemitteilungenPDF/2023/20231204_Studienbericht_Fraunhofer_ITWM_Muster-PIB.pdf`; not established for any of the consumer and comparison sources
- Retrieved: **the Fraunhofer study yes** (PDF, 12 pp., 04.12.2023, read 2026-08-30). **No consumer guide, comparison-portal page or product rating was retrieved**, and none was searched for
- Used for: the study supplies what the consumer material was supposed to and did not — a **comparative charge observation across named carriers**. It computes *Effektivkosten* for the fund-linked Basisrenten of **Allianz** (BasisRente InvestFlex), **Alte Leipziger** (ALfonds-Basis FR70 / FR75), **NÜRNBERGER** (NFX3208T), **Stuttgarter** (BasisRente performance+) and **Volkswohl Bund** (BFR FondsPur / BGR), in a no-guarantee and an 80 %-*Beitragsgarantie* form, at 30 and 40 years, both on the *Muster*-PIB's maximum-charge convention and on realistic charge parameters. Without a guarantee the *Muster*-PIB figures run **3,00 – 4,58 percentage points** and the realistic ones **1,0 – 1,5**; with an 80 % guarantee the *Muster*-PIB figures run **2,5 – 3,5** and the realistic ones **1 – 2,3**, or 1 – 1,5 once fund kickbacks are counted. Its own conclusion is the caution this file carries: *Muster*-PIB *Effektivkosten* are "*als Obergrenze sicher sehr zuverlässig*" but "*überschätzt in der Regel tatsächlich realistische Werte deutlich*".
  **What is still not established is everything else in this entry.** Every price point, every market share and every buyer-profile statement in `product-spec.md` remains [unverified] general knowledge or a **[std]** construction, marked at the point of use, and gap 3 stands as to market size and channel mix

---

## Regulatory and actuarial references (product research numbering)

**Every German statute and regulation cited in this section was retrieved on 2026-08-30 as
canonical XML from gesetze-im-internet, with the law's *Stand* attached, and read at the section
the entry relies on.** Each entry says which. Two cautions carry across the whole section.
First, the per-section HTML page `gesetze-im-internet.de/<law>/__NNN.html` is a frameset shell of
about 5 kB carrying **no statutory text**; it is kept in each entry as the human-facing link and
is *not* what was read. Second, the entries that are **not** statutes — the amending acts at
[R5]–[R8], the BFH judgments at [R19], the BaFin material at [R21] and the market statistics at
[R22] — were **not** retrieved as documents, and say so individually. Where an entry is still
unconfirmed it now says why, rather than resting on the blanket condition the drafting session
was under.

(delib-basisrente-r1)=

### R1 — EStG § 10 Abs. 1 Nr. 2 Buchst. b — the definition of a Basisrentenvertrag
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` (the human-facing link; a frameset shell, not the text)
- Retrieved: **yes** (canonical XML, Stand: neugefasst durch Bek. v. 8.10.2009 I 3366, 3862, zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197; § 10 read in full 2026-08-30)
- Used for: **more than any other instrument in this product, and now quoted rather than paraphrased.** The five prohibitions are Satz 2 of Nr. 2 Buchst. b, verbatim: "*Die Ansprüche nach Buchstabe b dürfen nicht vererblich, nicht übertragbar, nicht beleihbar, nicht veräußerbar und nicht kapitalisierbar sein.*" That is the absence of a *Rückkaufswert*, a *Kapitalwahlrecht*, a *Teilkapitalauszahlung*, a policy loan, an assignment and a commutation, which `model.md` publishes as structural absences and `check_no_capital()` asserts. The payout shape and the **age floor** are Doppelbuchst. aa: "*die Zahlung einer monatlichen, auf das Leben des Steuerpflichtigen bezogenen lebenslangen Leibrente nicht vor Vollendung des 62. Lebensjahres*", and **the 60/62 split is Absatz 6 of the same section** — "*Absatz 1 Nummer 2 Buchstabe b Doppelbuchstabe aa ist für Vertragsabschlüsse vor dem 1. Januar 2012 mit der Maßgabe anzuwenden, dass der Vertrag die Zahlung der Leibrente nicht vor der Vollendung des 60. Lebensjahres vorsehen darf*" — so **both floors and their boundary date are confirmed and the tags go**; model points 1 and 6 sit either side of it. The **closed list of permitted survivors** is Satz 2 of aa: "*Hinterbliebene in diesem Sinne sind der Ehegatte des Steuerpflichtigen und die Kinder, für die er Anspruch auf Kindergeld oder auf einen Freibetrag nach § 32 Absatz 6 hat*", with the orphan's annuity limited to the period in which the child qualifies under § 32 — which is why `claims_death` is a survivor's single premium and never a lump sum. Two further readings the drafted entry did not have: Satz 3 permits **combining up to twelve monthly payments into one** and the **commutation of a *Kleinbetragsrente* im Sinne von § 93 Absatz 3 Satz 2 oder 4** (see [R23], and gap 19, closed), and Satz 5 shuts the door — "*Neben den genannten Auszahlungsformen darf kein weiterer Anspruch auf Auszahlungen bestehen*".
  **One correction.** The **50 % majority test is not in this section.** The statute requires only that a supplementary cover be *ergänzend*; the 50 % test is administrative, and its text is at [R18]: "*Die ergänzende Absicherung ist nur dann unschädlich, wenn mehr als 50 % der Beiträge auf die eigene Altersversorgung des Steuerpflichtigen entfallen*". The invariant `buz_prem_share < 0.50` should be cited to [R18] and [S12], not to this entry

(delib-basisrente-r2)=

### R2 — EStG § 10 Abs. 3 — the Höchstbetrag, its knappschaftliche peg, and the employee reductions
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` (human-facing link only)
- Retrieved: **yes** (canonical XML, same *Stand* as [R1]; § 10 Abs. 3 read 2026-08-30)
- Used for: the single annual *Höchstbetrag* and its peg, both now verbatim — Satz 1 and 2: "*Vorsorgeaufwendungen nach Absatz 1 Nummer 2 sind bis zu dem Höchstbeitrag zur knappschaftlichen Rentenversicherung, aufgerundet auf einen vollen Betrag in Euro, zu berücksichtigen. Bei zusammenveranlagten Ehegatten verdoppelt sich der Höchstbetrag.*" That confirms the *knappschaftliche* peg, the doubling on joint assessment **and the rounding convention** (`aufgerundet`, up to a whole euro) that `product-spec.md` uses to reproduce the series. The **2026 ceiling is now confirmed end to end**: the *Sozialversicherungsrechengrößen-Verordnung 2026* [R20] sets the *knappschaftliche* BBG at **124 800 € p.a.**, and 124 800 × 24,7 % = 30 825,60, rounded up to **30 826 €** — which is the figure in the table and at model point 9. The 2025 line reproduces the same way from 118 800 €. The two employee mechanisms are Satz 3 (the reduction by the *Gesamtbeitrag* to the general RV, for the employee groups of Nr. 1 and the § 22 Nr. 4 recipients of Nr. 2) and Satz 5 (the tax-free employer share subtracted afterwards). The argument that **the ceiling moves every year so the premium should too** is unchanged, and is why the model carries a *Beitragsdynamik* and a *Zuzahlung* rather than a level premium

(delib-basisrente-r3)=

### R3 — EStG § 10 Abs. 2 and Abs. 2a — certification and data transmission as conditions of relief
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` (human-facing link only)
- Retrieved: **yes** (canonical XML, same *Stand* as [R1]; § 10 Abs. 2 and Abs. 2a read 2026-08-30)
- Used for: the statement in `product-spec.md` that the *Sonderausgabenabzug* is conditional on certification and on electronic transmission of the contribution data, so that an uncertified contract, however economically identical, gets **no relief at all** — which is what makes the prohibitions bind the insurer's product design rather than merely the policyholder's rights. **Both paragraph addresses are now exact and the tag goes.** Certification is Abs. 2 Satz 2: "*Vorsorgeaufwendungen nach Absatz 1 Nummer 2 Buchstabe b werden nur berücksichtigt, wenn die Beiträge zugunsten eines Vertrags geleistet wurden, der nach § 5a des Altersvorsorgeverträge-Zertifizierungsgesetzes zertifiziert ist, wobei die Zertifizierung Grundlagenbescheid im Sinne des § 171 Absatz 10 der Abgabenordnung ist*" — the *Grundlagenbescheid* character being a detail the drafted entry did not have. Data transmission is Abs. 2a: the provider must transmit the contributions paid in the year **and the certification number** to the central body under § 93c AO

(delib-basisrente-r4)=

### R4 — EStG § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. aa — the Besteuerungsanteil
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` (human-facing link only)
- Retrieved: **yes** (canonical XML, Stand: neugefasst durch Bek. v. 8.10.2009 I 3366, 3862, zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197; § 22 Nr. 1 Satz 3 Buchst. a read in full, including the statutory cohort table, 2026-08-30)
- Used for: the payout-side rule of the layer. The *Kohortenprinzip* is Satz 3 of Doppelbuchst. aa: "*Der der Besteuerung unterliegende Anteil ist nach dem Jahr des Rentenbeginns und dem in diesem Jahr maßgebenden Prozentsatz aus der nachstehenden Tabelle zu entnehmen*". **The whole cohort table was read and every percentage in `product-spec.md` now matches it**, so the tags go: bis 2005 50,0; 2020 80,0; 2021 81,0; 2022 82,0; **2023 82,5; 2024 83,0; 2025 83,5; 2026 84,0**; then half a point a year to **2058 100,0**. The *Rentenfreibetrag* is Sätze 4 to 7, and they say more precisely what the documents claim: the difference between the annual annuity and the taxable part "*gilt ab dem Jahr, das dem Jahr des Rentenbeginns folgt, für die gesamte Laufzeit des Rentenbezugs*" — a euro amount frozen in the first full year — and, decisively for the payout-phase *Überschussverwendung*, "*Regelmäßige Anpassungen des Jahresbetrags der Rente führen nicht zu einer Neuberechnung und bleiben bei einer Neuberechnung außer Betracht*", so a *dynamische Rente*'s increases are fully taxable while a structural change in the annuity is not. That is the tax dimension the choice of surplus system has here and lacks in Schicht 3. On **gap 16**: aa applies to "*Rentenversicherungen im Sinne des § 10 Absatz 1 Nummer 2 Buchstabe b*" without distinguishing aa from bb, so a *BU-Rente* from a *Basisrentenvertrag* is on the same cohort basis; the drafted reading is confirmed. **No delib model computes tax**: this instrument explains the economics and justifies the model point, and reaches no cash flow

(delib-basisrente-r5)=

### R5 — Alterseinkünftegesetz (AltEinkG), 2004
- Publisher / doc type: Deutscher Bundestag / Bundesgesetzblatt; enabling statute
- URL: not established. **No Bundesgesetzblatt citation is given, because none was confirmed** (gap 23, still open for this entry)
- Retrieved: **no** — the AltEinkG is an amending act, not a consolidated instrument, so it has no gesetze-im-internet page of its own; no attempt was made to reach the Bundesgesetzblatt itself, and none of the claims below was read anywhere
- Used for: the opening of the regulatory-context section of `product-spec.md` — the statute effective **1 January 2005** that built the three-layer architecture, introduced *nachgelagerte Besteuerung* for the first layer and created the Basisrente so that the self-employed would have a vehicle with the statutory scheme's tax treatment, following the report of the commission chaired by **Bert Rürup**, from which the market name. Two corroborations are now available at one remove: the cohort table at [R4] begins "*bis 2005 50,0*", which fixes 2005 as the transition's first year, and § 10 Abs. 3 Satz 4 begins its phase-in at 2013 on a schedule that only makes sense from a 2005 start. The *Bundesverfassungsgericht* decision the statute responded to remains **[unverified]** as to year and case: it was not searched for

(delib-basisrente-r6)=

### R6 — Wachstumschancengesetz (2024) — the half-point step and the 2058 endpoint
- Publisher / doc type: Deutscher Bundestag / Bundesgesetzblatt; amending statute
- URL: not established; no Bundesgesetzblatt citation (gap 23, still open for this entry)
- Retrieved: **no** — an amending act with no consolidated page of its own; it was not retrieved. **Its effect, however, is now read directly in the consolidated law**: the statutory table at [R4] runs 2021 81,0 → 2022 82,0 → **2023 82,5** → 2024 83,0, i.e. one point a year to 2022 and half a point from 2023, ending at **2058 100,0**
- Used for: the amendment that cut the annual step from one percentage point to **half a point** with effect from the **2023** cohort — which is why 2023 is 82,5 % and not 83 % — and moved the 100 % year from 2040 to **2058**. Both of those are now confirmed in the statute itself, so the substance of the entry no longer depends on the amending act being identified. **What remains [unverified] is the attribution**: that it was the *Wachstumschancengesetz* of 2024 that made the change, and that it did so retrospectively for 2023. That was not checked against any Bundesgesetzblatt citation

(delib-basisrente-r7)=

### R7 — Jahressteuergesetz 2022 — the full Sonderausgabenabzug from 2023
- Publisher / doc type: Deutscher Bundestag / Bundesgesetzblatt; amending statute
- URL: not established; no Bundesgesetzblatt citation (gap 23, still open for this entry)
- Retrieved: **no** as to the amending act. **Its effect is read directly in § 10 Abs. 3 EStG** [R2]: Satz 4 sets 2013 at 76 %, and Satz 6 reads "*Der Prozentsatz in Satz 4 erhöht sich in den folgenden Kalenderjahren bis zum Kalenderjahr 2022 um je 2 Prozentpunkte je Kalenderjahr; ab dem Kalenderjahr 2023 beträgt er 100 Prozent*"
- Used for: the rule that **100 % of the capped contribution is deductible from the assessment period 2023**, brought forward from 2025 — **confirmed by the statute**. It is a genuine simplification of the specification: for any model point written at 2023 or later no phase-in factor is needed, so `product-spec.md` carries the current rule and a note that pre-2023 cohorts differ.
  **The entry's phase-in figures were wrong and are corrected.** It read "94 % in 2021 and 96 % in 2022". On the statutory schedule — 76 % in 2013 rising two points a year to 2022 — **2021 is 92 % and 2022 is 94 %**. The old figures were the pre-2023 *original* schedule's 2023 and 2024 values, shifted two years. The corrected series is 2020 90 %, 2021 92 %, 2022 94 %, 2023 onwards 100 %

(delib-basisrente-r8)=

### R8 — Jahressteuergesetz 2007 — the age floor from 60 to 62
- Publisher / doc type: Deutscher Bundestag / Bundesgesetzblatt; amending statute
- URL: not established; no Bundesgesetzblatt citation (gap 23, still open for this entry)
- Retrieved: **no** as to the amending act. **The split itself is now read in the consolidated law**: § 10 Abs. 1 Nr. 2 Buchst. b Doppelbuchst. aa gives 62, and § 10 Abs. 6 gives 60 "*für Vertragsabschlüsse vor dem 1. Januar 2012*" [R1]
- Used for: the **60/62 split at the end of 2011**, which is a model-point attribute rather than a formula: `conclusion_year` fixes which floor applies, and model point 6 is a 2009 contract converting at 60 while every new-business point converts at 67. **Both figures and the boundary date are confirmed and the tags go**; what stays unconfirmed is only the attribution of the change to the *Jahressteuergesetz 2007*, which was not checked. The entry also carries the resolution recorded at gap 22 — the commissioning brief said 63, the research file resolved it against 60, and **the statute settles it: 60 for pre-2012 contracts, 62 after, and 63 appears nowhere**

(delib-basisrente-r9)=

### R9 — AltZertG § 5a — certification of Basisrentenverträge
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/altzertg/__5a.html` (human-facing link only; this one is a 4 kB shell that the sweep classified THIN, so it is emphatically not what was read)
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294, with a change by Art. 5 G v. 26.5.2026 I Nr. 156 noted as textually recorded but not yet documented; §§ 5a, 2 and 2a read 2026-08-30)
- Used for: certification as a formal conformity check and a condition of the relief; **and the load-bearing part is now provable from the text rather than inferred from a silence.** § 5a reads in full: "*Die Zertifizierungsstelle erteilt die Zertifizierung nach § 2 Abs. 3, wenn ihr die nach diesem Gesetz erforderlichen Angaben und Unterlagen vorliegen sowie die Vertragsbedingungen des Basisrentenvertrags dem § 2 Absatz 1 oder Absatz 1a sowie dem § 2a entsprechen und der Anbieter den Anforderungen des § 2 Absatz 2 entspricht.*" The conditions imported are therefore **§ 2 Abs. 1 or 1a and § 2a only**; § 2 Abs. 1 in turn does nothing but require the contract to satisfy § 10 Abs. 1 Nr. 2 Buchst. b Doppelbuchst. aa EStG. **The Riester *Beitragserhaltungsgarantie* lives in § 1 Abs. 1 Satz 1 Nr. 3, which § 5a does not reach** — so a Basisrente may be sold with a full guarantee, a partial one or none at all, which is why the two subsidised layers diverged after the interest-rate collapse and why `Riester_DE_S` and `Basis_DE_S` are different models rather than one with a switch. **The 1 January 2010 start date for compulsory certification was not established and stays [unverified]**; nothing in the retrieved text dates it. The certifying authority is the *Bundeszentralamt für Steuern*, named in that role at [R11] and in the GDV model conditions at [S12]

(delib-basisrente-r10)=

### R10 — AltZertG § 1 and § 2 Abs. 2 — what certification is, and the guarantee it does not extend
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provisions
- URL: `https://www.gesetze-im-internet.de/altzertg/__1.html` (human-facing link only)
- Retrieved: **yes** (canonical XML, same *Stand* as [R9]; §§ 1, 2 and 2a read 2026-08-30)
- Used for: the Riester conditions § 5a does **not** pick up. Two are now located exactly. The *Beitragserhaltungsgarantie* is **§ 1 Abs. 1 Satz 1 Nr. 3** — the undertaking that at the start of the payout phase "*zumindest die eingezahlten Altersvorsorgebeiträge für die Auszahlungsphase zur Verfügung stehen*" — and the five-year spreading is **§ 1 Abs. 1 Satz 1 Nr. 8**, "*die vorsieht, dass die angesetzten Abschluss- und Vertriebskosten gleichmäßig mindestens auf die ersten fünf Vertragsjahre verteilt werden, soweit sie nicht als Prozentsatz von den Altersvorsorgebeiträgen abgezogen werden*". Both sit in the *Altersvorsorgevertrag* definition, and **§ 5a reaches neither**.
  **Gap 8 is resolved, and in the affirmative, but by a different route.** The AltZertG does not impose the five-year spreading on a Basisrente. **VVG § 165 Abs. 2 does**: the paid-up benefit is computed on the *Rückkaufswert* of § 169 Abs. 3, whose floor is "*das Deckungskapital, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt*" [R14] — and since a *Beitragsfreistellung* is the only exit a Basisrente has, the floor binds it. The GDV model conditions state exactly that at § 10 Abs. 1, and CosmosDirekt's LA 1079 A at § 8 Abs. 1 [S1] [S12]. **`zill_spread_y = 5` is therefore a cited fact, not a [std] choice.**
  § 2a is the third thing this entry now carries: a Basisrentenvertrag "*darf ausschließlich die nachfolgend genannten Kostenarten vorsehen*" — a closed list of six charge bases plus three event charges — which is the statutory shape of the model's charge set. And the statement repeated in every delib document that mentions certification, that **certification is expressly not a seal of quality**, is consistent with § 2 Abs. 3, which defines it as the *Feststellung* that the terms match §§ 2 Abs. 1/1a and 2a and nothing more

(delib-basisrente-r11)=

### R11 — AltZertG § 7 and the *Produktinformationsstelle Altersvorsorge*
- Publisher / doc type: Bundesministerium der Justiz / juris; Produktinformationsstelle Altersvorsorge gGmbH (PIA), Kaiserslautern; statutory provision and the body administering it
- URL: `https://www.gesetze-im-internet.de/altzertg/__7.html` (human-facing link only); the implementing regulation is the **AltvPIBV**, `https://www.gesetze-im-internet.de/altvpibv/BJNR141300015.html`
- Retrieved: **yes** — § 7 and § 7a AltZertG as canonical XML (same *Stand* as [R9]) and the AltvPIBV in full, both read 2026-08-30
- Used for: the pre-sale information regime behind [S13], which the entry can now set out instead of gesturing at. § 7 Abs. 1 lists **fifteen** mandatory fields, of which the ones that matter here are Nr. 7 the *Chancen-Risiko-Klasse*, Nr. 9 the cost schedule broken out by each § 2a heading, Nr. 10 the *Angaben zum Preis-Leistungs-Verhältnis* (under which the *Effektivkosten* sit), Nr. 12 the insolvency safeguard, Nr. 13 **information on *Anbieterwechsel* and *Kündigung***, and Nr. 14 the consequences of a *Beitragsfreistellung*. § 7 Abs. 4 requires a ***Muster*-PIB for assumed terms of 12, 20, 30 and 40 years**, published on the provider's own website — which is why two could be retrieved at [S13] when no individual PIB can be. § 7 Abs. 2 adds a point the drafted entry did not have: the PIB replaces the VVG-InfoV product information sheet, and **"*Eine Modellrechnung nach § 154 des Versicherungsvertragsgesetzes ist für zertifizierte Altersvorsorgeverträge und für zertifizierte Basisrentenverträge nicht durchzuführen*"**, nor may one be attached — so [REG-R25]'s *Modellrechnung* does not apply to this product.
  The AltvPIBV supplies the mechanics: § 5 puts every contract in **CRK 1 to 5** on the PIA simulation, computed separately for each of the four assumed terms; § 8 Nr. 3 defines the *Effektivkosten* as "*die Minderung der Wertentwicklung des Vertrags bis zum Beginn der Auszahlungsphase durch Kosten in Prozentpunkten*"; and § 10 fixes the returns they are computed against — **2 / 3 / 4 / 5 / 6 % for CRK 1 to 5** for the *Effektivkosten*, and four scenarios per CRK for the benefit projections, **−1 %, 2 %, 5 % and 6 % for CRK 4**. **Gap 7 is closed.** `product-spec.md`'s statement that **delib does not implement the PIA simulation** stands unchanged

(delib-basisrente-r12)=

### R12 — ZPO § 851c — Pfändungsschutz bei Altersrenten
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/zpo/__851c.html` (human-facing link only; a 6 kB shell)
- Retrieved: **yes** (canonical XML, Stand: neugefasst durch Bek. v. 5.12.2005 I 3202, zuletzt geändert Art. 2 G v. 22.12.2025 I Nr. 349; §§ 851c and 851d read 2026-08-30)
- Used for: the third leg of the product in `product-spec.md`, beside the relief and the prohibitions. **The four conditions of Abs. 1 are confirmed verbatim**: the benefit must be paid "*in regelmäßigen Zeitabständen lebenslang und nicht vor Vollendung des 60. Lebensjahres oder nur bei Eintritt der Berufsunfähigkeit*"; "*über die Ansprüche aus dem Vertrag nicht verfügt werden*" darf; "*die Bestimmung von Dritten mit Ausnahme von Hinterbliebenen als Berechtigte ausgeschlossen ist*"; and "*die Zahlung einer Kapitalleistung, ausgenommen eine Zahlung für den Todesfall, nicht vereinbart wurde*" — the same four features § 10 demands. **The § 851c age is 60, not 62** — gap 10 confirmed and now quotable, and the two provisions must still not be merged.
  **Gap 9 is closed, and the reason the practitioner ladders contradicted each other is now visible.** Abs. 2 as it currently stands has only **two bands**, not the multi-rung ladder the summaries carried: annual savings are protected up to **6 000 €** for a debtor from 18 to the completed 27th year and **7 000 €** from 28 to the completed 67th, subject to an aggregate ceiling of **340 000 €** — which also confirms the figure [REG-R40] carried as [unverified]. Abs. 2 Satz 2 requires the amounts to be re-set every fifth year on 1 July in the *Pfändungsfreigrenzenbekanntmachung*, which is why any figure printed anywhere has a shelf life; and Satz 3 protects three tenths of any *Rückkaufswert* above the protected amount, up to three times the aggregate ceiling. The protection is a **by-product of the prohibitions**, and it is the principal non-tax reason a self-employed person buys the product

(delib-basisrente-r13)=

### R13 — ZPO § 851d, SGB II § 12, SGB XII § 90 — insolvency and means-testing
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provisions
- URL: `https://www.gesetze-im-internet.de/zpo/__851d.html` for the first of the three; not established for SGB II § 12 or SGB XII § 90
- Retrieved: **ZPO § 851d yes** (canonical XML, same *Stand* as [R12], read 2026-08-30); **SGB II § 12 and SGB XII § 90 no** — neither book is in the statutory cache and neither was fetched
- Used for: the surrounding protection — old-age provision whose realisation is contractually excluded being exempt from the means test — which with [R12] is the market's *insolvenzfest* and *Hartz-IV-fest* claim. **§ 851d is not what the entry assumed.** It reads in full: "*Monatliche Leistungen in Form einer lebenslangen Rente oder monatlicher Ratenzahlungen im Rahmen eines Auszahlungsplans nach § 1 Abs. 1 Satz 1 Nr. 4 des Altersvorsorgeverträge-Zertifizierungsgesetzes aus steuerlich gefördertem Altersvorsorgevermögen sind wie Arbeitseinkommen pfändbar.*" It is the **Riester** counterpart of § 851c and reaches a *Basisrentenvertrag* only through VVG § 168 Abs. 3 Nr. 2 [R14]; it is not an insolvency provision. **The two SGB addresses stay [unverified]** and the means-test conditions were not established. The social-insurance treatment of the annuity in payment (gap 21) was likewise not established: the ~18 % figure is unsupported. The direction is not in doubt

(delib-basisrente-r14)=

### R14 — VVG § 165 *Prämienfreie Versicherung* (the *Beitragsfreistellung*), § 168 *Kündigung des Versicherungsnehmers*, § 169 *Rückkaufswert*
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provisions
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html`, `.../__168.html`, `.../__169.html` (human-facing links only; §§ 165 and 153 are 4–5 kB shells)
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; §§ 153, 163, 165, 168, 169 and 171 read 2026-08-30)
- Used for: the exits, and what becomes of them here. **§ 165 survives intact** and is the product's only behavioural exit, which is the whole of `bf_rate`, `pols_paidup` and the premium-free account block — and the reason `model.md` insists a freeze is a transfer between ledgers rather than a decrement. § 165 Abs. 2 adds the computational rule that carries `zill_spread_y`: the paid-up benefit is calculated "*unter Zugrundelegung des Rückkaufswertes nach § 169 Abs. 3 bis 5*", whose floor is the reserve on a five-year spreading of acquisition and distribution costs (see [R10]). **§ 169 is inoperative** as a payment: there is a *Deckungskapital* and no duration at which any part of it is payable as capital, which is why the model has no surrender cells, no *Stornoabzug* and no floor under `prem_to_av_pp` — but its Abs. 3 is very much operative as the *measure* of the paid-up benefit, which is a distinction the drafted entry did not draw.
  **§ 168 is the entry's error and is corrected.** The termination right does **not** "survive but have nothing to pay out": it is disapplied by statute. § 168 Abs. 3 reads "*Die Absätze 1 und 2 sind nicht auf einen für die Altersvorsorge bestimmten Versicherungsvertrag anzuwenden, 1. wenn die Vertragsparteien bei einem nach § 5a des Altersvorsorgeverträge-Zertifizierungsgesetzes zertifizierten Basisrentenvertrag die Verwertung der Ansprüche gemäß § 10 Absatz 1 Nummer 2 Satz 1 Buchstabe b des Einkommensteuergesetzes ausgeschlossen haben*". The practical outcome the documents describe is nonetheless right, because carriers grant a contractual termination anyway and word it as a conversion: CosmosDirekt LA 1079 A § 7 Abs. 1 and the GDV model conditions § 9 Abs. 3 both say a *Kündigung* turns the contract paid-up and pays no *Rückkaufswert* [S1] [S12]. Where the statutory disapplication bites visibly is the single-premium contract, which LA 1079 A § 7 Abs. 2 declares "*auf Grund der gesetzlichen Restriktionen ... über die gesamte Vertragsdauer nicht kündbar*". **How individual AVB word the exits is no longer [unverified]** — two wordings were read — and the outcomes are settled

(delib-basisrente-r15)=

### R15 — VVG § 153 — Überschussbeteiligung
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` (human-facing link only; a 5 kB shell)
- Retrieved: **yes** (canonical XML, same *Stand* as [R14]; § 153 read 2026-08-30)
- Used for: the policyholder's statutory entitlement to a share of the *Überschuss* and of the *Bewertungsreserven*, which a Basisrente holds **on exactly the same terms as any other German life contract** — the layer changes the tax and the exits, not the surplus machinery. The half-share is Abs. 3 Satz 2: "*Bei der Beendigung des Vertrags wird der für diesen Zeitpunkt zu ermittelnde Betrag zur Hälfte zugeteilt und an den Versicherungsnehmer ausgezahlt*".
  **Abs. 4 is the sentence this product turns on, and the drafted entry did not have it**: "*Bei Rentenversicherungen ist die Beendigung der Ansparphase der nach Absatz 3 Satz 2 maßgebliche Zeitpunkt.*" So the allocation date for an annuity contract is the end of the accumulation phase **as a matter of statute**, not merely because no earlier exit exists — which is exactly the single-date `terminal_bonus_rate` in `fund_at_conv()`. CosmosDirekt's LA 1079 A § 2 Abs. 2 c) implements it and adds two further trigger dates the model does not carry: **death, where a survivor's benefit is insured, and a transfer to another provider** [S1].
  **Gap 17 is closed by observation.** The claim that the *Überschussverwendung* options are narrower in the *Aufschubphase* was an inference; two retrieved wordings now show it. LA 1079 A applies the annual surplus to a *Bonussumme* and offers a cash-paying system at no point before *Rentenbeginn*, and at *Rentenbeginn* offers only *dynamische Rente* or *Zusatzrente* [S1]

(delib-basisrente-r16)=

### R16 — Deckungsrückstellungsverordnung (DeckRV) — Höchstrechnungszins and Höchstzillmersatz
- Publisher / doc type: Bundesministerium der Justiz / juris, with amendment by the Bundesministerium der Finanzen; regulation
- URL: **now established**: `https://www.gesetze-im-internet.de/deckrv_2016/` — the *Deckungsrückstellungsverordnung* of 18 April 2016, whose slug the drafting session could not find
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250; §§ 2 and 4 read 2026-08-30)
- Used for: the two numbers in this model that are **not** standardizations, both now quotable. The ***Höchstrechnungszins*** is § 2 Abs. 1: "*wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf 1 Prozent festgesetzt*" — **the current text reads 1 %**, and the amending regulation of 19 July 2024 is the instrument that raised it from 0,25 %. That it **applies at conclusion and stays with the contract** is § 2 Abs. 2 Satz 1, verbatim: "*Bei Versicherungsverträgen mit Zinsgarantie gilt der von einem Versicherungsunternehmen zum Zeitpunkt des Vertragsabschlusses verwendete Rechnungszins für die Berechnung der Deckungsrückstellung für die gesamte Laufzeit des Vertrages.*" That is the `gtd_rate` column and the guarantee-vintage ladder model points 6, 7 and 8 exercise. The ***Höchstzillmersatz*** is § 4 Abs. 1 Satz 2: "*Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten*", and § 4 Abs. 4 fixes it at conclusion for the whole term in the same way. The GDV model conditions restate the cap in customer language as "*2,5 % der von Ihnen während der Laufzeit des Vertrages zu zahlenden Beiträge*" [S12].
  **What stays [unverified]**: that the 1 January 2025 effective date is the amending regulation's, that the DAV recommends 1,00 % for 2026, that the LVRG cut the *Zillmersatz* from 40 ‰ in 2015, and the full vintage ladder — none of those is in the retrieved text, and none was separately checked

(delib-basisrente-r17)=

### R17 — DAV 2004 R — the annuity table
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV), Köln; actuarial table and its derivation guideline
- URL: **not established.** The DAV's own host was not reached on 2026-08-30 and the table is in any case not published free of charge
- Retrieved: **no** — the table itself was not opened and delib has never seen it. **Its use is now corroborated at one remove**, in three retrieved documents: CosmosDirekt LA 1079 A § 1 Abs. 1 names "*einer anerkannten Sterbetafel (DAV 2004R)*" as the basis of the guaranteed *Rentenfaktor* [S1], the GDV model conditions leave the table name as a per-company blank on the same sentence [S12], and BMF Rz. 19 requires the contract to oblige the provider "*vor Rentenbeginn die Leibrente auf Grundlage einer anerkannten Sterbetafel zu berechnen und dabei den während der Laufzeit der Rente geltenden Zinsfaktor festzulegen*" [R18]
- Used for: the mortality basis of the whole product. That DAV 2004 R is a ***Generationentafel*** — the improvement inside the table rather than applied on top — is why `mort_rate_at_age` takes a calendar year and why `cal_year(t)` is carried; that **first-order probabilities carry prudential margins and price the guaranteed *Rentenfaktor*** while second order is the best estimate is the wedge `mort_be_factor` and `ann_bonus_rate` sit either side of.
  **The conversion basis in this entry was wrong and is corrected.** The "DAV 2004 R at 0 % p.a." was a Schicht-3 observation and does not describe a Basisrente: CosmosDirekt's Basisrente wording strikes the guaranteed factor on DAV 2004 R at "*des tariflichen Garantiesatzes (Rechnungszins) von 1,25 Prozent p. a.*", the tariff's own rate [S1]. **A guaranteed *Rentenfaktor* level now also exists in the corpus** and gap 4 is closed as to existence: NÜRNBERGER's *Muster*-PIB gives **24,94 € of monthly annuity per 10 000 € of capital, guaranteed, at age 67 on a 2025 contract** [S13]. **The table is not public and delib does not redistribute it**: `mort_table.csv` is a **[std]** proxy anchored at `qx(67) = 0.014000`, and the entry carries what a replacement must preserve. The [std] view that a non-surrenderable annuity should select *lighter* than a Schicht-3 portfolio stays **[unverified]**: still no evidence either way

(delib-basisrente-r18)=

### R18 — BMF-Schreiben on Vorsorgeaufwendungen and Altersbezüge
- Publisher / doc type: Bundesministerium der Finanzen; consolidated administrative circular, *Einkommensteuerrechtliche Behandlung von Vorsorgeaufwendungen*, **BMF vom 24.05.2017 (BStBl I S. 820), IV C 3 – S 2221/16/10001 :004 – 2017/0392623**, as amended by BMF v. 06.11.2017 (BStBl I S. 1455), v. 28.09.2021 (BStBl I S. 1833), v. 16.12.2021 (BStBl I 2022 S. 155) and v. 28.12.2023 (BStBl I 2024 S. 209)
- URL: `https://amtliche-handbuecher.bundesfinanzministerium.de/esth/2024/C-Anhaenge/Anhang-01a/II/inhalt.html` — the circular as reproduced in the *Amtliches Einkommensteuer-Handbuch* 2024, Anhang 1a II. The `esth.` and `ao.` mirrors of the same host answer with a bot-check page and are not usable
- Retrieved: **yes** (HTML, ~1,15 MB, read 2026-08-30; Rz. 16 to 34 and the *ergänzende Absicherung* section read closely). **Gap 23 is closed for the BMF file number**
- Used for: **the operational detail the statute does not spell out — and the entry can now give it rather than disclose its absence.** All four of the points it listed as unestablished are answered.
  **The 50 % test and how it is computed**, Rz. 38: "*Die ergänzende Absicherung ist nur dann unschädlich, wenn mehr als 50 % der Beiträge auf die eigene Altersversorgung des Steuerpflichtigen entfallen. Für das Verhältnis der Beitragsanteile zueinander ist regelmäßig auf den konkret vom Steuerpflichtigen zu zahlenden (Gesamt‑)Beitrag abzustellen. Dabei dürfen die Überschussanteile aus den entsprechenden Risiken die darauf entfallenden Beiträge mindern.*" The denominator is the actual total premium, and rider surplus may be netted off the rider's share. Rz. 42 adds that the old-age cover and the supplementary cover must sit in **one contract**, failing which they are independent policies taxed under § 10 Abs. 1 Nr. 3a. Two allocation rules bear directly on the model's survivor and BUZ switches: Rz. 39 assigns a *Beitragsbefreiung* on disability to the old-age side, provided it only continues to build the annuity, and Rz. 41 does the same where "*die Hinterbliebenenversorgung ausschließlich aus dem bei Tod des Steuerpflichtigen vorhandenen Altersvorsorge-(Rest)kapitals finanziert*" is — which is precisely CosmosDirekt's RBH design [S1], so that survivor form consumes none of the 50 %.
  **A change of provider**, Rz. 29: "*Der Vertrag darf zulassen, dass die Ansprüche des Leistungsempfängers aus dem Vertrag unmittelbar auf einen nach § 5a AltZertG zertifizierten Vertrag ... des Leistungsempfängers auch bei einem anderen Unternehmen übertragen werden. Dabei ist lediglich die Übertragung innerhalb der jeweiligen Produktgruppe ... zulässig. Dieser Vorgang ist steuerfrei nach § 3 Nummer 55d EStG.*" So a transfer is **permitted, not required** — the contract *may* allow it — it is tax-free, it must stay within Basisrente-Alter or Basisrente-Erwerbsminderung, and the transferred capital is not a fresh contribution. **Gap 13 is closed**, and the two forms it takes in the market are both visible: CosmosDirekt grants it free of charge [S1], NÜRNBERGER and WWK exclude it on their PIBs [S13].
  **The administrative tolerance for a small annuity**, Rz. 16: "*Abweichend hiervon ist eine vertragliche Vereinbarung, wonach bis zu zwölf Monatsleistungen in einer Auszahlung zusammengefasst werden können, zulässig*" — with the *Kleinbetragsrente* commutation at Rz. 34, available only from the start of the payout phase and no earlier than the age floor. **Gap 19 is closed.**
  Two further readings worth carrying: Rz. 18 forbids a planned decline in the annuity and requires that the annuity computed at the start of the payout phase on the guaranteed capital plus irrevocably allocated surplus "*während der gesamten Auszahlungsphase nicht unterschritten werden darf*"; and Rz. 21–22 exclude a *Auszahlungsplan*, and a *Auszahlungsplan* followed by partial annuitisation, from qualifying as a lifelong annuity at all. **What the entry still does not carry is the *Rentenfreibetrag* mechanics**: those are in a different circular, on § 22 rather than § 10, which was not retrieved

(delib-basisrente-r19)=

### R19 — BFH, 19 May 2021 — the Doppelbesteuerung judgments
- Publisher / doc type: Bundesfinanzhof; two decisions of the same day, **X R 33/19** (ECLI:DE:BFH:2021:U.190521.XR33.19.0) and **X R 20/19**
- URL: `https://www.bundesfinanzhof.de/en/entscheidungen/entscheidungen-online/decision-detail/STRE202110106/` for X R 33/19; the companion sits at `.../STRE202110105/`
- Retrieved: **yes** for X R 33/19 (HTML, ~130 kB, read 2026-08-30, *Leitsätze* and grounds); the companion was located but only its file number was taken. **The case numbers and the date of 19 May 2021 are confirmed and the tags go**
- Used for: the framing of the tax section in `product-spec.md`, which the *Leitsätze* now support directly. Leitsatz 1 holds the 2005 system change and the basic architecture of the transition **constitutional**. Leitsatz 2 sets the test: a taxpayer who proves double taxation in his own case may have a constitutional claim to relief in the payout phase, and "*Eine solche doppelte Besteuerung ist nicht gegeben, wenn die Summe der voraussichtlichen steuerfrei bleibenden Rentenzuflüsse mindestens ebenso hoch ist wie die Summe der aus versteuertem Einkommen aufgebrachten Altersvorsorgeaufwendungen*", on the *Nominalwertprinzip*. Leitsätze 3 and 4 fix what may enter each side. On the facts the appeal was dismissed as unfounded, and the appellant was a *Freiberufler* who had paid at the ceiling since 1984 — this product's own buyer. **One qualification the entry should carry**: the proposition that the schedule will produce double taxation for *later* cohorts is not in the *Leitsätze*; it is the court's press framing of what its method implies, and it is on that footing that `product-spec.md` uses it. The legislative response was [R7] and [R6]

(delib-basisrente-r20)=

### R20 — Sozialversicherungsrechengrößen-Verordnung — the BBG series
- Publisher / doc type: Bundesministerium für Arbeit und Soziales, with the consent of the Bundesrat; annual regulation. The current instruments are the ***Sozialversicherungsrechengrößen-Verordnung 2026*** (SVBezGrV 2026) and its 2025 predecessor
- URL: `https://www.gesetze-im-internet.de/svbezgrv_2026/BJNR1160A0025.html` and `https://www.gesetze-im-internet.de/svbezgrv_2025/BJNR16D0A0024.html`
- Retrieved: **yes** — both, read 2026-08-30. § 3 Abs. 1 of the 2026 regulation sets the *Beitragsbemessungsgrenze* "*in der knappschaftlichen Rentenversicherung auf **124 800 Euro** jährlich; umgerechnet auf den Monat ergeben sich 10 400 Euro*"; the 2025 regulation gives **118 800 Euro**
- Used for: the inputs to the *Höchstbetrag* arithmetic at [R2]. **Gap 11 is closed for the two years that matter.** 124 800 × 24,7 % = 30 825,60, rounded up under § 10 Abs. 3 Satz 1 EStG to **30 826 €** — the 2026 ceiling and model point 9's premium; 118 800 × 24,7 % = 29 343,60 → **29 344 €** for 2025. The 2023 and 2024 lines reproduce on the same arithmetic from 107 400 € and 111 600 €, **which were not separately retrieved and are the two figures in the series that still rest on arithmetic alone**. Its real weight in these documents is unchanged and is a warning: **this instrument has to be re-read every year for this product in a way that is not true of any other delib product**, which is why the *Höchstbetrag* appears in the "living texts" paragraph of `product-spec.md` and in the model risks of `technical-notes.md`. That the *Bemessungsgrenzen* are uniform across the former East and West from 2025 stays **[unverified]** — the retrieved sections give a single national figure for the *knappschaftliche* branch, which is consistent with it but does not state it

(delib-basisrente-r21)=

### R21 — BaFin — Wohlverhaltensaufsicht and value for money
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht; supervisory *Merkblatt*, thematic publications and articles
- URL: not established. `bafin.de` is reachable from this build environment, but the *Merkblatt* path tried on 2026-08-30 returned **HTTP 404** and no replacement was located
- Retrieved: **no** — no BaFin document was opened; the supervisory material is still carried over from `_research/kapitallebensversicherung.md`, where it concerned the endowment chassis rather than this layer. The reason has changed — the host no longer refuses the environment; the document was simply not found at the address the sibling file recorded
- Used for: the single statement in `product-spec.md` that **a Basisrente is squarely inside the conduct-supervision perimeter** for capital-forming life products sold through commissioned intermediaries, the *Effektivkosten* on the § 7 AltZertG *Produktinformationsblatt* being the number that supervision runs on. **The second half of that is now sourced elsewhere**: § 7 Abs. 1 Satz 2 Nr. 9 and 10 AltZertG make the cost schedule and the *Effektivkosten* mandatory pre-sale disclosure, and the AltvPIBV fixes how they are computed [R11]. **Nothing Basisrente-specific was established from BaFin** and gap 15 stands

(delib-basisrente-r22)=

### R22 — GDV and BMF statistics on the Basisrente stock and new business
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft; Bundesministerium der Finanzen; annual statistics
- URL: not established. The GDV's own site is reachable — its *Musterbedingungen* index was retrieved at [S12] — but **no statistical publication on the Basisrente stock or new business was located on it**, and none was searched for
- Retrieved: **no** — not one statistic was opened
- Used for: **nothing quantitative, which is still the point.** The entry carries the disclosure in `product-spec.md` that **no market statistic of any kind was established** — contract stock, new business, average contribution, the *klassisch*/*fondsgebunden* split and the distribution-channel split are all [unverified] general knowledge given as orders of magnitude — and the instruction that **nothing downstream may cite a delib figure for the size of the Basisrente market**. **Gap 3 is narrowed on one point only**: [S16] observes fund-linked Basisrente tariffs, with and without an 80 % guarantee, at five large carriers at once, which is evidence that the fund-linked form is a market staple. It is not a market share and may not be reported as one

(delib-basisrente-r23)=

### R23 — EStG § 93 Abs. 3 — the Kleinbetragsrente, and its reach into Schicht 1
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__93.html` (human-facing link only)
- Retrieved: **yes** (canonical XML, same *Stand* as [R1]; § 93 Abs. 3 read 2026-08-30)
- Used for: **the de-minimis exception to the *Kapitalisierungsverbot*, which the retrieved text now settles in every particular.** § 93 Abs. 3 Satz 1: "*Auszahlungen zur Abfindung einer Kleinbetragsrente zu Beginn der Auszahlungsphase gelten nicht als schädliche Verwendung.*" Satz 2 Nr. 1 defines it as an annuity which, on an even annuitisation of the whole capital available at the start of the payout phase, "*eine monatliche Rente ergibt, die **1,5 Prozent** der monatlichen Bezugsgröße nach § 18 des Vierten Buches Sozialgesetzbuch nicht übersteigt*". **The 1 % / 1,5 % contest is resolved: the current law is 1,5 %.** Both readings were right at different times — the GDV model conditions of 21 July 2025 still print 1 % [S12], and the figure was raised by the 2026 amendment that also added the *Auszahlungsplan* limb of Satz 2 Nr. 2 for payouts from 1 January 2027 [REG-R44]. Satz 3 requires all of the taxpayer's contracts at one provider to be aggregated for the test.
  **Schicht 1 is not excluded from it, and the cross-reference is now exact.** § 10 Abs. 1 Nr. 2 Satz 3 EStG permits the commutation of "*eine Kleinbetragsrente im Sinne von § 93 Absatz 3 Satz 2 **oder 4***" — **not** "Satz 2 and 3", which is what this entry said. The older form survives in the documents that pin an earlier version: BMF Rz. 34 says "*in Anlehnung an § 93 Absatz 3 Satz 2 und 3 EStG*" [R18], and CosmosDirekt's LA 1079 A § 1 Abs. 2 pins "*die im Jahr 2009 geltende Fassung*" [S1]. **The earlier delib drafting that recorded no de-minimis exception at all stays withdrawn**; [REG-R42] had the correct position throughout. Two further points the retrieved sources add: the commutation is available only **from the start of the payout phase and no earlier than the age floor**, and — per the GDV model conditions § 1 Abs. 3 — it is drafted as the **insurer's** right ("*Wir sind allerdings berechtigt*"), not the policyholder's, so it is not an option the policyholder can elect. And **an *Abfindung* is in fact offered in the market**: LA 1079 A § 1 Abs. 2 provides for one, which is the half of gap 19 this entry left open.
  The modelling consequence is unchanged and remains a **[std]** decision: `Basis_DE_S` does not implement the commutation branch, because `Riester_DE_S` already carries the mechanic. **Its stated reasons no longer hold** — the threshold is no longer contested and a carrier's AVB has now been read — so the decision should be defended as a scope choice rather than as an evidential one. What the test module asserts is that decision — model point 10, at 300,00 € a year, projects a small annuity and no lump sum — and the unimplemented branch is a named model risk

(delib-basisrente-r24)=

### R24 — Independent rating and market-analysis houses
- Publisher / doc type: **Institut für Vorsorge und Finanzplanung (IVFP)**, Altenstadt; **Franke und Bornberg**, Hannover; **Morgen & Morgen**, Hofheim; **Assekurata**, Köln; comparative product ratings and market studies
- URL: `https://www.ivfp.de/rating/basisrente/` for the IVFP; not established for the other three
- Retrieved: **no.** The IVFP's rating page answers 200 but its body is navigation and marketing copy with no rating table, and **not one rating, score or ranking was obtained from any of the four houses**
- Used for: naming, in the variations section of `product-spec.md`, the four houses a checker should go to for comparative analysis in this layer — the IVFP publishing the best-known Basisrente rating — and for the disclosure that **not one rating, score, ranking or figure was established**, so no downstream document may invent one. **The two carriers described as highly rated or broker-strong ([S4], [S6]) still rest on this entry and are still [unverified]**: their Basisrente tariffs are now named from an independent study [S16], but that study ranks nothing

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R1–R56 numbering, frozen; research
provenance in `_research/regulatory-actuarial.md`). **That page still records `Fetched: no` on
every entry**, and the ones marked there as search-corroborated were corroborated by a
*search-result summary*, never by a retrieved document. It is rewritten on its own schedule, not
here. **Several of the instruments it points at have now been retrieved and read for this
product**, and where that is so the bullet below says which local entry carries the reading.
Entries cited by the Basisrente documents:

- **REG-R1** — Directive 2009/138/EG (Solvabilität II): the framework the undiscounted cash flows feed, cited and never computed.
- **REG-R2** — Delegierte Verordnung (EU) 2015/35: why no contract-boundary rule, cost-of-capital rate or standard-formula shock in this library rests on a retrieved text.
- **REG-R4** — EIOPA risk-free term structures: the curves a best estimate would discount `liability_cf` on.
- **REG-R5** — VAG 2016 and its *Sparten*: the undertaking writing this contract is a Solvency II life insurer.
- **REG-R6** — VAG §§ 74–110 and § 40: best estimate plus risk margin, and the SFCR — the valuation layer that consumes these cash flows.
- **REG-R7** — VAG §§ 124/125: the *Sicherungsvermögen* the *klassisch* form's assets sit in, and the record that the AnlV quotas no longer bind this insurer.
- **REG-R8** — VAG § 138: premium adequacy, the rule that makes the *Höchstrechnungszins* a pricing cap and not merely a reserving one.
- **REG-R9** — VAG § 139: the *Überschussbeteiligung* and the *Sicherungsbedarf* test on *Bewertungsreserven* — why making the declared rate endogenous would need the insurer's whole HGB result.
- **REG-R10** — VAG §§ 140/145: the *RfB* the declared surplus is drawn from.
- **REG-R14** — DeckRV and its § 2: the *Höchstrechnungszins* as the statutory ceiling on `gtd_rate`. **Retrieved and quoted at [R16]**; the current text reads 1 %, and § 2 Abs. 2 fixes the rate at conclusion for the whole term.
- **REG-R15** — the *Höchstrechnungszins* rate history: the guarantee-vintage ladder from 2,75 % down to 0,25 % and back to 1,00 %, which is what makes an in-force model point carry its cohort's rate rather than today's. **Only the current 1 % was retrieved; the ladder itself is still unread and [unverified].**
- **REG-R16** — DeckRV § 4: the *Höchstzillmersätze*, 25 ‰ and the pre-2015 40 ‰ — the two shipped tariffs. **The 25 ‰ is retrieved and quoted at [R16]; the pre-2015 40 ‰ is not in the current text and stays [unverified].**
- **REG-R17** — DeckRV § 5 Abs. 3: the *Referenzzins* and the *Zinszusatzreserve*, an HGB reserve that bites hardest on exactly this business and that delib does not compute.
- **REG-R18** — MindZV: the 90 / 90 / 50 minimum allocation under the declared rate this model takes as a scenario.
- **REG-R19** — RfBV: the collective part of the *RfB*, behind the same scenario.
- **REG-R20** — LVRG 2014: the reduction of the *Zillmersatz* to 25 ‰ and the wider cost reform.
- **REG-R22** — VVG 2008 and § 171: the contract law that governs throughout, and the *halbzwingend* character of the provisions the product turns on.
- **REG-R23** — VVG §§ 8 and 152: the 30-day *Widerruf*, which applies here as to any German life contract and is not modelled.
- **REG-R24** — VVG § 153: the statutory *Überschussbeteiligung* and the half-share in the *Bewertungsreserven*, beside [R15].
- **REG-R25** — VVG §§ 154/155: the *Modellrechnung* and the *Standmitteilung*, the disclosure counterpart of [S15]. **Corrected here**: § 7 Abs. 2 AltZertG disapplies the § 154 *Modellrechnung* for a certified Basisrentenvertrag altogether and forbids attaching one to the PIB [R11].
- **REG-R27** — VVG § 163: the premium- and benefit-adjustment channel, recorded as a model risk on the guaranteed *Rentenfaktor* and not implemented.
- **REG-R28** — VVG §§ 165–170: the *prämienfreie Versicherung*, the *Kündigung*, the *Rückkaufswert* and the *Stornoabzug* — the last two inoperative here, which is the product's defining absence.
- **REG-R29** — VVG §§ 172–177: the *Berufsunfähigkeitsversicherung* chapter a BUZ is written under; its mechanics belong to `BU_DE_S`.
- **REG-R30** — VVG §§ 19, 37, 38, 157, 158: misstatement, payment default and the age-error rule, which apply unchanged and are not modelled.
- **REG-R31** — VVG §§ 6, 7 and 214 with the VVG-InfoV: the product-level cost-disclosure regime the § 7 AltZertG *Effektivkosten* sits on top of.
- **REG-R32** — PRIIPs: the regime behind the *Basisinformationsblatt* at [S14], reaching the unit-linked and hybrid forms.
- **REG-R33** — IDD and § 34d GewO: the distribution regime this product depends on, which is predominantly brokered.
- **REG-R34** — Unisex (EuGH C-236/09, AGG): why `sex` is a reporting-only model point column and may not enter pricing for contracts concluded from 21 December 2012.
- **REG-R35** — BaFin Merkblatt 01/2023 (VA): *angemessener Kundennutzen*, the conduct perimeter this product sits in, beside [R21].
- **REG-R36** — the BGH line of authority: the narrowing of the *Treuhänderklausel*, recorded as a model risk on the guaranteed *Rentenfaktor*.
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: the layer architecture, beside [R5].
- **REG-R39** — **EStG § 10 Abs. 1 Nr. 2 Buchst. b and Abs. 3**: the cross-product entry for the five prohibitions and the ceiling, and the **best-corroborated fact in the tax section** because [REG-R40] reaches the same product shape from a different statute in a different research sweep. It is the entry that says in terms that a Basisrente model offering only a level regular premium models the wrong product.
- **REG-R40** — ZPO §§ 850b and 851c: the *Pfändungsschutz* conditions and the **340 000 € aggregate ceiling**, both **now retrieved and confirmed at [R12]**, where the annual savings bands are also printed for the first time — 6 000 € to the completed 27th year and 7 000 € thereafter to the completed 67th. The summaries contradicted each other because the ladder was replaced by these two bands; the figures are re-set every fifth year.
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a and § 55 EStDV: the *Besteuerungsanteil*, the *Rentenfreibetrag* and the *Ertragsanteil* comparator, beside [R4].
- **REG-R42** — EStG § 10a and Abschnitt XI (§§ 79–99): cited here for one thing only — its record that the *Kleinbetragsrenten-Abfindung* of § 93 Abs. 3 is available **for Riester and Basisrente alike**, and that both products need a commutation test at annuitisation. **Confirmed at [R23] from the statute**, where the threshold is also fixed at 1,5 % of the monthly *Bezugsgröße* and the cross-reference corrected to § 93 Abs. 3 Satz 2 oder 4. It is the entry that corrects this product's earlier reading; the Riester subsidy machinery itself belongs to `Riester_DE_S`.
- **REG-R43** — AltZertG, the BZSt, the AltvPIBV and the PIA: certification, the *Produktinformationsblatt* and the CRK scale, beside [R9] and [R11].
- **REG-R44** — the Altersvorsorgereformgesetz 2026: the reform that closes Riester to new business from 1 January 2027 and **leaves the Basisrente untouched** — the one piece of forward-looking context in `product-spec.md`.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the *Unterschiedsbetrag* and the 12/62 rule — Schicht-3 mechanics that **reach a Basisrente at no point in its life**.
- **REG-R46** — ErbStG and SGB V §§ 226, 229, 240: the social-insurance treatment of an annuity in payment (gap 21), stated as a driver of the after-tax comparison and not asserted.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV's ownership of the tables: the first-order/second-order distinction the conversion wedge is built on, and the reason no DAV table ships.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: the generational annuity bases, beside [R17], and what a replacement for `mort_table.csv` must preserve.
- **REG-R50** — DAV 1997 I / RI / TI: the *Berufsunfähigkeit* decrement family a BUZ would need, which lives in `BU_DE_S`.
- **REG-R52** — Destatis: the only freely reusable German mortality series, the intended base for a user-supplied replacement table.
- **REG-R53** — the German life market in numbers: named beside [R24] as where comparative figures would come from, and from which **none was obtained for this product**.
- **REG-R54** — HGB §§ 341–341o and the RechVersV: the statutory *Deckungsrückstellung* the model's `av_at` and annuity obligation stand behind, and which delib does not compute.
- **REG-R55** — IFRS 17: a profit-participating Basisrente is a direct-participating contract measured under the variable fee approach; nothing here implements it.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional practice the 1,00 % for 2026 rests on.

---

## Provenance note

Extraction details — one entry per source with an extended content block, the twenty-two
mechanic sections, and the twenty-five-item gaps-and-caveats register — live in
`_research/basisrente.md`. That file is the citation ground truth for the S# and R# numbering
used here, and it was written with **no research channel of any kind**: egress was blocked and
the session's search budget was already exhausted when this product was reached. **The entries
above are no longer in that position.** On 2026-08-30 the German statutes and regulations this
product turns on were read as canonical XML with their *Stand* attached; two carriers' Basisrente
*Bedingungswerke*, the GDV's Basisrente and BUZ *Musterbedingungen*, two filled-in *Muster*-PIBs,
the consolidated BMF-Schreiben on *Vorsorgeaufwendungen* and an independent *Effektivkosten* study
were retrieved and read. Each entry says what was opened and what was not.

**Where the register now stands.** Closed by a retrieved document: **gap 2** (an *Effektivkosten*
figure and a full charge schedule, [S13] [S16]); **gap 4** (a guaranteed *Rentenfaktor* level,
24,94 € per 10 000 € at 67 on a 2025 contract, [S13]); **gap 5** (the GDV does publish Basisrente
model conditions, [S12]); **gap 7** (the PIB's field list, scenario set and five-class CRK scale,
[R11]); **gap 8** (the five-year spreading reaches this product through VVG § 165 Abs. 2, [R10]
[R14]); **gap 9** (the § 851c ZPO protected amounts, [R12]); **gap 13** (a provider transfer is
permitted but not compulsory, [R18] [S1]); **gap 18** (a Basisrente BUZ wording and the 50 % rule
in contractual terms, [S12]); **gap 19** (up to twelve monthly annuities may be combined, and a
*Kleinbetragsrenten-Abfindung* is offered in the market, [R1] [R18] [S1]); and **gap 23** for the
BMF file number, [R18]. Narrowed: **gap 1** (four carrier or model wordings read, sixteen carriers
still unreached); **gap 3** (the fund-linked form is observed at five carriers, but no market
statistic); **gap 6** (the PIB displaces the VVG-InfoV sheet and the § 154 *Modellrechnung*, but
its relation to the PRIIPs KID is still unestablished); **gap 11** (2025 and 2026 confirmed from
the *Sozialversicherungsrechengrößen-Verordnung*, 2023 and 2024 still arithmetic). Unchanged:
**gap 10** — the § 851c age condition (60) and the § 10 EStG floor (62) are different provisions
and must not be merged; **gap 12**, **gap 15**, **gap 21**; and **gap 23** for the
*Bundesgesetzblatt* citations, which are still not given because none was confirmed.

Two items are living texts and move on their own schedule (gap 24): the *Höchstbetrag* changes
every year with the *Sozialversicherungsrechengrößen-Verordnung* [R20], and the
*Besteuerungsanteil* changes every year by construction [R4] [R6]. A third has now been seen
moving: the *Kleinbetragsrente* threshold of § 93 Abs. 3 EStG stood at 1 % of the monthly
*Bezugsgröße* in the GDV model conditions of July 2025 and reads 1,5 % in the statute as amended
in 2026 [R23]. Check all three, and every paragraph number in these documents, before relying on
anything here.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-basisrente-r1
[R10]: #delib-basisrente-r10
[R11]: #delib-basisrente-r11
[R12]: #delib-basisrente-r12
[R14]: #delib-basisrente-r14
[R15]: #delib-basisrente-r15
[R16]: #delib-basisrente-r16
[R17]: #delib-basisrente-r17
[R18]: #delib-basisrente-r18
[R19]: #delib-basisrente-r19
[R2]: #delib-basisrente-r2
[R20]: #delib-basisrente-r20
[R21]: #delib-basisrente-r21
[R22]: #delib-basisrente-r22
[R23]: #delib-basisrente-r23
[R24]: #delib-basisrente-r24
[R4]: #delib-basisrente-r4
[R5]: #delib-basisrente-r5
[R6]: #delib-basisrente-r6
[R7]: #delib-basisrente-r7
[R8]: #delib-basisrente-r8
[R9]: #delib-basisrente-r9
[REG-R25]: #delib-reg-r25
[REG-R40]: #delib-reg-r40
[REG-R42]: #delib-reg-r42
[REG-R44]: #delib-reg-r44
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
