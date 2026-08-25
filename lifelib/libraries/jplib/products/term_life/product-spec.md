# Product Specification

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's contract. Facts
carrying a source tag — [S#] (primary product documents: policy conditions (*yakkan*, 約款),
ご契約のしおり, 重要事項説明書, 商品ページ) and [R#] (product-specific regulatory and actuarial
references), both numbered per `_research/term-life.md` and resolved in `sources.md` in this
directory, numbering frozen; and [REG-R#], the cross-product library
`references/regulatory-and-actuarial-references.md`, whose R-numbering is distinct — were
extracted from the cited document. Values marked **[std]** are standardizations introduced
for the reference implementation; every **[std]** table row carries a numbered footnote with
its rationale and the observed range. Claims that could not be confirmed against a retrieved
document are flagged [unverified]. The composite is drawn from **nine carriers** across
fourteen documents: five policy-condition sets, one of which is also a pre-contract
disclosure booklet [S1] [S4] [S6] [S7] [S8]; one 約款 extract that could not be
text-extracted [S11]; one product brochure [S12]; and seven consumer or specification
pages [S2] [S3] [S5] [S9] [S10] [S13] [S14]. Carriers are named only in `sources.md` and
`_research/`; here a carrier is its tag.

This product is the library's **protection chassis**. The
[survivor income term product specification (収入保障保険)](../income_guarantee/product-spec.md)
(survivor income term) states only its deltas against this document and
[`technical-notes.md`](technical-notes.md) in this directory, so the shared machinery —
decrements, premium structure, renewal, exclusions, grace and reinstatement — is specified
here in full and not restated there.

---

## Product overview and market role

Level term life (*teiki hoken*, 定期保険) is first sector (*dai-ichi bun'ya*, 第一分野)
business under 保険業法第3条第4項第1号, which covers fixed-sum insurance on human survival or
death and separates it from the third sector (*dai-san-bun'ya*, 第三分野) list of
sickness, injury and nursing-care covers [REG-R1]. One parenthesis in that clause matters here more than anywhere
else in the library: it brings within the first sector the state of 「余命が一定の期間以内で
あると医師により診断された身体の状態」, a physician-certified limited life expectancy [R1].
The terminal-prognosis acceleration sold as リビング・ニーズ特約 (a *tokuyaku*, rider)
therefore sits inside the same
licence as the death benefit.

The dominant retail shape is level term (平準定期保険): non-participating (*muhaitō*, 無配当),
without surrender value (*mu-kaiyaku-henreikin-gata*, 無解約返戻金型), level sum assured, level
premium within the term, and the benefit paid on death **or** on severe disability (*kōdo
shōgai*, 高度障害) at the same amount [S1] [S4] [S8] [S9] [S12]; one carrier names the chassis
in its literature as 無配当平準定期保険 [S13]. Decreasing term (*teigen teiki hoken*, 逓減定期保険) is a
separate product, not a payout option on this one [S14]. Two term designs coexist
and are contrasted by name: a fixed number of years (*nen manryō*, 年満了) renews automatically
at attained-age rates, while to a stated age (*sai manryō*, 歳満了) never renews [S1] [S2]
[S4] [S5]; one carrier calls them 更新型 and 全期型 [S7]. That renewal structure is the
sharpest contrast with a UK term assurance, which simply expires, and with a U.S. level term,
whose post-level tail is priced annually rather than as a fresh level term.

定期保険 is a minority of new individual policies and a plurality of new individual **cover**.
For FY2024, 生命保険協会 member companies report it in force at 2,721万件 — 13.9% of 個人保険
by count, behind 医療保険 (23.3%) and 終身保険 (19.7%) — but at 300兆4,672億円 of sum insured,
**38.6%**, the largest single share; new business was 135万件 (10.9% by count) and
24兆6,666億円 (**43.2% by sum insured**) [REG-R31]. Household evidence agrees: 89.2% of
two-or-more-person households hold cover, average 世帯普通死亡保険金 is 1,936万円 and falling,
average household premium is 35.3万円 across 3.8 policies, and among most recently bought
policies 定期保険 is 8.3% against 終身保険 29.2% and 医療保険 28.1% [R9]. The product is bought
in large amounts by relatively few households, and matters to this library more as a building
block — the parent of the
[survivor income term product specification (収入保障保険)](../income_guarantee/product-spec.md), the death half of
every combination product — than as a headline seller.

**Published rate cards exist, and that is a real documentary contrast with `uklib`.** Where no
UK insurer publishes a premium basis and the `uklib` model had to treat the office premium as
an opaque input, four carriers here publish a monthly premium scale on an open page: two vary
the sum assured as well as sex and age [S2] [S9], one tabulates sex × age per ¥1,000,000 of
cover and publishes it both before and after a repricing [S10], and one tabulates sex × age at
a single sum assured [S12]. A fifth publishes single worked examples [S5]. Three price the
same cell — male 30, 10-year term, ¥10,000,000 — at ¥974, ¥980 and ¥1,068 a month
[S2] [S9] [S5]. What is still not published is the basis behind those prices: the
assumed interest rate (*yotei riritsu*, 予定利率), 予定死亡率
and 予定事業費率 sit in the 保険料及び責任準備金の算出方法書 filed under 保険業法第4条第2項第4号,
which is not public [REG-R2]. The observable pricing artefact for a Japanese protection
product is the rate card, not the parameters — which is why every pricing-basis parameter in
this library is **[std]** while every contractual parameter is sourced.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 平準定期保険, 無配当, 無解約返戻金型; main contract (*shu-keiyaku*, 主契約) pays death and 高度障害 only | [S1] [S4] [S8] [S9] [S13]; participation **[std]** (1) |
| Benefit shape | Level sum assured; 逓減 is a separate product, out of scope | [S1] [S4] [S8]; scope **[std]** (2) |
| Lives basis | Single life. No joint-life basis appears in any retrieved document | [S1] [S4] [S8] [S12] |
| Regulatory class | 第一分野 (保険業法第3条第4項第1号) | [REG-R1] [R1] |
| Issue age (契約年齢) | 20–65, age last birthday (*man-nenrei*, 満年齢) with fractions discarded | [S1] [S2] [S8] [S10]; envelope **[std]** (3) |
| 保険期間 / 保険料払込期間 | Equal, always. Base 年満了 10年 with automatic renewal; 歳満了 to 60/65/70/80歳 as a model-point variant | [S1] [S2] [S4] [S8] [S9]; menu **[std]** (4) |
| Renewal ceiling | Attained age 80; a renewal passing it truncates to an 80歳満了 term | [S1] [S2] [S8] [S13]; pick **[std]** (5) |
| Sum assured (保険金額) | ¥1,000,000 – ¥30,000,000, in ¥1,000,000 units | [S2] [S9] [S13]; envelope **[std]** (6) |
| Non-medical limit | 告知 only to ¥30,000,000 at ages 18–40, stepping to ¥5,000,000 at 71–80 | [S4]; adoption **[std]** (7) |
| Rate classes | One (標準体); preferred and non-smoker classes are a documented variant | [S1] [S2] [S4] [S8] [S9] [S10]; pick **[std]** (8) |
| **Anchor model cell** | Male, 契約年齢 30, 年満了 10年 更新型, 保険金額 ¥10,000,000, 月払保険料 **¥974**, ceiling 80 | premium [S2]; cell choice **[std]** (9) |

Footnotes to **[std]** rows:

1. Seven carriers write 無配当 [S1] [S4] [S8] [S9] [S10] [S13] [S14], four of them saying so
   in the product name itself [S1] [S4] [S13] [S14], and one 約款 putting it in a sentence:
   「この保険契約については、契約者配当はありません。」 [S1]. One writes a 有配当 design with
   policyholder dividends (*keiyakusha haitō*, 契約者配当) accumulating at interest and paid on
   request or termination, and says plainly that a dividend may not be payable at all in a
   given year [S7]. Composite: 無配当, the mode.
2. Level and decreasing are distinct products. The only retrieved 逓減 document states the
   decrement as a formula — the benefit falls by `基本保険金額 ÷ 保険期間` each year from the
   second policy year — and the **premium falls with the cover**, the opposite of the UK
   convention [S14]. Out of scope; Variations, item 11.
3. Observed minima run 6 to 25 (6 [S12]; 15 [S9] [S10]; 18 [S4]; 20 [S2] [S8]; 25 [S14]) and
   maxima 65 to 80 (65 [S2] [S10]; 69 [S8]; 75 [S12] [S14]; 80 [S4] [S9]). Composite: 20–65,
   the modal bounds and the exact envelope of one carrier [S2]. 契約年齢 is age last birthday
   (*man-nenrei*, 満年齢) with fractions discarded [S1]; one carrier measures it at the
   契約日, the first of the month after application [S4]. The valuation table is built for
   age nearest birthday (*hoken-nenrei*, 保険年齢) [REG-R20]; the technical notes must say what
   they do about the mismatch.
4. Observed menus span one fixed term [S8]; 10/20/30年 plus 65/80/90歳満了 [S4]; 年満了 10–30年
   and 歳満了 60–80歳, both in five-year steps [S2]; 10年 plus four 歳満了 ages [S9] [S10]; any
   term from 5 years in one-year steps [S14]; and a free 満了時年齢 envelope [S12]. Composite:
   the 10-year renewable term, the only term **every** carrier writes, with 歳満了 as a variant
   — the 更新型 / 全期型 contrast is the product's defining mechanic and a model that cannot
   represent both cannot represent the product. 保険期間 equals 保険料払込期間 everywhere, and
   altering one alters the other [S1] [S4] [S8] [S9] [S12].
5. Observed ceilings: 75 [S10], 80 [S2] [S8] [S13], 90 [S4] [S9], 99 [S12]; 80 is the mode.
   Behaviour at the ceiling varies more than the ceiling does (Variations, item 2); the
   composite truncates, the rule of the two carriers whose ceiling it adopts [S1] [S2] [S8].
6. Observed ceilings run ¥10,000,000 [S10] to ¥100,000,000 [S4] [S9], with two carriers at
   ¥30,000,000 [S2] [S13]; minima are ¥1,000,000 [S9] [S10], ¥2,000,000 [S9] or ¥5,000,000
   [S2] [S13], one carrier banding the minimum by age [S4]. Composite: the modal private-writer
   ceiling and unit, inside the surveyed cover bands [REG-R32] [R9]. Increases are refused at
   two carriers, which require a new contract; decreases are permitted above a floor [S4] [S8].
7. Two carriers publish non-medical limits by age band: ¥30,000,000 at 18–40 stepping to
   ¥5,000,000 at 71–80 [S4], and ¥50,000,000 at 15–39 stepping to ¥5,000,000 at 76–80 [S9].
   Composite: the tighter [S4]. Underwriting decline is not modeled; the limit is carried so a
   model point above it is visibly outside the represented product.
8. Class counts observed: 1 at five carriers [S1] [S2] [S4] [S8] [S9] [S10] — the word 非喫煙
   does not occur in one 84-page booklet [S8] — 3 at one [S12], 4 at another [S13], and an
   elective 健康体割引特約 at a further one [S14]; the ninth carrier publishes no rate-class
   position at all. Published maximum discounts are 約14.5% (優良体)
   and 約30.6% (非喫煙者優良体) on three tiers [S12] and 約54% on four [S13]. Composite: single
   class — the majority position, and a class structure multiplies the premium basis without
   changing any contractual mechanic. Two facts a model must keep if it implements one: the
   class is fixed at issue and **carried unchanged through every renewal to age 80 regardless
   of later health**, and applying a risk-segmented rate is the stated reason that carrier has
   no surrender value (*kaiyaku-henreikin*, 解約返戻金) [S13].
9. The anchor is the cell three carriers independently publish: male 30, 10-year, ¥10,000,000
   — **¥974/month** [S2] against ¥980 [S9] and ¥1,068 [S5], a 9.6% spread on the same risk.
   ¥974 is taken because that carrier publishes enough grid to decompose the premium (footnote
   11). ¥10,000,000 sits inside every carrier's band and near half the surveyed average
   household death cover of 1,936万円 [R9]. What is standardized is the choice of cell; the
   premium is a published figure.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level within the 保険期間; recomputed at each 更新 on attained age and the scale then in force | [S1] [S4] [S8] [S12] |
| Frequency | 月払 default; 半年払 and 年払 available and switchable | [S1] [S3]; default **[std]** (10) |
| Payment route | 口座振替 or credit card; 振込 and 団体扱 also seen | [S1] [S4] |
| Rate structure | Marginal rate per ¥5,000,000 of cover plus a flat monthly policy fee, adopted as **¥248** at every age and both sexes | [S2]; adoption **[std]** (11) |
| Rating factors | Sex, 契約年齢, 保険期間, 保険金額, 払込方法 | [S8] [S9] |
| Large-case discount (高額割引) | Not applied | [S7] [S9] [S14]; scope **[std]** (12) |
| Advance payment (前納) | Available at an insurer-set discount, held at interest; not modeled | [S1] [S10]; scope **[std]** (12) |
| Pricing basis (予定利率 etc.) | Not published for any protection product in the set; the model's basis is **[std]** | [REG-R2]; gap (13) |

10. One carrier offers 月払・半年払・年払 with switching [S1] [S3]; two are 月払 only, one
    noting 年払 was not on offer as at 2024年4月 [S4] [S8]; one allows 1–12 months or the whole
    remaining term at once [S10]. Monthly is available everywhere, so the composite defaults
    to it and the annual-grid model uses `P_a = 12 × P_m` **[std]**.
11. The published grid is exactly arithmetic in the sum assured. At male 30 the
    ¥5,000,000 / ¥10,000,000 / ¥15,000,000 premiums are ¥611 / ¥974 / ¥1,337 — a constant step
    of ¥363 per ¥5,000,000, leaving `611 − 363 = 248` as the flat element; female 30 and
    female 50 give the same ¥248, and male 40, male 50 and female 40 give ¥248.5, the
    half-yen being an artefact of the whole-yen rounding the card is printed at [S2]. Taking
    the flat element as **¥248** and rounding half up to the yen reconstructs **all eighteen
    published cells exactly** — six sex-and-age rows at three sums assured — the anchor among
    them as `974 = 248 + 2 × 363`. Limits worth stating: this
    is one carrier's grid at one date, and a second carrier's 歳満了 rows are exactly
    proportional to the sum assured with **no** flat element while its 10年更新 rows are not
    [S9]. The policy fee is a design choice, not a market constant.
12. 高額割引 exists at three carriers; only one publishes thresholds, at ¥30,000,000 with a
    further step at ¥50,000,000, the 基準額 for a term product being the 保険金額 itself [S7]
    [S9] [S14]. The anchor sits below the only published threshold, so the composite omits the
    discount rather than guess two unpublished schedules. 前納 is omitted for the same reason:
    its discount rate is insurer-set and unpublished [S1].
13. No carrier publishes the 予定利率 of its 定期保険; the disclosures naming 予定利率 and
    予定死亡率 relate to savings products [S7]. This is structural, not a research failure —
    those coefficients live in the unpublished 算出方法書 [REG-R2]. The current numeric
    standard valuation interest rate (*hyōjun riritsu*, 標準利率) for level-premium first-sector
    business likewise could not be established from any retrieved document and is
    [unverified]; the mechanism setting it is sourced [R5] [REG-R10]. The technical notes build
    a **[std]** pricing and best-estimate basis and reconcile it to the published rate card,
    rather than claim a basis they cannot see.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| 死亡保険金 | 保険金額, on death within the 保険期間; terminates the contract | [S1] [S4] [S8] [S9] [S12] |
| 高度障害保険金 | **The same 保険金額**, on entering a 高度障害状態 within the 保険期間 from a cause arising on or after 責任開始時; terminates the contract | [S1] [S4] [S8] [S9] [S12] |
| 高度障害状態 | The closed eight-item 別表3 schedule with numeric 備考 (corrected acuity ≤ 0.02; hearing loss `(a + 2b + c)/4 ≥ 90 dB` at 500/1,000/2,000 Hz) | [S1] |
| Recipient | 死亡保険金 to the 死亡保険金受取人; 高度障害保険金 to the **被保険者**, not redirectable | [S1] [S12] |
| Ordering | Whichever becomes payable first is paid; the other is then not paid | [S1] [S8] |
| Suicide exclusion | No death benefit where the insured takes their own life within **3 years** of the 責任開始日 (or of the last 復活); the window runs through renewals | [S1] [S4] [S7] [S8] |
| Other 免責事由 | Intentional killing by the 死亡保険金受取人, or by the 保険契約者 — three limbs in total in every 約款 retrieved | [S1] [S4] [S7] [S8] |
| Amount on a 免責 | Policy reserve (*sekinin-junbikin*, 責任準備金) to the policyholder on the suicide and beneficiary-intent limbs; **nothing** on the policyholder-intent limb | [S1] |
| War and catastrophe | Not an exclusion but a **reduction power** where an upheaval affects the costing basis | [S1] [S4] [S8] |
| Pre-inception cause | Bars 高度障害保険金 and the waiver, subject to disclosure exceptions; the **death** benefit carries no pre-existing-condition restriction | [S1] [S4] [S8] |
| 満期保険金 | None | [S1] [S8] [S10] [S14] |
| Claim timetable | 5 business days from complete documents; 45 days where verification is needed; 180 days for special enquiries. Not modeled as a lag | [S1]; scope **[std]** (14) |

14. The timetable is contractual and is a real lag, but no document publishes the mix of
    claims falling into the three bands, so any split would be invented. The composite pays at
    the step in which the claim arises and says so; a claim-lag module belongs in the technical
    notes' sensitivities, not the base run.

### Options

| Parameter | Representative value | Basis |
|---|---|---|
| リビング・ニーズ特約 | Attached automatically, no separate disclosed premium. Trigger: a physician's judgement of **6 months or less** to live even with treatment generally accepted in Japan | [S1] [S2] [S3] [S7]; attachment **[std]** (15) |
| — amount | `指定保険金額 − six months' interest on it − six months' premiums on it` | [S1] [S7] [S8] [S12] |
| — cap | ¥30,000,000 per insured, aggregated across all of that insurer's contracts | [S1] [S7] [S8] [S12] |
| — term bar | No payment within **1 year** of the 保険期間満了 unless automatic renewal is still available | [S1] [S7] [S8] |
| — effect | Full payment extinguishes the contract and all 特約 **retroactively to the claim date**; partial payment reduces the 死亡保険金額 from that date and the reduced premium continues. One payment per contract | [S1] [S7] |
| 保険料の払込の免除 | In the **主契約**: premiums waived where the insured, from an 不慮の事故 on or after 責任開始時, comes within **180 days** to a 別表4 身体障害の状態 | [S1] [S8] [S12] [S14]; placement **[std]** (16) |
| 更新 | Automatic unless declined; notice to decline **2 weeks** before expiry | [S1] [S8]; notice **[std]** (17) |
| 減額 | Permitted above an insurer-set floor; premium reset; no 払戻金 arises from the reduction | [S1] [S8] |
| 増額 | Not available; a new contract with fresh underwriting is required | [S4] [S8] |
| 指定代理請求特約 | Standard; a pre-nominated proxy may claim where the insured is the beneficiary and cannot | [S1] [S8] [S12] [S14] |
| Indexation / GIO / conversion / joint life | **Absent from every retrieved document** | [S1] [S4] [S8] [S9] [S12] |

15. Attachment varies three ways: automatic at two carriers [S2] [S3] [S7], elective at two
    [S8] [S12], and **absent** at one — the string リビング・ニーズ does not occur anywhere in
    its 45-page booklet [S4]. Composite: automatic, the position of the carrier supplying the
    anchor premium, so the acceleration sits inside the modeled contract. That the rider is
    free of charge is market convention but **[unverified]**: no retrieved document states a
    nil 特約保険料, though the six-month deduction supplies the economic reason it can be, and
    one carrier lists it among the 特約 carrying no dividend [S7].
16. Four carriers put the waiver in the main contract on the accident-plus-180-days-plus-別表4
    test [S1] [S8] [S12] [S14]; one puts it there but keys it off 傷害 generally [S4]; one
    sells it as an optional 保険料払込免除特約 [S7]. Composite: modal placement and trigger.
    別表4 is a materially lower bar than 別表3 — loss of one eye, deafness in both ears, loss of
    one limb at wrist or ankle — so the waiver decrement is not the 高度障害 decrement and must
    not share its rate. Once the waiver runs, the alteration rights are switched off [S1].
17. Observed notice: 2 weeks [S1] [S8], 1 month [S7], 2 months [S4]. Composite: 2 weeks, the
    mode and the shortest — the shorter the notice, the more renewals happen by inertia.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 解約返戻金 | **None, for the whole term**: 「この保険契約については、解約払戻金はありません。」 | [S1] [S3] [S4] [S6] [S8] [S9] [S10] [S13] [S14] |
| 責任準備金 | Exists although the 解約返戻金 does not, computed by months of premium paid and months elapsed; payable on two of the three 免責事由 | [S1] |
| 払済保険 / 延長定期保険 | Not available on the composite; one carrier offers 払済保険 | [S1] [S4] [S8]; [S12] |
| Grace (猶予期間) | Monthly premiums: the first to the last day of the month **following** the 払込期月, about one month | [S1] [S8]; length **[std]** (18) |
| Claim during grace | Paid, net of the unpaid premium. A **waiver** event in grace differs — arrears must actually be paid or the policy lapses and the waiver is refused | [S1] [S4] [S8] |
| Lapse (失効) | The day after grace ends; no value payable | [S1] [S8] |
| Reinstatement (復活) | Available for **3 years**, against arrears with interest at **年6% compound** [S1], on evidence of health [S8] | [S1] [S8]; availability **[std]** (19) |
| 自動振替貸付 | **Absent**, stated in terms by one carrier | [S7] (20) |
| 契約者貸付 | Not available on the composite. There is no 解約返戻金 to lend against — an inference, not a citation | [S11] [unverified] (20) |
| 告知義務違反 | Rescission for **2 years** from 責任開始 or the last 復活; barred 1 month after the insurer learns the ground; no 払戻金 on rescission | [S1] [S4] |
| 詐欺・不法取得目的 | Not time-limited; survive the 2-year window; no refund | [S1] |
| クーリング・オフ | 15 days from application at one carrier against a statutory floor of 8 days; **out of scope** | [S1] [REG-R36]; scope **[std]** (21) |
| 時効 | Rights to a 保険金, to the 責任準備金, or to a waiver extinguish 3 years after becoming exercisable | [S1] [S10] |

18. Observed range about one to three months (Variations, item 3). Composite: about one month,
    the mode [S1] [S8]. For 年払 and 半年払 one carrier's grace runs to the monthly anniversary
    in the month after next, with named substitutions where that falls on the last day of
    February, June or November [S1]; carried as documented detail, not modeled.
19. Observed: 3 years with 年6% compound interest on arrears [S1]; 3 years subject to health
    [S8]; and **not offered** at two carriers [S4] [S7]. The composite includes it. A policy
    that comes back is a real, modelable behaviour with no analogue in the `uklib` composite,
    which terminates lapsed policies finally, and 復活 is the only event that resets the
    suicide and contestability clocks. Its rate of use is a **[std]** behavioural assumption
    in the technical notes; no document publishes one.
20. The 自動振替貸付 absence is sourced: one carrier states it twice —
    「この保険には、保険料の自動振替貸付制度…はありません。」 [S7]. **The 契約者貸付 absence is not.**
    That same carrier points its policyholders at the 契約貸付制度 to settle an unpaid premium
    instead [S7], so [S7] is evidence *for* a policy loan, not against one; the only document
    appearing to rule the policy loan out is the one whose PDF could not be text-extracted, so
    that reading is [unverified] [S11]. What carries the composite is structural rather than
    documentary — with no 解約返戻金 there is no collateral for either loan — and it is stated
    here as an inference so a reader can reject it. The supervisory guideline requires an
    自動振替貸付, where one exists, to operate **at the policyholder's election** with prompt
    notice, not as an automatic no-lapse rule [REG-R14] — so its absence removes an election,
    not a guarantee. A lapse model for this chassis is therefore a plain lapse model, which is
    part of why it is the right chassis to specify first.
21. 保険業法第309条 gives an eight-day cooling-off from the later of disclosure-document delivery
    and application, effective **when the withdrawal document is dispatched**, and disapplies it
    where the insurance period is one year or less [REG-R36]. One carrier contracts for 15 days
    [S1], permitted because it favours the policyholder. It is a genuine early-duration
    decrement and the composite excludes it explicitly: the model begins with cover in force
    and the cooling-off population already out.

---

## Contractual mechanics

### Premium provisions

The office premium is level **within** each 保険期間 and is not guaranteed beyond it. With
`P_m` the monthly premium, `SA` the sum assured, `x` the 契約年齢 and `n` the term in years,
the composite's published rate structure [S2] is:

    P_m = f + r(sex, x, n) * SA / 5,000,000
    f   = 248                      (yen per month, the flat policy element)

At the anchor cell `r(M, 30, 10) = 363` and `P_m = 248 + 2 * 363 = 974` [S2]; the annual-grid
model uses `P_a = 12 * P_m = 11,688` **[std annualization]**. Premiums are due monthly by
口座振替 or credit card [S1] [S4]. There is no premium review within a term: the only
contractual route by which the premium changes is 更新, and it changes then by construction
rather than by insurer discretion.

### Death and 高度障害 benefits

The main contract (*shu-keiyaku*, 主契約) pays two benefits of the same amount, and either
terminates the contract [S1] [S4] [S8] [S9] [S12]:

    死亡保険金    = SA, on death within the 保険期間
    高度障害保険金 = SA, on entering a 別表3 高度障害状態 within the 保険期間

**There is no U.S. or UK analogue for the second in this library.** It is neither a
critical-illness rider nor a terminal-illness acceleration but the whole sum assured on a
closed schedule of permanent total disabilities, inside the main contract, at no separate
premium. The eight items are total permanent loss of sight in both eyes; of speech or
mastication; central-nervous-system or psychiatric impairment and thoracic or abdominal organ
impairment, each requiring constant lifelong care; and four limb-loss combinations at or above
wrist and ankle. The 備考 fix the operative terms numerically:
「視力を全く永久に失ったもの」 is corrected acuity of **0.02 or below** with no prospect of
recovery, and 「常に介護を要するもの」 requires inability to perform *any* of eating,
toileting, dressing, rising, walking and bathing unaided [S1].

Four mechanics follow that a claims model must get right.

**Ordering.** If the 高度障害保険金 is claimed and payable before the death benefit is paid,
the death benefit is not paid; once the death benefit has been paid, no 高度障害 claim is
entertained [S1]. One carrier words the same principle from the other side: if the insured
dies before the 高度障害 claim is settled, the death benefit is paid instead [S8]. The two are
**competing risks on one sum assured**, not additive covers.

**Recipient.** 高度障害保険金 goes to the 被保険者 and cannot be redirected, the only exception
being a corporate policyholder that is also the death beneficiary [S1] [S12]. That is why
指定代理請求特約 exists: someone disabled enough to meet 別表3 is often unable to claim.

**Run-off past expiry.** Where at the 保険期間満了日 the disability is present but its
irrecoverability is not yet established, and it later proves irrecoverable, the insurer treats
the 高度障害状態 as met **on the expiry date** and pays; if it recovers, nothing is paid [S1].
Expect 高度障害 claims to be *reported* after the term ends, though none is *incurred* after it.

**The decrement basis, and the trap in it.** 生保標準生命表2018（死亡保険用）**includes**
高度障害 inside its death rate [REG-R20]. A model that projects the standard-table `qx` for
death and adds a separate 高度障害 incidence on top double-counts the benefit. The composite
therefore treats 死亡 and 高度障害 as one decrement carrying one sum assured, and splits them
only where a stated reason exists.

### 更新 — automatic renewal at attained-age rates

Unless the policyholder gives notice, a 年満了 contract renews on the day after the
保険期間満了日 for the same term and the same 保険金額, with **no fresh underwriting and no
告知** [S1] [S4] [S8] [S12]. The renewed premium is recomputed on the attained age at the
renewal date and the scale then in force, and the renewed contract is governed by the 約款 then
in force [S1] [S4] [S8] [S12]. Every carrier warns that the renewed premium is usually higher
[S1] [S4] [S7] [S8]. Renewal is refused where the elapsed period from 契約日 to the renewed
expiry would exceed the insurer's range, where the attained age the day after the renewed
expiry would exceed it, and where the 保険期間 is 歳満了 — **a 歳満了 contract never renews**
[S1].

Four further mechanics matter to a projection:

- **The clocks do not restart.** Suicide and contestability run from the original 責任開始 and
  the renewed term is continuous with the prior one [S4]. One carrier words it from the
  exclusion side — 「ただし、更新された場合を除きます。」 [S8] — another from the coverage side,
  the three-year window running 「（更新後の保険期間を含みます。）」 [S1]. Only 復活 restarts them.
- **A failed first renewal premium unwinds the renewal.** The first premium of the renewed
  contract falls due by the last day of the month containing the renewal date; unpaid through
  grace, **the renewal is treated as never having happened** [S1] and the policy terminates at
  the original expiry rather than being 解除 [S7]. In a projection that is an expiry, not a
  lapse.
- **Product withdrawal does not lapse the policy.** If the insurer no longer writes the
  product, the policy moves to a comparable contract it designates [S1] [S4] [S12].
- **The reserve clock restarts although the risk clock does not.** The 責任準備金 basis
  「保険料を払い込んだ年月数および経過した年月数」 is read after renewal as counted from the
  renewal [S1]. No new 保険証券 is issued [S1] [S4].

At the ceiling the carriers diverge, and the divergence is a modelling fork rather than a
wording difference (Variations, item 2). The composite truncates: a renewal that would carry
the policy past attained age 80 renews instead as an 80歳満了 term, so cover always ends
exactly at 80 and never at an age determined by the renewal grid [S1] [S2] [S8].

### リビング・ニーズ特約

The insurer makes the six-month judgement on a physician's certificate and may require
examination by a physician it nominates [S1] [S7]. One carrier prints the amount as
`支払金額 = Ａ − Ｂ − Ｃ`, adding that where a 更新 falls inside those six months the
post-renewal months are charged at the renewal-age premium [S1]. That discount is the economic
reason the rider can be offered without a separate premium.

Three differences from UK terminal illness cover all matter to a model: the trigger is
**6 months**, not 12; the payment is **discounted**, not the full sum assured; and it is a
**rider** with a **¥30,000,000 per-insured cap aggregated across all of that insurer's
contracts** [S1] [S7] [S8] [S12], so on a large policy it accelerates only part of the cover.
Because a full payment extinguishes the contract retroactively to the claim date while a
partial payment leaves a reduced contract in force at a reduced premium [S1] [S7], the two
cases are different transitions in a projection, not one benefit with two amounts.

### Exclusions, contestability and rescission

Three 免責事由 for the death benefit, and only three, appear in every 約款 retrieved (Benefit
provisions, above). Where a part-beneficiary is the killer, the remaining shares are still paid
[S1]. What is paid instead differs by limb and is a real if small cash flow: the 責任準備金 goes
to the policyholder on the first two limbs and nothing on the third [S1]; one carrier pays the
解約払戻金 on the third limb where one exists [S7]. Two carriers note that suicide arising from
a mental disorder may still be paid [S4] [S8].

The three-year suicide window is **three times the UK's twelve months**, and it is contractual,
not statutory. 保険法第51条第1号 excludes suicide with **no time limit at all**; the 免責期間 in a
Japanese 約款 narrows that statutory exclusion in the policyholder's favour, which is why its
length is a per-carrier fact and never an assertion of law [REG-R34]. On the evidence here it
does not vary: four carriers all say three years [S1] [S4] [S7] [S8].

告知義務違反 runs on a separate, shorter clock. The insurer may rescind prospectively where the
policyholder or insured, intentionally or by gross negligence, failed to state or misstated a
fact it asked about — **even after a claim event**, in which case the benefit is not paid and
any benefit already paid may be reclaimed [S1]. Rescission is barred where the insurer knew or
negligently did not know the fact, where an intermediary obstructed or encouraged the
misstatement, one month after the insurer learns the ground, or where **2 years** have passed
from 責任開始 or the last 復活 without a claim or waiver event arising [S1] [S4]. Even after
rescission the benefit is paid if the claimant proves the event did not arise from the
concealed fact [S1] [S7]. The statutory ceiling behind the carriers' two years is **five
years** from conclusion, with a one-month use-it-or-lose-it clock from discovery [REG-R35];
contracting to two is permitted because it favours the policyholder, and the supervisory
guideline separately requires the window not to be unduly long [REG-R14]. Rescission for 詐欺
and voidness for 不法取得目的 sit outside both windows, are not time-limited, and carry no
refund [S1].

The product therefore carries **two windows on two clocks** — three years for suicide, two for
non-disclosure — both restarting on 復活 and neither on 更新.

### Grace, 失効 and 復活

For monthly premiums the 猶予期間 runs from the first to the last day of the month following
the 払込期月; the day after it the contract 失効s [S1] [S8]. A claim arising within grace is
paid net of the unpaid premium [S1] [S4] [S8]. A **waiver** event within grace is treated
differently, and the difference is easy to model wrongly: the arrears must actually be paid by
the end of grace, or the policy lapses and the waiver is refused [S1] [S4]. 復活 is then
available for three years, and resets the suicide and contestability clocks from the new
責任開始 [S1]. There is no 自動振替貸付 to carry the policy through non-payment — one carrier
states that absence in terms [S7] — and no collateral for a 契約者貸付 either, on the inference
of footnote 20 rather than on a citation: grace → 失効 → 復活-or-not is the entire persistency
machinery of this chassis, which is why it belongs in the chassis document.

### Expiry

A 歳満了 contract expires at the end of its term with nothing payable and no maturity value
[S1] [S8] [S10] [S14]. A 更新型 contract expires only at the renewal ceiling — attained age 80
on the composite — because until then it renews. That is the structural difference from
`uklib`, whose composite terminates all states at the end of a single term with no tail
liability: here the base model carries the policy across renewal boundaries, reprices it at
each one, and terminates it at the ceiling.

---

## Riders and options

**In scope (modeled or parameterized):**

- **高度障害保険金** — in the 主契約, same sum assured, one decrement with the death benefit
  [S1] [S4] [S8] [S9] [S12].
- **更新** — modeled: attained-age repricing, truncation at the ceiling, clocks not restarting
  [S1] [S4] [S8] [S12].
- **リビング・ニーズ特約** — parameterized as a discounted acceleration with the ¥30,000,000
  cap and the one-year bar; switchable off in the base run, and a model point above the cap
  must show the cap binding [S1] [S7] [S8] [S12].
- **保険料の払込の免除** — the waiver state is specified (accident, 180 days, 別表4) and
  excluded from the base projection **[std scope]**; its incidence is not the 高度障害
  incidence and must not reuse that rate [S1] [S8] [S12] [S14].
- **復活** — a reinstatement transition out of the lapsed state at a **[std]** behavioural
  rate, with the clocks restarting [S1].
- **減額** — a sum-assured change with no payment, since no 払戻金 arises from it here [S1] [S8].

**Out of scope:** 災害割増特約 [S8] [S9] [S14]; 傷害特約, 年金支払特約, 保険契約者代理特約 [S14];
特定疾病保険料払込免除特約 [S9]; 無配当災害特約, 医療特約 and 無配当先進医療特約, of which one
carrier permits at most three [S10]; 特定障害不担保特約, which excludes a named disability from
the 高度障害 and waiver triggers and **carries into renewed terms** [S1] [S4];
指定代理請求特約, which changes who claims and not what is paid [S1] [S8] [S12] [S14]; 据置支払,
the beneficiary's option to leave the benefit on deposit at interest [S1]; 保険期間の変更, which
is permitted with consent, resets premiums, refunds nothing and requires any shortfall in the
責任準備金 to be paid in [S1] [S8]; 特別条件 acceptance in its Japanese forms of 保険金削減支払法
and 特定部位不担保法 [S7]; 払済保険 conversion, which exists at the one carrier with a cash
value [S12]; and 逓減 cover, a separate product [S14].

**Absent from the market rather than out of scope:** no retrieved document offers indexation
or increasing cover, a guaranteed-insurability option on the main contract, joint-life cover,
or a conversion option. The nearest thing to a GIO is one carrier's post-expiry window: where
a contract has run more than two years and then expires, is surrendered or is reduced, a new
policy may be taken within **one month** without medical evidence or 告知 [S12].

---

## Variations across insurers

1. **Age and term envelope.** 契約年齢 minima run 6 to 25 and maxima 65 to 80; term menus run
   from a single 10-year term [S8] to a free 満了時年齢 envelope [S12]. Composite: 20–65, the
   10-year renewable base with 歳満了 as a variant (footnotes 3, 4).
2. **Behaviour at the renewal ceiling.** Four distinct rules. Truncate to a 歳満了 term, one
   carrier stating the band precisely — renewal ages 満71 to 満79 convert a 10-year term into an
   80歳満了 term [S1] [S2] [S8]. Shorten year by year so the expiry age is exactly 90, refusing
   renewal from attained age 満90 [S4] [S5]. Shorten **or lengthen** to reach a 指定年齢, with
   published examples of a 10-year term renewed for 7 years in one direction and 13 in the
   other [S7]. Or do not renew at all and auto-convert into a different product [S12].
   Composite: truncation (footnote 5). This is the item most easily got wrong by assuming the
   ceiling alone determines the run-off; it does not.
3. **Grace, lapse and reinstatement — the widest variation in the product.** About one month's
   grace then 失効, with 復活 for 3 years at 年6% compound [S1]; the same but 復活 subject to
   health [S8]; about two months then 失効 and **no 復活 at all** [S4]; and no 猶予期間 whatever,
   replaced by a 催告 and a 解除予定日 in the third month, ending in 解除 with no 復活 [S7] — at
   which carrier a single shared premium means non-payment 解除s every contract in the package
   except any paid separately, and a 頭金 already paid is lost with it [S7]. Composite: one
   month, 失効, 復活 for three years (footnotes 18, 19). One carrier's clauses are missing from
   this comparison because its PDF could not be text-extracted [S11].
4. **Surrender value: seven to one.** Seven carriers have none, in a single 約款 line [S1] [S4]
   [S6] [S8] [S9] [S10] [S13] [S14]; one has a 解約返戻金 and offers 払済保険 conversion after
   the first policy year, though not 延長定期保険 [S12]. **A Japan term chassis cannot assume the
   absence of a cash value the way a UK one can.** One carrier publishes the price of the
   difference: ¥4,864 a month for the protection-only design against ¥11,298 for an otherwise
   identical design with a surrender value — male 20, 90歳満了, ¥10,000,000, a factor of
   **2.32** — the cash-value version's surrender value running from ¥1,037,000 at duration 10
   to ¥5,084,000 at duration 60 and back to **zero at duration 70**, the age-90 expiry [S4].
   That last row is the diagnostic one: a 90歳満了 term is not an endowment however large its
   mid-term value. The carrier states it does not sell that version and that the figures are
   its own 参考金額 [S4]. Composite: no surrender value.
5. **Rate classes.** One class at five carriers, three at one, four at another, an elective
   健康体割引特約 at a further one [S1] [S2] [S4] [S8] [S9] [S10] [S12] [S13] [S14]. Published
   criteria where they exist are concrete: 最大血圧140未満・最小血圧90未満, BMI 18.0–27.0, and for
   the non-smoker tier no smoking within the past year evidenced by both a 告知 and the
   insurer's own cotinine test, failure of which drops the applicant one tier [S12]. Composite:
   one class (footnote 8).
6. **リビング・ニーズ特約 attachment.** Automatic [S2] [S3] [S7], elective [S8] [S12], or absent
   [S4]. Composite: automatic (footnote 15). Its **terms**, by contrast, do not vary at all —
   item 12.
7. **Waiver of premium placement.** Main contract on an accident test [S1] [S8] [S12] [S14];
   main contract on 傷害 generally [S4]; or an optional 保険料払込免除特約 [S7]. Composite: main
   contract, accident test (footnote 16).
8. **Participation.** 無配当 at seven carriers [S1] [S4] [S8] [S9] [S10] [S13] [S14]; one
   有配当 design with dividends accumulating at an insurer-set rate from the next 契約応当日 and
   paid on request or termination [S7]. Composite: 無配当 (footnote 1).
9. **Sum assured envelope and 高額割引.** Ceilings ¥10,000,000 to ¥100,000,000; discount
   thresholds published by one carrier only, at ¥30,000,000 and ¥50,000,000 [S7] [S9] [S14].
   Composite: ¥1,000,000–¥30,000,000, no discount (footnotes 6, 12).
10. **Payment frequency.** 月払 only at two carriers [S4] [S8]; 月払・半年払・年払 with switching
    at another [S1] [S3]; 1–12 months or a lump sum at a fourth [S10]. Monthly is available
    everywhere. Composite: monthly (footnote 10).
11. **Cover shape.** Level at seven carriers; one writes a 逓減 product in which the benefit
    falls by `基本保険金額 ÷ 保険期間` each year from the second policy year **and the premium
    falls with it** [S14]. Descriptions of other 逓減 designs, including one stepping down to a
    floor of 20% of the 基本保険金額, are [unverified]; no second 逓減 document was retrieved.
    Composite: level only (footnote 2).
12. **What does not vary.** Five things are identical at every carrier examined and are the
    product's fixed spine rather than choices: (i) the death benefit and the 高度障害保険金 are
    the **same amount** and either terminates the contract [S1] [S4] [S8] [S9] [S12]; (ii) the
    高度障害状態 schedule is the same eight-item 別表3 with the same numeric 備考 [S1]; (iii) the
    suicide exclusion is **3 years** from the 責任開始日, restarting only on 復活 and never on
    更新 [S1] [S4] [S7] [S8]; (iv) the contestability window is **2 years** on the same clock
    [S1] [S4]; and (v) where the living-needs rider exists at all its terms are uniform —
    指定保険金額 less six months' interest and premiums, capped at ¥30,000,000 per insured
    aggregated across contracts, barred within one year of a non-renewable expiry [S1] [S7]
    [S8] [S12]. A composite may choose among the eleven items above; it may not alter these
    five and still be describing the Japanese product.

---

## Regulatory context

**Prudential — ESR, and what it replaced.** From **2026年3月31日** insurers are supervised on
the economic-value-based solvency regulation (*keizai-kachi bēsu no soruvenshī kisei*,
経済価値ベースのソルベンシー規制, **ESR**), a three-pillar regime in which assets are at fair value and
insurance liabilities are the current estimate (*genzai suikei*, 現在推計) re-measured at the
reporting date plus a **MOCE**, calibrated to 99.5% over one year. Early corrective action is
triggered at **ESR below 100%**, with bands at 70% and 35% [REG-R15]. It replaces, as the
trigger, the ソルベンシー・マージン比率 threshold of **200%** [REG-R17] [REG-R15]. The two are
not comparable: at 2025年3月末 the life industry stood at ESR 215% against SMR 873%
[REG-R15]. What matters here is not the ratio but the basis — the old regime fixed mortality,
lapse and interest at issue (原則ロックイン) while ESR re-sets them at each 基準日, which makes a
re-runnable, assumption-parameterized liability cash-flow model the operative artefact.
`jplib` computes neither ratio.

**Statutory reserving — cited, not reproduced.** 保険業法第116条第1項 requires a policy
reserve (*sekinin-junbikin*, 責任準備金) at each 決算期; 第2項 delegates, for the long-term contracts
the ordinance specifies, both the accumulation method and the level of the underlying
coefficients [REG-R4]. 施行規則第68条 fixes the contracts in scope [REG-R7] and 第69条第1項 the
taxonomy 保険料積立金 / 未経過保険料 / 払戻積立金 / 危険準備金 [REG-R8]. In-scope contracts may
not fall below the Commissioner's basis; others are floored at the net level premium method
(*heijun jun-hokenryō-shiki*, **平準純保険料式**) amount, which the ordinance defines in
line as levelling the funding across the whole premium-paying period [R2]. 平成8年大蔵省告示第48号
supplies method and rates — 平準純保険料式 with no Zillmer adjustment, and the 標準生命表 vintage
by contract date [REG-R10]; from **2018-04-01** the basis is 生保標準生命表2018（死亡保険用）
[REG-R11]. The 標準利率 derives from an 指標金利 built on JGB yield averages with 安全率係数
applied by band [R5] [REG-R10]; its **current numeric value could not be established from any
retrieved document and is [unverified]**. This library projects gross cash flows and builds
none of these reserves.

**The valuation table, and why the shipped table is [std].** 生保標準生命表2018（死亡保険用）is
published in full, free, at a stable public URL by 日本アクチュアリー会 as the 指定法人 under
保険業法第122条の2第1項 [R3] [REG-R18] — the sharpest contrast in the library with `uklib`, where
the current CMI term-assurance tables are restricted to Authorised Users and cannot be read at
all. Anyone can retrieve the Japanese table and check a rate: male `q30 = 0.00068`,
`q60 = 0.00653`; female `q30 = 0.00037`, `q60 = 0.00363` [R4] [REG-R18]. Two qualifications
hold nonetheless. The publisher's terms prohibit reproduction, alteration and transmission to
third parties without written consent, so the library **cites** the table, quotes only the
rates a worked example needs, and **ships** its mortality CSV as a **[std]** construction whose
`provenance` column points at the IAJ entries [REG-R21]. And the table is a **valuation**
table: a risk-theory margin sized to about a 2σ exceedance probability capped at 130% of the
unadjusted rate, plus a forward improvement allowance of 2.5% p.a. for five years then 1.0% for
three, built on a 保険年齢 basis and **including 高度障害 inside the death rate** [REG-R20]. A
best-estimate basis is therefore a **[std]** adjustment of a sourced table, in a stated
direction, and each document must say which of the two it is using at each point.

**Professional standards, and what a Japanese projection is for.** 保険業法第121条第1項第1号
requires the 保険計理人 to confirm at each 決算期, in an 意見書, that the 責任準備金 is accumulated
on sound actuarial principles [REG-R6]. The IAJ practice standard turns that into the
**1号収支分析** (*ichi-gō shūshi bunseki*, item-1 income-and-outgo analysis): an annual forward
projection of premiums, claims, expenses and surrenders by 区分経理 segment over **at least ten
future years**, in open and closed variants, sufficiency tested over the first five [REG-R22].
That is the regulatory use of a liability cash-flow model in Japan, and the shape this
product's projection takes.

**Conduct and classification.** 定期保険 is 第一分野 business [REG-R1] [R1]. The supervisory
guideline fixes pre-contract disclosure: the 契約概要 must carry the product mechanism, the
cover with its main 支払事由 and 免責事由, the principal 特約, the 保険期間, underwriting terms,
the premium and its payment terms, dividends and the level of any 解約返戻金; the 注意喚起情報
must carry クーリング・オフ, 告知義務, 責任開始期, the main non-payment cases, and
**保険料の払込猶予期間、契約の失効、復活** [REG-R14]. Every one of those is specified above with a
source tag, which is what makes this composite documentation-grounded rather than plausible.
保険業法第309条 gives an eight-day cooling-off on a dispatch rule, scoped out here (footnote 21)
[REG-R36]. The contract itself is governed by the 保険法: 第51条 for the statutory suicide
exclusion, which has no time limit and which the 約款 narrows to three years [REG-R34], and
第55条 for 告知義務違反, whose five-year ceiling and one-month discovery clock bound the carriers'
two-year windows [REG-R35]. On insurer failure, 生命保険契約者保護機構 covers contracts up to
**90% of the 責任準備金**, under a rate delegated by 保険業法第270条の3 to ordinance [REG-R40]
[REG-R41]; the reduced rate for 高予定利率契約 is [unverified] here. Cited, never modeled.

**Tax.** Premiums fall in the 一般生命保険料 basket of the post-2012 三区分 —
一般 / 介護医療 / 個人年金 — each giving an 所得税 deduction of the full premium up to ¥20,000
tapering to a flat ¥40,000 above ¥80,000, the three capped together at **¥120,000** [R7]
[REG-R43]; the 住民税 schedule, absent from the tax authority's page, runs to a flat ¥28,000 per
basket above ¥56,000 [S4]. At the anchor cell the annual premium of ¥11,688 is deductible in
full, so the deduction is not a material driver at this size. Death-benefit taxation turns on
the 契約者 / 被保険者 / 受取人 triangle — 相続税 where 契約者 = 被保険者, 所得税（一時所得）where
契約者 = 受取人, 贈与税 where all three differ [S1] — and where 相続税 applies and the recipient
is an heir, **¥5,000,000 × the number of statutory heirs** is exempt, apportioned in proportion
to the amounts received [REG-R44] [REG-R45] [S4]. The 高度障害保険金 and the living-needs benefit
are in principle tax-free where received by the insured or a close relative [S1] [S4]. `jplib`
models contractual cash flows and not the policyholder's tax position.

**Accounting.** Japan has no mandatory IFRS 17: IFRS applies as 指定国際会計基準 on a
**voluntary** basis [REG-R47]. A `jplib` projection therefore feeds three separate measurement
bases — J-GAAP statutory reserving [REG-R10], the ESR economic balance sheet [REG-R15], and
IFRS where an insurer has adopted it — and a document that conflates them will be wrong about
which assumptions are locked in and which are re-set.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-term_life-r1
[R2]: #jplib-term_life-r2
[R3]: #jplib-term_life-r3
[R4]: #jplib-term_life-r4
[R5]: #jplib-term_life-r5
[R7]: #jplib-term_life-r7
[R9]: #jplib-term_life-r9
[REG-R1]: #jplib-reg-r1
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R31]: #jplib-reg-r31
[REG-R32]: #jplib-reg-r32
[REG-R34]: #jplib-reg-r34
[REG-R35]: #jplib-reg-r35
[REG-R36]: #jplib-reg-r36
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R43]: #jplib-reg-r43
[REG-R44]: #jplib-reg-r44
[REG-R45]: #jplib-reg-r45
[REG-R47]: #jplib-reg-r47
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
