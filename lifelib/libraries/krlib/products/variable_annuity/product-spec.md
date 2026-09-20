# Product Specification

**Status:** Draft, 2026-09-03. Every source cited below was accessed on **2026-09-03**.

**Scope note.** This is a *standardized composite specification* of a Korean individual
deferred variable annuity — 변액연금보험 (*byeonaek yeongeum boheom*) — assembled for
reference liability cash-flow modelling. It describes no single insurer's contract. Facts
carrying **[S#]** (primary product documents: 약관 (*yakgwan*, policy conditions),
상품요약서 (*sangpum yoyakseo*, the statutory product summary), 상품안내장 and 설명서) or
**[R#]** (product-specific regulatory and actuarial references) were extracted from the
cited document; both series are numbered in `sources.md` in this directory, which carries
forward the frozen numbering of `_research/variable-annuity.md`. **[REG-R#]** resolves
against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R1–R62 numbering is
distinct. Values marked **[std]** are standardizations introduced for the reference
implementation; every [std] table row carries a numbered footnote giving the rationale
and, where the research file brackets it, the observed range across insurers. Claims the
research file could not confirm against a retrieved document are flagged **[unverified]**
and stay flagged.

**Implementation anchor.** Eleven documents were read — ten from **six** current carriers,
plus the industry disclosure portal [S12]. The composite is built on two of them and takes
nothing structural from the rest:

- **The expense stack, the surrender-charge scale and the fund charges come from one
  carrier's 상품요약서** [S2]. It is the only retrieved document whose fee table,
  premium-allocation figures and surrender-value illustration **reconcile arithmetically
  against each other**, and the acquisition cost and the surrender charge are one quantity
  seen twice — the 해약공제 (*haeyak gongje*, surrender charge) is the unamortised
  acquisition cost [R2] — so they may not be taken from different carriers.
- **The guarantee design and both guarantee charges come from a second carrier's
  상품안내장** [S1]. It is the only retrieved document that prints a
  최저연금적립금보증 (GMAB) charge **as a formula**, and it also supplies the mandatory
  bond-weight ladder and the pre-annuitisation automatic de-risking rule. A guarantee
  charge is economically separable from an acquisition cost, so this join creates no
  inconsistency; [S1]'s guarantee base (premiums paid) is the base its 0.07% GMDB charge is
  priced against, and the pair travels together.

The two documents share one illustration point — 남자 40세, 기본보험료 ₩300,000, 10년납,
60세 연금개시 — which is the industry's standard illustration cell and is the anchor model
cell below. Four further shapes bracket the composite and are described but not modelled:
an unguaranteed contract with no GMAB at all [S4] [S5]; a monthly-ratchet GMAB funded by a
CPPI overlay with **no guarantee charge** [S6]; an elective GMAB the policyholder may
switch on and off [S9]; and the 실적배당 종신연금 (*siljeok baedang jongsin yeongeum*)
GLWB, in which the money stays in the separate account through the payout phase
[S2] [S7] [S8] [S10].

**What this document must be complete enough to do.** `technical-notes.md` derives the
recursions of `VA_KR_S` from this document alone, without returning to the research file, so
every parameter the model needs is tabulated here with its base, its timing and **the
account it lands in**.

---

## Product overview and market role

변액연금보험 is a two-period contract written on a **특별계정** (*teukbyeol gyejeong*,
separate account). Through the 연금개시 전 보험기간 — 「계약일부터 연금개시나이 계약해당일의
전일까지」 — the premium, net of a front-end expense deduction, is transferred into the
separate account and buys 좌 (*jwa*, units) at a daily 기준가격 (*gijun gagyeok*, unit
price); the policyholder's money is the 계약자적립액 (*gyeyakja jeongnibaek*, account
value), defined in the conditions as 「납입보험료에서 월공제액 및 인출금액 등을 공제한
금액을 특별계정의 운용실적을 반영하여 계산한 금액」 which 「특별계정의 평가 등에 따라 매일
변동할 수 있습니다」 [S7 제2조] [S4] [S5]. At the 연금개시나이 계약해당일 the accumulated
value — or a guaranteed floor where one was bought — becomes the annuity consideration,
and on the majority design the money **leaves the separate account for the 일반계정**
(*ilban gyejeong*, general account) and is run at the declared 공시이율 (*gongsi iyul*)
[S6] [R2].

The economic content is an investment wrapper plus two written options. The
**최저사망보험금보증** (*choejeo samang boheomgeum bojeung*, GMDB) floors the death
benefit at premiums paid and is **compulsory**: 보험업감독규정 제7-60조제7호 requires that
「변액보험 및 금리연동형보험(연금보험을 제외한다)의 경우 최저사망보험금 등을 설정하여야
한다」 [REG-R16] [R11], and all 36 products in the 2017 industry census carried one [R1].
The **최저연금적립금보증** (*choejeo yeongeum jeongnipgeum bojeung*, GMAB) floors the
annuity consideration at the annuity commencement date and is, since **April 2016**,
optional: 「2016년 4월 전에 판매한 변액연금에는 최저연금적립금 보증(GMAB)비용이
의무부과되었으나 이는 계약자 선택권을 제한한다는 의견이 제시되어 … 2016년 4월부터는
변액연금의 최저연금적립금(GMAB) 보증비용 부담여부를 계약자가 선택할 수 있다」 [R2], the
change following a 2014 감사원 audit direction that a way be found to reduce or remove the
charge [R1]. The same chassis therefore has to support a guaranteed and an unguaranteed
form, and the reference model carries the guarantee as a switch.

**The guarantee is not a floor on the account.** [R1] states the boundary in terms:
「만기에 적립된 금액이 최소보증금액보다 클 경우 보험회사는 이 적립금을 연금에 활용하거나
일시금을 지급하게 되는 것이다. 그러나 **만기 전에 사망 또는 해약이 발생하는 경우 이 보증은
성립하지 않으며**, 따라서 보험회사는 약정된 금액만을 보험계약자에게 지급하게 된다.」 The
GMAB is a European option struck on one date. Every retrieved product document says the
same thing in consumer language — 「연금개시 전 보험기간 중 중도해지시 해약환급금은
최저보증되지 않습니다」 [S1]; 「해지환급금은 특별계정의 운용실적에 따라 변동되므로 최저보증이
이루어지지 않으며, 원금손실이 발생할 수도 있습니다」 [S7 제50조제3항]; and the same in
[S6] [S8] [S10]. The 해약환급금 (*haeyak hwanreupgeum*, surrender value) of a Korean
variable annuity carries **no guarantee whatever**, and this is the single most important
fact about the product for a liability model.

**Market position.** Variable life insurance reached Korea in 2001, the variable annuity in
**October 2002** and the variable universal contract in 2003 [R1] [R2]. 변액보험 premium
income peaked at ₩17.9 trillion (17.9조원) in 2021 and fell every year after — ₩12.7tn
(2022), ₩12.2tn (2023), ₩11.6tn expected (2024), ₩10.1tn forecast (2025) — the decline
attributed to market uncertainty and explicitly to 「최저보증이율의 하락」 reducing demand
for guaranteed variable annuities [R9]; the cross-product forecast series puts the line at
₩12.4tn for 2026 [REG-R46]. *New* business moved the other way: 초회보험료 was ₩1.97tn in
2024 and **₩2.89tn in 2025, up 46.2%** [R3], against a published forecast of a 45.9% *fall*
[R9] — a standing warning against any Korean variable-annuity volume projection. The last
retrieved stock measurement is ₩109.1tn of 적립금 across about 8.3 million policies at
2016-09-30, 「국민 약 6명당 1건」 [R1].

**Conduct.** A shrinking in-force block beside a fast-growing new-business line draws
supervisory attention. The FSS ran a mystery-shopping exercise on variable-insurance sales
over September–November 2025 across nine of twenty-two life insurers, publishing the result
on 2026-03-24: overall grade 「양호」, the two weakest items being the explanation of
**변액보험의 자산운용 방식** and of the **위법계약해지권**; 1,308 variable-insurance
complaints in 2025, about **9%** of all life-insurance complaints [R3]. The product may be
sold only by a 변액보험판매관리사 (*byeonaek boheom panmae gwallisa*) who has passed the
생명보험협회 examination and does 「매년 1회 4시간 이상」 of refresher training
[R2] [R6] [S1], and a 적합성 진단 (*jeokhapseong jindan*, suitability diagnosis) must
precede any recommendation to an 일반금융소비자 [R2] [R3] [R14].

**Two behavioural facts that frame every assumption in the model.** 「변액보험의 7년 평균
유지율은 30% 미만으로 알려져 있다」 [R1], reported at second hand from a 2016 금융감독원
release that was not retrieved; and 「계약체결 후 적립금이 납입한 보험료인 원금에 도달하기
위해서는 약 7~10년의 기간이 걸릴 수 있으므로 중도 해지 시에는 원금에 미달할 가능성도
있다」 [R1]. The retrieved illustrations bear the second out exactly [S1] [S2].

**Where it sits in `krlib`.** This is the library's only product on which the policyholder
bears the investment risk, the only one carrying an option written on **investment
performance** — `Pension_KR_S`, `WholeLife_KR_S` and `Immediate_KR_S` each write a
최저보증이율 floor on a *declared* rate, and this product writes one of those too in its
payout phase — and the only one that **models** the 특별계정 / 일반계정 boundary. 감독규정
제5-6조제1항 also makes a separate account mandatory for the 연금저축계좌 of `Pension_KR_S`
(제1호, against 변액보험계약 at 제3호) [REG-R15], but that product neither cites the article
nor represents the boundary, so the two account ledgers below have no counterpart elsewhere
in the library. It is also the only product in the library **barred by regulation from the
무해지 / 저해지환급형 forms**:
감독규정 제7-66조제4항제1호 excludes 변액보험 from the dispensation permitting a surrender
value below the 별표 14 floor [REG-R19], so the cliff-shaped surrender curve that dominates
the library's protection products cannot appear here.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 무배당 변액연금보험, individual, 적립형 (level monthly premium), two periods | [S1] [S2] [S5] [S6] |
| Regulatory class | 생명보험상품 — 연금보험계약, 보험업법 시행령 제1조의2제2항 | [REG-R7] |
| Separate-account basis | 변액보험계약; a **mandatory** 특별계정 class under 감독규정 제5-6조제1항제3호, enabled by 보험업법 제108조제1항제3호 | [REG-R15] [REG-R6] [R4] |
| Participation | 무배당 (*mubaedang*, non-participating) | [S1] [S2] [S4] [S5] [S6] [S9] |
| Guarantee form | 최저연금적립금 **보증형** — GMAB elected at issue and fixed for the term; the 미보증형 is a model switch | **[std]** (1) |
| Guarantee level rule | Premium refund at **100%** of 이미 납입한 보험료 | **[std]** (2) |
| 구좌 (*gujwa*, contract unit) | One | **[std]** (3) |
| Age basis | **보험나이** (*boheom nai*) — age nearest birthday on the six-month rule of 표준약관 제21조; 만나이 only for 계약의 무효 | [REG-R25] |
| 가입나이 (issue age) | 만15세–70세 | [S1] [S2] |
| 연금개시나이 | 45–80 | [S1] [S5] [S6] [S9] |
| 납입기간 (premium term) | 5 / 7 / 10 / 12 / 15 / 20년납 | [S1] [S2] |
| Minimum 거치기간 (deferral after 납입완료) | 7 years on the 보증형; 5 years on a 5년납 contract | [S1] |
| 연금개시 전 보험기간 | 계약일 to the day before the 연금개시나이 계약해당일 | [S4] [S5] [S7] |
| 연금개시 후 보험기간 | 연금개시나이 계약해당일 to death (종신연금형) | [S4] [S5] [S7] |
| Underwriting | No medical basis is published; 계약 전 알릴 의무 under 표준약관 제13조–제14조 applies, and the **적합성 진단** is the operative gate | [REG-R25] [R2] [R14]; depth **[unverified]** |
| Distribution channel | 전속설계사 (tied agent) | **[std]** (4) |
| Sales licence | 변액보험판매관리사 only — 「이 상품은 생명보험협회에서 실시하는 자격시험에 합격한 모집 종사자에 한하여 판매할 수 있는 상품입니다」; 보험업법 제83조, 시행령 제56조, 감독규정 제5-4조 | [S1] [R2] [R6] |
| Currency | KRW | all sources |
| Deposit protection | Outside 예금자보호법 **except** the contractually guaranteed amounts (최저사망적립액, 최저연금적립액 and riders), to ₩100,000,000 (1억원) per person per insurer | [S5] [S6] [R2] [REG-R52] [REG-R32] |
| **Anchor model cell** | 남자, 보험나이 40 at issue; 기본보험료 ₩300,000 월납; 10년납 (120 premiums, ₩36,000,000 = 3,600만원 cumulative); 연금개시나이 60 (240 months pre-annuitisation, 120 months deferral); 보증형; 채권형 50% / 주식형 50% | **[std]** (5) |

Footnotes to [std] rows:

1. The retrieved current products divide as follows: guarantee charged and fixed at issue
   [S1] [S10]; electable and revocable an unlimited number of times at 연 0.85% of the
   account value while on [S9]; present but **unfunded**, paid for with a CPPI overlay
   [S6]; and no GMAB at all [S4] [S5]. The 2017 census of all 36 products on sale found
   **27** guaranteeing the annuity fund, 3 of those letting the policyholder decline, and
   **9** with no GMAB [R1] — the report gives 26 in one place and 27 in another, and the
   discrepancy is in the source. The composite takes the **charged, issue-fixed 보증형**: it
   is the only shape exercising a guarantee charge, a base and a payout in one run, the
   elective form has no retrieved take-up data, and the CPPI form replaces the charge with
   an asset rule a single deterministic path cannot distinguish from a fixed allocation.
2. Four level rules are documented — **premium refund**, **step-up**, **ratchet** and
   **roll-up** [R1 <표 Ⅲ-2>](#krlib-variable_annuity-r1), all four set out under "Contractual mechanics" — and 22 of
   the 36 census products set the guarantee **above** premiums paid [R1]. The composite
   takes premium refund at 100% because it is the textbook identity 「연금개시시
   계약자적립금(최저보증 포함) = Max(기납입보험료, 연금개시시 계약자적립금)」 [R2], because
   it is the level the only retrieved charged-GMAB contract uses [S1], and because it is
   the only rule whose strike is a modelled quantity rather than a second recursion. The
   others are carried as variants, since [R1]'s fifteen-year worked comparison shows that
   **the guarantee design, not the guarantee level, drives the option cost**.
3. Korean variable annuities are written in 구좌 — repeatable units of the basic premium,
   with the withdrawal residual floor and the maximum basic premium both expressed per 구좌
   [S1] [S2] [S10]. One 구좌 keeps the model point one contract.
4. The 계약체결비용 taken below is a tied-agent level. Bancassurance and online acquisition
   costs were capped at **50%** of the tied-agent level from 2016 [R1], and the one variable
   annuity [R1] found buyable directly online carried 계약체결비용 of **1.3%** of the basic
   premium against the 5.17–6.12% of the tied-channel documents retrieved here — roughly a
   quarter of the price, with **no acquisition commission at all**. Channel is a first-order
   parameter and is named rather than left implicit.
5. 남자 40세 / 기본보험료 30만원 / 10년납 / 60세 연금개시 is the illustration point three
   independent carriers publish [S1] [S2] [S6], which makes it the only cell at which the
   composite's parameters can be checked against published surrender-value tables. The
   20-year pre-annuitisation period puts the contract in the **>12년** band of the mandatory
   bond ladder, where the 채권형 floor is 50% [S1] [R1], so a 50/50 allocation sits exactly
   on the constraint. Ten years of premiums with ten of deferral exercises the step in the
   monthly deduction at 납입완료 (*nabip wallyo*), the feature of the Korean expense stack a
   model most easily gets wrong.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| 기본보험료 (basic premium) | ₩300,000 per month, level, in advance | anchor **[std]** (5); it is also this carrier's minimum [S1] |
| Observed minimum 기본보험료 | ₩50,000 [S2] · ₩100,000 [S4] [S10] · ₩200,000 [S5] [S6] · ₩300,000 [S1] · ₩500,000 below 10년납 [S9] | [S1] [S2] [S4] [S5] [S6] [S9] [S10] |
| Maximum 기본보험료 | ₩1,000,000 per 구좌 | [S1] [S2] [S9] |
| Mode | Monthly (월납) | [S1] [S2] |
| 납입기간 | 10 years — 120 premiums | anchor **[std]** (5) |
| 추가납입보험료 (*chuga nabip*, additional premium) | Permitted to **200%** of basic premium paid and payable, cumulative; **no loading** | [S1]; cap universal [S1] [S2] [S4] [S5] [S6] [S7] [S10] |
| Additional-premium headroom | Increased by the cumulative amount of any 중도인출 | [S1] [S2] [S4] [S5] [S6] [S7] |
| 선납 (prepayment) | Not more than 6 months, so the 월적립식 tax route stays open | [REG-R58] |
| 예정이율 (pricing interest rate) | **None.** A variable annuity's accumulation account is the fund; a full-text search of the 감독규정 returns zero occurrences of 예정이율, which speaks only of the 계약자적립액 적용이율 | [REG-R48] [REG-R9] |
| Payout-phase crediting rate | 공시이율, declared monthly off the 공시기준이율 | [S1] [S5] [REG-R18] [REG-R24] |
| 최저보증이율 (payout phase) | 경과 5년 미만 1.00% / 5–10년 0.75% / 10년 이상 0.50%, 연복리 | [S1] |
| 보험료 납입 일시중지 (premium holiday) | After 5 years; 12 months per request; up to 3 requests. During the holiday the 위험보험료, both guarantee charges, the 부가보험료 excluding 기타비용 and any rider premium are taken from the surrender value, and the holiday ends if they cannot be met. The premium term extends; if that would breach the minimum deferral, the annuity age defers | [S1] |
| 보험료 납입중지 (permanent cessation) | After 10 years, and only where 계약자적립액 ≥ 100% of 이미 납입한 보험료 | [S1] |
| 보험료 납입종료 (early release from the premium obligation) | On 퇴직, 폐업 or an accident or illness needing three months or more of hospital or convalescent care, applied for within six months and after half the premium term; separately after 5 years where the surrender value is ≥ ₩5,000,000 per 구좌 | [S1] |
| 보험료 납입면제 (premium waiver) | **Not** in the base contract — 「변액연금에는 … 납입면제기능은 없는 것이 일반적」; available as a rider | [R2]; riders [S2] [S5] [S6] [S10] |
| 보험계약대출 (policy loan) | Within the surrender value on the insurer's terms; units are cancelled from the separate account unless the general-account loan rider is taken | [REG-R25 제33조](#krlib-reg-r25) [S5] |

### Charges — the fee stack a 상품요약서 discloses

A savings-type variable contract must publish a **수수료 안내표** covering 보험관계비용
(계약체결비용, 계약관리비용, 위험보험료), 특별계정운용비용 (특별계정 운용보수, 기초펀드
보수·비용, 증권거래비용 등), 보증비용, 연금수령 기간 중 비용 and 해약공제비용, either in
the 생명보험협회 공제금액구분공시 screen or inside the 상품요약서, and must repeat it in
the 상품설명서 handed over at the point of sale [R2]. The composite reproduces that table.
**The five lines the task of modelling this product turns on are separate rows because they
are deducted from different bases at different times and land in different accounts.**

| Line | Rate | Base | Timing and point of deduction | Account | Basis |
|---|---|---|---|---|---|
| 계약체결비용 (*gyeyak chegyeol biyong*, acquisition cost) | **5.17%** (₩15,510) | 기본보험료 | Monthly, **deducted from the premium before it reaches the fund**, for 10 years from the contract date, nil thereafter | 일반계정 | [S2] |
| 계약관리비용 — 납입기간 이내 (*gyeyak gwalli biyong*, maintenance) | **3.50%** (₩10,500) | 기본보험료 | Monthly, deducted from the premium, during the premium-paying period | 일반계정 | [S2] |
| 계약관리비용 — 납입기간 이후 | **1.33%** (₩3,990; the document prints ₩4,000) | 기본보험료 | Monthly, **from the 계약자적립액 on the 월계약해당일**, after 납입완료 | 특별계정 → 일반계정 | [S2] [S7 제2조] |
| 기타비용 | Nil in the base run | — | Deducted from the premium where charged | 일반계정 | **[std]** (6) |
| 위험보험료 (*wiheom boheomnyo*, risk premium) | **0.004%–0.011%** of 기본보험료 (₩12–₩32) | 기본보험료, on a natural-premium scale by attained age | Monthly, in the 월공제액, from the 계약자적립액 on the 월계약해당일 | 특별계정 → 일반계정 | [S2] [S4]; scale **[std]** (7) |
| 최저사망보험금 보증비용 (GMDB charge) | **연 0.07%**, taken as 0.07%/12 a month | 특별계정 계약자적립액 | Monthly, in the 월공제액 | 특별계정 → 일반계정 (보증준비금) | [S1] [R2] |
| 최저연금적립금 보증비용 (GMAB charge), asset component | **연 0.25%**, taken as 0.25%/12 a month | 특별계정 계약자적립액 | Monthly, in the 월공제액 | 특별계정 → 일반계정 (보증준비금) | [S1] |
| 최저연금적립금 보증비용, premium component | **연 0.30%**, taken as 0.30%/12 a month = ₩9,000 a month on the anchor cell | **보험료총액** — 「이미 납입한 보험료(특약보험료 제외) 및 추후 납입할 기본보험료 합계」, i.e. ₩36,000,000 | Monthly, in the 월공제액, **for at most 7 years** | 특별계정 → 일반계정 (보증준비금) | [S1] |
| 특별계정 운용보수 (*teukbyeol gyejeong unyong bosu*) | 채권형 **연 0.40%**; 주식형 **연 0.60%**; blended **연 0.50%** at the anchor allocation | 특별계정 순자산 | **Daily**, at rate/365, taken out of net assets before the 기준가격 is struck | 특별계정 → 일반계정 | [S2]; blend **[std]** (8) |
| 증권거래비용 및 기타비용 | Nil in the base run; observed 연 0.00%–0.79% | 특별계정 자산 | On occurrence; borne directly by separate-account assets under 자본시장법 제188조 and 시행령 제265조 | 특별계정 → third parties | [S2] [S4] [S7 제44조]; **[std]** (9) |
| 기초펀드 보수·비용 | Nil in the base run; observed 연 0.01%–0.45% | Underlying fund net assets | Daily, inside the underlying fund | 특별계정 → third parties | [S2] [S4]; **[std]** (9) |
| 해약공제 (surrender charge) | `₩830,000 × (n − k) ÷ n` in completed whole years `k`, nil from `k = n`, with `n` = min(납입기간, 7) = 7 on the anchor cell | A level amount, run off linearly | On surrender, deducted from the 계약자적립액 | 특별계정 → 일반계정 | [S2]; form [R1] [R2]; **[std]** (10) |
| 중도인출 수수료 | **None** | — | — | — | [S1] [S2] [S9] |
| 펀드변경 수수료 | ≤ 0.1% of the amount transferred, capped at ₩5,000, four free a year | Amount switched | On switch | 특별계정 → 일반계정 | [S1] [S2] |
| 추가납입보험료 수수료 | **None** | — | — | — | [S1] |
| 연금수령기간 중 계약관리비용 | **연금 연액의 0.5%** | Annuity payable | Deducted from each annuity payment | 일반계정 | [S4]; adoption **[std]** (11) |

6. No retrieved 상품요약서 quantifies 기타비용 separately; [R2]'s cash-flow identity names
   it and [S7 제2조] confirms it is deducted at premium payment, but no rate was retrieved.
   Set to zero so the composite's premium allocation reproduces the observed ratio exactly;
   the line is kept because the identity needs it.
7. The 위험보험료 buys only the 고도재해장해급여금 below and, on the retrieved contracts
   that carry no basic death benefit, nothing else — which is why it is 0.004%–0.011% of
   the basic premium, ₩12 to ₩32 a month, and why the textbook can say the natural premium
   is immaterial and the premium allocation therefore flat by age [R2]. The **scale by
   attained age is [std]**: no retrieved document publishes a rate, and the 제10회
   경험생명표 is not public [REG-R33] [REG-R34]. The composite takes **0.0080%**, ₩24 a
   month — inside the published band and a little above its arithmetic mid-point of 0.0075%
   (₩22.50) — held level at the anchor age; the technical notes specify the age scale.
   An online product covering more carries 0.0217%–0.0397% [R1], which brackets the top.
8. Observed 특별계정 운용보수 across five documents: 0.20–0.78% [S4]; 0.25–0.64% [S9];
   0.32–0.89% [S5]; 0.345–0.815% [S1]; 0.40–0.70% [S2]. The composite takes the anchor
   carrier's own two funds — 채권형 0.40% and a 주식형 at 0.60% [S2] — and the **50/50
   blend of 0.50%** follows from the allocation. Every carrier publishes the fee split into
   운영보수 / 투자일임보수 / 수탁보수 / 사무관리보수 and states that the last three are
   maxima with actual cost charged [S1] [S5] [S9]; the model carries the total only.
9. Both lines are **ex-post estimates of actual spend**, not contractual rates — [S2] states
   its 증권거래비용 figures are estimated from FY2023 spend and its 기초펀드 보수·비용 from
   the FY2023 investment mix — so setting them to zero keeps the modelled charges
   contractual. The omission understates the drag by up to about 0.5 percentage points a
   year at the top of the observed ranges, and the technical notes say so.
10. Three scales were retrieved, all on the anchor cell and all the same function
    `C × (7 − t) ÷ 7`: **C = ₩830,000** [S2] (19.5% of premiums paid at year 1), **C =
    ₩1,077,000** [S5] (25.6%, reproducing the 2017 industry **mean** row exactly) and
    **C = ₩1,180,000** [S4] (28.1%, above the 2017 maximum), against a 2017 census range of
    19.1%–27.6% with a mean of 25.6% [R1 <표 Ⅴ-2>](#krlib-variable_annuity-r1). The composite takes **[S2]'s
    C = ₩830,000** — not the market mean — because the 해약공제 is the unamortised
    계약체결비용 [R2] and the two must come from one carrier: pairing [S2]'s 5.17%
    acquisition cost with [S5]'s surrender charge would recover more on surrender than was
    ever loaded. The composite is therefore a **cheap tied-channel contract at both ends**,
    and the technical notes state the direction of that bias. All three sit inside the
    statutory 표준해약공제액 cap on the anchor cell (below), at 50%, 66% and 72% of it.
11. Two forms are published: **연금 연액의 0.5%** [S4] and 구좌당 매월
    min(영업보험료의 3.5%, ₩4,000) [S2]. The composite takes the proportional form: it is
    scale-free and needs no reference to a premium that has stopped being paid.

**The 표준해약공제액 cap.** 감독규정 제7-66조제1항제3호 requires the 해약공제액 to be the
**표준해약공제액** of 별표 14, and 제1항제2호 caps the 해약공제기간 at **7 years** where
the premium term is 7 years or more [REG-R19]. 별표 14 gives 표준해약공제액 = 연납순보험료의
5% × 해약공제계수 + 보장성보험의 보험가입금액의 10/1000, with — for a 저축성보험 — the
해약공제계수 equal to the premium term capped at 12 and the 연납순보험료 computed over a
premium term capped at 10, excluding the level-spread 부가보험료 [REG-R20]. On the anchor
cell the 부가보험료 is 8.67% of the basic premium, so 연납순보험료 = ₩3,600,000 × (1 −
0.0867) = ₩3,287,880 and the cap is **5% × ₩3,287,880 × 10 = ₩1,643,940**, against which
the representative `C` of ₩830,000 is 50.5%. The 보장성 term would add at most ₩100,000 on
the ₩10,000,000 재해장해 benefit; whether a disability-only benefit has a 보험가입금액 for
별표 15 purposes was not worked in any retrieved document and is **[unverified]**
[REG-R21]. Note 6 to 별표 14 further requires that, where the acquisition cost is loaded
onto the premium over the premium term — which is exactly what a 5.17% monthly
계약체결비용 does — the amount so loaded be **discounted at the 평균공시이율 and subtracted
from the cap**; no retrieved document works that netting, and the exact residual cap is
**[unverified]**. The observed scales are quoted as published and the statutory cap is
recorded beside them.

**First-year charge total on the anchor cell**, as a check on the stack: 계약체결비용
₩186,120 + 계약관리비용 ₩126,000 + 위험보험료 ₩288 + guarantee charges ₩113,576.29
(₩108,000 of it the premium-based GMAB component, the other two being struck on an account
still being built) = **₩425,984.29 on ₩3,600,000 of premium, 11.83%**, which is the figure
`technical-notes.md` traces line by line. [R1] puts the industry band at 「선취상품은
납입보험료의 5~15%를 … 차감한 후 85~95%만 투자」, and the composite's premium allocation of
**91.33%** sits inside the 91.3%–91.5% observed at three carriers on this cell
[S1] [S2] [S6].

### The separate account and the fund menu

| Parameter | Representative value | Basis |
|---|---|---|
| Funds modelled | **2** — 채권형 (bond) and 주식형 (equity) | **[std]** (12) |
| Allocation at issue | 채권형 50% / 주식형 50%, no rebalancing in the base run | **[std]** (12) |
| Mandatory 채권형 minimum | By 연금개시 전 보험기간: **<12년 → ≥80%; =12년 → ≥70%; >12년 → ≥50%**; binds both the premium allocation and the account mix, and survives every later switch | [S1] [R1 푸르덴셜 VIP](#krlib-variable_annuity-r1) |
| Selection at issue | Up to 3 funds including a 채권형, in 5% steps; each fund's share of the basic premium at least ₩50,000 | [S1] [S5] |
| Menu size in the market | 5 [S4] · 8 [S1] · 9 [S2] [S9] · 49 [S5] · 51 [S10] | [S1] [S2] [S4] [S5] [S9] [S10] |
| 좌 (unit) | 1원 = 1좌 at establishment; thereafter transfers in and out are in units at the daily 기준가격 | [S7 제43조제1호] [R2] |
| 기준가격 | 당일 특별계정 순자산가치 ÷ 특별계정 총좌수, quoted **per 1,000좌**, rounded to two decimal places (round-half-up at the third); opening price **1,000원 per 1,000좌** on the first day of sale; 순자산가치 is total assets **less the 특별계정 운용보수** | [S7 제43조제2호] [R2] |
| Valuation frequency | **Daily** | [S7 제37조] [S7 제42조] [R2] |
| Valuation basis | Market value under 자본시장과 금융투자업에 관한 법률, fund by fund; amortised cost plus accrued interest where no price is observable | [S7 제42조] [R2] |
| Base-run gross asset return | **3.00% p.a.**, constant | **[std]** (13) |
| Implied 투자수익률 (기준가격 return) | **2.50% p.a.** = gross less the blended 0.50% 운용보수, as a subtraction; on the model's own monthly compounding the realised figure is 2.49% | **[std]** (13) |
| Implied 순수익률 | **2.18% p.a.** = 투자수익률 less the two account-based guarantee charges (0.07% + 0.25%) | [S1]'s definition; **[std]** (13) |
| Mandated illustration returns | **−1.00% / 2.50% / 3.75%** — 「−1%, 평균공시이율, 평균공시이율의 1.5배」 at a 2026 평균공시이율 of 2.50% | rule [R2]; 평균공시이율 [REG-R48] |
| 펀드변경 (switch) | Priced at 변경요구일 + 제2영업일 기준가격; ≤0.1% capped ₩5,000, four free a year | [S1] [S5] [S7 제39조] |
| 펀드자동재배분 | Available on a 3-, 6- or 12-month cycle; **off in the base run** | [S5] [S7 제40조]; **[std]** (14) |
| Pre-annuitisation automatic de-risking | From 「연금지급개시일 − 3년」, on each annual 계약해당일, 채권형 is topped up to **80%** of total account value if it is below it | [S1] |
| 펀드자동전환옵션 (target de-risking) | 110%–200% target in 10% steps; **off in the base run** | [S5]; **[std]** (14) |
| 평균분할투자 | Additional premium fed from a short-duration bond fund over 3, 6 or 12 months; out of scope | [S7 제41조] |
| Separate-account wind-up | Permitted only on stated grounds, including **원본액 below ₩5,000,000,000 (50억원)** at the first anniversary or for a continuous month thereafter; switching fee and annual switch count waived on transfer | [S7 제45조] |
| Policyholder rights over asset management | None — 「계약자는 특별계정의 자산운용방법에 대해서는 일체의 관여를 할 수 없습니다」 | [S7 제37조] |

12. Two funds is the minimum that exercises a pro-rata allocation, a per-fund charge and
    the mandatory bond floor at once; real menus run from 5 to 51. The 50/50 split is the
    **binding** value of the >12년 bond ladder [S1], chosen so the constraint is visible
    rather than slack; no retrieved document prescribes an allocation. With no rebalancing,
    the drift of the realised mix away from 50/50 is itself a modelled quantity — which is
    what the automatic de-risking rules exist to control.
13. **Every return assumption in this product is [std].** The only realised returns
    retrieved are the top of a cross-sectional distribution in a trade news article —
    domestic equity 71.32% / 49.01% / 48.04% and overseas equity 44.61% / 44.16% / 43.08%
    annualised at 2026-04-30 [R10] — and one live fund panel showing the opposite, a
    기준가격 of **904.24원 against the statutory 1,000.00 opening price after fourteen
    years**, 연평균 −9.58% [S11]. No volatility, no correlation and no time series was
    retrieved. The base run therefore sets the **투자수익률 to the 2026 평균공시이율 of
    2.50%** [REG-R48], the middle of the three returns a Korean variable illustration must
    show [R2], and works back to a gross asset return of 3.00% so that the 운용보수 is a
    modelled cash flow rather than an assumption. That the disclosed 투자수익률 is already
    net of the 운용보수 is inferred: [S6]'s illustration shows a gross-to-net gap of
    **0.01 pp** on a product with no GMAB charge and no death cover, far too small to
    contain a 0.4% management fee, while [S1]'s gap of **0.32 pp** is exactly its two
    account-based guarantee charges.
14. Both automatic mechanics change the asset mix as a function of the account value, so
    both make the fund return path dependent on the guarantee's moneyness. They are
    specified in full under "Contractual mechanics" and left off in the base run, because a
    single deterministic path cannot distinguish their effect from a different fixed
    allocation. The pre-annuitisation de-risking at 「개시일 − 3년」 is **not** optional and
    is on.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| 사망보험금, 연금개시 전 | **Max(계약자적립액, 이미 납입한 보험료)** — the account value with the premiums paid as a floor | [S1] [S4] [S10] [R2] |
| 기본사망보험금 | **None.** The contract carries no death cover beyond the guarantee floor | **[std]** (15) |
| 이미 납입한 보험료 (the GMDB base) | 기본보험료 plus 추가납입보험료 actually paid, **excluding 특약보험료**; reduced for 중도인출 and 감액 (below) | [S1] [S4] [S7 제2조] |
| 고도재해장해급여금 | **₩10,000,000 (1,000만원) per 구좌, once only**, on the 고도재해장해 state | [S1] [S2] |
| 최저사망보험금 보증비용 | 연 0.07% of the separate-account account value, monthly | [S1] |
| GMDB after annuitisation | Ceases on the representative design, the cover extinguishing at 연금개시 — 「일반적으로 연금개시 후 보장은 소멸됨」 | [R2]; variant [S2] [S7] [S10] |
| 최저연금적립금 (GMAB) | **Max(계약자적립액, 이미 납입한 보험료)** at the 연금개시나이 계약해당일, **on survival to that date only** | [S1] [R1] [R2] |
| GMAB availability on early exit | **Void.** Not payable on surrender, lapse or death before the annuity commencement date | [S1] [S6] [S7 제50조제3항] [S8] [S10] [R1] |
| GMAB availability on 조기연금개시 | **Forfeited** — 「조기연금개시 신청시, 최저연금적립액은 보증되지 않습니다」 | [S1] |
| 최저연금적립금 보증비용 | 연 0.25% of the account value **plus** 연 0.30% of 보험료총액 for at most 7 years, both monthly | [S1] |
| 연금재원 (annuity consideration) | The 계약자적립액 at the 연금개시나이 계약해당일, floored at the GMAB, **transferred from the 특별계정 to the 일반계정** | [S6] [R2]; adoption **[std]** (16) |
| Payout form | **종신연금형 10년 보증기간부, 정액형** | menu [S1] [S2] [S5]; pick **[std]** (17) |
| Annuity basis | 연금사망률 (연금생명표) and 공시이율 in force **at annuitisation**, per the 산출방법서; the mortality basis may be re-struck at annuitisation but **only in the policyholder's favour** | [S1] [S2] [S5] |
| Annuity amount thereafter | Moves with the 공시이율, which is re-declared; 「연금개시후 보험기간의 공시이율이 한번이라도 변경된 경우 해당 연도의 연금연액은 … 차이가 있을 수 있습니다」 | [S5] |
| Death inside the 보증기간 | The remaining instalments are paid on their due dates, or may be commuted at the 공시이율 | [S2] [S5] |
| Death after the 보증기간 | The contract extinguishes with no further payment | [S1] [S5] |
| 자살면책 | 2 years from the 보장개시일 | [S5] [S6] |
| Payment where an exclusion bites | The 계약자적립액 at the date of death, without the guarantee floor | **[std]** (18) |

15. Three shapes are in the market: **no death cover, a 재해장해 benefit only**, with the
    account value paid on death subject to the GMDB floor [S1] [S2] [S6 1종(무사망형)]
    [S7 제3조]; a **기본사망보험금 proportional to premium** — 적립형 기본보험료의 10배,
    거치형 기본보험료의 10% — added to the account value [S5] [S6 2종(기본형)]; and the
    general rule 「사망보험금 = 기본사망보험금 + 사망 시점까지 적립된 계약자적립금」 with
    the observation that 「최근에는 환급률 제고를 위해 기본사망보험금 대신 장해보험금을
    지급하는 형태로 설계하는 상품이 더 많다」 [R2]. The composite takes the first: it is
    the shape of both anchor documents, it is what makes the 위험보험료 immaterial, and it
    isolates the GMDB as the only mortality-contingent guarantee in the model. Adding a
    basic death benefit is a one-line change and is a documented variant.
16. The alternative — keeping the money in the separate account through the payout phase
    and guaranteeing a lifetime withdrawal (실적배당 종신연금 / GLWB) — is offered by four
    of the retrieved carriers [S2] [S7] [S8] [S10] and is set out in full under
    "Contractual mechanics". The composite takes the general-account transfer because [R2]
    identifies it as the market default — 「대부분의 변액연금상품은 연금개시 이후 일반계정의
    공시이율을 반영하여 계산된다」 — and because the GLWB changes the product's economics
    entirely: [S2]'s GLWB charge is **연 3.30%** of the guarantee base for twenty years and
    1.70% thereafter, an order of magnitude above every GMDB charge retrieved and four
    times the dearest GMAB charge, and the same document's illustration never reaches a
    100% return of premium in twenty years at either illustration return.
17. The menu is uniform across carriers: 종신연금형 보증기간부 (10 / 15 / 20 years, to age
    100, or 기대여명보증; 정액형 or 체증형 at 3%, 5% or 10%); 종신연금형 보증금액부;
    확정연금형 (5 to 60 years by carrier); 상속연금형 (interest only, account paid on
    death); and a front-loaded 노후설계자금 slice, two forms being combinable in 10% steps
    [S1] [S2] [S4] [S5] [S6]. The composite takes the 10-year-guaranteed level lifetime
    annuity: it is the modal election, the only form exercising both longevity and a
    guarantee period, and the form the 소득세법 종신형 연금보험 route is written around,
    that route requiring any guarantee period to sit **within the published 기대여명 연수**
    [REG-R58].
18. No retrieved document states what is paid on an excluded death. The composite pays the
    계약자적립액 without the GMDB top-up — the treatment 표준약관 제22조 prescribes where a
    benefit becomes impossible [REG-R25], with 상법 제736조 as the floor [REG-R50]. The
    choice is **[std]**; the exclusion itself (2-year 자살면책) is sourced [S5] [S6].

### Options

| Option | Representative treatment | Basis |
|---|---|---|
| 추가납입 (additional premium) | **In scope, off in the base run.** ≤200% of basic premium paid and payable, no loading, headroom restored by withdrawals | [S1]; **[std]** (19) |
| 중도인출 (*jungdo inchul*, partial withdrawal) | **In scope, off in the base run.** 12 a policy year from one month after the contract date; ≤50% of the 해약환급금; residual ≥ ₩5,000,000 per 구좌; cumulative withdrawals ≤ premiums paid within the first 10 years; no fee | [S1]; **[std]** (19) |
| 펀드변경 | In scope; four free switches a year | [S1] [S2] |
| 펀드자동재배분 · 펀드자동전환옵션 | Described, off in the base run | [S5] [S7 제40조]; **[std]** (14) |
| 감액 (reduction of the basic premium) | In scope as a mechanic; releases the surrender value of the reduced part and **re-bases both guarantees** | [S4] [S7 제2조] |
| 조기연금개시 (early annuitisation) | Described, not modelled. Requires ≥7 years elapsed (10 where 납입종료 was used), premiums complete, and 계약자적립액 **≥110% of premiums paid**; from age 45; the account moves wholly to the bond fund on application; **the GMAB is forfeited** | [S1]; **[std]** (20) |
| 일반계정 전환 (voluntary transfer before annuitisation) | Described, not modelled — offered at 130% of premiums paid, or above premiums paid after two years, irreversibly | [R1] [S6] |
| 보험계약대출 | Described, not modelled | [REG-R25 제33조](#krlib-reg-r25) [S5] |
| 성과보너스 / 장기유지 보너스 | Out of scope | [S9] [S7 제6조] |
| 연금전환 / 상속·확정 payout forms | Out of scope; the base run takes the 종신연금형 | [S1] [S2] [S5] |

19. Both are switched off so the base run's account recursion is a clean function of
    premium, charges and return, and both are retained as active terms because each
    **leaks the guarantee**. [R1] is explicit that the withdrawal facility is a
    guarantee-risk mitigant and not only a convenience: 「중도인출은 정해진 한도하에서 연
    12회까지 허용되며, **중도인출금은 최저보증한도에서 차감된다**.」 A model that omits the
    adjustment lets a policyholder withdraw the fund and keep the strike.
20. Every retrieved 조기연금개시 condition is an **in-the-moneyness test** — 계약자적립액
    ≥110% of premiums [S1], 해약환급금 ≥100% of premiums [S9], 해지환급률 ≥100% and
    ≥₩5,000,000 [S10], with one carrier offering it on the 미보증형 only [S10]. The insurer
    will let a policyholder annuitise early only where the guarantee is out of the money.
    That is a policyholder-behaviour lever a stochastic model must respect and a
    deterministic one cannot exercise, so it is documented and excluded.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 해약환급금 | **max(0, 계약자적립액 − 해약공제액)**; the zero floor is statutory — 「계약자적립액에서 해약공제액을 공제한 금액이 음(陰)의 값인 경우에는 이를 영(零)으로 처리한다」 | [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) [S2] |
| Guarantee on the surrender value | **None**, at any duration | [S1] [S6] [S7 제50조제3항] [S8] [S10] |
| 해약공제액 | `₩830,000 × (n − k) ÷ n`, `k` = completed whole years, `n` = min(납입기간, 7); nil from `k = n` | [S2]; **[std]** (10) |
| 해약공제기간 | 7 years — the statutory ceiling where the premium term is 7 years or more | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) [R2] |
| 무해지 / 저해지환급형 | **Not permitted.** 변액보험 is excluded from the dispensation by 제7-66조제4항제1호 | [REG-R19] |
| Pricing of a surrender | 해지신청일 + 제2영업일 기준가격 | [S7 제50조제2항] [S9] |
| Payment | Within 3 business days of the claim | [S7 제50조] [REG-R25 제32조](#krlib-reg-r25) |
| Surrender-value table | The insurer must give the policyholder a table of surrender values by elapsed duration | [S7 제50조제6항] [REG-R25 제32조제3항](#krlib-reg-r25) |
| Single-premium contracts | Carry **no** 해약공제 at all, the whole 계약체결비용 having been taken at issue | [S5] [R1] |
| 청약철회 (*cheongyak cheolhoe*, cooling off) | Within **15 days** of receiving the 보험증권 and never after **30 days** from the application date; effective on despatch; premiums returned within 3 business days | [REG-R51] [REG-R25 제17조](#krlib-reg-r25) |
| 품질보증해지 (*pumjil bojeung haeji*) | Within **3 months** of formation where the 약관 was not delivered, its important content not explained, or the application not signed | [REG-R25 제18조제3항](#krlib-reg-r25) [REG-R49 제638조의3](#krlib-reg-r49) |
| 위법계약해지 | Where the seller breached 적합성원칙, 적정성원칙, 설명의무, 불공정영업행위 금지 or 부당권유행위 금지; the **계약자적립액** is returned, not the 해약환급금 | [R3] [R14] [REG-R25 제29조의2](#krlib-reg-r25) |
| 납입최고 and 해지 | Demand period of **at least 14 days**; termination the day after it ends; policy-loan principal and interest deducted from the surrender value | [REG-R25 제26조](#krlib-reg-r25) |
| 부활 (*buhwal*, reinstatement) | Within **3 years** of termination, provided the surrender value has not been drawn; arrears with interest at a rate the insurer sets within **평균공시이율 + 1%** | [REG-R25 제27조](#krlib-reg-r25) |
| 소멸시효 | 3 years on a claim, 3 years on a refund of premium or account value, 2 years on a premium | [REG-R49 제662조](#krlib-reg-r49) |
| Expiry | The contract runs to death on the 종신연금형; there is no maturity benefit | [S4] [S5] [S7] |

---

## Contractual mechanics

### Which account each cash flow falls in

The 특별계정 exists because **보험업법 제108조제1항제3호** permits an insurer to set up a
계정 「그 준비금에 상당하는 자산의 전부 또는 일부를 그 밖의 자산과 구별하여 이용하기
위한」 for a 변액보험계약 [R4] [REG-R6], and 감독규정 제5-6조제1항제3호 makes it
**mandatory** for a life insurer's variable business [REG-R15]. 제108조제2항 requires each
separate account's assets to be accounted for separately from every other separate account
**and** from all other assets [R4]. The conditions restate the statute and add the
consequences: 「제1항의 특별계정에서 관리되는 자산의 운용실적에 따른 이익 및 손실은 다른
계정의 자산운용에 따른 이익 및 손실에 관계 없이 이 계약으로 귀속됩니다」 [S7 제37조].

**감독규정 제5-7조 lists the only permitted transfers between the two accounts**: premium
receipt and benefit, dividend or refund payment; transfer to the general account of amounts
needed for risk cover and for acquisition, maintenance and administration; management fees;
loans and repayments; bond settlement; **covering a separate-account deficit out of the
general account's shareholder equity**; and anything else necessary to maintain the
account [REG-R15]. Every row below is one of them.

| Cash flow | Leaves | Arrives | Timing |
|---|---|---|---|
| 영업보험료 received | Policyholder | 일반계정 | On the 월계약해당일 |
| 계약체결비용, 계약관리비용(납입 중), 기타비용 | — | Retained in 일반계정; **never enters the 특별계정** | At premium payment [S7 제2조] |
| 특별계정 투입보험료 | 일반계정 | 특별계정, buying 좌 at the 투입일 기준가격 | At premium payment [R2] |
| 특별계정 운용보수 | 특별계정 net assets | 일반계정 | **Daily**, before the 기준가격 is struck [S7 제43조제2호] [S1] |
| 증권거래비용, 기초펀드 보수, 회계감사·채권평가 비용 | 특별계정 assets | Third parties, under 자본시장법 제188조 and 시행령 제265조; the insurer bears the 자산운용보고서 cost itself | On occurrence [S7 제44조] |
| 월공제액 — 위험보험료, 계약관리비용(납입 후), 최저사망보험금 보증비용, 최저연금적립금 보증비용 | 특별계정 계약자적립액 | 일반계정; the two guarantee charges are held there as **보증준비금** | Monthly, on the 월계약해당일 [S7 제2조] [R2] |
| 사망보험금 — the 계약자적립액 component | 특별계정 | Beneficiary | On death |
| 사망보험금 — the **guarantee top-up** (이미 납입한 보험료 less 계약자적립액, floored at zero) | 일반계정 보증준비금 | Beneficiary | On death [R2] |
| 해약환급금 | 특별계정 계약자적립액 | Policyholder | 해지신청일 + 제2영업일 [S7 제50조] |
| 해약공제액 | 특별계정 | Retained in 일반계정 | On surrender |
| 중도인출금 | 특별계정 | Policyholder | 신청일 + 제2영업일 [S2] [S5] |
| 보험계약대출 | 특별계정 (units cancelled), or the 일반계정 under the loan rider | Policyholder | 대출신청일 + 제2영업일 [S5] [R1] |
| 연금재원 at 연금개시 | 특별계정 | 일반계정 — 「연금개시시점부터 계약자적립액 모두에 대하여 특별계정에서 일반계정으로 자동전환하여 공시이율로 운용합니다」 | 연금개시나이 계약해당일 [S6] |
| GMAB top-up at 연금개시 | 일반계정 보증준비금 | 일반계정 연금재원 | 연금개시나이 계약해당일 |
| 연금 payments and 연금수령기간 중 계약관리비용 | 일반계정 | Policyholder / insurer | In the payout phase |
| Separate-account deficit | 일반계정 shareholder equity | 특별계정 | As needed [REG-R15 제5-7조](#krlib-reg-r15) |

The insurer may **pool** the assets of similar separate accounts across products on notice,
keeping each fund's accounts at head office for six months after the merger
[S7 제37조제4항]. Asset-concentration limits apply to special accounts on their own scale,
separate from and generally higher than the general account's, under 보험업법 제106조; their
values did not return and are **[unverified]** [R5].

### Premium provisions and the two deduction points

The premium meets the contract at **two distinct points**, and confusing them is the
commonest way to get a Korean variable model wrong. The conditions are explicit
[S7 제2조]:

> 월공제액이라 함은 해당월의 위험보험료, 계약관리비용(납입기간 종료 후 유지관련비용),
> 최저사망적립금 보증비용 및 실적배당 종신연금 보증비용의 합계액을 말합니다. … 다만,
> 계약체결비용, 계약관리비용(납입기간 중 유지관련비용), 계약관리비용(기타비용)은 보험료를
> 납입할 때 공제하며 …

so that:

1. **At premium payment**, the 계약체결비용, the 계약관리비용 for the premium-paying period
   and the 기타비용 are taken out of the gross premium in the general account. What is left
   is the **특별계정 투입보험료** and it is transferred to the separate account:

       특별계정 투입보험료 = 납입보험료 − (계약체결비용 + 납입 중 계약유지비용 + 기타비용)
                           = 순보험료 + 납입 후 계약유지비용                          [R2]

   The second line is the one that matters. **The 계약관리비용 for the period after
   납입완료 is collected during the premium period and carried inside the account value**,
   then drawn back out month by month once premiums stop. That is why the money entering
   the fund exceeds the pure net premium, and why the monthly deduction steps up at
   납입완료.
2. **On the 월계약해당일**, the 월공제액 — 위험보험료, 계약관리비용(납입 후) and both
   guarantee charges — is taken **out of the 계약자적립액** by cancelling units. The
   separate-account management fee is separate again and is taken **daily**: 「회사는
   특별계정 계약자적립금에서 매일 특별계정 운용보수를 차감합니다」 [S7 제36조].

On the anchor cell, month by month, in the premium period:

    납입보험료                                     ₩300,000
    − 계약체결비용         5.17% of 기본보험료      ₩ 15,510
    − 계약관리비용(납입 중) 3.50% of 기본보험료      ₩ 10,500
    = 특별계정 투입보험료                          ₩273,990   (91.33% of premium)

    월공제액 (from the account, on the 월계약해당일):
      위험보험료                                   ₩     24   [std]
      최저사망보험금 보증비용   0.07%/12 × AV
      최저연금적립금 보증비용   0.25%/12 × AV  +  0.30%/12 × ₩36,000,000 = ₩9,000
        (the premium-based component for at most 7 years)

and after 납입완료 the 월공제액 becomes 계약관리비용(납입 후) ₩3,990 plus the two guarantee
charges, with no premium arriving to offset it. The consequence is visible in [S2]'s own
illustration, where the cumulative separate-account contribution stops growing after year
10 and then **falls**, from ₩32,877,360 at ten years to ₩32,393,520 at twenty.

**The premium-based GMAB component deserves its own sentence.** 보험료총액 is 「이미 납입한
보험료(특약보험료 제외) 및 추후 납입할 기본보험료 합계(특약보험료 제외)」 — the whole
premium the policyholder has undertaken to pay, past *and* future — and the 0.30% is
levied on it 「납입기간(최대 7년) 동안」 [S1]. On the anchor cell that is ₩36,000,000 ×
0.30% = **₩108,000 a year for seven years**, against a first-year account value of
₩3,216,621. Expressed as a rate on the fund it is over 3% a year at outset, falling below
0.5% by year seven. A model that treats guarantee charges as basis points on the account
value will misstate the early-duration cash flow of this contract by an order of magnitude.

**Premium allocation observed.** The textbook publishes the ratios actually used, as a
percentage of premium reaching the fund before the monthly mortality deduction, by premium
term: 일시납 94.4, 3년납 96.6, 7년납 90.9, 10년납 90.0, 15년납 90.0, 20년납 90.0, the same
for both sexes at ages 20–45, because a variable annuity carries so little mortality cover
that the natural premium is immaterial — so the allocation is flat by age and **rises**
after ten years when the 계약체결비용 stops [R2]. Three carriers' first-year illustrations
put the realised ratio at 91.3%, 91.3% and 91.4% on the anchor cell [S1] [S2] [S6], and the
composite's 91.33% sits inside both.

### 좌수 and 기준가격 — the daily unit mechanics

The conditions and the industry textbook agree, and the model implements this arithmetic
directly [S7 제43조] [R2]:

    좌수:   특별계정을 설정할 때 1원을 1좌로 하며, 그 이후에는 매일 좌당 기준가격에 따라
            좌단위로 특별계정에 이체 또는 인출한다
    기준가격 = 당일 특별계정의 순자산가치 ÷ 특별계정 총 좌수
            — 1,000좌 단위로, 원 미만 셋째 자리에서 반올림하여 원 미만 둘째 자리까지
            — 판매 첫날의 기준가격은 1,000좌당 1,000원
            — 당일 순자산가치는 당일 총자산에서 특별계정 운용보수를 차감한 금액

    계약자 보유좌수 = (특별계정 투입보험료 ÷ 투입일 기준가격) × 1,000
    계약자적립금    = 해당일 기준가격 × (계약자 보유좌수 ÷ 1,000)
    해당일 기준가격 = (전일말 특별계정 순자산가치 ÷ 특별계정 총좌수) × 1,000

The textbook reconciles the 「당일」 and 「전일말」 wordings: 「여기서 당일의 의미는 당일초의
순자산가치를 반영해야 한다는 것으로 실제로는 전일말과 동일한 기준이다」 [R2]. Units increase
when money enters (premium, repayment of a policy loan) and decrease when money leaves (the
월공제액, a loan, a withdrawal); **the unit price moves only with investment performance**
[R2]. A price below 1,000 means the fund is below its launch value, which the one live fund
panel retrieved shows at 904.24원 after fourteen years [S11] [R2].

Transactions are priced with a **two-business-day lag** — a fund switch at 변경요구일 +
제2영업일 [S5] [S7 제39조], a withdrawal at 신청일 + 제2영업일 [S2] [S5], a surrender at
해지신청일 + 제2영업일 [S7 제50조제2항] [S9]. The reference model runs on a **monthly grid**
and does not represent the lag, which the technical notes record as an unmodelled timing
difference.

### 계약자적립액 — the account recursion

Contractually, 「계약자적립금에서 월계약해당일에 월공제액을 차감한 금액과 특별계정투입
보험료에 해당하는 이체금액에 대하여 특별계정의 운용실적을 반영하여」 계산하고, 「회사는
특별계정 계약자적립금에서 매일 특별계정 운용보수를 차감합니다」 [S7 제36조]. The
regulation says the same thing from the other side: what goes into the separate account is
the **적립 보험료**, 「영업보험료에서 위험보장에 필요한 부분과 사업비 등 기초서류에서 정한
사항을 차감한 금액」, together with its investment return [REG-R15 제5-6조제5항](#krlib-reg-r15); and the
separate-account 계약자적립금 for 변액보험 is **the whole profit or loss arising in that
account in the year, appropriated to the contract** [REG-R15 제6-26조](#krlib-reg-r15).

On the model's monthly grid, with `AV(t)` the account value at the start of month `t`:

    AV(t+1) = [ AV(t) + P_sa(t) − D(t) ] × (1 + i_gross) ^ (1/12) × (1 − f_mgmt / 12)

where `P_sa(t)` is the 특별계정 투입보험료, `D(t)` the 월공제액, `i_gross` the gross
separate-account asset return and `f_mgmt` the blended 특별계정 운용보수. The management fee
is written separately from the return because it is deducted **inside the 기준가격**
[S7 제43조제2호] while the 월공제액 is deducted by **cancelling units**, leaving the price
undisturbed. The exact form of the recursion sits in the **산출방법서** (*sanchul
bangbeopseo*), which is a filed 기초서류 and is not public [REG-R18 제7-64조](#krlib-reg-r18) [REG-R2] — so
the recursion above is a **[std]** construction consistent with, and not derived from, the
retrieved documents. That limit applies equally to the surrender value, the annuity amount
and the roll-up base, and it is the hard boundary on how far a public-source reconstruction
of a Korean variable annuity can go.

감독규정 제7-65조제2항 permits the 계약자적립액 to be computed 「연납보험료를 기준으로 하여」
— on an annualised-premium basis — which is how a Korean monthly-premium product reconciles
a monthly grid with an annual reserve [REG-R18]. `VA_KR_S` runs monthly throughout and does
not use the permission; the technical notes say so.

### 최저사망보험금보증 (GMDB)

**It is compulsory.** 보험업감독규정 제7-60조제7호: 「변액보험 및 금리연동형보험(연금보험을
제외한다)의 경우 최저사망보험금 등을 설정하여야 한다」 [REG-R16] [R11]. The clause was
retrieved in the cross-product reference library at first hand [REG-R16]; the product
research file reaches it only through a double quotation inside [R1], and the wider content
of 제7-60조 in that file is **[unverified]** [R11].

**The benefit.** The textbook states the standard definition as

    사망보험금(최저보증 포함) = Max(기납입보험료, 계약자적립금 + 기본사망보험금)      [R2]

which, with no 기본사망보험금 on the representative design, is
**Max(이미 납입한 보험료, 계약자적립액)**. Contract wordings agree: 「계약자적립액과 이미
납입한 보험료(단, 특약보험료 제외) 중 큰 금액을 계약자에게 지급합니다」 [S1]; 「사망한 날의
계약자적립액이 … "이미 납입한 보험료"보다 적은 경우 계약자적립액을 지급하지 않고 "이미
납입한 보험료"를 지급하는 것」 [S4]; 「특별계정의 운용실적과 관계없이 사망시점의 "이미
납입한 보험료(특약보험료 제외)의 100%"를 지급하여 드립니다」 [S10]. The insurer's cost is
the excess of the floor over the account value, and it is paid **out of the general
account**: 「매일(또는 매월) 특별계정 적립금에서 보증비용을 공제하여 일반계정 내에
최저사망보험금 보증준비금 항목으로 적립하고 사망보험금이 기납입보험료보다 적은 계약이
발생한 경우 그 부족분을 보전해주는데 사용한다」 [R2].

**The base is adjusted for withdrawals and reductions**, and without that adjustment a
policyholder could withdraw the fund and keep the strike: 「계약자적립액의 일부를 인출하거나
기본보험료를 감액하는 경우의 최저사망지급금 계산시 적용하는 "이미 납입한 보험료"는 …
계산된 보험료와 해당 감액 또는 인출 이후 납입된 보험료의 합계」 [S4], and the same rule at
[S7 제2조]. The representative implements the **proportional** form published for the
annuity guarantee base [S2] [S7 제51조제8항]:

    이미 납입한 보험료 (after)
        = 이미 납입한 보험료 (before)
          × (중도인출 전 계약자적립액 − 중도인출금액) ÷ 중도인출 전 계약자적립액

with subsequent premiums added at face value.

**The charge stops when the guarantee is worthless.** 「연금개시후 보험기간 중
최저사망적립금이 "0"이 되면, 이후 최저사망적립금 보증비용은 차감하지 않습니다」 [S7 제2조],
and [S10] states the same rule for its variant. The representative design extinguishes the
death cover at annuitisation, so the rule bites only on the GLWB variant, where the
guarantee survives into the payout phase and runs down by the annuity already paid:
「연금개시 후 보험기간에는 사망시점의 "연금기준금액"에서 연금개시 후 보험기간 중 발생한
실적배당 종신연금 연지급액의 합계를 차감한 금액을 말하며, 이 금액이 '0'보다 적은 경우
'0'으로 합니다」 [S2] [S7] [S10].

**Observed charges** — all annual rates deducted monthly or daily from the separate
account: **0.05%** of 특별계정 적립액 [S4] [S9] [S10]; **0.07%** [S1]; and **0.40%** of the
최저연금기준금액 for the first twenty years falling to 0.25% thereafter [S2]. The last is
dearer because its base is not premiums paid but a **roll-up** amount growing at 7%/6%
simple, so the option is far deeper in the money. The composite takes 0.07% on a
premiums-paid base, which is the pairing [S1] publishes.

One carrier caps the enhanced death guarantee by attained age, after which the 보증강화형
falls back to the plain premiums-paid base — 보증강화종료나이 = 연금지급개시나이 + 21
(개시 55–59세), +19 (60–69), +17 (70–79), +15 (80) [S7 제2조]. The composite has no enhanced
form and does not carry it.

### 최저연금적립금보증 (GMAB) — the guarantee the product is named for

**Definition.** 「피보험자가 연금개시시점에서 생존하였을 경우 특별계정의 펀드수익률과
상관없이 연금개시시점의 연금재원으로 최소한 기납입보험료 이상으로 설정된 일정수준을
보증해주는 옵션」, with the identity [R2]:

    연금개시시 계약자적립금(최저보증 포함) = Max(기납입보험료, 연금개시시 계약자적립금)

**It is a European option struck on one date**, and every part of the contract says so. It
is not payable on surrender [S1] [S6] [S7 제50조제3항] [S8] [S10], not payable on death
before annuitisation [R1], and forfeited on 조기연금개시 [S1]. [R1] states the boundary
directly: 「만기 전에 사망 또는 해약이 발생하는 경우 이 보증은 성립하지 않으며, 따라서
보험회사는 약정된 금액만을 보험계약자에게 지급하게 된다」. The insurer's payoff at the
annuity commencement date `T` is therefore

    GMAB cost(T) = max( 0 , K(T) − AV(T) ) × 1{alive and in force at T}

with `K(T)` the guarantee base, `AV(T)` the account value, and the indicator carrying every
decrement — mortality **and lapse** — that occurred before `T`. A model that treats the
guarantee as a floor on the account value at every duration will overstate its cost by the
whole of the pre-annuitisation exit probability, and on a product whose seven-year
persistency is reported below 30% [R1] that is most of it.

**Guarantee base `K(T)` — four rules, one modelled.** [R1 <표 Ⅲ-2>](#krlib-variable_annuity-r1) sets out the four ways
a Korean carrier fixes the level:

| Rule | Definition | Where observed |
|---|---|---|
| **Premium refund** | 「연금 개시 시까지 납입하는 보험료 대비 일정비율에 해당하는 금액을 최저보증. 대부분의 상품은 일정비율을 100%로 설정. 연금 개시 시점까지의 거치기간이 길수록 일정비율이 증가하는 상품도 있음」 | [S1] [S9 at election] [R1]; **the representative** |
| **Step-up** | 「계약자 적립금이 계약 시 정해진 일정 수준(기납입보험료의 110%, 120%, 130% 등)에 도달하면 보증수준도 이에 비례하여 증가」 | [R1] — 미래에셋 120/150/180/200%, DB생명 and KDB 100–500%, ING 100–200% in five steps, 삼성 130% |
| **Ratchet** | 「일정주기로 계약자적립금을 파악하여 … 직전 주기에 설정된 보증금액을 초과하면 그 시점 이후 보증금액이 이에 비례하여 증가」 | [S6] monthly, [S9] monthly, [S7 보증강화형] annual, [R1] 3-yearly (교보 더드림) and daily with a three-day confirmation (KDB 트리플에셋) |
| **Roll-up** | 「기납입보험료를 특정 이율로 부리한 금액을 최저보증」 | [S2] 7%/6% simple, [S7] 5%/4% simple, [S10] 1.0%/2.0% compound |

[R1] works all four against one set of fund values — ₩1,000,000 a month for ten years then
five years deferred — and the result is the clearest available demonstration that **the
guarantee design, not the guarantee level, drives the option cost**: at year 15 the account
stands at 1,003만원 against premiums of 1,200만원, and the four guarantees stand at 1,200
(premium refund), 2,100 (roll-up at 5% simple), 1,624 (step-up, which locked in a year-12
spike) and 1,240 (three-yearly ratchet, which missed it).

The composite takes **premium refund at 100%**, `K(T) = 이미 납입한 보험료` — the textbook
identity, the level of the only retrieved charged-GMAB contract, and the only rule whose
strike is already a modelled quantity. The other three are specified here so the technical
notes can implement them as variants without returning to the research file:

- **Roll-up, simple, day-counted.** 「기준 기본보험료 및 기준 추가보험료에 … 매년
  최저연금기준금액비율 해당액을 … 일자 계산하여 더한 금액」, the ratio being 7/100 to the
  twentieth anniversary and 6/100 thereafter, 7/100 throughout where the pre-annuitisation
  period is under twenty years [S2]; or 5/100 during the premium term and 4/100 after it,
  the 5% band always using the **original** premium term [S7]. [S2] publishes the conversion
  a model should target: 「대표계약기준(40세 남성, 10년납, 연금개시나이 65세) 복리이자율로
  환산시 **연복리 4.32%**」. A compound variant credits 연복리 1.0% or 2.0% on a base **net
  of the risk and expense loadings but gross of the guarantee charge** [S10].
- **Ratchet, monthly, unfunded.** [S6] is the purest form retrieved and it dispenses with
  the guarantee charge altogether:

      경과확정보증액
        1차월도       계약일의 기본보험료(특약보험료 제외) × 보증비율
        2차월도 이후  Max( 이미 납입한 보험료 × 보증비율,
                           매월 계약해당일의 계약자적립액,
                           직전월도 계약해당일의 경과확정보증액 )
      최저연금적립액  = 연금개시 전까지의 경과확정보증액 중 가장 큰 금액

      보증비율, by 연금개시 전 보험기간: 15년 이하 100%; 16–44년 85% + 1% × 연수;
                                         45년 이상 130%

  with 「최저연금적립액보증수수료 … 가 부가되지 않습니다」 and the guarantee void on
  surrender or lapse [S6].
- **Step-up ladder.** The 초과성과금액 — the difference between the step just attained and
  the step previously attained — is added to the guarantee and, at two carriers, is
  **compulsorily transferred to the bond fund** [R1]. The step is tested at a stated
  frequency and, once attained, cannot fall.

**Withdrawals and reductions re-base the guarantee.** The published formula, which the
composite applies to both guarantee bases, is proportional [S2] [S7 제51조제8항]:

    연금기준금액 (after) = 연금기준금액 (before)
                           × (중도인출 전 계약자적립액 − 중도인출금액)
                           ÷ 중도인출 전 계약자적립액

On the roll-up designs both carriers instead re-derive the 기준 기본보험료 and 기준
추가납입보험료 under the reduction and withdrawal articles and restart the accrual from the
reduced base [S2] [S7 제2조] — economically the same adjustment, mechanically a different
one, and the technical notes implement whichever base is in force.

**Observed GMAB charges.** 0.25% p.a. of the account value **plus** 0.30% p.a. of
보험료총액 for at most seven years [S1]; 0.85% p.a. of the account value while the elective
guarantee is switched on [S9]; none, the guarantee being funded by a CPPI overlay [S6];
none, no GMAB offered [S4] [S5]; and a GLWB charge instead at 0.30%/0.35% of the account
value [S10] or 3.30%/1.70% of the guarantee base [S2]. The textbook's illustrative
disclosure table uses **계약자적립금의 연 0.5%** for a 보증형 against 없음 for a 미보증형
[R2]; that is a teaching figure, not a market rate.

**A caveat that must travel with any quotation of [R1]'s charge table.** [R1]'s <표 Ⅲ-1>
prints a column headed 「연간보증비용」 with ranges — GMDB 0.04–0.07%, GMAB 기납입보험료
0.56–0.98%, GMAB step-up/ratchet/roll-up 0.84–1.05%, GMWB 0.6–0.9%, GLWB 0.6–0.9% — under
the note 「보증비용은 보험업감독규정시행세칙 <별표 24> 보증준비금 산출기준을 따름」.
Reconstructing them from the 별표 24 tables reproduced later in the same report shows they
are **exactly the reserve standard's floors, not observed carrier charges**: 0.7% ×
0.4%/0.5% = 0.56%, 0.7% × 0.7%/0.5% = 0.98%, and so on [R1]. They must not be quoted as
market guarantee charges. The observed charges are the ones listed above.

### What a single deterministic path can and cannot say about the guarantees

This section exists because the reference model runs **one deterministic return path**, and
the two things it is asked to value are options.

**What the run does say.** On a given path the guarantee cost is well defined and is
computed exactly:

- **GMDB.** For each month `t` before annuitisation the guarantee outgo is
  `pols_death(t) × max(0, K_d(t) − AV(t))`, where `K_d(t)` is 이미 납입한 보험료. This is a
  real expected cash flow on that path, because the mortality decrement is a probability
  applied to a deterministic account value, not a scenario.
- **GMAB.** At the single date `T` the guarantee outgo is
  `pols_if(T) × max(0, K(T) − AV(T))`. On one path this is the option's **intrinsic value
  at maturity**, evaluated at the one terminal account value the path produces.
- The charges are exact on every path, because they are contractual rates on modelled bases.

**What the run does not say, and must not be read as saying.**

1. **There is no time value.** The GMAB payoff `max(0, K − AV(T))` evaluated at one `AV(T)`
   is the payoff of the option, not its value. By Jensen's inequality the expectation of
   the payoff is at least the payoff at the expected account value, with equality only in
   the degenerate case, so the single-path
   figure is a **lower bound on the expected cost** and is zero whenever the path lands the
   account above the strike. At the base-run 투자수익률 of 2.50% the anchor cell's account
   is above premiums paid at annuitisation, so **the base run reports a GMAB cost of exactly
   zero while collecting the full guarantee charge**. That result is an artefact of the
   path, not a finding about the guarantee.
2. **The GMDB is a strip of puts, not one.** Its single-path figure is the same intrinsic
   evaluation repeated monthly, and it inherits the same bound.
3. **The statutory reserve is not computable from this run and is not published by it.**
   보험업감독규정 제6-11조의5 requires a **보증준비금** inside retained earnings for expected
   losses on benefit guarantees [REG-R10], and the calculation delegated to 시행세칙 별표 24
   is 「사망률, 해지율, 자산이익률(**1,000개**)을 이용하여 만기까지 장래 예상되는 순손실액을
   현가로 환산한 상위 30% 평균 금액」 — a **CTE(70) over a thousand scenarios** — or a
   standard factor table, whichever is greater [R1] [R12] [REG-R26]. The **standard factor
   exists precisely because a deterministic number is meaningless**, and the model publishes
   **neither** — no CTE(70) and no factor result. The factor tables are
   reproduced under "Regulatory context" below; every figure in them is at second hand from
   [R1] and is **[unverified]** against the rule itself [R12] [REG-R26].
4. **Guarantee risk does not diversify.** [R1] is explicit: 「시장리스크 … 리스크 노출량을
   합하여도 리스크가 감소하지 않는다. 모든 보험계약자들이 같은 입장에 있어 동시에 보증을
   이용하려고 하기 때문이다」. Mortality risk *does* diversify — longevity raises the value
   of the GMAB, mortality raises the cost of the GMDB — and policyholder-behaviour risk
   「헤징이 불가능하며」 does not.
5. **Lapse is not exogenous.** [R1] states that dynamic lapses are the market and reserving
   convention — 「동적해지율이란 최저보증 발생률(In-the-moneyness)에 따라 해지율을 달리
   적용하는 방법으로, 최저보증 발생률이 높을수록 해지율을 감소시키고, 최저보증 발생률이
   낮을수록 해지율을 증가시켜야 한다」 — but **no retrieved document publishes a functional
   form or a single parameter**. Any dynamic-lapse formula in the model is a **[std]**
   construction, and the base run uses a static rate.
6. **Every option the policyholder holds points the same way.** 조기연금개시 is available
   only where the guarantee is out of the money [S1] [S9] [S10]; 일반계정 전환 is offered at
   130% of premiums paid or above premiums paid, irreversibly [R1]; and the automatic
   transfer at the CPPI barrier is the same trade made by the insurer [S6]. A deterministic
   run cannot exercise any of them.

**What the model publishes instead.** The base run at 투자수익률 2.50% and the two other
mandated illustration returns, **−1.00% and 3.75%** [R2] [REG-R48], with the GMAB out of the
money on the two upper paths and in the money on the lower one, so that the reader sees the
guarantee's intrinsic value on both sides of the strike; and the guarantee charges collected
in each case. The gap between the charge collected and the intrinsic cost is reported as
what it is — **a single-path residual, not a profit**. The 별표 24 standard factor is
reproduced under "Regulatory context" as a citation and is **not** computed by the model.

### Investment constraints and automatic de-risking

The insurer manages the guarantee not only by charging for it but by **constraining the
assets** [R1] [S6], and the reserve rule gives it a direct financial reason to: the 별표 24
standard factor is indexed to 주식비중한도, 「기초서류상 최대 주식투자 비중을 적용함」, so
lowering the equity cap lowers the reserve floor [R1] [R12].

- **The mandatory bond weight is a function of the deferral period**, and the same ladder
  appears at two carriers eight years apart — <12년 ≥80%, =12년 ≥70%, >12년 ≥50%
  [S1] [R1]. It binds both the premium allocation and the account mix and survives every
  later switch [S1].
- **Automatic rebalancing into bonds before annuitisation.** 「「연금지급개시일 − 3년」시점
  부터 매년 연계약해당일에 … 채권형 및 단기안정채권형 계약자적립액의 합계가 펀드 전체
  계약자적립액의 80%(또는 70%) 미만인 경우 … 채권형 계약자적립액이 자동 조정됩니다」 [S1].
  A second carrier does the same on a different trigger, moving anything above 30% of the
  account held outside the bond funds into them on each anniversary from the second
  [S7 제40조]. **This is on in the base run.**
- **펀드자동재배분** restores the chosen weights on a 3-, 6- or 12-month cycle, with a
  bond-plus-MMF floor of 60% enforced while a 계약유지보장 is running [S5] [S7 제40조].
- **펀드자동전환옵션** is target-return de-risking: the policyholder picks a 목표수익률 from
  **110% to 200% in 10% steps** of 이미 납입한 보험료; on attainment the whole balance of
  every fund other than the chosen 채권형 or MMF재간접형 is transferred into it; the insurer
  must notify within 30 days; the option is then released and any re-application must be at
  least the attained target plus one step; selectable or cancellable four times a year and
  mutually exclusive with 펀드자동재배분 [S5].
- **Electing a guarantee overrides fund choice.** One carrier forces 채권형II 50% + EMP AI형
  50% on election of the GMAB [S9]; another transfers everything into a single 글로벌MVP30
  fund the day before the (연금개시나이 − 1)세 anniversary on its 1+α form and runs the 2+α
  form on that fund alone from the outset, with equity caps of 80% unguaranteed, 60% for 1+α
  and a single fund for 2+α [S10]. **The guarantee level and the investment freedom are
  traded against each other**, explicitly.
- **The CPPI alternative.** Where there is no guarantee charge, there is a
  constant-proportion portfolio insurance rule instead [S6] [R1]:

      성장자산펀드 편입비율 = Min(기준성장자산적립금 × 승수, 특별계정 계약자적립금 × 80%)
                              ÷ 특별계정 계약자적립금
      안전자산펀드 편입비율 = 100% − 성장자산펀드 편입비율

  with the multiplier in the range **1.0–4.0**, notified on conversion and changeable by the
  insurer on written notice [S6]. It has an **absorbing barrier**: where the growth weight
  is 0% and the account has fallen to 기준경과확정보증액 × 평가비율 × **1.02** or below, the
  contract 「자동으로 특별계정에서 일반계정으로 전환되어 공시이율(최저보증이율 연복리
  1.75%)로 운용되며, 이럴 경우에는 특별계정으로 다시 전환되지 않습니다」 [S6] — once the
  cushion is exhausted it becomes a general-account declared-rate contract, irreversibly.
- **Fund choice is constrained by the suitability diagnosis**: 「보험계약자의 '변액보험
  가입성향 진단'에 따라 펀드의 선택이 제한될 수 있습니다」, with the menu mapped onto five
  투자성향 bands and six 위험등급 [S5].

### 추가납입 and 중도인출 — the flexibility, and the guarantee leakage it creates

**추가납입보험료** is capped at **200% of the basic premium** in every retrieved contract,
variously expressed as 200% of the basic premium paid to date [S1] [S4], of the basic
premium payable to date including prepayment [S2] [S7 제2조], or of the contracted total
[S5] [S6] [S10]. It attracts **little or no loading** — 「추가납입시, 추가납입보험료에 대한
수수료가 없습니다」 [S1], and the same at [S4] [S6] [S9]; only one carrier charges it, at
1.5% reduced to Min(0.5%, ₩10,000) within the cumulative amount previously withdrawn [S2].
This is the single largest lever a policyholder has over the product's cost, and it is why
the front-loaded 계약체결비용 is levied on the **기본보험료** alone.

The 2019 FSC expense reform announced a cut of the additional-premium limit **from 2× to
1×** [R7] [REG-R29], but every variable annuity retrieved — including three produced in
2025 and 2026 — still publishes 200% [S1] [S4] [S5] [S6] [S7] [S10]. Either the measure did
not extend to this line, or it was reversed, or it was never implemented; the 200% figure is
well-evidenced and the 2019 announcement is recorded beside it. The question is
**[unverified]**.

**중도인출** is uniformly twelve times a policy year, opening one month after the contract
date (one year at one carrier), limited to 50% of the 해약환급금 (60% at one carrier) with a
residual floor per 구좌 of ₩5,000,000 [S1] [S5], ₩3,000,000 [S2] or 기본보험료의 1200%
[S4]. Withdrawals come **out of the additional-premium account first** [S2] [S5]. Two
further rules are universal and both are tax rules showing through into the policy
conditions:

- **A ten-year cap on cumulative withdrawals**: 「계약일 이후 10년 이내에는 인출금 총액이
  실제 납입한 보험료 총액(단, 특약보험료 제외)을 초과할 수 없습니다」 [S1] [S2] [S5]. It
  exists to keep the 소득세법 시행령 제25조 ten-year exemption route open [REG-R58].
- **A withdrawal restores additional-premium headroom** [S1] [S2] [S4] [S5] [S6] [S7], so
  the two facilities together let a policyholder cycle money through the contract.

And, as set out under the GMAB above, **중도인출금은 최저보증한도에서 차감된다** [R1] — the
withdrawal reduces both guarantee bases proportionally [S2] [S4] [S7].

### 해지공제 and 해약환급금

The surrender value is 「계약이 해지된 날의 기준가격을 적용하여 산출방법서에 따라」 computed,
at the 해지신청일 + 제2영업일 price, paid within three business days, and — the sentence the
whole product turns on — 「해지환급금은 특별계정의 운용실적에 따라 변동되므로 **최저보증이
이루어지지 않으며, 원금손실이 발생할 수도 있습니다**」 [S7 제50조].

**The charge is the unamortised acquisition cost, capped at seven years.** 「해약공제액은
보험료납입기간(납입기간이 7년 이상인 경우 7년) 이내에 계약을 해지할 경우 계약자적립액에서
차감하는 금액으로, 중도해지에 따른 보험회사의 손해에 대한 패널티 성격이 있다」 and
「해약환급금의 경우 해지시점의 적립금에서 해지공제액(미상각신계약비, 최대 7년까지 적용)을
차감한 후 지급」 [R2]. The seven-year ceiling is statutory [REG-R19 제7-66조제1항제2호](#krlib-reg-r19).

**The run-off is linear in the amount, not in the ratio.** All three retrieved scales fit
`C × (7 − t) ÷ 7` exactly: [S5]'s published amounts decline by exactly ₩153,857 a year,
giving `C = ₩1,077,000` with no rounding at all; [S2]'s 71 / 59 / 47 / 36 / 24 / 12 만원 are
`C = 83만원` rounded to the 만원; [S4]'s 101 / 84 / 67 / 51 / 34 / 17 만원 are `C = 118만원`
on the same rounding [R1] [S2] [S4] [S5]. The published **ratio** falls far faster than the
amount because its denominator — premiums paid — is growing. The representative scale, in
full:

| 경과 `k` (완성 연수) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7+ |
|---|---|---|---|---|---|---|---|---|
| 해약공제액 | ₩830,000 | ₩711,429 | ₩592,857 | ₩474,286 | ₩355,714 | ₩237,143 | ₩118,571 | ₩0 |
| as % of premiums paid | — | 19.8% | 8.2% | 4.4% | 2.5% | 1.3% | 0.5% | 0.0% |

The ratios are the composite's own. [S2] publishes 19.5 / 8.2 / 4.4 / 2.5 / 1.3 / 0.6% off
amounts rounded to the 만원, which is where the first and last figures differ.

The reform history behind the shape: the 개인연금 활성화 방안 of 2013-08 required a carrier
to file its 산출방법서 unless it spread **at least 50% of the 계약체결비용 over seven
years**, capped the deferrable share at 50%, and cut bancassurance and online 계약체결비용
to 50% of the tied-agent channel; [R1] reproduces the formula that regime implies —
`해약 시 공제액 = 판매보수(50%) × (7년 − 경과기간) ÷ 7년` — which is exactly the linear,
seven-year run-off the three retrieved scales show. The rule survives in the current
감독규정 as 제7-51조's pre-notification trigger for a 저축성보험 that does not spread at
least 50% of the acquisition cost evenly [REG-R22].

**A single-premium contract carries no surrender charge at all**: 「일시납 … 계약체결 직후
계약체결비용이 모두 부과되므로 … 해지공제비용이 부과되지 않는다」 [R1] [S5].

**Where the surrender value goes to zero.** [S6]'s illustration shows a surrender value of
**zero at three months** on an account of ₩821,751, because the charge exceeds the account —
which the statutory floor turns into zero rather than a debt [REG-R19]. The representative
scale does the same for roughly the first four months.

### Exclusions and 면책

- **자살면책** runs **2 years** from the 보장개시일 on the two contracts that state it
  [S5] [S6]. Within it, the representative pays the 계약자적립액 without the GMDB floor
  **[std]** — see footnote 18.
- 상법 제659조 excludes the intention or gross negligence of policyholder, insured or
  beneficiary generally, and 제660조 war and civil disturbance absent agreement [REG-R49];
  but 상법 제732조의2 provides that gross negligence does **not** exclude a death benefit,
  and that where one of several beneficiaries intentionally kills the insured the others are
  still paid [REG-R50]. Both are one-way mandatory under 제663조 [REG-R49].
- The **고도재해장해급여금** pays on the 고도재해장해 state arising from a 재해 as defined in
  the 재해분류표 [S1] [S2]; the exclusions are those of that schedule. No retrieved document
  reproduces the schedule for this product and its contents here are **[unverified]**.
- 표준약관 제22조 (계약의 소멸) provides that where death makes further benefits impossible
  and death is not itself an insured event, the insurer pays 「산출방법서에서 정하는 바에
  따라 회사가 적립한 사망 당시의 계약자적립액」 [REG-R25], with 상법 제736조 as the
  statutory floor [REG-R50].

### 고지의무 and 계약 전 알릴 의무

The 표준약관 states in terms that the 계약 전 알릴 의무 (*gyeyak jeon allil uimu*)
「상법상 '고지의무'와 같습니다」 [REG-R25 제13조·제14조](#krlib-reg-r25). The insurer may **not** terminate
for breach where it knew or was negligent in not knowing at formation; where **one month**
has passed since it learned of the breach, or **two years** from the 보장개시일 without a
claim event (one year for disease in a 진단계약); where **three years** have passed since
the contract date; where it accepted on a health-examination document and the claim arises
from a matter stated in it; or where the 보험설계사 prevented truthful disclosure.
제14조제4항 carries the causation defence and 제14조제5항 bars termination for
non-disclosure of **other insurance held** [REG-R25]. The statutory frame is 상법 제651조 and
제651조의2 — one month from discovery and three years from formation, with a matter asked
about **in writing presumed material** — and 제655조's causation defence [REG-R49].

**사기에 의한 계약** — proxy examination, drugs taken to pass underwriting, forged
certificates, or concealment of a pre-application cancer or HIV diagnosis — may be cancelled
within **five years of the 보장개시일 and one month of learning of the fraud**
[REG-R25 제15조](#krlib-reg-r25).

On this product the practically operative pre-sale duty is not medical but **suitability**:
a producer recommending a variable contract to an 일반금융소비자 must observe
금융소비자보호법 제17조, and selling without recommending engages 제18조 (적정성원칙); the
information gathered must include 연령, 재산상황, 보험계약 체결의 목적, experience of
acquiring and disposing of financial products, and understanding of financial products
[R2] [R14]. 취약금융소비자 — 「만 65세 이상 고령자, 미성년자, 정신적 장애로 일상이나
사회생활에서 제약을 받는 자 등」 — may be judged 부적합자 under a separate standard, with an
exception for over-65s who have bought a variable contract or a financial-investment product
before [R2]. Under the 「변액보험 표준계약 권유준칙」 and the 「변액보험 모범판매규준」 the
seller must explain the possibility of loss and the material loss on early surrender and
hand over a 변액보험 주요내용 확인서; a post-sale 해피콜 is separately required [R2].

### 청약철회, 품질보증해지 and 위법계약해지

Three distinct exits sit in front of the surrender value and none of them charges the
해약공제:

- **청약철회** — within **15 days of receiving the 보험증권** and never after **30 days from
  the application date**, whichever comes first; effective on despatch; no damages or
  penalty; premiums returned within 3 business days, late return carrying interest at the
  보험계약대출이율 compounded annually. Excluded for contracts of 90 days or less, for an
  insurer-funded health examination, and for a 전문금융소비자. Ineffective where a claim
  event has already occurred unless the policyholder withdrew knowing it had
  [REG-R51 제46조](#krlib-reg-r51) [REG-R25 제17조](#krlib-reg-r25).
- **품질보증해지** — within **3 months of formation** where the 약관 and the policyholder's
  copy of the application were not delivered, the important content was not explained, or
  the policyholder did not sign; premiums returned with 보험계약대출이율 interest
  [REG-R25 제18조제3항](#krlib-reg-r25) [REG-R49 제638조의3](#krlib-reg-r49).
- **위법계약해지** — where the seller breached 적합성원칙, 적정성원칙, 설명의무,
  불공정영업행위 금지 or 부당권유행위 금지 [R3] [R14]. Where the contract is terminated on
  that ground the **계약자적립액** is returned rather than the 해약환급금
  [REG-R25 제29조의2](#krlib-reg-r25) — i.e. the 해약공제 is not taken. The FSS's 2025 mystery shopping found
  the explanation of this right one of the two weakest items in the whole exercise [R3],
  which makes its take-up rate a live and unquantified behavioural risk.

### 실효 and 부활

The 표준약관 machinery applies: a demand period (납입최고) of **at least 14 days**, the
contract terminating the day after it expires, with policy-loan principal and interest
immediately deducted from the surrender value [REG-R25 제26조](#krlib-reg-r25); and **부활** within **three
years** of termination provided the surrender value has not been drawn, on payment of
arrears with interest at a rate the insurer sets within **평균공시이율 + 1%**, the insurer
being unable to refuse because a claim event occurred before termination
[REG-R25 제27조](#krlib-reg-r25) [REG-R49 제650조의2](#krlib-reg-r49).

Two things make lapse behave differently here from a protection product. First, **the
account funds the monthly deduction**, so a contract does not fail merely because a premium
is missed; the documented case is the 납입 일시중지, during which the charges are taken from
the surrender value and the holiday ends if they cannot be met [S1]. Second, **the 해약공제
runs off to zero at seven years while the account is still small**, so the penalty for
surrendering falls away long before the guarantee matures — which is what makes lapse the
dominant assumption on this product. [S2]'s illustration shows the 해약환급금 and the
계약자적립액 coinciding from year 7 onwards.

### Expiry and the payout phase

At the 연금개시나이 계약해당일 the representative contract does three things at once: the
GMAB is tested and, if in the money, topped up out of the general account; the resulting
연금재원 is transferred **from the 특별계정 to the 일반계정** — 「연금개시시점부터
계약자적립액 모두에 대하여 특별계정에서 일반계정으로 자동전환하여 공시이율로
운용합니다」 [S6]; and the pre-annuitisation cover ceases, 「일반적으로 연금개시 후 보장은
소멸됨」 [R2].

The annuity is then computed 「연금사망률 및 공시이율을 적용하여 산출방법서에 따라」
[S1] [S2] [S5], and two features of that computation are real options in the
policyholder's favour:

- **The annuity factor is not locked at issue.** 「보증기간부 종신연금의 경우 연금지급개시전
  연금생명표의 개정 등에 따라 연금액이 증가하게 되는 경우에는 연금개시 당시의 연금생명표 및
  계약자적립액을 기준으로 산출한 연금액을 지급하여 드립니다」 [S1], and the same **one-way**
  ratchet at [S5] and [S2]. The mortality basis is re-struck at annuitisation but only where
  it helps the policyholder, which is why [R1] classifies 사망률리스크 as a guarantee risk in
  its own right.
- **The annuity moves with the 공시이율 after it starts** [S5], subject to the
  최저보증이율 floor of 1.00% / 0.75% / 0.50% by elapsed duration [S1]. A charge is taken
  from each payment [S2] [S4] [S5].

**The variant that keeps the money in the separate account** is the 실적배당 종신연금 /
GLWB, and it is a different product. The payment identity common to every retrieved GLWB
contract is

    실적배당 종신연금 지급액 = Max(연금기준금액, 계약자적립금) × 실적배당 종신연금 지급률

[S2] [S7 제2조] [S8], with the 연금기준금액 set at annuitisation as the greater of the
최저연금기준금액 and the account value and, on the enhanced forms, ratcheted annually
thereafter [S2] [S7] [S8]. The 지급률 is a three-factor scale — a base rate by sex and
annuity age, uplifted by a persistency factor and an in-the-moneyness factor — and that
three-factor structure is the **Korean market convention**, not one carrier's idea
[S2] [S7] [R1]:

    실적배당 종신연금 지급률 = 기본지급률 × (1 + 장기유지 가산율 + 투자실적 가산율)

    기본지급률 (연, [S2])      55–59세 남 4.00 / 여 3.80;  60–64세 4.65 / 4.45;
                               65–69세 5.10 / 4.85;        70–80세 5.50 / 5.30  (%)
    기본지급률 (월, [S7])      55–59세 0.29 / 0.27;  60–69세 0.33 / 0.31;
                               70–79세 0.37 / 0.36;  80세 0.41 / 0.41           (%)
    장기유지 가산율 ([S2])     10–19년 0%; 20–24년 5%; 25–29년 10%;
                               30–39년 15%; 40년 이상 25%
    투자실적 가산율 ([S2])     계약자적립액 ÷ 연금기준금액 < 60% → 0%;
                               60–90% → 15%; ≥90% → 30%

A 0.33% monthly rate is 3.96% a year, so the two scales are close once annualised, and [R1]
records the same carrier's earlier product at 0.30/0.29 and 0.35/0.33 — the scale has been
**cut** between the 2017 census and the retrieved contract. One further document prints the
rate as a closed-form formula — 연금지급개시나이 × (3 × 연금개시 전 보험기간 + 2 × 거치기간
+ 100) ÷ (365 × 365 × 12), times 1.4 for the 10년 집중지급형 — the only algebraic annuity
factor found in any Korean variable document; but **the unit of its output is not stated**
and the two readings differ by a factor of a hundred, so its **form is verified and its
level is [unverified]** [S8].

Under the GLWB the guarantee charge **continues to be deducted from the separate account for
life** — 「일반적인 변액연금과 다르게 연금개시 이후에도 특별계정 적립금에서 보증비용이
공제됨」 [R2]. On [S2]'s own illustration, at a −1.0% gross return the account is
**exhausted before year 20**, and even at the 평균공시이율 the twenty-year surrender value is
₩11.5 million against ₩36 million of premium. A GLWB of this shape is not a savings product;
it is a purchase of guaranteed lifetime income, and the technical notes say so.

---

## Riders and options

**In scope (modelled).** The base contract's compulsory GMDB and elected GMAB, both
parameterized above [S1] [REG-R16]; the 고도재해장해급여금 [S1] [S2]; the full charge stack
[S2]; the 해약공제 [S2]; and the 종신연금형 10년 보증기간부 payout [S1] [S2] [S5].

**Modelled as switches, off in the base run.** 추가납입 [S1]; 중도인출 [S1]; the 미보증형,
with the GMAB and its charge both removed [S4] [S5] [R2]; 펀드자동재배분 and
펀드자동전환옵션 [S5] [S7 제40조]; and a static-versus-dynamic lapse basis, the dynamic form
being a **[std]** construction [R1].

**Described but not modelled.** 보험료 납입 일시중지, 납입중지 and 납입종료 [S1]; 감액
[S4] [S7 제2조]; 조기연금개시 [S1] [S9] [S10]; voluntary 일반계정 전환 [R1] [S6];
보험계약대출 and its general-account variant [REG-R25 제33조](#krlib-reg-r25) [S5]; 정기중도인출서비스 and
자동인출서비스 [S1] [S5]; 평균분할투자 [S7 제41조]; the 성과보너스 at 120/140/160/180/200%
of premiums paid, each paying 기본보험료의 100% once [S9]; the 장기유지 보너스, funded from
a general-account reserve and **forfeited on surrender** [S7 제6조] [S7 제50조제5항]; and the
장기유지 운용보수 환급 [S7 제7조].

**Riders offered but out of scope.** (무)보험료납입면제특약 on a 50%-or-more disability
[S5] [S6]; 무배당 신보험료납입면제특약(3대질병형) on cancer (excluding 기타피부암, 갑상선암,
대장점막내암, 비침습 방광암), 뇌출혈 or 급성심근경색증, with a **90-day cancer waiting
period** [S2]; 납입면제특약Ⅱ in an 80%-disability form and an
80%-disability-plus-three-major-illness form [S10]; 연금전환특약Ⅲ and
장기간병연금전환특약 [S7]; 지정대리청구서비스특약 [S7]; 변액보험 펀드추가서비스특약 [S7];
and the 장애인전용보험전환특약 under 소득세법 제59조의4제1항제2호 and 시행령 제107조제1항
[S5]. Rider premium on a variable annuity qualifies for the 보장성보험료 credit —
「납입한 특약보험료 연간 100만원 한도로 납입금액의 100분의 12를 세액공제」 [S5] [S6]
[REG-R57].

**Out of scope entirely.** The GLWB / 실적배당 종신연금 and the GMWB
[S2] [S7] [S8] [S10] [R2]; the roll-up, step-up and ratchet GMAB bases, specified above but
not run [S2] [S6] [S7] [S9] [S10]; the CPPI-funded guarantee and its absorbing barrier [S6];
the elective, revocable GMAB [S9]; 거치형 (single-premium) forms and their nil surrender
charge [S5] [S6] [S10] [R1]; the 확정연금형, 상속연금형, 보증금액부 종신연금형, 체증형 and
노후설계자금 payout options [S1] [S2] [S5]; joint-life annuity forms [S9]; and **GMIB**,
which [R1] found 미도입 in Korea at 2017-05-31 and which nothing retrieved in 2026 either
shows on sale or rules out — **[unverified]** as a current statement.

---

## Variations across insurers

Carrier identity below is by `[S#]` tag, as in the research file. Where a row is bracketed
by a single source that is said, because a range of one is not a range.

1. **Whether there is a GMAB at all, and who pays for it** — the widest variation in the
   product, and the one the 2016 rule change created. Observed: charged and fixed at issue
   [S1] [S10]; charged, electable and revocable, the floor set at the account value two
   business days after election and ratcheted monthly [S9]; **unfunded**, paid for with a
   CPPI overlay [S6]; and absent [S4] [S5]. [R1] predicted the drift — 「IFRS17이 도입되고
   보증리스크를 공정가치로 평가하여야 하는 보험회사의 입장에서 … 최저보증이 없는
   변액연금상품의 출시와 판매가 늘어날 것으로 예상된다」 — and made the counter-argument
   this spec should record: 「최저보증이 없는 변액연금상품은 펀드 등 유사한 금융상품과
   차별성이 약하기 때문에 경쟁력 강화를 위한 방안이 모색될 필요가 있다」. **Chosen:**
   charged and fixed — the only shape exercising charge, base and payout in one run.
2. **The guarantee base.** Premium refund ↔ step-up ↔ ratchet ↔ roll-up, with 22 of 36
   census products setting the guarantee above premiums paid [R1]. Roll-up rates observed:
   7%/6% simple, converting to **연복리 4.32%** on that document's own 대표계약 — 40세 남성,
   10년납, **연금개시나이 65세**, and so not this composite's anchor cell [S2]; 5%/4%
   simple [S7]; 1.0% or 2.0% compound on a net base [S10]; and an illustrative 6% per three
   years [R2]. **Chosen:** premium refund at 100% — footnote 2 above.
3. **Ratchet frequency spans three orders of granularity**: monthly [S6] [S9], annual
   [S7 보증강화형] [S8], three-yearly and **daily with a three-business-day confirmation**
   [R1]; and one design tests only over a window ending three years before annuitisation
   [R1]. [R1]'s fifteen-year comparison shows the three-yearly ratchet missing a year-12
   spike the step-up locked in. **Chosen:** no ratchet in the base run, with the monthly
   form [S6] as the specified variant because it is the hardest to model and subsumes the
   coarser ones.
4. **The GMDB base and charge move together.** Premiums paid at 0.05% [S4] [S9] [S10] or
   0.07% [S1]; the roll-up 최저연금기준금액 at 0.40% falling to 0.25% after twenty years
   [S2]. The eight-fold spread in the charge is a spread in the *base*, not in the price of
   risk. **Chosen:** premiums paid at 0.07% [S1].
5. **Where the money goes at annuitisation.** Transfer to the general account and a
   declared-rate annuity — the market default, 「대부분의 변액연금상품은 …」 [R2] [S6] —
   against staying in the separate account with a lifetime withdrawal guarantee
   [S2] [S7] [S8] [S10]. The second doubles the charge stack and carries it for life.
   **Chosen:** the general-account transfer — footnote 16 above.
6. **The 계약체결비용 and what happens at year ten.** 5.17% of the basic premium for ten
   years [S2]; 6.12% for ten years and then **exactly 0.00%** [S4]; 1.3% online [R1]. The
   2017 census found the same split — 「월납 적립식 변액연금의 경우 계약체결비용은 계약체결
   후 10년 이내까지 부과되는 것이 일반적이며, 해지공제가 적용되지 않는 8년 이후에는
   계약체결비용이 줄어드는 경우가 대부분이다」, with 5.58–6.91% charged through year 7,
   2.33–3.6% from year 8, and 5.02–6.1% where a flat ten-year charge is used [R1].
   **Chosen:** the flat ten-year 5.17% [S2], the simplest shape and the one whose surrender
   charge is published alongside it.
7. **The 해약공제 scale.** Year-1 ratios 19.5% [S2], 25.6% [S5] and 28.1% [S4] against a
   2017 census range of 19.1%–27.6% with a mean of **25.6%** [R1]; [S5]'s 2025 scale
   reproduces the 2017 mean row **exactly**, [S4] sits above the 2017 maximum and [S2] at
   the 2017 minimum. The distribution has not moved in eight years, and the functional form
   `C × (7 − t) ÷ 7` is identical across all three. **Chosen:** [S2]'s C = ₩830,000, for
   the internal-consistency reason at footnote 10.
8. **Investment-risk control.** A mandatory bond-weight ladder by deferral period
   [S1] [R1]; automatic rebalancing three years before annuitisation [S1] or above a 30%
   non-bond share from year two [S7 제40조]; target-return de-risking at 110–200% [S5]; a
   forced 50/50 채권형II + EMP AI형 allocation on electing the guarantee [S9]; equity caps
   of 80% / 60% / a single fund as the guarantee deepens [S10]; and a CPPI overlay with an
   irreversible transfer to the general account [S6] — one trade in six forms: **the
   guarantee level and the investment freedom are priced against each other**. **Chosen:**
   the bond ladder plus the three-year de-risking [S1], on in the base run.
9. **Death cover before annuitisation.** None, with a 재해장해 benefit instead
   [S1] [S2] [S6 1종] [S7 제3조]; or a 기본사망보험금 of 적립형 기본보험료의 10배 / 거치형
   기본보험료의 10% added to the account [S5] [S6 2종]. [R2] records the drift to the first
   form 「환급률 제고를 위해」. **Chosen:** no death cover — footnote 15 above.
10. **Transaction charges.** 추가납입 free at six carriers, 1.5% at one [S2]; 중도인출 free
    at three [S1] [S2] [S9] and Min(0.2%, ₩2,000) with four free a year at four
    [S4] [S5] [S6] [S10]; 펀드변경 free at two [S5] [S9], ≤0.1% capped ₩5,000 with four free
    at two [S1] [S2], Min(0.1%, ₩2,000) at one [S10]; 연금수령기간 중 관리비용 연금 연액의
    0.5% [S4] against min(영업보험료의 3.5%, ₩4,000) per month per 구좌 [S2]. **Chosen:**
    the free forms and the proportional annuity charge, matching the anchor carriers.
11. **Issue and term envelopes.** 가입나이 0–75 across the set and 만15세–70세 at the anchor
    carriers; 납입기간 3–30 years plus single premium; minimum deferral **1–7 years**;
    연금개시나이 45–85, with the **guaranteed forms starting later (55) and ending earlier
    (80)** [S10]. The minimum deferral is the insurer's first line of defence against the
    GMAB and it lengthens with the guarantee: 「연금적립금을 보증하는 상품의 경우 일반적으로
    최소거치기간을 5년 또는 7년 정도 설정하고 있다」 [R1]. **Chosen:** 만15세–70세, 45–80,
    seven-year minimum deferral [S1].
12. **Menu size.** 5 funds [S4] to 51 [S10], with 특별계정 운용보수 totals from 0.20% to
    0.89% across five published tables [S1] [S2] [S4] [S5] [S9]. [R2] notes that roll-up
    designs 「일반적으로 선택 가능한 펀드의 수가 적게 구성될 수 있으며 다른 펀드로 변경이 안
    되고」, so menu size is itself a guarantee-control device. **Chosen:** two funds at the
    anchor carrier's own rates.
13. **What does not vary at all.** The separate account is set up under 보험업법
    제108조제1항제3호 and accounted for separately [R4] [S7]; the unit is ₩1 at establishment,
    the price opens at ₩1,000 per 1,000좌 and is published to two decimals [S7] [R2]; the
    account is valued **daily** and the 운용보수 deducted **daily** while the mortality and
    guarantee charges come out **monthly on the 월계약해당일** [S7 제36조] [R2]; a GMDB is
    compulsory [REG-R16] [R1]; **the surrender value carries no guarantee whatever**
    [S1] [S6] [S7] [S8] [S10]; the surrender charge runs off to zero within seven years
    [S2] [S4] [S5] [R2]; additional premium is capped at 200% and a withdrawal restores the
    headroom [S1] [S2] [S4] [S5] [S6] [S7] [S10]; withdrawals are limited to twelve a policy
    year and, within ten years, to premiums paid [S1] [S2] [S5]; the guarantee base is
    reduced pro rata for withdrawals and reductions [S2] [S4] [S7]; the annuity factor may
    be re-struck at annuitisation but **only upward** [S1] [S2] [S5]; the licence and the
    적합성 진단 gate the sale [R2] [R3] [R6] [S1] [S5]; three illustration returns must be
    shown with a 순수익률 beside each [R2]; and the contract is outside the 예금자보호법
    except for the guaranteed amounts [R2] [S1] [S2] [S5] [S6] [S8].

---

## Regulatory context

**The separate account is a statutory construct.** 보험업법 제108조제1항 permits an insurer
to set up a 특별계정 for four contract classes, of which **제3호 is 변액보험계약**; 제2항
requires each account's assets to be accounted for separately from every other separate
account and from all other assets; 제3항 permits the account's profits to be distributed to
its policyholders; 제4항 delegates asset management, valuation, profit distribution and
comparative disclosure to Presidential Decree [R4] [REG-R6]. 감독규정 제5-6조제1항제3호 makes
the account **mandatory** for a life insurer's variable business, 제5-6조제3항 permits it to
be run as two or more 집합투자기구, and **제5-6조제5항 defines what goes into it** — the
적립 보험료, 「영업보험료에서 위험보장에 필요한 부분과 사업비 등 기초서류에서 정한 사항을
차감한 금액」 — which is exactly the account recursion this model implements [REG-R15].
제5-7조 lists the permitted transfers and 제6-26조 appropriates the whole of the account's
annual profit or loss to the contract [REG-R15]. 보험업법 시행령 제52조 and 제53조 were
identified (시행 2024-10-25, 대통령령 제34960호) but **not read**, so the account-per-class
rule, the bar on exercising voting rights on separate-account shares and the bar on
guaranteeing a return in advance on a 변액보험계약 are entirely **[unverified]** [R13]; no
fact in this document rests on them.

**The GMDB is compulsory; the GMAB is not.** 감독규정 제7-60조제7호 requires a 최저사망보험금
on every 변액보험 [REG-R16] [R11]. The same article's **제2호** is the reason the surrender
value may be unguaranteed at all: a 저축성보험's survival benefit must exceed premiums paid
**except** for an annuity paying a 생존연금 and **except for 변액보험** [REG-R16]. **제3호
and 제4호** carry a design test that names this product's charges explicitly — the
계약자적립액 accumulated at the 평균공시이율 must exceed premiums paid at 납입완료, and in
running that test the **risk premium, the guarantee charge and the separate-account
management fee are set to zero** [REG-R16]. The April 2016 amendment making the GMAB
optional was to the 보험업감독규정 and the 보험업감독업무시행세칙 [R2]; the amending
instrument was not retrieved and its identity is **[unverified]**.

**Surrender values.** 감독규정 제7-66조제1항 sets 해약환급금 = 계약자적립액 less the
해약공제액, floored at zero; caps the 해약공제기간 at **7 years**; and fixes the charge at
the **표준해약공제액** of 별표 14 [REG-R19] [REG-R20]. **제7-66조제4항제1호 excludes
변액보험 from the 무해지 / 저해지 dispensation** [REG-R19] — the exclusion was inserted on
2020-11-19 — so a Korean variable annuity may never pay less than the 별표-14-floored value
during the payment period, and the suppressed-surrender-value forms that dominate Korean
protection sales cannot appear on this chassis. **제5항** requires 미경과보험료 to be added
to the surrender value on termination [REG-R19]. The 계약자적립액 itself accrues **monthly
before 납입완료 and daily afterwards** under 제7-66조제1항제4호, whose two formulas render as
images in the retrieved 고시 and did not extract [REG-R19].

**The 산출방법서 is the boundary of what is public.** 감독규정 제7-64조 lists its five
필수기재사항, which include the 해약환급금 calculation with its interest rate, 위험률 and
해약공제액, a comparison against the 표준해약공제액 where the 계약체결비용 exceeds it, and —
listed separately — **the calculation of any 보증비용** [REG-R18]. The document is filed with
the supervisor and is not published [REG-R2]; the 보험상품신고서 must be filed **30 days
before the sale-start date** with the 기초서류 verified by the 선임계리사 [REG-R8 제71조](#krlib-reg-r8).
Every recursion in `technical-notes.md` is therefore a **[std]** construction consistent
with, and not derived from, the retrieved contracts.

**Reserving.** 보험업법 제120조 → 시행령 제63조 → 감독규정 제6-11조 restate the reserve in
IFRS 17 vocabulary as a 보험계약부채 split into 발생사고요소 and 잔여보장요소, measured on a
**현행추정치** basis, with the detailed calculation delegated to the FSS Governor
[REG-R3] [REG-R8] [REG-R10]. Two further reserves sit inside retained earnings and both bear
on this product:

- **해약환급금준비금** (감독규정 제6-11조의6) — a **company-level** comparison, at every
  balance-sheet date including quarterly interim closes, of the fair-valued liability
  against the 해약환급금 computed under 제7-66조제1항, reserving the shortfall
  [REG-R11] [R8]. Its 제2항 test explicitly brings in **특별계정부채 limited to the
  계약자적립금 of 제6-26조제1항제1호** — that is, this product's account value [REG-R11].
- **보증준비금** (감독규정 제6-11조의5) — required inside retained earnings for expected
  losses on benefit guarantees, and **explicitly junior**: 「보증준비금은 제6-11조의6에 따른
  해약환급금준비금을 적립한 후에 적립하여야 하며, 이익잉여금에서 … 해약환급금준비금을
  차감한 금액을 한도로 한다」 [REG-R10]. The surrender-value reserve is taken **first** and
  the guarantee reserve second — the opposite of the intuition a drafter brings from a
  market where guarantee reserves are liabilities. [R8] describes the same construction from
  the FSC's side: the 보증준비금 is 「기존 보증준비금 + 장래 수취할 보증수수료」, both
  reserves moving from liability accounts into statutory reserves inside retained earnings
  from **2023**, restricting distributable profit while protecting policyholders.

**The guarantee reserve's measure.** 시행세칙 <별표 24> makes it the greater of a stochastic
figure — 「사망률, 해지율, 자산이익률(1,000개)을 이용하여 만기까지 장래 예상되는 순손실액을
현가로 환산한 상위 30% 평균 금액」, i.e. **CTE(70) over 1,000 scenarios** — and a standard
factor tabulated by 보험종류 × 최저보증종류 × 보증수준 × 주식비중한도 [R1] [R12] [REG-R26].
**별표 24 was not retrieved** in either research pass: law.go.kr returned the navigation
shell and the mirror returned HTTP 403, so every figure below is reproduced from [R1] and is
**[unverified]** against the rule. For 변액연금 GMAB:

| 주식비중한도 | 기납입보험료 보증, 보증수준 <95% … ≥115% | 스텝업·롤업 등 |
|---|---|---|
| 40% 미만 | `0.7% × Max{적립률, 0.40%} ÷ 0.5%` … `0.55% ÷ 0.5%` | `0.60% ÷ 0.5%` |
| 40% 이상 50% 미만 | `0.7% × Max{적립률, 0.45%} ÷ 0.5%` … `0.60% ÷ 0.5%` | `0.65% ÷ 0.5%` |
| 50% 이상 60% 미만 | `0.7% × Max{적립률, 0.50%} ÷ 0.5%` … `0.65% ÷ 0.5%` | `0.70% ÷ 0.5%` |
| 60% 이상 | `0.7% × Max{적립률, 0.55%} ÷ 0.5%` … `0.70% ÷ 0.5%` | `0.75% ÷ 0.5%` |

and for the other guarantee types a plain floor — 변액연금 GMDB `Max{적립률, 0.04%}` rising
to 0.07% by equity band, GMWB and GLWB `Max{적립률, 0.6%}` rising to 0.9% — with
「적립률 = 직전 1년간 최저보증비용 합계 ÷ {(기시 계약자 적립금 + 기말 계약자 적립금) ÷ 2}」
and 「주식비중한도는 기초서류상 최대 주식투자 비중을 적용함」 [R1] [R12]. **The last note is
why the mandatory bond weight matters to the insurer and not only to the policyholder**: the
reserve floor is indexed to the maximum equity weight in the filed basis, so lowering the
equity cap lowers the reserve directly. The anchor cell's 50% equity allocation puts it in
the 50–60% band. Required capital, **보증위험액**, is a **CTE(95)** less the 보증준비금,
floored at zero, subject to minima of 계약자적립금의 0.15% (저축성 최저사망보험금), 1%
(보장성 최저사망보험금) and **2% (최저연금적립금)** [R1]. Fair-value measurement of the
guarantee liability commenced May 2017 with the capital increase phased 35% / 70% / 100% at
the 2017, 2018 and 2019 year-ends [R1]. Hedging is recognised against 보증위험액, the stress
being the worst of four corners — **주식 ±12% × 금리 ±90bp** — which is the only explicit
guarantee stress scenario retrieved [R1]. [R1] also catalogues the four management
strategies — 무헤지 자본금 충당, 재보험, 정적헤징 and 동적헤징 — none of which the model
represents.

**The two live measurement regimes.** K-IFRS 제1117호 has been **mandatory** for Korean
insurers since 2023-01-01 [REG-R60] [REG-R14], and K-ICS commenced the same day; the
건전성감독기준 재무상태표 is re-measured 「경제적이고 시장가격과 일관된 가치로」 with no
own-credit adjustment, the required capital aggregating five risk modules of which the
life-and-long-term-health module alone carries seven shock-based sub-risks including
**해지위험액** and **사업비위험액** [REG-R13]. The 지급여력비율 floor is **100%**
[REG-R8 제65조제2항제1호](#krlib-reg-r8), below which the 적기시정조치 ladder starts [REG-R14]. The
transition 부칙 accumulates the transition-date **변액보험 guarantee reserve at 「매 사업연도별
해당시점의 평균공시이율」** [REG-R14] [REG-R48]. **No `krlib` model computes a CSM, a risk
adjustment, a 요구자본 or a 보증준비금**; the model projects gross contractual cash flows and
names the measurement each would feed.

**Disclosure.** A carrier selling variable products must run a 변액보험공시실 publishing,
**daily**, 「특별계정 운용현황(기준가격, 기간별 수익률 및 연환산수익률, 매월 말 자산구성내역,
특별계정보수 및 비용 등)」 and let a logged-in policyholder see their 적립금, 해약환급금,
보유좌수 and 수수료 안내표 [R2] [S1]. A 보험계약관리내용 must go out in writing
**quarterly** for a variable contract, showing 「납입보험료와 납입보험료에서 사업비,
위험보험료를 차감한 특별계정 투입금액 및 계약자적립금」, and — because the separate account
is treated as a 자본시장법 투자신탁 — so must an 자산운용보고서 confirmed by the trustee
[R2]. The 생명보험협회 공시실 publishes daily unit prices and returns by fund and, for
savings-type variable products, 사업비율, 위험 보장비율 and **최저보증비용비율**
[R2] [S12] [REG-R45]. The **수수료 안내표** is compulsory before sale, after sale and
always [R2] — it is the table reproduced under "Charges" above.

**Illustration.** Three returns are mandatory and their level is set by regulation:
「−1%, 평균공시이율, 평균공시이율의 1.5배」, with a **순수익률** beside each since
2009-04-01, 순수익률 being 「투자수익률에서 최저보증관련 비용 등이 차감된 후의 수익률」
[R2]. Where a contract has **no GMAB** the low case must be negative and at least three
returns shown, or the surrender-value illustration omitted altogether: 「최저연금적립금을
미보증하는 상품의 경우에는 … 해약환급금 예시를 제외하거나 (-)평균공시이율 가정을 포함하여
3개 이상의 수익률을 가정하여 기재하도록 하고 있다」 [R2] — which is exactly [S9]'s
−2.25% / 2.25% / 3.375% set. The 평균공시이율 is **2.50% for 2026**, down from 2.75% — the
first fall since the 2.50% → 2.25% cut that took effect for 2021 [REG-R48]; the article
number [S9] cites for its definition, 감독규정 제1-2조제13호, was not verified against the
retrieved 고시 and is **[unverified]** [R2].

**Deposit protection.** A variable contract is **outside** 예금자보호법 — 「이 상품의
해약환급금 등 지급금은 '예금자보호법'에 의해 보호받지 않습니다」 [S8] — **except** that
since **2016년 6월** 「최저보증 옵션에 따른 최저보증보험금에 한해서는 「예금자보호법」에
따라 예금보험공사가 보호하는 것으로 변경되었다」 [R2], the contracts naming 최저사망적립액,
최저연금적립액 and riders as the protected amounts [S1] [S2] [S7 제63조]. The limit is
**₩100,000,000 (1억원)** per person per insurer under 예금자보호법 시행령 제18조제7항, in
force 2025-09-01 [REG-R52] [REG-R32] — the two 2025 product documents state it [S5] [S6]
against ₩50,000,000 in the 2023–2025 documents [S1] [S2] [R2], whose date and instrument the
research file could not retrieve.

**Tax.** 변액연금보험 is a **non-qualified** annuity: no contribution-stage tax credit, and
its gain is 이자소득 rather than 연금소득 [S8]. 소득세법 제16조제1항제9호 makes the 보험차익
of a 저축성보험 interest income except on two routes, both in 시행령 제25조 [REG-R58]:

- the **10-year route**, requiring ten years from first premium to maturity or surrender and
  either aggregate premiums per policyholder across all such policies of **₩100,000,000
  (1억원)** or less for contracts made from 2017-04-01, or a **월적립식** policy meeting all
  three of a payment term of **5 years or more**, a level monthly basic premium (an increase
  up to 1× allowed) with prepayment of no more than six months, and aggregate monthly
  premiums per policyholder of **₩1,500,000 (150만원)** or less; and
- the **종신형 연금보험 route**, requiring an annuity from age 55 after the premium term
  until death, no payment in any other form, extinction of the contract and the annuity fund
  on death with any guarantee period **within the 기대여명 연수 published by the
  국가데이터처**, identity of policyholder, insured and beneficiary, no surrender after the
  first annuity payment, and an annual annuity within a stated formula (which renders as an
  image and did not extract).

The anchor cell — ₩300,000 a month, level, ten-year term, twenty years to annuitisation —
clears the 월적립식 route on every limb, and the representative payout form is written so
that the 종신형 route is also available [REG-R58]. A contract may be **elected as taxable**
at issue or later, in which case its premiums do not count against the caps, and the reverse
election is not permitted; where an exemption condition fails the tests are applied in the
order 종신형 → 월적립식 → 일시납; and changing the policyholder, converting a protection
contract to a savings contract, or increasing the basic premium by more than one times the
original all **restart the ten-year clock** [R2] [REG-R58]. **Payout-phase taxation of a
실적배당 종신연금 was not established by any retrieved document and is [unverified]** — it
does not arise on the representative design, which pays from the general account.

**Contract law.** 상법 제4편 is one-way mandatory under 제663조 [REG-R49]. The provisions
this product touches are 제638조의3 (delivery and explanation of the 약관, three-month
cancellation), 제649조 (termination at will, with the 미경과보험료), 제650조의2
(reinstatement where the surrender value has not been paid), 제651조 and 제651조의2
(고지의무위반), 제655조 (the causation defence) and 제662조 (three-year prescription)
[REG-R49]; and, in 인보험, 제727조제2항 (payment by instalments, the statutory hook for an
annuity), 제730조–제731조 (consent), 제732조의2 and 제736조 (return of the 보험적립금)
[REG-R50]. The 표준약관 of 시행세칙 별표 15 implements all of it and is where the 보험나이
rule, the 15/30-day cooling-off period, the three-month 품질보증해지, the 14-day 납입최고
and the three-year 부활 window come from [REG-R25] [REG-R23].

**Sales.** 보험업법 제83조, 시행령 제56조 and 감독규정 제5-4조 gate the licence; the
examination is 40 questions in 60 minutes with a pass mark of 「100점 만점에 70점 이상」,
open only to solicitors under 제83조 and closed to those handling only non-life or 제3보험
products [R6]. The continuing-education requirement comes from [R2], not from the
examination regulations, which do not state it [R6]. 금융소비자보호법 제17조 and 제18조
carry the suitability and appropriateness principles and 제46조 the cooling-off right
[R14] [REG-R51].

**Expense and commission regulation.** The 2019 FSC reform required from **January 2021**
that first-year commission plus surrender value not exceed premiums paid, offering
split-payment commission structures as an alternative to front-loading [R7] [REG-R29].
감독규정 제4-32조 now carries that test and requires an instalment structure paying **no more
than 60% of the 표준해약공제액 a year** where that amount exceeds one year's premiums;
제7-51조 requires pre-notification of a 저축성보험 that does not spread at least 50% of its
acquisition cost evenly over the premium term (70% bancassurance, 100% online) [REG-R22].
The distribution economics behind the composite, from the 2017 census: 월납 변액연금
모집수수료율 averaged **2.11%** of total premiums payable over five years (maximum 3.13%,
minimum 1.10%), and single-premium products paid **2.47%** entirely at issue [R1].

**What the model does not attempt.** No CTE(70), no CTE(95), no 보증준비금, no
해약환급금준비금, no 요구자본, no CSM and no stochastic scenario set. The model projects the
contractual cash flows of one policy on one return path, publishes the guarantee's intrinsic
cost on that path and the 별표 24 standard factor beside it, and states — here and in
`technical-notes.md` — that the difference between the guarantee charge collected and the
intrinsic cost computed is a single-path residual, not a measure of the guarantee's value.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-variable_annuity-r1
[R10]: #krlib-variable_annuity-r10
[R11]: #krlib-variable_annuity-r11
[R12]: #krlib-variable_annuity-r12
[R13]: #krlib-variable_annuity-r13
[R14]: #krlib-variable_annuity-r14
[R2]: #krlib-variable_annuity-r2
[R3]: #krlib-variable_annuity-r3
[R4]: #krlib-variable_annuity-r4
[R5]: #krlib-variable_annuity-r5
[R6]: #krlib-variable_annuity-r6
[R7]: #krlib-variable_annuity-r7
[R8]: #krlib-variable_annuity-r8
[R9]: #krlib-variable_annuity-r9
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R14]: #krlib-reg-r14
[REG-R15]: #krlib-reg-r15
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R23]: #krlib-reg-r23
[REG-R24]: #krlib-reg-r24
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R45]: #krlib-reg-r45
[REG-R46]: #krlib-reg-r46
[REG-R48]: #krlib-reg-r48
[REG-R49]: #krlib-reg-r49
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R57]: #krlib-reg-r57
[REG-R58]: #krlib-reg-r58
[REG-R6]: #krlib-reg-r6
[REG-R60]: #krlib-reg-r60
[REG-R7]: #krlib-reg-r7
[REG-R8]: #krlib-reg-r8
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
