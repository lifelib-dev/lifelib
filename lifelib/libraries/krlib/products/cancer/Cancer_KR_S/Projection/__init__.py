# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Cancer_KR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace projecting
model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy months**, 0-based: ``t = 0`` is the month beginning at the 보험계약일
and ``t = proj_len() - 1`` the 100세 계약해당일 at which the contract expires. ``proj_len()``
is the **number of projected months**, the frame's exclusive end -- ``12 x (100 - issue_age)
+ 1``, so 721 on the anchor cell and 721 rows in :func:`result_cf`, indexed 0 to 720, and the
frame is ``range(proj_len())``. Nothing is paid at expiry: there is no
만기환급금 on the 순수보장형 form and the only retrieved surrender-value illustration shows
the value returning to nil at maturity [S8].

.. rubric:: The age basis

The contract ages on **보험나이** (*boheom nai*, insurance age): 「계약일 현재 피보험자의
실제 만 나이를 기준으로 6개월 미만의 끝수는 버리고 6개월 이상의 끝수는 1년으로 하여
계산」, incrementing at each 계약해당일 [S3] [REG-R25 제21조]. **This model projects on
만나이** (*man nai*, age last birthday), because every decrement it uses is published on
만나이 -- the 국가암등록통계 age bands [R1], the 보험개발원 참조순보험요율 age grid [R5] and
the 국가데이터처 생명표 [REG-R38] -- and converting a public 만나이 rate to a 보험나이 basis
would need a distribution of issue dates within the policy year that no source supplies.
Because of the six-month rule the two differ for roughly half of all issue dates, so the
model reads its tables for a life on average half a year younger than the contract calls him.
The offset is a **[std] simplification** and it is not negligible on the steep part of the
curve: between 60 and 70 the published male rate roughly doubles [R5], so half a year of age
is worth about 3.5% of the rate. ``age(t)`` is 만나이 and the model point's ``issue_age``
column is 만나이.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/cancer/``, read at run time rather than stored inside the model. The model folder
therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded values -- so a
diff of the model shows logic changes only, and an input can be edited or swapped without
rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's IOSpec
machinery. The consequence worth knowing: **the model is not portable on its own.** Copying
the ``Cancer_KR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.Cancer_KR_S.Data`,
reached here through the ``data`` Reference:

=======================  ====================================  ==========================
Reference                Cells                                 File
=======================  ====================================  ==========================
model_point_file         data.model_point_table()              model_point_table.csv
mort_table_file          data.mort_table()                     mort_table.csv
incidence_table_file     data.incidence_table()                incidence_table.csv
tier_share_file          data.tier_share_table()               tier_share_table.csv
tier_table_file          data.tier_table()                     tier_table.csv
survival_table_file      data.survival_table()                 survival_table.csv
care_table_file          data.care_table()                     care_table.csv
lapse_table_file         data.lapse_table()                    lapse_table.csv
=======================  ====================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an analogue --
``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for annual rates and
``*_rate_mth`` for their monthly counterparts, ``claims(t, kind)`` with an uppercase ``kind``
string. The technical notes use compact symbols instead. The mapping is:

=========================  ====================================  ========================
Notes symbol               Cells                                 Meaning
=========================  ====================================  ========================
(model point row)          model_point()                         The selected model point
t                          (the cells argument)                  Policy month, 0-based
x                          issue_age()                           만나이 at issue
age(t)                     age(t)                                Attained 만나이, x + t//12
y(t)                       policy_year(t)                        Policy year, 1-based
(horizon)                  proj_len()                            Number of projected months
S                          sum_assured()                         보험가입금액
P                          premium_mth_pp()                      Level monthly premium
W                          wait_months()                         면책기간 in months
W_j                        tier_wait_months(tier)                Tier j's own 면책기간
cover(t)                   cover(t)                              1 from t >= W, else 0
cover_z(t)                 cover_similar(t)                      유사암 cover, from t = 0
G                          reduction_months()                    감액기간 in months
g(t)                       reduction_factor(t)                   0.50 inside it, else 1.00
r_j                        benefit_ratio(tier)                   Tier j's share of S
(payment term)             pay_months()                          납입기간 in months
(base rate)                inc_rate(t)                           암 발생률 ex C44, C73
m(a)                       minor_share(t)                        특정소액암 share of it
h(a)                       high_share(t)                         고액암 share of it
z(a)                       similar_share(t)                      유사암 ratio to it
i_g(t)                     inc_rate_gen_mth(t)                   Monthly 일반암 incidence
i_m(t)                     inc_rate_minor_mth(t)                 Monthly 특정소액암
i_h(t)                     inc_rate_high_mth(t)                  Monthly 고액암
i_z(t)                     inc_rate_similar_mth(t)               Monthly 유사암
q(x)                       mort_rate(t)                          Annual base mortality
q_mth(t)                   mort_rate_mth(t)                      Monthly base mortality
mu_k                       excess_hazard(tier, k)                Select excess hazard
q_w(t,k)                   mort_rate_waived_mth(t, k)            Monthly q, 일반암 state
q_n(t,k)                   mort_rate_minor_mth(t, k)             Monthly q, 특정소액암
w(t)                       lapse_rate(t)                         Annual lapse rate
w_mth(t)                   lapse_rate_mth(t)                     Monthly lapse rate
w_c(t)                     lapse_rate_canc_mth(t)                Monthly lapse, waived
s_0(t)                     surv_healthy(t)                       Healthy survival factor
s_w(t,k)                   surv_waived(t, k)                     일반암 survival factor
s_n(t,k)                   surv_minor(t, k)                      특정소액암 survival factor
l(0)                       pols_if_init()                        Exposure at t = 0
l_0(t)                     pols_healthy(t)                       Never invasively diagnosed
D_n(t,k)                   pols_minor_dur(t, k)                  특정소액암 state, cohort k
D_w(t,k)                   pols_waived_dur(t, k)                 일반암 state, cohort k
(exposure)                 pols_minor_exp(t, k)                  D_n plus the month's entry
(exposure)                 pols_waived_exp(t, k)                 D_w plus the month's entry
G_n(t,k), G_w(t,k)         minor_grad(t, k), waived_grad(t, k)   Cohort graduation flows
l_n(t)                     pols_minor(t)                         특정소액암 state, total
l_w(t)                     pols_waived(t)                        일반암 state, total
l_c(t)                     pols_cancer(t)                        Diagnosed, both states
l(t)                       pols_if(t)                            Total in force
(intra-month timing)       pols_if_at(t, timing)                 In force at a named point
d(t)                       pols_death(t)                         Deaths in month t
lap(t)                     pols_lapse(t)                         Lapses in month t
(expiry)                   pols_maturity(t)                      Cover ending, at proj_len()-1
n_g(t)                     diag_gen(t)                           일반암 diagnoses
n_h(t)                     diag_high(t)                          고액암 diagnoses
n_m(t)                     diag_minor(t)                         특정소액암 diagnoses
n_z(t)                     diag_similar(t)                       유사암 diagnoses
Z(t)                       similar_avail(t)                      유사암 tier unused, at start of t
(consumed)                 similar_used(t)                       유사암 tier consumed by start of t
A(k)                       treat_avail(k)                        Treatment benefit unused
P x pols_payer             premiums(t)                           Premium income
(claim lines)              claims(t, kind)                       Benefit outgo by kind
V(t)                       av_pp(t)                              계약자적립액 per policy at start of t
CV_std(t)                  cv_std_pp(t)                          표준형 해약환급금, at start of t
CV(t)                      cv_pp(t)                              해약환급금 as written, at start of t
alpha(t)                   surr_chg_pp(t)                        해약공제액, at start of t
alpha_cap                  surr_chg_cap_pp()                     표준해약공제액
e(t)                       expenses(t)                           Acquisition + maintenance
ec(t)                      claim_expenses(t)                     Claim handling expense
(commission)               commissions(t)                        Commission outgo
net_cf(t)                  net_cf(t)                             Net cash flow, income +
=========================  ====================================  ========================

.. rubric:: Three states, and why two will not do

``Medical_KR_S`` projects a single in-force population and reads a utilisation rate off it.
A cancer model cannot. The premium waiver, the inpatient, surgery and treatment limbs and the
계약자적립액 payable on a later death all depend on **how long the insured lives after
diagnosis**, and the 특정소액암 tier does not stop the premium while the 일반암 tier does. So
the model carries:

:func:`pols_healthy`
    In force and never diagnosed with an invasive cancer. Pays premium, and it is the only
    state a first diagnosis can be made from.

:func:`pols_minor`
    In force, first invasive diagnosis was a 특정소액암 (직.결장암, 유방암 C50,
    여성생식기암, 전립선암 C61). **Still pays premium**, because [S3 제14조제1항] excludes
    특정소액암 from the waiver by name, and can still lapse. Carries its own, much lighter,
    excess hazard: the three named sites' published five-year relative survivals are 75.6,
    94.7 and 96.9 per cent [R1].

:func:`pols_waived`
    In force, has had a 일반암 or 고액암. **Pays nothing and cannot lapse** -- there is no
    premium to miss and no surrender value to take on the 미지급형 form during the 납입기간.

A 특정소액암 life can go on to a 일반암, and that transition is modelled: it is folded into
:func:`surv_minor` as a ``(1 - i_g cover)`` factor and shows up as the second limb of
:func:`diag_gen`. The reverse is not: a 일반암 life's later 특정소액암 is a **[std]
omission**, and so is a second 고액암 after a plain 일반암. Both understate.

The 유사암 tier is emphatically **not** a fourth state. It is a second benefit at a second
rate on its own once-only ledger, it does not move the life anywhere, it does not stop the
premium and it carries **no excess mortality at all** -- 갑상선 five-year relative survival is
100.2% and lifetime 갑상선 mortality risk 0.1% [R1]. Implementing it as a discount on the
main diagnosis benefit gets the amount right and the ledger, the waiver and the waiting period
all wrong.

.. rubric:: Six select-duration cohorts, and why a flat hazard will not do

Relative survival is steeply select: most of the excess mortality of a cancer diagnosis falls
in the first two years, and 62.1% of Korea's prevalent cancer population is more than five
years out from diagnosis [R1]. A flat hazard fitted to the five-year point therefore kills
long survivors far too fast, and long survivors are exactly who the inpatient, surgery and
treatment limbs are paid for.

Each diagnosed state is therefore resolved into **six cohorts by elapsed duration** -- select
years 1 to 5 and an ultimate -- and the excess hazard is read per cohort. The cohorts are
tracked exactly, as a **delay on the entry flow** rather than as a transfer rate:
:func:`waived_grad` and :func:`minor_grad` carry the entrants of month ``t - 13`` forward on
cohort 1's own decrements -- thirteen, not twelve, because the entry month is itself a full
month of cohort-1 exposure -- and each later cohort hands on twelve months after that. The
graduation flows telescope out of the sum, which is what :func:`check_cancer_roll_fwd`
asserts. :func:`check_canc_dur_ledger` rebuilds the first cohort
independently from the entry history, so an off-by-one in the delay shows up there and nowhere
else.

.. rubric:: The waiting period is a hard zero, and there are two of them

:func:`cover` multiplies **every invasive-tier benefit and both invasive transitions**. In
months 0, 1 and 2 the model diagnoses nobody with an invasive cancer, pays nothing for one,
and still collects the premium -- the 유사암 tier and every other cover are already in force
from day 1, and the invalidity rule of 상법 제644조 returns the premium for the affected
cover if a diagnosis does fall inside the window [S1 제28조제2항] [R7].

:func:`cover_similar` is the second start date and it is **1 from t = 0**. Reading one waiting
period off the model point and applying it to both tiers is the commonest way to break this
product, and at young ages it is not a small error: at female 만나이 30 the 유사암 tier's
incidence is larger than the invasive base rate it is a ratio of.

.. rubric:: The 감액기간 is a first-year phenomenon, not a benefit scaling

:func:`reduction_factor` is 0.50 for ``t < reduction_months()`` and 1.00 after, on **every**
diagnosis tier [S1] [S6] [R6]. It must not be modelled as a permanent scaling of the benefit:
on a 비갱신형 contract it bites once, at the start, and on a 갱신계약 it is disapplied
altogether -- 「※ 갱신계약의 경우 감액지급을 적용하지 않습니다」 [S2] [S4]. The observed
designs are 0, 12 and 24 months and ``reduction_months`` is a model point column carrying all
three. One refinement is **not** implemented and the omission is stated: the clock's second
endpoint differs by benefit, running to the 진단확정일 for a diagnosis benefit [S3 별표 1 주2]
but to the 수술일 for a surgery or treatment benefit [S4] [S5], so a cancer diagnosed at month
10 and operated on at month 14 really does draw a reduced diagnosis benefit and a full surgery
benefit -- and so does the model. The reduction multiplies the four diagnosis lines **only**
and never the care limbs, so the model gives the contract's own answer whenever the treatment
date falls outside the 감액기간 -- which includes every case in which the diagnosis itself
does -- and overstates the care limbs of a treatment falling inside it.

.. rubric:: Premiums ride on pols_healthy + pols_minor, claims on the diagnosed

:func:`pols_payer` is where the waiver is applied and it is a **product** choice, not a
refinement: on the composite the waiver fires on the first 일반암 or 고액암, so the premium
is carried by the never-diagnosed and the 특정소액암 sub-population together, and the two
weights are disjoint from the one the care benefits ride on. On the ``waiver_trigger =
"none"`` design -- model point 9 -- the diagnosed keep paying and can lapse, which is why
:func:`lapse_rate_canc_mth` is not simply zero.

.. rubric:: A payment on death, with no death benefit

The composite has no death benefit at all, and it still pays something when the insured dies:
감독규정 제7-63조제1항제1호 requires a 제3보험 product to be designed so that death from a
cause the policy does not cover pays the **계약자적립액** and terminates the contract
[REG-R17], the 표준약관 implements it -- 「회사가 적립한 사망 당시의 계약자적립액」 [REG-R25
제22조] -- and 상법 제736조 is the floor beneath it [REG-R50]. :func:`av_pp` is that account,
a retrospective recursion at the 예정이율 on the allocated premium less the risk premium, and
``claims(t, "DEATH")`` is it multiplied by the month's deaths. ``LTC_KR_S``, ``Child_KR_S``
and ``Medical_KR_S`` inherit the same requirement.

The 해약환급금 is a *different* number and Korean regulation keeps them apart deliberately:
``max(계약자적립액 - 해약공제액, 0)`` [REG-R19], overridden on the **미지급형** form to nil
during the 납입기간 and to 50% of the 표준형 value afterwards [S3 제41조]. :func:`cv_pp` is
what is actually paid and :func:`cv_std_pp` the 표준형 comparator that cannot be bought;
:func:`check_cv_floor` asserts the relation between them.

.. rubric:: Modules that are off in the base run

- **The validity adjustment**, ``void_adjust``. A diagnosis inside the 90-day window makes the
  affected cover **무효**, not merely unpayable [S1 제28조제2항] [R7]: it is a
  de-recognition, not a decrement, so it releases the premium already collected as well as the
  future benefit and belongs in a validity adjustment at outset. :func:`void_prob` is that
  probability and switching ``void_adjust`` on scales :func:`pols_if_init` down by it.
- **The best-estimate adjustment to the incidence basis**, ``inc_be_factor = 1.0``. The
  shipped rate is a **참조순보험요율**, a net premium rate with a safety loading already
  inside it, not a best estimate [REG-R4]. The claim that the loading is about 10% was seen
  only in a search summary and is **[unverified]**, so the factor is left at the identity
  rather than resting the model on an unconfirmed number. What *is* sourced is that the rate
  contains **no trend allowance at all** -- 「현재도 예정위험률 산출 시 미래의 추세를 반영하지
  않고 있음」 [R4] -- while Korea's crude cancer incidence has risen 161% since 1999 [R1].
- **Repricing at renewal**, ``renew_reprice_rate = 0.0``, on the 10년 갱신형 chassis flag.
  Setting the flag already removes the 면책기간, the 감액기간 and the waiver's persistence;
  the base run holds the issue rate flat and records the contract-boundary tension rather than
  resolving it, which is a K-IFRS 1117 question [REG-R60] this model does not answer.
- **The diagnosed lapse loading**, ``lapse_canc_factor = 1.0``. Inert rather than off:
  wherever the waiver fires a diagnosed life has no premium to miss and no surrender value to
  take, so :func:`lapse_rate_canc_mth` returns zero whatever the factor is. It reaches a cash
  flow only on model point 9.

Three constructions the specification names are deliberately **not** implemented and the
absence is stated rather than left to inference. **재진단암** is a rider whose two-year clock
is sourced [S1] but whose rate is not -- no public source gives a cancer re-diagnosis
incidence [R1] [R4] -- so it is specified and switched off. **부활** is not modelled and lapse
is absorbing, which is the conservative direction: a reinstated Korean cancer policy re-runs
the 90 days from the 부활일 [S1] [S3] [S7], so it is not the policy that lapsed.
**요양병원 days** are excluded from the inpatient limb and their separate 90-day rider is not
carried [S2] [S8], which is the market's own structural answer to the most disputed benefit in
Korea [R3].

.. rubric:: Sign convention

:func:`net_cf` is **income positive** -- premiums less every benefit line, less expenses, less
the claim handling expense, less commission -- which is the library-wide sign, so there is no
outgo-positive ``liability_cf`` companion to publish: one stream, one sign, one name.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

# ===== Cells: the model point =====


def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The policy identifier of the selected model point."""
    return str(model_point()["policy_id"])


def sex():
    """The sex (M / F) of the insured.

    A unisex cancer basis is materially wrong at every age and wrong in **opposite
    directions** either side of about 55: at 만나이 40 the published female invasive rate is
    2.52 times the male, and at 80 the male rate is 2.44 times the female [R5]. The registry
    states the crossing point in terms -- 「50대 초반까지는 여자의 암발생률이 더 높다가, 50대
    후반부터 남자의 암발생률이 더 높아지는」 [R1] -- and the published reference rate crosses
    in the same place.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """x: the age at issue on a **만나이** basis, in the composite's 15-65 range.

    The contract's own age is 보험나이 and the two differ for roughly half of all issue dates;
    see the Space docstring for why the model runs on 만나이 and what the offset costs. The
    lower bound matters more than it looks: at 보험나이 15 the 면책기간 carve-out that
    ``Child_KR_S`` inherits switches sign [S2] [R3], and 15 is the age 상법 제732조 uses for
    death cover [REG-R50]. The upper bound is left at 65 rather than raised to the 75 that
    간편심사 products reach, because [R4] names the 61-75 band as the one carrying
    수준리스크 from an absence of experience.
    """
    v = int(model_point()["issue_age"])
    if not 15 <= v <= 65:
        raise ValueError("issue_age outside the composite's 15-65 range")
    return v


def expiry_age():
    """The 만나이 at which cover ends: 100, the 100세 계약해당일.

    Two retrieved contracts run to a 100세 계약해당일 [S4] [S7] and the supervisor's account
    of where the market moved reads 보험기간 「통상 80세 이하」 to 「100세 혹은 사망
    시(종신)까지」 [R3]. 종신 was not taken because no retrieved life contract is written
    종신 and because a terminal age lets the projection end at a stated 계약해당일 rather than
    at the terminal age of a **[std]** mortality table.
    """
    return int(model_point()["expiry_age"])


def sum_assured():
    """S: the 보험가입금액, the unit every diagnosis tier is a ratio of.

    3,000만원 on the anchor cell **[std]**: the retrieved documents give ratios far more often
    than amounts, the one clean ladder stating every tier at 보험가입금액 1,000만원 [S3 별표
    1]. The observed anchors are a 금융감독원 분쟁조정 case turning on 일반암 진단비
    3,000만원 against 갑상선암 진단비 300만원, an earlier case on 5,000만원, and the
    supervisor's own illustration at 「예: 5천만 원」 [R3]. The event modules' own amounts
    scale with it off the 3,000만원 reference; see :func:`hosp_daily`.
    """
    return float(model_point()["sum_assured"])


def premium_mth_pp():
    """P: the level **monthly** office premium per policy **[std]**.

    ``premium_mth_pp`` and not ``premium_pp``: the library spells a monthly per-policy premium
    ``premium_mth_pp``, and this product's grid step is the payment interval.

    An input, not a computed quantity. **No Korean carrier publishes a rate table for a cancer
    main contract**: the 산출방법서 is a 기초서류 filed with the FSC and not a public document,
    and the 참조순보험요율 reaches the public only as the 보험가격지수 ratio -- 보험료총액
    divided by (참조순보험료 총액 + 보험회사 평균사업비총액) -- which is a ratio and never a
    rate [REG-R22] [REG-R4]. The only retrieved premium figures carry **no stated
    보험가입금액**, so they are price points without a benefit denominator [S8]. The anchor's
    45,000 won is anchored by arithmetic rather than by quotation and no result in this
    library depends on its being a market rate; ``technical-notes.md`` performs the
    equivalence calculation on the shipped basis and its figure governs.
    """
    return float(model_point()["premium"])


def chassis():
    """The cover chassis: ``bi_gaengsin`` (비갱신형) or ``gaengsin`` (10년 갱신형).

    비갱신형 is the composite although it is the **minority** design -- four of the seven
    retrieved carriers renew [S4] [S6] [S7] [S8] -- and the reason is that **the 면책기간 and
    the 감액기간 are disapplied on every 갱신계약** [S2] [S4] [S6] [S7]. On a renewable chassis
    the two devices this product exists to demonstrate bite once, in the first ten years of a
    sixty-year projection, and are invisible thereafter. The 비갱신형 form is also the only one
    on which a level premium, a 계약자적립액 and a 해약환급금 curve exist over the whole term.
    """
    v = model_point()["chassis"]
    if v not in ("bi_gaengsin", "gaengsin"):
        raise ValueError("invalid chassis")
    return v


def pay_term():
    """The 납입기간 in **years**; 0 means 전기납 (payment for the whole 보험기간).

    20년납 is the composite. It is the 해약공제계수 cap for a 보장성보험 in 감독규정 [별표 14]
    -- 「보험기간(최대 20년)」 -- and the payment term that schedule's note 3 forces the
    연납순보험료 to be recomputed on where the policy term is 20 years or more [REG-R20]. It
    puts 납입완료 at a known date, which makes the 무해지 surrender-value step-up a cliff
    rather than a curve [S3], and it leaves 40 years of paid-up cover on the anchor cell, so
    the projection exercises both halves of every recursion.
    """
    return int(model_point()["pay_term_y"])


def wait_months():
    """W: the 면책기간 the model point carries, in months; 3 on the composite.

    The 암보장개시일 is the 91st day counting the 보험계약일 as day 1, which on a monthly grid
    is ``t = 3``; the wording is stable across carriers and across eight years [S1] [S2] [S3]
    [S4] [S7] and both the institute [R3] and the supervisor [R6] describe it as the norm. It
    is **not** asserted to be a 표준약관 requirement: the 생명보험 표준약관 carries no
    암보장개시일 clause [REG-R25] and one retrieved product has no waiting period at all,
    defining 보장개시일 as the day the first premium is received [S6] -- which is only possible
    if the 90 days is permitted rather than required.

    Zero on a 갱신계약 -- 「※ 갱신계약의 경우 면책기간을 적용하지 않습니다」 [S2] [S4] -- and
    zero for a life under 보험나이 15, which is the carve-out ``Child_KR_S`` inherits and
    inverts [S2] [R3] [R6]. This value is the model point's; each tier's own waiting period is
    :func:`tier_wait_months`, and the two are combined by taking the shorter.
    """
    return int(model_point()["wait_months"])


def reduction_months():
    """G: the 감액기간 in months; 12 on the composite, with 0 and 24 as switches.

    Observed: **none at all** on 일반암 in the newest retrieved contract [S2]; **1 year at
    50%** across 23 named benefits at the same carrier eight years earlier [S1] and at one
    life carrier [S6]; and **2 years at 50%** at four contracts from two life carriers [S3
    제14조제9항] [S4] [S5] [S7]. Two years is modal, at four of seven, and the composite
    nevertheless takes one year: it is the median of the three distinct designs, it is the
    level the supervisor describes -- 「통상 보험계약일 이후 1~2년 이내에 암 진단확정시에는 암
    보험 가입금액의 50%」 [R6] -- and the direction of travel is one-way, the institute
    recording removals from 2019 [R3] and a carrier confirming in 2025 that 「일반암에 대한
    감액 기간이 축소되는 등」 [S10].
    """
    return int(model_point()["reduction_months"])


def similar_ratio():
    """The 유사암 benefit as a fraction of the 보험가입금액; 0.20 on the composite.

    **The most contested parameter in the product**, and the observed range is enormous: 10%
    at both contracts of one life carrier [S6] [S7], 20% at both of another [S3] [S4], 70% on
    a pre-2022 non-life design [S8], and a separately underwritten rider with its own
    가입금액 at the two non-life contracts [S1] [S2]. What moved it is reported but not
    primary: a 금융감독원 공문 of **August 2022** is said to have cut 유사암 benefits to about
    20% of the 일반암 level, from a market in which they had reached 5,000만원 [R12]. **That
    is a news source and the 공문 was not retrieved**; what is sourced is the *effect* -- 20%
    at the two 2024-25 life contracts against 70% in 2021 -- and not the instrument. Model
    point 10 carries the 70% design so that the difference can be priced.
    """
    return float(model_point()["similar_ratio"])


def diag_module():
    """Whether the graded diagnosis benefit is written at all; 1 on the composite.

    Switched off on model point 8, which is the **treatment-cost-only** shape of [S5] -- one
    retrieved contract pays on surgery, inpatient days and chemotherapy and carries **no
    diagnosis lump sum at all**. The state transitions and the premium waiver still run, so
    the switch removes four benefit lines and nothing else.
    """
    return int(model_point()["diag_module"])


def hosp_module():
    """Whether the 암 직접치료 입원급여금 module is attached; 1 on the composite."""
    return int(model_point()["hosp_module"])


def surg_module():
    """Whether the 암 수술급여금 module is attached; 1 on the composite."""
    return int(model_point()["surg_module"])


def treat_module():
    """Whether the 항암약물.방사선 치료급여금 module is attached; 1 on the composite."""
    return int(model_point()["treat_module"])


def waiver_trigger():
    """The 보험료 납입면제 trigger: ``cancer_diag`` or ``none``.

    ``cancer_diag`` is the composite: the waiver fires on the **first diagnosis of a 일반암 or
    고액암** on or after the 암보장개시일, or on a cumulative 장해지급률 of 50% or more, and
    특정소액암 and every 유사암 member other than 중증 갑상선암 are excluded by name [S3
    제14조제1항] [S1 제9조제1항]. The disability limb is out of scope **[std]**: no disability
    incidence appears in this product's source set. On ``none`` the diagnosed keep paying and
    can lapse; one retrieved contract switches the waiver on and off through the **사업방법서**
    rather than through the 약관 at all [S2], so its presence cannot always be read off the
    policy conditions.
    """
    v = model_point()["waiver_trigger"]
    if v not in ("cancer_diag", "none"):
        raise ValueError("invalid waiver_trigger")
    return v


def cv_form():
    """The surrender-value form: ``mijigeup`` (해약환급금 미지급형) or ``pyojun`` (표준형).

    미지급형 is the base because that is where the Korean market is: the 무.저해지 share of
    보장성 초회보험료 ran 11.4% (2018) to 30.4% (2021) to 47.0% (2023) to 63.8% (2024 H1)
    [REG-R27], so a library modelling only 표준형 products models a minority. It is a
    regulatory dispensation and not a contractual gimmick -- 감독규정 제7-66조제4항 permits it
    only where the premium was calculated using a **최적해지율** [REG-R19]. The 표준형 is a
    pricing comparator that **cannot be bought**: 「'표준형'은 보험료 및 해약환급금의 비교
    안내만을 위한 상품으로 가입이 불가능하며」, and its own 해약환급금 「해지율을 적용하지
    않고」 [S3 제41조].
    """
    v = model_point()["cv_form"]
    if v not in ("mijigeup", "pyojun"):
        raise ValueError("invalid cv_form")
    return v


# ===== Cells: the projection frame =====


def proj_len():
    """The **number** of projected policy months, ``12 x (expiry_age - issue_age) + 1``.

    721 on the anchor cell, so :func:`result_cf` carries 721 rows indexed 0 to 720 and the
    frame is ``range(proj_len())``. ``proj_len()`` is the **exclusive end** of the frame and
    not the last index: the last projected month is ``proj_len() - 1``. The ``+ 1`` is the
    terminal row -- the 720 months of cover are ``t = 0 ... proj_len() - 2`` and
    ``t = proj_len() - 1`` is the 100세 계약해당일 itself, which carries the expiring exposure
    and no cash flow at all. Nothing shortens the horizon: paying a diagnosis benefit neither
    terminates nor exhausts the contract [S1] [S3] [S4], and the 갱신형 chassis flag renews
    automatically to the same 100세 계약해당일.
    """
    return 12 * (expiry_age() - issue_age()) + 1


def age(t):
    """age(t): the attained **만나이** in policy month t, ``x + t // 12``."""
    return issue_age() + t // 12


def policy_year(t):
    """y(t): the policy year containing month t, ``t // 12 + 1``.

    The **contractual** policy year, a **1-based** label: the 0-based month ``t = 0`` falls
    in policy year 1.  It is derived from the frame's index and is never the index itself;
    only :func:`lapse_rate` reads it, the lapse scale being written in policy years.
    """
    return t // 12 + 1


def pay_months():
    """The 납입기간 in months; the whole 보험기간 on a 전기납 model point.

    240 on the anchor cell, so 납입완료 falls at ``t = 240`` and the surrender-value cliff of
    the 미지급형 form with it: 「보험료 납입기간 중이라 함은 계약일로부터 보험료 납입기간이
    경과하여 최초로 도래하는 계약해당일 전일까지의 기간」 [S3]. On a 전기납 model point it is
    the whole 보험기간, ``proj_len() - 1`` months -- 720 on model point 3, the 전기납 cell
    carrying the anchor's term, the frame's 720 months of cover without its terminal expiry
    row.
    """
    return proj_len() - 1 if pay_term() == 0 else 12 * pay_term()


def in_force(t):
    """1.0 while the contract is running, 0.0 at the 100세 계약해당일 itself.

    The last row of :func:`result_cf`, ``t = proj_len() - 1``, carries the expiring exposure
    and no cash flow at all, because nothing is paid at expiry [S4] [S7] [S8].
    """
    return 1.0 if t < proj_len() - 1 else 0.0


def tier_wait_months(tier):
    """W_j: the 면책기간 tier ``tier`` carries, in months, after the model point's own.

    The shorter of the tier's contractual wait and the model point's ``wait_months``, so that
    a 갱신계약 or a life under 보험나이 15 removes both. The tier's own value comes from
    *tier_table.csv*: **3 for the invasive tiers and 0 for 유사암**, which is where the
    product's two start dates come from -- 「유사암의 보장개시일은 계약일임」 [S1], the
    면책기간 table marking 유사암 진단비 with a cross [S1] [S2].
    """
    return min(wait_months(), int(data.tier_table().loc[tier, "wait_months"]))  # noqa: F821


def cover(t):
    """cover(t): 1 from the 암보장개시일, 0 inside the 90-day 면책기간.

    A **hard zero**, not a reduced rate. It multiplies every invasive-tier benefit and both
    invasive transitions, so in months 0, 1 and 2 the model diagnoses nobody with an invasive
    cancer and pays nothing for one -- while still collecting the premium, because the 유사암
    tier and every non-cancer cover are already in force and because the invalidity rule
    returns the premium for the affected cover if a diagnosis does fall inside the window [S1]
    [S2] [S3]. It also closes at expiry.
    """
    return 1.0 if tier_wait_months("general") <= t < proj_len() - 1 else 0.0


def cover_similar(t):
    """cover_z(t): the 유사암 tier's cover, in force from ``t = 0``.

    The second of the product's two start dates. 「유사암의 보장개시일은 계약일임」 [S1], and
    the 면책기간 table of both non-life contracts marks 유사암 진단비 with a cross [S1] [S2]
    while the summary of a life contract marks its four 유사암 limbs with a dash [S7]. One
    life carrier does apply the wait to 갑상선암 [S3] [S4] and the composite follows the
    majority.
    """
    return 1.0 if tier_wait_months("similar") <= t < proj_len() - 1 else 0.0


def reduction_factor(t):
    """g(t): 0.50 inside the 감액기간 and 1.00 after it, on **every** diagnosis tier.

    The clock runs 「보험계약일부터 진단 확정일까지」 [S3 별표 1 주2], so on the monthly grid
    the boundary is ``t = reduction_months()``. It is disapplied on a 갱신계약, which the
    model point carries as ``reduction_months = 0`` rather than as a separate switch [S2] [S4].
    """
    return 0.5 if t < reduction_months() else 1.0


# ===== Cells: decrement, incidence and survival bases =====


def mort_rate(t):
    """The annual all-cause mortality of the insured at :func:`age` ``(t)``.

    ``mort_be_factor`` times the shipped **[std]** table, which is a Makeham reproducing the
    국가데이터처 생명표's published 2024 기대여명 at 40 and 65 exactly [REG-R38] rather than a
    copy of the 제10회 경험생명표, which is not published in full [REG-R33] [REG-R34]. The
    factor is 1.0: the table is already a *population* all-cause basis rather than a valuation
    table with a margin in it, so there is nothing to unwind. Mortality here is a pure
    liability-releasing decrement except for the 계약자적립액 it pays out.
    """
    tbl = data.mort_table()                                          # noqa: F821
    a = min(age(t), int(tbl.loc[sex()].index.max()))
    return min(1.0, mort_be_factor * float(tbl.loc[(sex(), a), "mort_rate"]))  # noqa: F821


def mort_rate_mth(t):
    """q_mth(t): the monthly base mortality, ``1 - (1 - q)^(1/12)``."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def excess_hazard(tier, k):
    """mu_k: the annual excess hazard of a diagnosed life in select duration bucket k.

    Read from *survival_table.csv* by sex, tier and ``dur_year``, with ``k = 6`` standing for
    the ultimate. **Relative survival is a ratio, not a transition rate** -- 「관찰생존율을
    일반인구의 기대생존율로 나누어 구한 값」 [R1] -- so it converts into an excess hazard
    **added to** the base table rather than a replacement for it, and multiplying survivorship
    by it would double-count the background. The five select years are calibrated so that
    ``exp(-sum)`` equals the published 2019-2023 five-year relative survival excluding
    thyroid, 남 65.9% / 여 74.0% [R1], for the general tier, and an [R1]-derived 87.1% / 88.8%
    for the 특정소액암 tier; the front-loading and the ultimate level are **[std]**.
    """
    return float(data.survival_table().loc[                          # noqa: F821
        (sex(), tier, k), "excess_hazard"])


def mort_rate_waived_mth(t, k):
    """q_w(t,k): the monthly mortality of a 일반암 / 고액암 life in duration bucket k.

    ``1 - (1 - q_mth) exp(-mu_k / 12)`` -- the baseline **plus** an excess hazard. At the
    anchor cell's first select year the excess is 0.146 a year against a base mortality of
    0.0011, so the diagnosed decrement is two orders of magnitude above the healthy one and it
    is what every post-diagnosis limb is integrated over.
    """
    return 1.0 - (1.0 - mort_rate_mth(t)) * math.exp(                # noqa: F821
        -excess_hazard("general", k) / 12.0)


def mort_rate_minor_mth(t, k):
    """q_n(t,k): the monthly mortality of a 특정소액암 life in duration bucket k.

    Much lighter than :func:`mort_rate_waived_mth`, and that is a data fact rather than a
    modelling choice: the three sites in the tier publish five-year relative survivals of 대장
    75.6, 유방 94.7 and 전립선 96.9 per cent against 69.6 for all cancer excluding thyroid
    [R1]. Giving the two states one hazard would kill the tier that pays no waiver at the rate
    of the tier that does.
    """
    return 1.0 - (1.0 - mort_rate_mth(t)) * math.exp(                # noqa: F821
        -excess_hazard("minor", k) / 12.0)


def lapse_rate(t):
    """The **annual** lapse rate applying in policy year ``y(t)`` **[std]**.

    A 로그-선형 curve from 4.6% in policy year 1 to **0.1% at 납입완료**, stepping to a
    **0.8%** ultimate thereafter. The functional form is prescribed rather than fitted: the
    FSS's November 2024 계리가정 ruling makes the 로그-선형 모형 converging to 0.1% at 완납 the
    **원칙모형** for 무.저해지 business, with a 0.8% post-완납 ultimate [REG-R27], and
    감독규정 제7-66조제4항 permits the 미지급형 form only where a **최적해지율** was used to
    price it [REG-R19]. **No public Korean lapse or persistency figure for 암보험 exists**
    [R3], so the level of the first year is standardized and the shape is not.

    Nothing breaks the fall on this product: the 미지급형 form has no surrender value during
    the 납입기간, so there is no 보험계약대출 to draw on and no 자동대출납입, and a missed
    premium lapses at the end of the 14-day 납입최고 [S3] [REG-R25 제26조] [REG-R28].
    """
    tbl = data.lapse_table()                                         # noqa: F821
    r0 = float(tbl.loc["first_year", "lapse_rate"])
    r1 = float(tbl.loc["at_completion", "lapse_rate"])
    r2 = float(tbl.loc["post_payment", "lapse_rate"])
    n = max(pay_months() // 12, 2)
    y = policy_year(t)
    if y > n:
        return r2
    return r0 * (r1 / r0) ** ((y - 1) / (n - 1))


def lapse_rate_mth(t):
    """w_mth(t): the monthly lapse rate of a premium-paying life, ``1 - (1 - w)^(1/12)``."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def lapse_rate_canc_mth(t):
    """w_c(t): the monthly lapse rate of a **waived** life; zero in the base run.

    A product fact, not a refinement. The waiver fires on the first 일반암 or 고액암, so a
    waived life has no premium to miss, and on the 미지급형 form there is no surrender value
    to cash in and no 보험계약대출 to take against it [S3 제41조] [REG-R28] -- so there is no
    mechanism by which a waived policy leaves the book other than death. Applying the healthy
    lapse rate to that state deletes exactly the claimants the product exists to pay. On the
    ``waiver_trigger = "none"`` design the premium does not stop and the rate becomes the
    healthy one scaled by ``lapse_canc_factor``.
    """
    if waiver_trigger() == "cancer_diag":
        return 0.0
    return lapse_rate_mth(t) * lapse_canc_factor                     # noqa: F821


def inc_rate(t):
    """The annual incidence of an invasive cancer **excluding C44 and C73**, per policy.

    Read off 보험개발원's published 「기타피부암 및 갑상선암 이외의 암 발생률」 grid for the
    참조순보험요율 in force from 2024-04-01 [R5] [REG-R61] and interpolated **log-linearly**
    between its ten-year age points, which is the shape cancer incidence actually has. 0.001343
    at the anchor cell, sourced and not standardized.

    Its definition is the *insured* one -- invasive cancer excluding 기타피부암 and 갑상선암,
    classified by **원발부위** -- so it already embodies both the tier carve-out the 약관 make
    and the primary-site rule the supervisor imposed from 2011-04-01, which was a direct
    instruction about the pricing basis: 「갑상선을 원발부위로 하는 경우를 갑상선암에 모두
    포함한 위험률을 적용하라는 것임」 [R3]. An independent reconciliation against the registry
    agrees to within 1.6% at male 만나이 40 [R1].

    ``inc_be_factor`` is the **[std]** adjustment from a 참조순보험요율 -- a net premium rate
    with a safety loading inside it [REG-R4] -- to a best estimate, and it is left at 1.0
    because the only figure for the loading is **[unverified]**.
    """
    tbl = data.incidence_table().loc[sex()]                          # noqa: F821
    ages = list(tbl.index)
    a = min(max(age(t), ages[0]), ages[-1])
    lo = max(g for g in ages if g <= a)
    hi = min(g for g in ages if g >= a)
    r_lo = float(tbl.loc[lo, "inc_rate"])
    if hi == lo:
        return r_lo * inc_be_factor                                  # noqa: F821
    r_hi = float(tbl.loc[hi, "inc_rate"])
    frac = (a - lo) / (hi - lo)
    return math.exp(math.log(r_lo) + frac * (                        # noqa: F821
        math.log(r_hi) - math.log(r_lo))) * inc_be_factor            # noqa: F821


def tier_share(col, t):
    """The **[std]** tier share ``col`` at :func:`age` ``(t)``, linear in age.

    Reads *tier_share_table.csv*, whose anchors are at 만나이 20, 40, 60 and 80 and which is
    clamped outside them. The three shares are graded in age because the tiers' age mixes
    differ violently: 갑상선 is the rank-1 site for women to 39 and for men to 49 [R1] while
    the invasive base rate rises by a factor of 20 between 40 and 80 [R5], so an age-invariant
    decomposition misprices the reduced tier by a wide margin.
    """
    tbl = data.tier_share_table().loc[sex()]                         # noqa: F821
    ages = list(tbl.index)
    a = min(max(age(t), ages[0]), ages[-1])
    lo = max(g for g in ages if g <= a)
    hi = min(g for g in ages if g >= a)
    v_lo = float(tbl.loc[lo, col])
    if hi == lo:
        return v_lo
    v_hi = float(tbl.loc[hi, col])
    return v_lo + (v_hi - v_lo) * (a - lo) / (hi - lo)


def minor_share(t):
    """m(a): the share of :func:`inc_rate` falling in the 특정소액암 tier **[std]**.

    직.결장암, 유방암 (C50), 여성생식기암 and 전립선암 (C61) [S3]. Anchored on [R1]'s 2023
    all-ages crude site rates -- 대장 63.8, 유방 58.4 and 전립선 44.3 against an
    excluding-thyroid base of 495.0 per 100,000, i.e. 33.6% on both sexes combined -- and then
    graded in age and split by sex on the registry's own site-by-age rankings, 유방 being rank
    1 for women from 40 to 69 and 전립선 rank 1 for men from 60 to 79 [R1]. Its complement is
    the 일반암 tier, which is why :func:`check_tier_shares` asserts the two sum to the base
    rate.
    """
    return tier_share("minor_share", t)


def high_share(t):
    """h(a): the 고액암 sub-share of :func:`inc_rate` **[std]**.

    C40-C41 (골 및 관절연골), C70-C72 (뇌 및 중추신경계통) and C91-C95 + D47.1 + D47.5
    (백혈병) -- the tight three-site list, the only one of the three retrieved definitions
    given as KCD ranges rather than Korean site names, and the same three sites a carrier calls
    the market's base definition [S3] [S10]. **Its incidence is not separately published**:
    none of 골, 뇌 or 백혈병 appears in [R1]'s 2023 top-ten table, whose smallest entry is 간
    at 28.8 per 100,000, so the tier is a construction rather than a rate.

    It is a **sub-share of the general tier and not a fourth partition**: the benefit adds to
    the 일반암 amount rather than replacing it [S3], so a leukaemia diagnosis pays 200% of the
    보험가입금액 and a stomach cancer 100%.
    """
    return tier_share("high_share", t)


def similar_share(t):
    """z(a): 유사암 incidence as a **ratio to** :func:`inc_rate` **[std]**.

    Additive rather than a partition, because 기타피부암 (C44), 갑상선암 (C73), 대장점막내암,
    제자리암 (D00-D09) and 경계성종양 (D37-D48) are all outside the base rate's own
    definition. Two components are sourced -- 갑상선 조발생률 69.3 and 상피내암 74.7 per
    100,000, 남 48.0 / 여 101.2 [R1] -- and three are not: [R1] does not cover 경계성종양 at
    all, does not identify 대장점막내암 inside 대장 D010-D012, and does not carry 기타피부암 in
    its top-ten table. **The ratio is therefore a floor.**

    The age grading is steep and the sex split large because the tier is overwhelmingly a
    young-female exposure: 갑상선 is the rank-1 female site to age 39, the female 30-39
    갑상선 crude rate is 164.3 per 100,000 [R1], and the in-situ increment is 8.1% of male
    invasive cases against 18.9% of female [R1]. The trend is the other reason this tier is
    carried separately: the in-situ age-standardised rate rose by a factor of **7.9** between
    1999 and 2023 while the invasive one rose by 1.30 [R1].
    """
    return tier_share("similar_share", t)


def inc_rate_gen_mth(t):
    """i_g(t): monthly 일반암 incidence, ``inc_rate (1 - m) / 12``.

    The tier that pays 100% of the 보험가입금액, triggers the premium waiver and moves the
    life into :func:`pols_waived`. Uniform within the year **[std]**.
    """
    return inc_rate(t) * (1.0 - minor_share(t)) / 12.0


def inc_rate_minor_mth(t):
    """i_m(t): monthly 특정소액암 incidence, ``inc_rate x m / 12``."""
    return inc_rate(t) * minor_share(t) / 12.0


def inc_rate_high_mth(t):
    """i_h(t): monthly 고액암 incidence, ``inc_rate x h / 12``, a subset of i_g."""
    return inc_rate(t) * high_share(t) / 12.0


def inc_rate_similar_mth(t):
    """i_z(t): monthly 유사암 incidence, ``inc_rate x z / 12``, additive to i_g and i_m."""
    return inc_rate(t) * similar_share(t) / 12.0


def surv_healthy(t):
    """s_0(t): the survival factor of a never-diagnosed life over month t.

    ``(1 - q_mth)(1 - w_mth)``, applied to the survivors of the month's diagnoses: a life
    diagnosed in month t leaves this state **before** the decrement and takes its new state's
    mortality for the month it is diagnosed in **[std]**.
    """
    return (1.0 - mort_rate_mth(t)) * (1.0 - lapse_rate_mth(t))


def surv_waived(t, k):
    """s_w(t,k): the survival factor of a waived life in duration bucket k over month t.

    ``(1 - q_w)(1 - w_c)``, and in the base run ``w_c = 0``, so it is pure mortality: a waived
    policy leaves the book only by death.
    """
    return (1.0 - mort_rate_waived_mth(t, k)) * (1.0 - lapse_rate_canc_mth(t))


def surv_minor(t, k):
    """s_n(t,k): the survival factor of a 특정소액암 life in bucket k over month t.

    Three factors, not two: ``(1 - i_g cover)`` for the transition **out** of the tier into
    the 일반암 state, then ``(1 - q_n)`` and ``(1 - w_mth)``. The first is what makes a later
    일반암 on a 특정소액암 life a modelled event rather than an omission, and it is applied
    first, so a life that transitions takes the waived state's mortality for the rest of the
    month.
    """
    return ((1.0 - inc_rate_gen_mth(t) * cover(t))
            * (1.0 - mort_rate_minor_mth(t, k))
            * (1.0 - lapse_rate_mth(t)))


# ===== Cells: the three states =====


def void_prob():
    """The probability of an invasive diagnosis inside the 면책기간; zero in the base run.

    ``1 - (1 - i_g(0) - i_m(0))^W``. A diagnosis inside the window does not merely go unpaid:
    the affected cover is **무효** and its premiums are returned, the rest of the contract
    surviving unless the policyholder cancels it within 90 days of the 진단확정일 [S1
    제28조제2항.제3항] [S2] [S3]; the statutory hook is 상법 제644조 [R7]. **That is a
    de-recognition, not a decrement**: the cover was never in force, so it releases premium
    already collected as well as future benefit, and it belongs in a validity adjustment at
    outset rather than in the lapse column. ``void_adjust`` is off in the base run and the
    omission is quantified here rather than waved at.
    """
    if not void_adjust:                                              # noqa: F821
        return 0.0
    return 1.0 - (1.0 - inc_rate(0) / 12.0) ** wait_months()


def pols_if_init():
    """The exposure in force at ``t = 0``: one policy, less any validity adjustment.

    The acquisition expense and the initial commission are deliberately **not** scaled by it:
    they were incurred whether or not the invasive cover turns out to have been void.
    """
    return 1.0 - void_prob()


def pols_healthy(t):
    """l_0(t): in force at the start of month t and **never diagnosed with an invasive cancer**.

    ``(pols_healthy(t) - diag_first(t)) s_0(t)``. A 유사암 diagnosis does **not** move a life
    out of this state: it is a second benefit tier on its own ledger, not a state change, and
    it carries no excess mortality [R1].
    """
    if t <= 0:
        return pols_if_init() if t == 0 else 0.0
    if t >= proj_len():
        return 0.0
    return (pols_healthy(t - 1) - diag_first(t - 1)) * surv_healthy(t - 1)


def diag_gen_h(t):
    """First 일반암 (including 고액암) diagnoses arising from the healthy state in month t."""
    return pols_healthy(t) * inc_rate_gen_mth(t) * cover(t)


def diag_minor(t):
    """n_m(t): first 특정소액암 diagnoses in month t, from the healthy state alone.

    A general-tier life's later 특정소액암 is a **[std]** omission; it understates.
    """
    return pols_healthy(t) * inc_rate_minor_mth(t) * cover(t)


def diag_first(t):
    """All first invasive diagnoses in month t: the whole exit from :func:`pols_healthy`.

    ``diag_gen_h(t) + diag_minor(t)``, which is ``pols_healthy(t) x inc_rate_mth(t) x
    cover(t)`` because the two tier shares partition the base rate -- the identity
    :func:`check_tier_shares` asserts.
    """
    return diag_gen_h(t) + diag_minor(t)


def diag_gen_m(t):
    """일반암 diagnoses arising on lives already in the 특정소액암 state in month t.

    The second limb of :func:`diag_gen`, and the transition the ``(1 - i_g cover)`` factor of
    :func:`surv_minor` removes from the 특정소액암 state. It matters more than it looks: the
    특정소액암 sites are between a fifth and a half of all invasive incidence depending on age
    and sex, their survival is much better than the general tier's, and those lives are still
    paying premium -- so a model that never lets them progress keeps them paying for ever.
    """
    return (pols_minor(t) + diag_minor(t)) * inc_rate_gen_mth(t) * cover(t)


def diag_gen(t):
    """n_g(t): all 일반암 / 고액암 diagnoses in month t, from both source states.

    The event that pays 100% of the 보험가입금액, stops the premium and starts the six-cohort
    duration clock.
    """
    return diag_gen_h(t) + diag_gen_m(t)


def diag_high(t):
    """n_h(t): 고액암 diagnoses in month t, a **subset** of :func:`diag_gen`.

    Paid **in addition to** the general-tier benefit and not instead of it, so a life diagnosed
    with a leukaemia draws 200% of the 보험가입금액 and neither amount is paid twice: 「보험
    기간 중 이미 암진단자금을 지급한 이후 특정 고액치료비관련 암진단자금의 지급사유가 발생한
    경우에는 암진단자금을 다시 지급하지 않습니다」 [S3]. A 고액암 following a plain 일반암 is a
    **[std]** omission.
    """
    return (pols_healthy(t) + pols_minor(t) + diag_minor(t)) * \
        inc_rate_high_mth(t) * cover(t)


def diag_similar(t):
    """n_z(t): 유사암 diagnoses drawing the reduced benefit in month t.

    Attaches to the **whole in-force**, not to the never-diagnosed alone, because the tier is
    independent of the invasive ones and a 유사암 can follow an invasive cancer. Gated by
    :func:`similar_avail`, which is the once-only ledger.

    **A [std] simplification with a stated direction**: the contracts pay each of the five
    유사암 members once in its own right [S3] [S4], so a life can draw the tier up to five
    times, and a single aggregate ledger therefore **understates** the tier. Modelling it
    member by member would need incidence rates for 경계성종양 and 대장점막내암 that [R1] does
    not publish at all.
    """
    return (pols_if(t) * similar_avail(t) * inc_rate_similar_mth(t)
            * cover_similar(t) * diag_module())


def waived_grad(t, k):
    """G_w(t,k): the waived-state cohort graduating out of duration bucket k at month t.

    The duration clock is a **delay keyed to the diagnosis month**, not a transfer rate, so it
    is implemented on the entry history: the lives diagnosed in month ``t - 13`` reach elapsed
    duration 13 at ``t`` and leave bucket 1, and each later bucket takes the previous bucket's
    graduates twelve months on, carried forward on that bucket's own decrements. A rate-based
    transfer would smear a cohort across every bucket at once and flatten exactly the selection
    the six buckets exist to carry.
    """
    if k == 1:
        s = t - 13
        if s < 0:
            return 0.0
        cohort = diag_gen(s)
    else:
        s = t - 12
        if s < 0:
            return 0.0
        cohort = waived_grad(s, k - 1)
    if cohort == 0.0:
        return 0.0
    factor = 1.0
    for u in range(s, t):
        factor = factor * surv_waived(u, k)
    return cohort * factor


def minor_grad(t, k):
    """G_n(t,k): the 특정소액암 cohort graduating out of duration bucket k at month t.

    :func:`waived_grad`'s twin on the other diagnosed state, carried forward on
    :func:`surv_minor` -- which includes the transition into the general state, so a cohort
    that progresses is removed from this ledger as well as from the population.
    """
    if k == 1:
        s = t - 13
        if s < 0:
            return 0.0
        cohort = diag_minor(s)
    else:
        s = t - 12
        if s < 0:
            return 0.0
        cohort = minor_grad(s, k - 1)
    if cohort == 0.0:
        return 0.0
    factor = 1.0
    for u in range(s, t):
        factor = factor * surv_minor(u, k)
    return cohort * factor


def pols_waived_dur(t, k):
    """D_w(t,k): in force, premium waived, elapsed duration in select year k.

    ``k = 1`` holds elapsed months 1 to 12, ``k = 5`` months 49 to 60 and ``k = 6`` everything
    beyond. Bucket 1 takes the month's new :func:`diag_gen`; every bucket takes the previous
    one's graduates and gives up its own, and the graduation terms telescope out of the sum,
    which is the identity :func:`check_cancer_roll_fwd` asserts.
    """
    if t <= 0 or t >= proj_len():
        return 0.0
    total = pols_waived_exp(t - 1, k) * surv_waived(t - 1, k)
    if k >= 2:
        total = total + waived_grad(t, k - 1)
    if k <= 5:
        total = total - waived_grad(t, k)
    return total


def pols_minor_dur(t, k):
    """D_n(t,k): in force, 특정소액암 only, elapsed duration in select year k.

    The state that still pays premium. Same six-cohort machinery as :func:`pols_waived_dur`,
    on :func:`surv_minor`.
    """
    if t <= 0 or t >= proj_len():
        return 0.0
    total = pols_minor_exp(t - 1, k) * surv_minor(t - 1, k)
    if k >= 2:
        total = total + minor_grad(t, k - 1)
    if k <= 5:
        total = total - minor_grad(t, k)
    return total


def pols_waived_exp(t, k):
    """The waived-state exposure in bucket k **during** month t, entrants included.

    ``D_w(t,k)`` plus, for ``k = 1``, the month's own :func:`diag_gen`. A life diagnosed in
    month t is exposed to the waived state's decrements for the rest of that month **[std]**,
    which is the convention the healthy state's ``- diag_first`` term is the other half of.
    """
    return pols_waived_dur(t, k) + (diag_gen(t) if k == 1 else 0.0)


def pols_minor_exp(t, k):
    """The 특정소액암 exposure in bucket k during month t, entrants included."""
    return pols_minor_dur(t, k) + (diag_minor(t) if k == 1 else 0.0)


def pols_waived(t):
    """l_w(t): in force with a 일반암 or 고액암, premium waived, summed over the six cohorts."""
    return sum(pols_waived_dur(t, k) for k in range(1, 7))


def pols_minor(t):
    """l_n(t): in force with a 특정소액암 only, still paying, summed over the six cohorts."""
    return sum(pols_minor_dur(t, k) for k in range(1, 7))


def pols_cancer(t):
    """l_c(t): the diagnosed in-force population, waived plus 특정소액암.

    The weight on all three event benefits. Publishing it beside :func:`pols_healthy` and
    :func:`pols_minor` in :func:`result_cf` is what makes the product's central asymmetry
    visible in the table itself: premiums ride on two of the three states and the care benefits
    on the other two.
    """
    return pols_waived(t) + pols_minor(t)


def pols_if(t):
    """The total in force at the **start** of month t: healthy plus diagnosed.

    A start-of-period count, equal to :func:`pols_if_init` on the first row, and the weight on
    the maintenance expense of the same :func:`result_cf` row -- a waived policy is still
    serviced. It is **not** the weight on ``premiums``, which rides on :func:`pols_payer`, nor
    on the benefit lines. A first diagnosis moves a life between states and leaves this figure
    untouched.
    """
    return pols_healthy(t) + pols_cancer(t)


def pols_if_at(t, timing):
    """The in-force count at a named point inside month t.

    The library-wide timing vocabulary over the whole book:

    ``"BEF_DECR"``
        the start-of-month count, :func:`pols_if`, and the weight on the
        ``result_cf()`` row of the same ``t``.

    ``"BEF_LAPSE"``
        after mortality and before lapse, **summed over the three states**, each
        decremented on its own basis and the diagnosed ones bucket by bucket. A
        single blended rate applied to :func:`pols_if` does not reproduce it.

    ``"AFT_DECR"``
        after both decrements, which is :func:`pols_if` of ``t + 1``.

    What the vocabulary cannot show is the movement that defines the product: the three
    timings are *decrement* timings and a diagnosis is not a decrement. Read
    :func:`pols_healthy`, :func:`pols_minor`, :func:`pols_waived` and :func:`diag_gen` for the
    state movement; ``pols_if_at`` answers only how many lives are left.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DECR":
        return pols_if(t + 1)
    if timing == "BEF_LAPSE":
        total = (pols_healthy(t) - diag_first(t)) * (1.0 - mort_rate_mth(t))
        for k in range(1, 7):
            total = total + pols_waived_exp(t, k) * (
                1.0 - mort_rate_waived_mth(t, k))
            total = total + pols_minor_exp(t, k) * (
                1.0 - inc_rate_gen_mth(t) * cover(t)) * (
                1.0 - mort_rate_minor_mth(t, k))
        return total
    raise ValueError("invalid timing")


def pols_death(t):
    """d(t): deaths at the end of month t, from all three states.

    There is **no death benefit** -- the composite pays the 계약자적립액 and terminates, which
    is what 감독규정 제7-63조제1항제1호 requires of a 제3보험 product [REG-R17] [REG-R25
    제22조] -- so mortality is a liability-releasing decrement carrying only ``claims(t,
    "DEATH")``. Lives diagnosed in month t are already in their new state for this purpose.
    """
    if t >= proj_len() - 1:
        return 0.0
    total = (pols_healthy(t) - diag_first(t)) * mort_rate_mth(t)
    trans = 1.0 - inc_rate_gen_mth(t) * cover(t)
    for k in range(1, 7):
        total = total + pols_waived_exp(t, k) * mort_rate_waived_mth(t, k)
        total = total + pols_minor_exp(t, k) * trans * mort_rate_minor_mth(t, k)
    return total


def pols_lapse(t):
    """lap(t): lapses at the end of month t, taken from the survivors of mortality.

    Zero out of the waived state in the base run, because a waived life has no premium to miss.
    What a lapse pays is :func:`cv_pp`, which on the 미지급형 form is **nil for the whole
    납입기간** and 50% of the 표준형 value afterwards [S3 제41조제2항] [REG-R19].
    """
    if t >= proj_len() - 1:
        return 0.0
    total = ((pols_healthy(t) - diag_first(t)) * (1.0 - mort_rate_mth(t))
             * lapse_rate_mth(t))
    trans = 1.0 - inc_rate_gen_mth(t) * cover(t)
    for k in range(1, 7):
        total = total + (pols_waived_exp(t, k)
                         * (1.0 - mort_rate_waived_mth(t, k))
                         * lapse_rate_canc_mth(t))
        total = total + (pols_minor_exp(t, k) * trans
                         * (1.0 - mort_rate_minor_mth(t, k))
                         * lapse_rate_mth(t))
    return total


def pols_maturity(t):
    """The exposure whose cover ends at the 100세 계약해당일; zero everywhere else.

    ``pols_maturity`` and not ``pols_expiry``: the library's name for the count whose cover
    ends at the scheduled end of the contract, whether or not anything is paid for it. Here
    nothing is -- there is no 만기환급금 on the 순수보장형 form [S8] -- so ``claims(t,
    "MATURITY")`` is identically zero and the column is published rather than dropped.

    It falls on the frame's last row, ``t = proj_len() - 1``.
    """
    return pols_if(t) if t == proj_len() - 1 else 0.0


# ===== Cells: the once-only ledgers =====


def similar_avail(t):
    """Z(t): the probability the once-only 유사암 benefit is still unused.

    ``Z(t+1) = Z(t) (1 - i_z(t) cover_z(t))`` from ``Z(0) = 1``. A ledger of its own rather
    than a flag on the diagnosis benefit, because the tier has its own cap, its own start date
    and no effect on the premium waiver or on mortality.
    """
    if t <= 0:
        return 1.0 if t == 0 else 0.0
    return similar_avail(t - 1) * (
        1.0 - inc_rate_similar_mth(t - 1) * cover_similar(t - 1) * diag_module())


def similar_used(t):
    """The once-only 유사암 tier consumed per in-force policy before month t.

    Accumulated straight off the published claim line, ``diag_similar(s) / pols_if(s)``, with
    no reference to the :func:`similar_avail` recursion, so that
    :func:`check_similar_ledger` asserts that what was paid and what remains still sum to one.
    """
    if t <= 0:
        return 0.0
    lives = pols_if(t - 1)
    used = diag_similar(t - 1) / lives if lives > 0.0 else 0.0
    return similar_used(t - 1) + used


def treat_avail(k):
    """A(k): the probability a diagnosed life's 치료급여금 is still unused, in bucket k.

    The 항암약물.방사선 치료급여금 is 「최초 1회한」 in every retrieved contract [S1] [S4]
    [S5] -- a sharp structural contrast with Japan's per-month design -- so it needs a
    once-only ledger per diagnosed life rather than a rate. ``A(k) = exp(-H(m_k))`` where
    ``H`` is the cumulative first-treatment hazard of *care_table.csv* and ``m_k`` is the
    bucket's midpoint in months, so it is a function of elapsed duration alone and not of the
    block. The ultimate hazard is **zero [std]**: the benefit is on the *first* qualifying
    treatment and essentially every patient who will ever receive 항암화학요법,
    항암면역요법 or 고에너지 전리 방사선 receives it within five years of diagnosis, which
    also makes the once-only bound hold at any horizon.
    """
    tbl = data.care_table()                                          # noqa: F821
    m = 12 * (k - 1) + 6
    cum = 0.0
    for j in range(1, min(k, 6) + 1):
        span = min(12, m - 12 * (j - 1)) / 12.0
        cum = cum + float(tbl.loc[j, "treat_hazard_yr"]) * span
    return math.exp(-cum)                                            # noqa: F821


def treat_cum_pp(t):
    """The cumulative 치료급여금 payment probability of a life diagnosed at ``t = 0``.

    A pure function of elapsed duration, independent of the block, accumulated month by month
    off exactly the rate and availability :func:`claims` uses. It is what makes the once-only
    cap checkable: :func:`check_treat_ledger` asserts it never passes 1.
    """
    if t <= 0:
        return 0.0
    k = min(6, (t - 1) // 12 + 1)
    rate = float(data.care_table().loc[k, "treat_hazard_yr"]) / 12.0  # noqa: F821
    return treat_cum_pp(t - 1) + rate * treat_avail(k)


# ===== Cells: benefit amounts =====


def benefit_ratio(tier):
    """r_j: tier ``tier``'s benefit as a fraction of the 보험가입금액.

    200 / 100 / 60 / 20 per cent for 고액암 / 일반암 / 특정소액암 / 유사암, the 고액암 figure
    being carried as a **100% top-up** because the benefit adds to the general tier rather
    than replacing it. The ratios are **read, not inferred**: one retrieved contract states
    every tier as an amount at 보험가입금액 1,000만원 [S3 별표 1]. The 유사암 ratio is taken
    from the model point rather than from the file, because it is the one ratio the market
    moved -- 10% [S6] [S7], 20% [S3] [S4] and 70% [S8] are all observed -- and
    *tier_table.csv*'s own 0.20 row is the composite default.
    """
    if tier == "similar":
        return similar_ratio()
    return float(data.tier_table().loc[tier, "benefit_ratio"])       # noqa: F821


def hosp_daily():
    """The 암 직접치료 입원급여금 daily amount, 50,000 won at the 3,000만원 reference **[std]**.

    Paid from day 1 of a stay whose **direct purpose** is cancer treatment, to 180 days per
    stay [S1] [S4] [R3]. Scaled linearly with the 보험가입금액 off the composite's 3,000만원,
    because the retrieved contracts sell the module with its own 가입금액 and the composite
    carries one. Days at a **요양병원** are excluded and fall to a separate 90-day rider this
    model does not carry [S2] [S8] -- the market's own structural answer to the benefit that
    drew 2,125 complaints to 금융감독원 in 2018 alone [R3].
    """
    return hosp_daily_base * sum_assured() / sa_ref                  # noqa: F821


def hosp_day_cap():
    """The 180-day per-stay cap on the inpatient benefit.

    Sourced -- 180 days per stay at one carrier, 120 at another, and the institute describing
    the market as 「1회 입원당 120일 또는 180일」 with same-cancer admissions summed and 「최종
    입원의 퇴원일부터 180일이 경과하여 개시한 입원은 새로운 입원」 [R3] -- and it does **not
    bind** on the deterministic mean stay this model carries. :func:`check_hosp_cap` states
    that rather than leaving a reader to discover it: the cap is a property of the contract and
    of a stochastic model, and on an expected-value projection it is inert.
    """
    return float(hosp_day_cap_days)                                  # noqa: F821


def surg_open_amt():
    """The 관혈 (open) 암 수술급여금, 5,000,000 won at the 3,000만원 reference **[std]**.

    The 5 : 1 관혈 / 비관혈 split is read directly off a module schedule at 보험가입금액
    500만원 [S4]. 대뇌내시경, 흉강경수술, 복강경수술 and 조혈모세포이식 「관혈수술에
    준합니다」, and where both are performed in one operation only this amount is paid [S1]
    [S4]. Unlimited count.
    """
    return surg_open_base * sum_assured() / sa_ref                   # noqa: F821


def surg_closed_amt():
    """The 비관혈 암 수술급여금, 1,000,000 won at the 3,000만원 reference **[std]**.

    What counts as 수술 is a 수술분류표 plus a general clause, and the exclusion list is the
    operative part: 흡인, 천자, 신경 BLOCK, cosmetic and contraceptive surgery, diagnostic
    procedures including 생검 and 복강경검사, and 발정술.내고정물제거술 are excluded, while
    procedures approved by the 신의료기술평가위원회 are included [S4]. 항암방사선치료 and
    항암약물치료 are excluded too and are covered separately [R3] -- a model that paid both
    would double-count.
    """
    return surg_closed_base * sum_assured() / sa_ref                 # noqa: F821


def treat_benefit():
    """The 항암약물.방사선 치료급여금, 10,000,000 won at the 3,000만원 reference **[std]**.

    「최초 1회한」 in every retrieved contract [S1] [S4] [S5], so it is a **single indicator on
    the first treatment date** and not a stream: the definitions are anchored to a specialty
    rather than to a drug list -- 항암화학요법 or 항암면역요법 for the drug limb and 고에너지
    전리 방사선 under a 방사선종양학과 전문의 for the radiation limb -- and immune-support
    agents given with no cancer cells present (압노바, 헬릭소, 셀레나제 are named) are excluded
    [S4].
    """
    return treat_base * sum_assured() / sa_ref                       # noqa: F821


# ===== Cells: cash flows =====


def premium_factor(t):
    """The repricing factor on the 10년 갱신형 chassis flag **[std]**; 1 in the base run.

    A Korean renewal recomputes the premium at the attained age on the rate basis then in
    force, silence renewing the contract unless the policyholder objects 「보험기간 만료일
    15일전까지」 [S4 제2-11조의6]. Holding the issue rate flat records the contract-boundary
    tension rather than resolving it, which is a K-IFRS 1117 question [REG-R60] this model does
    not answer; set ``renew_reprice_rate`` above zero to step the premium at each renewal.
    """
    if chassis() != "gaengsin" or renew_reprice_rate == 0.0:         # noqa: F821
        return 1.0
    return (1.0 + renew_reprice_rate) ** (t // renewal_months)       # noqa: F821


def prem_payable(t):
    """Whether a premium falls due in month t: 1 during the 납입기간, else 0.

    Premium is payable **monthly in advance from the 보험계약일, through the 90-day 면책기간**,
    because the 유사암 tier and every non-cancer cover are already in force and because the
    invalidity rule returns the premium for the affected cover if it bites [S1] [S2] [S3]. It
    ceases at the earliest of 납입완료, death, lapse and the operation of the waiver.
    """
    return 1.0 if t < pay_months() else 0.0


def pols_payer(t):
    """The in-force policies actually paying premium at the start of month t.

    ``pols_healthy + pols_minor`` on the composite: the waiver fires on the first 일반암 or
    고액암 and 특정소액암 is excluded from it by name [S3 제14조제1항], so the 특정소액암 state
    goes on paying. ``pols_if`` on the ``waiver_trigger = "none"`` design. **Weighting the
    premium by ``pols_if`` on the composite overstates income by exactly the waived
    population**, and the error is invisible for the first three months because the two are
    equal.
    """
    if waiver_trigger() == "cancer_diag":
        return pols_healthy(t) + pols_minor(t)
    return pols_if(t)


def premiums(t):
    """Premium income at the start of month t, an inflow.

    ``P x premium_factor x pols_payer(t)`` while a premium is due. Level for the whole
    납입기간 and not varying with the policy year, the claim history or the insurer's
    experience: the contract is 무배당, so there is no dividend and no premium review on the
    비갱신형 chassis [S1] [S3] [S8] [REG-R12].
    """
    return (premium_mth_pp() * premium_factor(t) * pols_payer(t)
            * prem_payable(t) * in_force(t))


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"DIAG_GEN"``
        the 암진단자금, ``g(t) x r_general x S x diag_gen(t)`` -- 100% of the
        보험가입금액, 최초 1회한, on the first 일반암 on or after the 암보장개시일.

    ``"DIAG_HIGH"``
        the 특정 고액치료비관련 암진단자금, paid **in addition** to the general
        tier on the same event, so a 고액암 draws 200% in total [S3].

    ``"DIAG_MINOR"``
        the 특정 소액암 진단자금 at 60% of the 보험가입금액, 최초 1회한. It does
        not waive the premium.

    ``"DIAG_SIMILAR"``
        the 소액질병 진단자금 at the model point's 유사암 ratio, on the tier's own
        once-only ledger and its own start date of ``t = 0``.

    ``"HOSP"``
        the 암 직접치료 입원급여금, ``D x min(mean stay, 180) x admissions x
        pols_dur(t,k)`` summed over the six duration cohorts, so the benefit is
        weighted by how long the diagnosed have been diagnosed rather than by a
        single average.

    ``"SURGERY"``
        the 암 수술급여금, the 관혈 and 비관혈 amounts each times their own
        frequency per diagnosed life-year, unlimited count.

    ``"TREAT"``
        the 항암약물.방사선 치료급여금, ``B_tr x hazard x A(k) x pols_dur(t,k)``:
        an indicator on the **first** qualifying treatment, gated by the once-only
        ledger :func:`treat_avail`.

    ``"DEATH"``
        the **계약자적립액 at the date of death**, ``av_pp(t) x pols_death(t)``.
        This is not a death benefit -- the composite has none -- it is the payment
        감독규정 제7-63조제1항제1호 requires a 제3보험 product to make when the
        insured dies of a cause the policy does not cover [REG-R17] [REG-R25
        제22조] [REG-R50 제736조].

    ``"LAPSE"``
        the 해약환급금, ``cv_pp(t) x pols_lapse(t)``. **Identically zero for the
        whole 납입기간 on the 미지급형 base**, and zero at every duration on a
        전기납 contract on that form [S3 제41조제2항].

    ``"MATURITY"``
        zero, always. The contract ends at the 100세 계약해당일 and nothing is
        paid: there is no 만기환급금 on the 순수보장형 form and the only retrieved
        surrender-value illustration returns to nil at maturity [S8]. The kind
        exists so that the zero is stated rather than left to inference.

    **The 유사암 tier draws the lump sum and nothing continuing [std].** It generates no
    inpatient days, no surgery and no treatment benefit here, although real contracts pay those
    limbs at a reduced rate -- 20% of the daily amount on 입원일당 [S1], 25% through a separate
    limb on 항암치료비 [S4]. The direction is stated rather than hidden: it understates the
    reduced tier. Real contracts also do **not** grade uniformly, and the composite's single
    20% relativity is itself the simplification flagged in the specification.
    """
    if kind is None:
        return sum(claims(t, k) for k in (
            "DIAG_GEN", "DIAG_HIGH", "DIAG_MINOR", "DIAG_SIMILAR", "HOSP",
            "SURGERY", "TREAT", "DEATH", "LAPSE", "MATURITY"))
    if kind == "DIAG_GEN":
        return (benefit_ratio("general") * sum_assured() * reduction_factor(t)
                * diag_gen(t) * diag_module())
    if kind == "DIAG_HIGH":
        return (benefit_ratio("high") * sum_assured() * reduction_factor(t)
                * diag_high(t) * diag_module())
    if kind == "DIAG_MINOR":
        return (benefit_ratio("minor") * sum_assured() * reduction_factor(t)
                * diag_minor(t) * diag_module())
    if kind == "DIAG_SIMILAR":
        return (benefit_ratio("similar") * sum_assured() * reduction_factor(t)
                * diag_similar(t))
    if kind == "HOSP":
        if not hosp_module():
            return 0.0
        tbl = data.care_table()                                      # noqa: F821
        total = 0.0
        for k in range(1, 7):
            days = min(float(tbl.loc[k, "hosp_days_adm"]), hosp_day_cap())
            total = total + (float(tbl.loc[k, "hosp_adm_yr"]) / 12.0 * days
                             * pols_diag_dur(t, k))
        return hosp_daily() * total * in_force(t)
    if kind == "SURGERY":
        if not surg_module():
            return 0.0
        tbl = data.care_table()                                      # noqa: F821
        total = 0.0
        for k in range(1, 7):
            total = total + (
                surg_open_amt() * float(tbl.loc[k, "surg_open_yr"]) / 12.0
                + surg_closed_amt() * float(tbl.loc[k, "surg_closed_yr"]) / 12.0
            ) * pols_diag_dur(t, k)
        return total * in_force(t)
    if kind == "TREAT":
        if not treat_module():
            return 0.0
        tbl = data.care_table()                                      # noqa: F821
        total = 0.0
        for k in range(1, 7):
            total = total + (float(tbl.loc[k, "treat_hazard_yr"]) / 12.0
                             * treat_avail(k) * pols_diag_dur(t, k))
        return treat_benefit() * total * in_force(t)
    if kind == "DEATH":
        return av_pp(t) * pols_death(t)
    if kind == "LAPSE":
        return cv_pp(t) * pols_lapse(t)
    if kind == "MATURITY":
        return 0.0
    raise ValueError("invalid kind")


def pols_diag_dur(t, k):
    """The diagnosed population in duration bucket k, both states.

    The weight on all three event benefits: a 특정소액암 life is treated for cancer as a
    일반암 life is, so the care limbs run on both states while the premium waiver runs on one.
    """
    return pols_waived_dur(t, k) + pols_minor_dur(t, k)


def inflation_factor(t):
    """The expense inflation factor in month t, ``(1 + pi)^(t // 12)`` **[std]**.

    2.0% a year, stepping at each 계약해당일 rather than gliding monthly.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def maint_expenses(t):
    """e_m(t): the 계약관리비용 at the start of month t **[std]**.

    2,500 won per policy per month inflating at 2% a year, on :func:`pols_if` -- a waived
    policy is still serviced, so the expense runs on the diagnosed population with no premium
    against it. **No retrieved document quantifies any expense item for this product**: [S1]
    names 계약체결비용 and 계약관리비용 without amounts and [S8] states the surrender value is
    「계약자적립액에서 해약공제액을 공제한 금액」 without quantifying the deduction.
    """
    return expense_maint * inflation_factor(t) * pols_if(t) * in_force(t)  # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense in month t **[std]**; **not** claim handling.

    300,000 won of 계약체결비용 at ``t = 0``, then the inflating maintenance expense. The
    acquisition cost is set at or below the **표준해약공제액** of 감독규정 [별표 14]
    [REG-R20], which is the statutory ceiling on what may be deducted, and the FSC's 2019
    expense reform states the same cap as 13 months' premium for a 보장성보험 [REG-R29] --
    585,000 won at the anchor cell, which is :func:`surr_chg_cap_pp`. Claim handling is
    :func:`claim_expenses`, a separate cells with a column of its own: the library-wide split,
    so that ``expenses`` means the same thing in every model.
    """
    acq = expense_acq if t == 0 else 0.0                             # noqa: F821
    return maint_expenses(t) + acq


def claim_expenses(t):
    """The claim handling expense at the end of month t **[std]**.

    150,000 won per diagnosis of any tier and 30,000 won per cancer admission. Kept out of
    :func:`expenses` and published as its own column, because on this product the two move on
    different weights: policy servicing rides on :func:`pols_if` and claim handling on the
    diagnosis and admission counts, which are separated by a sixty-year deferral.
    """
    tbl = data.care_table()                                          # noqa: F821
    adm = 0.0
    for k in range(1, 7):
        adm = adm + float(tbl.loc[k, "hosp_adm_yr"]) / 12.0 * pols_diag_dur(t, k)
    diags = diag_gen(t) + diag_minor(t) + diag_similar(t)
    return (expense_claim_diag * diags                               # noqa: F821
            + expense_claim_hosp * adm) * in_force(t)                # noqa: F821


def commissions(t):
    """Commission outgo in month t **[std]**.

    0.6 times the annualized premium at ``t = 0`` -- 324,000 won on the anchor cell -- then 3%
    of premium income from policy year 2. The regulatory bound is real and is what the level is
    set inside: first-year remuneration may not exceed the first year's expected premium, and
    instalment structures pay no more than **60% of the 표준해약공제액** a year [REG-R22
    제4-32조제5항.제8항] [REG-R29]. No Korean commission scale for this product is public.
    """
    init = comm_init_rate * 12.0 * premium_mth_pp() if t == 0 else 0.0   # noqa: F821
    renew = (comm_renewal_rate * premiums(t)                         # noqa: F821
             if t >= comm_renewal_start else 0.0)                    # noqa: F821
    return init + renew


def net_cf(t):
    """The net cash flow of month t, **income positive**.

    Premiums less every benefit line, less :func:`expenses` (acquisition and maintenance), less
    :func:`claim_expenses` deducted explicitly, less commission. The library-wide sign, so
    there is no outgo-positive ``liability_cf`` companion to publish.

    The asymmetry that defines this product's signature is worth stating here: premiums are
    weighted by :func:`pols_payer` and the care benefits by :func:`pols_cancer`, and the two are
    disjoint, so every error in the incidence basis hits both sides of the cash flow at once.
    """
    return (premiums(t) - claims(t) - expenses(t) - claim_expenses(t)
            - commissions(t))


# ===== Cells: the 계약자적립액 and the 해약환급금 =====


def prem_alloc_pp(t):
    """The premium allocated to the 계약자적립액 in month t, per policy **[std]**.

    The **순보험료**: gross premium less a level 부가보험료 loading, being 계약체결비용 plus
    계약관리비용, for the whole 납입기간. Level rather than front-loaded, because that is what
    makes the 해약공제액 of :func:`surr_chg_pp` the recovery of *unamortised* 신계약비 rather
    than a second deduction of the same cost. Both levels are standardizations: the 약관 name
    the two cost categories and quantify **neither** [S1], so what is available is a statutory
    ceiling -- the 표준해약공제액 of [별표 14] [REG-R20] -- and the composite sets its loadings
    inside it.
    """
    load = prem_load_acq + prem_load_maint                           # noqa: F821
    return (premium_mth_pp() * premium_factor(t) * (1.0 - load)
            * prem_payable(t) * in_force(t))


def risk_prem_pp(t):
    """The month's benefit outgo per policy in force, the 위험보험료 of the account.

    Every benefit line **except** the two that are the account itself -- ``DEATH`` and
    ``LAPSE`` -- divided by :func:`pols_if`. Excluding those two is not tidiness: including
    them would make :func:`av_pp` depend on itself.
    """
    lives = pols_if(t)
    if lives <= 0.0:
        return 0.0
    total = sum(claims(t, k) for k in (
        "DIAG_GEN", "DIAG_HIGH", "DIAG_MINOR", "DIAG_SIMILAR", "HOSP",
        "SURGERY", "TREAT"))
    return total / lives


def av_pp(t):
    """V(t): the 계약자적립액 per policy at the start of month t.

    A retrospective recursion -- allocated premium less risk premium, accumulated at the
    **예정이율** -- floored at zero **[std]**, since an account cannot be negative and the
    premium here is a modelling input rather than an equivalence solution. It accrues
    **monthly before 납입완료 and daily afterwards** by regulation [REG-R19 제7-66조제1항제4호],
    which on a monthly grid is one step; 감독규정 제7-65조제2항 permits it to be computed on an
    **annualised premium** basis -- 「연납보험료를 기준으로 하여 산출할 수 있다」 -- which is
    the provision that lets a monthly-premium Korean product carry an annual account recursion
    [REG-R18].

    This is the quantity paid on death, and the reason a product with **no death benefit** none
    the less pays something when the insured dies [REG-R17] [REG-R25 제22조].
    """
    if t <= 0:
        return 0.0
    return max(0.0, (av_pp(t - 1) + prem_alloc_pp(t - 1) - risk_prem_pp(t - 1))
               * (1.0 + prem_int_rate) ** (1.0 / 12.0))              # noqa: F821


def prem_int_rate_used():
    """The 예정이율 credited to the 계약자적립액, 2.50% a year, 금리확정형 **[std]**.

    A full-text search of the 감독규정 returns **zero** occurrences of 예정이율: the regulation
    speaks only of the 계약자적립액 적용이율 and of the 금리확정형 / 금리연동형 distinction
    [REG-R9] [REG-R48]. The 예정이율 of a specific Korean product is therefore not a published
    number for any product in this library. The anchor is the **평균공시이율**, which *is* a
    regulatory figure computed by the FSS Governor and which stands at 2.50% for 2026, down
    from 2.75% and its first fall since the 2.50% -> 2.25% cut that took effect for 2021
    [REG-R48]. The observed bracket is wide and both
    ends are recorded: one non-life product credits its 계약자적립액 at 「연복리 1.5%」 [S8],
    another the 공시이율 with a 최저보증이율 of 「연단위 복리 0.5%」 [S1].
    """
    return prem_int_rate                                             # noqa: F821


def surr_chg_months():
    """The 해약공제기간 in months: the 납입기간 or 7 years, whichever is shorter.

    감독규정 제7-66조제1항제2호 caps it at the shorter of the 납입기간, the 신계약비 부가기간
    and **seven years** [REG-R19]. 84 months on the anchor cell.
    """
    return 12 * min(max(pay_months() // 12, 1), surr_chg_period_y)   # noqa: F821


def surr_chg_cap_pp():
    """alpha_cap: the **표준해약공제액**, the statutory ceiling on the surrender charge.

    감독규정 [별표 14] states it as a formula and every input comes from a different note
    [REG-R20]::

        표준해약공제액 = 연납순보험료 x 5% x 해약공제계수 + 보험가입금액 x 10/1000

    **해약공제계수** for a 보장성보험 is 「보험기간(최대 20년)」, so 20 on a sixty-year term.
    **보험가입금액** is where the Korea-specific mechanic bites, because this product has no
    death benefit at all: [별표 15] 제3호 covers only 일반사망을 보장하는 보장성보험, so the
    product falls into **제9호** -- 보험가입금액 = (위험보험료 / 정기보험의 위험보험료) x
    정기보험의 보험가입금액 -- computed at the 기준연령 요건, 남자 만 40세, 전기납, 월납, which
    is this specification's own anchor cell [REG-R21] [REG-R9]. **The 3,000만원 headline is
    therefore not the 보험가입금액 that enters [별표 14]**; ``notional_sa_ratio`` is the
    **[std]** 60% that stands in for it, and the whole is capped by the FSC's 2019 statement of
    the same ceiling as **13 months' premium for a 보장성보험** [REG-R29]. That cap binds at
    the anchor cell, giving 585,000 won.

    ``LTC_KR_S`` and ``Child_KR_S`` inherit the mechanic, with the difference that 제9호's
    third bullet excludes long-term-care risk premium from the ratio [REG-R21].
    """
    ann_net = 12.0 * premium_mth_pp() * (1.0 - prem_load_acq         # noqa: F821
                                         - prem_load_maint)          # noqa: F821
    formula = (ann_net * 0.05 * surr_chg_coef                        # noqa: F821
               + sum_assured() * notional_sa_ratio * 0.01)           # noqa: F821
    return min(formula, surr_chg_cap_months * premium_mth_pp())      # noqa: F821


def surr_chg_pp(t):
    """alpha(t): the 해약공제액 actually deducted in month t, running off straight-line.

    Full at issue and nil at the end of the 해약공제기간 **[std]**: [별표 14] states the cap
    and not its run-off shape, and no retrieved document gives one [REG-R20].
    """
    n = surr_chg_months()
    return surr_chg_cap_pp() * max(0.0, 1.0 - t / n)


def cv_std_pp(t):
    """CV_std(t): the **표준형** 해약환급금, ``max(av_pp - surr_chg_pp, 0)``.

    감독규정 제7-66조제1항제1호, with the negative case floored at zero rather than carried
    [REG-R19]. On this product it is a comparator that **cannot be bought**: 「'표준형'은
    보험료 및 해약환급금(환급률 포함)의 비교 안내만을 위한 상품으로 가입이 불가능하며」, and it
    is computed 「해지율을 적용하지 않고」 [S3 제41조] -- the clearest retrieved statement of
    why the 무해지 lapse assumption is a supervisory issue [REG-R27].
    """
    return max(av_pp(t) - surr_chg_pp(t), 0.0)


def cv_pp(t):
    """CV(t): the 해약환급금 actually payable in month t, per policy.

    On the **미지급형** base: 「해약환급금 미지급형(납입기간중 0%, 납입기간후 50%)」, and 「전기납
    계약의 경우에는 해약환급금을 지급하지 않습니다」 [S3 제41조제2항]. So the profile is a
    **cliff at a known date** rather than a curve, the date being 「계약일로부터 보험료
    납입기간이 경과하여 최초로 도래하는 계약해당일 전일까지의 기간」 [S3]. On the 표준형 switch
    it is :func:`cv_std_pp` itself.

    The caveat worth carrying: on a 순수보장성 cancer contract there is not much 계약자적립액 to
    suppress. The one retrieved illustration shows 환급률 of 0.0% at year 1, 21.6% at year 5
    and **0.0% at maturity** [S8] -- a pure-protection signature rather than a savings one --
    so the 환급률 floor of 제7-66조제4항제2호, which requires the post-payment 환급률 to exceed
    100%, binds **weakly** on a product whose 표준형 환급률 never approaches it [REG-R19].
    """
    if cv_form() == "pyojun":
        return cv_std_pp(t)
    if pay_term() == 0:
        return 0.0
    if t < pay_months():
        return cv_floor_ratio * cv_std_pp(t)                         # noqa: F821
    return cv_post_pay_ratio * cv_std_pp(t)                          # noqa: F821


# ===== Cells: roll-forward and ledger checks =====


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - deaths - lapses - maturities``. There is no benefit-driven
    termination to add: paying a diagnosis benefit neither ends nor exhausts the contract [S1]
    [S3] [S4], so a life leaves only by dying, by lapsing or by reaching the 100세 계약해당일. A
    diagnosis cancels out of this identity because it moves a life between states rather than
    out of the book.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month."""
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return all(abs(check_pols_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_cancer_roll_fwd_resid(t):
    """The diagnosed-state roll-forward residual in month t; zero everywhere.

    ``pols_cancer(t+1)`` against the exposures of month ``t`` carried forward on each cohort's
    own survival factor. Every duration bucket carries a graduation term of opposite sign to
    its neighbour's, so their sum must telescope to this one line: a sign slip or an off-by-one
    in the twelve-month delay shows up here and nowhere else in the in-force figures.
    """
    built = 0.0
    for k in range(1, 7):
        built = built + pols_waived_exp(t, k) * surv_waived(t, k)
        built = built + pols_minor_exp(t, k) * surv_minor(t, k)
    return pols_cancer(t + 1) - built


def check_cancer_roll_fwd():
    """True when the diagnosed-state roll-forward closes in every projected month."""
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return all(abs(check_cancer_roll_fwd_resid(t)) <= tol
               for t in range(proj_len() - 1))


def check_canc_dur_ledger_resid(t):
    """The first duration cohort's residual in month t; zero everywhere.

    Both diagnosed states' bucket 1 rebuilt **independently of their recursions**, straight off
    the entry history: the diagnoses of the previous twelve months, each carried forward on that
    bucket's own survival factors. The recursions reach the same figure through
    :func:`waived_grad` and :func:`minor_grad`, so a delay released a month early or late, or a
    cohort carried forward on the wrong bucket's hazard, fails here while every aggregate still
    adds up.
    """
    resid = 0.0
    for entry, surv, dur in ((diag_gen, surv_waived, pols_waived_dur),
                             (diag_minor, surv_minor, pols_minor_dur)):
        built = 0.0
        factor = 1.0
        for s in range(t - 1, max(t - 13, -1), -1):
            factor = factor * surv(s, 1)
            built = built + entry(s) * factor
        resid = resid + dur(t, 1) - built
    return resid


def check_canc_dur_ledger():
    """True when both first duration cohorts rebuild exactly in every projected month."""
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return all(abs(check_canc_dur_ledger_resid(t)) <= tol
               for t in range(proj_len()))


def check_similar_ledger_resid(t):
    """The once-only 유사암 ledger residual in month t; zero everywhere.

    ``similar_avail(t) + similar_used(t) - 1``. :func:`similar_used` is accumulated off the
    published claim line rather than off the ledger recursion, so the identity fails if the
    benefit is paid at a rate the ledger is not decremented by -- which is exactly what
    implementing the tier as a share of the main diagnosis benefit would do.
    """
    return similar_avail(t) + similar_used(t) - 1.0


def check_similar_ledger():
    """True when the once-only 유사암 ledger closes in every month it is observable in.

    The identity is read off the claim line, so it says nothing in months where no policy is in
    force. Those months carry no information and are excluded rather than papered over.
    """
    return all(abs(check_similar_ledger_resid(t)) <= roll_fwd_tol    # noqa: F821
               for t in range(proj_len()) if pols_if(t) > 0.0)


def check_treat_ledger_resid(t):
    """The 최초 1회한 treatment ledger's excursion past 1 in month t; zero everywhere.

    ``max(0, treat_cum_pp(t) - 1)``. The 항암약물.방사선 치료급여금 is payable once ever [S1]
    [S4] [S5], so the cumulative payment probability of a single diagnosed life must never pass
    one however long it survives -- which is the property the zero ultimate hazard of
    *care_table.csv* is what secures.
    """
    return max(0.0, treat_cum_pp(t) - 1.0)


def check_treat_ledger():
    """True when the once-only treatment ledger stays inside its cap in every month."""
    return all(abs(check_treat_ledger_resid(t)) <= roll_fwd_tol      # noqa: F821
               for t in range(proj_len()))


def check_tier_shares_resid(t):
    """The tier decomposition residual at month t; zero everywhere.

    Three properties in one line. The 일반암 and 특정소액암 monthly rates must sum to the base
    rate, because the two shares **partition** it; the 고액암 rate must not exceed the 일반암
    rate, because the tier is a **subset** of it and pays on top; and the 유사암 rate must be
    non-negative, because it is **additive** and outside the base rate's definition. Getting
    any of the three wrong is silent -- the projection runs and the answer is simply wrong by
    the size of a tier.
    """
    part = (inc_rate_gen_mth(t) + inc_rate_minor_mth(t)
            - inc_rate(t) / 12.0)
    subset = max(0.0, inc_rate_high_mth(t) - inc_rate_gen_mth(t))
    additive = min(0.0, inc_rate_similar_mth(t))
    return part + subset + additive


def check_tier_shares():
    """True when the tier decomposition holds at every projected age."""
    return all(abs(check_tier_shares_resid(t)) <= roll_fwd_tol       # noqa: F821
               for t in range(proj_len()))


def check_waiting_period_resid(t):
    """Invasive-tier benefit paid inside the 면책기간 in month t; zero everywhere.

    The 90 days is a **hard zero** and not a reduced rate, so the three invasive diagnosis
    benefits and every transition out of the healthy state must be exactly nil before the
    암보장개시일. The 유사암 tier is deliberately **not** in this sum: it has no waiting period
    at all [S1] [S2] [S7], and a check that asserted a zero there would be asserting the wrong
    product.
    """
    if t >= tier_wait_months("general"):
        return 0.0
    return (claims(t, "DIAG_GEN") + claims(t, "DIAG_HIGH")
            + claims(t, "DIAG_MINOR") + diag_first(t))


def check_waiting_period():
    """True when nothing invasive is paid or transitioned inside the 면책기간."""
    return all(abs(check_waiting_period_resid(t)) <= roll_fwd_tol    # noqa: F821
               for t in range(proj_len()))


def check_cv_floor_resid(t):
    """The 해약환급금's excursion outside its regulatory and contractual bounds; zero.

    Three bounds in one line: the value is non-negative, it never exceeds the 표준형 value of
    감독규정 제7-66조제1항제1호 [REG-R19], and on the 미지급형 form it is **exactly nil for the
    whole 납입기간** [S3 제41조제2항]. The third is the one that would break silently: a model
    that let a suppressed-surrender-value contract pay a surrender value during the payment
    period would be modelling a 표준형 product under a 무해지 premium.
    """
    resid = min(0.0, cv_pp(t)) + max(0.0, cv_pp(t) - cv_std_pp(t))
    if cv_form() == "mijigeup" and t < pay_months():
        resid = resid + cv_pp(t)
    return resid


def check_cv_floor():
    """True when the 해약환급금 stays inside its bounds in every projected month."""
    tol = roll_fwd_tol * max(sum_assured(), 1.0)                     # noqa: F821
    return all(abs(check_cv_floor_resid(t)) <= tol
               for t in range(proj_len()))


def check_net_cf_resid(t):
    """The published cash-flow statement's residual in month t; zero everywhere.

    Rebuilds ``net_cf`` from the columns of :func:`result_cf` rather than from :func:`net_cf`,
    so a column wired to the wrong cells, a benefit line dropped from the table or a
    double-counted claim expense shows up as a non-zero residual in the very table a reader is
    looking at. The benefit side is every column whose name begins ``claims_``, taken as a
    group rather than enumerated: :func:`result_cf` publishes the ten splits and **no bare
    ``claims`` subtotal beside them**, so the columns of the table sum to ``net_cf`` without a
    reader having to know which of them to skip.
    """
    row = result_cf().loc[t]
    outgo = sum(row[c] for c in row.index if str(c).startswith("claims_"))
    return (row["premiums"] - outgo - row["expenses"] - row["claim_expenses"]
            - row["commissions"] - row["net_cf"])


def check_net_cf():
    """True when the published cash flow statement adds up in every projected month."""
    tol = roll_fwd_tol * max(sum_assured(), 1.0)                     # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(proj_len()))


def check_hosp_cap_resid(t):
    """The inpatient benefit's excursion past the 180-day per-stay cap; zero everywhere.

    The largest mean stay in *care_table.csv* against :func:`hosp_day_cap`. The cap is a
    contractual term and it does **not** bind on a deterministic mean stay, which is a
    statement worth making in code rather than leaving a reader to discover: on a stochastic
    model of the same product it would bind on the tail, and the difference is a property of
    the model rather than of the contract.
    """
    tbl = data.care_table()                                          # noqa: F821
    return max(0.0, max(float(tbl.loc[k, "hosp_days_adm"])
                        for k in range(1, 7)) - hosp_day_cap()) * in_force(t)


def check_hosp_cap():
    """True when no cohort's mean stay passes the 180-day per-stay cap."""
    return all(abs(check_hosp_cap_resid(t)) <= roll_fwd_tol          # noqa: F821
               for t in range(proj_len()))


# ===== Cells: result tables =====


def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is the start-of-month count and the weight on ``expenses`` of the same row --
    but *not* on ``premiums``, which is carried by ``pols_healthy`` plus ``pols_minor``, nor on
    the benefit lines, three of which are carried by the diagnosed cohorts. Publishing the four
    counts side by side is what makes that asymmetry visible in the table itself.

    ``expenses`` is acquisition plus maintenance and ``claim_expenses`` the claim handling cost,
    in two columns rather than one: the library-wide split, and on this product the two move on
    weights separated by a sixty-year deferral.

    ``net_cf`` carries the library's income-positive sign. ``claims_maturity`` is a column of
    zeros by product design -- nothing is paid at the 100세 계약해당일 -- and ``claims_lapse``
    is identically zero for the whole 납입기간 on the 미지급형 base; both are published rather
    than dropped. There is **no ``claims_death`` in the ordinary sense**: that column is the
    계약자적립액 released on death, which a 제3보험 product must pay although it carries no
    death benefit [REG-R17].

    The ten benefit lines are published as splits and **no bare ``claims`` subtotal beside
    them**, so the table's columns add to ``net_cf`` as they stand. The :func:`claims` cells
    still returns the total when its ``kind`` argument is omitted; it is the *column* that is
    not published. :func:`check_net_cf` asserts the identity off this table in every projected
    month.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_healthy": [pols_healthy(t) for t in ts],
            "pols_minor": [pols_minor(t) for t in ts],
            "pols_waived": [pols_waived(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_diag_gen": [claims(t, "DIAG_GEN") for t in ts],
            "claims_diag_high": [claims(t, "DIAG_HIGH") for t in ts],
            "claims_diag_minor": [claims(t, "DIAG_MINOR") for t in ts],
            "claims_diag_similar": [claims(t, "DIAG_SIMILAR") for t in ts],
            "claims_hosp": [claims(t, "HOSP") for t in ts],
            "claims_surgery": [claims(t, "SURGERY") for t in ts],
            "claims_treat": [claims(t, "TREAT") for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts, decrement rates and ledgers, indexed by month t."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_healthy": [pols_healthy(t) for t in ts],
            "pols_minor": [pols_minor(t) for t in ts],
            "pols_waived": [pols_waived(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "diag_gen": [diag_gen(t) for t in ts],
            "diag_high": [diag_high(t) for t in ts],
            "diag_minor": [diag_minor(t) for t in ts],
            "diag_similar": [diag_similar(t) for t in ts],
            "similar_avail": [similar_avail(t) for t in ts],
            "inc_rate": [inc_rate(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "cv_std_pp": [cv_std_pp(t) for t in ts],
            "surr_chg_pp": [surr_chg_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 1.0

inc_be_factor = 1.0

void_adjust = False

lapse_canc_factor = 1.0

renew_reprice_rate = 0.0

renewal_months = 120

sa_ref = 30000000.0

hosp_daily_base = 50000.0

hosp_day_cap_days = 180

surg_open_base = 5000000.0

surg_closed_base = 1000000.0

treat_base = 10000000.0

prem_int_rate = 0.025

prem_load_acq = 0.10

prem_load_maint = 0.05

surr_chg_period_y = 7

surr_chg_coef = 20.0

surr_chg_cap_months = 13.0

notional_sa_ratio = 0.60

cv_floor_ratio = 0.0

cv_post_pay_ratio = 0.5

expense_acq = 300000.0

expense_maint = 2500.0

expense_claim_diag = 150000.0

expense_claim_hosp = 30000.0

inflation_rate = 0.02

comm_init_rate = 0.6

comm_renewal_rate = 0.03

comm_renewal_start = 12

roll_fwd_tol = 1e-10

math = ("Module", "math")

pd = ("Module", "pandas")
