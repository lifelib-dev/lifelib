```{module} krlib
```

# The **krlib** Library

```{warning}
{mod}`krlib` is in its draft stage, and its contents are subject to change as development
continues.
```

## Overview

The **krlib** library packages **ten reference liability cash flow projection models** for the
individual life, health and annuity products sold in Korea — built with modelx, and, for each
one, the product specification and technical notes the model was built from.

The coverage differs in kind from [jplib](../jplib/index.md), the closest market, and from
[uslib](../uslib/index.md), [uklib](../uklib/index.md), [frlib](../frlib/index.md) and
delib, because the Korean market does. **제3보험** (*je-sam boheom*,
"third insurance") is not a market label here but a **statutory licence category**: 보험업법
제4조제1항제3호 names 상해보험, 질병보험 and 간병보험, and 제4조제3항 deems a fully licensed
life insurer *or* a fully licensed non-life insurer to hold it [REG-R1]. Four of the ten
products sit in it, and they are not a supplement to the protection set — Korean personal
protection is written on both sides of the market, 생명보험 보장성보험 at ₩62.0조 against
손해보험 장기보험 at ₩73.3조 in 2025, and **the non-life figure is the larger of the two**
[REG-R47].

**실손의료보험** (*silson uiryo boheom*, indemnity medical insurance) is the sharpest case, and
the reason the set looks nothing like a translated jplib. The FSS calls it 「제2의 건강보험」 —
the second national health insurance — and it is held on **35.96 million individual contracts**
against a population near 51 million, sold as a reimbursement layer *on top of* 국민건강보험
[REG-R44]. It is the only **indemnity** contract anywhere in this repository: every other
product here, in every library, pays a stated sum, and this one reimburses an incurred cost
inside an annual limit. A Korea library without it would describe a market that does not exist.
Group business (단체보험), 퇴직연금, 자동차보험 and 일반손해보험 are out of scope. So is the
non-life carrier's version of each 제3보험 product: `krlib` models the life-insurer form
throughout, and each product document says where a 손해보험 contract differs and cites the
손해보험협회 disclosure portal where its documents actually came from [REG-R62].

The models are the centre of the library. Each is a by-model-point projection of one product's
gross liability cash flows: 보험료, 보험금, 해약환급금, expenses and commission, on the
product's own processing order and timing. None of them discounts — every model publishes the
cash flows and leaves discounting, the 책임준비금, the IFRS 17 CSM, the 해약환급금준비금 and
the K-ICS 요구자본 to a layer that consumes them.

**Each one of these models reproduces a documented worked example, asserted cell by cell to the
precision the notes display.** The chain is deliberate and complete in both directions:

- `product-spec.md` specifies a *representative* product — a standardized composite built from
  publicly available documentation of real products, not any single insurer's contract. It
  records contractual mechanics, a full parameter set, the observed variation across insurers,
  and the rationale for every representative choice.
- `technical-notes.md` turns that product into a liability cash flow model on paper: model
  point attributes, state variables, assumption inputs, the recursions with their explicit
  processing order, policyholder behaviour, and a numeric worked example.
- The **model** implements those notes, and the library's own `tests/` assert the worked
  example against it. Change an assumption, and the test tells you whether the model and the
  notes have parted company.
- `sources.md` lists every source the first two cite, with URLs, access dates and whether the
  document was actually retrieved.

Every quantitative parameter in the library is either **source-tagged** or marked **[std]** — a
standardization introduced for the reference implementation, carrying its rationale and, where
available, the observed range across insurers. Facts taken from source material are never
silently mixed with assumptions made to complete a model.

```{admonition} These are mechanics demonstrations, not pricing or reserving results
:class: warning

The **contractual** side of this library is unusually well sourced: Korean regulation puts more
of a product's mechanics into public instruments than any other market here — the 실손 benefit
definition is the supervisor's own 표준약관 [REG-R25], the surrender charge has a published
statutory cap with a formula [REG-R20], and the 무·저해지 lapse assumption is the subject of a
named supervisory ruling [REG-R27]. The **quantitative** side is the opposite. The 산출방법서
that holds every 예정이율, 적용위험률 and 예정사업비율 is a 기초서류, filed and never published
[REG-R2]; the 경험생명표 is released only as summary statistics [REG-R33] [REG-R34]; and no
Korean carrier publishes an expense rate, a commission scale or a lapse curve by duration. So
**every mortality table in this library is a [std] construction**, and so is every expense,
commission and behavioural assumption. Replace them with company data and a real 산출방법서
before drawing any conclusion from the numbers.
```

## The models

Model names are `<short name>_<country>_<grid>`: a short descriptor, then `KR`, then `_A` for
an annual step or `_S` for a monthly one. The grid letters follow lifelib, where
`annuallife/TradLife_A` is the annual-step model and `basiclife/BasicTerm_S` and
`savings/CashValue_SE` are the monthly ones. **Every model in this library runs on a monthly
grid**, so every name here carries `_S`; the `_A` half of the convention is still enforced by
`tests/test_model_conventions_kr.py` against the registry metadata, so a model added on an
annual step would have to be named for it. `S` carries a second sense in lifelib — scalar,
one model point at a time, as against the vectorized `_M` models — and that is true of all ten
here.

**The contract terms and the assumptions stay annual; only the grid underneath them is
monthly.** Korean bases are filed and published annually — 적용위험률 grids by age, the FSS
원칙모형 lapse vector by 경과기간, the 공시이율 as an annual declared rate — and the contracts
state their terms in whole years on the 계약해당일. So every model carries the annual figure
the source gives and applies a uniform-force monthly companion beside it: `mort_rate` with
`mort_rate_mth`, `lapse_rate` with `lapse_rate_mth`, `credit_rate` or `crediting_rate` with
its `_mth` form. Twelve of each compound back to the year's figure exactly, so the in-force at
every 계약해당일 reproduces the annual-step models these replaced, and the statutory annual
quantities — 별표 14's 연납순보험료, the 소득세법 세액공제 ceiling, the 연금수령한도 — are
computed annually and apportioned rather than restated on a monthly base the law does not
use.

The short names are **English, and chosen rather than found**. Everywhere else in this library
the English name leads and the Korean follows, which is the arrangement jplib, frlib and delib
settled on; a model name cannot carry the Korean at all, being a Python identifier and a
directory on disk. Nor is there much of a market short form to borrow — Korea says "CI보험" and
writes `CI`, and after that the abbreviations run out. So the pairing of model to product is
written down here and in `tests/kr_registry.py` rather than inferred.

**보장성 — protection**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [whole life (종신보험)](products/whole_life/index.md) | `WholeLife_KR_S` | monthly | 종신보험 (*jongsin boheom*), the savings-and-protection chassis: the 계약자적립액, the 해약환급금 as `max(0, V − SC)`, 보험계약대출 as a modelled state, and the 납입면제 with premiums **deemed paid** — which on a suppressed form is the only route to the cliff the policyholder does not have to fund. The 저해지환급형 suppression multiplies a **표준형 comparison twin priced with the lapse assumption switched off and never sold**, so there is one account in the model and the payable value is independent of the sold form's own premium. The step at 납입완료 is exactly `1/k` = 2.0 and falls thirteen years *after* the surrender charge has run off, so it cannot be explained as a surrender-charge effect |
| [term life (정기보험)](products/term_life/index.md) | `Term_KR_S` | monthly | 정기보험 (*jeonggi boheom*), the protection chassis and the most sourced product in the library: the anchor's ₩15,080 a month is published twice independently, and the whole 갱신형 (*gaengsinhyeong*, renewable) ladder ₩9,000 → ₩21,000 → ₩56,000 → ₩201,000 is public. The premium is a function of the **renewal index** and not of the policy year, so the horizon is the 보험나이 80 ceiling rather than the term, and renewal decline is its own decrement taken after mortality and after lapse — 90.7% of everyone who leaves in a boundary year. Both contract-boundary readings ship as model points, and they differ in sign |
| [critical illness (CI보험)](products/ci_insurance/index.md) | `CI_KR_S` | monthly | CI보험 / 중대질병보험 (*jungdae jilbyeong boheom*): 80% accelerated on the first qualifying event, with the contract **surviving** it, because 감독규정 제7-60조제8호 forbids extinguishing a contract while the risk it covers remains. So an acceleration is a **transition and not an exit**, and the post-CI cohort is carried by the policy year it accelerated in. The residual death benefit is `max(20% B, 105% V)` on two different clocks, and the account limb passes the nominal at duration 7 — a model hard-coding 20% of the sum assured understates the post-CI liability by a factor of **4.43** over the anchor's life. The 저해지 suppression here has two exits, 납입완료 and a CI claim, the second a random date correlated with the product's own decrement |

**제3보험 — third insurance (보험업법 제4조제1항제3호)**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [indemnity medical (실손의료보험)](products/indemnity_medical/index.md) | `Medical_KR_S` | monthly | 4세대 실손의료보험 (*silson uiryo boheom*), the library's only **indemnity** contract: an annual limit that *caps* a claim rather than a 보험가입금액 that determines one, on a benefit definition that is the supervisor's 표준약관 and not a carrier's [REG-R25]. Five reductions must be applied in order — the public 본인부담상한제 truncation first, as an exclusion from covered loss; then the per-event co-payment and deductible, applied to the cost **distribution** and never to its mean; then the ₩2,000,000 annual inpatient cap, the 3대비급여 sub-limits and the ₩50,000,000 aggregate. The renewal premium of the 비급여 rider is a function of that policyholder's own prior-year claim, so claims feed premium inside a single policy on an annual clock, and the discount is **solved** from the wording's revenue-neutrality constraint rather than set |
| [cancer (암보험)](products/cancer/index.md) | `Cancer_KR_S` | monthly | 암보험 (*am boheom*), the fixed-benefit (정액) 제3보험 chassis, and the one morbidity model in `krlib` whose incidence basis is **sourced**: 보험개발원's published 「기타피부암 및 갑상선암 이외의 암 발생률」 grid, stated on the insured definition excluding C44 and C73 [REG-R61]. The tier algebra differs line by line — 일반암 and 특정소액암 **partition** that rate, 고액암 is a **subset** paid in addition, and 유사암 is **additive**, with a share that reaches 1.60 at female 만나이 20 — so a model constraining four shares to sum to one prices the reduced tier out of existence exactly where it dominates. Two waiting periods, one of which is zero; six select-duration cohorts behind the care limbs, on a thirteen-month delay that only one identity catches |
| [long-term care (간병보험)](products/long_term_care/index.md) | `LTC_KR_S` | monthly | 간병보험 (*ganbyeong boheom*): a three-state model — healthy, in care, dead — whose trigger is the **public** scheme's own 장기요양등급 under the 노인장기요양보험법 [REG-R54], so the benefit definition belongs to a statute rather than to a carrier. The one large public dataset counts people **holding** a certification, not entering one, so the modelling work is the prevalence-to-incidence conversion, done in the open with its excess-mortality term shown; and the care state is entered in two steps, direct entry and progression, because only 13.3% of current 1등급 certifications arose from a first application. The 간병연금 is survival-tested annually with the amount **and** the 감액 decision both frozen at first certification |
| [children's insurance (어린이보험)](products/child/index.md) | `Child_KR_S` | monthly | 어린이보험 (*eorini boheom*), commonly written **in utero**, so the projection opens on a life that does not yet exist: months 0–4 carry premium on three streams, a **void** decrement that refunds every won paid, and no cover on the child at all. Its 납입면제 runs on the **계약자** as well as the child — a decrement on a life who is not the insured, 33 years older, read from a second row of the same table — and 상법 제732조's bar on insuring the death of a life under 만 15 means the death column pays the 계약자적립액 rather than a benefit [REG-R50] [REG-R17]. 1,201 months on the anchor cell, eighty of the hundred years paid-up |

**저축·연금 — savings and annuity**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [pension savings (연금저축보험)](products/pension_savings/index.md) | `Pension_KR_S` | monthly | 연금저축보험 (*yeongeum jeochuk boheom*), the tax-qualified accumulation contract: the whole-life account with a declared 공시이율 over a stepping 최저보증이율 floor, the 100.1%-of-premiums minimum fund at the 연금개시일, and the annuitisation step. There is **no survivorship release** — the 계약자적립액 is a contractual balance, not a net-level-premium reserve, so the deferral-phase mortality strain is exactly zero and `claims_death` and `claims_lapse` pay the same number under two decrements. The payout factor is a **monthly** annuity-due, which is what reconstructs all eight published illustration figures on both interest bases from one formula; and which vintage of the annuitant table it is struck on is a switch, because a one-way ratchet clause makes the base something the evidence does not settle |
| [variable annuity (변액연금보험)](products/variable_annuity/index.md) | `VA_KR_S` | monthly | 변액연금보험 (*byeonaek yeongeum boheom*), a 특별계정 contract [REG-R6] [REG-R15], and the only model here that has to state a **two-account identity**: `net_cf = net_cf_gen + net_cf_sep`, every internal transfer appearing twice with opposite signs and cancelling. Ten charge lines come off **five bases at three times into two accounts**, and the GMAB charge is 0.30% of *past and future* premium for at most seven years — ₩9,000 a month against ₩57.08 of the asset-based component, a factor of 158, stopping three years before the premiums do. Both guarantees are **written options** and one deterministic path values them at intrinsic only, so `run.py` prints charge collected against cost incurred and labels the gap a single-path residual rather than a profit |
| [immediate annuity (즉시연금)](products/immediate_annuity/index.md) | `Immediate_KR_S` | monthly | 즉시연금 (*jeuksi yeongeum*), the payout phase standing alone: no premium term, no acquisition strain — the charge taken at inception exactly meets the outgo at inception, and `check_premium_split()` asserts it — and `pols_if` redefined as the probability that a **payment obligation remains**, which inside the 보증지급기간 is `max(l(t), 1{t < g})`, a max and not a sum; the additive reading gives an annuity 30.3% too low. Three shapes and only 종신연금형 reads the table at all. The 상속연금형's interest retention is a **switch, because the law could not decide either**: 금융분쟁조정위원회 held in 2017 that it could not be asserted against the policyholder and the 대법원 restored it in 2025, and two shipped model points are the same contract on the two bases |

(krlib-one-shape)=

### One shape, enforced

Every model has the same two Spaces — `Data` reads the input CSVs once per model, and
`Projection` is parameterized by `point_id` — with inputs as **external** CSVs beside `run.py`,
so the model folder holds formulas and nothing else. `Projection`'s docstring carries the
mapping from the technical notes' actuarial symbols to the cells names, and `Data`'s names the
`annuallife/TradLife_A` layout it follows.

That shape is asserted rather than merely described: `tests/test_model_conventions_kr.py`
applies it to every model in the registry, and each model additionally has its own test module
for its worked example and its product-specific invariants — the notes' "Known modeling
pitfalls" sections are written up there as tests.

The pairing of model name to folder is deliberately *not* derivable from the folder name —
`indemnity_medical` spelled out is unusable in a model name — so it is registered once in
`tests/kr_registry.py`, and the conventions suite asserts that the registry, the directory on
disk and the model's own `_name` all agree, along with the country and grid tags. The registry
also carries `INPUT_FILES`, the exact set of CSVs a full sweep of each model's shipped model
point table reads, so that "each file is read once per model" is a statement about *which*
files rather than about whatever happened to be read.

The registry is per library; the contract it enforces is the one [uslib is held
to](#uslib-one-shape), and cells names come from lifelib — `basiclife/BasicTerm_S` first, then
`savings/CashValue_SE` — so a name means the same thing here, in uslib, in uklib, in jplib, in
frlib, in delib and in lifelib. The [shared vocabulary table](#uslib-shared-vocabulary) is the
settled ruling across the libraries, and krlib takes the repository-wide time index with it.
**The time index `t` is 0-based**: `t = 0` is the first period of a policy projected from
issue — the issue **month** in every model here — period `t` runs from time `t` to time
`t + 1`, and the attained age is `age_at_entry + duration(t)` with `duration(t) = t // 12`,
which is exact on 보험나이 because it increments on the 계약해당일. **`proj_len()` is the
number of periods from `t = 0`**, i.e. the exclusive end of the frame: `result_cf()` covers
`t = t_first, ..., proj_len() - 1`, where `t_first` is 0 for a point projected from issue and
the elapsed periods for an in-force point. This is lifelib's own convention
(`basiclife/BasicTerm_S`, `savings/CashValue_SE`: `for t in range(proj_len())`). A
contractual policy year is the 1-based label `duration(t) + 1` and is derived, never indexed
by; where a model publishes the horizon in years as well, `proj_len()` is `12 * proj_years()`.

The registry lives in `tests/kr_registry.py` rather than in `conftest.py` for a reason worth
knowing: `conftest` is a name pytest fixes, so six in-library suites collected in one run put
six files of that name on `sys.path`, one wins `sys.modules`, and a suite silently locates
another library's models — a green run against the wrong thing.

(krlib-own-rulings)=

### The two rulings this library added

krlib inherits delib's two — `check_net_cf()` is required of every model, and every assumption
CSV carries a `provenance` column — and adds two of its own, both enforced by the conventions
suite.

**A provenance cell must carry a tag, not merely text.** delib's ruling asks that the column
exist and be populated; it does not ask what is in it, so `interpolated` or `see notes`
satisfies it while saying nothing a reader can follow. Here every cell in a `provenance` column
must name its authority in the library's own citation vocabulary — a bare `[std]`, or an
`[S#]`, `[R#]` or `[REG-R#]` tag resolving against that product's `sources.md`. This is the
escalation the Korean data forced. When **every** row of a decrement file is a standardization
— which, for mortality, is the position throughout this library — "the column is populated"
stops being a meaningful check and "the row says which authority it stands on" starts being
one.

**The age basis is declared in the registry and named in the model.** Korea runs two age
conventions and this library uses both, because its sources do. `kr_registry.MODELS` records
which one each model is on and the suite requires the `Projection` docstring to say the same,
so the two cannot be confused silently. What that is protecting against is set out below.

The conventions suite was also checked against a library it does not govern: before any krlib
model existed it was run over `Term_JP_S` and `WholeLife_JP_S` through a throwaway registry,
and the only failures were the intended differences — the `_KR_` country tag, the mandatory
`check_net_cf`, the provenance-tag escalation and the age-basis requirement. A krlib model that
satisfies it is therefore conforming rather than merely self-consistent.

(krlib-kr-specific)=

### What is Korea-specific about these models

Six things recur across the set and are worth knowing before reading any one of them.

**경험생명표 cannot be read at all, and that is a stronger statement than any sister library
has to make.** The industry experience table (*gyeongheom saengmyeongpyo*, currently the
제10회, applied to new business from 2024-04) is prepared by 보험개발원 and goes to member
insurers; what reaches the public is **평균수명 and 기대여명 and nothing else**, and even those
reached this library through a trade newspaper [REG-R33] [REG-R34]. jplib's 生保標準生命表 is a
free public PDF with `qx` by single year of age and only its *redistribution* is restricted;
uklib's CMI tables need a subscription but exist as a purchasable object; delib cites the DAV
tables by name and cannot ship them. Korea offers no third option: there is no published Korean
insured rate to anchor a proxy on. So **every `mort_table.csv` in krlib is a [std]
construction**, built on carrier-disclosed 예정 경험사망률 where a 상품요약서 prints one and on
the public 국가데이터처 완전생명표 otherwise [REG-R38], with a `provenance` cell on every row
saying which. The models make the construction checkable rather than asking to be trusted. Five
of the ten fit their tables so that the **published 65세 기대여명 of 23.7 years (male) and 27.1
(female) is reproduced exactly** — `WholeLife_KR_S`, `Term_KR_S`, `LTC_KR_S`, `VA_KR_S` and
`Immediate_KR_S` — and they ship the whole age range rather than stopping where the model
points stop, so the claim can be recomputed from the CSV instead of taken on trust. The
external check each then reports is the **selection gap**: the shipped tables sit about 4.2
years (male) and 3.4 (female) above the public 완전생명표's own 65세 기대여명 of 19.5 and 23.7
[REG-R38], which is the insured-versus-population margin any Korean insured table must show,
and a constructed table that does not show it is not an insured-lives table. **No row of any of
these files is a 경험생명표 value**, and no document in this library may present one as such.

**But the morbidity side is different, and this is the correction that matters most.** The
first draft of the reference library generalised the mortality finding to "every morbidity,
incidence and disability rate in krlib is [std]". That is wrong. 보험개발원 is the statutory
보험요율 산출기관 of 보험업법 제176조, and while the **life-side** 참조순보험요율 are filed
with the FSC and never published — a carrier's 상품요약서 prints only the notification's
document number, and the rate reaches the public only as the ratio called the 보험가격지수
[REG-R4] [REG-R22] — the bureau **does** publish a dated numeric **장기손해보험
참조순보험요율** display, in force from 2024-04-01 [REG-R61]. It carries, by age and sex, a
「기타피부암 및 갑상선암 이외의 암 발생률」 grid and a 질병입원율 grid. So `Cancer_KR_S`'s
incidence basis is **sourced rather than standardized**, and it is the only morbidity basis in
the library that is. The definition it is stated on is the *insured* one — invasive cancer
excluding **C44** (기타피부암) and **C73** (갑상선암), which is exactly the 유사암 carve-out
the 약관 draw — so the grid and the reduced tier fit together rather than needing
reconciliation, and the 유사암 limb can be additive to the published rate instead of a slice of
it. Two boundaries keep the claim honest. It is a **net premium rate with a safety loading
inside it**, not a best estimate: 감독규정 제1-2조 keeps a 참조순보험요율 and a 최적기초율
apart, so the step from one to the other is still a **[std]** adjustment, and `Cancer_KR_S`
holds `inc_be_factor` at the identity rather than resting the model on a loading no retrieved
document sizes. And the display does not reach everything: **실손 위험률 is not among the
published categories and neither is any long-term-care inception rate**, so `Medical_KR_S`'s
utilisation basis and `LTC_KR_S`'s whole morbidity construction stay [std], built from public
epidemiology [REG-R41] [REG-R42]. `Medical_KR_S` uses the 질병입원율 grid for the age **slope**
of its admission rate and deliberately not for the level, and says so.

**제3보험 is a statutory category rather than a market segment, and four of the ten models sit
in it.** 보험업법 제4조제1항제3호 names 상해보험, 질병보험 and 간병보험 as a licence class in
their own right, and 제4조제3항 deems both a fully licensed life insurer and a fully licensed
non-life insurer to hold it, which is why the same 암보험 and the same 간병보험 are written on
both sides of the market [REG-R1]. It is Korea's structural analogue of Japan's 第三分野 and
has no US, UK, French or German parallel. Being a statutory class, it carries statutory design
rules that reach into the models: 감독규정 제7-63조제1항제1호 requires a 제3보험 contract to
pay the **계약자적립액 plus the 미경과보험료** on a death from a cause it does not cover
[REG-R17], which the 표준약관 제22조 implements [REG-R25] and 상법 제736조 floors [REG-R50] —
so `Cancer_KR_S`, `LTC_KR_S`, `Child_KR_S` and `Medical_KR_S` all carry a `claims_death` column
that is **not a death benefit**, and on a one-year 순수보장성 실손 contract it is nil because
the account is. The surrender-value rules reach the category by the *mutatis mutandis*
cross-references of 감독규정 제7-69조 and 제7-70조 [REG-R19]. And one of the four is unlike
anything else in the repository: `Medical_KR_S` is an indemnity contract whose defining
constraint, `check_indemnity()`, is that the claim never exceeds the incurred covered loss — an
identity no other model in any of the six libraries has to assert.

**Two age conventions run at once, and the registry records which one each model is on because
nothing raises when it is wrong.** **보험나이** (*boheom nai*, insurance age) is the
contractual age: months are rounded by the six-month rule, so a life 40 years and 7 months old
is 41, and it increments on the 계약해당일 rather than on the birthday [REG-R25]. It is what
every rate basis is graduated on, what a carrier's rate card is indexed by, and what the
경험생명표 itself is built on. **만나이** (*man nai*, age last birthday) is what the public
statistical series are published on — 완전생명표 [REG-R38], 국가암등록통계 [REG-R40], the
노인장기요양보험 통계연보 [REG-R42] — and those series are the only citable basis for the
models whose decrements are morbidity rather than mortality. So seven models here are 보험나이
models and three — `Medical_KR_S`, `Cancer_KR_S` and `LTC_KR_S` — are 만나이 models, and
`Child_KR_S` prints both ages in adjacent columns of `result_pols()` because the offset between
them is a modelled quantity on a contract written in utero. The difference is **half a year of
ageing on every row** and no exception is raised when a model point on one basis is read
against a table on the other: reading `Term_KR_S`'s anchor cell one year of ageing early cuts
total death claims from ₩2,071,060.31 to ₩1,903,445.06, an **8.1% understatement that flatters
`net_cf` by more than the whole answer**. That is why the basis is registry metadata asserted
against the `Projection` docstring rather than a remark in the notes, and why `Cancer_KR_S`
records that half a year is worth about 3.5% of the rate on the steep part of its own incidence
curve.

**IFRS 17 and K-ICS have both been live since 2023-01-01, with a Korea-specific
해약환급금준비금 on top — three measurement bases, one set of gross cash flows, and the models
deliberately stopping before all three.** K-IFRS 제1117호 is the Korean adoption of IFRS 17
[REG-R60] and K-ICS (신지급여력제도) the economic-value solvency regime [REG-R13]; they
commenced in the same quarter under the same 부칙. Japan's economic-value regime commences 2026
and the EU's long predates IFRS 17; Korea switched liability measurement and capital
measurement together and is four years into living with the result. On top of them sits the
**해약환급금준비금** (*haeyak-hwangeupgeum-junbigeum*, surrender value reserve), which has no
counterpart in uslib, uklib, jplib, frlib or delib: at each balance-sheet date the insurer
compares, **company-wide**, the IFRS 17 잔여보장요소 against the aggregate contractual
해약환급금 computed on 감독규정 제7-66조제1항 — on that rule even for the products that may
contractually pay less — and appropriates the shortfall inside 이익잉여금 [REG-R11]. It is
neither an accounting liability nor a capital requirement but a **brake on dividends**, and it
stood at ₩32.2조 at end-2023 [REG-R36]. The three bases share one set of premiums, claims,
expenses, surrenders and policy-loan flows and differ in the discounting, the margin, the
aggregation level and the purpose, which is exactly why the models publish `result_cf()` as a
gross best-estimate stream and compute none of the three. What they *do* compute beyond the
cash flows is the **계약자적립액 and the 해약환급금**, because both are contractual quantities
with a published bound [REG-R19] [REG-R20] — and because `CI_KR_S`, for one, publishes its
unsuppressed 표준형 twin value specifically so that the third basis above has the quantity it
measures against.

**Two Korean product forms are model structure rather than parameters, and each changes what a
model must contain.** The first is **무·저해지환급형** (*mu-jeohaeji hwangeuphyeong*), the
no-surrender-value and low-surrender-value designs that took the market: the 무·저해지 share of
보장성 초회보험료 ran 11.4% in 2018, 30.4% in 2021, 47.0% in 2023 and **63.8% in 2024 H1**
[REG-R27], so a Korea library modelling only 표준형 products would be modelling a minority of
the market. The surrender value is nil, or a stated fraction, throughout the premium-paying
period and steps up at 납입완료 — a cliff and not a curve, permitted by 감독규정 제7-66조제4항
only where the product was priced on a **최적해지율** [REG-R19] [REG-R28] — and the value that
is multiplied is a comparison twin's, so the model runs one account and never two. What the
models actually found is worth stating, because it is the opposite of the intuition: **on the
FSS 원칙모형 lapse basis the cliff moves almost no cash.** The November 2024 계리가정 ruling
makes a log-linear decay the 원칙모형 for 무·저해지 business, converging to **0.1% at
납입완료** with an **0.8% post-완납 ultimate** [REG-R27] — so the prescribed basis puts the
lapse rate at its minimum in exactly the year the payable value doubles. On `WholeLife_KR_S`'s
anchor cell that is ₩30,608.06 of surrender benefit in the cliff year against ₩905,221.12 on a
level 4% comparison, with the outgo arriving the year *after* the step, when the rate returns
to 0.8% against a value that has doubled. Every protection model here therefore ships the
표준형 comparison basis beside the 원칙모형 one — which is the comparison the guideline itself
obliges an insurer to disclose, not an afterthought. The second form is **갱신형**
(*gaengsinhyeong*), renewal: most Korean health cover renews automatically at attained-age
rates, and the renewal is repriced across the **whole 기초율**, issued on a new product code,
and extinguishes a premium waiver already running — yet it is guaranteed-issue, with no 고지
and no underwriting, so the repricing cannot reflect the particular policyholder's risk.
Nothing retrieved settles where the IFRS 17 contract boundary falls [REG-R60], and the Korean
facts pull both ways, so `Term_KR_S` **publishes both readings as model points rather than
ruling**: +₩2,976,124.30 of undiscounted net cash flow projecting to the 보험나이 80 ceiling
against −₩179,423.24 for a single cycle. They differ in sign, which is the reason neither is
quietly chosen; and the two are not the same projection truncated, because shortening the
horizon also compresses the 적용해지율 decay, so the model prints the reason rather than hiding
it.

### Chassis relationships

Products that share machinery point at the file where it is specified rather than silently
restating it, and each pointer states what it inherits and where it deviates:

- **`WholeLife_KR_S` is the savings-and-protection chassis.** The [whole life technical notes
  (종신보험)](products/whole_life/technical-notes.md) are the primary home of the 계약자적립액
  recursion, the 해약환급금 identity and its 별표 14 cap, the 무해지/저해지 suppression and its
  cliff, the 보험계약대출 and the 납입면제 with premiums deemed paid. `CI_KR_S` inherits all of
  it and adds the acceleration — with the consequence that its suppression acquires a *second*
  exit at the CI event, which the chassis's deterministic cliff does not have. `Pension_KR_S`
  inherits the **accumulation half** and replaces the crediting: a declared 공시이율 over a
  stepping guarantee where the chassis carries a fixed 예정이율, and no survivorship release in
  either. The two mortality tables are **not** interchangeable — one is loaded for death and
  the other for survival, and using either for both is wrong in a known direction.
- **`Term_KR_S` is the protection chassis** — the decrement and premium recursion, the
  비갱신형/갱신형 split, the renewal index and the renewal-decline decrement. It deliberately
  does **not** compute a surrender value: the representative 전기납 무해지 form pays nothing at
  any duration, and the shortened-pay value that would arise after 납입완료 is the savings
  chassis's quantity, so projecting it here would duplicate `WholeLife_KR_S` in the one product
  that exists to demonstrate the decrement recursion without it. `Medical_KR_S` borrows exactly
  one name from it, `renewal_decline_rate`, for the same event on a one-year cycle instead of a
  ten-year one.
- **`Cancer_KR_S` is the fixed-benefit (정액) 제3보험 chassis** — the 진단급여금 on diagnosis,
  the 90-day 면책기간, the 감액기간, the 최초 1회한 ledgers, the 유사암 reduced tier and the
  계약자적립액 paid on a non-covered death. `LTC_KR_S` and `Child_KR_S` state their deltas
  against the [cancer technical notes (암보험)](products/cancer/technical-notes.md) rather than
  restating the diagnosis machinery: `LTC_KR_S` replaces a pathological event that has a date
  with an **administrative determination of a state** the insured then lives in, and gets a
  compartment chain and a survival-tested annuity ledger in place of a severity ladder;
  `Child_KR_S` keeps the ledgers and adds 태아가입 and a waiver on the 계약자. Neither inherits
  in modelx — `Projection._bases` is empty everywhere in this library — so the relationship is
  documentary and each delta is written down.
- **`Medical_KR_S` stands alone.** It inherits nothing and nothing states a delta against it,
  because it is the only contract here whose benefit is a reimbursement of an incurred cost.
  Its own `model.md` says in terms that the cancer chassis's machinery must not be reused there
  and the cancer model says the reverse: there is no 급여/비급여 split, no 자기부담금, no
  annual limit and no 재가입 in a 정액 product, and no benefit in this one reimburses a cost.
  The single shared mechanic is the 제3보험 requirement to pay the 계약자적립액 on a
  non-covered death [REG-R17].
- **`Immediate_KR_S` is `Pension_KR_S`'s payout phase as a product in its own right** — which
  is why an immediate-annuity document is direct evidence for a deferred contract's conversion
  basis — and the two are deliberately not one model: the deferred contract needs the
  annuitant-table-vintage ratchet and the immediate one cannot, there being no interval between
  issue and annuitisation for a table revision to land in. `VA_KR_S` shares the annuitisation
  step and nothing else, its accumulation being a 특별계정 unit ledger with no 예정이율 at all.
- **Across markets.** `Pension_KR_S`'s nearest relative is jplib's
  [個人年金保険](../jplib/products/individual_annuity/index.md), and the difference is
  structural rather than parametric: a Japanese 保険料積立金 divides by `(1 − q')` and releases
  the premiums of those who die to the survivors, while the Korean 계약자적립액 does none of
  that. `Term_KR_S` and jplib's [定期保険](../jplib/products/term_life/index.md) share the
  renewing-term problem and differ in two ways worth carrying: Korea has **no analogue of the
  高度障害保険金**, so there is no competing benefit on one sum assured, and the model points
  and the table are on one age basis, so no age-basis shift is applied anywhere.
  `WholeLife_KR_S` states the same kind of absence: **no 자동대출납입 was found in any Korean
  document read for this library**, so lapse here is a plain behavioural decrement where
  jplib's whole life chassis makes it a *funded* event — and that absence is tagged
  [unverified] rather than asserted, because it is the single highest-value item for a later
  research pass. `Immediate_KR_S` and frlib's [rente
  viagère](../frlib/products/rente_viagere/index.md) take opposite postures on improvement: the
  French tables are generational and an improvement factor would double-count, the Korean table
  is a period construction on undated anchors and **must not acquire one**.

## How to use the library

Create your own copy of the *krlib* library, as described in the {ref}`create-a-project`
section. For example, to copy it to *C:\\path\\to\\your\\krlib*:

```python
>>> import lifelib

>>> lifelib.create("krlib", r"C:\path\to\your\krlib")
```

Each model reads from its own directory, so run one directly:

```bash
python products/term_life/run.py
```

or read it and take the cash flow statement:

```python
>>> import modelx as mx

>>> model = mx.read_model("products/term_life/Term_KR_S")

>>> model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is each model's worked-example anchor cell,
and wherever the product admits it that cell is the **기준연령 요건** — 전기납, 월납, 남자 만
40세 — which 감독규정 제1-2조제2호 makes the single reference cell at which Korean comparison
disclosure is computed [REG-R9]. `result_cf()` returns a tidy `DataFrame` indexed by `t` with
one column per cash flow line. Several models publish companion frames beside it where a cash
flow statement alone hides the mechanic — `result_val()`, `result_pols()`, `result_charges()`,
`result_prem()`, `result_tax()` — and each `model.md` says which and why.

Everything the `run.py` scripts print is **pure ASCII**, so the output survives a Windows
console under any code page: Korean is romanized in Revised Romanization and amounts are
labelled `KRW`.

The tests ship inside the library and run against *your* copy:

```bash
python -m pytest tests -q
```

## Library contents

```{list-table}
:header-rows: 1
:widths: 28 72

* - File or folder
  - Description
* - `products/<product>/`
  - One directory per product, holding its documents *and* its model together. Ten of them.
* - `products/<product>/product-spec.md`
  - The representative product specification: mechanics, parameters, variation across insurers.
* - `products/<product>/technical-notes.md`
  - The liability cash flow model on paper: state variables, recursions, processing order, worked example.
* - `products/<product>/model.md`
  - How the model implements those notes — what was standardized, what diverges, what the tests cover.
* - `products/<product>/sources.md`
  - Every source the product's documents cite, with URLs, access dates and retrieval status.
* - `products/<product>/<Model>/`
  - The modelx model itself. Formulas only — no embedded data.
* - `products/<product>/*.csv`
  - The model's inputs, external to the model folder so they can be edited or swapped in place. Every assumption file carries a `provenance` column whose every cell names an authority.
* - `products/<product>/run.py`
  - Reads the model and prints its cash flow statement. Pure ASCII output.
* - `references/`
  - The cross-product regulatory and actuarial bibliography, cited as `[REG-R#]`.
* - `tests/`
  - One module per model for its worked example and invariants, plus `test_model_conventions_kr.py` for the house style, and `kr_registry.py` carrying the model registry and the input-file map.
* - `_research/`
  - The raw research notes every citation traces back to. Provenance, not documentation — shipped but not rendered.
```

`_research/` carries one file per product plus `regulatory-actuarial.md`, and records which
documents were actually retrieved and which fetches failed. Its source lists are **never
renumbered**: the product documents cite against them.

(krlib-citation-conventions)=

## Citation conventions

Whether a citation tag is a link tells you what kind of source it is. `[R1]` and `[REG-R61]`
are links: the first lands on entry R1 in **that product's** `sources.md`, the second on entry
R61 of the shared [reference library](references/regulatory-and-actuarial-references.md).
`[S6]` is not a link. It stays on the page as you see it, brackets and all, and names entry S6
in that product's `sources.md` for you to look up.

That asymmetry is deliberate, and it is the same line the `sources.md` files draw between their
own sections. A regulatory or actuarial reference is an **authority** the model is held to, and
following it is part of reading the document. A primary product source is a **specification**
citation — the 약관, 상품요약서, 보험안내자료 or 공시자료 a number was taken from — which says
where a figure came from rather than what the model must obey. So one reads as a tag on the
page and the other as a link off it.

Numbering is per product — S1 is a different source in each — so tags resolve against the
document's own product rather than one global list.

| Tag | On the page | Meaning |
|---|---|---|
| `[S#]` | bracketed text | Fact taken from a primary product document (약관, 상품요약서, 보험안내자료, 사업방법서 extract, 공시자료) listed in the product's `sources.md` |
| `[R#]` | link | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | link | Fact taken from the cross-product reference library (frozen R-numbering) |

(krlib-std)=

**[std]** — a *standardization introduced for the reference implementation*: a parameter or
convention chosen where sources vary, are proprietary, or are silent. Each carries a rationale
and, where available, the observed range across insurers.

(krlib-unverified)=

**[unverified]** — a claim from general knowledge or a secondary snippet that could **not** be
confirmed against a retrieved document. Treat it as a to-verify item, not an established fact.

The hard rule throughout: **every quantitative parameter is either source-tagged or marked
[std]**. In this library that rule does most of its work on the decrement bases and on the
pricing and expense basis, because the 산출방법서 that holds a Korean product's 예정이율,
적용위험률 and 예정사업비율 is a 기초서류 filed with the FSC and never published [REG-R2], and
because the industry mortality table cannot be read at all — see [What is
Korea-specific](#krlib-kr-specific).

## Regulatory and actuarial reference library

The [reference library](references/regulatory-and-actuarial-references.md) is the curated
cross-product bibliography — frozen numbering **R1–R62**, cited as `[REG-R#]` — with a
product-relevance matrix running every entry against the ten products in three states. It spans
the prudential and supervisory frame, which in Korea is a five-rung ladder (법률 → 시행령 →
시행규칙 → the FSC's **보험업감독규정** → the FSS's **보험업감독업무시행세칙** → 별표) in which
nearly every operative number lives on the last two rungs and not in the statute: 보험업법 with
its 제3보험 licence class, its 기초서류 filing regime and its 참조순보험요율 bureau; the
감독규정's 책임준비금, 보증준비금, **해약환급금준비금** and K-ICS articles; the product-design
rules for 생명보험 and for 제3보험; the 해약환급금 articles and the two schedules that bound
them, **별표 14**'s 표준해약공제액 formula and **별표 15**'s 보험가입금액 construction; the
시행세칙's 표준약관 and its 공시기준이율 schedule; and the FSC and FSS releases that carry the
2024 계리가정 ruling, the 무·저해지 product-structure reform, the 2019 사업비·모집수수료 reform
and the 실손 generations. It then covers the actuarial layer (보험개발원 as statutory rate
bureau, the 경험생명표's public summary statistics, and the published 장기손해보험
참조순보험요율 display); the public statistical series the morbidity bases are built on
(국가데이터처 생명표 and KOSIS, 국가암등록통계, the 건강보험 진료비 실태조사, the 장기요양
등급판정 and 통계연보 series, the FSS 실손 사업실적, and both trade-association disclosure
portals); contract law and conduct (상법 제4편 with its 인보험 chapter, 금융소비자보호법's
청약철회 and 예금자보호법); the public schemes these private products sit on top of
(국민건강보험법 and 노인장기요양보험법 with its 등급판정기준); and tax and accounting
(소득세법's 세액공제 for 연금저축 and for 보장성보험료, the 보험차익 rules, 상속세및증여세법,
and K-IFRS 제1117호 with the three measurement bases one projection feeds).

Two entries were added by the reference library's own adversarial pass and both are corrections
rather than additions: **R61**, the 보험개발원 참조순보험요율 display, which overturns a stated
finding that no Korean reference rate is public; and **R62**, the 손해보험협회 공시실, through
which four products reached primary product documents that must not be attributed to the
생명보험협회 portal. Read the page's own §7 first: it discloses every failed fetch, every
formula that was located and could not be extracted because the regulation renders it as an
image, and every claim left [unverified], and it records the two corrections above as findings
rather than quietly applying them.

## Known gaps and caveats

Aggregated from the per-product research; each product's documents carry the full list.

- **The 경험생명표 qx table is the single largest gap in the library.** No mortality rate from
  any edition of the industry table was located in any public KIDI channel — the 보도자료
  listing serves no 경험생명표 item and the 빅데이터 플랫폼 refused connection — so only
  평균수명 and 65세 기대여명 are public, and only through a trade newspaper [REG-R33]
  [REG-R34]. Every `mort_table.csv` here is consequently a **[std]** construction. A related
  item is a live task rather than a closed gap: the **KOSIS single-year 완전생명표 `qx` tables
  were never downloaded** [REG-R39], and the table builds use the published summary statistics
  [REG-R38] instead.
- **The 예정이율 of any specific Korean product is the most consequential unresolved number.**
  A full-text search of the retrieved 감독규정 returns **zero** occurrences of 예정이율
  [REG-R9] — the regulation names only the 계약자적립액 적용이율 and the 금리연동형/금리확정형
  split — and the rate itself lives in the unpublished 산출방법서 [REG-R2]. So every 예정이율
  in this library is **[std]**, anchored on the published 평균공시이율 series, which is
  verified at **2.50% for 2026** [REG-R48]. Trade reporting placing 보장성 공시이율 at 2.2%,
  연금 at 2.29% and 저축 at 2.22% before that cut was seen only as a search summary and is
  **[unverified]**.
- **No Korean carrier publishes an expense rate, a commission scale or a lapse curve by
  duration.** Both 상품요약서 in the corpus define 계약체결비용 and 계약관리비용 and then give
  no number. What is public is a **cap**, and it has no US or UK analogue at this level of
  prescription: 별표 14's 표준해약공제액 formula [REG-R20], the seven-year 해약공제기간 of
  제7-66조제1항제2호 [REG-R19], the 1.4× 계약체결비용 tolerance and the first-year commission
  ceiling of 제4-32조 [REG-R22], and the FSC's own rule of thumb that the cap is about thirteen
  months' premium for a 보장성보험 [REG-R29]. Four models compute the cap from the schedule and
  sit their acquisition cost inside it, which demonstrates the binding constraint instead of
  inventing an interior point — and two of them record that 별표 15's construction of a
  notional 보험가입금액 for a product with no death benefit is either awkward or, for a
  care-only contract, unusable, because 제9호 excludes long-term-care risk premium from the
  very ratio it needs [REG-R21].
- **The 계리가정 guideline itself was never read.** The 2024-11-07 보도자료 was retrieved in
  full and its numbers are verified from it — the log-linear 원칙모형, the **0.1%** convergence
  at 납입완료, the **0.8%** post-완납 ultimate, the ≥ 30% additional lapse at a bonus date, the
  63.8% 무·저해지 share — but the 「IFRS17 주요 계리가정 가이드라인」 attachment is HWP and was
  never converted, so **the model's functional form and the definition of the 실무상 수렴점 are
  [unverified] at instrument level** [REG-R27]. Every product that leans on the shape rather
  than on the values tags it.
- **보험업감독업무시행세칙 별표 22 and 별표 24 were not retrieved**, and 별표 22's `bylSeq` was
  recovered from the index while the fetch was simply never made — a live task, not a closed
  gap. So the **K-ICS 대량해지위험 shocks, including the 고환급형 test, and the 보증준비금
  CTE(70) basis are second-hand through [REG-R36] and carry [unverified]** [REG-R26]. That
  matters most to `WholeLife_KR_S` and `Term_KR_S`, whose 무·저해지 forms are what the 고환급형
  test is about, and to `VA_KR_S`, which publishes neither a CTE nor a standard-factor
  보증준비금 and says so.
- **Several regulations render their formulas as images, and none is reproduced anywhere in
  this library.** The 해약환급금 display and the two 계약자적립액 accrual formulas of
  제7-66조제1항 [REG-R19], the α and β weight formulas of 시행세칙 별표 27 [REG-R24], the
  기본요구자본 correlation formula [REG-R13], and the 연금수령한도 and 연금소득 원천징수
  formulas of the 소득세법 시행령 [REG-R56] were each located and could not be extracted. Where
  a model needed one it carries a stated **[std]** approximation of the operative words
  instead.
- **No 한국보험계리사회 document of any kind was retrieved.** There is no krlib counterpart to
  jplib's 保険計理人の実務基準 or frlib's NPA standards, and none is claimed. Where a document
  here describes a Korean actuarial convention that is not in a retrieved regulation — the
  위험률차/이자율차/사업비차 framing is the clearest case, and it has been **deleted from the
  감독규정** — it says "market practice" and tags the claim.
- **The market figures are news-sourced.** The 2025 industry outturn — 수입보험료 ₩266.6595조,
  당기순이익 ₩12.2172조 and the life and non-life line splits — comes from a trade newspaper
  reporting an FSS release that the research pass could not open [REG-R47], as do the 제10회
  경험생명표 summary statistics [REG-R33]. Two FSS releases reached the library only through
  the KDI mirror [REG-R44] [REG-R30]. A correction is recorded rather than smoothed over:
  **`fss.or.kr` is not unreachable** — a later pass fetched a release and a 15-page PDF
  directly from it — so the discriminator is the fetcher and the path, not the host, and those
  news-sourced figures are replaceable with a primary release rather than being the best
  available evidence [REG-R31].
- **Every behavioural rate in the library is unsourced, and the products say so individually.**
  No Korean reinstatement rate, acceleration take-up, 50%-plus 장해 incidence, renewal-decline
  series or 변액연금 적용해지율 was retrieved for any carrier, and the disclosures that exist
  give the *price* path and not the *persistency* path. Where a rate was needed the models
  label it a **placeholder** rather than an estimate and switch the module it drives **off in
  the base run**, so the worked examples are independent of all of them; `Term_KR_S` names
  three such placeholders in terms and distinguishes them from `renewal_decline_base`, which is
  argued rather than chosen and is live on the points the renewal machinery exists for.
- **Three specific quantitative gaps are large enough to name.** `LTC_KR_S` has neither a
  published 장기요양 inception table nor a post-onset mortality table to work from, so its
  whole morbidity basis is a prevalence-to-incidence conversion of the public 인정률 series,
  and the one disclosed 예정위험률 it can compare against runs about **4.2 times** the model's
  own best estimate at the same ages — a level difference the model publishes as a ratio rather
  than closing with an invented factor. `VA_KR_S` retrieved **no volatility, no correlation and
  no return series** of any kind, so its two written options are valued at intrinsic on one
  path and the residual between charge and cost is labelled a single-path residual, not a
  profit. And `Medical_KR_S`'s utilisation level is solved against a *published 2022 loss
  ratio*, so it reproduces that result exactly and carries none of the deterioration that
  followed — the model re-rates from year 2 and the real book, under the five-year grace on
  rate-adequacy verification, could not.
- **[unverified] items remain wherever a claim could not be corroborated by a retrieved
  document**, and each sits at the point of use rather than in a list: the absence of a Korean
  自動振替貸付 analogue on the whole life chassis; whether the 감액완납 and 연장정기보험
  options a jplib reader will reach for exist in a Korean 약관 at all; the size of the safety
  loading inside a 참조순보험요율; the operative text of 소득세법 시행령 제187조의2, on which
  the 3.3% 종신계약 withholding rate depends; and the 지방세법 grossing-up behind the 13.2% and
  16.5% 연금저축 tax credit rates, which is arithmetic on a verified base.

```{toctree}
:hidden:
:maxdepth: 1
:caption: Products

products/whole_life/index
products/term_life/index
products/ci_insurance/index
products/indemnity_medical/index
products/cancer/index
products/long_term_care/index
products/child/index
products/pension_savings/index
products/variable_annuity/index
products/immediate_annuity/index
```

```{toctree}
:hidden:
:maxdepth: 1
:titlesonly:
:caption: Reference

references/regulatory-and-actuarial-references
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[REG-R1]: #krlib-reg-r1
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R15]: #krlib-reg-r15
[REG-R17]: #krlib-reg-r17
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R24]: #krlib-reg-r24
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R30]: #krlib-reg-r30
[REG-R31]: #krlib-reg-r31
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R40]: #krlib-reg-r40
[REG-R41]: #krlib-reg-r41
[REG-R42]: #krlib-reg-r42
[REG-R44]: #krlib-reg-r44
[REG-R47]: #krlib-reg-r47
[REG-R48]: #krlib-reg-r48
[REG-R50]: #krlib-reg-r50
[REG-R54]: #krlib-reg-r54
[REG-R56]: #krlib-reg-r56
[REG-R6]: #krlib-reg-r6
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R62]: #krlib-reg-r62
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
