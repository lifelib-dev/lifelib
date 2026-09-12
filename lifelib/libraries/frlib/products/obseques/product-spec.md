# Product Specification

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26; see `sources.md`).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash flow modeling of the French **contrat obsèques** (funeral contract) in its
**capital form** (*contrat en capital*). It does not describe any single insurer's product.
Facts carrying a source tag — [S#] (primary product documents: *conditions générales*,
*notice d'information*, *document d'information clé*, and the CCSF *tableaux comparatifs*)
and [R#] (regulatory/actuarial references), both numbered per `_research/obseques.md`, and
[REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) —
were extracted from the cited document and resolve against `sources.md`. Values marked
**[std]** are standardizations introduced for the reference implementation; each [std] in a
parameter table carries a numbered footnote giving the rationale and, where the research file
recorded one, the observed range across insurers. Facts the research file could not verify
are flagged [unverified]. Euro amounts are printed with a decimal point and no thousands
separator so that every figure is machine-checkable; the source documents use the French
decimal comma (336,03 €) and the figures are transcribed unchanged.

Three product cells are specified. They are the same contract with one model point column
changed — the **premium form**, which is this product's signature:

- **RefOBS-VIA** — *primes viagères*, a level premium payable for life.
- **RefOBS-TMP** — *primes temporaires*, a level premium payable for a stated term.
- **RefOBS-UNI** — *prime unique*, a single payment at outset.

The **contrat en prestations** (services form), in which the same whole-life capital is tied
to a named, personalised list of funeral goods and services, is described here and declared
out of model scope — see Riders and options.

---

## Product overview and market role

The capital-form *contrat obsèques* is an **individual whole-life assurance** (*assurance vie
entière*) on the subscriber's own head, written under the Code des assurances (branche 20
Vie-Décès) or, for *mutuelles*, under Livre II du Code de la mutualité [S1] [S8] [S9] [S13].
The enabling provision is art. L. 132-1 CA — a person's life may be insured by themselves or
by a third party [R7]. Subscriber and insured are the same person in every retrieved contract
[S1] [S8]; one insurer additionally permits a member to insure a spouse, ascendant or
descendant [S9] [S12]. Cover is **lifelong and has no maturity date**: the contract ends only
on death, on *rachat* (surrender) or on lapse [S1] [S8] [S9] [S11]. There is no survival
benefit of any kind.

What makes it a *contrat obsèques* rather than a small whole-of-life policy is one sentence of
statute. Art. L. 2223-33-1 CGCT: "*Les formules de financement d'obsèques prévoient
expressément l'affectation à la réalisation des obsèques du souscripteur ou de l'adhérent, à
concurrence de leur coût, du capital versé au bénéficiaire.*" — the capital paid to the
beneficiary is **earmarked to the funeral, up to its cost** [R2] [REG-R38]. Art. L. 2223-33
CGCT makes such a *formule de financement d'obsèques* the only lawful way to pre-arrange and
pre-pay a funeral: advance offers of funeral services are otherwise prohibited [R1], and a
funeral operator has been barred since the décret n° 95-653 du 9 mai 1995 from holding a
client's money in advance of death [R21].

**Market and benchmark.** All market figures come from secondary summaries of a CCSF opinion
that could not itself be retrieved [R11], and are therefore [unverified]: more than 5.3 million
contracts in force in 2023, a portfolio of 1.8 bn €, about 190 000 deaths covered a year —
roughly 30 % of French deaths — and an average capital of about 5000 € [R14] [R15]. A widely
quoted figure of 5.7 million active contracts in 2024 could not be sourced to France Assureurs
and is likewise [unverified] [REG-R49]. Seven insurers independently state, in the same
footnote of their standardised tables, that a 5000 € capital "*est proche du coût moyen des
obsèques en France hors marbrerie*" [S5] [S6] [S7] [S10] [S14] [S15] [S16]; a secondary study
puts the average French funeral at 4730 € in 2025, split 5044 € *inhumation* / 4434 €
*crémation* [R22]; and up to 5965 € may be drawn from the deceased's bank account for funeral
costs, with 1500 € deductible from the estate [R17].

**The structural point that shapes everything below.** Since 1 July 2025 every French funeral
insurer publishes a **standardised comparison table** (*tableau d'exemples normalisés*) giving,
for a 5000 € guaranteed capital and entry ages 50 / 60 / 70, the annual premium, the cumulative
premiums by age at death and the surrender values by duration, for each premium form on offer
[R13] [R15]. Sixteen such tables from seven insurers were retrieved. They are the closest thing
to a public rate card that exists for any French life product, and they are the numerical
backbone of this specification. Each carries the line that it has no contractual value and that
the surrender values are shown *sans participation aux bénéfices* [S5] [S6] [S7] [S10] [S14]
[S15] [S16] — excellent for calibrating a mechanics demonstration, worthless as a pricing basis.

**Contrast with the UK over-50s sibling.** The UK guaranteed-acceptance whole of life plan in
`uklib/products/whole_of_life` is the same idea — guaranteed acceptance, a small fixed sum, a
first-year return-of-premium moratorium, premiums ceasing at a stated age. Three things differ,
and all three are first-order. (1) The capital is **not level**: it is uprated annually out of
the *participation aux bénéfices* [S1] [S2] [S15] [S16] or, at one insurer, by contract [S14].
(2) There **is** a surrender value, equal to the *provision mathématique* [S1] [S8] [S9] [S12],
because a whole-life funeral contract falls in art. L. 132-23 CA's residual *autres assurances
sur la vie* class, where the insurer may refuse neither *réduction* nor *rachat*. The article
withholds them from a closed list: temporary death assurance and immediate or in-payment life
annuities may carry **neither** *réduction* **nor** *rachat*, and survivorship capital and
annuity contracts, pure endowments and deferred annuities without return of premium may carry
**no** *rachat* [R10]. (3) Non-payment produces *réduction* (a paid-up contract), not forfeiture,
wherever the surrender value is sufficient [R7] [S1] [S8] [S9]. The UK design's "lapse is free"
arithmetic does not carry over.

---

## Representative specification

### Table 1 — Chassis, legal form, eligibility

| Parameter | Representative value | Basis |
|---|---|---|
| Product type | Individual whole-life assurance (*assurance vie entière*), branche 20 Vie-Décès; non-linked; participating; capital earmarked to the funeral | [S1] [S8] [S9]; [R1] [R2] [REG-R38] |
| Lives assured | Single life, subscriber = insured | [S1] [S8]; one insurer allows a relative [S9] [S12] |
| Cover term | None — cover to death; no maturity, no renewal, no conversion | [S1] [S8] [S9] [S11] |
| Underwriting | **Guaranteed acceptance — no medical questionnaire, no medical examination** | [S1] [S11] [S12] [S13] |
| Entry ages | 18–84 (*différence de millésime*) | [S1]; band choice **[std]** (a) |
| Age basis | *Différence de millésime* — calendar year of subscription minus calendar year of birth | [S1] [S8] [S9] |
| Residence | Metropolitan France, Monaco and the DROM; stays abroad limited | [S1]; variants [S8] [S11] |
| Prohibited lives | No death cover on a child under 12, an adult under *tutelle*, or a person in psychiatric hospitalisation; premiums fully refunded | [R7] [R21] |
| Anchor model point | Male, entry age 50, capital 5000 €, *primes viagères* 336.03 €/year, revalorisation 1.00 % p.a. | [S14]; cell **[std]** (b) |

Footnotes:
- (a) **[std]** entry band 18–84: observed windows are 18–84 [S1], 18–80 inclusive [S9] [S11]
  [S12], a band that **depends on the premium form** — 10-year temporary under 80, 15-year under
  75, 20-year under 70, 25-year under 65, lifetime premiums from 40 to under 86 [S8] — and a
  20-year term capped at entry 69 [S14]. 18–84 is the widest fully documented single band; the
  form-dependent band is carried as a variation. All standardised tables are published at entry
  ages 50, 60 and 70 [S5] [S6] [S7] [S10] [S14] [S15] [S16].
- (b) **[std]** anchor cell: entry 50 is the lowest published entry age and 5000 € the unanimous
  illustrative capital. Premium, revalorisation rate and surrender-value scale are all taken
  from **one** document [S14] so that the three are mutually consistent — it is the only
  retrieved contract carrying a *guaranteed* uprating together with surrender values that
  already reflect it. Which insurer to anchor on is the standardization.

### Table 2 — Capital amounts and caps

| Parameter | Representative value | Basis |
|---|---|---|
| Guaranteed capital range | 2000 – 10000 €, free choice | [S1]; nine fixed steps 2000/3000/…/10000 € at another insurer [S8] |
| Illustrative capital | 5000 € | [S5] [S6] [S7] [S10] [S14] [S15] [S16] |
| Aggregate cap per insured | 10000 € across all funeral capitals with the same insurer | [S1] [S8]; 17580 € at a third [S12] |
| Minimum after a reduction in cover | 2000 €, and not below the contract's *valeur de réduction* | [S1] |
| Capital increases | Permitted to age 84; the increment is priced at the age of the request and carries its **own fresh waiting period** | [S1]; one increase per year to age 86 elsewhere [S8] |
| Guarantee fund (FGAP) | 70000 € in aggregate per insured across capital contracts with a failed undertaking | [S11]; membership under art. L. 423-1 CA [S1] |
| Modeled capital | 5000 € at issue, uprated annually (Table 5) | [S14]; per-policy model, aggregate caps not modeled **[std]** (c) |

Footnotes:
- (c) **[std]** aggregate caps not modeled: they bind at the level of the insured across
  contracts (10000 € [S1] [S8], 17580 € [S12]), not per policy, and are immaterial to a
  per-policy expected-value projection. They matter only to the *primes manifestement
  exagérées* exposure discussed under Regulatory context.

### Table 3 — Premium forms, levels and payment

| Parameter | Representative value | Basis |
|---|---|---|
| Premium forms offered | *prime unique*; *primes temporaires* over 5 / 10 / 15 / 20 / 25 years or to a stated age; *primes viagères* | [S1] [S5] [S8] [S9] [R17] [R21] |
| Choice | **Final at inception** — the form cannot be changed later | [S1] |
| Payment | Annual in advance, with monthly / quarterly / half-yearly instalment options | [S1] [S8] [S9] |
| Instalment loading | 2.2 % from annual to monthly (4952.68 € annual vs 5061.48 € monthly on one documented cell) | [S11] |
| RefOBS-VIA premium | 336.03 €/year for life, entry 50, capital 5000 € | [S14] |
| RefOBS-TMP premium | 651.26 €/year for 10 years, entry 50, capital 5000 € | [S14] |
| RefOBS-UNI premium | 4274.04 € once, entry 50, capital 5000 € | [S5] |
| Premium indexation | Fixed at inception, never indexed | [S5] [S6] [S7] [S14] [S16]; **but** uprated in step with the guarantees at one insurer [S9] [S10] [S11] |
| Do lifetime premiums stop? | No cessation age in the reference cell | **[std]** (d) |
| Modeled instalment frequency | Annual in advance | **[std]** (e) |

Observed annual premiums for a 5000 € guaranteed capital, transcribed from the standardised
tables (a representative extract; the full set is in `_research/obseques.md` §7):

| Insurer / form | Entry 50 | Entry 60 | Entry 70 | Basis |
|---|---|---|---|---|
| CNP Trésor Prévoyance — *viager* / *temporaire* 10 ans / *prime unique* | 164.52 / 455.64 / 4274.04 | 234.24 / 502.68 / 4548.60 | 361.92 / 576.60 / 4819.56 | [S5] |
| La Banque Postale — *viager* / *prime unique* | 252 / 4305 | 313 / 4530 | 434 / 4772 | [S6] |
| Macif — *viager* / *jusqu'à 80 ans* | 232 / 266 | 325 / 406 | 499 / 793 | [S10] |
| AXA Serenova — *viager* / *temporaire* 10 ans | 336.03 / 651.26 | 390.68 / 663.61 | 524.23 / 693.43 | [S14] |
| Sogecap BUDGET — *viager* / *prime unique* | 250 / 4282 | 352 / 4530 | 534 / 4751 | [S15] |
| Mutex NÉOBSIA — *temporaire* 10 / 5 ans | 678 / 1240 | 695 / 1245 | not printed | [S2] |

Two readings of that table are load-bearing, and both are arithmetic on the printed figures
(`_research/obseques.md` §7), not quotations. The **single premium** is 85.5–86.1 % of the
capital at entry 50, 90.6–91.0 % at entry 60 and 95.0–96.4 % at entry 70; the three insurers
publishing one agree to within **0.7 percentage points at entry 50, 0.4 pp at entry 60 and
1.4 pp at entry 70** [S5] [S6] [S15] — the clearest public signal of the underlying reserving
basis, and tightest in the middle of the range. The **lifetime premium** ranges from 3.3 % to
6.7 % of the capital at entry 50, 4.7 % to 7.8 % at entry 60 and 7.2 % to 10.7 % at entry 70:
a spread of **2.0:1** between the cheapest and dearest insurer at entry 50 that **narrows with
age**, to 1.7:1 at 60 and 1.5:1 at 70. The often-repeated "2:1 at every age" holds only at the
youngest published entry age.

Footnotes:
- (d) **[std]** no cessation age for lifetime premiums: the retrieved tables disagree. One runs
  them to attained age 115 with no cessation [S15]; another to 95 with none shown [S5]; a third
  prints the same cumulative lifetime premium at ages 90 and 95 (9400 € in both columns), from
  which cessation near age 90 is **inferred, not stated** [S6]; a fourth sells an explicit
  "*jusqu'à vos 80 ans*" form alongside the lifetime one [S9] [S10]. The reference cell takes
  the documented no-cessation design [S15] because it produces the overrun the product is
  criticised for; `prem_cease_age` is a model point column, so the others are one row away.
- (e) **[std]** annual instalments: premiums are contractually annual and payable in advance
  [S1] [S8] [S9], and the published rate cards and cumulative-premium columns are annual [S5]
  [S14]. The 2.2 % annual-to-monthly loading is documented [S11] and is a model point column,
  not a re-tariffing.

### Table 4 — Délai de carence and benefit structure

| Parameter | Representative value | Basis |
|---|---|---|
| *Délai de carence* / *délai d'attente* | **12 months** from the effective date | [S1] [S8] [S9] [S11] [S12] [S13] |
| Accidental death | **Full capital from day 1**, waiting period does not apply | [S1] [S8] [S9] [S11] [S13] [R21] |
| Non-accidental death inside the waiting period | **Refund of the premiums collected**, to the balance beneficiaries | [S1]; net of the assistance premium at [S8]; net of instalment charges at [S9] |
| Interest on the refund | **None** in any retrieved contract | [S1] [S8] [S9]; the "refund with interest" design is [unverified] (f) |
| Death from month 13 | Full guaranteed capital as uprated (Table 5), any cause | [S1] [S8] [S9] |
| Accident definition | "*Toute atteinte corporelle … non intentionnelle …, provenant de l'action soudaine et imprévisible d'une cause extérieure*"; **cerebral and cardio-vascular events are never accidents**, whatever their origin; burden of proof on the claimant | [S1] for all three. A near-identical core wording — "*l'action violente, soudaine et imprévisible, d'une cause extérieure et non intentionnelle*" — at [S8], which carries **no** cerebral / cardio-vascular carve-out and excludes acute and chronic illness and harm from medical or surgical treatment instead. The market description adds myocardial infarction, coronary conditions and emotional shock [R21] |
| Accidental-death enhancement | 1× the capital | [S1] [S9] [S14]; **2× from year 2, capped at 20000 €, at one insurer** [S8] |
| Suicide | Excluded in the first 12 months, and again for the year following a capital increase | [S1] [S8] [S12] [S13] |
| Other exclusions | War, civil war, military conflict; nuclear transmutation and radiation; murder of the insured by a beneficiary (that beneficiary's share) | [S1] [S8] [S12] |
| Amount paid in an excluded case | The **valeur de rachat** / *provision mathématique* — not zero, not the capital | [S1] [S8] [S12] |
| Waiting period on a capital increase | A **fresh** period of the same length on the increment only | [S1] [S8] [S9] [S13] |
| Market cap on the waiting period | One year maximum for new contracts from 1 July 2025, against up to two years previously | [R13] [R14] [R15]; [unverified] against [R11] |

Footnotes:
- (f) **[unverified]** refund with interest: no retrieved contract pays interest on premiums
  refunded inside the waiting period [S1] [S8] [S9]. A different rule exists in statute and must
  not be confused with it — art. 8 of the loi Sueur requires the capital paid by the subscriber
  of an advance-***prestations*** contract to bear interest at not less than the legal rate
  [R6]. `carence_refund_rate` defaults to zero **[std]**.

### Table 5 — Revalorisation of the capital

| Parameter | Representative value | Basis |
|---|---|---|
| Mechanism | *Participation aux bénéfices* credited annually to the guaranteed capital | [S1] [S2] [S15] [S16]; statutory obligation [REG-R14] [REG-R15] |
| Frequency and eligibility | Annually, for contracts in force at least one year | [S1] [S9] |
| Effect on premiums | **Premiums unchanged** in the reference cell | [S5] [S6] [S7] [S14] [S16] |
| Rate, reference cell | **1.00 % p.a., contractually guaranteed**: "*le contrat prévoit une revalorisation annuelle de 1 % du capital souscrit sans augmentation de la cotisation*" | [S14] |
| Compounding | Compound on the current capital | **[std]** (g) |
| Illustrative discretionary rate | 1.2854 % p.a., derived from a KID performance scenario (3000 € → 3038.56 / 3633.50 / 4400.77 € at 1 / 15 / 30 years) | [S11], derivation in `_research/obseques.md` §10 |
| One insurer's PB formula | 90 % of technical and financial profits, after a 1 % management charge on funds under management and after the technical interest guaranteed at inception (art. A 335-1 CA) | [S16] [REG-R23] |
| Premium-linked variant | Capital **and remaining premiums** uprated at the same rate, credited to the *provision mathématique* on 1 April of the following year | [S9] [S10] [S11] |
| Post-mortem revalorisation | Capital uprated from death until receipt of the payment documents, at the lower of the 12-month average TME and the last TME at 1 November of the preceding year | [S1] [S8] [R8] [REG-R31] |

Footnotes:
- (g) **[std]** compound: the wording is "*1 % du capital souscrit*", which reads naturally as
  1 % of the **subscribed** capital — a simple uplift — while the same document's surrender
  values run to 7854.08 € against a 5000 € original capital at 45 years [S14], which pins down
  neither reading. Compounding on the current capital is adopted because that is the form the
  other retrieved mechanisms take (PB credited to the *provision mathématique*, which then earns
  in its turn [S9] [S16]) and because the one derivable rate in the file is demonstrably
  geometric [S11]. Which reading the wording intends is **[unverified]**; `reval_simple` is the
  variation flag.

### Table 6 — Rachat, réduction and non-payment

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender right | Yes; **total surrender only**, no partial. At any time [S1] [S9] [S11]; at one insurer only once **one annual premium** has been paid [S8] | [S1] [S8] [S9] [S11]; statutory basis [R10] |
| Surrender value | The **provision mathématique** at the effective date of the request | [S1] [S8] [S9] [S12] |
| Surrender penalty | **None** in the reference cell | [S1] [S11]; 5 % in the first 10 years, plus a 5 % charge inside the provision in the first 8, at one insurer [S8] |
| Payment deadline | 30 days | [S1] [S8]; 2 months at [S9] [S11]; statutory maximum 2 months [REG-R31] |
| Beneficiary acceptance | Acceptance makes the designation irrevocable and **blocks surrender** | [S1] [S8] [S11] |
| Non-payment path | 10 days, then a 40-day formal notice; at expiry either termination (surrender value nil or insufficient) or ***réduction*** | [R7] [S1] [S8] [S9] |
| Cover during the 40 days | **Suspended** — no death capital is payable in that window | [S1] |
| *Valeur de réduction* | Paid-up capital computed from the provision reached, the attained age, the technical rate and the contractual loadings | [S8]; from entry age, completed premium years, capital and premium form at [S1] |
| Automatic substitution | Surrender substituted for *réduction* where the surrender value falls below half the monthly SMIC | [S1] (art. R. 132-2 CA); 50 % of SMIC at [S8]; general power at [R10] |
| Assistance guarantees on *réduction* | Cancelled | [S1] [S8] [S9] |
| *Renonciation* (cooling-off) | 30 calendar days from being informed the contract is concluded; **full refund of all premiums** | [S1] [S8] [S11] [R7] [R21] [REG-R29] |

Observed surrender values for a 5000 € capital, transcribed as printed — **all nine published
quinquennial anchors**, because these six grids are exactly the ones shipped as
`surr_scale_table.csv` and an omitted anchor is an interpolated guess in the model (see
`technical-notes.md`, *Rachat and réduction*):

| Insurer, entry age, form | 5 yr | 10 yr | 15 yr | 20 yr | 25 yr | 30 yr | 35 yr | 40 yr | 45 yr | Basis |
|---|---|---|---|---|---|---|---|---|---|---|
| CNP, 50, *viager* | 650.15 | 1275.19 | 1876.68 | 2460.79 | 3004.02 | 3484.41 | 3876.12 | 4176.77 | 4399.53 | [S5] |
| CNP, 50, *prime unique* | 4162.06 | 4282.64 | 4398.69 | 4511.38 | 4616.18 | 4708.86 | 4784.43 | 4842.43 | 4885.41 | [S5] |
| AXA Serenova, 50, *viager* | 784.01 | 1574.90 | 2346.97 | 3151.33 | 3980.74 | 4828.57 | 5659.93 | 6429.96 | 7135.11 | [S14] |
| AXA Serenova, 50, *temporaire* 10 ans | 2701.65 | 5767.93 | 6003.11 | 6256.67 | 6530.11 | 6824.80 | 7142.86 | 7485.99 | 7854.08 | [S14] |
| Sogecap BUDGET, 70, *viager* | 1148 | 2067 | 2808 | 3369 | 3775 | 4129 | 4473 | 5000 | 5000 | [S15] |
| Mutex NÉOBSIA, 50, *temporaire* 25 ans | 981 | 1958 | 2933 | 3938 | **5074** | 5057 | 5043 | 5033 | 5026 | [S2] |

Three shapes, all first-order for the model. **Lifetime-premium values rise steadily but stay
well below the capital for decades** — 88 % of the capital after 45 years at entry 50 [S5]; the
one lifetime grid that does reach exactly 5000 € at 40 and 45 years is an entry-**70** case, by
which duration the insured is 110 [S15]. **Paid-up contracts — a single premium, or a temporary
term that has expired — sit just below the capital and drift up towards it**: the *prime unique*
value grows from 4162.06 € at 5 years to 4885.41 € at 45 [S5], the mathematical provision of a
paid-up whole life converging on the sum assured.
**Where the capital is uprated the surrender value overshoots the original capital** —
7854.08 € against 5000 € at 45 years [S14] — while one temporary-premium grid *peaks* at 5074 €
at 25 years and then declines, because a 0.40 % p.a. charge on the guaranteed capital keeps
running after the last premium [S1] [S2].

A common expectation that *primes viagères* carry no surrender value is **not supported by any
retrieved document**: five insurers publish lifetime-premium surrender values [S5] [S6] [S10]
[S14] [S15], which is what art. L. 132-23 CA requires. That article withholds *rachat* only from
a closed list — temporary death assurance and immediate or in-payment life annuities, which may
carry neither *réduction* nor *rachat*, and survivorship capital and annuity contracts, pure
endowments and deferred annuities without return of premium, which may carry no *rachat*. A
whole-life contract is none of those; it sits in the residual *autres assurances sur la vie*
class, where "*l'assureur ne peut refuser la réduction ou le rachat*" [R10]. The model therefore
carries a surrender value for every premium form.

### Table 7 — Charges

The three insurers that disclose a charge structure disclose three different structures.

| Charge | Mutex NÉOBSIA [S1] | VIASANTÉ / UCR [S8] | Macif [S9] [S12] |
|---|---|---|---|
| Entry / on premiums | 5 % of every premium | acquisition max 10 % of the annual premium (10.3 % lifetime) and in any case ≤ 2.5 % of the guaranteed capital; collection admin max 20 % of the annual premium | max 5.38 % of the capital guaranteed at subscription (4.89 % on top-ups), as an annual percentage over the average contract duration |
| Ongoing | 0.40 % p.a. of the guaranteed capital for life, **plus** 0.57 % p.a. while lifetime premiums are paid or 0.80 % p.a. while temporary premiums are | max 0.4 % p.a. of the guaranteed capital plus 3.3 % p.a. of the annual premium | none |
| Exit | none | 5 % inside the mathematical provision in the first 8 years; 5 % surrender penalty in the first 10 | none |
| Instalment / assistance | none / included | not stated / 12 €/year outside the above | yes / included |

One insurer puts a single number on the whole thing: a PRIIPs **reduction in yield of 1.77 %
p.a. over a 30-year holding** (24.08 % over 1 year, 4.86 % over 15), classified entirely as an
entry cost with zero ongoing, exit, transaction and performance costs; total costs 75 € / 1120 €
/ 1493 € at 1 / 15 / 30 years on a premium of 247.60 €/year, and a risk class of **2 of 7**
[S11]. Nothing in the retrieved set caps a French life charge — art. A. 132-8 CA requires maxima
to be *disclosed* in the *encadré*, not limited [REG-R30] — which is why every expense level in
the technical notes is **[std]**.

---

## Contractual mechanics

Notation is shared with `technical-notes.md`. Let *t* be the policy month (*t* = 1, 2, …),
*y* = policy year = floor((*t*−1)/12) + 1, *C(y)* the guaranteed capital in policy year *y*,
*P* the level annual premium, *CumPrem(t)* the premiums collected to the beginning of month
*t*, and *n_car* the waiting period in months.

### Death benefit and the délai de carence

From the effective date, **accidental** death pays the full guaranteed capital. **Non-accidental**
death inside the waiting period pays a refund of the premiums collected. Any death from month
*n_car* + 1 pays the guaranteed capital [S1] [S8] [S9] [S11] [S13]:

      DB_acc(t)   = k_adb x C(y)          k_adb = 1 for t <= n_car; 1 or 2 thereafter [S8]
      DB_illn(t)  = CumPrem(t)            if t <= n_car
                  = C(y)                  if t >  n_car

The refund is of premiums *collected*, so with an annual premium in advance it is a **step
function**, constant through the first twelve months, not a monthly accrual. Two insurers net
it down — of the assistance premium [S8], of instalment charges [S9]; the reference cell takes
the gross basis [S1] and carries the netting as a parameter.

The accident definition is narrow, and deliberately so: cerebral and cardio-vascular events are
never accidents whatever their origin, and the burden of proving the accidental cause lies on
the claimant [S1] — the market description adding myocardial infarction, coronary conditions
and emotional shock [R21], and the other contract that defines an accident narrowing it a
different way, by excluding acute and chronic illness and harm from medical or surgical
treatment [S8]. On a claim inside the waiting period the insurer requires a
**medical certificate stating whether the cause was illness, accident or suicide** [S1] [S8]
[S9]. The waiting period is the anti-selection device that replaces underwriting [R21]; it is
the whole of the insurer's protection against a guaranteed-issue book whose entrants may be 84
years old and know their own health.

### Premium forms and the overrun

      P(t) = P     if a premium falls due in month t and t is inside the paying period
           = 0     otherwise

with the paying period being month 1 only (*prime unique*), months 1 to 12·*n_term* (*primes
temporaires*), or all months (*primes viagères*). The choice is final at inception [S1].

Cumulative premiums under *primes viagères* grow without bound while the capital grows at most
at the revalorisation rate, so **the insured can and often does pay more than the capital**.
The KID says so in terms: "*Le total des cotisations payées pendant toute la durée du contrat
peut dépasser le montant du capital qui sera versé en cas de décès*" [S11]. The age at which
cumulative lifetime premiums first exceed a 5000 € capital, across entry ages 50 / 60 / 70, is
80–84 at one insurer, 70–82 at a second, 72–80 at a third, 65–80 at a fourth and 70–79 at a
fifth (arithmetic on the printed cumulative columns, `_research/obseques.md` §7); the largest
figure printed anywhere is **24019 € of lifetime premiums against a 5000 € capital**, for entry
age 70 surviving to 115 [S15]. That is what a consumer body means when it warns that "*la somme
totale des prélèvements en viager pourra être équivalente à plusieurs fois le prix des
obsèques*" [R21], and why the CCSF asked insurers to offer temporary alternatives
systematically alongside lifetime premiums [R13] [R15].

### Revalorisation of the capital

      C(y) = C_0 x (1 + r)^(y-1)                            reference cell, r = 1.00 % [S14]
      C(1) = C_0                                            no uprating in the first year [S1] [S9]

and, in the premium-linked variant, *P(y) = P_0 × (1 + r)^(y−1)* on the **remaining** premiums
[S9] [S10] [S11]. The uprating comes out of the *participation aux bénéfices*, whose statutory
machinery — the obligation at art. L. 331-3 CA [REG-R14], the *compte de participation aux
résultats* at arts. A. 132-10 to A. 132-15 [REG-R15] and the eight-year release horizon of the
*provision pour participation aux bénéfices* at art. A. 132-16 [REG-R16] — is set out once for
the whole library in `../assurance_vie_euro/technical-notes.md` and is **not restated here**.
What is specific to this product is where the money lands: on the **guaranteed capital**, not
on an account value, and generally with the premium left alone [S1] [S2] [S14] [S15] [S16].

A separate statutory duty is easy to confuse with it. Art. L. 132-5 CA requires the contract to
state the conditions under which the guaranteed capital is revalued **from the date of death**
until the payment documents are received, or until deposit at the Caisse des dépôts [R8]; two
insurers state the rate identically as the lower of the twelve-month average TME computed at
1 November of the preceding year and the last TME available at that date [S1] [S8]. Art.
L. 132-23-1 CA sets the clock it runs against — fifteen days to request documents, one month
from a complete file to pay, penalty interest at twice then three times the legal rate
[REG-R31] — and where a contract goes unclaimed the revalorisation continues until deposit with
the Caisse des dépôts, the proceeds becoming State property after twenty years there [REG-R39].

### Rachat, réduction and non-payment

A *rachat* is total only and pays the *provision mathématique* at the effective date of the
request [S1] [S8] [S9] [S12]; no partial surrender and no *avance* appears in the retrieved
capital contracts. Non-payment does **not** ordinarily terminate the contract: art. L. 132-20 CA
gives the insurer no action to compel payment, requires a registered letter ten days after the
due date, and provides that at the expiry of a further forty days continued non-payment produces
**either termination — where the surrender value is nil or insufficient — or *réduction*** [R7].
Every retrieved contract implements exactly that [S1] [S8] [S9], with cover **suspended during
the forty days** [S1]; one insurer splits by contract year, terminating in year 1 and reducing
from year 2 [S8]. *Réduction* leaves a paid-up whole-life contract with a smaller capital, no
further premiums and a continuing death liability; the reference implementation computes the
paid-up capital as the whole-life cover that the accumulated provision buys as a single premium
at the attained age, using the published *prime unique* rate card [S5] as that scale — see
`technical-notes.md`.

### Beneficiary designation and the earmarking rule

The default architecture is two-tier in every retrieved capital contract. The **first-rank
beneficiary** is the funeral firm that carried out the services, failing that whoever paid its
invoice, up to the costs actually incurred and within the guaranteed capital; the **balance**
goes to the freely designated beneficiaries and, failing them, to a standard cascade — surviving
spouse, then PACS partner, then *concubin notoire*, then children in equal shares, then the
heirs [S1] [S8] [S9] [S12]. One insurer requires a named designation to be followed by the words
"*à charge pour ce ou ces bénéficiaires de financer les obsèques de l'assuré à concurrence de
leur coût et dans la limite du capital garanti*" [S12] — the drafting device that carries art.
L. 2223-33-1 CGCT into the beneficiary clause [R2] [REG-R38]. The designated operator may be
changed at any time [S12] [R5]; the documents required on death include a **detailed paid
invoice from the funeral operator** [S1] [S8] [S9]; payment deadlines run from 8 days [S1] to
30 days [S8] [S9]. The national file created by art. L. 2223-34-2 CGCT [R4] is operated as an
AGIRA search, and insurers must respond to a request within **3 business days** [R19].

---

## Riders and options

**In scope (modeled):**

- The **accidental / non-accidental split inside the waiting period** [S1] [S8] [S9] — an
  integral benefit, not a rider.
- The **2× accidental-death enhancement from year 2**, capped at 20000 €, as a variation flag
  [S8].
- **Revalorisation** of the capital, with and without the matching premium uprating [S14] [S9].
- **Rachat** at the *provision mathématique*, with an optional first-ten-years penalty [S8].
- **Réduction** to a paid-up capital on premium cessation [S1] [S8] [S9] [R7].

**Described, out of model scope:**

- **The *contrat en prestations* (services form).** The same whole-life capital tied to a
  defined and personalised list of funeral goods and services which a named operator undertakes
  to deliver [R21] [S3] [S13]; observed packages at 3500 / 4500 / 6000 € [S3] and at capital
  equivalents of 3800 € and 4580 € [S13]. **It is out of scope because the tariff is the same
  object**: one insurer's *prestations* table reproduces its *capital* table's premiums exactly
  for a 5000 € capital at entry age 50 — 356 / 405 / 494 / 678 / 1240 € for the 25/20/15/10/5-year
  terms in both [S2] [S3]. The two forms differ in who receives the money and in the contractual
  service list, not in the cash-flow mechanics. Two statutory duties attach to it and to nothing
  else in this file: art. L. 2223-34-1 CGCT makes any clause promising advance funeral services
  **without a detailed and personalised description of them "*réputée non écrite*"** [R3], and
  art. L. 2223-35-1 CGCT requires the contract to let the subscriber change, at any time during
  life, the nature of the funeral, the mode of burial, the content of the services and supplies,
  the designated operator and any *mandataire*, with only the general conditions' management
  charges payable for changes at equivalent services, on pain of a **15000 € fine per
  infringement** [R5].
- **Assistance guarantees** — repatriation, formalities help, psychological support — included
  in the premium at two insurers [S1] [S9] and priced at 12 €/year at a third [S8]. Not a cash
  benefit; cancelled on *réduction* [S1] [S8] [S9].
- **Capital increases** [S1] [S8]: an anti-selective option on a guaranteed-issue book, mitigated
  by the fresh waiting period on the increment. Flagged as a model risk, not projected.
- **Couple discount**, excluded from the quoted premiums at one insurer [S14]; and **choice and
  change of the funeral operator** [S12] [R5] — a payee question with no amount effect.
- **Post-mortem revalorisation** [S1] [S8] [R8] [REG-R31] — a settlement-lag uplift; excluded
  from the base projection and pointed at in the technical notes.

---

## Variations across insurers

The seven insurers whose documents were retrieved diverge on six axes, and a configurable model
must carry all six as model point columns rather than as code branches.

1. **Premium forms offered.** Five temporary terms plus lifetime but no single premium [S1];
   seven forms including the single premium [S5]; only two temporary terms, neither lifetime nor
   single [S16]; lifetime, "to age 80", 10-year and 5-year [S9] [S10]. Chosen: all three
   families available, selected by `premium_form` **[std]**.
2. **Revalorisation coupling.** Capital only at five insurers [S1] [S5] [S14] [S15] [S16];
   capital **and** remaining premiums in the same proportion at one [S9] [S10] [S11]. Chosen:
   capital only, with `reval_prem_linked` as the switch.
3. **Waiting-period benefit basis.** Gross premiums collected [S1]; net of the assistance
   premium [S8]; net of instalment charges [S9]. Chosen: gross **[std]**.
4. **Exclusion benefit.** *Valeur de rachat* [S1] [S8] versus *provision mathématique* [S12] —
   in practice the same quantity, but one insurer substitutes the net premiums collected where
   they exceed the surrender value [S8].
5. **Surrender penalty.** None [S1] [S11] versus 5 % in the first ten years plus a 5 % charge
   inside the provision in the first eight [S8]. Chosen: none **[std]**.
6. **Accidental-death multiplier.** 1× everywhere [S1] [S9] [S14] except one insurer, where
   accidental death from year 2 pays **double** the capital subject to a 20000 € cap [S8].

Two further divergences are recorded but not modeled. Entry-age bands are **form-dependent** at
one insurer — lifetime premiums only from age 40, temporary terms narrowing as the term
lengthens [S8] — which is a new-business eligibility rule, not a projection rule. And a snippet
describing a contract with capitals from 1000 € to 15000 €, revalued annually, with no waiting
period where the premium is paid in one instalment, is **[unverified]**: the publisher's page
returned HTTP 403 on both attempts and no document was retrieved [S19].

**Why these representative choices.** One wording [S1] is the cleanest single chassis — an
individual whole-life contract, capital 2000–10000 €, entry 18–84 with no medical selection, six
premium forms, a one-year waiting period with premium refund, a fully specified charge
structure, PB credited to the capital, surrender at the *provision mathématique*, and a
published worked grid. It publishes no single premium, and in one distribution its lifetime form
is marked NA [S2], so a second rate card [S5] supplies the missing arm. The numerical anchor for
the worked example is a third document [S14], chosen because premium, revalorisation rate and
surrender-value grid are mutually consistent inside it. Between them these three pin down every
quantity the model needs except the pricing basis itself, which no insurer publishes.

---

## Regulatory context

**Funeral-specific statute (CGCT).** Art. L. 2223-33 prohibits advance offers of funeral
services except *formules de financement d'obsèques* [R1]; art. L. 2223-33-1 earmarks the
capital to the funeral up to its cost [R2] [REG-R38]; art. L. 2223-34-1 voids any advance-services
clause without a detailed and personalised description, and imposes on such contracts an annual
PB allocation of **at least 85 %** of the credit balance of the financial account, pro-rated by
mathematical provisions and net of technical interest credited [R3]; art. L. 2223-34-2 creates
the national file [R4]; art. L. 2223-35-1 guarantees the lifelong freedom to modify, on pain of
a 15000 € fine [R5].

Three cautions. First, **the loi Sueur does less than it is usually credited with**: the
retrieved JORF text of loi n° 2008-1350 du 19 décembre 2008 contains the amendment to
L. 2223-33 (art. 7), the legal-interest floor added to L. 2223-34-1 (art. 8) and the national
file (art. 9), and **not** the "detailed and personalised description" or the faculty to modify
[R6]. Those come from loi n° 2004-1343 du 9 décembre 2004 [R21] and, per Légifrance's own
legislative history, from loi n° 2005-1564 du 15 décembre 2005 art. 15 (V) [R5]; the current
wording of L. 2223-34-1 comes from loi n° 2013-672 du 26 juillet 2013 arts. 73–74 [R3]. A
widespread attribution of L. 2223-35-1 to the 2004 statute [R21] conflicts with Légifrance and
is not followed. Second, **the 85 % PB floor is drafted for the *prestations* form** — "*tout
contrat prévoyant des prestations d'obsèques à l'avance*" — and whether it reaches a pure
capital contract is not settled by the retrieved text [R3]; the *arrêté* that was to specify its
calculation was not located. Third, from **1 October 2026** every funeral operator must hand
families a standardised neutral information notice under décret n° 2026-770 du 13 août 2026 and
an arrêté of the same date [R20] — a duty on the operator, not on the insurer.

**Contract law (Code des assurances / Code de la mutualité).** Art. L. 132-1 enables the cover
and L. 132-3 prohibits it on certain lives [R7]; L. 132-5 requires the PB allocation conditions
and the post-mortem revalorisation rules to be stated [R8]; L. 132-5-1 gives 30 days'
*renonciation* with a full refund, extended where the notice was not delivered and capped at
eight years [R7] [REG-R29]; L. 132-13 keeps the death capital outside *rapport à succession* and
*réduction pour atteinte à la réserve*, "*à moins que [les primes] n'aient été manifestement
exagérées eu égard à ses facultés*" [R7]; L. 132-20 sets the non-payment path [R7]; L. 132-21
requires the contract to state how surrender, transfer and paid-up values are computed and caps
settlement at two months [REG-R31]; L. 132-22 prescribes the annual statement [R9] [REG-R31];
L. 132-23 makes whole-life contracts *rachetables* and *réductibles* [R10]. The
*mutualité*-code contracts run the same architecture under arts. L. 223-8, L. 223-19-1,
L. 223-20-1, L. 223-22, L. 223-22-1 and R. 223-9; **those articles could not be retrieved** —
the code's landing page loads but the articles do not [R23] — so everything attributed to them
rests on the insurer notices [S8] [S9] and the article texts themselves are [unverified].

**Conduct.** The CCSF opinion of 8 October 2024 [R11] — **not retrieved, HTTP 403 on three
attempts** — is reported by four independent secondary sources [R13] [R14] [R15] [R16] as
committing insurers, from 1 July 2025, to publish the standardised examples table, to cap the
*délai de carence* at one year, to offer temporary alternatives systematically alongside
lifetime premiums, to limit exclusion clauses, and to state the surrender value payable when
death falls within an exclusion, with an effectiveness review in July 2026. The opinion is
non-binding [R13]. All of that is **[unverified]** against the opinion itself; the one part
independently corroborated is the table, of which sixteen were retrieved from seven insurers.
The pre-contractual documents are prescribed: the *note d'information* by art. A. 132-4 CA and
the one-page *encadré* by art. A. 132-8 CA, the latter requiring charge **maxima** in four
categories to be disclosed [REG-R30]. Funeral firms selling these contracts must be registered
as insurance intermediaries [R21].

**Prudential.** Solvabilité II as transposed into the Code des assurances governs the valuation
basis [REG-R1] [REG-R2] [REG-R4]; the best estimate is the probability-weighted average of future
cash flows discounted at the EIOPA risk-free term structure [REG-R5]. The French statutory
balance sheet persists alongside it, with the *provision mathématique* — the difference between
the present values of the two parties' commitments, **including future management costs** — the
first of eleven named technical provisions [REG-R6], and the provision this contract's surrender
value is contractually equal to [S1] [S8] [S9]. Any guaranteed technical rate is capped by art.
A. 132-1 CA at the lower of 3.5 % and 60 % of the reference TME for contracts with periodic
premiums [REG-R17]; the only technical bases published anywhere in the retrieved set are a rate
of **0.75 %** with table **TH 00-02** at one insurer [S8] and **0 %** in another's worked example
[S1]. TH 00-02 and TF 00-02 are the regulatory non-annuity tables homologated by the arrêté du
20 décembre 2005 [REG-R22] and reproduced in the annexe to art. A. 335-1 CA, which also fixes
the *décalage d'âge* schedules and permits only homologated or actuary-certified tables
[REG-R23]. **They are cited by name and never redistributed here**: the decrement inputs shipped
with this product are **[std]** proxies built from INSEE population data [REG-R24].

**Tax.** Applicability is verified from four primary documents [S1] [S9] [S11] [S13]: death
benefits arising from premiums paid **before** the insured's 70th birthday fall under art. 990 I
CGI; premiums paid **from** the 70th birthday fall under ordinary inheritance duty under art.
757 B CGI; a surrender is taxed on its gain under art. 125-0 A CGI; social levies apply under
art. L. 136-7 CSS [S1]. The verified thresholds — a 152500 € allowance per beneficiary then 20 %
up to 700000 € and 31.25 % above under 990 I, and a single global 30500 € allowance under
757 B — are carried on the cross-product entry [REG-R41] alone, because **this product's own
research file could not fetch the CGI articles** [R24]. The *primes manifestement exagérées*
exposure [R7] is real at high entry ages, is a fact-specific judicial test that no retrieved
document quantifies, and is bounded here by the aggregate capital caps (10000 € [S1] [S8],
17580 € [S12]) and by the single premiums (at most 4819.56 € for 5000 € of cover at 70 [S5]).

**Professional standards and accounting.** NPA 2 *Modèles actuariels* is the recommended-practice
standard against which a published model, its worked example and its test suite are judged
[REG-R44]. IFRS 17 applies to IFRS reporters from 1 January 2023 with no French carve-out
[REG-R45].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-obseques-r1
[R10]: #frlib-obseques-r10
[R11]: #frlib-obseques-r11
[R13]: #frlib-obseques-r13
[R14]: #frlib-obseques-r14
[R15]: #frlib-obseques-r15
[R16]: #frlib-obseques-r16
[R17]: #frlib-obseques-r17
[R19]: #frlib-obseques-r19
[R2]: #frlib-obseques-r2
[R20]: #frlib-obseques-r20
[R21]: #frlib-obseques-r21
[R22]: #frlib-obseques-r22
[R23]: #frlib-obseques-r23
[R24]: #frlib-obseques-r24
[R3]: #frlib-obseques-r3
[R4]: #frlib-obseques-r4
[R5]: #frlib-obseques-r5
[R6]: #frlib-obseques-r6
[R7]: #frlib-obseques-r7
[R8]: #frlib-obseques-r8
[R9]: #frlib-obseques-r9
[REG-R1]: #frlib-reg-r1
[REG-R14]: #frlib-reg-r14
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R17]: #frlib-reg-r17
[REG-R2]: #frlib-reg-r2
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R31]: #frlib-reg-r31
[REG-R38]: #frlib-reg-r38
[REG-R39]: #frlib-reg-r39
[REG-R4]: #frlib-reg-r4
[REG-R41]: #frlib-reg-r41
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R49]: #frlib-reg-r49
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
