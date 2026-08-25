# Product Specification

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's contract. Facts
carrying a source tag — [S#] (primary product documents: policy conditions (*yakkan*, 約款),
ご契約のしおり, 契約概要, 注意喚起情報, 重要事項説明書, 商品ページ) and [R#] (product-specific regulatory and actuarial
references), both numbered per `_research/income-guarantee.md` and resolved in `sources.md`
in this directory, numbering frozen; and [REG-R#], the cross-product library
`references/regulatory-and-actuarial-references.md`, whose R-numbering is distinct — were
extracted from the cited document. Values marked **[std]** are standardizations introduced
for the reference implementation; every **[std]** table row carries a numbered footnote with
its rationale and the observed range. Claims that could not be confirmed against a retrieved
document are flagged [unverified]. The composite is drawn from ten carriers: four
policy-condition sets [S1] [S3] [S14] [S15], one rider-conditions document [S13], three
pre-contract disclosures [S2] [S4] [S5], and nine consumer or specification pages [S6]–[S12]
[S16] [S17]. Carriers are named only in `sources.md` and `_research/`; here a carrier is its
tag. **Nine of the ten write the product as a main contract; the tenth writes the same
economics as a 収入保障特約 rider [S13]**, and counts below say which population they are
counting.

**This is a death benefit.** Survivor income term (*shūnyū hoshō hoken*, 収入保障保険) pays on the
death of the insured — or on the contractual severe disability state (*kōdo shōgai jōtai*,
高度障害状態, treated throughout as an accelerated equivalent of death) — and pays it as a monthly
income instead of a lump sum. It is **not** income protection in `uklib`'s sense: `uklib`'s
`IP_UK_S` insures disability and pays while the insured is unable to work. The Japanese
product's insured event is death, its beneficiary is the survivor, and disability and
long-term-care income appear on this chassis only as special provisions (*tokusoku*, 特則) and
riders (*tokuyaku*, 特約), all of which are out of scope here.

**This document states deltas.** [term life (定期保険)](../term_life/product-spec.md) is the library's
protection chassis.
The decrement structure, the premium-payment machinery, the exclusion grounds (*menseki
jiyū*, 免責事由), the grace / 失効 / 復活 sequence, the 告知義務違反 contestability window and the 高度障害
double-counting trap are specified in full in the
[term life product specification (定期保険)](../term_life/product-spec.md) and its
[technical notes](../term_life/technical-notes.md) and are **not restated here**. What
follows is what this product adds or changes: the benefit shape, the 最低支払保証期間,
commutation, the preferred-risk rate classes, and the absence of renewal.

---

## Product overview and market role

収入保障保険 sells the same insured event as level term life (*teiki hoken*, 定期保険) in a different
currency: instead of a fixed sum assured (保険金額) the contract promises a level monthly annuity
amount (*nenkin getsugaku*, 年金月額) running from the insured event to a fixed expiry date
[S1] [S3] [S5] [S9] [S12] [S14]. Because the expiry date is fixed at issue and the monthly
amount is level, the **number of remaining instalments — and therefore the total benefit —
falls month by month as the term runs off** [S3] [S5] [S7] [S9] [S12] [S14]. It is the
Japanese analogue of UK family income benefit, sold in Japan as a stand-alone main contract
rather than as a payout option on a term policy.

The design answers a specific demand-side fact. Household death cover in Japan is falling:
the 2024 national survey puts household ordinary death cover (世帯普通死亡保険金額) at ¥19,360,000
against ¥20,270,000 in the previous wave, and the household head's own cover at ¥12,580,000
against ¥13,860,000 [R11]. A declining income benefit is priced against a need that also
declines — a surviving family needs replacement income until the children are independent,
not a level lump sum for thirty-five years. The anchor cell below shows the arithmetic
consequence: ¥150,000 a month to age 65 from age 30 is a headline maximum benefit of
**¥63,000,000**, more than three times the average household lump sum, for a monthly premium
of ¥2,565 [S6] [S14]. The undiscounted total is not what the insurer is exposed to, which is
the first thing a model of this product has to get right.

**How large the product is, is not published.** The 生命保険協会 industry series reports 個人保険 in
force by category — 医療保険 4,545万件 (23.3%), 終身保険 3,848万 (19.7%), 定期保険 2,721万 (13.9%) by count,
with 定期保険 the largest by sum insured at 300兆4,672億円 (38.6%) and 43.2% of new business by sum
insured [REG-R31] — but has no 収入保障保険 line. Whether the category sits inside 定期保険 in that
taxonomy is [unverified]. The national household survey does not break the product out
either: a full-text search of the 200-page speed report returns no occurrence of 収入保障 [R11].
What can be said with a source is that ten carriers write it, and that the structural
variants they exhibit span the design space: 無解約返戻金型 and 低解約返戻金型, 定額型 and 逓増型 and 逓減型,
monthly and annual instalments, two to five rate classes, main-contract and rider
construction, full and relaxed underwriting. Nothing retrieved characterizes those carriers
by distribution model or size, so this document does not. Any claim about market share is
[unverified].

**Two documentary contrasts with the chassis.** First, one carrier publishes a monthly
premium grid by age and sex for two plan shapes [S6], where
[term life (定期保険)](../term_life/product-spec.md) had four such grids
— premium disclosure is thinner here, and the anchor rests on a single carrier's table.
Second, and more valuable, one 特約条項 publishes **the commutation factor tables themselves**
[S13], which no direct writer does. That single document is why the commutation basis in
this library is a **[std]** value inside a *published* range rather than a guess.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 定額型 収入保障保険, 無配当, 無解約返戻金型; the main contract (*shu-keiyaku*, 主契約) pays a death annuity and a 高度障害年金 of the same amount | [S2] [S5] [S6] [S7] [S9] [S15]; participation and cash value **[std]** (1) |
| Benefit shape | Level 年金月額 from the insured event to the expiry date, floored by the 最低支払保証期間 | [S1] [S3] [S5] [S9] [S12] [S14] |
| Lives basis | Single life. No joint-life basis appears in any retrieved document | [S1] [S3] [S5] [S14] |
| Regulatory class | 第一分野 (保険業法第3条第4項第1号) — a fixed-sum death cover, paid in instalments | [REG-R1] |
| Issue age (契約年齢) | 20–70, age last birthday (*man-nenrei*, 満年齢) with the fraction truncated | [S6] [S7] [S14]; envelope **[std]** (2) |
| 保険期間 | 歳満了 only — to a stated attained age, 45–90; **no 年満了, no 更新** | [S6] [S8]; menu **[std]** (3) |
| 保険料払込期間 | Equal to the 保険期間, always | [S2] [S8] [S12] |
| 年金月額 | ¥50,000 minimum, in ¥10,000 steps | [S6] [S8] [S12] |
| Benefit cap | 年金現価保険金額 ¥300,000,000 — a cap on the **present value**, not on the monthly amount | [S8]; adoption **[std]** (4) |
| 最低支払保証期間 | 2年 or 5年, elected at issue and not changeable | [S3] [S5] [S7] [S9] [S12]; menu **[std]** (5) |
| Rate classes | Four: 非喫煙者優良体 / 喫煙者優良体 / 非喫煙者標準体 / 喫煙者標準体, fixed at issue | [S2] [S5] [S14]; count **[std]** (6) |
| **Anchor model cell** | Male, 契約年齢 30, 65歳満了 (420 monthly steps), 最低支払保証期間 2年, 年金月額 **¥150,000**, 非喫煙者優良体, 月払保険料 **¥2,565** | premium [S6]; cell choice **[std]** (7) |

Footnotes to **[std]** rows:

1. Seven of the nine direct writers write 無配当無解約返戻金型, with no surrender value at any
   duration [S2] [S5] [S6] [S7] [S9] [S15] [S16]. One writes a **低解約返戻金型** design whose
   surrender value is the ordinary value times a reduced surrender-value ratio
   (*tei-kaiyaku-henreikin wariai*, 低解約返戻金割合) of **70%** [S12], and one 約款 retains full
   surrender value (*kaiyaku-henreikin*, 解約返戻金) and policy reserve (*sekinin-junbikin*,
   責任準備金) machinery in its text although the product is sold without a value
   [S1 第23条・第24条]. No
   retrieved product pays a policyholder dividend [S1 第39条] [S2] [S5] [S15]. Composite: 無配当,
   無解約返戻金型 — the mode, and the design for which the widest evidence exists. The 70% variant
   is Variations, item 8.
2. Observed: 15–75 [S12], 20–70 [S6] [S7] [S14], 20–80 [S8]; two carriers publish no range
   at all [S2] [S3] [S5]. Composite: 20–70, the modal envelope at three carriers. 契約年齢 is
   the 満年齢 with the fraction truncated —
   「契約日における満年で計算し、1年未満の端数は切り捨てます」 [S1 第37条], worked as 「35歳7カ月の被保険者の方の契約年齢は35歳」 [S14]. That
   is not the age basis the valuation table is built on (Regulatory context; the
   [term life technical notes (定期保険)](../term_life/technical-notes.md) carry the reconciliation).
3. Every published contract example sets the term as to a stated attained age (*sai manryō*,
   歳満了): 60歳満了 [S2] [S6] [S9] [S12], 65歳満了 [S2] [S5] [S6] [S14] [S15] [S17], to 90歳 at the
   extreme [S6] [S8]. Minimum expiry 45歳 and maximum 90歳 are published by one carrier [S8],
   maximum 90歳 by a second (75歳 when a named 特約 is attached) [S6]. **No retrieved document
   offers renewal (更新)** and one states the absence in terms [S5]. That is the single
   largest structural delta from the chassis, where 年満了 with automatic renewal at
   attained-age rates is the base design
   ([term life product specification (定期保険)](../term_life/product-spec.md)).
4. Only one carrier publishes a benefit ceiling, and it is expressed as a present value:
   年金現価保険金額 ¥300,000,000 [S8]. Two others publish only floors — the residual 年金月額 after a
   partial commutation may not fall below ¥50,000 [S7], and any payout election must leave
   at least ¥50,000 a month [S6]. Composite: adopt the one published cap, because a
   PV-denominated cap is the only ceiling that binds consistently across issue ages on a
   declining benefit; a cap on 年金月額 would bind far harder at age 30 than at age 60.
5. Published menus: 1年/5年 [S2] [S3]; 2年/5年 [S7]; 2年, with 5年 opened by a 平準払込方式 premium
   election [S9]; 2年/3年/5年/10年 [S5]; 1年/2年/5年 [S12]; 「会社の定める範囲内」 with no values [S1 第1条第2項].
   The union is 1, 2, 3, 5 and 10 years; **5年 appears in every published menu** and 2年 in
   four of the five. Composite: {2年, 5年}, with 2年 the anchor default because it is the
   guarantee the only published premium grid is priced on [S6]. One carrier notes that some
   guarantee lengths become unavailable at some combinations of issue age and term [S5]; the
   composite does not model that restriction.
6. Structures observed: two classes (非喫煙優良体型 / 標準体型) [S6]; **four** (非喫煙者優良体 / 喫煙者優良体 /
   非喫煙者標準体 / 喫煙者標準体) [S2] [S5] [S14]; five, the four plus a 保険料率区分なし cell used when the
   contract is written without death cover [S7]; the class delivered as a 健康体料率特約 rider
   [S11]; and two separable discount 特約 [S16]. Composite: four, the mode. What is published
   about them is unusually concrete — they are gated on **measurements**, not declarations
   (footnote 9) — but **no carrier publishes the premium differential between classes for
   this product**, so the class loading itself is a **[std]** parameter in the technical
   notes, not a sourced one.
7. The anchor is the one cell where a published premium and a published benefit illustration
   meet. The premium ¥2,565/month is the published 65歳満了 / 保証2年 / 非喫煙優良体型 / 年金月額¥150,000
   rate for a male aged 30 [S6]; the benefit arithmetic — 420 instalments of ¥150,000 for a
   death in the first policy month, ¥63,000,000 in total — is the first case of another
   carrier's published three-case illustration at the identical age, term and monthly amount
   [S14]. Two honest qualifications. The premium comes from a **two**-class carrier, so its
   非喫煙優良体型 is not exactly the composite's 非喫煙者優良体 cell; and [S14]'s illustration is written
   on a 5年 guarantee, which changes nothing before the last two policy years. Total premium
   if the contract runs to expiry is ¥2,565 × 420 = **¥1,077,300**, about 1.7% of the
   headline maximum benefit. The annual premium of ¥30,780 sits in the lowest published
   household band of 年間払込保険料 (under ¥120,000, 17.8% of households) [REG-R32], which is the
   right order for one policy inside a household's average of several.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level for the whole 保険期間. No review mechanic and no renewal repricing appears in any retrieved document | [S1] [S2] [S5] [S6] [S8] [S12] |
| Frequency | 月払 default; 半年払 and 年払 available | [S1 第12条]; default **[std]** (8) |
| Payment route | 口座振替, 送金, 団体扱・集団扱, or クレジットカード | [S1 第13条] |
| Rate structure | Not published as a rate table by any carrier. Published rate points only; the office premium is a model-point input | [S6] [S12]; gap (9) |
| Rating factors | Sex, 契約年齢, 保険期間 (expiry age), 年金月額, 最低支払保証期間, rate class | [S6] [S12] |
| Premium ceases | On an annuity event: no further premium is payable once the death or 高度障害 annuity begins | [S1 第12条第2項] [S3 第5条] [S8] |
| Advance payment (前納) | Available at an insurer-set discount; not modeled | [S1 第14条]; scope **[std]** (8) |
| Non-level patterns | A two-step premium (ステップ払込方式) exists at one carrier and a 平準払込方式 is named as one option at another; **out of scope** | [S1 第43条] [S9]; scope **[std]** (10) |
| Large-case discount (高額割引) | Exists at one carrier; thresholds not published; not applied | [S6]; scope **[std]** (10) |
| Pricing basis (assumed interest rate (*yotei riritsu*, 予定利率) etc.) | **Not published for any 収入保障 contract in the set.** The model's basis is **[std]** | [REG-R2]; gap (9) |

8. 月払・半年払・年払 are all available [S1 第12条] and the grace table distinguishes them [S1 第15条]
   [S4]. Monthly is the mode of the published examples and the frequency the only published
   rate grid is quoted in [S6], and the model runs on a monthly grid, so the composite
   defaults to 月払 and omits 前納, whose discount rate is insurer-set and unpublished.
9. Published rate points, and there are only three sets in the whole session's evidence:
   60歳満了 / 保証2年 / 非喫煙優良体型 / 年金月額¥100,000 at
   ¥1,410 (M30), ¥1,340 (M35), ¥1,360 (M40), ¥1,330 (M45) and ¥1,200 / ¥1,330 / ¥1,400 /
   ¥1,340 for females at the same ages; 65歳満了 / 保証2年 / 非喫煙優良体型 / 年金月額¥150,000 at ¥2,565 /
   ¥2,565 / ¥2,730 / ¥2,865 (M) and ¥2,175 / ¥2,475 / ¥2,700 / ¥2,760 (F), both as at
   2025年12月2日 [S6]; and one 低解約返戻金型 point, 30歳男性 / 60歳満了 / 保証1年 / 年金月額¥200,000 at ¥5,780
   [S12]. Two features of that grid are worth a model's attention. Premiums are **nearly
   flat in issue age** on the 60歳満了 plan — ¥1,410 at 30 against ¥1,330 at 45, a *fall* of
   5.7% — because the shortening term offsets rising mortality, where a level-term premium
   at a fixed term rises steeply with age. And per ¥10,000 of 年金月額 the 65歳満了 plan costs
   ¥171.0 a month against ¥141.0 for the 60歳満了 plan, the price of the extra five years of
   run-off. The 低解約返戻金型 point works out at ¥289 per ¥10,000, roughly double, but the
   carriers, guarantee lengths and rate classes all differ, so that is not a controlled
   comparison of the cash value's price. The parameters behind any of these numbers — 予定利率,
   予定死亡率, 予定事業費率 — sit in the 保険料及び責任準備金の算出方法書
   filed under 保険業法第4条第2項第4号 and are not public [REG-R2].
10. The two non-level premium patterns are real and documented — one 約款 provides that
    premiums after an insurer-set ステップ期間 are the earlier premium times an insurer-set factor
    [S1 第43条], and one carrier's product page names a 平準払込方式 as one election among others
    and couples the 5年 guarantee to it [S9] — but neither publishes the factor or the step
    date, so a composite that included them would be inventing the numbers. Same reason for
    高額割引, whose existence is published and whose thresholds are not [S6]. Both are excluded
    and named, not silently dropped.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Death annuity (遺族年金) | 年金月額, monthly, from the insured event to the 保険期間満了日, extended where the 最低支払保証期間 requires it | [S1 第3条] [S3 第3条] [S5] [S9] [S12] [S14] |
| 高度障害年金 | **The same 年金月額 on the same timetable and the same guarantee**, on entering a 高度障害状態 within the 保険期間; the two annuities are mutually exclusive | [S1 第3条] [S3 第3条] [S5] [S9] |
| Instalment count | `max(N - m + 1, G)` — one instalment per monthly payment date from the event to expiry, floored at the guarantee | [S5] [S14] [S15]; derivation (11) |
| Payment timetable | First instalment on the **day before** the first monthly policy anniversary falling on or after the event; each later instalment on the day before the corresponding anniversary | [S1 第3条第2項] [S5]; pick **[std]** (12) |
| Recipient's death | Remaining instalments commuted and paid as a lump sum to the 法定相続人 | [S1 第3条第6・7項] [S3 第7条] [S14] |
| Survival condition | **None** on the composite: instalments do not depend on the recipient being alive | [S1] [S5] [S14]; pick **[std]** (12) |
| Commutation (一括受取) | The recipient may take the present value of unpaid instalments in whole, in part, or as the residue mid-payment | [S2] [S3] [S5] [S7] [S10] [S12] [S14] |
| Commutation basis | Annuity-certain at **0.65% p.a. effective**, monthly in arrears | **[std]** (13) |
| Residual floor | A partial commutation is refused if it leaves the 年金月額 below ¥50,000 | [S7]; [S1 第5条第3項] [S3 第6条第4項] [S14] |
| Suicide exclusion | No annuity where the insured dies by suicide within **3 years** of the 責任開始期, reset to the last 復活 | [S1] [S3] [S4] [S5]; identical to the chassis |
| Other 免責事由 | 故意 of the 保険契約者 or 受取人; 戦争その他の変乱 as a **reduction power**, not an absolute exclusion | [S1 第3条・第4条] [S3 第3条・第4条] |
| Amount on a 免責 | 責任準備金 to the policy owner; **nothing** where the policy owner caused the death; a reduced commuted amount may not fall below the 責任準備金 | [S1 第3条第10項] [S3 第3条第17項・第4条] |
| 満期保険金 | None on the 主契約. One carrier sells a 満期給付金支払特則; out of scope | [S12]; scope **[std]** (14) |
| Graded early benefit | None on the composite. The 引受基準緩和型 variant pays **50%** for illness death in policy year 1 | [S15]; scope **[std]** (14) |

11. The rule is derived from three published illustrations and reproduces all of them. With
    `N` the term in months, `m` the policy month in which the insured event falls and `G`
    the guarantee in months: 65歳満了 from 契約年齢30 gives `N = 420`, and the published counts are
    420 for month 1, 240 for 15年1か月 (`m = 181`), 60 for 30年1か月 (`m = 361`) [S14]; 411 for a
    death at 10 months and 178 for 20年3か月 (`m = 243`) [S15]; and on a 5年 guarantee, 420 for
    the first month, 246 after 14年6か月 elapsed and **60** for a death 33 years in, where the
    remaining term is 24 months and the guarantee binds [S5]. Carriers label the elapsed
    duration inconsistently — one counts the month of the event, another counts completed
    months — but every published count satisfies the same arithmetic, and the guarantee case
    is the only one where the two conventions could not both hold.
12. The two-carrier modal timetable is adopted [S1 第3条第2項] [S5]. One carrier instead sets a
    年金支払基準日 equal to the event date and runs monthly anniversaries off it, making the first
    instalment effectively immediate, and makes second-and-later instalments payable **only
    while the recipient is alive**, commuting the residue to the 法定相続人 on the recipient's
    death [S3 第3条第3項] [S3 第7条]; a third runs later dates off the monthly policy anniversary
    following the first payment [S15]. Composite: instalments in arrears with the first at
    most one month after the event, and **no recipient-mortality decrement** — every other
    retrieved carrier reaches the same cash flow by commuting on the recipient's death
    rather than by a survival condition [S1] [S14], so the annuity is an annuity-certain and
    no post-event mortality basis is needed.
13. **The single most important [std] number in this product, and the best-evidenced.** No
    direct writer publishes the discount basis; the wordings are 「年金月額に所定の係数を乗じた額」 [S6],
    「将来に発生する利息を差し引いて算出した現在の保険契約の価値」 [S10], 「将来に発生する利子を割引いて算出した現在の保険契約の価値」 [S12] and
    「年金基金設定時の基礎率で計算」 [S17]. Four published anchors bound it. (i) One 特約条項 publishes the
    factor table: 年金の現価相当額 = 基本年金額 × a tabulated rate with no dependence on the annuitant's
    age or sex, running 4.975 at a 5-year payment period, 9.801 at 10, 14.474 at 15, 18.997
    at 20, 23.377 at 25, 27.616 at 30 and 39.542 at 45 [S13 別表1]; fitting an annual
    annuity-due **less a small constant** to those gives about **0.61% p.a.**, and the
    second column of the same table, for a different main contract, about 1.45%. The
    constant matters to the fit and is stated rather than dropped: a plain annuity-due with
    no constant fits the same seven factors at 0.59%. (ii)–(iv) Three carriers publish a
    worked commutation amount: ¥100,000 × 180 instalments commuted to ¥16,594,260 [S6],
    ¥200,000 × 300 to 約¥55,310,000 [S10], and ¥100,000 × 300 to 約¥27,640,000 [S17] —
    **ratios of 0.92190, 0.92183 and 0.92133**, a remarkably tight cluster across very
    different terms. The only two independent published anchors are 0.61% from the factor
    table and 0.66% implied by the two 300-instalment amounts; their midpoint is 0.635%,
    and the composite takes that rounded to the nearest 0.05% — **0.65% p.a. effective**.
    It reproduces those two amounts to ¥27,688,945 (+0.18%) and
    ¥55,377,891 (+0.12%), both inside the published rounding of 約. It does **not** reproduce
    the 180-instalment amount: at 0.65% that stream commutes at a ratio of 0.9527, not
    0.9219. That is not a failure of the fit but a fact about the data — **no single flat
    rate can produce a near-constant ratio at 180 and at 300 instalments**, so either the
    carriers' bases differ or a term-dependent adjustment is in use, and neither is
    published. The technical notes carry this as a sensitivity, and the observed range to
    test over is **0.61%–1.45%**.
14. Two designs sit outside the composite and are named so a reader knows they exist. A
    満期給付金支払特則 adds a survival benefit at expiry where no annuity event occurred, and that
    benefit is explicitly **not** subject to the carrier's 70% low-surrender factor [S12].
    The relaxed-underwriting (引受基準緩和型) version grades the benefit: death from the 責任開始日 to
    the day before the first policy anniversary pays 50% of the 年金月額, with 不慮の事故 and
    specified 感染症 deaths paying in full, and the worked example applies the 50% across all
    411 remaining instalments [S15] — a per-instalment reduction, not a shortened stream.

### Options

| Parameter | Representative value | Basis |
|---|---|---|
| Payout elections | 全部一括受取, 一部一括受取, 残額一括受取 | [S2] [S3] [S12]; menu **[std]** (15) |
| — 一部一括受取 restrictions | Not available once the first instalment has been paid; limited to **once** during the term | [S3 第6条第4項第1号] [S10] [S12] |
| — effect of a full commutation | Extinguishes the contract | [S1 第5条第2項] [S3 第6条第3項] [S12] [S14] |
| 保険料払込免除 | In the 主契約: premiums waived where the insured, from an 不慮の事故 on or after 責任開始期, comes within **180 days** to a 別表4 身体障害の状態. Disease-based waiver is a rider only | [S1 第6条] [S3 第8条] [S5] [S6] |
| リビング・ニーズ特約 | Attached automatically and free. Pays the 年金現価 of the designated 年金月額 less six months' interest and premium equivalent, capped at **¥30,000,000**; barred in the final year before expiry | [S2] [S5] [S7]; attachment **[std]** (15) |
| Reduction (減額) | Permitted above an insurer-set floor; on a 無解約返戻金型 contract it produces **no refund at all** | [S1 第28条] [S3] [S7] |
| 指定代理請求人特約 | Standard; a nominated proxy may claim where the insured cannot | [S1] [S5] [S12] |
| 更新 / conversion / indexation / joint life | **No 更新 in any retrieved document.** One carrier offers 保険契約の変換 into a 定期保険 or 終身保険 without underwriting, blocked in the final two years | [S5]; [S6]; scope **[std]** (16) |

15. All four payout elections in the set are: 全部一括受取 at **all nine** direct writers [S1]
    [S2] [S3] [S5] [S6] [S7] [S10] [S12] [S14] [S17] — the one election that does not vary;
    一部一括受取 at six of them [S2] [S3] [S5] [S7] [S10] [S12] [S14]; 残額一括受取, taken
    mid-payment, at two [S2] [S3] [S12]; and deferral of instalments, in whole or part
    (すえ置) at one [S5].
    Composite: the first three, dropping すえ置 as a single-carrier election that adds a
    deferred-interest basis nobody publishes. リビング・ニーズ特約 is attached automatically and free
    at three carriers [S2] [S5] [S7], and its terms — 年金現価 of the designated amount, less
    six months' interest and premium equivalent, ¥30,000,000 cap, no claim in the final year
    — do not vary where it exists [S2] [S5]. It is the same rider on the same terms as on
    the chassis ([term life product specification (定期保険)](../term_life/product-spec.md)), with one
    product-specific consequence: on
    this product the amount is the present value of an income stream, so the cap binds far
    earlier in the term than it does on a level sum assured.
16. The absence of renewal is a product fact, stated in terms by one carrier [S5] and
    implied by every other carrier's 歳満了-only term menu. Its replacement, where one is
    offered, is 保険契約の変換 — conversion into a 定期保険 or a 終身保険 without underwriting, unavailable
    in the last two years before expiry [S6]. The composite scopes conversion out: it
    creates a new contract on a different chassis at then-current rates, so it produces no
    liability on the modeled policy, exactly as the chassis treats its own out-of-scope
    options.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 解約返戻金 | **None, for the whole term** | [S2] [S5] [S6] [S7] [S9] [S15] |
| Grace (猶予期間), 月払 | From the first day of the month following the 払込期月 to the last day of that month | [S1 第15条] [S3] [S4] |
| Claim during grace | The unpaid premium is deducted from the annuity payable; if that is insufficient, from the 死亡時保障換算額, and the 基準年金月額 is restated | [S1 第16条第1項] [S1 第12条第5項] |
| Lapse (失効) | The day after grace ends; nothing payable | [S1 第15条第2項] |
| Reinstatement (復活) | Available for **3 years** from lapse, on fresh underwriting and arrears with interest; the rate class carries over unchanged | [S1 第17条] [S3] [S5] |
| 自動振替貸付 / 契約者貸付 | **Explicitly not offered.** With no cash value there is nothing to lend against | [S2] |
| 告知義務違反 | Rescission within **2 years** of the 責任開始日 or last 復活日; after two years still available where the event occurred inside them | [S1 第21条第5号] [S4] [S5] |
| 時効 | Rights to an annuity, the 責任準備金, the 解約返戻金 or a waiver extinguish after 3 years | [S1 第41条] |
| クーリング・オフ | 14 days from the later of application and receipt of the 注意喚起情報, against a statutory floor of 8 days; **out of scope** | [S5] [REG-R36]; scope **[std]** (17) |

17. 保険業法第309条 gives an eight-day cooling-off effective on dispatch of the withdrawal
    document [REG-R36]; one carrier contracts for 14 days [S5], permitted because it favours
    the policyholder. As on the chassis, the model begins with cover in force and the
    cooling-off population already out, and says so rather than absorbing it into a
    first-year lapse rate.

---

## Contractual mechanics

Everything in this section that is *not* stated here is stated in the
[term life product specification (定期保険)](../term_life/product-spec.md) — the three 免責事由 and what is
paid on each, the two-year and
three-year windows and the clocks they run on, the grace-to-失効-to-復活 sequence, the 別表3
高度障害状態 schedule with its numeric 備考, and the reasoning behind treating 死亡 and 高度障害 as one
decrement. All of it applies here unchanged, and the source tags above confirm it carrier by
carrier for this product too.

### The benefit: a declining annuity-certain

Let `N` be the 保険期間 in months, `m` the policy month in which the insured event falls, `G`
the 最低支払保証期間 in months, and `A` the 年金月額. The number of instalments is

    n_pay(m) = max(N - m + 1, G)

and the total benefit is `A × n_pay(m)`, paid monthly in arrears with the first instalment
falling on the day before the first monthly policy anniversary on or after the event [S1
第3条第2項] [S5]. Two properties follow, and both are the product.

**The benefit falls by one instalment every month.** At the anchor cell, `N = 420` and `A =
¥150,000`: a death in policy month 1 pays ¥63,000,000, in month 181 pays ¥36,000,000, in
month 361 pays ¥9,000,000 [S14]. There is no schedule, no rate and no formula behind the
decline — it is the calendar. That is the sharpest contrast with a UK decreasing term
assurance, whose benefit falls on a *notional mortgage schedule* at a chosen interest rate,
and with the 逓減定期保険 sold in Japan, whose benefit falls by `基本保険金額 ÷ 保険期間` a year and whose
**premium falls with it** ([term life product specification (定期保険)](../term_life/product-spec.md)).
Here the premium is level and
the benefit declines by construction.

**The tail does not go to zero.** Without the guarantee the benefit would decline to a
single instalment on the day before expiry. The guarantee stops that.

### 最低支払保証期間 — a term extension, not a benefit floor

This is the mechanic to get right, and the one an implementation is most likely to get
wrong. Where the insured event occurs so late that the remaining term is shorter than the
guarantee, **the annuity payment period is extended past the policy expiry date** until the
guarantee has run [S1 第3条第2項] [S3 第3条第3項] [S5] [S12] [S14]. One 約款 words it as an extension
of the insurance period itself — 「保険期間は、死亡し…た日からその日を含めて最低支払保証期間を経過した日までとします」 [S1 第3条第2項] —
and another as an equality of periods, 「年金支払期間は支払保証期間と同じ期間とします」 [S3 第3条第3項]. Both produce
the same cash flow, and it is not the same cash flow a floor would produce.

The difference matters because the two implementations diverge in *timing*, not in amount. A
benefit floor pays `max(N - m + 1, G)` instalments **inside** the original term, compressing
them; the term extension pays them **after** expiry, on the same monthly timetable. On the
anchor cell a death in policy month 419 pays 24 instalments running to policy month 442 — 22
months beyond the 保険期間満了日. A projection that terminates all states at `t = N` therefore
truncates real cash flow, and a reserve that stops at `N` is short. The rider construction
at one carrier reaches the same economics from the other side and confirms the reading: its
年金支払期間 shortens by one year at every policy anniversary but is **floored at 5 years** [S13
第5条], which is the same promise expressed as a floor on the payment term.

Two further consequences are published. Riders written on the chassis inherit the main
contract's guarantee — a 就労不能保障特約's guarantee period 「は主契約の最低保証期間と同一」 [S11], and the 障害年金
and 介護年金 under one carrier's 生活支援特則 use the main contract's 最低支払保証期間 [S5]. And under that
特則, where a disability or care annuity starts just before expiry and the insured then dies,
the payment period runs from the **first disability or care annuity payment date** plus the
guarantee [S5] — the guarantee attaches to the first annuity event, not to the death.

### 一括受取 — commutation

The recipient may take the present value of the unpaid instalments as a lump sum, in whole,
in part, or as the residue during payment [S2] [S3] [S5] [S7] [S10] [S12] [S14]. With `i`
the commutation rate and `v = (1 + i)^(-1/12)`:

    L(n) = A * v * (1 - v^n) / (1 - v)

for `n` unpaid instalments, at `i` = 0.65% p.a. effective **[std]** (footnote 13). At the
anchor cell a death in policy month 1 commutes ¥63,000,000 of instalments to
**¥56,352,382**, a ratio of 0.8945; at 300 remaining instalments the ratio is 0.9230,
against the 0.9213–0.9219 the three published illustrations show [S6] [S10] [S17].

Three contractual restrictions bind and are cited. A partial commutation reduces the future
年金月額 and is refused where the residual falls below the insurer's minimum, published as
¥50,000 at one carrier [S7] [S1 第5条第3項] [S3 第6条第4項] [S14]. 一部一括受取 is unavailable once the
first instalment has been paid [S3 第6条第4項第1号] and is limited to once during the term at two
carriers [S10] [S12]. And paying the whole present value **extinguishes the contract** [S1
第5条第2項] [S3 第6条第3項] [S12] [S14] — commutation is a settlement of the claim, not a policy
alteration, so in a projection it changes the shape of the claim payment and nothing else.

The published factor table is worth one further note, because it is the only one of its
kind. Its 年金の現価相当額 depends on the payment period and the type of main contract and
explicitly **not** on the annuitant's age or sex [S13 別表1] — direct confirmation that the
post-event stream is an annuity-certain. A companion table gives 未払年金の現価 by 残存年金支払回数 (38.792
at 44 remaining payments, 19.007 at 20), then further discounts it from the request date to
the day before the next payment date by a method the insurer determines [S13 別表2]. The 別表2
factors sit about 0.010 above the 別表1 factors at equal counts; no explanation is published
and none is asserted here.

### Rate classes gated on measurements

The composite's four classes are 非喫煙者優良体, 喫煙者優良体, 非喫煙者標準体 and 喫煙者標準体 [S2] [S5] [S14]. What
is unusual, and worth a model's attention, is that the qualification is **measured rather
than declared**: BMI of 18.0 or more and under 27.0, 最大血圧 under 140 mmHg **and** 最小血圧 under
90 mmHg, and no tobacco in the past year [S2] [S5], with one carrier at 139/89 mmHg for its
single preferred class [S6] and one banding the thresholds by issue age — BMI 17–27 at
契約年齢20–39 and 17–28 at 40–70, 最高血圧 under 140 then under 150, 最低血圧 under 90 then under 100
[S14]. 「喫煙」 is defined broadly enough to include cigars, pipe, chewing and snuff tobacco,
e-cigarettes, heated tobacco and nicotine patches or gum [S2] [S5] [S6], and non-smoker
status is verified by a **cotinine (コチニン) test** within an insurer-set range, which passive
smoking can fail [S2] [S5]. A preferred class additionally requires a 健康診断結果通知書 or a 人間ドック
result; without one the standard class applies [S2] [S5].

Two facts a model must carry. **The class is fixed at issue and cannot be changed later**
even if BMI, blood pressure or smoking status changes [S2] [S14], and it survives a lapse: a
reinstated contract keeps the class it had before [S3]. And **the premium effect is not
published**. One carrier annotates each of its options by direction — 割引 for the
health-rating and health-check 特約 and for three benefit-narrowing 特則, 割増 for a
mental-illness 特則 and a waiver rider, no change for リビング・ニーズ特約 [S16] — which is a published
sign with no published magnitude. The only published magnitudes anywhere near this are rider
premiums: +¥30 for a three-disease waiver and +¥100 for a five-disease waiver on a
30-year-old male's ¥100,000-a-month plan [S6].

### Premium cessation on an annuity event

Once the death or 高度障害 annuity begins, **no further premium is payable** [S1 第12条第2項] [S3
第5条] [S8], and the recipient succeeds to the rights under the contract [S3 第5条]. This is not
the chassis's behaviour, where a death claim terminates the contract and the premium stream
with it in the same step; here the contract continues in a paid-up claims-in-payment state
for up to `N` further months, or beyond `N` where the guarantee extends it. A cash-flow
model that nets premiums against claims on a single in-force count will double-count the
premium in every month of an annuity run-off unless the claims-in-payment population is held
separately.

---

## Riders and options

**In scope (modeled or parameterized):**

- **高度障害年金** — in the 主契約, same 年金月額, same timetable, same guarantee, mutually exclusive
  with the death annuity [S1] [S3] [S5] [S9]. One decrement with death, for the reason the
  chassis gives: the 死亡保険用 valuation table already **includes** 高度障害 inside its death rate
  [R2] [REG-R20].
- **最低支払保証期間** — a model-point parameter with the composite menu {2年, 5年}, implemented as a
  term extension [S1] [S3] [S5] [S12] [S14].
- **一括受取** — parameterized: full commutation at the claim date, at the **[std]** 0.65%
  basis, switchable off in the base run [S2] [S3] [S5] [S7] [S10] [S12] [S14].
- **保険料払込免除** — the accident-plus-180-days-plus-別表4 waiver is specified and excluded from
  the base projection **[std scope]**, exactly as on the chassis; its incidence is not the
  高度障害 incidence [S1 第6条] [S3 第8条] [S5] [S6].
- **リビング・ニーズ特約** — parameterized as a discounted acceleration with the ¥30,000,000 cap and
  the final-year bar; on this product the cap binds early in the term [S2] [S5] [S7].
- **復活** — a reinstatement transition out of the lapsed state at a **[std]** behavioural
  rate, carrying the rate class over unchanged [S1] [S3] [S5].
- **減額** — a 年金月額 change with no payment on the 無解約返戻金型 composite [S1 第28条] [S3].

**Out of scope:** the 逓増型 benefit, `年金月額 = 基準年金月額 × (1 + 0.03 × 経過年数)`, whose escalation
continues through the extended guarantee tail at 3% of the 基準年金月額 a year [S1 第1条・第2条]; the
引受基準緩和型 version with its 50% first-year grading [S15]; the 低解約返戻金型 version and its 満期給付金支払特則
[S12]; the rider construction with annual instalments and a 逓減 payment period [S13]; 一部すえ置
and 全部すえ置 deferral [S5]; and the whole disability and care family sold on this chassis —
生活支援特則 (障害年金 on a 身体障害者手帳 grade 1–4 or 介護年金 on 要介護1以上 certification) [S5], 障害介護収入保障特則 and
高度障害収入保障特則 [S7], 無解約返戻金型就労不能保障特約 [S11], 収入サポート特約 with its income-tested benefit ceilings and
its 60-occurrence short-term benefit [S6], 無解約返戻金型メンタル疾患保障付七大疾病保障特約 with a *fixed* 2- or
5-year payment period [S11], ストレス・メンタル疾病サポート特則 [S16], and 配偶者同時災害死亡時割増特則, under which a
same-accident death of the insured and the legally married spouse pays two full guaranteed
annuities **at no extra premium** [S5]. Disease-based waiver riders — three-disease,
five-disease and seven-disease variants with 90-day cancer waiting periods and differing
heart and cerebrovascular triggers [S2] [S5] [S6] [S11] [S16] — are out of scope. The
care-income 特則 turn on 要介護状態 as defined by 介護保険法第7条 [REG-R42]; written alone they would be
third sector (*dai-san-bun'ya*, 第三分野) business, which is why they are 特則 on a 第一分野 main
contract [REG-R1].

**Absent from the market rather than out of scope:** no retrieved document offers 更新, joint
life, indexation, or a guaranteed-insurability option on the main contract. The nearest
thing is one carrier's 保険契約の変換 into a different product without underwriting [S6].

---

## Variations across insurers

1. **The guarantee menu.** 1年/5年 [S2] [S3]; 2年/5年 [S7]; 2年 with 5年 opened by a premium-
   pattern election [S9]; 2年/3年/5年/10年 [S5]; 1年/2年/5年 [S12]; unpublished 「会社の定める範囲内」 [S1];
   and, on the rider construction, a 5-year **floor** on a shrinking period [S13].
   Composite: {2年, 5年} (footnote 5).
2. **How the guarantee is implemented.** A term extension past expiry at four carriers [S1]
   [S5] [S12] [S14]; an equality of the 年金支払期間 with the 支払保証期間 at one [S3]; a floor on a
   shrinking payment term at the rider carrier [S13]. All three produce the same instalment
   count. Composite: the term extension, the mode and the wording that makes the post-expiry
   cash flow explicit.
3. **Instalment frequency and the survival condition.** Monthly everywhere except the rider
   construction, which pays **annually**, with second and later payments on the annual
   anniversary of the first [S13 第6条]. One carrier alone conditions second-and-later
   instalments on the recipient being alive [S3 第3条第3項]; the others reach the same result by
   commuting on the recipient's death [S1] [S14]. Composite: monthly, no survival condition
   (footnote 12).
4. **Rate-class structure.** Two [S6], four [S2] [S5] [S14], five [S7], delivered as a rider
   [S11], or split into two separable discount 特約 [S16]. Thresholds are published and
   numeric everywhere they exist, and age-banded at exactly one carrier [S14]. Composite:
   four (footnote 6).
5. **Benefit shape.** 定額型 at all nine direct writers, one of which **also** offers 逓増型, the
   escalating version adding 3% of the 基準年金月額 a year and continuing to escalate through the
   guaranteed tail [S1 第2条]; 逓減型 and 固定型 as the two types at the rider carrier [S13].
   Composite: 定額型 (Riders, out of scope).
6. **高度障害 cover.** In the 主契約 at eight of the nine direct writers [S1] [S3] [S5] [S9] [S12]
   [S14]; at the ninth it is an optional 高度障害収入保障特則, mutually exclusive with an alternative
   障害介護収入保障特則, and that carrier will also switch the **death** cover off (死亡収入保障年金不担保特則) so
   the contract becomes a pure disability and care income policy [S7]. Composite: in the 主契約
   — and the variant is the clearest evidence that the death cover and the disability cover
   are separable modules, not one benefit.
7. **Commutation disclosure.** Factor tables published at one carrier [S13 別表1・別表2]; a
   worked numeric example at three [S6] [S10] [S17]; nothing but a wording at the rest [S2]
   [S3] [S5] [S12] [S14]. Composite: **[std]** 0.65% p.a. with the published range
   documented (footnote 13). This is the parameter where the gap between what is contractual
   and what is published is widest.
8. **Surrender value.** None at seven of the nine direct writers [S2] [S5] [S6] [S7] [S9]
   [S15] [S16]; a **低解約返戻金型** design at one, the surrender value being the ordinary value
   times a 低解約返戻金割合 of **70%** [S12]; and one 約款 that retains the machinery in its text for a
   product sold without a value [S1 第23条・第24条]. The 70% variant has a feature worth
   recording: because the 保険料払込期間 equals the whole 保険期間 here, there is **no 払込満了 step-up to
   100%** — the suppression runs to expiry, so the cliff that characterises 低解約返戻金型 whole
   life has no analogue on this product [S12]. Composite: no surrender value (footnote 1).
9. **Issue and term envelope.** 契約年齢 15–75 [S12], 20–70 [S6] [S7] [S14], 20–80 [S8]; maximum
   expiry 90歳 at two carriers [S6] [S8], 75歳 at one of them when a named 特約 is attached
   [S6]; two carriers publish neither [S2] [S3] [S5]. Composite: 20–70, 歳満了 45–90
   (footnotes 2, 3).
10. **Underwriting tier.** One carrier sells a named 引受基準緩和型 version [S5] [S15], one states
    explicitly that it offers **no** relaxed-underwriting version [S7], and the rest are
    silent. The relaxed version is priced above the fully underwritten product and grades
    the first year's benefit to 50% [S15]. Composite: fully underwritten only.
11. **What does not vary.** Across all nine direct writers (the rider construction [S13] is
    excluded, being the one design that pays annually and shrinks its payment period), the
    benefit is a **level monthly annuity from the insured event to a fixed
    expiry date**, so the total falls month by month; a guarantee period stops the tail
    reaching zero; 高度障害 is paid on the same terms as death and the two are mutually
    exclusive; the recipient may commute the remaining instalments; **premiums cease on an
    annuity event**; 保険料払込期間 equals 保険期間; the suicide exclusion runs **3 years** from the
    責任開始期 and the 告知義務違反 window **2 years**; grace for monthly premiums runs to the end of
    the following month and 復活 is available for **3 years**; and every product is 無配当 with
    no policyholder dividend. A composite may choose among the ten items above; it may not
    alter these and still be describing 収入保障保険.

---

## Regulatory context

**Classification — and why it is a first-sector product.** 保険業法第3条第4項第1号 defines 第一分野 as
fixed-sum insurance on human survival or death, and separates it from the 第三分野 list of
sickness, injury and nursing-care covers [REG-R1]. 収入保障保険 is squarely first-sector: the
insured event is death or 高度障害, and paying the fixed sum in monthly instalments changes the
settlement, not the trigger. That is precisely why the disability and care income benefits
described above are sold as 特則 attached to this contract rather than as the contract itself
[S5] [S7] [S11], and why one carrier needs a 死亡収入保障年金不担保特則 to write the disability cover on
its own [S7].

**Prudential — ESR, and what it replaced.** From **2026年3月31日** insurers are supervised on
the economic-value-based solvency regulation (*keizai-kachi bēsu no soruvenshī kisei*,
経済価値ベースのソルベンシー規制, **ESR**): assets at fair value, insurance liabilities as the current
estimate (*genzai suikei*, 現在推計) re-measured at each 基準日 plus a MOCE, calibrated to 99.5%
over one year, with early corrective action triggered below **100%** [REG-R15]. It replaces,
as the trigger, the ソルベンシー・マージン比率 threshold of **200%** [REG-R17] [REG-R15]. `jplib`
computes neither ratio. What matters for this product is the re-measurement: a benefit whose
amount is a function of the *time* the claim occurs, discounted on a curve that moves, is
far more interest-sensitive than a level sum assured, and a locked-in basis hides it.

**Statutory reserving — cited, not reproduced.** A conventional guaranteed 収入保障 contract is
inside the standard policy reserve (*hyōjun sekinin junbikin*, 標準責任準備金) regime: 保険業法第116条第2項
delegates the method and the coefficients [REG-R4], and 施行規則第68条 excludes only
separate-account-linked contracts, contracts with no 保険料積立金, contracts where the insurer has
disclosed it may change the basis, and residually designated classes — none of which catches
this product [R8] [REG-R7]. 第69条 requires 保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金 per category [R8]
[REG-R8]. The discount rate is the standard valuation interest rate (*hyōjun riritsu*,
**標準利率**), which the supervisory guideline defines as 「責任準備金告示に規定する予定利率」 [R9]; the 告示 is
**平成8年大蔵省告示第48号**, amended alongside 平成13年金融庁告示第24号 with effect from 令和3年10月1日 and 令和4年4月1日
[R10] [REG-R10]. Its **current numeric value could not be established from any retrieved
document and is [unverified]** — the 新旧対照表 attachments on the regulator's page were not
fetched [R10]. This library projects gross cash flows and builds none of these reserves.

**The valuation table, and the one place this product simplifies it.**
生保標準生命表2018（死亡保険用）applies from April 2018 [R3] [REG-R11] and is published in full, free, at
a stable public URL by 日本アクチュアリー会 as the 指定法人 under 保険業法第122条の2第1項 [R3] [REG-R18]: male qx
is 0.00068 at 30, 0.00653 at 60, 0.01015 at 65 and 0.05006 at 80; female qx is 0.00363 at 60
[R1]. Two qualifications carry over from the chassis. The publisher's terms restrict
reproduction, so the library **cites** the table, quotes only the rates a worked example
needs, and **ships** its mortality CSV as a **[std]** construction whose `provenance` column
points at the IAJ entries [REG-R21]. And it is a **valuation** table — a 2σ risk-theory
margin capped at 130% of the unadjusted rate, a forward improvement allowance of 2.5% p.a.
for five years then 1.0% for three, built on an age nearest birthday (*hoken-nenrei*, 保険年齢)
basis, and **including 高度障害 inside the
death rate** [R2] [REG-R20] — so a best-estimate basis is a **[std]** adjustment of it.

The simplification is this: **no post-event mortality basis is needed.** On the composite
the annuity is an annuity-certain, confirmed from the contract side by a factor table that
explicitly does not depend on the annuitant's age or sex [S13 別表1], so the 年金開始後用 table —
which stays on the 2007 vintage [REG-R11], and whose existence in a 2018 edition is
[unverified] against the retrieved table set [R1] — is not in play. The one carrier that
conditions instalments on the recipient's survival [S3] would need one, and is out of the
composite partly for that reason.

**Professional standards.** 保険業法第121条第1項第1号 requires the 保険計理人 to confirm in an 意見書 that the
責任準備金 is accumulated on sound actuarial principles [REG-R6], and the IAJ practice standard
turns that into the **1号収支分析**: an annual forward projection of premiums, claims, expenses
and surrenders by 区分経理 segment over at least ten future years, tested for sufficiency over
the first five [REG-R22]. That is the regulatory use of a liability cash-flow model in Japan
and the shape this product's projection takes — with the caveat that a ten-year window on a
35-year contract sees only the early, largest instalment counts.

**Conduct.** The supervisory guideline fixes what a 契約締結前交付書面 must carry, including the
cover with its 支払事由 and 免責事由, the principal 特約, the level of any 解約返戻金, and クーリング・オフ, 告知義務,
責任開始期 and **払込猶予期間・失効・復活** [REG-R14] — every one of which is specified above with a source
tag. 保険業法第309条 gives the eight-day statutory cooling-off on a dispatch rule, contracted to
14 days at one carrier [S5] [REG-R36]. Where a 低解約返戻金型 design is sold, the 説明義務 under
金融サービス提供法第4条 reaches the suppression period and its effect [REG-R39] — relevant to the [S12]
variant, not to the composite. The contract itself is governed by the 保険法: 第51条 for the
statutory suicide exclusion, which has **no time limit** and which the 約款 narrows to three
years in the policyholder's favour [REG-R34], and 第55条, whose five-year ceiling and
one-month discovery clock bound the carriers' two-year contestability windows [REG-R35]. On
insurer failure 生命保険契約者保護機構 covers contracts up to **90% of the 責任準備金** under a rate
delegated by 保険業法第270条の3 to ordinance [REG-R40] [REG-R41]. Cited, never modeled.

**Tax — two layers, and the second is what makes this product different.** At the death the
object taxed for 相続税 is the right to the annuity (*nenkin jukyūken*, **年金受給権**), not the
instalments [R5]. A 有期定期金 whose 給付事由 has occurred is valued at the **greatest** of the
surrender value payable at that moment, the lump sum available in lieu of the annuity, and
the average annual amount over the remaining period times the 複利年金現価率 at the contract's 予定利率
[R6, 相続税法第24条第1項第1号](#jplib-income_guarantee-r6). On a 無解約返戻金型 design the first limb is zero, so **the published
commutation amount sets the tax value** — the ¥300,000,000 年金現価 cap [S8] and the commutation
factors [S13] are tax-relevant numbers, not just claims-settlement numbers. The 複利年金現価率
itself is prescribed by 財務省令, which was not fetched, so its numeric values are [unverified].
Each subsequent instalment is then **雑所得** in the recipient's hands but only in part: the
first year of payment is wholly exempt and the taxable share rises **in steps (階段状)** keyed
to the 相続税評価割合 — a 相続税評価割合 above 50% and up to 55% gives a 課税割合 of 45% [R4,
所得税法第35条・所令185・186](#jplib-income_guarantee-r4). One carrier discloses the consequence on its product page, warning that
instalments may be withheld at source as 雑所得 so that the amount actually received is less
than illustrated [S12]. Whether the ¥5,000,000 × statutory-heirs death-benefit exemption of
相続税法第12条 [REG-R44] [REG-R45] applies to an annuity right valued under 第24条 was **not
established** in the research pass and is [unverified] here. On the premium side a pure 収入保障
contract falls in the 一般生命保険料 basket of the post-2012 three-basket 生命保険料控除, each basket
giving the full premium to ¥20,000 tapering to a flat ¥40,000 above ¥80,000, the three
capped together at **¥120,000** [R7] [REG-R43]; the 就業不能 and 介護 riders sold on this chassis
are what can reach the 介護医療 basket [R7]. At the anchor cell the annual premium of ¥30,780
sits in the ¥20,000–¥40,000 band, so the deduction is `30,780 ÷ 2 + 10,000 = ¥25,390`.

**Accounting.** Japan has no mandatory IFRS 17; IFRS applies as 指定国際会計基準 on a **voluntary**
basis [REG-R47]. A `jplib` projection therefore feeds three separate measurement bases —
J-GAAP statutory reserving [REG-R10], the ESR economic balance sheet [REG-R15], and IFRS
where an insurer has adopted it — and a document that conflates them will be wrong about
which assumptions are locked in and which are re-set.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-income_guarantee-r1
[R10]: #jplib-income_guarantee-r10
[R11]: #jplib-income_guarantee-r11
[R2]: #jplib-income_guarantee-r2
[R3]: #jplib-income_guarantee-r3
[R5]: #jplib-income_guarantee-r5
[R7]: #jplib-income_guarantee-r7
[R8]: #jplib-income_guarantee-r8
[R9]: #jplib-income_guarantee-r9
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
[REG-R39]: #jplib-reg-r39
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R42]: #jplib-reg-r42
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
