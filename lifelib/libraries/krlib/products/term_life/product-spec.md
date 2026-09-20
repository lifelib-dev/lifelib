# Product Specification

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modelling of a Korean level term assurance, 정기보험 (*jeonggi boheom*,
term life insurance). It does not describe any single insurer's contract, and it is not a
translation of one. Facts carrying a source tag — [S#] (primary product documents: 약관
(*yakgwan*, policy conditions), 상품요약서 (*sangpum yoyakseo*, the statutory product
summary), 상품비교공시 (*sangpum bigyo gongsi*, the cross-carrier comparative disclosure)
and carrier product pages) and [R#] (regulatory, supervisory and statistical references
this product needs and the cross-product library does not carry), both numbered per
`_research/term-life.md` and resolved in `sources.md` in this directory, numbering frozen;
and [REG-R#], the cross-product library
`references/regulatory-and-actuarial-references.md`, whose R-numbering is distinct — were
extracted from the cited document. Values marked **[std]** are standardizations introduced
for the reference implementation; every **[std]** table row carries a numbered footnote
with its rationale and, where the research file could bracket it, the observed range across
insurers. Claims that could not be confirmed against a retrieved document are flagged
[unverified].

**What the composite is drawn from, and why Korea is unusually well documented.** Fifteen
carriers appear in the evidence. The 생명보험협회 (Korea Life Insurance Association)
공시실 publishes a statutory 상품비교공시 in which **45 정기보험 products across 15
carriers** are priced on **one prescribed 대표계약 (*daepyo gyeyak*, representative
contract) basis** [S4] [S5], and links each product's 상품요약서, which must print the
적용이율 (*jeogyong iyul*, the pricing interest rate), the 예정 경험사망률 (*yejeong
gyeongheom samangnyul*, assumed experience mortality) at ages 20/40/60, the 적용해지율
(*jeogyong haejiyul*, the pricing lapse rate) wherever a lapse rate is used in pricing, and
a 해약환급금 (*haeyak hwangeupgeum*, surrender value) illustration by elapsed duration.
Eight 상품요약서 [S1] [S6] [S8] [S9] [S10] [S11] [S12] [S15], two 예상 갱신보험료 예시
[S7] [S16], two more 상품요약서 for the corporate and simplified-issue forms [S17] [S18],
one **190-page 약관 read in full** [S2], three consumer pages [S3] [S13] [S14] and four
whole-life sources used as negative evidence [S19] [S20] [S21] [S22] stand behind this
document. **No other country library in this repository has a like-for-like published
premium comparison for its protection chassis, and none has a published pricing lapse
rate.** What is *not* public in Korea is the thing that is public in Japan: the 산출방법서
(*sanchul bangbeopseo*, the premium and surrender-value calculation document) is a
기초서류 (*gicho seoryu*, filing document) filed with the FSC and never published
[REG-R2], and the industry mortality table, the 경험생명표 (*gyeongheom saengmyeongpyo*,
experience life table), is released only as summary statistics [REG-R33] [REG-R34]. So in
`krlib` the *contractual* parameters are sourced and the *basis* parameters are, with the
three-point exception the 상품요약서 discloses, **[std]**.

**This product is the library's protection chassis.** It specifies, once and in full, the
decrement structure, the premium recursion and the **갱신형 (*gaengsinhyeong*, renewable) /
비갱신형 (*bi-gaengsinhyeong*, non-renewable)** split that runs through the whole Korean
market. The [critical illness product specification (CI보험)](../ci_insurance/product-spec.md)
and the [cancer product specification (암보험)](../cancer/product-spec.md) state only their
deltas against this document and [`technical-notes.md`](technical-notes.md) in this
directory. The savings machinery it deliberately does **not** carry — the 계약자적립액
(*gyeyakja jeongnibaek*, policyholder account balance) as a projected quantity, the
표준형 해약환급금 curve, the 보험계약대출 (*boheom gyeyak daechul*, policy loan) — belongs
to the [whole life product specification (종신보험)](../whole_life/product-spec.md), which
is the savings chassis.

**Out of scope, and said so where it matters.** 단체정기보험 (group term); 신용생명보험 /
대출안심보험 (creditor life, whose decreasing cover shadows a loan and for which no
document was retrieved); 변액정기보험, the separate-account form, whose machinery is in
[`variable_annuity`](../variable_annuity/product-spec.md); the 제3보험 riders — 암진단,
뇌출혈진단, 급성심근경색증진단, 입원·수술 — that ride on a Korean 정기보험 and are
researched under `cancer`, `ci_insurance` and `indemnity_medical`; and the corporate tax
treatment of the 경영인정기보험 (*gyeongyeongin jeonggi boheom*, key-person term), which is
described below for its escalating-benefit and three-step surrender-value mechanics and for
its price level, and for nothing else.

---

## Product overview and market role

정기보험 is **생명보험상품** (first-sector life business), not 제3보험. 보험업법 제2조제1호
가목 defines a 생명보험상품 as a contract undertaking payment 「위험보장을 목적으로 사람의
생존 또는 사망에 관하여」, and 다목 defines the 제3보험상품 as one concerning 「사람의
질병ㆍ상해 또는 이에 따른 간병」; 제4조제1항제1호 licenses 생명보험업 separately from
제3보험업 [REG-R1] [R1] [R2]. The classification matters inside this library because four
of the ten `krlib` products sit on the other side of that line, and because the **재해사망
(accidental death) uplift** several carriers sell as a product variant does **not** cross
it: a fixed sum payable on death from a refined cause is still 생명보험, and the trigger is
narrowed rather than the class changed [S6] [S10] [REG-R1].

Within life business the product is a **보장성보험** (*bojangseong boheom*, protection
insurance) and not a 저축성보험, on the test 감독규정 제1-2조제3호 applies at the
**기준연령 요건** (*gijun yeollyeong yogeon*, reference-age condition) — whether the
maturity value exceeds premiums paid, evaluated for a male aged 만 40 buying on a
whole-term-pay monthly basis [REG-R9]. 소득세법 제59조의4 draws the boundary for tax in the
same place and in almost the same words [REG-R57]. The 순수보장형 (*sunsu bojanghyeong*,
pure protection) form passes the test by construction, having no maturity value at all; the
만기환급형 (*mangi hwangeuphyeong*, return-of-premium) form passes it by design, returning
exactly 100% of premiums paid and no more [S1] [S8] [S12] [S17].

**The market shape.** Of the 45 정기보험 products in the current disclosure, roughly 19 are
retail (기본형, 순수보장형 or 만기환급형), 12 are 경영인정기보험, only **three are 갱신형**,
and only two carriers sell a renewable term at all; nine of the nineteen retail rows are
sold through the CM (online) channel — a far higher direct share than the Korean life market
as a whole [S4]. The retail twenty-year market clears in a narrow band. On the disclosure's
prescribed basis — male, 보험나이 40, 20-year term, 전기납 (*jeongi-nap*, whole-term pay),
월납 (monthly), ₩100,000,000 (1억원) of cover [S5] — seven carriers price a male life
between **₩14,400 and ₩18,400 a month**, a spread of 28% [S4]. Face-to-face products sit
40–90% above that band and simplified-issue products above again, so **the channel, not the
carrier, is the first-order price driver**, a reading the published 보험가격지수 (*boheom
gagyeok jisu*, insurance price index) confirms directly: every CM product in the table sits
between 72% and 101% of the industry-average price, and every 대면 retail product between
104% and 175% [S4] [S6].

**Term life is not where the Korean life market is growing.** 보장성보험 premium income ran
₩48.6조 (2023) → ₩55.0조 (2024) → about ₩61.5조 (2025E) → about ₩66.2조 (2026E), against a
저축성 book in slow decline [REG-R46]; but 보험연구원's reading of where that growth sits is
「무·저해지환급형 질병보험과 상해보험」 — third-sector sickness and injury cover, not death
cover [R16] [REG-R46]. Death protection is the chassis on which the growth products are
built rather than the growth product itself, which is exactly why it is specified first and
in full here.

**Three things make the Korean contract worth a document of its own rather than a
translation of `jplib`'s 定期保険.**

1. **There is no Korean analogue of the 高度障害保険金.** A Japanese term policy pays the
   full sum assured on a closed eight-item schedule of permanent total disability, inside
   the main contract and at no separate premium, so its claims model carries two competing
   benefits on one sum assured. A Korean term policy does not. What the 장해 (*janghae*,
   disability) state does instead is **switch the premium off** — the 보험료 납입면제
   (*boheomnyo nabip-myeonje*, waiver of premium) on a 장해지급률 (*janghae jigeumnyul*,
   disability payment percentage) of 50% or more from any cause [S1] [S2] [S6] [S8] [S9]
   [S10] [S11] [S12]. The benefit definition is therefore two lines long, the exclusion set
   is fixed by statute and identical everywhere, and **all the product variation lives in
   the premium, in the surrender-value form and in the renewal structure**.
2. **무해지환급형 (*mu-haeji hwangeuphyeong*, the no-surrender-value form) is the
   representative design, and it is a regulatory dispensation rather than a contractual
   gimmick.** 감독규정 제7-66조제4항 permits a 순수보장성보험 whose premiums were calculated
   using a 최적해지율 (best-estimate lapse rate) to pay **less than** the surrender value
   the 별표 14 floor would otherwise require [REG-R19] [REG-R20]. Nearly two-thirds of
   Korean protection business by first-year premium is now written in that form — the
   무·저해지 share of 보장성 초회보험료 went 11.4% (2018) → 30.4% (2021) → 47.0% (2023) →
   **63.8% (2024 H1)** [REG-R27]. **A Korean reference library that modelled only 표준형
   products would be modelling a minority of the market.**
3. **갱신형 is a genuine contract-boundary question and not a wording detail.** A Korean
   renewal happens **without fresh 고지 (disclosure) and without underwriting**, on the rate
   scale then in force, at attained 보험나이, on a **new product code**, and a premium
   waiver already running does **not** carry into the renewed contract [S6] [S9] [S15].
   Every one of those facts pulls in a different direction on the IFRS 17 boundary, and no
   Korean supervisory document retrieved settles it. This specification publishes both
   readings and makes the horizon a model parameter rather than picking one silently.

---

## Representative specification

The representative product is a composite: a 무배당 (*mubaedang*, non-participating),
개인 (individual), 순수보장형, **해약환급금 미지급형** level term contract on one life,
written 비갱신형 on a 전기납 basis, with 갱신형 as a first-class variant the model must be
able to represent. The anchor cell is the one cell that is doubly prescribed in Korea — it
is both the 감독규정's **기준연령 요건** [REG-R9] and the disclosure's **대표계약** basis
[S5] — so its premium is quoted on one prescribed basis right across the disclosure and
the model point built on it can be checked against the market rather than asserted. The
comparison is genuinely like-for-like only for the carriers that actually write a 20-year
term: the 경영인 rows are 90세만기 전기납 contracts and two retail rows are 80세만기 ones,
so those rows cannot be on the prescribed basis however the disclosure presents them [S4]
[S18].

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 정기보험, 개인, 무배당, 순수보장형, 해약환급금 미지급형(무해지환급형); 주계약 pays a death benefit and nothing else | [S1] [S2] [S12]; participation [S4]; form pick **[std]** (1) |
| Renewal structure | **비갱신형** base; **갱신형** a modelled variant on a 10-year cycle to a ceiling of 보험나이 80 | [S4] [S6]; pick **[std]** (2) |
| Regulatory class | 생명보험상품 (보험업법 제2조제1호 가목, 제4조제1항제1호); **보장성보험** at the 기준연령 요건 (감독규정 제1-2조제3호) | [REG-R1] [REG-R9] [R1] [R2] |
| Lives basis | Single life. No joint-life or first-death form appears in any retrieved Korean document | [S1] [S6] [S8] [S10] [S11] [S12] |
| Benefit shape | Level 보험가입금액 (*boheom gaip geumaek*, sum assured). 체증형 (escalating) is corporate-only; 체감형 (decreasing) is a disclosure category with no retail product in it | [S4] [S18]; scope **[std]** (3) |
| Age basis | **보험나이** (*boheom nai*, insurance age): 만나이 with fractions of six months or more rounded up, incrementing on the **policy anniversary** and not on the birthday | [S2 제22조] [REG-R25 제21조](#krlib-reg-r25) |
| 가입나이 (issue age) | 만19세 to 보험나이 65세 | [S1] [S6] [S9] [S11] [S12]; envelope **[std]** (4) |
| 보험기간 (policy term) | Base **20년만기**; menu 10/20/30년만기 and 60/65/70/80/90세만기 | [S1] [S8] [S10] [S12]; menu **[std]** (5) |
| 납입기간 (premium-paying period) | Base **전기납** (equal to the term); 10년납 and 20년납 shortened-pay variants | [S1] [S8] [S11] [S12]; base **[std]** (5) |
| 보험가입금액 | ₩30,000,000 – ₩500,000,000 (3천만원–5억원), in ₩10,000,000 (1,000만원) units | [S6] [S9] [S11] [S12] [S14]; envelope **[std]** (6) |
| Rate classes | One (**표준체**) in the base run; 비흡연자 / 건강체 / 슈퍼건강체 parameterized from published mortality relativities | [S11] [S12]; pick **[std]** (7) |
| Rate class permanence | **Not fixed at issue.** A class rider tracks smoking status for the life of the contract and moves in both directions | [S2 건강체서비스특약Ⅱ 제4조] [S11] [S12] |
| 건강진단 (non-medical limits) | 일반진단 required above ₩120,000,000 at 20–39, ₩70,000,000 at 40–49, ₩30,000,000 at 50–54, ₩10,000,000 at 55+ | [S6]; adoption **[std]** (8) |
| 위험등급 (occupational class) | 위험1급 capped at ₩100,000,000; all other classes at ₩200,000,000. Carried, not modelled | [S6]; adoption **[std]** (8) |
| 계약자 / 피보험자 / 수익자 | Three roles, routinely three people. Written consent of the 피보험자 is required where they are not the 계약자 | [REG-R50 제731조](#krlib-reg-r50) [S2 제20조] |
| Minimum age of the life assured | A contract on the death of a person **under 만 15**, or of a 심신상실자 or 심신박약자, is **void**; this one test uses 만나이 and not 보험나이 | [REG-R50 제732조](#krlib-reg-r50) [S2 제20조·제22조] |
| **Anchor model cell (model point 1)** | Male, 보험나이 40, 20년만기 전기납, ₩100,000,000 (1억원), 표준체, 순수보장형 해약환급금 미지급형, 월납 **₩15,080** | premium [S12] [S4]; cell = 기준연령 요건 [REG-R9] and 대표계약 [S5]; **[std]** (9) |
| Anchor, female twin (model point 2) | Same cell, female: 월납 **₩8,010** | [S12] [S4] |
| Anchor, 갱신형 (model point 3) | Male, 보험나이 40, **10년만기 갱신형 전기납**, ₩100,000,000, 표준체, 월납 **₩9,000** at issue, ceiling 보험나이 80 | [S6] [S7] [S4]; **[std]** (2) |

Footnotes to **[std]** rows:

1. **Form.** Every one of the 45 disclosed products is 무배당, and the 약관 says so in a
   sentence — 「이 계약은 무배당보험이므로 계약자 배당금이 없습니다」 [S2 제35조] [S4]. There
   is no variation to standardize; the **[std]** is the choice of the **해약환급금
   미지급형** over the 표준형, and it is made because the 표준형 **cannot be bought**. The
   약관 says so in terms: 「'표준형'은 보험료 및 해약환급금(환급률 포함)의 비교 안내만을
   위한 상품으로 가입이 불가능하며」 [S2 제33조]. A composite that adopted the 표준형 would
   be specifying a comparator rather than a product. The 만기환급형 is a real alternative and
   is carried as a variant (Variations, item 3).
2. **Renewal.** 비갱신형 is the base because it is the market: only three of 45 disclosed
   products renew, and only 흥국생명 and 푸본현대생명 sell a renewable term at all [S4].
   갱신형 is nonetheless a first-class variant rather than a footnote, because the mechanic
   runs through every other Korean protection product this library models and because the
   only carrier selling both forms of one product supplies a clean comparison (mechanics,
   below). The 10-year cycle and the 보험나이 80 ceiling are 흥국생명's [S6]; observed cycles
   run **1년** [S15], **10년** [S6] and **15년** on a rider [S9], and observed ceilings
   **80세** [S6], **five years' total cover** [S15] and **the main contract's expiry** [S9].
3. **Benefit shape.** The 체증형 formula is published — 「체증보험금 = 보험가입금액 ×
   체증률 × (계약경과년수 − 9)」 at a 체증률 of 10%, so the sum assured is level for ten
   years and then rises by 10% of the original each year — but every 체증형 product
   retrieved is a 90세만기 전기납 corporate contract sold at ₩50,000,000 to ₩3,000,000,000
   [S18] [S4]. 체감형 is a category the disclosure recognises [S4] [S5] and in which no
   retail product appeared. Composite: level only.
4. **Issue age.** Observed minima 만15세 [S10] [S17], 만19세 [S1] [S6] [S11] [S12] and 20세
   [S8] [S9] [S15], with particular cells starting later; observed maxima 60세 [S6] [S10]
   [S15], 64세 [S8], 65세 [S1] [S9] and 70세 [S11] [S12] [S17] [S18]. Nothing in the set
   issues above 70. Composite: 만19세, the modal retail minimum, to 65세, the median maximum
   and the exact ceiling of two carriers [S1] [S9]. **The mixed age basis in that row is not
   an error**: a minimum written 만19세 is 만나이 and a maximum written 65세 is 보험나이, and
   the documents are consistent about which is which [S2 제22조]. Note also that the real
   constraint is a **최고가입나이 matrix**, not a scalar: 한화생명 publishes maximum issue
   ages of 49/54/55/60/65/65 at 60/65/70/80/90/100세만기 on a 10년납 male 순수보장형 basis,
   39/44/49/59/65/65 on 20년납, and 60 at 10년만기 with 50/55/55/60/65/**56** at the 세만기
   options on 전기납 [S1]. The composite carries the scalar envelope and the anchor sits well
   inside it.
5. **Term and payment period.** Observed term menus run from a single option (90세만기 only
   [S18]; 1년만기 only [S15]) to eleven (three 년만기 and eight 세만기 [S12]). Every carrier
   offering a menu offers both 년만기 and 세만기, and the 세만기 ceiling has crept from 80세
   to 90세 [S9] [S12] [S17] [S18] and 100세 [S1]. 전기납 is available everywhere and is the
   disclosure's basis [S5]; shortened pay is available almost everywhere, the widest menu
   reaching 5년납 and a 일시납 at 80세만기 [S10] [S11]. Composite: the 20-year whole-term-pay
   contract, because it is the cell the regulation and the disclosure both prescribe, with
   the shortened-pay variants carried because **they are the only way the 무해지 form's
   post-완납 step-up can arise at all** (mechanics, below).
6. **Sum assured.** Observed retail ceilings ₩10,000,000 [S15], ₩100,000,000 [S17 간편],
   ₩200,000,000 [S6] [S17], ₩300,000,000 [S8] [S10], ₩500,000,000 [S1] [S9] [S11] [S14] and
   ₩1,000,000,000 [S12]; observed floors ₩1,000,000 [S15] through ₩100,000,000 [S12], modal
   ₩30,000,000. Composite: the modal floor and the modal ceiling, in the ₩10,000,000 unit the
   two carriers that publish one both use [S6] [S12]. The corporate ceiling is
   ₩3,000,000,000 (30억원) [S18] and is out of scope. One carrier's floor **rises with the
   rate class** — ₩30,000,000 표준체, ₩50,000,000 비흡연체, ₩70,000,000 건강체, ₩100,000,000
   슈퍼건강체 — which is a real anti-selection control rather than a marketing band, the
   underwriting cost of a preferred class being worth incurring only above a size [S11].
7. **Rate classes.** Observed counts 1 [S15] [S17] [S18], 2 [S1] [S6] [S8] [S9], 3 [S4] and
   4 [S11] [S12] [S14]. Composite: one class in the base run, because a class structure
   multiplies the premium basis without changing a single contractual mechanic. It is
   nonetheless parameterized rather than dropped, because **Korea publishes the mortality
   behind it** — two carriers print a full 예정 경험사망률 table per class (Premiums, below)
   — which no other library in this repository can do.
8. **Underwriting limits.** Only 흥국생명 publishes a 건강진단 grid and only 흥국생명
   publishes an occupational cap [S6]; every other carrier says only that a 건강진단 may be
   required 「기존 다른 보험상품의 가입유무, 나이, 청약서의 계약 전 알릴 의무 사항 등에
   따라」 [S1] [S8] [S10] [S11] [S12] [S17]. Composite: adopt the one published grid.
   Underwriting decline is not modelled; the limits are carried so that a model point above
   them is visibly outside the represented product.
9. **The anchor.** ₩15,080 a month is not a standardization — it is a published figure that
   appears **twice independently**, in 교보라이프플래닛's own 상품요약서 premium grid and as
   that product's row in the cross-carrier disclosure, and the two agree to the won [S12]
   [S4]. What is standardized is the choice of carrier. It is taken because [S12] is the
   only retrieved document that prints the **무해지 form and its 표준형 comparator side by
   side, premium and surrender value, in one table**, so the anchor cell carries its own
   counterfactual; because [S12] publishes four rate classes and four mortality tables at the
   same cell; and because the cell is simultaneously the regulation's 기준연령 요건 [REG-R9]
   and the disclosure's 대표계약 [S5]. Observed premiums for the same risk at other carriers
   are ₩14,400 / ₩15,000 / ₩16,000 / ₩16,000 / ₩16,100 / ₩18,400 [S4].

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium form | Level within the 보험기간, payable monthly in advance over the 납입기간 | [S1] [S2] [S8] [S12] |
| 갱신형 premium form | Level **within each cycle**; recomputed at each renewal on attained 보험나이 and the whole 기초율 then in force — 적용이율, 계약체결비용, 계약관리비용 and 위험률 | [S9] [S15] |
| 납입주기 (frequency) | **월납** only in the base | [S1] [S6] [S8] [S9] [S12] [S17] [S18]; pick **[std]** (10) |
| Annualization for the model | `P_a = 12 × P_m` = **₩180,960** at the anchor | **[std]** (10) |
| Rate structure | Per-mille of 보험가입금액. **No separable flat policy fee can be identified**: no Korean grid retrieved varies the sum assured | [S1] [S8] [S11] [S12] [S14]; gap (11) |
| Rating factors | 성별, 보험나이, 보험기간, 납입기간, 보험가입금액, rate class, 해약환급금 유형, 갱신 여부, 위험등급 | [S1] [S6] [S8] [S10] [S11] [S12] |
| 적용이율 (pricing interest rate) | **2.50% 연복리** | [S1] [S8] [S11] [S12]; pick **[std]** (12) |
| 예정 경험사망률, male | q20 **0.000280**, q40 **0.000650**, q60 **0.003390** | [S12]; table build **[std]** (13) |
| 예정 경험사망률, female | q20 **0.000200**, q40 **0.000430**, q60 **0.001390** | [S12]; table build **[std]** (13) |
| Rate-class mortality relativities (male 40 / female 40) | 표준체 1.000 / 1.000; 비흡연자 0.828 / 0.956; 건강체 0.723 / 0.907; 슈퍼건강체 0.583 / 0.856 | computed from [S12] |
| 예정 재해사망률 (재해보장 variant), male | q20 0.000097, q40 0.000110, q60 0.000355 | [S6]; and [S10] within 10% |
| 적용해지율 (pricing lapse) | Log-linear decay from **4.6% at duration 1 to 0.1% at 납입완료**; **0.8%** thereafter where a post-완납 period exists | shape [REG-R27]; endpoints [S12] [S1]; extension **[std]** (14) |
| Best-estimate lapse | Not disclosed by any carrier for a 표준형 term; **[std]** in `technical-notes.md` | gap (14) |
| 계약체결비용 / 계약관리비용 | Defined in every 상품요약서, **rate published by none**; **[std]**, bounded by 별표 14 and by the 보험가격지수 | [S1] [S6] [S8] [S10] [S11] [S12]; gap (15) |
| 보험가격지수 at the anchor | **88.1 (male) / 85.5 (female)** — the product's total premium as a percentage of 참조순보험료 총액 plus 평균사업비 총액 | [S4] [S1] |
| 단체취급 discount | Available at 1.5%–5% of the 영업보험료 for a group of five or more; **not applied** in the base | [S1] [S10]; scope **[std]** (16) |
| 고액할인 (large-case discount) | Offered at one carrier above ₩100,000,000, **rate unpublished**; not applied | [S9]; scope **[std]** (16) |
| Behavioural discount | 걷기할인형: −10% of the 영업보험료 **for the first twelve premiums only**, on 8,000 steps a day on 20 days in the qualifying month; not applied | [S8]; scope **[std]** (16) |
| 선납 (advance payment) | Permitted at an insurer-set discount; not modelled | [S12]; scope **[std]** (16) |
| 만기환급형 premium at the anchor | **₩142,000** male / ₩87,340 female — **9.42×** and **10.90×** the 순수보장형 | [S12] [S4] |
| 표준형 comparator premium at the anchor | **₩15,320** male / ₩8,120 female — the 무해지 form saves **1.57%** and **1.35%** | [S12] |
| 갱신형 premium path (male 40, ₩100m, 10-year cycles) | ₩9,000 → ₩21,000 (50) → ₩56,000 (60) → ₩201,000 (70); index 1.00 / 2.33 / 6.22 / 22.33 | [S7] |

10. **Frequency.** Monthly is available at every carrier retrieved and is the only frequency
    on seven of the retrieved products, from five carriers [S1] [S6] [S8] [S9] [S12] [S17]
    [S18]; one adds 연납 [S15], one adds 3개월납·6개월납·연납 [S11], one adds 연납 and
    일시납 [S14] [S10]. It is also the disclosure basis [S5] and half of the 기준연령 요건
    [REG-R9]. `Term_KR_S` runs on a **monthly grid**, which is the frequency the contract
    is actually paid on, so the published monthly office premium is the projection's own
    cash flow and no annualization convention stands between the rate card and the
    statement. `P_a = 12 × P_m` survives as a reporting figure and as the base of the
    commission scale. An earlier annual-grid version of this model collected the twelve
    premiums at the start of the year, which was conservative in the insurer's favour by
    **half a year's interest on the whole premium** — 1.136% of a year's premium at the
    적용이율, the mean deferral of the twelve payments being 5.5/12 of a year; the technical
    notes record what removing that convention moved.
11. **The policy fee gap.** Unlike `jplib`'s オリックス生命 grid, from which a flat ¥248
    monthly policy element could be extracted exactly because the card varies the sum
    assured, **every Korean grid retrieved fixes the sum assured and varies age, sex, rate
    class or product form instead**. The per-mille rate and any per-policy fee therefore
    cannot be separated, and the composite prices proportionally to the sum assured and says
    so. One consequence is visible in the data and is worth recording: female premiums run
    at 52–56% of male across the six direct writers on the same cell, and anywhere from 47%
    to 90% across the eleven face-to-face and simplified-issue rows [S4]. A flat per-policy
    loading pushes that ratio up as the loading grows, and the face-to-face band does reach
    higher — but it also reaches lower than the direct writers' band, so the spread is
    consistent with a per-policy fee without establishing one.
12. **적용이율.** Observed 1.75% [S4] to **4.00%** [S4], with a retail mode of **2.50%** at
    five carriers [S1] [S8] [S9] [S11] [S12]. Two patterns hold across carriers and are
    carried into the variants rather than averaged away: the **만기환급형 is priced at a
    lower rate than the 순수보장형 of the same product** (2.25% against 2.50% at two
    carriers [S8] [S12]) — the rates are sourced, the usual explanation that the savings
    element carries a longer duration and a tighter guarantee is an inference and nothing
    retrieved states it; and a **갱신형 is priced at a different rate again** (3.00% renewable
    against 2.75% non-renewable at one carrier [S4] [S6]; 2.00% for a 갱신형특약 against
    2.50% for the 주보험 at another [S9]). The composite's 2.50% also happens to equal the
    **2026 평균공시이율** [S12], which is the rate the 약관 uses for instalment settlement
    and for the 선지급 discount — a coincidence of level, not an identity of concept.
    There is no 공시이율 and no 최저보증이율 on a Korean protection product; the disclosure's
    guarantee columns are empty for every 정기보험 row [S4].
13. **Mortality.** The rates above are one carrier's **예정 경험사망률**, disclosed at three
    ages as the 상품요약서 requires [S12]. Seven carriers' three-point disclosures were
    collected and they do **not** agree: at male 40 the observed spread is 0.000480 to
    0.000850, a factor of **1.77**; at female 40, 0.000310 to 0.000540, a factor of 1.74; at
    male 60, 0.002710 to 0.004165, a factor of 1.54 [S1] [S6] [S8] [S10] [S11] [S12] [S17].
    They differ because each is a **carrier-specific adjustment of the 보험개발원
    참조순보험요율** [R19] [REG-R4], not a common table — the exact opposite of Japan, where
    every carrier prices off one publicly downloadable 標準生命表. The industry table, the
    제10회 경험생명표 applied from April 2024, is **not published**: only 평균수명 (male
    86.3, female 90.7) and 65세 기대여명 (male 23.7, female 27.1) are released [REG-R33]
    [REG-R34] — and even those four numbers reach this library through a **trade
    newspaper**, 보험개발원's own announcement not being retrievable. **Therefore
    `mort_table.csv` in this product is a [std] construction**,
    anchored on [S12]'s three published points, graduated against the public 국가데이터처
    완전생명표 [REG-R38] [REG-R39], with a `provenance` column on every row. A usable sanity
    check falls out of the two public sources: the 경험생명표's 65세 기대여명 of 23.7 years
    (male) and 27.1 (female) [REG-R33] runs **4.2 and 3.4 years above** the public national
    table's 19.5 and 23.7 at the same age [REG-R38]. That gap is underwriting selection, and
    a constructed table that does not reproduce it is not an insured-lives table.
14. **Lapse.** The **shape** is supervisory, not chosen: the 2024 IFRS17 계리가정
    가이드라인 makes a **로그-선형 (log-linear) 모형 converging to 0.1%** the 원칙모형 for
    무·저해지 business, permits only 선형-로그 (to 0%) and 로그-로그 (to 0.1%) as exceptions
    and only on onerous disclosure conditions, and sets a **post-완납 ultimate rate of 0.8%**
    [REG-R27]. The **endpoints** are disclosed: 「납입기간 이내에 대하여 경과기간별로 연
    0.1%~4.6%, 납입기간 이후에 대하여 경과기간별로 연 0.7%~1.6%」 at the anchor carrier
    [S12], and 「연 0.1%~8.4%, 납입기간 이후 연 0.8%」 at another [S1]. **The chain from
    supervisory guideline to disclosed pricing parameter runs end to end**, which is unique
    in this repository — with one qualification that must travel with it: the guideline's
    *values* are verified from the 보도자료 while its 별첨 was never converted from HWP, so
    the functional **form** is **[unverified]** at instrument level [REG-R27]. Two **[std]**
    steps remain. Both disclosed ranges are on a
    **10년납** basis and the composite is 전기납 over twenty years, so the same endpoints are
    stretched over the representative's own payment period. And the 적용해지율 is a
    **pricing** rate for the 무해지 form — deliberately low, by regulatory design — and is
    **not** a best-estimate. Nothing in the retrieved set discloses a best-estimate term
    lapse rate, and the only Korean experience datum available is a whole-life one: 5·7년납
    저해지 단기납 종신보험 ran a **37회차 유지율 of 50.2% against an assumed 71.5%** [R18].
    The direction of that error, not its size, is the reason the technical notes carry the
    best-estimate lapse basis as an explicit **[std]** with a sensitivity attached.
15. **Expenses.** Every 상품요약서 defines 계약체결비용 and 계약관리비용 in the same words —
    「보험회사가 보험계약의 체결, 유지 및 관리 등에 필요한 경비로 사용하기 위하여 보험료 중
    일정비율을 책정한 것」 — and **not one publishes a rate** [S1] [S6] [S8] [S10] [S11]
    [S12]. Two public handles bound a **[std]** expense basis. The first is the 별표 14
    표준해약공제액, which caps the recoverable acquisition cost by formula [REG-R20]; at the
    anchor cell the sum-assured component alone is ₩100,000,000 × 10/1000 = **₩1,000,000**,
    which is **5.5 years' gross premium**, so on this product the statutory cap is very far
    from binding (mechanics, below). The second is the 보험가격지수: an index of 88.1 means
    the product's total premium is 88.1% of the industry-average net premium plus the
    industry-average expense loading [S1] [S4], and the *dispersion* of that index across the
    45 products — 51.6% to 239.1% — bounds what an expense assumption may plausibly be.
16. **Discounts.** All four are real, all four are documented, none is applied in the base
    run. The 단체취급 discount requires an affinity group of five or more and is worth 1.5%
    of the 영업보험료 at one carrier and 5% from the second premium at another [S1] [S10],
    so it is a distribution feature rather than a product feature. The 고액할인 threshold is
    published (₩100,000,000) and its rate is not [S9], so applying it would mean inventing
    the number that matters. The 걷기할인형 is a twelve-month acquisition discount dressed
    as a wellness feature and is the only behaviour-linked pricing in the retrieved set [S8].
    선납 is permitted at an insurer-set and unpublished discount [S12].

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| 사망보험금 (death benefit) | **보험가입금액**, on death within the 보험기간. Payment terminates the contract immediately and automatically | [S1] [S2 제4조·제23조] [S8] [S10] [S11] [S12] [S17] |
| What counts as death | Includes a court 실종선고 (deemed to occur when the 실종기간 ends) and a 관공서 disaster notification (the date entered in the 가족관계등록부) | [S2 제5조제2항] |
| Withdrawal of life-sustaining treatment | Expressly does **not** affect the cause of death or the payment | [S2 제5조제3항] |
| 만기보험금 (maturity benefit) | **None** on the representative 순수보장형 | [S1] [S8] [S12] |
| — on the 만기환급형 variant | 100% of 「이미 납입한 주계약 보험료」, computed **as if any waived premiums had been paid** | [S1] [S8] [S12] [S17] |
| Disability benefit | **None.** There is no Korean analogue of the Japanese 高度障害保険金; the 50% 장해 state waives premiums instead | [S2 제5조]; contrast `jplib` term |
| 재해사망 uplift | **Not in the base.** Where a carrier offers it, it is a product 형 paying **2×** the sum assured on 재해사망 and 1× otherwise | [S6] [S10]; scope **[std]** (17) |
| Suicide exclusion | No death benefit where the 피보험자 intentionally takes their own life within **2 years** of the 보장개시일 (or of the 부활 application date). **The window does not restart on renewal** | [S1] [S2 제6조] [S3] [S6] [S8] [S10] [S11] [S13] [S17] |
| — exception with no time bar | Payment is made where the act occurred in a state of 심신상실 in which free decision was impossible | [S2 제6조] |
| Other 면책사유 | Intentional killing by the 보험수익자 (other beneficiaries' shares still paid) or by the 계약자. **Three limbs in total, in every 약관 retrieved** | [S1] [S2 제6조] [S6] [S8] [S10] [S11] [S17] |
| Gross negligence | **Not an exclusion**, by statute: 상법 제732조의2 preserves the death benefit where the event arose from gross negligence | [REG-R50] [R4] |
| War, aviation, hazardous pursuits | **Absent from every 약관 and every 상품요약서 retrieved.** Occupational risk is handled at underwriting through the 위험등급 and 직업별 가입한도 | [S2 제24조제4항] [S3] [S6] |
| Pre-existing conditions | No restriction on the death benefit and no 감액기간 on the 일반가입형 | [S1] [S2] [S8] [S11] [S12] |
| — on the 간편고지형 variant | **50% of the 보험가입금액** for a non-accidental death within **2 years** of the contract date | [S17] [S18] |
| 재해 (accident) definition | 별표3 재해분류표: 「한국표준질병·사인분류상의 (S00~Y84)에 해당하는 우발적인 외래의 사고」 plus a 제1급감염병, with a closed carve-out list that includes 고의적 자해 (X60~X84) and 법적 처형 (Y35.5) | [S2 별표3·제3조] |
| Classification in force | 제9차 개정 한국표준질병·사인분류 (통계청 고시 제2025-299호, 시행 2026-01-01), judged at diagnosis or occurrence and never re-judged | [S2 제3조] |
| Default beneficiary | 사망보험금 to the 피보험자의 법정상속인; 만기보험금 to the 계약자 | [S2 제12조] |
| Claim timetable | **3영업일** from complete documents; **10영업일** where investigation is needed; a payment date within **30영업일** except in six named cases; a 가지급보험금 of up to **50%** of the estimate on request where the deadline will be missed | [S2 제9조]; scope **[std]** (18) |
| Instalment settlement | The benefit may be taken in instalments, deferred amounts accruing at the **평균공시이율** on an annual-compound basis and accelerated amounts discounted at it | [S2 제10조] |

17. **재해사망.** Two of nine carriers sell the uplift, and both sell it as a **product
    variant rather than a rider**: 신한SOL's 재해보장형 and 흥국생명's 2형(보장추가형), each
    paying twice the sum assured on 재해사망 and once otherwise [S6] [S10]. It is cheap
    relative to the base cover, though not as cheap as one might assume: on 흥국생명's own
    published pair of 예정 경험사망률 and 예정 재해사망률, accidental death is about **31% of
    all-cause mortality at male 20 and about 9% at male 60** [S6]. Against the table this
    library actually ships — all-cause from [S12] and accidental from [S6], a cross-carrier
    pairing and so a [std] combination rather than either carrier's own ratio — the shares
    are 34.6% and 10.5% at the same two ages. Either way the share falls steeply with age,
    because accidental mortality is close to flat while all-cause is not, which is why the
    uplift is bundled into the base price rather than priced separately: at the ages that
    dominate the in-force it costs little. The composite excludes it so that the chassis
    carries **one decrement to the benefit**, and parameterizes it as a second mortality
    vector for the model points that switch it on. One structural asymmetry is worth
    recording: 흥국생명 **does not sell its 기본형 to women at all**, so a female life at that
    carrier must buy the 보장추가형, and the disclosure prints ₩0 in the 기본형 female column
    — a structural gap, not a price [S4] [S6].
18. **Claim lag.** The timetable is contractual and real, but no Korean document publishes
    the mix of claims falling into the three bands, so any split would be invented. The
    composite pays at the projection step in which the claim arises and says so; a claim-lag
    module belongs in the technical notes' sensitivities and not in the base run. The
    surrender value is likewise payable within 3영업일 of claim [S2 제33조] [REG-R25 제32조](#krlib-reg-r25).

### Options

| Parameter | Representative value | Basis |
|---|---|---|
| 보험료 납입면제 (waiver of premium) | **In the 주계약**, at no separate premium: future premiums are waived where the 피보험자 reaches a 장해지급률 of **50% or more**, from 「동일한 재해 또는 재해이외의 동일한 원인」 | [S1] [S2 제5조제1항] [S6] [S8] [S9] [S10] [S11] [S12] |
| — cause | **Cause-neutral.** Sickness qualifies equally with accident | [S2]; narrowed to accident only on 간편고지형 riders [S17] [S18] |
| — determination | The 장해지급률 is fixed at **180 days** from the accident or the confirmed diagnosis if not settled sooner, with a look-back of **2년** where the term is ten years or more and **1년** where it is shorter | [S2 제5조제4항·제5항] |
| — combination | Additive across body parts from one cause; two impairments in the **same** part take the higher rate, not the sum. A temporary disability lasting five years or more counts at **20%** of its rate | [S2 제5조제8항·제9항] |
| — effect | 「차회 이후의 보험료 납입을 면제」 — future premiums only, no refund of past ones. The contract stays in force | [S2 제5조제1항] |
| — interactions | Switched off by the same three intent limbs as the death benefit; **kills the 무해지 step-up**; **does not survive a renewal** | [S2 제6조·제33조] [S6] [S12] |
| 선지급서비스특약 (accelerated death benefit) | Attached as a 제도성특약 at no disclosed premium. Trigger: a specialist at a 종합병원 judges the remaining life expectancy to be **12 months or less** | [S2] [S10] [S12] [S17] [S18]; attachment **[std]** (19) |
| — amount and cap | Up to **50% of the 사망보험금**, aggregated across the insurer's contracts to a maximum of **₩50,000,000 (5,000만원)**; up to ₩10,000,000 (1,000만원) may be **100%** of the sum assured | [S2 제4조] |
| — computation | The accelerated amount, discounted over the remaining life expectancy at the **평균공시이율**, less the similarly discounted premiums on it and less any outstanding 보험계약대출 | [S2 제4조제6항] |
| — effect | The 보험가입금액 is treated as reduced by the amount paid, from the payment date; **no surrender value arises on the reduction**. One payment per contract; paid to the **피보험자** | [S2 제4조] |
| 갱신 (renewal, 갱신형 variant) | Automatic and **negative-option**: the contract renews unless the policyholder objects **15 days** before expiry. No 고지, no underwriting, no health condition | [S6] [S9] [S15]; notice **[std]** (20) |
| 감액 (reduction of sum assured) | Permitted; the premium is reset. On the representative form **no payment arises**, there being no surrender value to release | [S2] [S12] |
| 증액 (increase) | Not available; a new contract with fresh underwriting is required | [S1] [S12]; [unverified] as a market-wide rule |
| 지정대리청구서비스특약 | Standard where 계약자, 피보험자 and 보험수익자 are the same person: a pre-nominated agent may claim | [S1] [S2] [S10] [S11] [S12] [S17] |
| 장애인전용보험전환특약 | Converts the contract into a 장애인전용보장성보험 so that the **15%** tax credit applies instead of 12% | [S1] [S10] [S11] [S12] [S17] [REG-R57] |
| 출산육아휴직 보험료 납입유예특약 | A premium holiday of **6 or 12 months, once per contract**, where the policyholder or their spouse is within a year of childbirth or on parental leave | [S1] [S12] [S17] [S18] |
| 종신전환특약 / 연금전환특약 | Present at one carrier only; conversion to whole life is capped at the pre-conversion death benefit and is on the terms and rates then in force | [S17] [S18]; scope **[std]** (21) |
| Indexation, GIO, joint life, 감액완납, 연장정기 | **Absent from every retrieved document** | [S1] [S2] [S6] [S8] [S10] [S11] [S12] |

19. **Acceleration.** The rider appears at every carrier whose full document set was
    retrieved and carries no separate premium in any of them, which is why the composite
    attaches it and treats it as part of the modelled contract rather than an add-on. That
    it is genuinely free is **[unverified]** — no document states a nil 특약보험료 — but the
    discount in the payment formula supplies the economic reason it can be. The trigger is
    **12 months** at every carrier except one, which narrows it **specifically for 정기보험**
    to 「6개월 이내」 [S17]; the comparison with Japan is instructive, where リビング・ニーズ
    特約 triggers at six months, caps at ¥30,000,000 of the whole benefit, and is barred
    within a year of expiry. Korea's trigger is looser, its cap is tighter — half the sum
    assured to ₩50,000,000 — and **there is no bar near expiry at all**.
20. **Renewal notice.** Observed **15일** at the two carriers that publish one [S9] [S15];
    흥국생명 does not publish a notice period [S6]. Composite: 15 days. The direction matters
    for a projection: the shorter the notice and the more negative the option, the more
    renewals happen by inertia, and Korea's is the shortest and most negative arrangement in
    this repository — no carrier retrieved requires a positive election.
21. **Conversion.** 미래에셋생명 alone offers both a **종신전환특약** — 「보험계약자는
    보험기간이 종료되기 전 이 보험계약을 '종신전환특약 무배당'을 통해 종신보험으로 변경할
    수 있습니다. 이 경우 전환 후 보험계약의 보험가입금액은 전환 전 보험계약의 사망보험금을
    한도로 합니다」 — and a **연금전환특약** with 종신연금형, 확정연금형 and 상속연금형
    options credited at a 공시이율 with a floor of 1.0% before the tenth policy year and 0.5%
    after [S17] [S18]. It is the Korean conversion option and `jplib` has nothing like it.
    Two of nine carriers is too thin a base for a composite, so it is specified and excluded.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 해약환급금 (surrender value) | **Nil at every duration.** On a 전기납 무해지 contract the premium-paying period never ends before the term does, and the 약관 pays nothing during it | [S1] [S2 제33조제2항] [S12] |
| — on a shortened-pay 무해지 contract | Nil during the 납입기간; **50% of the 표준형's** surrender value thereafter | [S1] [S2 제33조제2항] [S12] |
| — where premiums have been waived | **Nil**, even after the nominal 납입기간 would have ended: the step-up is forfeited | [S2 제33조제2항 단서] [S12] |
| — 표준형 comparator | A **phantom**: it cannot be bought, is disclosed only for comparison, and is computed 「해지율을 적용하지 않고」 as 순보험료식 계약자적립액 less the 해약공제액 | [S1] [S2 제33조] [S12] [S18] |
| 해약공제액 (surrender charge) | Capped by the **표준해약공제액** = 연납순보험료의 5% × 해약공제계수 + 보험가입금액의 10/1000, with 해약공제계수 = 보험기간 capped at 20 years and the 연납순보험료 recomputed on a whole-term-pay (20-year-pay if longer) basis | [REG-R20] [R9] |
| 해약공제기간 (amortisation period) | The 납입기간 or the 신계약비 부가기간, **capped at seven years** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| Floor | 계약자적립액 less 해약공제액, **floored at zero** — never negative | [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 미경과보험료 | Added to the surrender value on termination | [REG-R19 제7-66조제5항](#krlib-reg-r19) |
| 보험계약대출 (policy loan) | Contractually permitted within the surrender value, 「그러나 순수보장성보험 등 보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다」 — and **nil in fact** on the representative form | [S2 제34조] [REG-R25 제33조](#krlib-reg-r25) [REG-R28] |
| 자동대출납입 (automatic premium loan) | Contractually available — requested before the 납입최고기간 ends, running **1년 at a time**, unwindable within **1개월**, notified within **15일** of ending — and **inoperative** for the same reason | [S2 제26조] |
| 납입최고(독촉)기간 (grace) | **14일** from the written, recorded-telephone or electronic demand (**7일** where the term is under a year), extended to the next business day | [S2 제27조] [REG-R25 제26조](#krlib-reg-r25) |
| Claim within grace | Paid: 「해지 전에 발생한 보험금 지급사유에 대하여 회사는 보상하여 드립니다」 | [S2 제27조] |
| 실효 / 해지 (lapse) | The day after the 납입최고기간 ends; the surrender value is paid, net of any policy loan | [S2 제27조] [REG-R25 제26조](#krlib-reg-r25) |
| 부활 (reinstatement) | Available for **3년** from the termination date provided the surrender value was not drawn — 「해약환급금이 없는 경우를 포함합니다」, so a 무해지 policy is **always** eligible. Arrears bear interest 「평균공시이율+1% 범위 내에서 회사가 정하는 이율로」 | [S2 제28조] [REG-R25 제27조](#krlib-reg-r25) |
| — effect on the clocks | Re-runs the 계약 전 알릴 의무, the 사기 rule, acceptance and the start of cover, and **restarts the two-year suicide window**. A disclosure breach at the original application still bites | [S2 제6조·제28조] |
| 특별부활 | Where the contract was terminated by 강제집행, 담보권실행 or a tax seizure: the insurer notifies the 보험수익자 within **7일**, who may repay the creditor, become the policyholder and revive the contract within **15일** | [S2 제29조] |
| 청약철회 (cooling-off) | **15일 from receipt of the 보험증권 and never more than 30일 from the application date** (45일 where a policyholder aged 65 or over contracted by telephone). Effective on despatch; refund in full within **3영업일** | [S2 제18조] [REG-R25 제17조](#krlib-reg-r25) [REG-R51]; scope **[std]** (22) |
| — exclusions | Where the insurer paid for a health examination, where the term is 90일 or less, or for a 전문금융소비자 | [S2 제18조] [REG-R25] |
| 품질보증해지 | Cancellation within **3개월 of formation** where the 약관 was not delivered, its important content not explained, or the application not signed; premiums returned with 보험계약대출이율 interest | [REG-R25 제18조제3항](#krlib-reg-r25) [REG-R49 제638조의3](#krlib-reg-r49) |
| 위법계약의 해지 | Within **1년 of learning of a selling-rule breach and 5년 of the contract date**; the insurer answers within **10일** and returns the **계약자적립액** — the full reserve, **with no surrender charge** | [S2 제30조의2] [REG-R25 제29조의2](#krlib-reg-r25) |
| 계약 전 알릴 의무 (contestability) | Termination barred once **2년** have run from the 보장개시일 without a claim event (**1년** for disease on a 진단계약), or **1개월** after the insurer learns the ground, or **3년** from the contract date | [S2 제14–15조] [REG-R25 제13–14조](#krlib-reg-r25) [REG-R49 제651조](#krlib-reg-r49) |
| 사기에 의한 계약 | **취소 within 5년 of the 보장개시일** (and 1개월 of learning), on proof of 뚜렷한 사기의사; premiums paid are returned | [S1] [S2 제16조] [REG-R25 제15조](#krlib-reg-r25) |
| 계약의 무효 | No written consent of the life assured; a life under 만 15 or of unsound mind; or an issue age outside the product's range. Premiums returned | [S2 제20조] [REG-R50 제731조·제732조](#krlib-reg-r50) |
| 중대사유로 인한 해지 | Claim provocation, or forging or altering claim documents: 해지 within **1개월** of learning, surrender value paid | [S2 제31조] |
| 소멸시효 (prescription) | **3년** on the 보험금청구권, the 보험료 반환청구권, the 해약환급금청구권 and the 계약자적립액 반환청구권 | [S2 제38조] [REG-R49 제662조](#krlib-reg-r49) |
| 감액완납 / 연장정기 | **Neither exists** in any retrieved 약관 or 상품요약서 | [S1] [S2] [S6] [S8] [S10] [S11] [S12] |
| 예금자보호 | 해약환급금 plus 기타지급금 protected to **₩100,000,000 per person**, and 사고보험금 protected to a **separate and additional ₩100,000,000**. **Corporate policyholders are not protected at all** | [S3] [S11] [S13] [REG-R52 제18조제7항](#krlib-reg-r52) [REG-R32] |
| Interpretation | Good faith; **contra proferentem** — 「회사는 약관의 뜻이 명백하지 않은 경우에는 계약자에게 유리하게 해석합니다」; no expansive reading of exclusions; a sales document contradicting the 약관 is read in the policyholder's favour | [S2 제39조·제40조] |

22. **Cooling-off.** 금융소비자보호법 제46조제1항제1호 gives the statutory right — the
    earlier of 15 days from receiving the 보험증권 and 30 days from application — and the
    표준약관 implements it verbatim [REG-R51] [REG-R25]. One carrier markets it as 「100%
    무료 반품 … 가입일로부터 30일 이내」 [S13]. It is a genuine early-duration decrement and
    the composite excludes it explicitly: the model begins with cover in force and the
    withdrawn population already out.

---

## Contractual mechanics

### Premium provisions

The office premium is level **within** each 보험기간 and, on a 비갱신형 contract, for the
whole of it. With `P_m` the monthly office premium, `SA` the 보험가입금액 and `x` the issue
보험나이, the representative structure is proportional in the sum assured:

    P_m = r(sex, x, n, class, form) * SA / 100,000,000

with `r(M, 40, 20, 표준체, 무해지 순수보장형) = 15,080` at the anchor [S12] [S4], and the
annual-grid model using `P_a = 12 * P_m = 180,960` **[std]**. **No flat policy element can
be separated out**, because no Korean rate card retrieved varies the sum assured (Premiums,
footnote 11); the model therefore treats the office premium as proportional and records the
approximation.

There is **no premium review within a term** and no insurer discretion over the level. On a
비갱신형 contract the only contractual route by which the premium ever changes is a change
the policyholder initiates — a 감액, a rate-class movement (below), a 단체취급 election, or
the 납입면제 switching it off entirely. On a 갱신형 contract the premium changes at renewal
by construction, and the whole basis moves, not just the age: 「보험나이증가, 기초율(적용이율,
계약체결비용, 계약관리비용 및 위험률) 등의 변동에 따라 갱신시 보험료가 변동(특히, 인상)될 수
있습니다」 [S15], in the same words at [S9].

**The rate class is not a fixed attribute of the policy, and that is a Korean peculiarity
with no analogue anywhere else in this repository.** In `jplib` a preferred class is set at
issue and carried unchanged through every renewal to age 80 regardless of later health. In
Korea the class is a rider that tracks the insured's smoking status for the life of the
contract, and it moves in **both** directions [S2 건강체서비스특약Ⅱ 제4조]. If the life
smokes continuously for 30 days or more, the policyholder must notify the insurer in writing
without delay; the insurer then recovers a **정산차액** — the discount already taken — and
reverts the premium to the 표준체 scale, or, if the arrears are not paid, **reduces the
보험가입금액 in the ratio of the preferred premium to the standard premium**. Failure to
notify for 30 days without good reason lets the insurer make the same reduction and cancel
the rider unilaterally, whether or not a claim has arisen. In the other direction a standard
life who quits and passes the tests may **upgrade mid-term**, paying the discounted premium
from the application date and receiving back any excess 계약자적립액 released by the
repricing. The same upgrade path exists at two more carriers for a life originally accepted
under a substandard rider whose condition improves [S11] [S12]. `Term_KR_S` does not model
class movement; the specification records that the Korean class is a **state**, not a
parameter, because a model that later needs it will need a transition and not a relabelling.

### The death benefit, and the disability benefit Korea does not have

The main contract's benefit article is two lines. On the 만기환급형 [S2]:

> 제 4 조 보험금의 지급사유
> 회사는 피보험자에게 다음 중 어느 하나의 사유가 발생한 경우에는 보험수익자에게 약정한
> 보험금(별표 1 '보험금 지급기준표' 참조)을 지급합니다.
> 1. 보험기간이 끝날 때까지 살아 있을 경우: 만기보험금
> 2. 보험기간 중 사망한 경우: 사망보험금

The 순수보장형 carries limb 2 alone. Termination is immediate and automatic: 「보험기간 중
피보험자에게 제4조 제2호에서 정한 보험금의 지급사유가 발생한 경우에는 이 계약은 그때부터
효력이 없습니다」 [S2 제23조].

**One decrement pays one benefit.** This is the single largest structural difference between
`Term_KR_S` and the Japanese term chassis, and it simplifies the model in a specific way: a
Japanese projection carries 死亡 and 高度障害 as competing risks on one sum assured and must
be careful not to double-count them against a standard table that already includes the
second inside the first. Korea has no such interlock. What Korea has instead is a **second,
smaller decrement that switches the premium off without terminating the contract** — the
50% 장해 waiver — so the state space is: in force paying, in force premium-waived, dead,
lapsed, and (on the 갱신형) declined at renewal. The waived state is a real state and not a
cash-flow adjustment, because on the 만기환급형 the maturity benefit is computed as if the
waived premiums had been paid [S1] [S12], and because on the 무해지 form entering it
**destroys the post-완납 surrender-value step-up** [S2 제33조] [S12].

**What counts as death is wider than the fact of death.** A court's 실종선고 counts, deemed
to occur when the recognised 실종기간 ends, as does a 관공서 disaster notification at the
date entered in the 가족관계등록부 [S2 제5조제2항]. And the 약관 expressly disposes of an
argument that would otherwise be live in a jurisdiction with a life-sustaining-treatment
statute: 「연명의료중단등결정 및 그 이행은 … '사망'의 원인, '사망보험금' 지급에 영향을 미치지
않습니다」 [S2 제5조제3항].

### 갱신형 and 비갱신형 — attained-age repricing and where the contract ends

Three carriers publish renewal rules and they assemble into one structure [S6] [S9] [S15].

1. **Renewal is automatic and negative-option.** The contract renews unless the policyholder
   says otherwise, the notice period being 15 days where one is published [S9] [S15]. No
   carrier requires a positive election.
2. **There is no 고지 and no underwriting at renewal.** Nothing in any of the three
   conditions the renewal on health, on a 계약 전 알릴 의무 or on a 건강진단. The only
   conditions are age and term ceilings; the 갱신계약's own 가입나이 band (29세~79세 at
   흥국생명 [S6]) describes who can *be* in a renewed contract, not who may be
   re-underwritten into one. **This is the defining feature of the Korean 갱신형.**
3. **Repricing is at attained 보험나이 on the whole basis then in force** — 적용이율,
   계약체결비용, 계약관리비용 and 위험률, each named in the carriers' own words [S9] [S15].
   A renewal is not an age step on a frozen scale.
4. **The renewal is a new contract on a new product code.** 푸본현대생명 prints them
   separately (주계약 최초계약 `LO01011`, 갱신계약 `LO01012`, and the same split for every
   optional rider) and 삼성생명 states 「갱신형특약은 매 갱신시마다 갱신시점의 상품코드를
   적용합니다」 [S9] [S15].
5. **The ceiling truncates rather than refuses.** Where the run to the ceiling is shorter
   than a full cycle, the renewed term is cut to the remainder: 「갱신일부터 최종 갱신계약의
   보험기간 종료일까지가 10년미만일 경우에는 갱신일부터 갱신계약의 보험기간 종료일까지 이
   계약의 보험기간으로 합니다」 [S6].
6. **A premium waiver already running does not survive the renewal.** 흥국생명, verbatim:
   「다만, 새로이 갱신되는 계약에서는 갱신 전 보험료 납입면제 사유로 인한 보험료 납입면제를
   적용하지 않고, 보험료를 계속 납입하여야 합니다」 [S6]. A disabled life must resume
   paying. This is a material cash-flow rule and the sharpest single piece of evidence that
   a Korean renewal really is a fresh contract.
7. **The suicide and contestability clocks, by contrast, run from the original 보장개시일 and
   restart only on 부활** [S2 제6조]. So the contract is fresh for pricing and for the waiver
   and continuous for the exclusions — which is precisely the tension the boundary question
   turns on.

**The premium path, and what the 갱신형 actually is.** 흥국생명 publishes the mandatory
예상 갱신보험료 예시 on the anchor cell — 갱신형, ₩100,000,000, 40세, 10년만기, 전기납,
월납, 표준체 [S7]:

| 구분 | 가입시 | 1회갱신 | 2회갱신 | 3회갱신 |
|---|---|---|---|---|
| 갱신시 나이 | 40세 | 50세 | 60세 | 70세 |
| 남자 | ₩9,000 | ₩21,000 | ₩56,000 | ₩201,000 |
| 여자 | ₩6,000 | ₩10,000 | ₩24,000 | ₩103,000 |

Index against the issue premium: male **1.00 → 2.33 → 6.22 → 22.33**; female 1.00 → 1.67 →
4.00 → 17.17. The document's own caveat is essential and is reproduced rather than smoothed
over: the path 「최초계약 가입 당시의 보험료율을 기준으로 산출(연령증가만 반영)하였으므로,
갱신시 보험료율이 변동될 경우 갱신시점의 보험료는 상기 예시와 크게 달라질 수 있습니다」 [S7]
— it holds the rate scale frozen at its issue level and reflects **age alone**. A projection
that also moved 위험률 and 적용이율, as the contract permits, would differ.

흥국생명 is the only carrier selling both forms of one product, so it supplies the only clean
comparison available. On the disclosure basis (male 40, ₩100,000,000): 비갱신형 20년만기
전기납 is **₩15,000** a month, 갱신형 10년만기 전기납 is **₩9,000** [S4] [S6]. The renewable
form is **40% cheaper at issue** and, on the carrier's own frozen-scale projection, costs
₩21,000 from age 50 — 40% *more* than the level twenty-year premium — for the second half of
the same twenty years. Average monthly outlay over twenty years: level ₩15,000; renewable
`(9,000 × 120 + 21,000 × 120) / 240 = ₩15,000`. **On the carrier's own numbers the two are
almost exactly equivalent in undiscounted total cost**, which is the cleanest available
statement of what a 갱신형 is: the same risk, financed differently, with the repricing risk
moved onto the policyholder.

**The premium is a function of the renewal index, not of the policy year.** On a 갱신형 the
premium at policy year `t` is `P(k)` where `k = 1 + floor((t − 1) / cycle)` is the renewal
index — 1 in the original 보험기간, as `technical-notes.md` and `Term_KR_S.term_index` both
number it — and `P(k)` is struck at attained age `x + (k − 1) × cycle` on the scale in force
at that date. A model that indexes the premium by policy year cannot represent the product,
and a
model that carries a single level premium across a renewal boundary silently converts a
갱신형 into a 비갱신형 at the wrong price.

**The horizon is the renewal ceiling, not the term.** The 보험기간 of the contract in force
is one cycle. The horizon of the *cash flows the contract generates* is the ceiling: at
흥국생명, 보험나이 80, reached from the anchor issue age of 40 in exactly four cycles [S6]
[S7]. `Term_KR_S` therefore projects a 갱신형 model point to the ceiling, not to the end of
the first cycle, and reprices at each boundary.

**The renewal decline is its own decrement, and folding it into the lapse rate hides the
boundary.** At each renewal date a fraction of the surviving in-force population leaves
rather than accept the repriced contract. It is not ordinary lapse: ordinary lapse is
continuous, spread through the year and driven by affordability and by competing products,
whereas the renewal decline is **discrete, concentrated on a single date, and driven by the
size of the repricing step** — a step the policyholder was warned about in the 상품요약서 and
which, on the published path, is 2.33× at the first renewal and 3.6× at the third [S7]. The
representative projection therefore applies, at each renewal boundary and in this order:
mortality for the year; ordinary lapse for the year; then the renewal decline, on the
survivors of both. The ordering is not cosmetic — reversing it applies the decline to lives
that died or lapsed during the boundary year and understates the exposure of the renewed
cohort.

| Parameter | Representative value | Basis |
|---|---|---|
| Renewal cycle | 10 years | [S6]; observed 1 / 10 / 15 years [S15] [S6] [S9] |
| Renewal ceiling | 보험나이 80, with a final cycle truncated to the remainder | [S6] |
| Repricing rule | Attained 보험나이 on the whole 기초율 then in force | [S9] [S15] |
| Renewal-decline rate | **20% of in-force lives at each renewal date**, applied after mortality and after ordinary lapse | **[std]** (23) |
| Waiver carry-over | **None** — a waived contract resumes paying at renewal | [S6] |
| Suicide / contestability clocks | Continuous through renewals; restart only on 부활 | [S2 제6조·제28조] |

23. **The renewal decline is not published anywhere in Korea, for any product**, and this is
    a real gap rather than a research failure: the 예상 갱신보험료 예시 the disclosure
    requires shows the price path and not the persistency path [S7] [S16]. The **[std]** 20%
    is argued from three directions. First, the option is negative and the notice is only 15
    days, so inertia dominates and the rate must be well below a positive-election rate.
    Second, the step is large and disclosed in advance — an insurer that expected no reaction
    to a 2.33× repricing would not need to print the projection at all. Third, the nearest
    Korean supervisory calibration of a behavioural jump at a discrete contractual event is
    the FSS's floor of **at least 30% additional lapse** at the point a 단기납 종신보험's
    refund ratio peaks, itself calibrated to the 29.4%–30.2% eleventh-year lapse observed on
    single-premium bancassurance savings [REG-R27]. A renewal offers the policyholder no cash
    and no maturing option, only a higher price, so 20% sits deliberately below that floor.
    An arguable range is roughly 5% (pure inertia) to 40%, and the technical notes carry the
    parameter with an explicit sensitivity rather than a point estimate dressed as a fact.

**The contract boundary: both readings, published.** Under K-IFRS 제1117호 [REG-R60] the
question is whether the substantive obligation ends at the renewal date. Nothing retrieved
in this session — not the 감독규정 [REG-R9] [REG-R19], not the 표준약관 [REG-R25], not the
IFRS17 계리가정 가이드라인 [REG-R27] — addresses a Korean term renewal's boundary, so which
reading Korean insurers take is **[unverified]** and this document takes neither.

- **The short reading — the boundary falls at each renewal date.** The insurer may reprice
  the *entire* basis at renewal, 위험률 included, and the carriers say so in terms [S9]
  [S15]; the renewal is issued on a new product code [S9] [S15]; the renewed contract is
  governed by the rate scale and the 약관 then in force; and a waiver already running is
  extinguished [S6], which is hard to reconcile with a single continuing obligation. On this
  reading the contract in the measurement is one cycle long, the renewal premiums are outside
  it, and the renewal decline is not a decrement at all but simply the end of the contract.
- **The long reading — the boundary falls at the ceiling.** The renewal is
  **guaranteed-issue**: there is no 고지, no underwriting and no health condition [S6] [S9]
  [S15], so an impaired life renews at the same price as a healthy one of the same attained
  age. The repricing is therefore at portfolio level and cannot fully reflect the risks of
  the *particular* policyholder, which is the test that keeps a renewal inside the boundary.
  On this reading the contract runs to 보험나이 80, every renewal premium and every renewal
  decline is inside it, and the anti-selective drift of the renewing population is a modelled
  quantity.

`Term_KR_S` implements the long reading as its **base**, because it is the one that requires
the machinery — the repricing, the ceiling, the decline decrement — and because a model that
can project to the ceiling can always be truncated to one cycle, while the reverse is not
true. The horizon is a model parameter and the projection is re-runnable on either reading;
the technical notes show both.

### 무해지환급형 — the suppressed surrender value

The clause, in the anchor form's own words [S2 제33조]:

> ② 회사는 '해약환급금 미지급형(납입기간중 0%, 납입기간후 50%)' 계약이 보험료 납입기간 중
> 해지될 경우 해약환급금을 지급하지 않으며, 보험료 납입기간이 경과된 이후 해지될 경우
> '표준형' 해약환급금의 50%에 해당하는 금액을 지급합니다. 다만, 보험료 납입이 면제된 이후
> 보험료 납입기간이 경과되기 이전에 해지할 경우에는 해약환급금을 지급하지 않으며, 보험료
> 납입기간이 보험기간과 동일한 계약(이하 '전기납 계약'이라 합니다)의 경우에는 보험기간 중
> 계약이 해지될 경우 해약환급금을 지급하지 않습니다.

Six consequences, each of which a model has to respect.

1. **The 표준형 is a phantom.** It cannot be bought — 「가입이 불가능」 — and exists only as
   the comparator the insurer is obliged to disclose. It is nonetheless fully specified: its
   해약환급금 is 「산출방법서에 정한 방법에 따라 계산한 금액으로 **해지율을 적용하지 않고**
   계산」. So the 표준형 value is the ordinary net-premium reserve less the surrender charge,
   and the 무해지 value is a **contractual override of it**, not a different reserve. Two
   more carriers use the identical construction and the identical phrase [S12] [S18].
2. **On the representative 전기납 contract the surrender value is nil at every duration**,
   because the payment period never ends before the term does. 한화생명's published
   해약환급금 예시 for 순수보장형, ₩100,000,000, 40세, 60세만기, 전기납 shows 환급률 0.0% at
   **all eleven durations printed**, for both sexes, against cumulative premiums rising to
   ₩3,840,000 [S1]. That is the 단서 in numbers, and it is why the representative product has
   **no policy loan and no automatic premium loan in fact** even though the 약관 grants both.
3. **The step-up exists only on a shortened-pay contract**, and it is **50% of the 표준형**
   at both carriers that publish one [S1] [S2] [S12], **95% of the 기본형** on the corporate
   three-step schedule [S18]. The FSC's 2021 measures contemplated a menu at 10 / 20 / 30 /
   40 / 50% [R12].
4. **A waiver kills the step-up.** A life whose premiums have been waived and who then
   surrenders before the nominal 납입완료 date receives nothing, where a paying policyholder
   at the same duration would receive the 50% [S2] [S12]. The waived state and the paying
   state are therefore different states for the value as well as for the cash flow.
5. **The payment period is defined to the day and it shortens if premiums are paid up
   early**: 「계약일로부터 보험료 납입기간이 경과하여 최초로 도래하는 계약해당일 전일까지」,
   with an express override where the total is completed sooner [S2 제33조제3항].
6. **The regulator, not the contract, is what makes it possible.** 감독규정 제7-66조제4항
   permits a 순수보장성보험 whose premiums or benefits were calculated using a **최적해지율**
   to pay less than the 별표-14-floored value — a dispensation conditional on having used a
   best-estimate lapse rate in pricing, which is why the 적용해지율 is disclosed at all
   [REG-R19] [S1] [S12]. 제4항제2호 then caps the design: where the value during the payment
   period is less than 50% of an equivalent 표준형's, the post-payment value must exceed 50%
   of the 표준형's **and** the post-payment 환급률 must exceed the greater of 100% and the
   표준형's [REG-R19] [REG-R28]. Variable products are excluded outright [REG-R19
   제4항제1호](#krlib-reg-r19).

**What the suppression is worth, and why it is worth so little here.** Three independent
measurements differ by an order of magnitude:

| Basis | 무해지 | 표준형 | Saving |
|---|---|---|---|
| Anchor cell: male 40, ₩100m, 20년만기 20년납 [S12] | ₩15,080 | ₩15,320 | **−1.57%** |
| Same, female 40 [S12] | ₩8,010 | ₩8,120 | **−1.35%** |
| Male 40, ₩100m, **100세만기** 전기납, as stated [S3] | — | — | **−14%** |
| FSC illustration, post-완납 refund 50% against 100% [R12] | ₩24,000 | ₩32,100 | **−25.2%** |

The reason the term product's saving is so small is structural and belongs in the
specification rather than in a footnote: **on a twenty-year level term the 표준형 reserve is
itself tiny**, peaking near a third to a half of cumulative premiums around duration six and
running to exactly zero at maturity, so suppressing it releases almost nothing. On a
100세만기 contract — which is a whole-life contract wearing a term product's name — the
reserve is large and the saving is real. The 무해지 form is a **savings-product device
carried across to term**, and its economics on term are marginal. That is why the anchor
carrier quotes a 1.57% saving on the twenty-year basis and another quotes 14% on a 100세만기
one; both are correct about different contracts.

The FSC's own illustration makes a second point that matters for any attempt to parameterize
the depth of the suppression [R12]:

| 납입완료 후 해지환급금 | 10% | 20% | 30% | 40% | 50% | 표준형 (100%) |
|---|---|---|---|---|---|---|
| 보험료 | ₩26,400 | ₩25,200 | ₩24,300 | ₩24,000 | ₩24,000 | ₩32,100 |

The saving is **not linear in the suppressed value** — it saturates by the 30–40% step and
40% and 50% price identically. The whole span from 10% to 50% is worth ₩2,400 out of
₩32,100, while the step from 표준형 to *any* suppressed form is worth ₩5,700 to ₩8,100.
**The pricing gain is in applying a 해지율 at all, not in how deep the suppression goes.**

**The surrender charge, and why the statutory cap does not bite on this product.** Every
carrier states the formula in the same words: 「순보험료식 계약자적립액에서 해약공제액
(미상각신계약비)을 공제한 금액」 [S1] [S6] [S10] [S11] [S12]. The deduction is capped by
보험업감독규정 제7-66조제1항제3호 and its 별표 14 [REG-R19] [REG-R20] [R9]:

    표준해약공제액 = 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000

with 해약공제계수 = the policy term in years capped at 20 for a 보장성보험, and the
연납순보험료 recomputed on a whole-term-pay basis (20-year pay where the term is 20 years or
more) [REG-R20]. At the anchor cell the sum-assured component alone is
`100,000,000 × 10/1000 = ₩1,000,000`, against a gross annual premium of ₩180,960 — **5.5
years' premium**, before the 연납순보험료 term is added at all. An insurer applying the full
statutory cap could therefore pay a nil surrender value on this contract for its whole term.
Published 표준형 curves do not: they reach 46% of premiums paid by duration six [S10]. **So
the constraint that shapes a Korean term surrender value is not 별표 14's level.** It is
제7-66조제1항제2호's **해약공제기간 — the payment period or the acquisition-cost period,
capped at seven years** — together with the zero floor of 제1항제1호 [REG-R19], and beyond
those it is commercial choice. That distinction matters for the technical notes, which
calibrate the amortisation to the published curves rather than to the cap, and it resolves a
question the product research file had to leave open: the article's own text was not
retrievable there, and it was retrieved for the cross-product reference library [REG-R19].

For the same reason the 2019 rule of thumb — the 표준해약공제액 as **13 months' premium for a
보장성보험** [REG-R29] — does not transfer to this product. It is calibrated on a 보장성보험
whose premium is large relative to its sum assured; a ₩100,000,000 term policy costing
₩15,080 a month is the opposite extreme, and its 별표 14 cap exceeds thirteen months'
premium by roughly a factor of five.

**The published surrender-value shapes** are the calibration target and are recorded here
because they are the only public reserve data in the Korean retail market. On a 표준형-
equivalent 순수보장형, male 40, ₩100,000,000, 20-year term, as 환급률 (surrender value over
cumulative premiums) [S6] [S8] [S9] [S10] [S12]:

| 경과 | 흥국 [S6] | 삼성 인터넷 [S8] | 삼성 내리사랑 [S9] | 교보라플 표준형 [S12] | 신한 [S10] |
|---|---|---|---|---|---|
| 1년 | 0.0% | 0.0% | 0.0% | 0.00% | 4.0% |
| 2년 | 28.9% | 20.3% | 0.0% | 23.20% | 31.9% |
| 3년 | 38.8% | 27.9% | 0.0% | 31.42% | 40.6% |
| 5년 | 45.1% | 33.4% | 9% | 36.73% | 45.8% |
| 7년 | 45.6% | — | — | 37.25% | 45.6% |
| 10년 | 39.4% | 30.3% | 21% | 32.36% | 38.9% |
| 15년 | 24.1% | 18.7% | 13% | 19.57% | 23.0% |
| 20년 | 0.0% | 0.0% | 0.0% | 0.00% | 0.0% |

Two features must be reproduced by any model that claims to represent this reserve. The
ratio peaks around duration six and the **absolute amount peaks later** — 신한라이프's male
value peaks at ₩673,100 at duration 10 while its 환급률 peaks at 46.0% at duration 6 [S10] —
so a check against these tables must compare amounts, not ratios. And the value runs to
**exactly zero at maturity** on every 순수보장형 curve published, which is the diagnostic
that separates a term reserve from an endowment's.

**On the 갱신형 the reserve builds and unwinds inside each cycle.** 흥국생명's ten-year
renewable, male 40, ₩100,000,000: 0.0% at 3, 6 and 9 months; **0.1% at 1년**; 15.5% at 2년;
19.1% at 3년; 18.4% at 5년; 13.4% at 7년; **0.0% at 10년** [S6]. The policyholder receives
nothing at the renewal date. Modelling a 갱신형 as a single long contract with a single
reserve would misstate this completely, which is the second reason the boundary question is
not academic.

### 보험료 납입면제 — the premium waiver

The trigger is identical at every carrier in the set and it is a disability test, not an
accident test [S2 제5조제1항]:

> ① 보험료 납입기간 중 피보험자가 장해분류표(별표 4 참조) 중 동일한 재해 또는 재해이외의
> 동일한 원인으로 여러 신체부위의 장해지급률을 더하여 50% 이상인 장해상태가 되었을 경우에는
> 차회 이후의 보험료 납입을 면제하여 드립니다.

The same sentence, to the word, appears at seven more carriers [S1] [S6] [S8] [S9] [S10]
[S11] [S12]. Four features drive the model.

- **Cause-neutral.** 「동일한 재해 또는 재해이외의 동일한 원인으로」 — sickness qualifies
  equally with accident, so the waiver decrement is a general disability incidence and not a
  scaled accident rate. Only the simplified-issue riders narrow it to accident alone [S17]
  [S18]. This is the opposite of `jplib`'s composite, where the waiver keys off an 不慮の事故
  within 180 days.
- **Percentage-based and additive.** The 장해분류표 is a **percentage scale**, not a binary
  trigger [REG-R25 부표 3](#krlib-reg-r25), and separate impairments from one cause are added, subject to the
  rule that two impairments in the same body part take the higher rate rather than the sum
  [S2 제5조제9항]. 장해 is defined as a **permanent** state remaining after treatment, which
  excludes temporary states during treatment [REG-R25 부표 3](#krlib-reg-r25); a temporary disability lasting
  five years or more nonetheless counts at 20% of its rate [S2 제5조제8항].
- **Determined at 180 days**, with a look-back if the state worsens later — 2년 where the
  term is ten years or more, 1년 where it is shorter [S2 제5조제4항·제5항]. There is a
  reporting lag here, and it is longer than the claim lag on death.
- **Future premiums only**, with no refund of past ones, and the contract continues in force
  [S2 제5조제1항].

The waiver is switched off by the same three intent limbs as the death benefit — 「보험료의
납입면제 사유가 발생한 때에는 납입을 면제하지 않습니다」 [S2 제6조] — it does not survive a
renewal [S6], and it forfeits the 무해지 step-up [S2 제33조] [S12]. `Term_KR_S` specifies the
waived state and its transitions and excludes the incidence from the base projection
**[std]**, for the reason `jplib` gives for the same decision: no Korean document publishes a
50%-plus 장해 incidence rate, the 참조순보험요율 behind it is not public [REG-R4] [R19], and
an invented rate attached to a real state is worse than a stated omission. The state is
carried so the technical notes can switch it on.

One carrier sells the idea the other way round, as an **optional diagnosis-triggered waiver
rider** in five varieties (일반암 / 뇌출혈 / 급성심근경색증 in five combinations, each 최초
1회한), whose own 가입금액 is defined as **the premium it waives**: 「이 특약의 가입금액은 이
특약이 부가된 종형별 주계약 및 그 주계약에 부가된 특약의 보험료 합계액」 [S12]. Another
splits its waiver rider by whether the rider's own 계약자적립액 is paid on death before a
waiver event — [특약유형 W] not paid and cheaper, [특약유형 S] paid — which is a
mini-version of the 무해지 device applied to a rider [S17] [S18]. Neither is in the
composite.

### 선지급서비스특약 — the acceleration

The rider is a 제도성특약 attached as standard and carrying no separate premium in any
retrieved document. Its terms, verbatim in the relevant parts [S2]:

> 제 3 조 … 피보험자의 남은 생존기간이 **12개월 이내**라고 판단한 경우에 … 주계약
> 사망보험금액의 일부를 선지급 사망보험금 … 으로 피보험자에게 지급합니다.
> 제 4 조 ① 이 특약에 의한 보험금 한도는 주계약 사망보험금액의 **50% 이내**에서 피보험자별로
> 통산하여 최고 **5,000만원**까지로 합니다. 다만, **1,000만원까지는 주계약 사망보험금액의
> 100% 이내**로 할 수 있습니다.

The judgement must come from a specialist at a 종합병원 as defined by 의료법 제3조의3, or a
foreign equivalent. The amount paid is the accelerated benefit **present-valued over the
remaining life expectancy at the 평균공시이율**, less the similarly discounted premiums that
would have fallen due on it and less any outstanding policy loan [S2 제4조제6항]. Payment
reduces the 보험가입금액 from the payment date and **no surrender value arises on the
reduction**; there is one payment per contract, and the recipient is the **피보험자** and not
the death beneficiary [S2 제4조].

At the anchor cell of ₩100,000,000 the 50% limb would give ₩50,000,000 and the ₩50,000,000
aggregate cap binds exactly, so the cap is visible at the anchor rather than only at large
model points. Against Japan's リビング・ニーズ特約: the Korean trigger is **12 months rather
than six**, the cap is **half the sum assured to ₩50,000,000** rather than the whole benefit
to ¥30,000,000, and there is **no bar on payment near expiry** at all. One carrier narrows
the trigger specifically for term business to six months [S17], which is the only variation
retrieved.

### Exclusions and 면책

The exclusion article has three limbs and only three, and they are reproduced almost word for
word at six more carriers [S1] [S2 제6조] [S6] [S8] [S10] [S11] [S17]:

> 1. 피보험자가 고의로 자신을 해친 경우 … 나. 계약의 보장개시일(부활(효력회복)계약의 경우는
>    부활(효력회복)청약일)부터 **2년**이 지난 후에 자살한 경우에는 … 사망보험금을 지급합니다.
> 2. 보험수익자가 고의로 피보험자를 해친 경우 … 다만, 그 보험수익자가 보험금의 일부
>    보험수익자인 경우에는 다른 보험수익자에 대한 보험금은 지급합니다.
> 3. 계약자가 고의로 피보험자를 해친 경우

**The suicide window is two years** and it is invariant across the whole Korean market —
every carrier in the set says 2년 [S1] [S2] [S3] [S6] [S8] [S10] [S11] [S13] [S17]. It is
one year shorter than Japan's three and one year longer than the UK's twelve months. It
restarts on 부활 and, expressly, **never on renewal**. Its first limb carries an exception
with no time bar at all, for an act committed 「심신상실 등으로 자유로운 의사결정을 할 수
없는 상태에서」, and the 약관 defines that state [S2].

**Why there is nothing else.** 상법 제659조 discharges the insurer generally for 「고의 또는
중대한 과실」, but 제732조의2 removes gross negligence for a death contract and preserves the
benefit where one of several beneficiaries is the killer [REG-R49] [REG-R50] [R4] [R6]. The
Korean life exclusion list is therefore **statutorily determined** and contains **no
negligence limb, no war clause, no aviation clause and no dangerous-pursuits clause** — none
appears in any 약관 or 상품요약서 retrieved. Nor is there any war-emergency **reduction
power** of the kind two Japanese carriers hold in `jplib`. Korea handles occupational and
avocational risk entirely at underwriting, through the **위험등급** and 직업별 가입한도 [S2
제24조제4항] [S3] [S6], and through the substandard-acceptance toolkit (Riders, below). **So
a Korean term policy's claim rate is a mortality question and not partly a coverage
question**, which is the opposite of the French position and materially different from the
German one.

The only graded benefit in the retrieved set is on the **간편고지형**: a non-accidental death
within two years of the contract date pays 「보험가입금액의 50%」 [S17] [S18]. There is no
감액기간 and no pre-existing-condition restriction on the 일반가입형 at any carrier.

### 계약 전 알릴 의무, 사기 and 계약의 무효 — three unwinding routes on three clocks

**계약 전 알릴 의무** is the Korean 고지의무 and the 약관 says so in terms [REG-R25 제13조](#krlib-reg-r25).
The insurer may terminate, or restrict cover, where the 계약자 or 피보험자 intentionally or
by gross negligence misstated or concealed a material matter — but **not** where [S2
제14–15조] [REG-R25 제13–14조](#krlib-reg-r25):

1. it knew the fact, or negligently did not know it, at the time of contracting;
2. **1개월** has passed since it learned of the ground, **or 2년 has passed from the
   보장개시일 without a claim event arising** (1년 for disease on a 진단계약);
3. **3년** have passed since the contract date;
4. it accepted on a 건강진단서 사본 and the claim arises from something recorded there; or
5. the 보험설계사 prevented truthful disclosure.

Limbs 2 and 3 track 상법 제651조's 1개월 / 3년 pair, and the **2년 / 1년 no-claim window is a
contractual improvement on the statute** and is the operative contestability period
[REG-R49]. A causation defence runs alongside: 상법 제655조 requires payment where the
non-disclosure is proved not to have affected the event [REG-R49]. On rescission the insurer
pays the surrender value — nil, here; where it restricts cover instead, 「보험료, 보험가입금액
등이 조정될 수 있습니다」 [S1] [S2] [S11].

**사기에 의한 계약 is separate and much longer.** Where the insurer proves 뚜렷한 사기의사 —
a proxy medical, drugs taken to pass a test, a forged certificate, or concealment of a
pre-application cancer or HIV diagnosis — it may **취소** the contract 「보장개시일부터 5년
이내(사기사실을 안 날부터는 1개월 이내)」 and returns the premiums paid [S1] [S2 제16조] [S6]
[S8] [S10] [S11] [S17] [REG-R25 제15조](#krlib-reg-r25). **The effective outer limit on unwinding a Korean
life policy is therefore five years, not two or three.**

**계약의 무효** is the third route and is statutory rather than contractual: absence of the
life assured's written consent (상법 제731조), a life under 만 15 or of unsound mind (제732조),
or an issue age outside the product's range [S2 제20조] [REG-R50] [R3] [R4]. Premiums are
returned; where premiums had been waived, only those actually paid are returned. Note that
this one test uses **만나이 and not 보험나이**, and the 약관 says so expressly [S2 제22조제1항
단서].

### 청약철회, 품질보증해지 and 위법계약의 해지 — three exits with different money

Korea gives the policyholder three distinct statutory exits, and they are worth separating
because each returns a different amount.

- **청약철회**, under 금융소비자보호법 제46조 [REG-R51]: the earlier of **15일 from receiving
  the 보험증권** and **30일 from the application** (45일 for a telephone contract by a
  policyholder aged 65 or over), effective **on despatch**, with the premium returned in full
  **within 3영업일** and interest at the 보험계약대출이율 if late [S2 제18조] [REG-R25 제17조](#krlib-reg-r25).
  Not available where the insurer paid for a health examination, where the term is 90일 or
  less, or for a 전문금융소비자. One carrier markets it as a 30-day free return [S13].
- **품질보증해지**, under 상법 제638조의3제2항 [REG-R49]: where the 약관 and the
  policyholder's copy of the application were not delivered, the important content was not
  explained, or the policyholder did not sign, cancellation **within three months of
  formation** with premiums returned plus 보험계약대출이율 interest [REG-R25 제18조제3항](#krlib-reg-r25).
- **위법계약의 해지**, under 금융소비자보호법 제47조: where the insurer breached the selling
  rules, termination may be demanded **within 1년 of learning of the breach and 5년 of the
  contract date**; the insurer must answer within **10일**; and on termination it returns
  「회사가 적립한 해지 당시의 **계약자적립액**」 — **the full reserve, with no surrender
  charge deducted** [S2 제30조의2] [REG-R25 제29조의2](#krlib-reg-r25).

The third is materially better than an ordinary 해지 and it has **no analogue in any other
library in this repository**. On the representative 무해지 form the difference is the whole
value: an ordinary surrender pays nothing, and a 위법계약 termination pays the entire
계약자적립액. `Term_KR_S` does not model it, there being no published incidence of
mis-selling findings, but a Korean model that treated the surrender value as uniformly nil
would be wrong about a real, if small, cash flow.

### 납입최고, 실효, 부활, and the two loans

The persistency machinery is short and is the whole of it [S2 제26–29조] [REG-R25 제26–27조](#krlib-reg-r25).
Non-payment starts a **납입최고(독촉)기간 of 14일** — 7일 where the policy term is under a
year — extended to the next business day if it ends on a non-business day. The demand must be
in writing, by recorded telephone or by electronic document, and must state both the arrears
and the fact that the contract terminates the day after the period ends. A claim arising
**before** the termination is paid. On termination the insurer pays the surrender value and
immediately deducts any policy-loan principal and interest.

**부활 is available for three years** from the termination date, provided the surrender value
was not drawn — and expressly 「해약환급금이 없는 경우를 포함합니다」, so a 무해지 policy is
**always** eligible, which is the case that matters here [S2 제28조] [REG-R25 제27조](#krlib-reg-r25). Arrears
carry interest at a rate the insurer sets 「평균공시이율+1% 범위 내에서」. Reinstatement
re-runs the 계약 전 알릴 의무, its violation effects, the 사기 rule, acceptance and the start
of cover, and **restarts the two-year suicide window** — but 「회사는 해지 전 발생한 보험금
지급사유를 이유로 부활을 거절하지 않습니다」, and a disclosure breach at the *original*
application still bites after reinstatement. **부활 is the only event that resets a clock on
this chassis; 갱신 resets none.** There is also a **특별부활** where the contract was
terminated by 강제집행, 담보권실행 or a tax seizure of the surrender-value claim: the insurer
notifies the 보험수익자 within 7일 and the beneficiary may, with the policyholder's consent,
repay what the insurer paid the creditor and revive the contract within 15일 [S2 제29조].

**Both loans exist in the 약관 and neither operates on the representative product.** The
보험계약대출 is available within the surrender value, with the express warning 「그러나
순수보장성보험 등 보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다」 [S2 제34조]
[REG-R25 제33조](#krlib-reg-r25); the FSS made the point directly in its 2019 consumer alert — a 무해지환급금
contract **cannot support a policy loan during the payment period** [REG-R28]. The
자동대출납입 is genuinely available on this chassis, unlike `jplib`'s composite where one
carrier states its absence in terms: it must be requested before the 납입최고기간 ends, stops
once loan plus interest would exceed the surrender value, runs for **1년 at a time** and must
be re-applied for, may be unwound by asking to 해지 within **1개월** of the end of the
original grace period (in which case the insurer treats it as never having happened), and its
ending must be notified within **15일** [S2 제26조]. On a 전기납 무해지 contract there is
nothing to lend against at any duration, so **the lapse model for this chassis is a plain
lapse model**: 납입최고 → 실효 → 부활-or-not, with no no-lapse mechanism in between. That is
part of why it is the right chassis to specify first.

### Expiry and maturity

A 비갱신형 순수보장형 contract expires at the end of its 보험기간 with **nothing payable, no
maturity value and a surrender value that has already run to zero** [S1] [S8] [S12] — the
zero being a property of the reserve on every published curve, not merely of the 무해지
override. On the 만기환급형 variant the maturity benefit is 100% of the premiums paid on the
주계약, computed **as if any waived premiums had been paid** [S1] [S12]; the maturity-date
surrender value on that form includes the maturity benefit and therefore reads 100.0% [S1].

A 갱신형 contract does not expire at the end of its cycle at all — it expires at the ceiling,
보험나이 80 on the composite, and until then it renews. If the first premium of a renewed
cycle is not paid the ordinary 납입최고 machinery applies to the renewed contract; nothing in
the retrieved Korean set contains the Japanese rule under which a failed first renewal
premium is treated as unwinding the renewal itself, so the composite treats it as an ordinary
lapse of the renewed contract and marks the point **[unverified]**.

---

## Riders and options

**In scope (modelled or parameterized):**

- **보험료 납입면제** — in the 주계약, 50%-plus 장해지급률 from any cause, waiving future
  premiums only. The state is specified and its incidence is excluded from the base run
  **[std scope]**, no Korean 장해 incidence rate being public [REG-R4] [R19]. It is **not**
  the mortality decrement scaled and must not reuse that rate [S1] [S2] [S6] [S8] [S9] [S10]
  [S11] [S12].
- **갱신** — modelled in full on the 갱신형 variant: attained-age repricing on the whole
  basis, truncation at the ceiling, the waiver not carrying over, the clocks not restarting,
  and the renewal decline as a separate decrement [S6] [S7] [S9] [S15].
- **선지급서비스특약** — parameterized as a discounted acceleration with the 50% / ₩50,000,000
  cap and the ₩10,000,000 full-payment window; switched off in the base run. At the anchor
  sum assured the aggregate cap is **exactly reached and reduces nothing** — 0.5 ×
  ₩100,000,000 = ₩50,000,000 — so it binds only above it [S2] [S10] [S12] [S17] [S18].
- **감액** — a sum-assured reduction with **no payment**, no surrender value arising from it
  on this form [S2] [S12].
- **부활** — a reinstatement transition out of the lapsed state at a **[std]** behavioural
  rate, restarting the suicide clock; no Korean document publishes a reinstatement rate [S2].
- **Rate classes** — four-class mortality relativities are published and are carried as a
  parameter, though the base run is 표준체 [S11] [S12].
- **재해사망 uplift** — a second mortality vector at 2× the sum assured, published
  예정 재해사망률 at three ages, switched off in the base [S6] [S10].

**Specified but out of scope (contractual detail carried, not modelled):**

- **지정대리청구서비스특약** — changes who may claim, not what is paid [S1] [S2] [S10] [S11]
  [S12] [S17].
- **단체취급특약 / 신한단체취급보험료할인특약Ⅱ** — a 1.5%–5% discount for an affinity group
  of five or more [S1] [S10] [S12] [S13].
- **장애인전용보험전환특약** — moves the contract into the 15% tax-credit basket of 소득세법
  제59조의4 제1호 [REG-R57]; present at every carrier [S1] [S10] [S11] [S12] [S17].
- **출산육아휴직 보험료 납입유예특약** — a 6- or 12-month premium holiday, once per contract,
  around childbirth or parental leave. A genuinely Korean policy response to the birth rate,
  present at four carriers [S1] [S12] [S17] [S18].
- **The substandard-acceptance toolkit** — 특정 신체부위·질병 보장제한부 인수특약,
  표준하체인수특약 / 특별조건부인수특약 / 표준미달체조건부인수특약, and the three methods one
  carrier names in a line: 「할증보험료법, 보험금감액법, **나이가산법**」 [S17]. The first two
  map onto Japan's 保険金削減支払法 and 特定部位不担保法; **나이가산법**, rating up the age,
  has no `jplib` counterpart.
- **사후정리특약 / 사망보험금 신속지급특약** — an advance of part of the death benefit for
  funeral costs [S10] [S12] [S17].
- **양육자금(사망보험금분할지급설정)서비스특약** — pays the death benefit to a child in annual
  instalments with interest [S12] [S13].
- **건강체서비스특약Ⅱ and the class-discount riders** — 비흡연자할인특약Ⅲ, 건강체할인특약,
  슈퍼건강체할인특약Ⅱ, which is how two carriers implement rate classes without a 종 split
  [S2] [S12].
- **종신전환특약 and 연금전환특약** — present at one carrier [S17] [S18]; see Options,
  footnote 21.
- **Optional diagnosis-triggered waiver riders** — five varieties at one carrier, whose
  가입금액 is the premium they waive [S12], and a W/S 유형 split at another [S17] [S18].

**Absent from the market rather than out of scope.** No retrieved document offers indexation
or an increasing-cover option on a retail contract (the 체증 designs are corporate-only), a
guaranteed-insurability option on life events, joint-life or first-death cover, **감액완납
(reduced paid-up)** or **연장정기 (extended term)**. A Korean term policyholder in difficulty
has the 납입유예 rider, a 감액, or lapse, and nothing else — 자동대출납입 is granted by the
약관 but inoperative on the representative form, there being no surrender value to lend
against [S2 제26조·제34조] [REG-R28]. That is a shorter list of alternatives to lapse than
any other library in this repository carries.

**The 정기특약 — a term rider on a 종신보험 — is a live question this document leaves open.**
The structure is a standard part of the Korean traditional-agency proposition in secondary
material, including a rule that 「무배당 정기특약의 경우 보장내용이 동일한 특약에 대하여
갱신형과 비갱신형을 함께 부가할 수 없습니다」 — [unverified], a search snippet whose source
page could not be retrieved and whose intended primary source returned HTTP 404 [S23].
**Four current whole-life documents were checked as negative evidence and none carries a term
rider**: two 한화생명 products, one AIA product and the 종신보험 view of the comparative
disclosure across two pages, in which the substring 정기 appears only in the page's own
category labels [S19] [S20] [S21] [S22]. The honest reading is that the 정기특약 is a legacy
and traditional-channel structure displaced in the current product set by standalone online
정기보험 and by health and CI riders on the whole-life chassis. This document therefore treats
the **standalone contract as the market form** and records the rider form as alternative
packaging, tagged [unverified].

---

## Variations across insurers

1. **Age and term envelope.** 가입나이 minima run 만15세 to 30세 and maxima 60세 to 70세;
   term menus run from a single option — 90세만기 only [S18], 1년만기 only [S15] — to eleven
   [S12]. The 세만기 ceiling has moved from 80세 to 90세 and 100세 within the current product
   set [S1] [S9] [S12] [S17]. Composite: 만19세–65세, 20년만기 전기납 base with a 년만기 /
   세만기 menu (footnotes 4, 5).
2. **Surrender-value form — and the disclosure taxonomy that obscures it.** Observed: nil
   throughout on a 전기납 무해지 [S1] [S2]; **50%** of the 표준형 after 납입완료 [S1] [S2]
   [S12]; **0% / 30% / 95%** at three and five years on the corporate form [S18]; and a
   10–50% menu contemplated by the regulator [R12]. In the disclosure only **6 of the 45
   정기보험 rows** are flagged 무해지/저해지환급 and **all six are 경영인정기보험** [S4] —
   which is a **disclosure-taxonomy artefact, not a product fact**. The 해약환급금 column
   carries a product's headline 환급 type (순수보장 / 만기환급 / 무해지·저해지환급 /
   무진단무심사), so a 순수보장 term product whose surrender value is suppressed is still
   tagged 순수보장, and both the anchor product and 한화생명's 미지급형 appear as 순수보장. A
   later reader must not mistake that column for a census of 무해지 term.
3. **Maturity form.** 순수보장형 only [S9] [S10] [S15] [S18]; a 0% / 100% binary [S1] [S8]
   [S11] [S12] [S17]; and, at one carrier alone, a three-way **선택형 만기환급률 of 0% / 50%
   / 100%** [S14]. That carrier's own grid shows how convex the choice is on one cell — male
   40, ₩100,000,000, 20년만기 전기납: ₩17,100 / ₩29,800 / ₩110,100 — and prints ₩17,000 for
   what it describes as the same 표준체 cell elsewhere on the page, a 0.6% discrepancy
   recorded rather than reconciled [S14]. Composite: 순수보장형, with the 만기환급형 as a
   variant at 9.4× the premium [S12].
4. **Renewal.** Cycles of **1년** [S15], **10년** [S6] and **15년** on a rider [S9];
   ceilings of 80세 [S6], five years' total cover [S15] and the main contract's expiry [S9];
   an opt-out notice of 15일 where published [S9] [S15]. **What does not vary is that no
   carrier requires 고지 or underwriting at renewal** [S6] [S9] [S15]. Composite: 10-year
   cycle to 보험나이 80 (footnote 2).
5. **Rate classes.** One to four (footnote 7), with published maximum male-40 discounts of
   −11.1% [S6], −17.5% [S1], −30.5% [S4], −37.5% [S8], −40.4% [S11], −41.4% [S12] and −42.9%
   [S14], against female-40 discounts of −6.0% to −22.2%. The **criteria** are concrete and
   converge on two tiers: a preferred tier at 수축기/이완기혈압 <140/90 and BMI 18.5–26.5,
   and a super-preferred tier at <120/80 and BMI 20.0–25.0, with a smoking test of one year
   at the first and never at the second [S2] [S8] [S9] [S11] [S12]. Two carriers add a
   glucose test and one adds a **총콜레스테롤 <190 mg/dL** test found nowhere else [S8] [S11]
   [S12]. One defines 당뇨 진단이력 exhaustively, including the only HbA1c threshold in the
   set at 6.5% [S12]. No carrier mentions a cotinine assay, unlike Japan.
6. **Why the female preferred discount looks small — and it is not smaller than the
   mortality saving.** The published class mortality shows a best-to-standard ratio at male
   40 of **0.583** and **0.597** at the two carriers that print full tables — a 41.7% and
   40.3% saving, which lines up with the observed male premium discounts of 41.4% and 40.4%.
   At female 40 the ratios are **0.856** and **0.861**, savings of 14.4% and 13.9%, against
   premium discounts of **15.4%** and **14.1%** [S11] [S12] — so the female discount is
   marginally *deeper* than the disclosed mortality saving, not shallower, which is the one
   place a flat expense loading does not explain the data and nothing retrieved does. The
   female discount looks small in absolute terms only because female mortality is already
   low.
7. **적용이율.** 1.75% [S4] to **4.00%** [S4], retail mode 2.50%. Two internal patterns hold
   at every carrier that prices more than one form: 만기환급형 ≤ 순수보장형, and 갱신형 priced
   differently again from both (footnote 12).
8. **Mortality.** A factor of **1.77** between the highest and lowest disclosed 예정
   경험사망률 at male 40, and 1.74 at female 40 [S1] [S6] [S8] [S10] [S11] [S12] [S17]. The
   male-40 to female-40 ratio itself varies from 1.33 to 1.70 across carriers. By contrast
   the two carriers publishing **예정 재해사망률** agree to three significant figures at age
   20 and to within 10% everywhere [S6] [S10] — strong evidence that accidental-death rates
   are taken from the 보험개발원 참조 table almost unadjusted while all-cause rates are
   heavily adjusted [R19].
9. **적용해지율.** Disclosed only where a 무해지 form is sold, and both disclosures start at
   **0.1%**: 「납입기간 이내 연 0.1%~4.6%, 이후 연 0.7%~1.6%」 [S12] and 「연 0.1%~8.4%,
   이후 연 0.8%」 [S1]. The upper end of the in-payment range differs by a factor of 1.8; the
   convergence point does not vary at all, because it is prescribed [REG-R27].
10. **Waiver of premium.** **No variation on the standard form** — 장해지급률 합산 50% 이상,
    from any cause, at eight carriers in identical words [S1] [S2] [S6] [S8] [S9] [S10] [S11]
    [S12]. The variation is in the *optional* riders: absent at five of nine, a five-way
    diagnosis-triggered rider at one [S12], a W/S 유형 split at another [S17] [S18], and a
    narrowing to accident alone on simplified-issue forms [S17] [S18].
11. **재해사망 uplift.** Present at two of nine, and at both as a **product 형 rather than a
    rider** [S6] [S10]; one of the two sells only the uplifted form to female lives [S6].
12. **Acceleration.** The 선지급서비스특약 is present at every carrier whose full documents
    were retrieved, and its **terms do not vary** — 12 months, 50% of the sum assured
    aggregated to ₩50,000,000, 100% up to ₩10,000,000, discounted at the 평균공시이율 — with
    the single exception of a carrier that narrows the trigger to six months **for 정기보험
    specifically** [S2] [S10] [S12] [S17].
13. **Early-duration surrender-value shape — the widest cross-carrier variation in the
    product.** Every carrier but one pays nothing for a full year and then jumps: 0.0% at 1년
    and 20–32% at 2년 [S6] [S8] [S9] [S12]. One pays **9.5% at six months, 24.8% at nine and
    32.5% at one year** [S11]. Two others pay 4.0% at one year [S10] and 0.0% [S9]. That is a
    difference in 해약공제 amortisation within a common seven-year statutory window [REG-R19],
    not a difference in reserve, and any calibration of the amortisation must say which shape
    it is reproducing.
14. **Distribution and price.** Every CM (online) product in the disclosure has a
    보험가격지수 between 72% and 101%; every 대면 (face-to-face) retail product between 104%
    and 175%; the extreme values in the whole table are **51.6%** for one carrier's
    슈퍼건강체 form and **239.1%** for a simplified-issue product's female row [S4] [S6]. The
    index is computed against a 참조순보험료 that does not know about preferred underwriting,
    which is why a preferred class can read below 60%.
15. **What does not vary, and may not be altered by a composite.** Seven things are identical
    at every carrier examined and are the product's fixed spine rather than choices: (i) the
    benefit is the 보험가입금액 on death and nothing else, and payment terminates the contract
    [S1] [S2] [S8] [S10] [S11] [S12]; (ii) the suicide bar is **2년** from the 보장개시일,
    restarting on 부활 and never on renewal [S1] [S2] [S3] [S6] [S8] [S10] [S11] [S13] [S17];
    (iii) the exclusion list is the three intent limbs of 상법 제659조 / 제732조의2 and
    contains no negligence, war, aviation or hazardous-pursuit limb [S2] [REG-R49] [REG-R50];
    (iv) the premium waiver triggers on a **50%-plus 장해지급률** from any cause and waives
    future premiums only [S1] [S2] [S6] [S8] [S9] [S10] [S11] [S12]; (v) the 사기 취소 window
    is **5년** [S1] [S2] [S6] [S8] [S10] [S11] [S17]; (vi) every product is **무배당**, at all
    45 disclosed products [S4] [S2 제35조]; and (vii) the surrender value is 순보험료식
    계약자적립액 less the 해약공제액, capped by 별표 14 [REG-R20], floored at zero [REG-R19],
    and runs to **exactly zero at maturity** on every 순수보장형 curve published [S6] [S8]
    [S9] [S10] [S12]. A composite may choose among items 1–14; it may not alter these seven
    and still be describing the Korean product.

---

## Regulatory context

**Classification and licensing.** 정기보험 is written under 보험업법 제4조제1항제1호 as
생명보험, and only a 생명보험회사 may write it; every one of the fifteen carriers in the
disclosure is one [REG-R1] [S4]. The 제3보험 category of 제4조제1항제3호 — 상해보험,
질병보험, 간병보험 — is the boundary four other `krlib` products live on, and the 재해사망
variant of this product does **not** cross it [REG-R1] [R1] [R2].

**The filing, and what it means for provenance.** A Korean product filing is three documents
— 「사업방법서, 보험약관, 보험료 및 해약환급금의 산출방법서」 — under 보험업법 제5조제3호, and
제127조 makes prior notification to the FSC the exception rather than the rule [REG-R2]. The
**산출방법서** is where the 예정이율, the 예정위험률, the 예정사업비율 and the surrender-value
formula actually live, and it is **not published**; the 약관, the 상품요약서 and the 공시
disclosures are. 감독규정 제7-64조 lists its five mandatory contents, including — for a
contract longer than three years, which must use **현금흐름방식** (cash-flow pricing) — an
analysis of premium adequacy on **최적기초율** with projected cash flows, and a comparison
against the 표준해약공제액 at the 기준연령 요건 wherever the acquisition cost exceeds it
[REG-R18]. **That is the regulatory use of a liability cash-flow model in Korea, and it is
the shape this product's projection takes.** Every pricing-basis parameter here is
consequently **[std]** and every contractual parameter is sourced — the same position
`jplib` reaches from 保険業法第4条 and for the same reason.

**Product design.** 감독규정 제7-60조 constrains a life product's design; two of its limbs
touch this one. 제9호 requires the death benefit to be **at least cumulative premiums paid**,
except after annuity payments have begun and **except where the premium-paying period ends at
age 80 or below** [REG-R16]. On the representative contract the exception applies and the
constraint is slack in any case — ₩100,000,000 against ₩3,619,200 of premiums over twenty
years [S12] — but it binds directly on the 만기환급형's long-dated 세만기 cells, and it is
part of why a Korean 만기환급형 returns exactly 100% of premiums and not less. 제8호's rule
that a contract must not be extinguished while the risk it covers remains effective is the
rule behind the Korean cancer and CI designs that continue after a diagnosis payment; it does
not bite here, death being the terminating event [REG-R16].

**Surrender values.** 감독규정 제7-66조 governs, and is the article this library computes
against rather than cites past. 제1항제1호 sets the value as 계약자적립액 less the 해약공제액
with a **floor of zero**; 제1항제2호 sets the **해약공제기간 at the payment or acquisition-cost
period capped at seven years**; 제1항제3호 sets the deduction at the 별표 14 표준해약공제액;
제1항제4호 accrues the 계약자적립액 **monthly before 납입완료 and daily afterwards**; and
제5항 requires the 미경과보험료 to be added on termination [REG-R19]. 별표 14 supplies the cap
itself and its seven notes [REG-R20]; 별표 15 defines the 보험가입금액 that enters it, and its
제3호 — 「일반사망을 보장하는 보장성보험은 일반사망보험금으로 한다」 — makes the term product
the *base case* of the whole schedule, the one against which a 제3보험 product's notional sum
assured is scaled by a ratio of risk premiums under 제9호 [REG-R21]. **The cap is public and
has a formula, which is the sharpest single difference from the US and UK libraries.**
제7-66조제4항 is the 무해지 permission and its 환급률 cap [REG-R19] [REG-R28].

**Lapse assumptions are supervised, and this product's are visibly so.** The 2024 IFRS17
계리가정 가이드라인 makes a **로그-선형 model converging to 0.1%** the principle model for
무·저해지 lapse, sets a post-완납 ultimate of **0.8%**, closes the list of permitted
alternatives, and conditions any departure on disclosure in the audit report and the
management disclosure of the difference from the principle model in **CSM, best-estimate
liability, K-ICS ratio and net income**, quarterly reporting to the FSS and exposure to
on-site inspection [REG-R27]. Its 2021 predecessor had already imposed a design rule —
「해지환급금 수준이 낮으면(10%, 50%) 해지율을 더 낮게(0.2%, 1%) 적용」 and 「보험료 납입중
해지율은 기간이 경과할수록 하락」 [R12] — and the carriers' disclosed 적용해지율 are visibly
what that rule produces (Premiums, footnote 14). The 2019–2020 measures behind them defined
the form as 「보험료 산출 또는 보험금 산출시 **해지율을 사용한 보험**」 — an
assumption-driven class, not a contract-driven one — and recorded that a 무해지 contract
**cannot support a policy loan during the payment period** [REG-R28].

**Prudential and accounting.** Korea has run **K-IFRS 제1117호** and **K-ICS** together since
2023-01-01 [REG-R60] [REG-R13] [REG-R14], and on top of them a **해약환급금준비금**
(*haeyak hwangeupgeum junbigeum*, surrender value reserve) — a company-level appropriation
inside 이익잉여금 whose purpose is to stop an IFRS 17 balance sheet distributing earnings
that the contractual surrender-value floor would later demand [REG-R11]. It has no
counterpart in any other library here, and it is a distributable-earnings device rather than
a solvency device. The K-ICS 요구자본 rose from ₩67.9조 under RBC at 2022-12-31 to ₩118.9조 at
2024-09-30, and the industry ratio after 경과조치 stood at 210.8% (생명보험 201.4%) at
2025-09-30 against a regulatory minimum of 100% [REG-R30]. The **대량해지위험** shock a
protection contract carries under the standard formula — 25% immediate lapse on a
보장성보험, with a **+25%p** or **× (1 − 40%)** adjustment on a 저해지환급형 비고환급형
depending on whether the shock reduces or increases net assets — is known only at second
hand and is [unverified] here [REG-R26] [REG-R36]. `krlib` **computes none of these.**
This product projects gross best-estimate liability cash flows; the 책임준비금 [REG-R3]
[REG-R10], the 해약환급금준비금 [REG-R11], the CSM and risk adjustment [REG-R60] and the
K-ICS 요구자본 [REG-R13] are cited and left to a layer that consumes the cash flows.

**The valuation and pricing table, and why the shipped table is [std].** The industry table
is the **경험생명표**, prepared by 보험개발원 every five years from life-insurance
policyholder statistics; the current edition is the **제10회**, applied from **April 2024**,
and its headline outputs are public — 평균수명 male 86.3, female 90.7; 65세 기대여명 male
23.7, female 27.1, retrieved through a trade newspaper rather than through 보험개발원
itself [REG-R33]. **The table itself is not published**, and no numeric
경험생명표 or 참조순보험요율 was retrievable from any public source [REG-R34] [R19] [R20].
That is the sharpest contrast in this library with `jplib`, whose 標準生命表2018 is a free
public PDF with `qx` by single year of age. What *is* public is the 국가데이터처 완전생명표 —
2024 기대수명 83.7 overall, 80.8 male, 86.6 female; 65세 기대여명 19.5 and 23.7 [REG-R38] —
and the carriers' three-point 예정 경험사망률 disclosures. `Term_KR_S` therefore ships a
`mort_table.csv` that is a **[std] construction** with a `provenance` column on every row,
anchored on the three-point disclosures because they are *pricing* rates for *this product*
at *these ages* from seven carriers, and graduated against the public national table.

**Conduct.** The 표준약관 [REG-R25] is the source of every contractual mechanic in this
document that is not carrier-specific — 보험나이, 청약철회, 품질보증해지, 계약 전 알릴 의무,
사기, 납입최고, 부활, 해약환급금, 보험계약대출, 장해분류표 — and the retrieved carrier 약관
[S2] reproduces it almost article for article, which is why a single 약관 could be read in
full and treated as representative. The contract itself is governed by 상법 제4편, which is
**one-way mandatory** under 제663조: 제731조 (written consent), 제732조 (voidness under 15),
제732조의2 (gross negligence preserved), 제651조 (1개월 / 3년 rescission), 제655조 (the
causation defence) and 제662조 (three-year prescription) [REG-R49] [REG-R50]. 금융소비자보호법
제46조 supplies the cooling-off right [REG-R51] and 제47조 the 위법계약의 해지 [S2 제30조의2]
[REG-R25 제29조의2](#krlib-reg-r25). On insurer failure, 예금자보호법 시행령 제18조제7항 protects claims to
**₩100,000,000 per person per
bucket** — with 사고보험금 in a separate bucket from 해약환급금 and 기타지급금, so a
₩100,000,000 term policy is protected in full on the claim side — and **corporate
policyholders are not protected at all**, which bears directly on the 경영인정기보험 market
[REG-R52] [REG-R32] [S3] [S11] [S13].

**Tax.** A premium on a 보장성보험 attracts a **세액공제 (*seaek gongje*, tax credit), not a
deduction**: 소득세법 제59조의4제1항 gives 12% of the premium — 15% for a
장애인전용보장성보험 — with each basket capped at **₩1,000,000 a year**, so the maximum
annual benefit on an ordinary 정기보험 is **₩120,000** and on a 장애인전용 policy
**₩150,000** [REG-R57] [R8]. The cap is on the **premium**, not on the credit, and the anchor
cell's annual premium of ₩180,960 is **18% of it**, so the whole premium attracts relief and
the credit is 12% of it — **₩21,715 a year**. The basket binds only where a policyholder's
보장성 premiums across every such policy together exceed ₩1,000,000. The structural
difference from Japan is therefore the *form* of the relief rather than its reach: a Korean
세액공제 is a flat 12% credit on the premium, where the Japanese 生命保険料控除 is a deduction
whose value depends on the marginal rate. The 장애인전용보험전환특약 present at every carrier
exists precisely to move a policy into the 15% basket [S1] [S10] [S11] [S12] [S17]. The
qualifying test — maturity value not exceeding premiums paid — is the **same economic test**
감독규정 제1-2조제3호 uses to define a 보장성보험, so tax law and supervisory law draw the line
in the same place [REG-R9] [REG-R57]. Death-benefit taxation turns on the 계약자 / 피보험자
/ 수익자 triangle: 상속세 및 증여세법 제8조제1항 treats a benefit received on the deceased's
death under a policy **of which the deceased was the 계약자** as estate property, 제8조제2항
extends that to a policy the deceased in substance paid for, and 제34조 makes a benefit
attributable to another's premiums a **gift** to the beneficiary [REG-R59]. **No Korean
carrier document in this set addresses that triangle**, unlike the Japanese carrier booklet
`jplib` cites, and no 국세청 page was retrieved; the treatment above rests on the statute
alone and no numeric rate or threshold is asserted. `krlib` models contractual cash flows
and not the policyholder's tax position.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-term_life-r1
[R12]: #krlib-term_life-r12
[R16]: #krlib-term_life-r16
[R18]: #krlib-term_life-r18
[R19]: #krlib-term_life-r19
[R2]: #krlib-term_life-r2
[R20]: #krlib-term_life-r20
[R3]: #krlib-term_life-r3
[R4]: #krlib-term_life-r4
[R6]: #krlib-term_life-r6
[R8]: #krlib-term_life-r8
[R9]: #krlib-term_life-r9
[REG-R1]: #krlib-reg-r1
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R14]: #krlib-reg-r14
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R30]: #krlib-reg-r30
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R46]: #krlib-reg-r46
[REG-R49]: #krlib-reg-r49
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R57]: #krlib-reg-r57
[REG-R59]: #krlib-reg-r59
[REG-R60]: #krlib-reg-r60
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
