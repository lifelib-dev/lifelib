# Product Specification

**Status:** Draft, 2026-09-03 (every cited source accessed 2026-09-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modelling of a Korean **children's insurance (어린이보험, *eorini
boheom*)** contract — a fixed-benefit (정액, *jeongaek*) 제3보험 (*je-sam boheom*,
third-sector) policy written on a child, very often **before the child is born**, running from
birth to a 100세 만기 (*mangi*, expiry), and consisting of a small accidental-disability basic
contract carrying a very large bundle of riders. It describes **no single insurer's contract**,
and it must not be read as one.

Facts carrying a source tag — [S#] (primary product documents: 보험약관 (*boheom yakgwan*,
policy conditions), 상품요약서 (*sangpum yoyakseo*, the statutory pre-contract product
summary), and the 손해보험협회 comparison-disclosure board) and [R#] (product-specific
supervisory, statutory and research references), both numbered per `_research/child.md` and
resolved in `sources.md` in this directory (numbering frozen, never renumbered), and [REG-R#]
(the cross-product reference library `references/regulatory-and-actuarial-references.md`, whose
own R-numbering is distinct and also frozen) — name the document the claim was read from.
Values marked **[std]** are standardizations introduced for the reference implementation; each
[std] row carries a numbered footnote giving the rationale and, where the research file
brackets it, the range observed across insurers. Claims no retrieved document could confirm are
flagged [unverified].

The composite is drawn from **eleven carriers**. Five current 상품요약서 from five 손해보험
(non-life) writers give the benefit menus, the issue-age grids, the 면책기간 matrix and three
complete cash-value tables [S2] [S3] [S4] [S5] [S6]; a 2019 상품요약서 from the same line as
[S3] gives the pre-2023 issue ages, the graded 무해지 scale and the only **published pricing
lapse rates and the only published incidence rate** in the whole file [S1]; three 약관 — two
생명보험 and one 손해보험 — give the 태아가입특칙 verbatim, the 생명보험 form of the premium
waiver and a pure 비갱신 무해지 wording [S8] [S9] [S10] [S12]; one 약관 gives the 갱신형
architecture and the 보험나이 article with its worked example [S7]; and the 손해보험협회's
regulated comparison board supplies **41 products from 10 carriers** with their published
premiums, 예정이율, 공시이율, 최저보증이율 and 보험가격지수 [S11]. Two documents could not be
used — a 생명보험 약관 whose CID-keyed fonts defeated extraction [S14] and a product page whose
two fetches returned mutually contradictory renderings [S15] — and a third is used only as a
marker of [unverified] figures [S16]. Company and branded product names appear only in
`sources.md` and in `_research/child.md`.

**Deltas against the fixed-benefit 제3보험 chassis.** The [cancer specification
(암보험)](../cancer/product-spec.md) is `krlib`'s 정액 제3보험 chassis: diagnosis-triggered
lump sums on a tier ladder keyed to the KCD, a 90-day 면책기간 whose breach makes the affected
cover void, a 감액기간 on top of it, a 유사암 reduced tier, a premium waiver correlated with
the diagnosis benefit, and a contract with no death benefit that pays the 계약자적립액
(*gyeyakja jeongnipaek*, the policyholder's account balance) on a death it does not cover.
`Child_KR_S` inherits all six and changes six things. Three of them have no counterpart
anywhere in this repository.

1. **태아가입 (*taea gaip*, foetal enrolment): the contract is written before the insured
   exists.** A 태아 has no legal personality and cannot be the 피보험자 of an 인보험 contract,
   so the 태아가입특칙 makes the foetus the insured **at birth** [S8 제54조] [R3]. Cover
   attaches at birth and not at the 계약일 — sixteen insurers were ordered in 2016 to stop
   advertising otherwise [R2] — the 계약나이 is fixed at 0 at the 계약일 [S8 제60조], the
   contract is **priced male** because the sex is unknown and trued up after delivery
   [R3] [S8], and if the pregnancy ends in 유산 or 사산 the contract is **무효** and every
   premium is returned [S8 제56조]. The projection opens on a life that does not yet exist: its
   first months carry premium income, a void decrement and a short pre-birth benefit term, but
   no mortality and no morbidity on the insured at all.
2. **보험료 납입면제 on the 계약자 (*gyeyakja*, policyholder): a premium-waiver decrement on a
   life who is not the insured.** On the 생명보험 form the waiver fires on the child's cancer
   diagnosis or 50% disability **or on the 계약자's own death or 50% disability**, in one
   clause [S10 제22조]; it works because that wording makes the 피보험자 of the contract
   「계약자와 가입자녀」 — the policyholder is himself an insured [S10 제3조]. On the 손해보험
   form the same economics arrive as a compulsory 부양자 death rider written on the parent's
   own life, obligatory on any 태아 contract [S5] [S11]. Either way the model carries **two
   decrement lives**, and the premium stream stops on the earlier of two events drawn from two
   different mortality tables.
3. **The 면책기간 is disapplied below 보험나이 15, and entirely on a 태아 contract.** The
   90-day cancer waiting period that defines the chassis was removed for 어린이보험 in 2006,
   there being no evidence of anti-selection or of a 위험률차손 at child ages [R5]; current
   wordings implement it as 「최초계약과 부활계약의 면책기간은 **보험나이 15세 이상인 경우에만
   적용**」 [S3], and a 태아가입용 rider has 「면책기간 없음」 at all [S3]. The chassis's
   sharpest anti-selection control is switched off for the first fifteen years of a
   hundred-year contract.
4. **There is no 감액기간, and on a 태아 contract there may not be one.** The market has moved
   to 감액없음 and prints the word in the benefit names [S1] [S3] [S11]; where a 감액 survives
   it is a first-year 50% [S6] [S11]. And a supervisory 변경권고 of 2015 removed the 감액 for
   contracts written while the insured was a foetus, across 17 carriers and 56 products, with
   the before-and-after wording set out side by side [R2].
5. **No death benefit below 만 15세, by statute rather than by design.** `Cancer_KR_S` has no
   death benefit because the composite chose not to carry one; `Child_KR_S` may not have one.
   상법 제732조 makes a contract on the death of a person under 15 **void**, and the 표준약관
   restates it at 제19조제2호 with an express refusal to extend the age-correction saving to it
   [R7] [REG-R50] [REG-R25]. 제739조 disapplies 제732조 to 상해보험, so an accidental-death
   cover on a child is lawful, but the market does not write one below 15 [S1] [S4] [S11].
6. **The benefit is a bundle, not a ladder.** The basic contract is a 상해후유장해 (accidental
   residual-disability) cover paying **보험가입금액 × 장해지급률** on a continuous percentage
   scale [S1] [S2] [S4] [S5] [S11]; the cancer, cerebrovascular and cardiac diagnosis benefits
   the chassis is built around are three riders among more than a hundred [R5]. Two whole rider
   blocks are written **on other lives** — the 부양자 stack on the parent and the 임신·출산질환
   stack on the mother — and 가족일상생활배상책임 is a **third-party liability** cover that
   only a non-life licence may attach [R5] [S5].

The horizon is the other structural fact. At 계약나이 0 to a 100세 만기 the projection runs
**1,200 monthly periods**, the longest in `krlib`, and the premium is paid over the first 240
of them. A child policy is a seventy-to-hundred-year guarantee on a bundled rider stack whose
morbidity has barely begun, written on a life whose sex is not yet known.

---

## Product overview and market role

### What an 어린이보험 is, and the two licences that write it

The industry disclosure board's own definition is 「태아·어린이를 포함한 성장기 자녀에게 발생할
수 있는 질병과 상해위험을 보장하는 보험」 [R12]. The supervisor's older and fuller formulation
adds the liability limb and the issue-age band: 「자녀의 성장 과정 중 발생할 수 있는
질병·상해로 인한 의료비와 자녀의 일상생활 중 발생하는 배상책임 등을 보장하는 보험상품(가입연령
: 0세~15세)」 [R2].

It is 제3보험 business — 상해보험 and 질병보험 together, under 보험업법 제2조제1호다목 and
제4조제1항제3호 — and 제4조제3항's deeming provision makes the class writable by a life or a
non-life insurer alike [REG-R1]. In this product the two licences have **not** converged, and
that is the first thing a specification has to get right. 보험연구원 is direct: 「어린이 보장성
상품은 손해보험회사를 중심으로 판매되고 있으며, 생명보험회사는 변액과 연금의 강점을 내세워
어린이 저축성 상품 시장을 선점」, and attributes the split to the fact that only a non-life
insurer may attach **배상책임담보** and **비용담보** [R5]. The comparison board carries **41
products from 10 non-life carriers** [S11]; there is no 생명보험 counterpart to it in this
file, and that absence is the largest single gap behind this document. The composite is
therefore drafted as a **non-life carrier's 장기손해보험**, which 감독규정 제7-61조 designs
identically to a 제3보험 contract [REG-R17], with one deliberate exception: the **premium
waiver is taken from the 생명보험 form** [S10 제22조], the only retrieved wording in which the
계약자's death is a contractual event of the main contract rather than the benefit of a
separate rider.

Structurally the contract is a **small 기본계약 plus a very large 특별약관 stack**. At every
non-life carrier examined the 기본계약 is a 상해후유장해 cover paying 가입금액 × 장해지급률
[S1] [S2] [S4] [S5] [S11]; everything else — cancer diagnosis, cerebrovascular and ischaemic
heart diagnosis, surgery, hospital cash, fracture, burn, liability, the foetal covers, the
parent covers, the mother covers — is a rider. The rider count is a competitive strategy: by
2018 a child policy carried 「100여개 이상의 질병 및 상해사고에 대한 보장 담보」 [R5], and
[S2]'s eligibility tables run to roughly forty pages. Naming is not standardised — 어린이보험,
자녀보험, 아이보험, 태아보험 and branded names all appear — and the 2023 supervisory
restriction bites on the **name** rather than the design [R1], so a product sold at older issue
ages may be renamed rather than restructured.

### 태아보험 is not a product — it is an 어린이보험 with a 특칙 attached

The 태아보험 (*taea boheom*) of ordinary Korean speech has no separate legal existence. The
supervisor says so:

> 법규 상 '태아보험'이라는 별도의 보험상품은 없으나, 어린이보험에 태아가입특약(胎兒加入
> 特約)이 첨부되어 출생 전 태아 상태에서 보험가입이 가능한 상품을 실무적으로 '태아보험'
> 으로 지칭하고 있음
> \* 태아는 법적으로 인격(人格)을 갖지 못하므로 인보험의 보호대상이 될 수 없음. 따라서
> 태아의 출생을 조건으로 하는 '태아가입특약'을 통해 태아를 대상으로 한 보험계약을 체결

and, in one line, 「태아보험 = 어린이보험 + 출생시 위험보장」 [R3].

It is not a fringe variant. In FY2007 **335,135 of 1,622,639 new child contracts — 20.7% — were
written in utero**, and about the same fraction of premium [R3]. The 태아가입특약 was
introduced in 2000 and 보험연구원 calls it the single largest contributor to the product's
growth [R5]. Every current 상품요약서 retrieved offers it, with 가입나이 written as 「태아」 at
the head of the issue-age grid [S2] [S3] [S4] [S5] [S6].

### The market: size, share and the shape of the in-force book

**Current size, from a primary supervisory document.** 어린이보험 annual premium is
**₩9.4조원**, against about **₩42.7조원** for all 보장성 인보험, both as at 2026-03 [R6]. That
puts 어린이보험 at roughly **22% of all Korean protection personal-lines premium** — a
remarkable share for a product sold to a cohort that is shrinking every year.

**Historic size, and the reversal of the licence split** [R3], 수입보험료 in 억원: 생명보험
23,947 (FY05) → 24,888 → 23,995 against 손해보험 3,936 → 5,888 → **8,406**, on FY07 신계약
583,888 (생명, of which 138,965 태아) and 1,038,751 (손해, 196,170 태아).

| | FY05 | FY06 | FY07 | 신계약건수 FY07 (태아가입) |
|---|---|---|---|---|
| 생명보험 | 23,947 | 24,888 | 23,995 | 583,888 (138,965) |
| 손해보험 | 3,936 | 5,888 | 8,406 | 1,038,751 (196,170) |
| 합계 | 27,883 | 30,776 | 32,401 | 1,622,639 (335,135) |

In FY07 the market was ₩3.24조원 and **74% of it was 생명보험**; the 손해보험 side then doubled
in two years while the 생명보험 side was flat, which is the 굿앤굿어린이CI보험 effect [R5].
Today the position is reversed. **In-force, 2013–2015**, sourced by the FSS to 보험개발원:
보유계약 1,141만건 (2013.4–12) → 1,182만건 (2014) → 1,162만건 (2015 잠정), with 수입보험료
₩33,385억 → ₩45,611억 → ₩44,906억 and 신계약 88만건 → 127만건 → 123만건 against 출생자수 of
43.7만 / 43.5만 / 43.9만 [R2]. New child contracts ran at roughly **three times the birth
count** — which is what a multi-rider, multi-contract product looks like in a count statistic,
and a warning that "contracts" in Korean insurance statistics are not "insured children".

**Growth against a falling birth rate.** 보험연구원 predicted in 2018 that 「출산율 저하에 따라
15세 미만 인구 수가 지속적으로 줄어들어 어린이보험의 시장규모가 앞으로 크게 성장할 가능성은
낮다」 [R5] and was wrong: ₩3.24조원 (FY07) [R3] and ₩4.49조원 (2015) [R2] became ₩9.4조원 by
2026 [R6]. The mechanism is the one [R5] itself identified — the **term extension**. A
100세만기 policy written at age 0 collects premium for twenty years and stays in force for a
hundred, so the in-force premium grows even as the cohort shrinks. That is also the whole of
the product's IFRS 17 problem, and it is why this reference model runs 1,200 periods. **Loss
ratio.** [R5], in 2018: 「어린이보험의 손해율은 보험회사 평균 손해율(약 80% 수준) 미만인 것으로
알려져 있어 우려할 만한 수준은 아니지만, 이러한 담보경쟁은 향후 어린이보험의 손해율이 높아질
가능성이 매우 높다」. Two documented deteriorations exist: the 2010 outpatient riders, whose
frequent infant colds and fevers were claimed together with the then-attachable 실손 rider, and
the 2013 requirement to pay neonatal claims on the diagnosis name rather than the KCD code,
which ended refusals of 뇌출혈 claims coded **P52** and raised frequency sharply [R5]. **No
current loss-ratio figure for 어린이보험 was retrieved** and none is asserted here.

### How the product reached 100세 만기, and the 2023 supervisory action

The line is old and the dates are known [R5] unless marked. **1958-07**: 진학보험, Korea's
first education endowment; 교육보험 dominates the individual market into the 1980s and declines
from 1990 as tuition inflation outruns the benefit. **1997**: the first true 어린이 보장성
상품, at 가입연령 2~14세 and 15/20년 or 18/22세만기, with a 사망위로금 that returned premiums
on death before 15. **2000**: the 태아가입특약. **2003** and **2004-07**: the first child CI
products, the second of which [R5] calls the best-selling child policy ever written in Korea,
at 주피보험자 태아~15세, 피부양자 20~50세, 보험기간 15/18/20세만기. **2005**: high-cost
critical-illness benefits. **2006**: the 90-day cancer waiting period is removed for
어린이보험. **2010**: outpatient riders, and their loss experience. **2011**: the move to
**100세 만기**, after which a hundred-year term becomes the norm and adult-disease covers are
bolted on for the post-30 segment. **2012-10-01**: all foetuses of a multiple pregnancy become
insurable [R4]. **2013-09**: the P-code decision. **2015-06-17 → 2016-04**: the 감액 for foetal
contracts is removed [R2]. **2016-07**: sixteen carriers are ordered to stop advertising cover
before birth [R2].

**2023-07-19** is the datable intervention and it is easy to get wrong. It is a **감독행정**
(supervisory administration), not a rule change, announced in a 보도자료 distributed 2023-07-19
for publication on 2023-07-20, with existing products to be amended by the end of **2023-08**
[R1]. The 어린이보험 section reads, verbatim:

> **2 어린이보험**
> □ (현황 및 문제점) 가입연령을 35세까지 확대함에 따라 어린이 특화 상품에 성인이
> 가입하는 등 불합리한 상품 판매 심화
> ◦ 또한, 어린이에게 발생빈도가 극히 희박한 뇌졸중, 급성심근경색 등 성인질환 담보를
> 불필요하게 부가
> □ (추진방안) 최대 가입연령이 15세를 초과하는 경우 '어린이(자녀)보험' 등 소비자 오인
> 소지가 있는 상품명 사용 제한

Three things follow. First, **the measure restricts the product name, not the issue age**; a
carrier remains free to sell above 15, it may not call the result an 어린이보험. In practice
every carrier cut the age, and the current 상품요약서 show 태아~15세 [S2] [S4]. Second, the
second limb is a **supervisory statement about the morbidity basis**: the adult-disease riders
on a 100세만기 child policy are priced on an exposure that barely exists for the first three
decades of the term. Third, the framing is prudential as well as conduct — the release names
「보험계약마진(CSM) 증대 등을 위한 불합리한 보험상품 개발·판매」 as the cause, and flags that
the 무·저해지 lapse assumption would be dealt with separately 「금년 중」, which it was
[R11] [REG-R27].

The age creep itself, evidenced within two product lines:

| Product line | Edition | 가입나이 (100세만기 forms) | Source |
|---|---|---|---|
| Carrier A, 어린이보험 1910 | 2019-10 | 0 ~ 30세 | [S1] |
| Carrier B, 다이렉트 어린이보험 (Hi2204) | 2022-04 | 0 ~ 30세 | [S7] |
| Carrier B, 어린이종합보험Q (Hi2607) | 2026-07 | 태아 ~ 15세 | [S2] |
| Carrier C, 자녀보험Plus (26.07) | 2026-07 | 태아, 0 ~ 15세 | [S4] |

The **35** figure named in [R1] is not visible in any retrieved product document; both
pre-action products stop at 30, and that two carriers went to 35 in 2023 rests on news reports
and is **[unverified]**.

### What is public, what is not, and what that forces

The data position for this product is worse than for `Cancer_KR_S` and it must be stated at the
outset, because it decides which parameters below can be sourced and which cannot.

**Public and used.** The 손해보험협회's regulated comparison board publishes, for every
non-life 어린이보험 on sale, the product name, the channel, the **보장부분 적용이율**, the
**적립부분 공시이율** and its **최저보증이율**, a specimen male and female monthly premium on a
standardised basis, the **보험가격지수**, and a link to the 상품요약서 [S11]. The standardised
basis is printed on the board and is the only specification of a Korean child policy the market
itself publishes [R12]. Every 상품요약서 publishes a complete surrender-value grid on a named
specimen contract [S1] [S2] [S3] [S4].

**Partly public, and the consequence.** 보험개발원 files the **참조순보험요율** with the FSC
under 보험업법 제176조제4항 and there is no general obligation to publish it [REG-R4], and on
the **life** side nothing of it reaches the public. On the **장기손해보험** side — which is the
chassis this product is written on — 제176조제9항 permits publication where policyholder
protection requires it, and 보험개발원 **does** publish a dated display carrying, by age and
sex, a 「기타피부암 및 갑상선암 이외의 암 발생률」 grid on the insured definition that excludes
C44 and C73, a 질병입원율 grid stated in expected days per life-year, and 후유장해 rates
[REG-R61]. Its published age grid reaches **연령 0 and 10**, so it is not true that no Korean
child incidence rate exists in public, and this document does not say so. Two things are
nonetheless true and both bind here. **This product's own research pass never opened that
display** — it was reached in the `cancer` and `indemnity_medical` passes on the same day, and
[REG-R61] records the omission — so nothing in `incidence_table.csv` was built off its values.
And a 참조순보험요율 is a **net premium rate carrying a safety loading, not a best estimate**
[REG-R9] [REG-R61], so adjusting one to a best-estimate basis would itself be a [std] step. The
**산출방법서** that holds each carrier's own 적용위험률 and 예정사업비율 remains an undisclosed
기초서류 [REG-R2], and the **경험생명표** is released only as summary statistics
[REG-R33] [REG-R34]. **Every incidence assumption in `Child_KR_S` is therefore still a [std]
construction and says so at the point of use** — but as a construction that has *not* been
reconciled to a published reference grid rather than as one for which no grid exists. The
direction of the gap is stated where it bites: on the general cancer tier the shipped
paediatric anchors sit at roughly **0.6 (male) and 0.5 (female) of the published rate at 연령 0
and 10**, while the adult anchors sit near or slightly above it, so the divergence has no
single sign and a later pass should re-base the rows rather than rescale them.

Three public anchors bound the construction, and only one of them is a rate: the **published
premium levels** on the [R12] basis (§*Premiums*), which bound the total; the **보험가격지수**,
which bounds the ratio of total premium to the sum of the 참조순보험료 and average expense
[S11] [REG-R22]; and exactly **one 적용위험률 published anywhere in this file** — 일반상해
후유장해 발생률(3~100%) at the 기본계약, 5세, 상해 1급: **남자 0.0001823, 여자 0.0001163**
[S1]. That single pair is the only observation of a Korean child morbidity rate in the whole
research file, and it is the calibration point for the basic contract's decrement in
`technical-notes.md`.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 어린이보험, **무배당** (*mubaedang*, non-participating), **정액** (fixed-benefit); a 상해후유장해 기본계약 with a bundled 특별약관 stack, plus a 태아 module, a 계약자 waiver module and rider blocks on the parent and the mother | [S1] [S2] [S4] [S5] [S11]; menu **[std]** (1) |
| Regulatory class | 제3보험상품 — 상해보험 and 질병보험 (보험업법 제2조제1호다목, 제4조제1항제3호), written as a **장기손해보험** to which 감독규정 제7-61조 applies the whole 제3보험 design rule | [REG-R1]; [REG-R17] |
| Written by | A **손해보험회사**; the composite adopts the **생명보험** wording of the premium waiver only | [R5]; [S10]; **[std]** (1) |
| 보장성 / 저축성 | **보장성보험** — the maturity value does not exceed premiums paid at the 기준연령 요건 (감독규정 제1-2조제3호) | [REG-R9]; [REG-R57] |
| Chassis | **비갱신형** on the core covers; **갱신형 blocks** on 가족일상생활배상책임 (3년만기) and named riders, renewing at attained age | [S2] [S3] [S12] vs [S7]; **[std]** (2) |
| Policy term (보험기간) | To the **100세 계약해당일**; no 만기환급금 on the protection part | [S1] [S2] [S3] [S5] [S6] [S11]; **[std]** (3) |
| Premium-paying period (보험료 납입기간) | **20년납** on the core covers; 전기납 on the 태아 module and on the 갱신형 blocks | [R12]; [S2] [S4]; **[std]** (4) |
| Issue age (가입나이) | **태아 ~ 보험나이 15세** | [S2] [S4] [S5] [S6]; [R1]; **[std]** (5) |
| Issue age, pre-2023 | **0 ~ 30세** on the 100세만기 forms — retained as a documented historic variant, not offered | [S1] [S7]; [R1] |
| Contractual age basis | **보험나이** (*boheom nai*, insurance age): 계약일 현재 만 나이 with a fraction under six months discarded and six months or more rounded up, incrementing at each 계약해당일. The 만 15세 nullity test uses **실제 만 나이** | [S7 제27조] [S8 제30조] [S12 제30조]; [REG-R25 제21조](#krlib-reg-r25); [R8] |
| Foetal age basis | **계약나이 0세** at the 계약일; the benefit-scale age runs **from the date of birth**; the 계약일 is moved back where birth falls more than six months after it | [S8 제58조·제60조·제61조] |
| Model age basis | **만나이** (age last birthday), offset from 보험나이 by up to six months | **[std]** (6) |
| Sum insured, 기본계약 | **₩100,000,000 (1억원)** of 상해후유장해, paid as 보험가입금액 × 장해지급률 | [R12]; [S11] |
| Lives basis | **Three lives.** The child is the 피보험자; the **계약자** (a parent) carries the waiver decrement; the **mother** carries the 임신·출산질환 block. All three are on one contract | [S2] [S5] [S10]; **[std]** (7) |
| 계약자 | A parent, **만 33세** at the 계약일, male | [S2]; **[std]** (7) |
| Sex of the insured | **Male at pricing on a 태아 contract**, since the sex is unknown at issue; trued up after delivery | [R3]; [S8]; **[std]** (8) |
| Underwriting | 계약 전 알릴 의무 questionnaire, no medical examination; a 태아 contract is additionally subject to a **gestational-week window** on the neonatal riders | [S5]; [REG-R25 제13조](#krlib-reg-r25) |
| Substandard terms | 특정 신체부위·질병 보장제한부 인수특약 | [S8] |
| 배당 | None — 무배당 | [S1]–[S6] [S11]; [REG-R12] |
| Death benefit | **None below 만 15세, by statute.** On death the **계약자적립액 + 미경과보험료** is paid and the contract ends | [R7]; [REG-R50 제732조](#krlib-reg-r50); [REG-R17 제7-63조제1항제1호](#krlib-reg-r17); [REG-R25 제22조](#krlib-reg-r25); [REG-R19 제7-66조제5항](#krlib-reg-r19); **[std]** (9) |
| 암보장개시일 | **제1회 보험료를 받은 때** while the insured is 보험나이 15 미만; the 91st day counting the 계약일 as day 1 from 보험나이 15; **no waiting period at all** on a 태아가입 cover | [S3]; [S11]; [R5]; **[std]** (10) |
| 감액기간 | **None** | [S1] [S3] [S11] vs [S6]; [R2]; **[std]** (11) |
| Surrender-value form | **표준형** base, with **해약환급금 미지급형 (납입기간 중 0%, 납입 후 50%)** as the switch | [S2] [S11]; [REG-R19 제7-66조제4항](#krlib-reg-r19); **[std]** (12) |
| **Anchor model cell (point_id 1)** | **태아가입**; 계약나이 0 at the 계약일, priced male; **birth at policy month 5**; 보험기간 to the 100세 계약해당일 (`t = 1200`); **20년납** (`t = 240`); 월납; 표준형; 계약자 male 만 33 with the waiver module on; 기본계약 상해후유장해 ₩100,000,000; the [R12] rider set at 질병후유장해 ₩10,000,000, 암진단비(유사암 제외) ₩10,000,000, 유사암진단비 ₩2,000,000, 뇌출혈진단비 ₩10,000,000, 급성심근경색증진단비 ₩10,000,000, 암·뇌출혈·급성심근경색증 수술비 ₩5,000,000 each, 상해·질병 입원일당 ₩40,000 per day to 180 days per stay, 골절진단비 ₩400,000, 화상진단비 ₩200,000, 가족일상생활배상책임 ₩100,000,000; 태아 module on to `t = 17`; office premium **₩31,000 per month to `t = 16`, ₩28,000 from `t = 17` to `t = 239`** | **[std]** (13) |

Footnotes to the [std] rows:

1. **The menu, and the licence.** No two retrieved products carry the same rider set and none
   could be reproduced in full — [S2]'s eligibility tables run to roughly forty pages and
   [S4]'s 상품요약서 to 207. What every retrieved non-life product shares is the **shape**, a
   상해후유장해 기본계약 paying 가입금액 × 장해지급률 with everything else a 특별약관
   [S1] [S2] [S4] [S5] [S11], and a **published standardised specification** of the compulsory
   covers exists on the comparison board [R12]. The composite takes [R12]'s specification
   rather than any one carrier's, because it is the only child-policy benefit menu the Korean
   market publishes and because every published premium in §*Premiums* is quoted on it. The
   contract is drafted non-life because the protection product is a non-life product [R5] and
   because the liability rider needs that licence; 감독규정 제7-61조 makes the design rules
   identical either way [REG-R17], so nothing turns on the licence except the waiver wording of
   footnote (14).
2. **비갱신형 with 갱신형 blocks inside it, which is what the market actually sells.** Both
   pure forms exist: one direct product is built end to end of 20년만기 / 30년만기 renewable
   blocks with ceilings written as `(100−보험기간)세` [S7], and one is a pure **비갱신 무해지**
   contract [S12]. Between them sits the dominant design — a 비갱신 core with a few 갱신형
   riders, of which 가족일상생활배상책임 is universally one, at a **3년만기** renewal [S2] and
   갱신형 at two more [S3] [S5]. The composite takes the mixed form because it is the majority
   and because it is the only one on which a level premium over a hundred-year term and a
   waiver that fires once coexist with a renewal mechanic the model must nevertheless carry
   (*Contractual mechanics*).
3. **100세 만기.** Observed maxima: 100세 at four carriers [S1] [S2] [S5] [S6] and **110세** at
   one [S4], the longest term found anywhere in this research; the full ladder at the
   archetypal product is 10세 / 20세 / 30세 / 80세 / 90세 / 100세만기 [S2]. 100세 is the modal
   maximum, the term on which every published premium and cash-value grid in this file is
   quoted [S11] [S2] [S1], and the term whose 2011 arrival made the product what it is [R5];
   110세 is a documented variant and adds no mechanic. There is **no 만기환급금** on the
   protection part — the published grids show the 표준형 at 16.0% of premiums paid at 95 years
   and the 미지급형 at nil [S2] — and the residual at maturity is the 적립부분, not a
   guaranteed benefit.
4. **20년납.** Observed on the 100세만기 forms: 10 / 15 / 20 / 25 / 30년납 at both current
   carriers [S2] [S4] and 10 / 20 / 25 / 30년납 in the pre-2023 generation [S1]. 20 years is
   the payment term the comparison board quotes every premium on [R12]; it is the
   **해약공제계수 cap** for a 보장성보험 in 감독규정 [별표 14], 「보험기간(최대 20년)」, and
   the basis on which the same schedule's note 3 forces the 연납순보험료 to be recomputed
   [REG-R20]; it puts 납입완료 at a known date, which is what makes the 무해지 step-up a cliff
   [S2]; and it leaves **eighty years of paid-up cover** on the anchor cell — four times the
   payment period, and the reason a child policy's IFRS 17 measurement is dominated by what
   happens long after the premium stops.
5. **가입나이 태아 ~ 15세.** The current envelope, from two 2026 상품요약서 [S2] [S4] and
   confirmed at two more [S5] [S6]. The full grid narrows the upper bound as the payment term
   lengthens — 30세만기 20년납 accepts to 9세 and 25년납 to 4세, the payment period not being
   allowed to outrun the term [S2] — and the composite carries the 100세만기 row, at which
   every payment term accepts to 15. **The bound is a supervisory artefact and is datable**:
   the pre-action generation of the same two lines accepted to 30 [S1] [S7], and the 2023
   감독행정 restricted the product name above 15 rather than the age itself [R1]. 15 is also
   where two other rules change sign — the 면책기간 switches on (footnote 10) and 상법 제732조
   stops voiding a death benefit (footnote 9) — so it is the most load-bearing age in the
   product.
6. **The two age bases, and the third one a foetal contract adds.** The contract ages on
   **보험나이**: 「계약일 현재 피보험자의 실제 만 나이를 기준으로 6개월 미만의 끝수는 버리고
   6개월 이상의 끝수는 1년으로 하여 계산하며, 이후 매년 계약해당일에 나이가 증가」, identical
   in both 표준약관 and reproduced verbatim by every carrier, with the worked example 생년월일
   1988-10-02 / 계약일 2014-04-13 ⇒ 25년 6월 11일 ⇒ **26세** [R8] [S7 제27조] [S8 제30조] [S12
   제30조] [REG-R25 제21조](#krlib-reg-r25). Because of the six-month rule 보험나이 differs from 만나이 for
   **roughly half of all issue dates**. `Child_KR_S` projects on **만나이**, because every
   decrement it could use — the 생명표 [REG-R38] [REG-R39], the 국가암등록통계 age bands
   [REG-R40] and the NHIS statistics [REG-R41] — is published on 만나이, and no source supplies
   the distribution of issue dates within a policy year a conversion would need. On a **태아**
   contract the offset is not an average but a **stated quantity**: 보험나이 runs ahead of
   만나이 by exactly the pre-birth period, which [S8 제61조] caps at six months, and which is
   **five months for the life of the contract** on the anchor cell (footnote 13).
7. **Three lives on one contract, and why the 계약자's age is 33.** The child is the 피보험자;
   the 부양자 block is written on the parent at issue ages 만15세 ~ (77−보험기간)세; the
   임신·출산질환 block is written on the mother at **20세 ~ 47세** for most riders, 20~39세 for
   출산전특정태아이상진단 and 20~40세 for the 융모막·양수검사 rider [S2]. The composite sets
   the 계약자 at 만 33, the **mid-point of the 20~47 band the mother-side riders themselves
   state** [S2] and the only sourced anchor for a parental age in this file; Korean statistics
   on mean age at first birth were not retrieved and are not relied on. The 계약자 is male so
   that the waiver decrement runs on the male table, which is the conservative direction; a
   female 계약자 is a model-point variant.
8. **The male-rate convention on a 태아 contract.** 「태아보험 가입시 태아의 성별을 구별하기가
   어려운 점 때문에, 일단 남자 아이를 기준으로 납입보험료가 산정되고 출산 후 성별대로 정산하는
   구조」 [R3], and a carrier's published 민원 case says the same [S8]. The composite adopts it
   and **does not model the true-up**, because the direction is no longer reliable: the current
   published tables show the female rate above the male at four carriers and below it at seven
   [S11], so a refund on the birth of a girl is a product-specific fact rather than a market
   rule (footnote 16).
9. **No death benefit, and what is paid instead.** 상법 제732조: 「15세미만자, 심신상실자 또는
   심신박약자의 사망을 보험사고로 한 보험계약은 무효로 한다」 [R7] [REG-R50], restated by the
   표준약관 at 제19조제2호 with 제19조제3호 refusing to extend the age-correction saving to it
   [R8] [REG-R25]. The design consequences are visible everywhere: 일반상해사망 is fixed only
   「기본계약 최초가입시 피보험자의 나이가 15세 이상인 경우」 [S1], one carrier writes it only
   at 만 15세 [S4], the board note reads 「15세이상 가입시 일반상해사망 특약 고정부가」 [S11],
   and the 생명보험 wording pays a 사망보험금 only 「만 15세 계약해당일 이후」 [S10 제21조].
   The supervisor states the general rule — 「피보험자의 사망시 사망보험금이 아니라
   **기납입보험료**가 지급됨」 [R3] — but the composite pays the **계약자적립액 plus the
   미경과보험료**, because that is what 감독규정 제7-63조제1항제1호 requires of a 제3보험
   contract on a death it does not cover [REG-R17], what 표준약관 제22조 implements [REG-R25],
   and what 상법 제736조 floors [REG-R50]. On a 무해지 contract inside the payment period that
   sum is close to nil — a real and uncomfortable feature of the form, stated rather than
   smoothed. **상법 제739조 disapplies 제732조 to 상해보험** [R7], so the market's uniform
   refusal to write accidental-death cover below 15 is more conservative than the statute
   requires; that reading is [unverified], no judgment on it having been retrieved.
10. **The waiting period, disapplied.** Two independent primary statements, from two carriers
    and two document types. A 상품요약서 footnote to the 면책기간 matrix: 「주1) 최초계약과
    부활계약의 면책기간은 **보험나이 15세 이상인 경우에만 적용**」 [S3]. A benefit definition
    on the comparison board: 「피보험자가 보장개시일(계약일로부터 90일이 지난날의 다음날,
    **계약일 현재 보험나이 15세 미만 피보험자의 경우 1회 보험료를 받은 때**) 이후에
    암(유사암제외)으로 진단확정시」 [S11]. The origin is 2006: 「암에 대한 위험률이 낮아 역선택
    우려가 있다거나 이로 인한 위험률차손이 크다는 근거가 없기 때문에 암 보장에 대한 90일 부담보
    기간이 삭제되었다」 [R5]. A 태아가입용 cover goes further and has 「면책기간 없음」 at all,
    including on the 10-day waits some infection and influenza riders carry [S3]. The composite
    implements all three limbs; the waiting periods that **do** survive are named at
    *Contractual mechanics*.
11. **No 감액기간.** The market has moved to 감액없음 and puts the word in the benefit names —
    암진단비(유사암제외)**(감액없음)**, 뇌혈관질환진단비**(감액없음)** — at five carriers
    [S1] [S3] [S11]. Where a 감액 survives it is a first-year 50%: one carrier publishes its
    암진단비 as 「1천만원(1년이내 50%지급)」 and its 항암방사선·약물치료비 as 「100만원(1년미만
    50%지급)」 [S6] [S11]; another applies 감액 only to dental benefits, at 25% or 50%
    「최초계약일부터 2년 경과시점 전일 이전」, with cancer at 「-」 throughout [S3]. The
    composite takes 감액없음 and carries `reduction_months` with observed values 0 and 12, so
    the 감액 machinery specified by `Cancer_KR_S` remains reachable. **A foetal contract may
    not be subject to 감액 at all**: the 2015 변경권고 inserted 「단, 피보험자가 보험가입 당시
    태아(胎兒)인 경우에는 보험금의 100%를 지급합니다」 across 17 carriers and 56 products, on
    the reasoning that 「태아는 보험가입시 역선택 가능성이 거의 없는데도」 [R2]; a current
    carrier confirms it still holds [S8].
12. **표준형 as the base, 무해지 as the switch — the opposite of `Cancer_KR_S`.** Every carrier
    on the board offers a 해약환급금 미지급형 beside the 표준형 [S11], and the 무·저해지 share
    of 보장성 초회보험료 ran 11.4% (2018) → 30.4% (2021) → 47.0% (2023) → **63.8%** (2024 H1)
    [R11] [REG-R27], so the suppressed form is where the market is and `Cancer_KR_S` ships it
    as its base. `Child_KR_S` deliberately ships the **표준형**. The 적립부분 credited at the
    **공시이율**, with its own floor and reset machinery, exists only there — the suppressed
    forms are 순수보장성 and show 「-」 for it on the board [S11] [S2]; the 표준형's surrender
    value **exceeds premiums paid from about year 30** on the published grid [S2], a shape no
    other `krlib` protection product produces and only a hundred-year term can; and shipping
    the two forms on two products lets a reader compare them inside one library without either
    model carrying both. The switch is specified at *Termination and values* and its premium
    ratio at footnote (17).
13. **The anchor cell, and why it is the foetal one.** `Cancer_KR_S` anchors on the 기준연령
    요건 of 감독규정 제1-2조제2호 — 남자 만 40세, 전기납, 월납 [REG-R9] — the cell at which the
    표준해약공제액 and 보험가입금액 computations are performed. **No child policy can be
    written at that cell**, so 제1-2조제2호's own fallback applies: the 기준연령 요건 is taken
    at the mid-point issue age and the longest available payment term [REG-R9]. That fallback
    governs the regulatory computations and is not the modelling anchor. The modelling anchor
    is the **태아 contract at 계약나이 0**, because 태아가입 and the 계약자 waiver are the two
    mechanics this product exists to demonstrate and a worked example exercising neither would
    be a worked example of `Cancer_KR_S`. **Birth at policy month 5** is [std]: the neonatal
    riders close at 임신 22주 [S5], so a contract written inside that window still has **at
    least** 4.1 months of gestation to run, and [S8 제61조] caps the pre-birth period at six
    months; five is between those two bounds and is a whole number of grid steps. The
    **premium is a model-point input** (footnote 16). A calibration cell is
    shipped alongside: **male, 보험나이 5, 표준형, no 태아 module, no 계약자 waiver**, at
    ₩27,000 a month, the cell every published premium in this file is quoted on [R12] [S11].

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | **Level** for the whole 납입기간 on the 비갱신 core; 무배당, so no dividend and no premium review. The 갱신형 blocks are recomputed at each renewal on the attained age and the rate basis then in force | [S1] [S2] [S11]; [S7 제29조]; [REG-R12] |
| Frequency (납입주기) | **월납**; 연납 offered; one product on the board is 일시납 | [S1] [S2] [S7] [S11]; **[std]** (15) |
| Anchor premium | **₩31,000 per month to `t = 16`; ₩28,000 from `t = 17` to `t = 239`** — being ₩27,000 of core 보장보험료, ₩1,000 for the 계약자 waiver module and ₩3,000 for the 태아 module over `t = 0..16` | **[std]** (16) |
| Calibration-cell premium | **₩27,000 per month**, male, 보험나이 5, 상해 1급, 100세만기 20년납, on the [R12] specification | published cluster [S11]; **[std]** (16) |
| Rating factors | 보험나이, sex, 보험가입금액 per cover, riders elected, 형 (표준형 / 미지급형), 납입기간, **상해급수** (the comparison basis is 상해 1급), 계약 전 알릴 의무 outcome | [R12]; [S1] [S2] [S11] |
| Rate structure | **Not published by any carrier.** A carrier's own 적용위험률 and 예정사업비율 live in the 산출방법서, an undisclosed 기초서류; the bureau's 참조순보험요율 is filed under 보험업법 제176조제4항 with no general publication obligation, though the **장기손해보험** display is published under 제176조제9항 and was not opened in this product's pass | [REG-R2]; [REG-R4]; [REG-R61]; [REG-R34] |
| The one published rate | 일반상해 후유장해 발생률(3~100%), 기본계약, **5세, 상해 1급: 남 0.0001823, 여 0.0001163** | [S1] |
| 보험가격지수 | Published per product, sex and 형; observed **79.6–116.0** (male) and **72.4–123.3** (female). The suppressed form's index is **8 to 18 points above the 표준형's at eight of the nine carriers publishing both, and about 7 points below it at the ninth** | [S11]; [REG-R22 제7-45조제7항](#krlib-reg-r22) |
| Pricing method | **현금흐름방식** — mandatory for a contract longer than three years, with an adequacy analysis on 최적기초율 and projected cash flows | [REG-R18 제7-64조제1호](#krlib-reg-r18) |
| 보장부분 적용이율 (예정이율) | **2.75% p.a.** | observed 2.50–3.00 [S11]; **[std]** (18) |
| 적립부분 공시이율 | **1.70% p.a.**, reset off a published 공시기준이율 | observed 1.60–2.20 [S11] [S2]; **[std]** (18) |
| 최저보증이율 | **0.30% p.a.** | observed 0.20–0.50 [S11]; **[std]** (18) |
| 평균공시이율 | **2.50%**, itself capped at the 공시이율 in force on the selling date | [S2]; [REG-R9 제1-2조제13호](#krlib-reg-r9); [REG-R48] |
| Pricing lapse rate (적용해지율) | Disclosed on the suppressed forms at one carrier: **5.0% / 3.0% / 1.0% p.a.** during the payment period by duration band (≤10년 / 10–15년 / >15년), **0.5%** afterwards on the 미지급형Ⅱ and **0.65%** on the 미지급형Ⅲ; 「1형(표준형) 및 2형(계약전환형)에는 적용해지율이 적용되지 않습니다」 | [S1]; **[std]** (19) |
| Lapse basis adopted | The **2024 계리가정 guideline** — log-linear decay to **0.1%** at 납입완료 and **0.8%** thereafter — not the 2019 disclosure | [R11]; [REG-R27]; **[std]** (19) |
| Minimum premium | **₩20,000 a month** modal; observed ₩0–₩25,000 | [S11]; **[std]** (15) |
| Published discounts | 다자녀 1%–3% (2 or 3+ siblings); 출산할인 2% on a **sibling's** policy; 국가유공자 3%; existing-policyholder 1% | [S11] |
| Statutory discount, 2026 | **1%–5% for one year** on a 보장성 어린이보험 where the policyholder or spouse is within a year of a birth, on 육아휴직 or on 육아기 근로시간 단축; industry-wide from **2026-04-01**. 어린이보험 is **expressly excluded** from the companion premium-deferral scheme | [R6]; **[std]** (20) |
| Premium waiver — the child | 50% 이상 후유장해 (상해 or 질병), **or** diagnosis of one of the **7대질병**, **or** a 중대한특정상해수술; with a **P코드 carve-out** | [S2]; **[std]** (14) |
| Premium waiver — the 계약자 | The **계약자's death**, or a cumulative 장해지급률 of **50% 이상** from one cause | [S10 제22조]; **[std]** (14) |
| Effect of either waiver | 차회 이후의 보장보험료 waived for the remainder of the 납입기간; payment of the **적립보험료 stops as well**; cover continues in full | [S2]; **[std]** (14) |
| Waiver and renewal | A waiver granted in one renewal cycle **does not carry into the renewed contract** on the 표준형 | [S2] |
| Commission | First-year remuneration may not exceed the first year's expected premium; instalment structures pay no more than **60% of the 표준해약공제액** a year | [REG-R22 제4-32조제5항·제8항](#krlib-reg-r22); [REG-R29] |
| Acquisition and maintenance cost | Named in the 약관, **never quantified** in any retrieved document; the composite sets 계약체결비용 at or below the **표준해약공제액** of 감독규정 [별표 14] | [REG-R20]; [REG-R29]; **[std]** (21) |

14. **Two premium waivers, on two lives, and why the composite carries both.** The market
    splits them by licence and the composite refuses the split. On the **손해보험** chassis the
    waiver is on the **child**, and the archetypal current product states the trigger set on
    the cover page of its 상품요약서: 「보장보험료 납입면제 — 상해 및 질병으로 50%이상후유장해
    발생시 또는 7대질병으로 진단시 또는 중대한특정상해수술 받은 경우」, where 7대질병 is
    「암(유사암 제외), 뇌혈관질환, 중대한재생불량성빈혈, 양성뇌종양, 심혈관질환(특정Ⅰ,
    I49제외), 심혈관질환(I49), 심혈관질환(특정Ⅱ)」 and 중대한특정상해수술 is 「상해로 뇌손상,
    내장손상을 입고 사고일로부터 180일 이내에 받은 개두·개흉·개복수술」 [S2]. The **parent's**
    death and disability are handled instead by a 부양자 rider stack on the parent's own life,
    which pays a lump sum or a 교육자금 annuity rather than waiving and is **compulsory on a
    태아 contract**: 「태아 가입 시에는 상해사망(부양자) 특별약관, 질병사망(부양자) 특별약관 중
    1개의 특별약관을 의무가입」 [S11] [S5]. On the **생명보험** chassis the two collapse into
    one clause [S10 제22조제1항]:

    > 보험료 납입기간 중 가입자녀가 암(단, 상피내암, 기타피부암 및 경계성종양은 제외)으로
    > 진단확정되거나 장해분류표 중 동일한 재해 또는 재해이외의 동일한 원인으로 여러 신체부위의
    > 합산 장해지급률이 50% 이상인 장해상태가 되었거나 **계약자가 사망** 또는 …
    > 장해지급률이 50% 이상인 장해상태가 되었을 때에는 차회 이후의 보험료 납입을 면제하여
    > 드립니다.

    It works because that wording makes the 피보험자 of the contract 「계약자와 가입자녀」 [S10
    제3조] — the policyholder is himself an insured, so his death is a contractual event of the
    main policy and not a third party's, and 상법 제731조's written-consent requirement is
    satisfied by his own signature [REG-R50]. The composite takes the **손해보험 trigger set
    for the child** [S2], the current market form stated in a primary document, and the
    **생명보험 clause for the 계약자** [S10], because the alternative is a benefit and not a
    decrement and because a waiver on a life who is not the insured is the mechanic this
    product exists to demonstrate. Both are specified at *Contractual mechanics*, with the
    **P코드 carve-out**, the exclusion lists and the non-survival of a waiver across a renewal
    [S2]. One carrier's narrower form is a switch — 「2종(보험료 납입면제형)」 on
    암(유사암포함), 뇌졸중 or 급성심근경색증 or a 50% 후유장해, with its own exclusion list of
    some 130 riders [S1] — and one publishes the waiver as a **benefit in its own right**,
    보험료 납입면제대상, at a 가입금액 of ₩100,000 [S11], which is the presentation the
    composite adopts because it makes the waiver a priced item the model can carry separately.
15. **월납, and why the model runs on a monthly grid.** Every retrieved product quotes 월납
    [S1] [S2] [S11] and one adds 연납 [S7]; a single 3년만기 product on the board is 일시납
    [S11]. Monthly is what the arithmetic wants: the 90-day waiting period that applies from
    보험나이 15 lands on a grid boundary, the 태아보장기간 and the 1년만기 neonatal block are
    whole numbers of months, and the premium stream and the 계약자적립액 recursion share one
    step. 감독규정 제7-65조제2항 permits the 계약자적립액 to be computed 「연납보험료를
    기준으로 하여 산출할 수 있다」, which is what lets a monthly-premium Korean product carry
    an annual account recursion and is the reconciliation `Child_KR_S` shares with
    `Cancer_KR_S`, `Medical_KR_S` and `LTC_KR_S` [REG-R18]. The **최저가입 보험료** is
    published: ₩20,000 at five carriers, ₩25,000 at one, ₩15,000 and ₩10,000 on two channels of
    another, 보장보험료 ₩5,000 at one, and 「없음」 on two direct forms [S11].
16. **The two premium figures, and what they are anchored on.** No carrier publishes a rate
    table by age and duration, so the office premium is a **model-point input**. What is
    published is a specimen premium per product on a standardised basis — 보험나이 5세, 상해
    1급, 100세만기 20년납, 월납, the **보장보험료 of the compulsory covers only** [R12] [S11].
    The observed levels vary by a factor of seven, ₩21,502 to ₩148,250 for a male 5-year-old,
    because carriers include different compulsory sets in the quoted figure, so the level is
    not comparable across the board and the 보험가격지수 is the normalising statistic. The
    composite takes **₩27,000** for the calibration cell — the tight cluster of the three
    mid-market carriers whose compulsory sets are closest to [R12]'s (₩26,841, ₩26,999,
    ₩27,480) [S11] — and the anchor cell adds ₩1,000 for the 계약자 waiver module and ₩3,000
    for the 태아 module over its own 17-month term. On entry age, [R5] publishes an index on a
    simulation of 암진단 ₩40,000,000, 20년 납입, 100세 만기: total premium 100% at 0세, 189% at
    20세, 264% at 30세, 625% at 60세, on residual terms of 100 / 80 / 70 / 40 years — from
    which a 계약나이-0 rate sits slightly **below** a 5세 rate. The composite does not attempt
    that refinement and holds ₩27,000 at both, a **[std] simplification** stated here so a
    later pass can remove it. **`technical-notes.md` performs the equivalence calculation on
    the shipped basis and its figure governs where the two differ**; nothing depends on ₩27,000
    or ₩31,000 being a market rate.
17. **The 무해지 discount, measured.** Taking every carrier on the board that publishes both a
    표준형 and a suppressed form on the same specification, the suppressed premium as a
    percentage of the 표준형's is 70.4 / 71.2 (M/F), 72.6 / 74.0, 79.7 / 81.9, 72.6 / 71.6,
    78.0 / 79.4, 78.9 / 79.9, 76.5 / 77.9, 76.4 / 76.9 and 67.4 / 68.2 [S11]. The observed
    range is **67%–82% of the 표준형 premium**, i.e. an 18%–33% discount, and the composite
    takes **78%** — the modal cluster and, at the anchor cell, ₩21,840 against ₩28,000.
18. **Interest.** A full-text search of the 감독규정 returns **zero** occurrences of 예정이율:
    the regulation speaks only of the **계약자적립액 적용이율** and of the 금리확정형 /
    금리연동형 distinction [REG-R9] [REG-R48]. What the comparison board publishes instead, per
    product, is the **보장부분 적용이율** — the pricing rate under another name — and the
    **적립부분 적용이율** with its 최저보증이율 [S11]:

    | 보장부분 적용이율 | 적립부분 공시이율 (최저보증) |
    |---|---|
    | 2.65% | 2.20% (0.3%) |
    | 2.75% | 1.60% (0.3%) |
    | 3.00% | 1.60% (0.3%) |
    | 3.00% | 1.60% (0.3%) |
    | 2.75% | 1.90% (0.25%) |
    | 2.70% | 1.70% (0.3%) |
    | 2.75% / 2.50% | 1.65% (0.2%) |
    | 2.75% / 2.50% | 1.75% (0.2%) |
    | 3.00% | 1.75% (0.5%) |

    Observed: **보장부분 2.50%–3.00%, 공시이율 1.60%–2.20%, 최저보증이율 0.20%–0.50%** [S11].
    The composite takes **2.75% / 1.70% / 0.30%**, the modal value of each column. The 공시이율
    is a **금리연동형** quantity reset off a published 공시기준이율 under 감독규정
    제7-65조제3항 and 시행세칙 [별표 27] [REG-R18] [REG-R24]; one carrier prints the formula,
    「공시기준이율(%) = 외부지표금리수익률 × α + 운용자산이익률 × (1−α)」, with α a function of
    the prior-year opening 보험료적립금, the asset duration and the prior-year premium income,
    but the extracted bracketing of α is uncertain and is [unverified] [S1]. `Child_KR_S`
    **implements no crediting at all**: it reads the published 환급률 grid, whose own interest
    basis is that 1.70% with the 2.50% 평균공시이율 and the 0.30% floor [S2], and recovers the
    계약자적립액 from it, so the three rates are recorded as the basis of the shipped grid and
    are not read by any formula. Both the recursion and the 공시이율 reset are carried by
    reference to `WholeLife_KR_S`. The 평균공시이율 of 2.50% enters only
    through the surrender-charge and disclosure computations [S2] [REG-R9] [REG-R48].
19. **The lapse basis, and the one carrier that published its own.** [S1] discloses the
    **적용해지율** actually used to price each suppressed form — a step function at 5.0% / 3.0%
    / 1.0% a year during the payment period by duration band, and 0.5% or 0.65% after 납입완료
    — and states that the 표준형 carries none [S1]. That is a published, product-specific
    decrement basis and it is directly usable, but it is **of exactly the shape the supervisor
    moved against**: the 2024-11-07 계리가정 guideline names the log-linear model converging to
    **0.1%** at 납입완료 as the 원칙모형, sets the post-completion ultimate at **0.8%** (or a
    20% relativity to the 표준형 rate), and requires an insurer departing from it to disclose
    the CSM, BEL, K-ICS and net-income differences quarterly [R11] [REG-R27]. 어린이보험 is not
    named in the release, but every 무해지 어린이보험 form on the board is inside its scope
    [S11]. `Child_KR_S` uses the **guideline basis** and ships [S1]'s 2019 vector as a
    comparison switch, which is exactly the comparison the guideline requires an insurer to
    disclose.
20. **The 2026 discount is a real cash-flow item and is carried as a parameter.** From
    2026-04-01 every Korean insurer operates a **1%–5% premium discount for one year** on a
    보장성 어린이보험, the rate and period set by each insurer, where the policyholder or
    spouse is within a year of a birth, on 육아휴직, or on 육아기 근로시간 단축 for a child of
    12 or under [R6]. On the birth limb the discount applies to a **sibling's** policy and not
    the newborn's own — 「(출산) 형제, 자매 출산 시 보험료 할인 가능(피보험자 출산사유 할인은
    제외)」 [R6]. It is limited to one use per contract, pre-existing contracts qualify, and
    the expected industry cost is about **₩1,200억원 a year** [R6]. So it is a
    `premium_discount_rate` and a `premium_discount_months` parameter, **off in the base run**;
    and because 어린이보험 is expressly excluded from the companion premium-deferral limb [R6],
    no deferral state is needed. Whether the discount applies to the 영업보험료 or the
    보장보험료 is not stated and is [unverified].
21. **Expenses.** No retrieved document quantifies any expense item for this product. What is
    available is a statutory ceiling: 감독규정 [별표 14] caps the deductible acquisition cost
    at the **표준해약공제액** [REG-R20], and the FSC's 2019 expense reform states the same cap
    as thirteen months' premium for a 보장성보험 [REG-R29]. The composite sets 계약체결비용 at
    or below the 표준해약공제액 and computes the schedule at *Contractual mechanics*. The
    보험가격지수 gives an independent bound the other way: it is the ratio of total premium to
    the sum of the 참조순보험료 total and the average expense total [S11], so an index of 98
    means the product's premium is 2% below the reference net-plus-average-expense premium, and
    the observed 79.6–116.0 band brackets how far a real product sits from that reference.

### Benefit provisions

All amounts are stated at the anchor cell. The rider set is the 손해보험협회 comparison basis
[R12], which is the only standardised specification of a Korean child policy the market itself
publishes, plus a 유사암 tier and a 태아 module that basis does not carry.

| Parameter | Representative value | Basis |
|---|---|---|
| **기본계약 — 일반상해후유장해** | **보험가입금액 × 장해지급률** on a **3~100%** scale, 보험가입금액 **₩100,000,000 (1억원)**, 상해 1급. Payable more than once, the percentages accumulating | [R12]; [S1] [S2] [S4] [S5] [S11]; **[std]** (22) |
| Definition of 장해 | 표준약관 부표 3 (장해분류표): 「상해 또는 질병에 대하여 치유된 후 신체에 남아 있는 **영구적인** 정신 또는 육체의 훼손상태 및 기능상실 상태」, excluding temporary states during treatment | [REG-R25] |
| **질병후유장해** | 보험가입금액 × 장해지급률, **3~100%**, 보험가입금액 **₩10,000,000 (1천만원)** | [R12]; [S11] |
| 후유장해 variants offered | 20~100%, 3~79%, 50% 이상, 80% 이상; and 50%/80% 이상 생활지원금 forms paying an annuity over **20 years** | [S11]; scope **[std]** (22) |
| **암진단비 (유사암 제외)** | **₩10,000,000 (1천만원)**, 최초 1회한 | [R12]; [S11]; **[std]** (23) |
| **유사암진단비** | **₩2,000,000 (200만원)** — 20% of the general tier — with each member payable once: 기타피부암, 갑상선암, 대장점막내암, 제자리암, 경계성종양 | [S1] [S3] [S11]; **[std]** (24) |
| **뇌출혈진단비** | **₩10,000,000 (1천만원)**, 최초 1회한 | [R12]; **[std]** (23) |
| **급성심근경색증진단비** | **₩10,000,000 (1천만원)**, 최초 1회한 | [R12]; **[std]** (23) |
| **수술비** | **₩5,000,000 (500만원)** per named-disease surgery — 암수술, 뇌출혈수술, 급성심근경색증수술 — per qualifying operation | [R12]; **[std]** (23) |
| **입원일당** | **₩40,000 (4만원) per day**, 상해 and 질병 limbs, **1–180일 per stay** | [R12]; [S2]; **[std]** (25) |
| **골절진단비** | **₩400,000 (40만원)** per fracture, 치아파절 excluded | [S1] [S11]; **[std]** (25) |
| **화상진단비** | **₩200,000 (20만원)** per burn | [S1] [S11]; **[std]** (25) |
| **가족일상생활배상책임** | **₩100,000,000 (1억원)** per occurrence, applied separately to 대인배상, 대물(누수사고)배상 and 대물(누수사고 제외)배상; deductibles **₩500,000** on a 누수 대물 claim and **₩200,000** on any other 대물 claim; the 보험가입금액 is fixed and not selectable; **3년만기 갱신형** | [S5]; [S2]; [S3]; **[std]** (26) |
| 배상책임 — insured persons | 피보험자 및 배우자, 자녀, 동거중 친족 (8촌 이내의 혈족(모계 8촌 포함), 4촌 이내의 인척 및 배우자) | [S5] |
| 배상책임 — 보장개시일 | The 누수사고 limb starts **90 days** after the 계약일, resetting to the renewal date on each renewal; the rest starts at inception | [S5]; [S3] |
| **태아 module** | See the table below; on to `t = 17` at the anchor cell | [S1] [S2] [S5] [S8]; [R3]; **[std]** (27) |
| **보험료 납입면제대상** | Published as a benefit in its own right, 보험가입금액 **₩100,000 (10만원)**, whose 지급사유 is the occurrence of a waiver event | [S11]; [S2] |
| 면책기간 (waiting period) | **None while the insured is 보험나이 15 미만**; the 91st day counting the 계약일 as day 1 from 보험나이 15; **none at all** on a 태아가입 cover | [S3]; [S11]; [R5]; **[std]** (10) |
| Waiting periods that do apply | **90 days** on the 누수사고 limb of the liability rider [S5]; **90 days** on cancer-treatment hospital-cash and outpatient riders [S5]; **10 days** on certain infection and influenza riders, disapplied on a 태아가입용 form [S3]; every one of them re-runs from a **부활일** [S3] | [S3] [S5] |
| 감액기간 | **None.** `reduction_months` is a parameter with observed values 0 and 12; a **태아** contract is never subject to 감액 | [S1] [S3] [S11] vs [S6]; [R2]; **[std]** (11) |
| Repeat payment | The diagnosis benefits are 최초 1회한 each; the 후유장해, 입원, 수술, 골절, 화상 and 배상책임 limbs are payable repeatedly | [S1] [S2] [S11] |
| Termination on payment | **None.** No benefit payment terminates or exhausts the contract; cover runs to the 100세 계약해당일 | [S1] [S2] [S11] |
| Death of the insured | **No death benefit below 만 15세** (상법 제732조). The **계약자적립액 at the date of death plus the 미경과보험료** is paid and the contract ends: 「피보험자가 사망한 경우, 이 계약은 그 때부터 효력이 없습니다」 | [R7]; [REG-R50]; [REG-R17]; [REG-R25 제22조](#krlib-reg-r25); [REG-R19 제7-66조제5항](#krlib-reg-r19); [S7 제28조]; [S10] |
| Death of the insured, 만 15세 이상 | An 일반상해사망 rider becomes writable; **not carried in the base run** and not offered by any retrieved product on a contract issued below 15 | [S1] [S4] [S11]; **[std]** (9) |
| Exclusions (보험금을 지급하지 않는 사유) | The general exclusion articles were **not read in full** for this product line | [unverified]; **[std]** (28) |
| Suicide | The composite has no death benefit, so the 2-year 자살면책 clause has nothing to attach to | [S8]; **[std]** (28) |

**The 태아 module.** These covers exist only on a 태아가입 contract, are written on two
different terms, and are the only part of the product that can pay in respect of an event
before the insured legally exists.

| Cover | Representative amount | Term | Basis |
|---|---|---|---|
| 저체중아 육아비용 (인큐베이터 일당) | **₩50,000 per day**, actual days used **less 2 days**, **60 days** maximum | 1년만기 from birth | [S1]; [R3]; **[std]** (27) |
| 주산기질환 입원일당 | **₩10,000 per day**, on a continuous stay of **4 days or more**, paid **from the 4th day** (3일 초과 1일당), **120 days per stay** | 1년만기 from birth | [S8]; [S1]; [R3] |
| 선천이상 진단비 | **₩1,000,000**, 최초 1회한, on diagnosis of a 선천성 기형, 변형 또는 염색체 이상 after birth | 1년만기 from birth | [S1] |
| 선천이상 수술비 | **₩1,000,000** per qualifying operation | 1년만기 from birth | [S1]; [R3] |
| 신생아 뇌출혈 진단비 | **₩2,000,000** = 20% of the module's 가입금액, 최초 1회한 | 1년만기 from birth | [S1]; **[std]** (27) |
| 출생위험 (저체중·장해 출생) | 저체중아 출생 **10%**, 장해 출생 **20%**, 심한 장애 출생 **100%** of the module's 가입금액 | 태아보장기간 | [S1] |
| 조산 진단 | 보험가입금액 on birth **within 27 weeks** (one carrier's equivalent tests **31 weeks**) | 태아보장기간 | [S1]; [S2] |
| 태아보장기간 | **계약일 ~ 출생일**, including an event arising in labour or delivery; premium 전기납 | — | [S2] |
| Neonatal block term | **1년만기 전기납** from birth, matching 「출생 전후에 발생하는 질환에 대한 보장을 강화하려는 목적으로 출생 후 1년까지만 보장」 | — | [S2]; [S5]; [R5] |
| Enrolment window | The neonatal riders accept a foetus **임신 22주 이내**; one dental rider **임신 15주 이내** | — | [S5]; **[std]** (27) |
| Waiting period, 감액 | **None on either** | — | [S3]; [R2] |
| 유산 / 사산 | The contract is **무효** and every premium paid is returned | — | [S8 제56조]; [S9] |

22. **The basic contract is a percentage scale, not a lump sum, and that is the first
    structural delta.** Every retrieved non-life 기본계약 is 일반상해후유장해 paying
    **보험가입금액 × 장해지급률** [S1] [S2] [S4] [S5] [S11], on the 표준약관's 장해분류표, a
    percentage scale across thirteen body systems and explicitly a scale of **permanent**
    impairment [REG-R25]. `Cancer_KR_S`'s benefit fires once at a stated amount; this one fires
    at a stated *fraction* of a stated amount, may fire more than once, and accumulates. The
    ₩100,000,000 level is not [std]: it is the level printed on the comparison basis [R12] and
    the level every published premium is quoted at [S11]. The variant bands — 20~100%, 3~79%,
    50% 이상, 80% 이상 — and the two 생활지원금 forms converting a 50% or 80% disability into a
    **twenty-year annuity** [S11] are left out of the base run: an annuity on a disabled child
    is a materially different liability and belongs in a model point of its own.
23. **The diagnosis set, and a deliberate narrowing.** Two definitions are in the market for
    each adult-disease limb: the narrow 뇌출혈 and 급성심근경색증 the comparison basis prices
    [R12], and the broad **뇌혈관질환** and **허혈성심장질환** most current products sell, at
    ₩10,000,000–₩50,000,000 [S11] [S2]. The composite takes the **narrow** pair, against the
    grain of current practice, for one reason: every published premium in this file is quoted
    on [R12]'s specification [S11], so pricing the broad definitions against a premium
    collected for the narrow ones would make the anchor cell internally inconsistent. The broad
    pair is a switch. Read it alongside the supervisor's second complaint of 2023 —
    「어린이에게 발생빈도가 극히 희박한 뇌졸중, 급성심근경색 등 성인질환 담보를 불필요하게
    부가」 [R1] — a supervisory statement that these two limbs are priced on an exposure that
    barely exists for the first three decades of the term, which a paediatric incidence basis
    must reproduce rather than smooth away. Named-cancer riders stacking on the general tier —
    **다발성소아암**, 16대특정암, 5대고액치료비암, 전이암, 재진단암 [S1] [S3] [S11] — are out
    of the base; 다발성소아암 is named because it is the one cancer rider whose exposure is
    genuinely paediatric.
24. **The 유사암 tier, inherited unchanged in structure and changed in level.** `Cancer_KR_S`
    sets the tier at **20%** of the general amount on the same five members [REG-R40]; the
    child products publish 유사암 amounts of ₩2,000,000–₩20,000,000 against general-tier
    amounts of ₩10,000,000–₩100,000,000 [S11], and the composite takes 20% of its own
    ₩10,000,000 so that the chassis ratio is preserved. The clinical reason is the same at both
    ages — 갑상선암 is the single most common cancer in Korea and its five-year relative
    survival is **100.2%** [REG-R40] — but the **exposure is not**: thyroid cancer is
    concentrated in adults, so on a child policy the 유사암 tier costs almost nothing for
    thirty years and then becomes the most frequently paid diagnosis benefit in the contract.
    That is a shape a level premium has to fund, and it is the clearest single illustration of
    what a 100세만기 child policy actually is.
25. **The event benefits are small and frequent, which is the opposite of the chassis.**
    입원일당 at ₩40,000 a day [R12] on a 1–180일 basis [S2], 골절진단비 at ₩400,000 and
    화상진단비 at ₩200,000 [S1] [S11] are the covers a child policy actually pays on, an order
    of magnitude below the diagnosis benefits. The observed 입원일당 menu is wide — 1–180일,
    1–120일, 1–30일, 1–10일 and 4일이상 bases, with 종합병원 / 상급종합병원 / 중환자실 / 1인실
    variants and 암직접치료 and 요양병원 sub-limits [S1] [S2] — and the composite takes the
    comparison basis's single form. It does **not** implement a 180-day one-hospitalization
    memory: no retrieved Korean child wording states a re-admission grouping rule, and
    inventing one would be an unsourced benefit mechanic. Published 골절 and 화상 amounts run
    ₩100,000–₩400,000 [S1] [S11]; the composite takes the top of that range for fracture, the
    modal childhood accident claim, and the middle for burn.
26. **가족일상생활배상책임 is the cover only a non-life licence may write, and it is fixed.**
    The wording is reproduced in full at one carrier: cover where the insured, spouse, children
    or a cohabiting relative within the eighth degree of consanguinity or fourth of affinity
    incurs legal liability for injury to another or damage to another's property, 「1사고당
    대인배상, 대물(누수사고)배상, 대물(누수사고제외)배상 **각각 1억원 한도**」, with
    deductibles of **₩500,000** on a 누수 property claim and **₩200,000** on any other, arising
    from ownership, use or management of the dwelling or from daily life excluding
    non-residential property, and the 보험가입금액 **not selectable** [S5]. It is a **3년만기
    갱신형** at one carrier, renewing on 1–3년 blocks at 가입나이 태아~15세 [S2], and 갱신형 at
    two more [S3] [S5]; two forms, 누수 포함 and 제외, are offered and only one may be taken
    [S2]. The composite takes the 포함 form at ₩100,000,000, the specification the comparison
    basis prices [R12]. It is the only limb whose claim is a **third party's loss** rather than
    a state of the insured, and it is why [R5] gives the licence split the explanation it does.
27. **The 태아 module, and what is actually sourced in it.** The **structure** is sourced
    tightly: the 태아보장기간 as a term in its own right — 「계약체결일부터 출생시점(출산 또는
    분만 과정에서 보험금 지급사유가 발생하는 경우 포함)까지의 기간을 보험기간으로 하여」 [S2] —
    the parallel **1년만기 전기납** term for the 태아전용 block [S2], the 22-week enrolment
    bound on that block [S5], and the seven 태아전용 covers by name [S2]. The **benefit
    definitions** are sourced from one 2019 상품요약서 and the supervisor's 2008 rider table:
    「최고 60일을 한도로 실제 사용일수에서 2일을 공제하고 인큐베이터 사용 1일당 보험가입금액
    지급」 [S1], the older form of the same at 「인큐베이터를 3일 이상 사용했을 경우 1일당
    약정금액」 [R3], and 「'주산기질환'은 … 출생전후기에 기원한 특정 병태 대상 분류표에서 정한
    질병」 paid on a stay of at least four consecutive days, 3일 초과 1일당, 1회 입원당 120일
    한도 [S8]. The **amounts** are [std], taken from the supervisor's own worked claim [R3]: a
    birth at 32 weeks and 1.84 kg with congenital atresia and stenosis of the small intestine,
    an enterostomy, an incubator and a stay from 2007-12-07 to 2008-05-01 paid **₩16,836,420**
    in all — 신생아육아비용 ₩3,000,000 at 2일 초과 1일당 5만원 to a 60-day cap,
    신생아입원급여금 ₩1,200,000 at 3일 초과 1일당 1만원 to 120 days, 선천이상수술위로금
    ₩1,000,000, 질병입원급여금 ₩4,410,000 and 질병입원의료비 ₩7,226,420. Two things read off
    it: the neonatal block is capped **by days, not by amount**, so its severity is a
    length-of-stay distribution; and the indemnity element was 43% of the total, which is
    exactly the element no longer attachable (footnote 31).
28. **Exclusions are the honest gap in this document.** The general 보험금을 지급하지 않는 사유
    articles were not read in full for this product line and no retrieved document reproduces
    them, so no exclusion decrement is modelled and none is asserted. The statutory floor is
    상법 제659조 and 제660조, and 제663조 makes the whole Part one-way mandatory [REG-R49]. Two
    exclusions that *are* sourced sit outside the general article and are stated where they
    arise: the **P코드 carve-out** from the premium waiver [S2], and the exclusion of
    **혀유착증** and **선천성모반** from some 선천이상수술비 variants — the two high-frequency,
    low-severity conditions in that class [S1]. The 2-year 자살면책 [S8] has nothing to attach
    to.

### Options

Every item is specified so that a model point can switch it on; the **Base** column says what
the shipped anchor cell does.

| Option | Representative specification | Base | Basis |
|---|---|---|---|
| **태아가입 module** | 계약나이 0 at the 계약일, priced male; cover attaching at birth; the two terms and seven covers of the table above; the 무효-on-유산/사산 rule; the 계약일 reset where birth falls more than six months after issue | **on** | [S8 제53조~제61조]; [S2] [S5]; [R2] [R3] |
| **계약자 납입면제 module** | Waiver of all future premium on the **계약자's** death or 50% 이상 장해; 계약자 male 만 33 at the 계약일 | **on** | [S10 제22조]; **[std]** (14) |
| **Child 납입면제** | Waiver on the child's 50% 이상 후유장해, 7대질병 진단 or 중대한특정상해수술, with the P코드 carve-out | **on** | [S2] |
| **해약환급금 미지급형** | **0%** during the 납입기간; **50% of the 표준형 value** after 납입완료; premium at **78%** of the 표준형 | off | [S2] [S11]; [REG-R19 제7-66조제4항](#krlib-reg-r19); **[std]** (17) (29) |
| **해약환급금 미지급형Ⅲ (graded)** | A ten-step ladder from **5%** of the 표준형 value in the two years after 납입완료 to **50%** eighteen years after it, in 5-point steps every two years | off | [S1]; **[std]** (29) |
| **갱신형 chassis** | The whole product written of 20년만기 / 30년만기 renewable blocks, 최초 가입나이 0~30세, renewal ages `(보험기간)세 ~ (100−보험기간)세`, with cover-group ceilings of 80, 70, 98 and 30 in place of 100 for 중증화상, 장기이식, 재진단암 and 다발성소아암, and a 1년만기 renewal at 97/98/99세 for 재진단암. The company must notify the renewal premium and ask whether the contract is to continue **15 days** before the term ends | off | [S7 제29조]; **[std]** (2) |
| **보험기간 연장형 (3종)** | A third 종 whose 적립부분 is consumed to extend the cover term; its 환급률 is 76.0% at 20년 and then **falls on the 최저보증이율** to 61.8% at 25년, against 76.5% on the 공시이율 | off | [S2] |
| **110세만기** | The longest term found; same 가입나이 태아, 0~15세 and the same 납입기간 ladder | off | [S4] |
| **뇌혈관질환 / 허혈성심장질환 (broad definitions)** | The two adult-disease diagnosis limbs written on the broad KCD ranges rather than 뇌출혈 and 급성심근경색증, at ₩10,000,000–₩50,000,000 | off | [S11] [S2]; **[std]** (23) |
| **다발성소아암 진단비** | A named-cancer rider stacking on the general tier, whose exposure is genuinely paediatric; renewal ceiling **30세** where the rest of the contract renews to 100 | off | [S1] [S7] [S11] |
| **재진단암 진단비** | A repeating diagnosis benefit on a 1년 or 2년 대기형 cycle | off | [S1] [S3] [S11] |
| **임신·출산질환 module (the mother)** | 모성사망, 임신·출산질환 입원일당 (1-120일), 임신·출산 관련 고혈압·당뇨병 입원일당, 임신·출산질환수술, 분만전후출혈·수혈진단, 고위험임산부 집중치료실 입원, 유산 진단·수술·입원일당, 임신중독증, 태반조기분리, 양수색전증, 여성산과 자궁적출수술, and the indemnity-shaped 임신·출산질환실손입원의료비(통상분만일수 제외); mother's 가입나이 **20~47세**, term **계약일 ~ 분만 후 42일** (or 계약일 ~ 분만일) | off | [S2]; [S5] |
| **출산전 특정태아이상진단** | A benefit paid on **antenatal** diagnosis of a foetal abnormality, written on the **mother**, 가입나이 20~39세, term 계약일 ~ 분만일. The only cover in the product that pays before birth, and it pays the mother | off | [S2]; **[std]** (27) |
| **부양자 module (the parent, as a benefit)** | 상해사망(부양자), 상해후유장해(80% 이상)(부양자), 질병사망(부양자), 질병후유장해(80% 이상)(부양자), 보험료납입지원(6대질병진단)(부양자), and the 교육자금 / 자녀양육비 forms paying 「자녀나이에 따라」 or as a five-year annuity; parent's 가입나이 **만15세 ~ (77−보험기간)세**. **One of the two death forms is compulsory on a 태아 contract** | off — replaced by the 계약자 waiver | [S2] [S5] [S11]; **[std]** (14) |
| **2026 저출산 premium discount** | **1%–5%** for one year on birth, 육아휴직 or 육아기 근로시간 단축; one use per contract; pre-existing contracts qualify | off | [R6]; **[std]** (20) |
| **다태아 (multiple birth)** | Every foetus of a multiple pregnancy is insurable from 2012-10-01; carriers price a 다태아플랜 at roughly **2× for twins and 3× for triplets**, which [R5] notes probably understates the risk | out of scope | [R4]; [R5]; [S8 제57조] |
| **Adolescent and child-specific riders** | ADHD진단비 (payable from the 6세 계약해당일), 진성성조숙증진단비 (가입나이 태아~4세), 중증틱장애진단비 (태아~2세), 중증아토피진단비 (OSI 40점 이상, 태아 only), 시력치료비, 부정교합치료비, 유치보존치료비, 소아탈장수술비, 어린이심장시술비, 모야모야병개두수술, 수족구·중이염·폐렴·독감 진단비, 학교폭력피해치료비, 청소년폭력상해후유장해, 유괴납치피해일당 | out of scope | [S1] [S2] [S5] [S11] |
| **실손의료비 riders** | **Not available.** From April 2018 실손의료보험 must be sold as a standalone product | out of scope | [R9]; [R10]; [REG-R17]; **[std]** (31) |

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender-value form, base | **표준형** — 해약환급금 = 순보험료식 계약자적립액 less the 해약공제액, floored at zero | [S2]; [S1]; [REG-R19 제7-66조제1항제1호](#krlib-reg-r19); **[std]** (12) |
| Surrender-value form, switch | **해약환급금 미지급형**: **0%** during the 납입기간, **50% of the 표준형 value** afterwards | [S2] [S11]; **[std]** (29) |
| Legal basis of the suppressed form | 감독규정 제7-66조제4항 — a 순수보장성보험 priced with a **최적해지율** may pay less than the [별표 14]-floored value. A regulatory dispensation conditional on having used a best-estimate lapse rate in pricing, not a contractual device | [REG-R19]; [REG-R28] |
| 환급률 constraint on the suppressed form | Both the post-payment value must exceed **50%** of the 표준형's and the post-payment 환급률 must exceed the greater of **100%** and the 표준형's 환급률 | [REG-R19 제7-66조제4항제2호](#krlib-reg-r19); [REG-R28] |
| The comparison 표준형 | A **synthetic product**: 「3형과 동일한 보장내용으로 **해지율을 적용하지 않은** 상품이며, 비교안내를 위한 종목으로 **실제로 판매하지 않음**」 | [S3]; [S1]; **[std]** (29) |
| 해약공제액 | The **표준해약공제액** of 감독규정 [별표 14] | [REG-R20]; **[std]** (30) |
| 해약공제기간 | The 보험료 납입기간 or the 신계약비 부가기간, **capped at 7 years** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| 계약자적립액 accrual | **Monthly** before 납입완료, **daily** afterwards; credited at the **공시이율**, floored at the **최저보증이율** | [REG-R19 제7-66조제1항제4호](#krlib-reg-r19); [S2] [S11] |
| Unearned premium | On any termination the **미경과보험료** is added to whatever surrender value is paid | [REG-R19 제7-66조제5항](#krlib-reg-r19) |
| 만기환급금 | **None** on the protection part. The 표준형 pays whatever 계약자적립액 remains; on the published grid that is **16.0%** of premiums paid at 95 years and effectively nil at 만기, and the 미지급형 pays **0.0%** | [S2]; [S1]; **[std]** (3) |
| 보험계약대출 (policy loan) | Available against the 표준형's surrender value; **not available during the 납입기간** on the 미지급형, because there is none to lend against | [REG-R25 제33조](#krlib-reg-r25); [REG-R28] |
| Automatic premium loan | Not offered on the 미지급형; a missed premium lapses the contract at the end of 납입최고 | [REG-R28]; **[std]** (29) |
| 납입최고 (grace) | **At least 14 days** from the demand (7 where the term is under a year), the contract terminating the day after it expires. One carrier operates it as 「납입기일 다음날부터 납입기일이 속하는 달의 다음달 마지막 날까지」, so a premium due on 15 September is in grace to 31 October and the contract lapses on 1 November | [REG-R25 제26조](#krlib-reg-r25); [S8]; **[std]** (32) |
| Lapse (해지) | From the day after the 납입최고기간 expires | [REG-R25 제26조](#krlib-reg-r25); [S8] |
| Reinstatement (부활) | Within **3 years** of termination where the surrender value has not been drawn — **including where there is none**, which is the 무해지 case — on payment of arrears with interest at a rate within **평균공시이율 + 1%**, subject to fresh underwriting. **Every waiting period re-runs from the 부활일** | [REG-R25 제27조](#krlib-reg-r25); [S8]; [S3]; **[std]** (33) |
| First-premium failure | Liability never attaches; 상법 제656조 starts cover on receipt of the first premium absent other agreement | [REG-R49] |
| Pre-birth termination | 유산 or 사산 makes the contract **무효**, not lapsed, and **every premium paid is returned** | [S8 제56조]; [S9]; **[std]** (27) |
| Non-disclosure (계약 전 알릴 의무) | Termination within **1 month** of the insurer learning of the breach and **3 years** of formation (상법 제651조), narrowed by the 약관 to **2 years from the 보장개시일** with no claim event — one year for disease in a 진단계약 — with a causation defence | [REG-R49]; [REG-R25 제13조·제14조](#krlib-reg-r25) |
| Fraud (사기에 의한 계약) | Voidable within **5 years** of the 보장개시일 and one month of discovery | [REG-R25 제15조](#krlib-reg-r25) |
| 청약철회 (cooling-off) | **15 days** from receipt of the 보험증권 or **30 days** from the application, whichever comes first; effective on despatch; premiums returned within 3 business days | [REG-R51]; [REG-R25 제17조](#krlib-reg-r25); [S8]; out of scope for the model |
| 품질보증해지 | Cancellation within **3 months** of formation where the 약관 was not delivered, its important content not explained, or the application not signed | [REG-R49 제638조의3](#krlib-reg-r49); [REG-R25 제18조제3항](#krlib-reg-r25); [S8] |
| 지정대리청구서비스특약 | Standard; the 대리청구인 is the insured's spouse on the family register or a relative within the third degree, an unnamed designation defaulting to a direct ascendant or descendant. Must be offered wherever 계약자 = 피보험자 = 보험수익자 | [S8]; [S5] |
| Benefit claim prescription (소멸시효) | **3 years** | [REG-R49 제662조](#krlib-reg-r49); [REG-R25 제37조](#krlib-reg-r25) |
| Policyholder protection | 예금자보호법 cover of **₩100,000,000** per person per insurer, in a bucket that expressly excludes benefits payable because the term has ended | [REG-R52]; [REG-R25 제43조](#krlib-reg-r25) |
| Expiry | At the **100세 계약해당일** — `t = 1200` at the anchor cell. Nothing is paid beyond any residual 계약자적립액 | [S2]; **[std]** (3) |

29. **The 무해지 cliff, published.** One current 상품요약서 publishes both forms on one
    specification — 남자 5세, 상해 1급, 100세만기 20년납, 기본계약 상해후유장해 ₩150,000,000,
    의무부가 보험료납입면제대상 ₩100,000, and selected covers at 상해입원일당 ₩20,000,
    질병입원일당Ⅱ ₩20,000, 암진단Ⅱ(유사암 제외) ₩20,000,000, 유사암진단Ⅱ ₩1,000,000, 뇌혈관질환
    ₩10,000,000, 허혈심장질환진단 ₩10,000,000 — at 월납 ₩50,000 표준형 and ₩37,420 미지급형
    [S2]:

    | 경과 | 표준형 납입보험료 | 표준형 환급금 (환급률) | 미지급형 납입보험료 | 미지급형 환급금 (환급률) |
    |---|---|---|---|---|
    | 1년 | 600,000 | 0 (0.0%) | 449,040 | 0 (0.0%) |
    | 3년 | 1,800,000 | 820,910 (45.6%) | 1,347,120 | 60 (0.0%) |
    | 5년 | 3,000,000 | 1,876,960 (62.5%) | 2,245,200 | 280 (0.0%) |
    | 10년 | 6,000,000 | 4,422,580 (73.7%) | 4,490,400 | 550 (0.0%) |
    | 15년 | 9,000,000 | 7,050,220 (78.3%) | 6,735,600 | 420 (0.0%) |
    | 20년 | 12,000,000 | 9,923,370 (82.6%) | 8,980,800 | 0 (0.0%) |
    | 30년 | 12,000,000 | 12,149,980 (101.2%) | 8,980,800 | **5,752,590 (64.0%)** |
    | 40년 | 12,000,000 | 14,709,200 (122.5%) | 8,980,800 | 6,973,000 (77.6%) |
    | 50년 | 12,000,000 | 17,298,680 (144.1%) | 8,980,800 | 8,197,680 (91.2%) |
    | 60년 | 12,000,000 | 19,072,270 (158.9%) | 8,980,800 | 9,001,530 (100.2%) |
    | 95년 | 12,000,000 | 1,928,830 (16.0%) | 8,980,800 | **0 (0.0%)** |

    Interest basis for the table: 공시이율 **1.7%** (2026-07), 평균공시이율 **2.5%** capped at
    the selling-date 공시이율, 최저보증이율 **0.3%**, and for the 미지급형 a flat 보장부분
    적용이율 of **2.7%** 「적립한 금액으로 변동 없음」 because that form is 순수보장성 with no
    적립보험료 [S2]. **Three features a model must reproduce.** The suppressed form's value is
    nil through the entire payment period and jumps to 64.0% of premiums paid ten years after
    completion — a **cliff, not a curve** — and the 「60원」 and 「550원」 entries between are
    rounding on a nominally zero quantity. The 표준형's value **exceeds premiums paid from
    about year 30**, because the 적립부분 compounds at the 공시이율 while the 보장부분 reserve
    is still building; no other `krlib` protection product produces that shape and only a
    hundred-year term can. And **both forms collapse at maturity**. The 2019 generation of the
    other line shows the same shape at a higher level — 표준형 환급률 3.0% (1년), 51.1%, 66.3%,
    76.6% (10년), 86.8% (20년), 125.8% (40년), 155.7% (60년), 0.0% at 만기; 미지급형 0.0%
    throughout the payment period, 111.7% (20년), 161.8% (40년), 200.3% (60년), 0.0% at 만기
    [S1] — and that the 미지급형's 환급률 exceeds the 표준형's after completion is
    **arithmetic, not generosity**: the denominator is a smaller premium. The graded
    **미지급형Ⅲ** ladder is published in full, where M is the payment term in years: 5% from
    the day after the end of year M to the day before the M+2 계약해당일, then 10, 15, 20, 25,
    30, 35, 40, 45 and finally **50%** from M+18 to the end of the term [S1].
30. **The 표준해약공제액, computed for this product.** 감독규정 [별표 14] gives the cap as
    「연납순보험료의 5% × 해약공제계수 + 보장성보험의 보험가입금액의 10/1000」 [REG-R20]. For a
    보장성보험 the 해약공제계수 is the **policy term capped at 20** and the 연납순보험료 is
    recomputed on a 전기납 basis, or on **20년납 where the term is 20 years or more** — both of
    which bind here. The 보험가입금액 term is the harder half: this contract has **no
    일반사망보험금**, so [별표 15] 제3호 does not apply and 제9호 does — 「보험가입금액 =
    (위험보험료 / 정기보험의 위험보험료) × 정기보험의 보험가입금액」, computed at the 기준연령
    요건 on a term policy of the same 보험기간 [REG-R21]. A 제3보험 contract with no death
    benefit therefore gets a **notional** 보험가입금액 by scaling a term policy's face amount
    by the ratio of risk premiums, and that notional amount — not the ₩100,000,000 of
    accidental disability cover — is what enters the 10/1000 term, at the schedule's own rate
    of 10/1000, which is **one per cent**. `technical-notes.md` performs the arithmetic and
    finds that on this product **the [별표 14] limb does not bind**: it gives 56.25 months of
    core premium against the FSC's statement of the *same* ceiling as thirteen months'
    premium for a 보장성보험 [REG-R29] (item 21 above), so the cap is the lesser of the two,
    the thirteen-month reading, on every shipped model point. What belongs here is that the
    surrender charge is **capped by a computation whose inputs are themselves [std]**,
    deducted as a level amount over a 해약공제기간 capped at **7 years** [REG-R19].
31. **The 실손 rider is gone, and that is a regulatory fact rather than a design choice.**
    보험연구원's 2018 description of the structure still reads 「主보험 + 태아가입특약 +
    유자녀생활자금특약 + 산모보장특약 + 각종 선택특약 + **실손특약**」, and the 2004
    specification of the market's best-selling child policy includes 「일상상해 실손의료비 /
    질병입원 실손의료비」 [R5]. From April 2018 that is impossible: 실손의료보험 must be a
    standalone product consisting only of indemnity-medical cover, under 보험업감독규정
    제7-63조제2항제1호 as amended 2017-03-22 with a one-year transition [R9] [R10] [REG-R17].
    No child-side 실손 rider appears in any of the five current 상품요약서
    [S2] [S3] [S4] [S5] [S6]; what survives is one indemnity-shaped rider written on the
    **mother**, 임신·출산질환실손입원의료비(통상분만일수 제외), which is not a 실손의료보험
    [S2]. The general proportional-contribution clause survives in the older wording [S1] as a
    reminder that the 2019 generation still carried indemnity elements. **The consequence is
    structural**: a Korean family buys the indemnity layer as `Medical_KR_S` and the
    fixed-benefit layer as `Child_KR_S`, as two contracts, and the split is statutory.
32. **Grace.** The 표준약관 floor is 「14일(보험기간이 1년 미만인 계약은 7일) 이상」 [REG-R25
    제26조](#krlib-reg-r25); one carrier operates a calendar-month form running 「납입기일 다음날부터
    납입기일이 속하는 달의 다음달 마지막 날까지」, which is longer than the floor and is the
    observed practice [S8]. The composite takes the calendar-month form because it lands on the
    monthly grid, and notes that the two differ by up to a fortnight on the lapse date.
33. **Reinstatement, and why the model does not carry it.** 부활 is available within **3
    years**, even where there is no surrender value — the 무해지 case — and may not be refused
    merely because a claim event occurred before termination [REG-R25 제27조](#krlib-reg-r25) [S8]. Every
    waiting period re-runs from the 부활일 [S3], which below 보험나이 15 means almost nothing
    and above it a full 90 days. `Child_KR_S` treats lapse as **absorbing** and does not model
    reinstatement; the simplification is conservative on a protection product and is recorded
    in `technical-notes.md`.

---

## Contractual mechanics

Throughout, `t` is the number of complete months since the 계약일, `b` is the month of birth
(`b = 5` at the anchor cell), `n = 240` is the end of the 납입기간 and `T = 1200` is the 100세
계약해당일. `S` is the 보험가입금액 of the cover under discussion.

### Premium provisions

The premium is **level** for the whole 납입기간 on the 비갱신 core and does not vary with the
policy year, the claim history or the insurer's experience: the contract is 무배당, so there is
no dividend and no premium review [S1] [S2] [S11] [REG-R12]. It is payable **monthly in
advance** from the 계약일, including through the pre-birth period, and on the anchor cell it
runs in three streams:

    core 보장보험료          KRW 27,000    t = 0 .. 239
    계약자 waiver module      KRW 1,000     t = 0 .. 239
    태아 module (전기납)      KRW 3,000     t = 0 .. 16

The third is not an artefact of the composite. A 태아 contract really does carry a second,
short term with its own premium: 「아래의 계약은 계약을 체결할 때 피보험자가 될 자가
출생전자녀(태아)인 경우 계약체결일부터 출생시점 … 까지의 기간을 보험기간으로 하여 아래의
보험기간 및 보험료 납입기간을 **추가로 부가**합니다」 [S2], written elsewhere as a fixed
「1~10월만기 전기납 태아 월납」 sub-term [S1]. The composite merges the 태아보장기간 and the
1년만기 neonatal block into one module running `t = 0` to `t = b + 12 = 17`.

Premium ceases on the earliest of 납입완료 at `t = 240`, death of the insured, lapse, the
operation of **either** premium waiver, and — for the 태아 module — the end of its own term.
Where the 갱신형 flag is set the renewal premium is a function of the **renewal index** rather
than of the policy year, and the company must notify it and ask whether the contract is to
continue **15 days** before the term ends [S7 제29조]. Non-payment opens a 납입최고 of at least
14 days [REG-R25 제26조](#krlib-reg-r25), operated in practice as a calendar-month window [S8]. On the 표준형
there is a surrender value to lend against [REG-R25 제33조](#krlib-reg-r25); on the 미지급형 switch there is
neither that nor an automatic premium loan, and the lapse is immediate and complete [REG-R28].
That asymmetry is the whole difference between the two forms in a projection: the same lapse
rate produces a very different cash flow depending on whether anything is paid on it. Pricing
is by **현금흐름방식** with an adequacy analysis on 최적기초율 and projected cash flows
[REG-R18 제7-64조제1호](#krlib-reg-r18) — which on a hundred-year contract with a twenty-year premium term is
not a formality, since the adequacy of a level premium is decided almost entirely by
assumptions about the eighty paid-up years.

### 태아가입 — the contract written before the insured exists

This is the part of the product with no analogue anywhere in this repository, and the wording
is quoted rather than paraphrased. The articles are one carrier's 태아가입특칙, 제53조 to
제61조 [S8]; a second carrier's older wording carries the same 특칙 at 제44조 to 제51조 with
호적 references instead of 가족관계등록부, which is the evidence that the 특칙 is a
market-standard text and not one drafter's invention [S9].

- **제53조 (특칙의 적용)** — 「이 특칙은 피보험자로 될 자가 계약체결시 태아(胎兒)인 계약에
  한하여 적용합니다.」
- **제54조 (피보험자)** — 「제53조의 태아는 **출생시에 피보험자가 됩니다**.」
- **제55조 (출생통지)** — the policyholder must notify the birth immediately, with a 통지서,
  the child's 가족관계등록부 or 주민등록등본 and the 보험증권; the fact is endorsed on the
  policy.
- **제56조 (유산 또는 사산시의 처리)** — 「태아가 유산 또는 사산에 의해 출생하지 못한 경우에는
  **계약을 무효로 합니다** … 이미 납입한 보험료를 돌려드립니다.」
- **제57조 (복수출생의 경우)** — on a multiple birth each child may be nominated as an insured;
  where only one contract was written, one child is nominated and the others may be made the
  insured of new contracts. If the nominated child dies within a year of birth and a twin
  survives, the survivor may be substituted within a month with retroactive effect, unless a
  benefit or reserve has been paid or claimed or the policyholder killed the child.
- **제58조 (보험금 지급기준 적용나이)** — 「보험금 지급기준표에서 적용하는 피보험자 나이는
  **피보험자가 출생한 날부터** 계산합니다.」
- **제59조 (출생전 보험금 지급사유 발생)** — an event before birth is paid, but **from the date
  of birth**.
- **제60조 (계약나이의 계산 특례)** — 「계약일에 있어서의 피보험자의 계약나이는 **0세**로
  합니다.」
- **제61조 (계약일 및 계약나이의 변경)** — where the child is born **more than six months after
  the 계약일**, the 계약일 is moved back to six months before the birth, the 계약나이 is
  re-set, and premiums and reserves are adjusted under the 산출방법서.

Six modelling consequences, each carried explicitly.

1. **Cover attaches at birth.** 「태아보험의 피보험자는 태아 그 자체가 아니라 출생 후
   신생아이므로 … 태아보험의 보장은 … 보험가입 시점이 아니라 **태아의 출생 직후부터** 시작됨」
   [R3], and in 2016 sixteen carriers and nineteen products were ordered to stop using 「태아
   때부터 보장」, 「엄마 뱃속에서부터 보장」 and even the bare word 「태아보험」 in marketing
   material, under 보험업감독규정 제4-35조제3항 [R2]. In the model **every benefit on the
   child's own life is zero for `t < b`**; the only covers in force before birth are the
   태아보장기간 limbs, which pay from the date of birth even where the event preceded it [S8
   제59조], and the mother-side 출산전특정태아이상진단 if that option is on [S2].
2. **Foetal death is a void, not a decrement.** 「태아는 법적으로 인격을 갖지 못하여 인보험의
   보호대상이 될 수 없으므로 … 태아보험에서는 태아의 사망을 직접적으로 보장하지는 아니함」
   [R3]; what exists instead is mother-side 유산 cover. So the pre-birth period carries a
   **void decrement**: the contract is 무효, every premium is returned, and the projection
   de-recognises the policy rather than terminating it — a negative cash flow of premiums
   already collected, belonging in a validity adjustment and not in the lapse column. **No
   Korean source retrieved gives a foetal-loss rate**, so the rate is a `[std]` construction
   whose provenance `technical-notes.md` states; what the sources fix is the mechanic.
3. **The pre-birth period is bounded, and the bound is actuarial.** [S8 제61조] caps it at six
   months by moving the 계약일 back, with premiums and reserves adjusted under the 산출방법서;
   the neonatal riders close at 임신 22주 [S5], so a contract written inside that window still
   has **at least** 4.1 months of gestation to run; and the 태아 sub-term is written
   「1~10월만기」 [S1]. The composite takes `b = 5`, which is inside both bounds.
4. **The non-life chassis re-rates instead of resetting the 계약일**: 「태아보장기간에
   태아위험보장을 위한 보장보험료를 적용하며, 출생일 이후의 보장보험료는 **보험나이 0세
   기준**으로 변경하여 적용함. 다만, 출생통지가 이루어지지 않은 경우에는 **계약전환일**
   (출생예정일이 포함된 다음 달의 계약해당일)에 보험료를 변경하여 적용」 [S1]. The composite
   implements the re-rating form but holds the core 보장보험료 level across `t = b`, because
   the two rates are not separately published. The **계약전환일 fallback** is carried even so:
   a contract on which the birth is never notified converts anyway, on a date computed from the
   expected delivery date.
5. **Priced male, trued up after delivery.** 「태아보험 가입시 태아의 성별을 구별하기가 어려운
   점 때문에, 일단 **남자 아이를 기준으로** 납입보험료가 산정되고 출산 후 성별대로 정산하는
   구조」 [R3], confirmed by a carrier's published 민원 case [S8]. The composite prices male
   and **does not model the true-up**, because on the current published tables the direction is
   no longer reliable — four carriers price the female above the male and seven below, the
   spread running 62% to 114% of the male rate [S11].
6. **Multiple birth is insurable and is a real pricing question.** Before 2012 only the
   first-born was covered — 「태아가 복수로 출생한 경우에는 호적상 선순위로 기재된 자를
   가입자녀로 합니다」 [S9 제48조] [R3]; from **2012-10-01** all foetuses of a multiple
   pregnancy became insurable [R4], and the current 특칙 is the post-2012 wording [S8 제57조].
   Carriers responded with 다태아플랜 riders at roughly **2× for twins and 3× for triplets**,
   which [R5] notes probably understates the risk. The composite is a single-foetus contract;
   the detail of the 2012 measure is [unverified] because the supervisory attachment is a
   scanned image [R4].

### The two ages a foetal contract carries, and the five-month offset

보험나이 governs everything except the 만 15세 nullity test, where **실제 만 나이** applies [R8
제21조제1항 단서](#krlib-child-r8) [S7 제27조제1항]. On a 태아 contract the two ages separate by a **known**
amount rather than by an average, because the 계약나이 is 0 at the 계약일 [S8 제60조], the
child's 만나이 is 0 at birth, and the anniversaries on which 보험나이 increments run from the
계약일:

    보험나이(t)  =  floor(t / 12)
    만나이(t)    =  floor((t - b) / 12)      for t >= b,  undefined before

so the two differ by exactly `b` months for the life of the contract — **five months at the
anchor cell**, capped at six by [S8 제61조]. A model must hold both. **보험나이** governs the
premium, the anniversary on which the 갱신형 blocks renew, and the 15-year threshold at which
the 면책기간 switches on [S3] [S11]. **만나이 from the date of birth** governs the benefit
scale — 「보험금 지급기준표에서 적용하는 피보험자 나이는 피보험자가 출생한 날부터 계산합니다」
[S8 제58조] — the 만 15세 death threshold [R7] [R8], and the age conditions written into
individual riders (ADHD진단비 from the 6세 계약해당일; 진성성조숙증 at 태아~4세; 중증틱장애 at
태아~2세) [S2] [S11]. `Child_KR_S` projects decrements on 만나이 and carries 보험나이 as the
contractual clock; on a non-foetal model point the offset is the ordinary half-year average and
is a [std] simplification, and on the anchor cell it is exact.

### The basic contract — 보험가입금액 × 장해지급률

    benefit(event) = S x disability_rate(event),   S = KRW 100,000,000

on the 3~100% band, payable more than once, the percentages accumulating [R12] [S1] [S2] [S11].
장해 is 「상해 또는 질병에 대하여 치유된 후 신체에 남아 있는 **영구적인** 정신 또는 육체의
훼손상태 및 기능상실 상태」, excluding temporary states during treatment [REG-R25], so the
trigger is a **settled** impairment whose incidence lags the accident rather than coinciding
with it. The one published rate in this file attaches here: 일반상해 후유장해 발생률(3~100%),
기본계약, **5세, 상해 1급, 남자 0.0001823, 여자 0.0001163** [S1] — 18.2 and 11.6 per 100,000 a
year, the order of magnitude a child accidental-disability decrement has to reproduce, and the
only observation of one anywhere in the research. `technical-notes.md` builds the age curve as
a `[std]` construction anchored on that pair. And because the benefit is a *fraction* of `S`
and the modal 장해지급률 on a child accident is small, the expected claim per event is far
below `S`: a model treating this cover as a lump sum at `S` overstates the liability by a large
multiple. The severity distribution is not published and is `[std]`.

### 면책기간 — the under-15 disapplication, and the 태아 carve-out

    암보장개시일 =
        the day the first premium is received        if 보험나이 < 15 at the 계약일
        the 91st day counting the 계약일 as day 1     if 보험나이 >= 15 at the 계약일
        the day the first premium is received        if the cover is a 태아가입용 form

so on the anchor cell the cancer benefit is in force from `t = 0` and **the chassis's 90-day
control never operates at all**. Read carefully, the rule is tested **at the 계약일 and not at
the claim date** — 「계약일 현재 보험나이 15세 미만 피보험자의 경우」 [S11], 「최초계약과
부활계약의 면책기간은 보험나이 15세 이상인 경우에만 적용」 [S3]. A contract issued at 계약나이
0 therefore has **no cancer waiting period at any point in its hundred-year life**, including
the eighty-five years during which the insured is an adult. That is not a drafting oversight;
it is the price of a rule written once at issue, and it is a real anti-selection asymmetry
against the adult `Cancer_KR_S` chassis. **A model that re-tests the rule at each anniversary
is wrong.**

The chassis's invalidity mechanic — a diagnosis inside the waiting period voiding the affected
cover with premiums returned — therefore has nothing to attach to on the base run, and
`waiting_months` is 0 with 3 as the switch, the switch being what the same product looks like
written at 보험나이 15 or above, which is what the pre-2023 generation at 0~30세 was [S1] [S7].
**Waiting periods that do survive**, and which a model must not sweep away with the cancer one:
the **90-day 보장개시일 on the 누수사고 limb** of the liability rider, running from the 계약일
and **resetting to the renewal date on every renewal** [S5] [S3]; the ordinary 90-day
책임개시일 on cancer-treatment hospital-cash and outpatient riders [S5]; 10-day waits on
certain infection and influenza riders, expressly disapplied on a 태아가입용 form — 「주7)
태아가입용의 경우 면책기간 없음」 [S3]; and the re-run of all of them from a 부활일 [S3].

### 감액기간 — why there is none, and what removed it

    benefit = 1.00 x (the full amount)   at every duration

The market has moved to 감액없음 and prints the word in the benefit names at five carriers
[S1] [S3] [S11]; where a 감액 survives it is the chassis's first-year 50% [S6] [S11], and one
current matrix applies it only to **dental** benefits, at 25% or 50% 「최초계약일부터 2년
경과시점 전일 이전」, with cancer at 「-」 throughout [S3]. And a **태아 contract may not be
subject to 감액 at all**; the 2015 변경권고 set the before-and-after wording out side by
side [R2]:

| 종전 | 개선 |
|---|---|
| 제4조 ④ 피보험자에게 암보장개시일 이후 계약일부터 1년 이내에 … 보험금 지급사유가 발생한 경우 회사는 계약일부터 1년 초과시에 지급하는 보험금의 50%를 지급합니다. | 제4조 ④ (동일) **단, 피보험자가 보험가입 당시 태아(胎兒)인 경우에는 보험금의 100%를 지급합니다.** |

The reasoning was that 「태아는 보험가입시 역선택 가능성이 거의 없는데도 성인과 동일한 기준을
적용하여」 the reduction was applied, and the trigger case was a newborn with a cerebral
haemorrhage paid at 50%; 17 carriers and 56 products were covered, the recommendation was made
2015-06-17 and the wordings were amended between January and April 2016 [R2]. A current carrier
confirms it still holds: 「암진단일이 보험계약일로부터 1년 미만인 경우 보험금이 삭감될 수
있습니다.(**태아형의 경우 삭감없이 보험금이 지급됩니다**)」 [S8].

So on the anchor cell **both** of the chassis's anti-selection devices are disapplied, and each
by a different supervisory action a decade apart. That is the single most important thing this
document says about the morbidity basis: `Child_KR_S` has no contractual protection against
early claims at all, and whatever protection exists must come from the incidence assumption
itself.

### The neonatal module and its two terms

    태아보장기간   : t = 0 .. b            (계약일 ~ 출생일, including labour and delivery)
    neonatal block : t = b .. b + 11       (1년만기 from birth; the cover ends at t = b + 12)

with the module's premium 전기납 over the whole of it. The first term is stated as a term in
its own right at one carrier [S2] and as a fixed 「1~10월만기 전기납」 at another [S1]; the
second matches the description of the perinatal rider as 「출생 전후에 발생하는 질환에 대한
보장을 강화하려는 목적으로 **출생 후 1년까지만 보장**」 [R5], and the 태아전용 covers are all
written 1년만기 [S2]. Two benefit formulas are **day-capped rather than amount-capped** and
must be implemented as such:

    incubator benefit  = KRW 50,000 x max(0, min(days_used, 60) - 2)
    perinatal cash     = KRW 10,000 x max(0, min(stay_days, 120) - 3),
                         payable only where stay_days >= 4

from 「최고 60일을 한도로 실제 사용일수에서 **2일을 공제**하고 인큐베이터 사용 1일당
보험가입금액 지급」 [S1] — the supervisor's older form required 「인큐베이터를 **3일 이상**
사용」 instead of a two-day deduction [R3] — and from 「4일이상 계속 입원하여 … **4일째
입원일로부터** 입원 1일당 … (1회 입원당 120일 한도)」 [S1] and 「**3일 초과 1일당**, **1회
입원당 120일 한도**」 [S8]. Both are severity distributions over **days**, not amounts, which
is why the module's cost is a length-of-stay question and why the supervisor's worked claim is
the useful datum (footnote 27).

The **출생위험** limb is a three-tier scale on the pre-birth term — 저체중아 출생 10%, 장해
출생 20%, 심한 장애 출생 100% of the module's 가입금액, with a richer version adding a
저체중아(2.5kg 이하) tier at 5% [S1]. The **선천이상** limb pays on diagnosis of a 선천성 기형,
변형 또는 염색체 이상 after birth and again on surgery for one, with variants excluding
혀유착증 and 선천성모반 [S1]. The **신생아 뇌출혈** limb pays 가입금액 × 20% [S1], and it is
the cover at the centre of the 2013 P-code dispute: the supervisor required in 2013-09 that
neonatal claims be paid on the **diagnosis name rather than the KCD code**, ending refusals of
뇌출혈 claims coded **P52** rather than in the I chapter, after which frequency and the loss
ratio rose sharply and carriers tightened 뇌졸중 진단비 underwriting limits on 태아·어린이
business [R5]. A model of this module should treat its frequency basis as **regime-dependent**
rather than stationary, and say so.

### 보험료 납입면제 — the child trigger

    on 50% 이상 후유장해 (상해 or 질병),
    or on diagnosis of one of the 7대질병,
    or on a 중대한특정상해수술,
        the 보장보험료 is waived from the next instalment for the rest of the 납입기간

with 7대질병 = 암(유사암 제외), 뇌혈관질환, 중대한재생불량성빈혈, 양성뇌종양, 심혈관질환(특정Ⅰ,
I49 제외), 심혈관질환(I49), 심혈관질환(특정Ⅱ), and 중대한특정상해수술 = 「상해로 뇌손상,
내장손상을 입고 사고일로부터 180일 이내에 받은 개두·개흉·개복수술」 [S2]. Five operative rules
come with it [S2]: the waiver applies to the **보장보험료** from the next instalment;
**출생전후기에 기원한 특정 병태(P코드) 진단시 납입면제를 적용하지 않음**; on the 표준형 a
waiver granted in one renewal cycle **does not carry into the renewed contract**; once the
보장보험료 is waived **payment of the 적립보험료 stops as well**; and a long list of riders is
excluded — the whole 부양자 and 모성 block, and a second list (추간판장애수술, 시력교정,
시력치료, ADHD진단, 부정교합치료, 성조숙증, 중증틱장애, 대상포진, 원형탈모증, 특정언어장애 및
말더듬증, 틱장애약물치료, 질병악안면수술) for which the waiver applies only to events after
that rider's own 보장개시일.

**The P코드 carve-out is the sharpest interaction in the product.** The 태아 module's whole
reason for existing is the perinatal chapter of the KCD; the waiver expressly does not fire on
it. So the covers most likely to pay in the first year of a foetal contract are precisely the
ones that cannot stop the premium — which is coherent, a neonatal condition not being a
lifelong impairment, and which a model must implement rather than average away.

Like the chassis's waiver this one is a **correlated decrement**: it fires on the same events
that pay the diagnosis and disability benefits and then runs for as long as the insured
survives inside the 납입기간, so its value is an incidence rate multiplied by a post-onset
survival curve. Unlike the chassis's it is worth very little in the early years — paediatric
cancer and cerebrovascular incidence are two orders of magnitude below the adult rates the
chassis is calibrated on [REG-R40] — and a great deal from about `t = 180`, when the insured
reaches an age at which the 7대질병 begin to occur and which is still sixty months inside the
납입기간. The narrower alternative is switchable: one carrier sells the waiver as an optional
**2종(보험료 납입면제형)** on 「암(유사암포함)」, 「뇌졸중」 or 「급성심근경색증」 or a 50%
이상 후유장해, with its own exclusion list of some 130 riders [S1].

### 보험료 납입면제 on the 계약자 — a decrement on a life who is not the insured

    on the death of the 계약자,
    or on a cumulative 장해지급률 of 50% or more from one cause affecting the 계약자,
        all future premium is waived for the rest of the 납입기간

[S10 제22조제1항], quoted in full at footnote (14). This is the mechanic with no counterpart in
`uslib`, `uklib`, `jplib`, `frlib` or `delib`, and three things about it are worth stating
precisely.

**Why it is lawful in one clause.** The 생명보험 wording makes the 피보험자 of the contract
「계약자와 가입자녀」 — the policyholder is himself an insured [S10 제3조] — so his death is a
contractual event of the main policy and not a third party's, and 상법 제731조's
written-consent requirement for a policy on another's death is satisfied by his own signature
[REG-R50]. On the 손해보험 chassis, where the licence does not permit that drafting, the same
economics arrive as a separate **부양자** rider stack on the parent's own life, at issue ages
만15세 ~ (77−보험기간)세, of which **one death form is compulsory on any 태아 contract**:
「태아 가입 시에는 상해사망(부양자) 특별약관, 질병사망(부양자) 특별약관 중 1개의 특별약관을
**의무가입**」 [S11] [S5]. The market's name for the economic effect is 교육자금 or 자녀양육비
— 「자녀나이에 따라 교육자금을 지급」 at one carrier, 「엄마 상해 사망 자녀양육비(5년지급형) —
5년간 매년 2천만원」 at another [S5] [S11].

**Why the composite takes the waiver rather than the rider.** They are not the same cash flow.
The rider pays a benefit and leaves the premium running; the waiver stops the premium and pays
nothing. On a twenty-year premium term the waiver's value is the present value of the remaining
premium at the date the parent dies — a decreasing function of duration, zero after `t = 240` —
while the rider's value is a level sum assured throughout the rider's own term, which stops at
80 on the non-life chassis because of the 질병사망 design rule (*Regulatory context*).
Modelling one as the other would be wrong in both level and shape.

**What the model has to carry.** A **second decrement life** with its own age, sex and
mortality basis:

    prem_waived(t) = 1  if  the child trigger has fired at or before t
                          or the 계약자 has died at or before t
                          or the 계약자 is in a 50%+ 장해 state at or before t

with the 계약자 aged 만 33 at `t = 0`, so 만 53 at `t = 240`. The waiver's whole value is
concentrated in the twenty years in which a 33-to-53-year-old parent might die or become
severely disabled, and Korean mortality at those ages is low, which is why the module is cheap
enough to be compulsory. Two further points. The **decrements are not independent** of each
other in any way the model can see, and the composite treats them as independent — a `[std]`
simplification stated in `technical-notes.md`. And the **계약자 may be changed** during the
contract, which would change the decrement life mid-projection; no retrieved wording states how
the waiver responds, so the composite holds the 계약자 fixed and marks the point [unverified].
A rider inherits the main contract's waiver automatically — 「이 특약의 보험료 납입기간 중
주계약의 보험료 납입이 면제되었을 때에는 이 특약의 차회 이후의 보험료 납입을 면제하여
드립니다」 [S8] — so a single waiver event stops the whole premium stream and not just the
core.

### The 갱신형 blocks inside a 비갱신형 contract

The clearest statement of the architecture is a direct-channel product built end to end of
renewable blocks: 20년만기 / 30년만기 with 최초 가입나이 0~30세, renewal age ranges written as
`(보험기간)세 ~ (100−보험기간)세`, shorter 1~19년 and 21~29년 blocks renewing to
`(100−보험기간)세`, and **different ceilings by cover group** — 80, 70, 98 and 30 in place of
100 for 중증화상, 장기이식, 재진단암 and 다발성소아암, with 재진단암 additionally carrying a
1년만기 renewal at 97, 98 and 99세 [S7]. 제29조(계약의 자동갱신) requires notice **15 days**
before the term ends, and 제28조 provides that 「피보험자가 사망한 경우, 이 계약은 그 때부터
효력이 없습니다」 [S7].

In the composite the core covers are 비갱신 and only 가족일상생활배상책임 renews, on a
**3년만기** cycle [S2]. What the renewal does: the premium is recomputed at the attained
보험나이 on the rate basis in force at the renewal date, so it is a function of the **renewal
index** rather than of the policy year [S7]; the 보험가입금액 is unchanged; **no fresh waiting
period** attaches, except that the 누수사고 limb's 90-day 보장개시일 **does** reset to the
renewal date [S5]; **no 감액** [S2] [R2]; a waiver granted before renewal **does not carry
into** the renewed contract [S2]; and the block ends at its own cover-group ceiling, which may
be far short of 100 [S7]. The contract-boundary question is real and this document does not
resolve it: a 3년만기 자동갱신 liability rider inside a 비갱신 hundred-year contract is either
one contract with a repricing feature or a series of three-year contracts, and the answer
changes the CSM. `Child_KR_S` projects the renewals as a continuation of the same contract and
records the choice.

### Death of the insured, and what is paid instead

    on death at any age:  pay 계약자적립액(t) + 미경과보험료(t);  contract ends

There is **no 사망보험금 below 만 15세** and the prohibition is statutory: 상법 제732조 makes
such a contract 무효 [R7] [REG-R50], the 표준약관 restates it at 제19조제2호, and 제19조제3호
adds that the saving for an age misstatement discovered after the insured has reached the
contractual age 「제2호의 만 15세 미만자에 관한 예외가 인정되는 것은 아닙니다」 [R8] [REG-R25].
The 생명보험 wording pays a 사망보험금 only 「만 15세 계약해당일 이후」 [S10 제21조], and the
older market answer was to return premiums [R3] [R5].

The composite pays the **계약자적립액 plus the 미경과보험료**, because that is what 감독규정
제7-63조제1항제1호 requires of a 제3보험 contract on a death it does not cover [REG-R17] and
what 표준약관 제22조 implements — 「산출방법서에서 정하는 바에 따라 회사가 적립한 **사망 당시의
계약자적립액**」 [REG-R25] — with 상법 제736조 as the statutory floor [REG-R50]. On the 표준형
that is a real amount from about year 3 (₩820,910 at 3 years on a ₩50,000 monthly premium in
the published grid [S2]); on the 미지급형 switch it is close to nil for the whole payment
period, and a family whose child dies in year 10 receives almost nothing. That is a real and
uncomfortable property of the suppressed form and it is stated rather than smoothed. **상법
제739조** — 「상해보험에 관하여는 제732조를 제외하고 생명보험에 관한 규정을 준용한다」
[R7] [REG-R50] — makes accidental-death cover on a child under 15 lawful; the market
nonetheless writes 일반상해사망 only from 만 15세 [S1] [S4] [S11], which is more conservative
than the statute requires. That reading is **[unverified]** and no parameter depends on it.

### 계약자적립액, 해약환급금 and the 무해지 cliff

    계약자적립액(t)   accrues monthly to t = 240 and daily thereafter,
                      credited at the 공시이율 (1.70%) floored at the 최저보증이율 (0.30%)
    해약환급금(t)     = max( 계약자적립액(t) - 해약공제액, 0 )        [표준형]
                      = 0                                             [미지급형, t < 240]
                      = 0.50 x 표준형 해약환급금(t)                    [미지급형, t >= 240]
    on any termination, add 미경과보험료(t)

The basis is stated by the carriers in the same words: 「금융감독원장이 인가한 산출기준에 따라
계산한 이 보험의 **순보험료식 계약자적립액에서 해약공제액을 공제한 금액**을 해약환급금으로
지급하여 드립니다」 [S2], and 「순보험료식 책임준비금에서 해지공제액을 공제한 금액」 [S1]. The
regulation floors it at zero, caps the 해약공제기간 at seven years, fixes the 해약공제액 at the
**표준해약공제액** of [별표 14], and requires the monthly / daily accrual split
[REG-R19] [REG-R20].

**The 50% is 50% of a product nobody can buy.** The comparator is synthetic and both carriers
say so: 「기준이 되는 2종(표준형)의 해지환급금은 … **해지율을 적용하지 않고** 계산함」 [S1],
and 「'해약환급금미지급형 비교상품'은 … 해지율을 적용하지 않은 상품이며, 비교안내를 위한
종목으로 **실제로 판매하지 않음**」 [S3]. So the suppressed form's post-completion value is
half of a hypothetical cash value computed *without* the lapse assumption used to price the
form itself — which is the whole reason that assumption became a supervisory matter
[R11] [REG-R27] [REG-R28].

The published grid at footnote (29) is the target and it has three features no smooth curve
will fit. The suppressed value is **nil through the entire payment period and jumps to 64.0%**
of premiums paid ten years after completion. The 표준형's value **crosses premiums paid at
about year 30** and keeps rising to 158.9% at year 60. And **both collapse at maturity**, the
표준형 to 16.0% at 95 years and the 미지급형 to 0.0%, because there is no 만기환급금 on the
protection part and what remains is only the residual 적립부분. A third 종 shows a fourth
shape: on a 보험기간 연장형 the 환급률 is 76.0% at 20 years and then, on the **최저보증이율**,
**falls** to 61.8% at 25 years — 76.5% on the 공시이율 — because the 적립부분 is being consumed
to extend the cover [S2].

### Exclusions and 면책

The composite carries three grounds on which a claim is not paid and is honest that the general
article is missing: the **pre-birth invalidity rule**, under which 유산 or 사산 makes the
contract 무효 and every premium is returned [S8 제56조] [S9]; **non-disclosure**, below; and
**fraud in the formation of the contract**, voidable within five years of the 보장개시일 and
one month of discovery [REG-R25 제15조](#krlib-reg-r25). The general 보험금을 지급하지 않는 사유 articles were
**not read in full** for this product line. The statutory floor is 상법 제659조 and 제660조,
and 제663조 makes the whole Part one-way mandatory so that no 약관 may vary it against the
policyholder [REG-R49]. Two sourced exclusions sit outside the general article and are
implemented where they arise: the **P코드 carve-out** from the premium waiver [S2], and the
exclusion of 혀유착증 and 선천성모반 from some 선천이상수술비 variants [S1]. The 2-year
자살면책 [S8] has nothing to attach to. **No exclusion decrement is modelled**, and
`technical-notes.md` records this as an [unverified] area.

### 고지의무 and 계약 전 알릴 의무

The two names are one duty; the 표준약관 says the 계약 전 알릴 의무 is 「상법상 '고지의무'와
같습니다」 [REG-R25 제13조](#krlib-reg-r25). 상법 제651조 gives rescission for an intentional or grossly
negligent misstatement or omission of a material fact, within **one month** of the insurer
learning of it and **three years** of formation, and not at all where the insurer knew or was
grossly negligent in not knowing; a matter asked about in writing is presumed material, and
제655조 gives the **causation defence** [REG-R49]. The 약관 narrow the window in the
policyholder's favour, which 상법 제663조 permits: no termination where **two years** have
passed from the 보장개시일 with no claim event — **one year** for disease in a 진단계약 — or
where the insurer accepted on a health-examination document, or where the 보험설계사 prevented
truthful disclosure; and 제14조제5항 bars termination for non-disclosure of **other insurance
held** [REG-R25 제13조·제14조](#krlib-reg-r25).

Two features are specific to this product. **On a 태아 contract the disclosure is about the
pregnancy and the mother, not the insured** — the insured does not yet exist, and the material
facts at underwriting are the gestational week, the antenatal screening results and the
mother's own history. No retrieved wording states how 고지의무 applies to facts about a person
who is not the 피보험자, and the point is marked [unverified]. And **underwriting responds
short of rescission** through a 특정 신체부위·질병 보장제한부 인수특약 [S8], which on this
product would most naturally attach to a congenital finding.

### 청약철회, 품질보증해지, 실효 and 부활

**청약철회** is the cooling-off right of 금융소비자보호법 제46조제1항제1호 — 「보험증권을 받은
날부터 **15일**과 청약을 한 날부터 **30일** 중 먼저 도래하는 기간」 [REG-R51] — implemented at
표준약관 제17조 with three exclusions (an insurer-funded health examination, a contract of 90
days or less, a 전문금융소비자), effectiveness **on despatch**, and premiums returned within
three business days [REG-R25] [S8]. **품질보증해지** is the 상법 제638조의3제2항 right:
cancellation within **three months** of formation where the 약관 was not delivered, its
important content not explained, or the application not signed [REG-R49] [REG-R25
제18조제3항](#krlib-reg-r25) [S8]. Both are out of scope for the model, which projects from the point cover is
in force — though on a 태아 contract the cooling-off window has a peculiar property worth
recording: it expires months before the insured exists, so between its end and the birth the
policyholder's only routes out are 해지 or, if the pregnancy fails, the 무효 rule, which
returns everything.

Lapse is specified at *Termination and values*, and two things are peculiar to this product. On
the **표준형** base there is something to break the fall — a surrender value from about year 3
and a 보험계약대출 against it [REG-R25 제33조](#krlib-reg-r25) — whereas on the **미지급형** switch there is
nothing at all, so the same lapse rate produces a materially different cash flow [REG-R28]. And
**부활 restores almost nothing below 보험나이 15**: reinstatement is available within three
years even where there is no surrender value, and may not be refused merely because a claim
event occurred before termination [REG-R25 제27조](#krlib-reg-r25) [S8]; every waiting period re-runs from the
부활일 [S3]; but below 보험나이 15 there is no cancer waiting period to re-run, so a reinstated
child policy is, uniquely in this library, very nearly the policy that lapsed. `Child_KR_S`
nonetheless treats lapse as **absorbing** and records the simplification.

### Expiry

The contract ends at the **100세 계약해당일**, `t = 1200` at the anchor cell. Nothing is paid
beyond whatever 계약자적립액 remains — 16.0% of premiums paid at 95 years on the 표준형's
published grid and 0.0% on the 미지급형's [S2] — and there is no 만기환급금 on the protection
part [S1] [S2]. On a 태아 contract the terminal date is fixed by the **계약일**, not by the
birth, so the insured's age at expiry is 100 less the pre-birth period: on the anchor cell the
contract expires when the insured is **99년 7개월** old by 만나이. That five-month asymmetry
between the contractual clock and the life runs the whole length of the projection, and it is a
direct consequence of [S8 제60조] setting the 계약나이 to 0 before the child exists.

---

## Riders and options

**In scope (modelled or parameterized):**

- **태아가입 module** — the 태아보장기간 and the 1년만기 neonatal block, with the incubator,
  perinatal-cash, congenital-anomaly, neonatal-haemorrhage, birth-risk and preterm limbs; the
  무효-on-유산/사산 rule; the priced-male convention; the six-month 계약일 reset. **On** in the
  base run [S1] [S2] [S5] [S8] [R3].
- **계약자 납입면제 module** — a waiver decrement on the policyholder's own life, at 만 33
  male. **On** in the base run [S10 제22조].
- **Child 납입면제** — the 7대질병, 50% 후유장해 and 중대한특정상해수술 triggers with the P코드
  carve-out and the rider exclusion lists. **On** in the base run [S2]; the narrower 2종 form
  is a switch [S1].
- **해약환급금 미지급형** — 0% during payment, 50% after, premium at 78% of the 표준형.
  Switchable; **off** in the base run [S2] [S11] [REG-R19].
- **해약환급금 미지급형Ⅲ** — the ten-step graded ladder from 5% to 50% [S1]. A second switch.
- **갱신형 chassis** — attained-age re-rating on 20년/30년 blocks with cover-group ceilings; no
  fresh waiting period, no 감액, no carry-over of a waiver [S7] [S2]. **Off** in the base run.
- **뇌혈관질환 / 허혈성심장질환 broad definitions** — a benefit-definition switch on the two
  adult-disease limbs [S11] [S2].
- **감액기간** — `reduction_months` with observed values 0 and 12, disapplied on a 태아
  contract [S6] [S11] [R2]. **0** in the base run.
- **2026 저출산 premium discount** — a 1%–5% haircut for twelve months [R6]. **Off**.
- **110세만기** — a term switch [S4].
- **일반상해사망 from 만 15세** — a death benefit attaching at the anniversary on which the
  insured reaches 15 [S1] [S4] [S11]. **Off**.

**Out of scope:** the 임신·출산질환 module written on the mother, including 모성사망, the 유산
limbs, 임신중독증, 태반조기분리, 양수색전증 and 출산전특정태아이상진단 [S2] [S5]; the 부양자
benefit stack, including 상해사망(부양자), 질병사망(부양자), 보험료납입지원(6대질병
진단)(부양자) and the 교육자금 / 자녀양육비 annuity forms [S2] [S5] [S11]; 다태아 plans
[R4] [R5]; the named-cancer riders 다발성소아암, 16대특정암, 5대고액치료비암, 전이암 and
재진단암 [S1] [S3] [S11]; the 50% and 80% 후유장해 생활지원금 twenty-year annuity forms [S11];
the adolescent and child-specific riders listed at *Options*; 골절수술비, 성장판손상골절,
화상수술비, 중증화상·부식진단 and 깁스치료비 [S1] [S11]; the 보험기간 연장형 3종 [S2]; the
계약전환형 2형 [S1]; 실손의료비 riders of any kind, which are not attachable
[R9] [R10] [REG-R17]; and the 적립부분 mid-term withdrawal facility, which no retrieved child
wording specifies.

---

## Variations across insurers

1. **Maximum 만기.** 100세 at four carriers [S1] [S2] [S5] [S6] and **110세** at one [S4]; the
   life-chassis wordings retrieved are older and shorter [S8] [S9] [S10]. Composite: 100세, the
   modal maximum and the term every published premium and cash-value grid is quoted on.
2. **가입나이.** 태아~15세 at every current non-life product [S2] [S4] [S5] [S6]; **0~30세** in
   the pre-2023 generation of two of the same lines [S1] [S7]; 0~15세 and 0~20세 by 종 at one
   life carrier, [unverified] [S16]. Composite: 태아~15세, with the pre-2023 envelope
   documented because the change is datable to a supervisory action rather than to a market
   movement [R1].
3. **The 태아 sub-term.** A named 태아보장기간 = 계약일~출생일 with a separate rider block at
   one carrier [S2]; a fixed 「1~10월만기 전기납」 at another [S1]; a 1년만기 전기납 obligatory
   block at a third [S4]; a 특칙 with no separate term at all on the life chassis [S8] [S9].
   Composite: the two-term form, merged into one 17-month module.
4. **The 태아 enrolment window.** Stated in a primary document at only one carrier — **임신
   22주 이내** for the neonatal block, **임신 15주 이내** for one dental rider [S5]. The
   supervisor's 2008 statement is 「최장 임신 24주까지」 [R3] and 보험연구원's 2018 one 「임신
   8주가 지난 후부터 24주까지」 [R5]; the widely repeated 손해보험 22주 / 생명보험 16~22주
   split is a consumer-guide claim and is **[unverified]**. Composite: 22 weeks, the only bound
   in a primary product document.
5. **Suppressed surrender-value forms.** Every carrier offers at least one [S11]. The
   post-completion fraction is **50%** at seven [S2] [S3] [S5] [S6] [S11], and one carrier's
   2019 generation offered three at once — 납입후 100%, 납입후 50% and a graded 5%–50% ladder
   [S1]. Composite: the 50% form as the switch and the graded ladder as a second switch
   (footnote 29).
6. **The disclosed pricing lapse rate.** Published by exactly **one** carrier, in one edition —
   5.0% / 3.0% / 1.0% during payment and 0.5% or 0.65% afterwards [S1] — and by nobody else
   [S2] [S3] [S4] [S5] [S6]. Composite: the 2024 guideline basis, log-linear to 0.1% at 완납
   and 0.8% thereafter [R11] [REG-R27], with the 2019 disclosure as a comparison switch. The
   two are an order of magnitude apart inside the payment period and the difference falls
   almost entirely into the CSM.
7. **The waiver trigger on the child.** 50% 후유장해 or **7대질병** or 중대한특정상해수술 at
   one carrier [S2]; 암(유사암 포함), 뇌졸중 or 급성심근경색증 or 50% 후유장해, sold as an
   optional 종, at another [S1]; an obligatory 자녀 납입면제 rider at two more [S4] [S5]; a
   납입면제대상 특별약관 published as a benefit at a fifth [S11]; 암 or 50% 후유장해 on the
   life chassis [S10]. Composite: the 7대질병 set (footnote 14).
8. **The waiver on the parent.** A 부양자 rider stack at every non-life carrier
   [S2] [S4] [S5] [S11], **compulsory on a 태아 contract** at one [S5] [S11]; the **계약자's
   death or 50% 장해 in the main clause** on the life chassis [S10 제22조]. Composite: the
   life-chassis clause, because it is a decrement and the rider is a benefit (footnote 14).
   **This is the largest single design divergence in the product and the two forms are not
   interchangeable.**
9. **The P코드 carve-out from the waiver.** Stated at one carrier [S2] and not located in the
   extracted text of any other. Composite: adopted, because it is the only positively stated
   treatment and because it decides whether the 태아 module can stop the premium.
10. **The cancer 면책기간.** 90 days with an express **보험나이 15 이상만** qualification at
    one carrier [S3] and in a benefit definition at another [S11]; not located in the extracted
    text of [S2] or [S4]; a 90-day 책임개시일 on cancer riders at a fifth [S5]. Composite:
    disapplied below 15 and disapplied entirely on a 태아 form [S3] — evidenced twice, by two
    carriers, in two document types, and by the research institute's account of the 2006 change
    [R5].
11. **The 감액기간.** 감액없음 at five carriers, inferred from 「(감액없음)」 in the published
    benefit names [S1] [S3] [S11]; **1년 이내 50%** at one [S6] [S11]; 감액 on dental benefits
    only at another [S3]; 1년 미만 삭감 with an express **태아형 제외** on the life chassis
    [S8]. Composite: none. Reading 「(감액없음)」 in a benefit name is strong but is not the
    same as reading the clause, and the point is marked.
12. **배상책임.** A 갱신형 가족일상생활배상책임 Ⅲ/Ⅳ at one carrier [S3];
    일상생활중배상책임Ⅳ(가족) on a 3년만기 renewal with 누수 포함 / 제외 forms at another [S2];
    a fixed ₩100,000,000 with the three limits and two deductibles at a third [S5]; **absent
    entirely** from the life chassis, which has no licence to write it [S8] [S9] [S10] [R5].
    Composite: the fixed form (footnote 26).
13. **Interest.** 보장부분 적용이율 2.50%–3.00%, 공시이율 1.60%–2.20%, 최저보증이율
    0.20%–0.50%, published per product [S11]; not published at all on the life chassis.
    Composite: 2.75% / 1.70% / 0.30%, the modal value of each column (footnote 18).
14. **Sex relativity and price level, neither of which behaves.** Four carriers price the
    **female higher** and seven the **male higher**, the female premium running from 62% to
    114% of the male [S11] — a benefit-mix effect rather than a pure morbidity effect, since
    the products differ in whether the compulsory set is dominated by accident cover,
    male-heavy at child ages, or by cancer and thyroid cover, female-heavy at adult ages. Any
    `[std]` morbidity basis **must state which of the two it reproduces and why**, and the
    composite's does. The absolute level varies by a **factor of seven** on a nominally
    standardised basis — ₩21,502 against ₩148,250 for a male 5-year-old — because carriers
    include different compulsory rider sets in the quoted 보장보험료 [S11]; the normalising
    statistic is the **보험가격지수**, and even that mostly shows the 무해지 form's index
    **8 to 18 points above** the 표준형's — at eight of the nine carriers publishing both,
    because the index divides by a reference net premium computed without the
    suppressed-lapse credit — while the ninth prints its 미지급형Ⅱ at 89.5 (male) against a
    표준형 96.4, **about 7 points below**, so the pattern is strong but not universal [S11].
15. **What does not vary.** The insured comes into existence at birth and cover attaches then;
    유산 or 사산 voids the contract and returns the premium; a 태아 contract is priced at
    계약나이 0 and re-rated at birth; the death benefit is unavailable below 만 15세; the
    neonatal covers run on a one-year term; the 무해지 form exists at every carrier and is
    priced 18%–33% below the 표준형; the surrender value on the suppressed form is nil for the
    whole payment period and steps up at 납입완료; the product is 무배당; and there is **no
    만기환급금** on the protection part. These are the invariant core of the composite, and the
    parts of it any future child-product delta should expect to inherit unchanged.

---

## Regulatory context

**Classification.** 어린이보험 is 제3보험 business — 상해보험 and 질병보험 together, under
보험업법 제2조제1호다목 and 제4조제1항제3호 — and 제4조제3항's deeming provision makes the
class writable under a life or a non-life licence alike [REG-R1]. Written as a 장기손해보험 it
is designed identically, 감독규정 제7-61조 applying the whole of the 제3보험 design rule
제7-63조 to it [REG-R17]. Everything below follows from that classification and from one
article of the commercial code.

**상법 제732조 is the statute that shapes the product.** 「15세미만자, 심신상실자 또는
심신박약자의 사망을 보험사고로 한 보험계약은 무효로 한다」 [R7] [REG-R50]. It is why this
product has no death benefit, why the 표준약관 restates it at 제19조제2호 and refuses to extend
the age-correction saving to it [R8] [REG-R25], why 일반상해사망 is written only from 만 15세
across the whole market [S1] [S4] [S11], and why the composite pays the 계약자적립액 instead.
**제739조** makes accidental-death cover on a child lawful by excepting 제732조 from what
상해보험 borrows [R7] [REG-R50], and the market's refusal to write it is more conservative than
the statute requires; that reading is [unverified]. **제739조의2** (신설 2014-03-11) is the
only article of 상법 addressing disease insurance directly, and 제739조의3 borrows the life and
accident rules for the rest [REG-R50]: the contract law of this product is borrowed law, and
its detail lives in the 약관 and the 표준약관.

**The payment on a non-covered death.** 감독규정 제7-63조제1항제1호 requires a 제3보험 product
to be designed so that, on death from a cause the policy does not cover, the **계약자적립액**
and the 미경과보험료 of 제7-66조제5항 are paid and the contract terminates [REG-R17]; 표준약관
제22조 implements it and 상법 제736조 floors it [REG-R25] [REG-R50]. This is a **first-order
modelling requirement**: a Korean child policy must carry an account balance even though it is
not a savings product.

**Surrender values.** 감독규정 제7-66조제1항 sets 해약환급금 = 계약자적립액 less 해약공제액,
floored at zero, over a 해약공제기간 that is the payment period capped at seven years, with the
deduction fixed at the **표준해약공제액** of [별표 14] [REG-R19] [REG-R20]. Because this
contract has no 일반사망보험금, its 보험가입금액 for that formula is the **notional** amount of
[별표 15] 제9호 — the ratio of risk premiums scaled onto a term policy's face amount, computed
at the 기준연령 요건 [REG-R21]. 제7-70조 applies the whole regime to 제3보험 and 제7-69조 to
장기손해보험, so one surrender-value regime governs the product on either licence [REG-R19].

**The 무해지 form.** 제7-66조제4항 permits a 순수보장성보험 priced with a **최적해지율** to pay
less than the [별표 14]-floored value — a regulatory dispensation conditional on having used a
best-estimate lapse rate, not a contractual device — subject to 제2호's twin test that the
post-payment value exceed 50% of the 표준형's **and** the post-payment 환급률 exceed the
greater of 100% and the 표준형's [REG-R19]. The 2020 amendment inserting that test was
calibrated on a worked example in which a 표준형 20-year 환급률 of 97.3% stood against a 무해지
환급률 of 134.1% [REG-R28]. The FSS's 2019 consumer alert adds two operational facts this
document uses: the form is a **보장성보험 and unsuitable as savings**, and **a 무해지 contract
cannot support a policy loan during the payment period** [REG-R28] [REG-R25 제33조](#krlib-reg-r25).

**The lapse assumption.** The 2024-11-07 계리가정 guideline is why a `[std]` lapse vector on
this product is defensible at all. It names the **로그-선형 모형** converging to **0.1%** at
납입완료 as the 원칙모형, sets the post-completion ultimate at **0.8%** or a 20% relativity,
and requires an insurer departing from it to disclose, quarterly and in its audit report, the
difference in **CSM, best-estimate liability, K-ICS ratio and net income** [R11] [REG-R27]. It
records that the 무·저해지 share of 보장성 초회보험료 ran **11.4% (2018) → 30.4% (2021) → 47.0%
(2023) → 63.8% (2024 H1)** [R11] [REG-R27]; 어린이보험 is not named, but every 무해지
어린이보험 form on the comparison board is inside its scope [S11]. The same release requires
loss ratios to be **split by age cohort** where experience is sufficient and the split is
statistically significant, with the worked example running 30s 89% → 40s 103% → 50s 140% → 60s
186% on 상해수술 [REG-R27] — which on a hundred-year child contract is not a refinement but the
main event.

**Product-design interventions specific to this line.** Four are datable and all four are in
this document. **2012-10-01**: all foetuses of a multiple pregnancy become insurable [R4].
**2015-06-17 → 2016-04**: the first-year 감액 is removed for foetal contracts across 17
carriers and 56 products [R2]. **2016-07-14**: sixteen carriers and nineteen products are
ordered to stop advertising cover before birth, under 보험업감독규정 제4-35조제3항 [R2].
**2023-07-19**: a 감독행정 restricts the use of the names 어린이보험 and 자녀보험 where the
maximum issue age exceeds 15, with existing products to be amended by the end of 2023-08 [R1].
**None of the four is a rule change**; all four are supervisory administration, and all four
changed the product.

**The 실손 separation.** From April 2018 실손의료보험 must be sold as a standalone product
consisting only of indemnity-medical cover, under 보험업감독규정 제7-63조제2항제1호 as amended
2017-03-22 with a one-year transition [R9] [R10] [REG-R17]. That is why a modern 어린이보험 has
no child-side 실손 rider [S2] [S3] [S4] [S5] [S6], why a Korean family buys the indemnity layer
separately as `Medical_KR_S`, and why the supervisor's 2008 worked claim — 43% of whose
₩16,836,420 was indemnity — cannot be reproduced by a current contract [R3].

**A non-life design rule visible in the product.** One carrier's summary of its own 사업방법서
states: 「질병을 원인으로 하는 사망을 특약으로 보장하고자 하는 경우에는 … (1) 보험기간은
**80세만기 이내**로 함 (2) 질병사망보험금의 한도는 **개인당 2억원 이내**로 함 (3) 만기시에
지급하는 환급금은 납입 보험료 합계액의 범위 이내로 함」 [S5]. This is why the 질병사망(부양자)
rider stops at 80 while the child's own cover runs to 100 or 110, and it is a constraint the
계약자-waiver design has to work within if it is written as a rider rather than as a clause.

**Pricing and rate filing.** Pricing is by **현금흐름방식** for any contract longer than three
years, with an adequacy analysis on 최적기초율 and projected cash flows [REG-R18
제7-64조제1호](#krlib-reg-r18). The **참조순보험요율** is filed by 보험개발원 with the FSC under 보험업법
제176조제4항 and an insurer applying it is deemed to have filed [REG-R4]; there is **no general
publication obligation**, but 제176조제9항 lets the bureau publish 순보험요율 산출 자료 where
policyholder protection requires it, and for **장기손해보험** it does — a dated display of
암 발생률, 질병입원율 and 후유장해 by age and sex, reaching 연령 0 and 10 [REG-R61]. This
product's research pass did not open it, so every incidence rate in this model is `[std]` as
an **unreconciled** construction rather than for want of a public grid [REG-R61] [REG-R34]. The
**산출방법서**, which holds each carrier's own 적용위험률 and 예정사업비율, is a 기초서류 and
is not disclosed [REG-R2]. What reaches the public is the **보험가격지수**, published in the
상품요약서 and on the comparison board under 감독규정 제7-45조제7항 [REG-R22] [S11], and the
specimen premium on the board's standardised basis [R12] [S11]. Commission is capped:
first-year remuneration may not exceed the first year's expected premium and instalment
structures pay no more than 60% of
the 표준해약공제액 a year [REG-R22 제4-32조제5항·제8항](#krlib-reg-r22) [REG-R29].

**Mortality basis.** The industry table — the **제10회 경험생명표**, applied to new business
from April 2024 — is **not published in full**; only summary statistics are released, and the
retrieved figures come through a trade newspaper [REG-R33] [REG-R34]. Every `mort_table.csv` in
`krlib` is therefore a `[std]` construction anchored on the public 국가데이터처 완전생명표
[REG-R38] [REG-R39] and on the gap those summary statistics imply, with a `provenance` column
on every row, and **the library's tables must never be presented as the 경험생명표** [REG-R33].
On this product the mortality basis carries three lives — the child, the 계약자 and, if the
mother module is on, the mother — and the child's is the one for which Korean public data is
thinnest.

**Measurement.** K-IFRS 제1117호 has been mandatory since 2023-01-01 [REG-R60], K-ICS since the
same date [REG-R13], and on top of both sits the **해약환급금준비금**, a company-level
appropriation inside 이익잉여금 of the excess of aggregate contractual surrender value over the
IFRS 17 liability [REG-R11]. A 무해지 child policy is precisely the shape that reserve was
built to catch — the gap negative for twenty years and steeply positive afterwards — and
precisely the shape whose CSM is most sensitive to the lapse assumption [REG-R27].
**`Child_KR_S` computes none of the three.** What it owes them is a projection re-runnable on a
re-set assumption basis at a stated 기준일, over a hundred-year horizon, with the lapse vector
and the two waiver decrements as explicit and separately switchable parameters.

**Tax, protection and the 2026 state intervention.** A 보장성 어린이보험 premium attracts a
**12% tax credit** — 15% for a 장애인전용보장성보험 — capped at **₩1,000,000 (100만원) of
premium a year**, under 소득세법 제59조의4제1항, on a contract whose 「만기에 환급되는 금액이
납입보험료를 초과하지 아니하는」 [REG-R57]. That is a **credit, not a deduction**, worth at
most ₩120,000 a year before the local surtax, and its qualifying test is the same economic test
감독규정 제1-2조제3호 uses to define a 보장성보험 [REG-R9] — which is why this product sits
cleanly on one side of the 저축성 / 보장성 line. Benefits are not modelled net of policyholder
tax. 청약철회 is the 15/30-day right of 금융소비자보호법 제46조 [REG-R51] and 품질보증해지 the
three-month right of 상법 제638조의3제2항 [REG-R49]; the 지정대리청구 service must be offered
wherever 계약자 = 피보험자 = 보험수익자 [S5] [S8], which on a child policy it never is, so it
is one of the few standard Korean provisions this product does not need. On insurer failure,
예금자보호법 covers **₩100,000,000** per person per insurer, in a bucket that expressly
excludes benefits payable because the term has ended [REG-R52] [REG-R25 제43조](#krlib-reg-r25). And from
**2026-04-01** every Korean insurer operates a **1%–5% 어린이보험 premium discount for one
year** on a birth, 육아휴직 or 육아기 근로시간 단축, part of a 「저출산 극복 지원 3종 세트」
whose expected consumer benefit is about **₩1,200억원 a year**, from whose companion
premium-deferral limb 어린이보험 is **expressly excluded** [R6]. Beyond the cash-flow effect
(footnote 20), that release matters for a second reason: it is a primary supervisory document
treating 어린이보험 as a **distinct, identifiable product class with its own premium
aggregate** — ₩9.4조원 against ₩42.7조원 for all 보장성 인보험 [R6] — which is what makes a
reference model of it worth building.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-child-r1
[R10]: #krlib-child-r10
[R11]: #krlib-child-r11
[R12]: #krlib-child-r12
[R2]: #krlib-child-r2
[R3]: #krlib-child-r3
[R4]: #krlib-child-r4
[R5]: #krlib-child-r5
[R6]: #krlib-child-r6
[R7]: #krlib-child-r7
[R8]: #krlib-child-r8
[R9]: #krlib-child-r9
[REG-R1]: #krlib-reg-r1
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R17]: #krlib-reg-r17
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R24]: #krlib-reg-r24
[REG-R25]: #krlib-reg-r25
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R40]: #krlib-reg-r40
[REG-R41]: #krlib-reg-r41
[REG-R48]: #krlib-reg-r48
[REG-R49]: #krlib-reg-r49
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R57]: #krlib-reg-r57
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
