# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Medical_KR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 8            # or switch the default

``t`` counts **policy months**, 0-based: ``t = 0`` is the first policy month and
``t = proj_len() - 1`` the last, so the frame is ``range(proj_len())`` and
``result_cf()`` has ``proj_len()`` rows — ``proj_len()`` is the **number** of projected
months, the exclusive end of the frame, and not the last index. Month ``t`` is the
interval from ``t`` to ``t + 1`` months after the 계약일. The **policy year**
``y = policy_year(t) = t // 12 + 1`` is a contractual 1-based label and keeps its own
clock: it is derived from ``t``, never indexed by it.

.. rubric:: Age basis

The projection is on **만나이** (*man nai*, age last birthday), incremented at each
policy anniversary. The **contract** is not: it prices and renews on **보험나이**
(*boheom nai*, insurance age), the 만나이 at the 계약일 with a fraction under six months
discarded and six months or more rounded up, and the 표준약관 works the arithmetic out
in its own example. The model carries 만나이 because every calibration statistic
available for this product — the NHIS coverage ratios by age band, the 국가데이터처
생명표 mortality decrement and the 금융감독원 premium series — is compiled on 만나이,
and because a deterministic single-cell projection cannot represent the distribution of
issue dates within the year that separates the two conventions. The two differ for half
of all issue dates, so the difference is a half-year of age on average, and it is
recorded here rather than silently absorbed.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/indemnity_medical/``, read at run time rather than stored inside the model.
The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Medical_KR_S.Data`, reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
mort_table_file         data.mort_table()                   mort_table.csv
lapse_table_file        data.lapse_table()                  lapse_table.csv
utilisation_table_file  data.utilisation_table()            utilisation_table.csv
severity_table_file     data.severity_table()               severity_table.csv
claim_shape_file        data.claim_shape_table()            claim_shape_table.csv
oop_ceiling_file        data.oop_ceiling_table()            oop_ceiling_table.csv
======================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
annual rates with ``*_rate_mth`` for their monthly companions, ``*_pp`` for per-policy
amounts, ``claims(t, kind)`` with an uppercase ``kind`` string, ``pols_if_at(t, timing)``
for the within-month in-force reads. Quantities that live on the **policy year** rather
than the policy month take ``y`` and never ``t``, because the two are different clocks
and this product runs on both. The technical notes use compact symbols instead. The
mapping is:

=========================  ==============================  ===========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ===========================
(model point row)          model_point()                   The selected model point
x                          issue_age()                     가입나이, 만나이 at 계약일
age(t)                     age(t)                          Attained 만나이 in month t
y(t)                       policy_year(t)                  floor(t/12) + 1
(none)                     sex()                           M or F
proj_len                   proj_len()                      Number of projected months
P0                         premium_mth_pp()                First-year office premium
s                          np_share()                      비급여 share of the premium
(switch)                   np_rider()                      비급여 특약 held
(switch)                   three_np()                      3대비급여형 held
L                          annual_limit()                  연간 보험가입금액 per 보장종목
Lv                         visit_cap()                     통원 1회당 한도
(decile)                   oop_decile()                    본인부담상한제 소득분위
(mix)                      clinic_share()                  Clinic-tier share of 급여 통원
(switch)                   nhi_covered()                   Inside 국민건강보험 or not
k_trend                    trend_mult()                    Multiplier on the cost trend
k_util                     util_mult()                     Multiplier on the frequencies
(switch)                   reld_on()                       요율 상대도 in operation
(switch)                   noclaim_on()                    무사고 할인 in operation
(rate)                     suspend_rate()                  개인실손 중지 decrement
(table)                    mort_rate(t)                    Annual 만나이 mortality
q(t)                       mort_rate_mth(t)                Monthly mortality in month t
(table)                    lapse_rate(t)                   Annual lapse rate, policy year
w(t)                       lapse_rate_mth(t)               Monthly lapse in month t
(rate)                     suspend_rate_mth(t)             Monthly 중지 decrement
d_ren(t)                   renewal_decline(t)              Decline of the annual renewal
l(t)                       pols_if(t)                      In force at the start of t
l(t)(1-q), l(t+1)          pols_if_at(t, timing)           Within-month in-force reads
(none)                     pols_death(t)                   Deaths in month t
(none)                     pols_lapse(t)                   Lapses in month t
(none)                     pols_suspend(t)                 개인실손 중지 in month t
(none)                     pols_renewal_decline(t)         Renewals declined in month t
(none)                     pols_maturity(t)                Cover ending at the horizon
b(y)                       util_band(y)                    Five-year utilisation band
n_adm(y)                   adm_rate(y)                     Admissions a year per policy
n_ge(y)                    visit_rate_ge(y)                급여 통원 visits a year
n_np(y)                    visit_rate_np(y)                비급여 통원 visits a year
a_ph, a_in, a_mr           act_rate_physio/inject/mri(y)   3대비급여 acts a year
D(y)                       los_days(y)                     Mean days per admission
f_ge(y), f_np(y)           trend_ge(y), trend_np(y)        Cost trend from year 1
r_ge, r_np                 retain_rate_ge/np()             자기부담률, 20% / 30% / 60%
(table)                    sev_points(stream)              Cost-probability pairs
C_ge(y)                    oop_incurred_ge(y)              급여 본인부담금 incurred
S(decile)                  oop_ceiling()                   본인부담상한액
tau(y)                     oop_trunc(y)                    본인부담상한제 truncation
(loss)                     loss_incurred_pp(y)             보장대상 의료비 incurred
paid_in(y)                 claims_ge_in_pp(y)              급여 입원, before the limit
paid_out(y)                claims_ge_out_pp(y)             급여 통원, before the limit
(limit)                    ge_limit_factor(y)              급여 annual-limit factor
(sum)                      claims_ge_pp(y)                 급여 claim after the limit
paid_np_in(y)              claims_np_in_pp(y)              비급여 입원 incl 상급병실료
paid_np_out(y)             claims_np_out_pp(y)             비급여 통원 incl the carve-out
(limit)                    np_limit_factor(y)              비급여 annual-limit factor
(sum)                      claims_np_main_pp(y)            비급여 main after the limit
a_ph_eff, a_in_eff         acts_physio_eff/inject_eff(y)   Acts after the gates
paid_3(y)                  claims_np_three_pp(y)           3대비급여 after its sub-limits
(sum)                      claims_np_pp(y)                 All rider claims
C(y)                       claims_np_rated_pp(y)           Rated 비급여 claim, exemptions out
(table)                    shape_mean(), shape_rel(k)      The claim-shape distribution
band(a)                    band_of(a)                      요율 상대도 band of an amount
w_b(y)                     band_share(y, b)                Share of contracts in band b
r_b                        band_relativity(b)              100 / 200 / 300 / 400%
Sum w_b r_b (b>=2)         reld_surcharge(y)               The surcharge pool
r_1 solved                 reld_solved(y)                  Revenue-neutral band-1 factor
r_1                        reld_one(y)                     After the discount cap
Sum w_b r_b                reld_avg(y)                     Average relativity applied
(switch)                   reld_active(y)                  Whether the loop is running
nc(y)                      noclaim_share(y)                Share earning the 10% discount
a                          age_load                        4.0% age loading at renewal
b_ge, b_np                 basis_incr_ge/np()              Basis change, in the corridor
base_ge(y)                 prem_ge_base(y)                 급여 기준보험료 a month
base_np(y)                 prem_np_base(y)                 비급여 기준보험료 a month
gross(y)                   prem_gross_mth(y)               Office premium a month
P l(t)                     premiums(t)                     Premium income
claims_*(t)                claims(t, kind)                 Benefit outgo by kind
claims(t)                  claims(t)                       All benefit outgo
e(t)                       expenses(t)                     Maintenance expense
ec(t)                      claim_expenses(t)               Claim handling, on its own line
comm(t)                    commissions(t)                  Commission outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
=========================  ==============================  ===========================

.. rubric:: The reimbursement machinery, in the order it must be applied

Everything in this product is a rule for reducing an incurred cost to a payable amount,
and the order matters. Getting it wrong is the classic implementation failure here.

**1 — the 본인부담상한제 first, as an exclusion from covered loss.** The NHIS refunds a
member's annual 본인일부부담금 above an income-graded ceiling, and the 표준약관 excludes
anything so refundable from cover twice over. :func:`oop_trunc` is the deterministic
representation: the year's incurred 급여 본인부담금 is scaled to the ceiling when it
would otherwise exceed it. Two refinements a careful reader should know are deliberate
simplifications: the ceiling runs on the **calendar** year while every contractual limit
runs on the **policy** year, and a proportional truncation of an expectation is not the
same thing as truncating each realisation.

**2 — the co-payment and the deductible, per event.** Inpatient reimbursement is a flat
percentage of the covered cost — 80% on the 급여 side, 70% on the 비급여 side, 40% on
either where 국민건강보험 entitlement does not apply. Outpatient reimbursement is the
cost less ``max(flat floor, 자기부담률 x cost)``, then capped per visit. The flat floor
is ₩10,000 at the clinic tier and ₩20,000 at the hospital tier on the 급여 side and a
flat ₩30,000 at every provider on the 비급여 side, which is why the 급여 side needs a
provider mix and the 비급여 side does not. The shape matters more than the formula: at
the clinic tier the deductible is ₩10,000 until the covered cost reaches ₩50,000 and 20%
above it, so a ₩10,000 visit pays nothing, a ₩50,000 visit pays ₩40,000, and the
₩200,000 per-visit cap binds at a covered cost of ₩250,000. **Applying the deductible to
the mean cost instead of to the distribution removes the kink and overstates the claim.**

**3 — the ₩2,000,000 annual inpatient co-payment cap, on what remains.** Where the 20%
retained on inpatient 급여 treatment exceeds ₩2,000,000 in a policy year, the excess is
reimbursed. It applies to inpatient treatment only; there is no annual cap on the
outpatient deductible.

**4 — the 3대비급여 sub-limits, which displace the main limit for their three classes.**
도수·체외충격파·증식치료 share one 50-act counter and a ₩3,500,000 money limit;
주사료 has its own 50 acts and ₩2,500,000; MRI has ₩3,000,000 and no count limit. Both
gates are hard and neither is pro-rated: the limit that binds first stops cover for the
rest of the policy year and only the 계약해당일 restores it. Cover beyond the first ten
physical-therapy acts is conditional on a documented clinical re-assessment every ten
acts, which a projection can only represent as a continuation probability at the
boundary. Non-covered injections of 항암제, 항생제 and 희귀의약품 leave the ₩2,500,000
sub-limit and are reimbursed inside the main 비급여 limit, so the sub-limit bites on the
discretionary end of injection use and not on oncology.

**5 — the annual aggregate, per 보장종목 and per policy year.** 상해 and 질병 carry
separate ₩50,000,000 limits on each of the two parts, so the whole-contract annual
exposure is ₩100,000,000 in the ordinary reading. The split between the two 보장종목 is
[std]; nothing published gives it.

A word on what a deterministic projection can and cannot say about the limits.
``E[min(X, L)] != min(E[X], L)``, so a projection that applies a limit to an expectation
**understates** the limit's bite by ignoring dispersion. On every shipped model point the
₩2,000,000 inpatient cap, the three 3대비급여 money limits, the two 50-act counters, the
100-visit cap and the ₩50,000,000 annual limits do **not** bind, because the expected
annual claim of a single cell is two orders of magnitude below them — the supervisor's
own tail figure is that 0.005% of insureds took more than ₩50,000,000 in 2019. The
machinery is implemented anyway, because it binds under any seriatim or stochastic run
and because :func:`check_annual_limits` is what proves it is wired correctly. The one
limit that **does** bind on a shipped model point is the 본인부담상한제 truncation, on
model point 8, whose high-utilisation cell sits on the lowest 본인부담상한액 decile.

.. rubric:: 비급여 할인·할증 — the loop, and why it is a distribution and not a rate

**This is the mechanism that makes the contract unlike anything else in this
repository.** The renewal premium of the 비급여 rider is a function of the individual
policyholder's own prior-year non-covered claim amount, through five bands:
1단계 (no claim) at a solved discount, 2단계 (up to ₩1,000,000) at 100%, and 3단계,
4단계 and 5단계 at 200%, 300% and 400% as the prior-year claim crosses ₩1,000,000,
₩1,500,000 and ₩3,000,000. A hard floor sits under the surcharge: below ₩1,000,000 of
prior-year claims there is no surcharge at all, which is why 2단계 is exactly 100%.
Claims arising from a 국민건강보험법 산정특례 condition, and all claims of an insured
graded 장기요양 1등급 or 2등급, are struck out of the count — the severely ill are
exempt from the experience rating, which is the only direct statutory cross-reference
between this model and ``LTC_KR_S``.

**The band is memoryless.** It depends on the claim experience of the previous year
alone: a single bad year cannot compound into a permanently higher premium and a single
clean year returns the policyholder to the discount band. There is therefore no
no-claims ladder and no Markov chain to carry — the band distribution at renewal ``y`` is
simply the distribution of the annual rated claim in year ``y - 1``, which is what
:func:`band_share` computes from :func:`~.Medical_KR_S.Data.claim_shape_table` rescaled to that year's mean.
The loop is nonetheless live, and visibly so: the thresholds are **fixed money amounts**
while the claim level trends, so contracts migrate into the surcharge bands year by year
without anything in the model changing.

**The discount is solved, not set.** The wording defines it as the solution to a
revenue-neutrality constraint — the surcharge funds the discount, so that the rider
collects the same net premium before and after the relativity is applied. Writing
``w_b`` for the share of rider net premium in band ``b``, neutrality is
``Sum_b w_b r_b = 1``, hence ``r_1 = (1 - Sum_{b>=2} w_b r_b) / w_1``. On the
commencement band distribution that gives ``r_1 = 0.698 / 0.729 = 0.9575``, a **4.25%**
discount, against a published 잠정 figure of 5%. Solving rather than hard-coding is the
deliberate choice, and :func:`check_relativity_neutral` is the identity that proves it.
A **[std]** cap of 5% sits under the discount, from the two published values; once the
claim level has trended far enough that the surcharge pool would fund more than 5%, the
cap binds, the scheme stops being neutral and the average rider premium rises above the
base. That is the loop reaching the aggregate, and it is a feature of the design rather
than of this implementation.

Two things run alongside and are different animals. The **무사고 할인** takes 10% off
the **whole** office premium — 급여 and 비급여 together — after two consecutive years
with no 비급여 claim, where the relativity has a one-year lookback and touches only the
rider; the two stack. And the relativity was **deferred three years** after launch, so it
starts at the fourth policy year, which is why the first three renewals of the anchor
cell are a plain attained-age re-rate.

.. rubric:: 1년 갱신 — the renewal recursion and its corridor

The policy term is one year and renews automatically. The premium re-rates on everything:
the attained age, the basis, and — on the rider only — the experience relativity. The
recursion is

    base(y) = base(y-1) x (1 + a) x (1 + b(y)),   a = 0.04,  abs(b(y)) <= 0.25

and the order of operations is the thing a careless reading gets wrong. The 표준약관's
own illustration labels its basis increment 「전년도 기준보험료 x 25%」, but 3,640 is 25%
of 14,560 = 14,000 x 1.04, not of 14,000: **the corridor applies to the age-adjusted
prior premium**, and reproducing the illustration's printed row 14,000 -> 18,200 ->
23,660 -> 30,758 -> 39,985 -> 51,980 requires it. Getting it wrong costs 4% of the
corridor every year and compounds. The corridor binds **per 위험구분단위**, not on the
portfolio average, which is why the two units are re-rated separately here and
:func:`check_renewal_corridor` tests each of them.

``b(y)`` is not an input. Each priced unit is re-rated at **its own** claim trend,
clipped to the corridor: the 급여 unit at the growth of the statutory co-payment and the
비급여 unit at the growth of non-covered spend, which the public statistician measures at
1.0% and 8.1% respectively. That is a **[std]** re-rating rule and it is what keeps the
two halves of the model internally consistent — the loss ratio of each unit is stable
unless the corridor clips it, which is exactly what happens on model point 10.

.. rubric:: Modules that are off in the base run

- **개인실손 중지·재개**, the suspension facility for a policyholder doubly covered by a
  단체실손, which 감독규정 제7-63조제2항제7호 makes mandatory. Carried as a decrement
  with ``suspend_rate = 0`` on every model point but 9. Resumption is not modelled: the
  contract that resumes is a different projection.
- **The 40% branch**, where 국민건강보험 entitlement does not apply. ``nhi_covered = 0``
  on model point 10 raises the 자기부담률 to 60% on both parts and switches the
  본인부담상한제 off, because a life outside the scheme is not refunded by it.
- **The experience relativity and the 무사고 할인**, both switchable and both off on
  model points 5 and 9. With the relativity off the contract is a plain attained-age
  renewable, which is what 1세대 through 3세대 were.

.. rubric:: What is *not* modelled, and is a limitation rather than an omission

**The behavioural response to the experience rating.** The supervisor's own worked
example has a policyholder cutting his claims by 93% in response to a surcharge — from
₩10,000,000 to ₩700,000 — and shows him saving ₩300,000 of premium and ₩2,700,000 of
out-of-pocket cost in one year. The contract is *designed* to change the insured's
behaviour, and this model projects the loop on a fixed frequency basis: it models the
premium's response to claims and not the claims' response to premium.

**The frequency half of the claim distribution.** :func:`~.Medical_KR_S.Data.claim_shape_table` trends its
amounts and holds its zero-claim mass fixed, so the proportion of contracts with no rated
claim is constant at 72.9% while the size of a claim grows with age and cost. In reality
the frequency of claiming rises with age too, and the 1단계 share would fall.

**Anything a measurement basis would add.** No 책임준비금, no CSM, no risk adjustment, no
K-ICS requirement, no 해약환급금준비금 and no policyholder tax. On a one-year indemnity
contract the 잔여보장요소 is at most one year's unearned premium and the 발생사고요소 is
the material item, and the 해약환급금준비금 has nothing to bite on because there is no
surrender value at all.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — premiums less claims, less maintenance expense,
less claim handling expense, less commission — which is the library-wide sign and the
notes' own, so unlike the whole life and payout annuity models there is no
outgo-positive ``liability_cf`` companion to publish: one stream, one sign, one name.

.. rubric:: Three absences that are product facts

There is **no death benefit**: on death from a non-covered cause the contract pays the
계약자적립액 and the 미경과보험료, and on a one-year pure protection contract the
계약자적립액 is nil, so mortality is a pure liability-releasing decrement and no
``claims_death`` exists. There is **no surrender value**: 「이 상품은 1년만기 순수보장성
상품으로 해약환급금이 발생하지 않습니다」, so there is no ``cv_pp``, no
``claims_lapse``, no 보험계약대출 and no 보험료 자동대출납입 to break a missed premium.
And there is **no waiting period** on the general cover, which is unusual among Korean
health products and is a direct consequence of the indemnity form: there is no lump sum
to anti-select against.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells
# --- Model point attributes ------------------------------------------------

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def sex():
    """The sex, M or F.  A rating factor at every carrier.

    The 손해보험협회 comparison tool is filtered by 성별 and 보험나이 and by nothing
    else, which is the disclosure's own confirmation that the rate scale is an age x sex
    table [S7].  The scale itself is not public, so the sex effect reaches this model
    through the **[std]** utilisation factors rather than through a premium table.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """x: the 가입나이 on a **만나이** basis, 0 to 65 **[std]**.

    Nothing was retrieved for 4세대 or 5세대: the 표준약관 sets no issue age, it is a
    사업방법서 matter and the 사업방법서 is not published [REG-R2].  The only observed
    range is 0-49 on one direct-channel 2세대 product [S4].  The composite takes 0-65,
    a whole-of-working-life envelope that stays clear of the 노후실손 boundary at 75
    [REG-R17 제7-63조제2항제6호다목].  This is the widest single **[std]** in the
    specification.
    """
    return int(model_point()["issue_age"])


def premium_mth_pp():
    """P0: the **first-year** monthly office premium per policy, KRW.

    An **input, not a computed quantity**, and the one number in this model with a
    genuinely authoritative published anchor: the joint FSC/FSS launch release prints
    ₩11,982 as the 4세대 premium for a 40세 남자 on a 10-carrier 손해보험 average as at
    2021-06, against 1세대 ₩40,749, 2세대 ₩24,738 and 3세대 ₩13,326 for the same insured
    [R1].  Age 40 male is also the 기준연령 요건 of 감독규정 제1-2조제2호, so the anchor
    cell is the cell Korean supervisory disclosure is quoted on [REG-R9].

    No age x sex rate scale exists in public for any generation of this product, so the
    other model points' premiums are **[std]**, scaled off the anchor by the 4.0% age
    slope of ``age_load`` and floored at the child rate — a pure extrapolation of
    4% a year down to age 0 gives a premium the market does not write.

    Only the *first* year is an input.  Every later year is the renewal recursion of
    :func:`prem_ge_base` and :func:`prem_np_base`.
    """
    return float(model_point()["premium"])


def np_share():
    """s: the 비급여 특약 share of the first-year office premium **[std]**.

    Two published values, and they differ.  The FSC/FSS FAQ states that when both parts
    are held the rider is 「전체 보험료의 60% 수준」 and works an example at 급여 ₩5,000
    plus 비급여 ₩8,000 for a 45-year-old male, a 61.5% share [R2].  The 표준약관's own
    renewal illustration implies 48.75%: solving its band-2 and band-5 rows at renewal
    +1, ``g + n = 18,200`` and ``g + 4n = 44,818``, gives ``n = 8,873`` [S1].  The
    composite takes **60%**, because [R2] is a statement about the market as sold while
    the 표준약관 figure is a stylised illustration at an unnamed age.

    The share matters more than its size suggests, because the relativity multiplies
    **only** the rider: at 60% a band-5 policyholder pays
    ``0.40 + 0.60 x 4.00 = 2.80x`` the base total premium, but only 2.46x at 48.75%.
    """
    return float(model_point()["np_share"])


def np_rider():
    """Whether the 실손의료보험 특별약관 (비급여 실손의료비) is held [S1].

    On in the base run.  Switched off it removes 60% of the premium, the 100-visit cap,
    the three sub-limits and **the whole experience-rating loop** — the contract becomes
    a plain 급여-only attained-age renewable.  Model point 5 is that election.
    """
    return bool(int(model_point()["np_rider"]))


def three_np():
    """Whether 3대비급여형 is held [S1 특별약관 제1조]; on in the base run.

    It is a 보장종목 of the 특약 and not a separate contract, and its money and count
    limits **displace** the main ₩50,000,000 비급여 limit for the three classes.  Where
    it is not held those treatments are not covered at all rather than falling back into
    the main limit.  Model point 6 is that election.
    """
    return bool(int(model_point()["three_np"])) and np_rider()


def annual_limit():
    """L: the 연간 보험가입금액 per 보장종목, KRW.

    The 표준약관 sets a **ceiling** and leaves the level to the carrier: 「5천만원
    이내에서 회사가 정한 금액 중 계약자가 선택한 금액」 [S1 제5조].  No 4세대 menu was
    retrieved; a 5세대 carrier menu is ₩50,000,000 / ₩30,000,000 / ₩10,000,000 [S3].
    The composite takes the maximum **[std]**, because every published premium
    comparison is quoted on the full limit and because a lower limit only truncates the
    severity distribution further.  상해 and 질병 carry **separate** limits, so the
    whole-contract annual exposure with both parts held is ₩100,000,000.
    """
    return float(model_point()["annual_limit"])


def visit_cap():
    """Lv: the 통원 1회당 한도, KRW; ₩200,000 in the composite [S1 제5조제5항].

    A ceiling in the wording, like the annual limit; ₩100,000 to ₩200,000 observed on a
    5세대 carrier menu [S3].  It binds at a covered outpatient cost of ₩250,000 on the
    급여 side, the same crossing point at both provider tiers.
    """
    return float(model_point()["visit_cap"])


def oop_decile():
    """The insured's NHI-contribution decile, 1 to 10, for the 본인부담상한제 [R10].

    A model point attribute rather than an assumption because the ceiling is set by the
    **insured's own income**, and the spread is nine-fold: on the 2026 scale a 1분위
    insured is refunded everything above ₩900,000 a year and a 10분위 insured everything
    above ₩8,430,000.  The 급여 claim distribution is truncated, and truncated
    differently by income decile — which is exactly why the 비급여 half, which has no
    such truncation, is 57.1% of claims against a 15.8% share of national spend.
    """
    return int(model_point()["oop_decile"])


def clinic_share():
    """The share of 급여 통원 visits at the ₩10,000 clinic tier **[std]**.

    The 표준약관's deductible table has two rows: ₩10,000 at 의료법 제3조제2항
    institutions other than 종합병원, at 보건소·보건의료원·보건지소, at 보건진료소 and
    at their pharmacies; ₩20,000 at 전문요양기관, 상급종합병원, 종합병원 and their
    pharmacies [S1 제3조 <표1>].  0.63 is the 2025 claim split by provider class —
    의원 32.0%, 병원 21.8% and 요양병원 2.8% against 종합병원 17.6% and 상급종합 15.0%
    [R7] — normalised over the named classes.  Provider mix is a first-order variable in
    this product in a way it is in nothing else in the library.
    """
    return float(model_point()["clinic_share"])


def nhi_covered():
    """Whether the insured is inside 국민건강보험 or 의료급여 [S1 제3조제3항제1호].

    Where the insured falls outside 국민건강보험법 제5조·제53조·제54조 or the 의료급여법
    equivalents — most commonly a suspension of entitlement — reimbursement falls to
    **40%** of the amount actually borne on both parts, still within the annual limit.
    This is a **state, not an event**: it persists while entitlement is suspended, which
    is why it is a model point attribute.  It also switches the 본인부담상한제 off, since
    a life outside the scheme is not refunded by it.  Model point 10 is that branch.
    """
    return bool(int(model_point()["nhi_covered"]))


def trend_mult():
    """A multiplier on the medical cost trend of both units **[std]**; 1.0 in the base.

    It is the switch that exercises the ±25% renewal corridor, which no shipped trend
    reaches on its own: at 4.5 the 비급여 unit's re-rate would be 36.45% and the corridor
    clips it to 25%, so the rider's premium falls behind its own claim trend year after
    year.  Model point 10 carries it, and its loss ratio rises from 0.533 to 0.591 over the
    ten projected years — which is less than it sounds, because the corridor and the 4% age
    loading compose to admit a re-rate of 1.25 x 1.04 = 1.30 a year.  **The corridor does
    not bind economically below a 30% claim trend**, and that is a model finding rather than
    an artefact of this parameterisation.
    """
    return float(model_point()["trend_mult"])


def util_mult():
    """A multiplier on every claim frequency **[std]**; 1.0 in the base.

    The claim distribution of this product is extraordinarily concentrated — 65% of
    insureds claim nothing in a year and the top decile takes about 74% of all claims
    [R4] [R5] [R6] — so a single cell carrying the population mean frequency is not a
    policyholder anybody would recognise.  Model point 8 carries 10.0, a cell inside that
    top decile sitting on the lowest 본인부담상한액 decile, and it is the only shipped point
    on which the public truncation binds — at 0.8018 in policy year 1 and 0.6024 by policy
    year 10.
    """
    return float(model_point()["util_mult"])


def reld_on():
    """Whether the 요율 상대도 (비급여 할인·할증) is in operation [S1 특별약관 제6조].

    On in the base run, but only from ``reld_start_year``: the clause was in the
    wording from launch and its application was deferred three years 「충분한 통계 확보
    등을 위하여」, commencing 2024-07-01 [R3].  A 4세대 policy written in 2021 therefore
    had three renewals at flat relativity before the loop switched on.  Off on model
    points 5 and 9, where the contract is a plain attained-age renewable.
    """
    return bool(int(model_point()["reld_on"])) and np_rider()


def noclaim_on():
    """Whether the 무사고 할인 is in operation [R1] [S3]; on in the base run.

    10% off the **whole** office premium — 급여 and 비급여 together — after two
    consecutive years with no 비급여 claim, excluding 4대 중증질환 claims from the test.
    It has a two-year lookback where the relativity has one, it applies to the whole
    premium where the relativity applies only to the rider, and it **stacks** with the
    band-1 discount.
    """
    return bool(int(model_point()["noclaim_on"]))


def suspend_rate():
    """The annual 개인실손 중지 decrement **[std]**; 0 in the base run.

    A policyholder covered by a 단체실손 may suspend the individual policy for the
    duration and resume it within one month of the group cover ending, and the facility
    is **mandatory** under 감독규정 제7-63조제2항제7호 [R16] [S3] [REG-R17].  It is
    carried here as a decrement and not as a state: the contract that resumes is a
    different projection, entering the product in force at resumption.  Model point 9
    carries 3% a year.
    """
    return float(model_point()["suspend_rate"])


# --- Time and the projection horizon ---------------------------------------

def proj_len():
    """The **number** of projected policy months: the exclusive end of the frame, so the
    projection runs over ``t = 0 .. proj_len() - 1`` and ``result_cf()`` has
    ``proj_len()`` rows.

    Two five-year 보장내용 변경주기 — ten policy years — or the run to
    ``max_cover_age`` if that comes first, which on the shipped model points it does
    not.  The horizon is **stated** rather than
    contractual, and the distinction is the whole point.  감독규정 제7-63조제2항제6호나목
    requires the 보험기간 및 보장내용 변경주기 to be five years or less [REG-R17], and at
    the fifth 계약해당일 a 4세대 contract's benefit terms are replaced by whatever the
    supervisor is then prescribing, at a premium the insurer sets for that product.  No
    projection of this contract past the first 재가입 is a projection of *this*
    contract's terms; the model assumes re-entry on unchanged terms, twice over, and says
    so.

    The contract boundary this raises is genuinely contestable — a one-year term, an
    unrestricted right to re-rate, a supervisor-set cap on that re-rating, a five-year
    re-entry into a wording the insurer does not control and an obligation not to refuse
    re-entry on health grounds — and this model asserts no answer to it.
    """
    years = min(reentry_cycles * reentry_period,                     # noqa: F821
                max_cover_age - issue_age())                         # noqa: F821
    return 12 * int(years)


def policy_year(t):
    """y(t): the policy year containing policy month t, 1-based.

    The **연간** of this contract is 「계약일로부터 매1년 단위로 도래하는 계약해당일
    전일까지의 기간」 [S1 제5조제2항] — a policy year measured from the contract date and
    not a calendar year.  All four ₩50,000,000 limits, the ₩200,000 per-visit cap, the
    100-visit count, the three 3대비급여 sub-limits and the ₩2,000,000 inpatient
    co-payment cap run on this clock and reset at each 계약해당일.  The 본인부담상한제
    does **not**, and neither do the insurer's own statistics; both run on the calendar
    year, and this model does not attempt to reconcile the two clocks.
    """
    return t // 12 + 1


def age(t):
    """The attained **만나이** in policy month t, incremented at the policy anniversary.

    Not the 보험나이 the contract prices on — see the Space docstring.  The anniversary
    increment is itself a **[std]** convention: a deterministic single-cell projection
    has no birthday to increment on.
    """
    return issue_age() + t // 12


def pols_if_init():
    """The in-force count at the start of the projection: one policy.

    Every cash flow in ``result_cf()`` is per policy issued, so the frame is a unit
    projection and scales linearly.
    """
    return 1.0


# --- Decrements -------------------------------------------------------------

def mort_rate(t):
    """The annual mortality rate at the attained 만나이 in policy month t.

    The **[std]** Makeham construction of ``mort_table.csv``, read at ``age(t)`` and held
    flat at the terminal age.  On this contract **death releases the liability**: the
    main contract pays nothing on death beyond the 미경과보험료, so the direction of
    prudence is the reverse of every protection product in this library and an
    over-statement of mortality is *anti*-conservative.
    """
    x = min(age(t), int(data.mort_table().index.get_level_values(   # noqa: F821
        "age").max()))
    return float(data.mort_table().loc[(sex(), x), "mort_rate"])     # noqa: F821


def mort_rate_mth(t):
    """The monthly mortality rate in policy month t, from the annual rate.

    ``1 - (1 - q)^(1/12)``: a uniform force of mortality across the policy year
    **[std]**, the library-wide monthly conversion.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate(t):
    """The **annual** lapse rate in policy month t, from ``lapse_table.csv``.

    Keyed by policy year; policy years beyond the last row take that row.  This is
    **non-payment lapse only**.  A missed premium produces a 납입최고 of at least 14 days
    and the contract terminates the day after it ends [REG-R25 제26조], and there is
    nothing to break the fall: with no surrender value there is no 보험료 자동대출납입 to
    advance the premium, and 표준약관 제33조 excludes 「순수보장성보험 등」 from policy
    lending anyway.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate"])


def lapse_rate_mth(t):
    """The monthly lapse rate in policy month t, from the annual rate.

    ``1 - (1 - w)^(1/12)``, the library-wide conversion.  The annual rate is
    :func:`lapse_rate`; the two must not be confused, which is why the library spells
    them apart.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def suspend_rate_mth(t):
    """The monthly 개인실손 중지 decrement in policy month t.

    ``1 - (1 - r)^(1/12)`` on the model point's annual rate; identically zero on every
    model point but 9.  Suspension is not a lapse — the policyholder retains the right
    to resume — but for this projection it ends the cash flows, and the contract that
    resumes is a different projection.
    """
    return 1.0 - (1.0 - suspend_rate()) ** (1.0 / 12.0)


def renewal_decline(t):
    """The proportion declining the annual renewal at the end of policy month t.

    Non-zero only in the twelfth month of a policy year, when the contract comes up for
    renewal.  The asymmetry is contractual: 「the policyholder may decline renewal; the
    insurer may not」, within the 보장내용 변경주기 and the age range, provided the prior
    premium was paid [S5] [S3].  So this is a **policyholder option** on a contract the
    insurer cannot exit, and its rate is **[std]** — no published 실손 renewal-decline
    series exists, only the 3.3% blended in-force decay [R7].
    """
    if (t + 1) % 12 != 0:
        return 0.0
    return renewal_decline_rate                                      # noqa: F821


def pols_if(t):
    """l(t): the in-force probability at the **start** of policy month t.

    :func:`pols_if_init` at ``t = 0``, then
    ``l(t+1) = l(t)(1 - q)(1 - w)(1 - susp)(1 - decline)``.  This is the weight on every
    cash flow of the same ``result_cf()`` row.  Zero outside ``0 .. proj_len() - 1``.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The in-force probability at a point inside policy month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before lapses.

    ``"BEF_SUSPEND"``
        after lapses, before the 개인실손 중지 decrement.

    ``"BEF_RENEWAL"``
        after suspension, before the renewal decline — which acts only in the twelfth
        month of each policy year.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state, and zero in the final projected month because
        the projection horizon ends there.

    The processing order — mortality, then lapse, then suspension, then the renewal
    decline — is **[std]**; nothing published fixes it, and on rates of this size the
    ordering is worth less than a basis point a year.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "BEF_SUSPEND":
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    if timing == "BEF_RENEWAL":
        return pols_if_at(t, "BEF_SUSPEND") * (1.0 - suspend_rate_mth(t))
    if timing == "AFT_DECR":
        if t < 0 or t >= proj_len() - 1:
            return 0.0
        return pols_if_at(t, "BEF_RENEWAL") * (1.0 - renewal_decline(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """Expected deaths at the end of policy month t.

    A pure liability release.  On death from a cause the policy does not cover the
    insurer pays the 계약자적립액 and the 미경과보험료 of 감독규정 제7-66조제5항 and the
    contract terminates [REG-R17 제7-63조제1항제1호] [REG-R25 제22조]; on a one-year pure
    protection contract the 계약자적립액 is nil to the precision this model works at, so
    the payment reduces to the return of unearned premium and there is no
    ``claims_death`` anywhere in this model.  **This is the only place in ``krlib`` where
    that provision has no financial content** — in ``Cancer_KR_S`` and ``LTC_KR_S`` the
    same clause forces an account balance into a non-savings product.
    """
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Expected lapses at the end of policy month t, from the survivors of mortality.

    Pays nothing: 「이 상품은 1년만기 순수보장성 상품으로 해약환급금이 발생하지
    않습니다」 [S3], so there is no ``claims_lapse`` limb and no ``cv_pp`` cells.  A
    policyholder who cancels mid-term recovers the 미경과보험료 under 상법 제649조, which
    is a return of premium and not a surrender value.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_suspend(t):
    """Expected 개인실손 중지 suspensions at the end of policy month t.

    Zero on every model point but 9.  See :func:`suspend_rate`.
    """
    return pols_if_at(t, "BEF_SUSPEND") * suspend_rate_mth(t)


def pols_renewal_decline(t):
    """Expected renewals declined at the end of policy month t.

    Non-zero only in the twelfth month of each policy year.  It is a separate decrement
    from :func:`pols_lapse` because it is a separate act: a lapse is a missed premium
    and a decline is the exercise of a contractual option at a contractual date, and on
    a one-year renewable contract the second is the one the product is exposed to.
    """
    return pols_if_at(t, "BEF_RENEWAL") * renewal_decline(t)


def pols_maturity(t):
    """Policies whose cover ends at the scheduled end of the projection.

    The library-wide meaning: the count whose cover ends because the contract reaches
    its scheduled end, whether or not anything is paid for it.  **Nothing is paid** —
    there is no maturity benefit on a 순수보장성 contract, so there is no
    ``claims(t, "MATURITY")`` limb — but the count is needed for the in-force
    roll-forward to close in the final month.  What ends here is the *stated horizon* of
    :func:`proj_len`, which is the second 재가입 or the maximum cover age, whichever
    comes first; the contract itself continues into the then-current generation.
    """
    if t != proj_len() - 1:
        return 0.0
    return pols_if_at(t, "BEF_RENEWAL") * (1.0 - renewal_decline(t))


# --- Utilisation and severity, by policy year -------------------------------

def util_band(y):
    """The five-year utilisation band containing the attained age in policy year y.

    The lower edge of the band, capped at the last band of the table.  Utilisation is
    published by five-year band and not by single year, which is the granularity the
    NHIS coverage-ratio series comes at.
    """
    x = issue_age() + y - 1
    top = int(data.utilisation_table().index.get_level_values(       # noqa: F821
        "age_start").max())
    return min(5 * (x // 5), top)


def util_value(y, column):
    """A column of the utilisation table at the model point's sex and the band for y.

    The frequency columns carry the model point's :func:`util_mult`; ``los_days`` does
    not, because a longer stay is not a more frequent one and the room-differential cap
    is applied against the stay length itself.
    """
    v = float(data.utilisation_table().loc[                          # noqa: F821
        (sex(), util_band(y)), column])
    if column == "los_days":
        return v
    return v * util_mult()


def adm_rate(y):
    """n_adm(y): admissions a year per policy giving rise to a paid claim **[std]**.

    An admission drives **both** halves of the claim — the 급여 본인부담금 and the
    비급여 cost of the same stay — which is why it is one frequency and not two.  The
    level is solved from the anchor calibration; the age curve follows the NHIS coverage
    ratio by age band [R9].
    """
    return util_value(y, "adm_rate")


def los_days(y):
    """D(y): the mean length of stay per admission, days **[std]**.

    Carried because the 상급병실료 차액 cap is **₩100,000 per day averaged over the
    whole admission**, the average being total non-covered room charge divided by total
    days [S1].  A single expensive night inside a long stay is therefore smoothed
    against the stay length rather than capped night by night — a materially more
    generous treatment than a nightly cap, and one a per-night implementation
    understates.
    """
    return util_value(y, "los_days")


def visit_rate_ge(y):
    """n_ge(y): 급여 통원 visits a year per policy giving rise to a paid claim **[std]**.

    4세대 merged 외래 and 처방조제 into **one visit with one deductible**; the 3세대
    wording carried a separate ₩8,000 처방조제 deductible on top [S5] [S1].  This count
    is of merged visits, which is why a 3세대 frequency basis cannot be carried across
    without adjustment.
    """
    return util_value(y, "visit_rate_ge")


def visit_rate_np(y):
    """n_np(y): 비급여 통원 visits a year per policy **[std]**, before the count cap.

    Excludes the three 3대비급여 classes, which are counted as acts and carry their own
    deductibles and limits.
    """
    return util_value(y, "visit_rate_np")


def act_rate_physio(y):
    """a_ph(y): acts a year of 도수치료, 체외충격파치료 and 증식치료 **[std]**.

    The three **share one 50-act counter** and one ₩3,500,000 money limit, so they are
    one frequency here.  Two or more of them at one visit are **each** counted and
    **each** separately deducted [S1 특별약관 제3조(3)제4항제1호], which is the counting
    rule that makes the ₩30,000 per-act floor expensive for the insured.  근골격계 질환
    claims, of which this is the bulk, were 15.8% of all 실손 claims in 2025 [R7].
    """
    return util_value(y, "act_rate_physio")


def act_rate_inject(y):
    """a_in(y): acts a year of non-covered injection **[std]**.

    Two or more injections at one visit or admission are **one** act with one deduction
    [S1 제3조(3)제4항제2호] — the opposite of the physical-therapy rule, and worth money
    to the insurer.  주사료 means 「주사치료시 사용된 행위, 약제 및 치료재료대」: the
    procedure, the drug and the consumables together.  Non-covered injections were
    ₩2.81조, 18.5% of all claims, in 2024 [R8].
    """
    return util_value(y, "act_rate_inject")


def act_rate_mri(y):
    """a_mr(y): acts a year of non-covered MRI or MRA **[std]**.

    MRI at two or more sites, or the same site twice, are **separate** acts each
    carrying its own deduction [S1 제3조(3)제4항제3호] — worth money to the insured
    rather than to the insurer.  There is **no count limit** on this class, only the
    ₩3,000,000 money limit.
    """
    return util_value(y, "act_rate_mri")


def trend_ge(y):
    """f_ge(y): the cumulative 급여 cost trend from policy year 1 to policy year y.

    ``(1 + med_trend_ge x trend_mult)^(y-1)``.  The 국민건강보험공단 진료비 실태조사
    measures 2024 growth of the statutory co-payment at **1.0%** against 4.3% for the
    scheme's own outlay [R9] [REG-R41]; that is the anchor **[std]**.
    """
    return (1.0 + med_trend_ge * trend_mult()) ** (y - 1)            # noqa: F821


def trend_np(y):
    """f_np(y): the cumulative 비급여 cost trend from policy year 1 to policy year y.

    ``(1 + med_trend_np x trend_mult)^(y-1)``, anchored on the same survey's **8.1%**
    growth in non-covered spend in 2024 [R9] [REG-R41].  **비급여 is compounding at
    roughly twice the rate of the whole**, and it is the half of the claim that has no
    public price: the 건강보험심사평가원 price survey found 도수치료 quoted between
    ₩5,000 and ₩600,000 across Seoul hospitals [R2].  That divergence is why the two
    priced units are re-rated separately.
    """
    return (1.0 + med_trend_np * trend_mult()) ** (y - 1)            # noqa: F821


def retain_rate_ge():
    """r_ge: the 급여 자기부담률, 20% [S1] or 60% outside 국민건강보험.

    The wording always expresses it as its complement — 「본인부담금의 80%에 해당하는
    금액」 — and never as a co-payment percentage.  Where 국민건강보험 entitlement does
    not apply, reimbursement falls to 40% of the amount actually borne
    [S1 제3조제3항제1호], which is a retention of 60% **[std]**: the wording states the
    reimbursement and this model states the retention, and the flat outpatient
    deductible floor still applies on top.
    """
    return retain_rate_ge_base if nhi_covered() else retain_rate_nonhi  # noqa: F821


def retain_rate_np():
    """r_np: the 비급여 자기부담률, 30% [S1 특별약관 제3조] or 60% outside 국민건강보험.

    The 30% against the 급여 side's 20% is the generation's design statement:
    「필수 치료인 급여에 대해서는 보장을 확대하되, 환자의 선택사항인 비급여에 대해서는
    의료이용에 따라 보험료가 할인·할증되도록 하였습니다」 [R1].
    """
    return retain_rate_np_base if nhi_covered() else retain_rate_nonhi  # noqa: F821


def sev_points(stream):
    """The discrete cost distribution of a severity stream, as (cost, probability) pairs.

    Eight streams: ``ge_in``, ``ge_out``, ``np_in``, ``np_room``, ``np_out``, ``physio``,
    ``inject`` and ``mri``.  The distribution and not its mean is what the model needs,
    because the deductible is ``max(flat floor, percentage x cost)`` and the per-visit
    cap truncates the top: the payment is a kinked function of cost, and applying the
    rule to a mean removes both kinks.
    """
    sub = data.severity_table().loc[stream]                          # noqa: F821
    return list(zip(sub["cost"].tolist(), sub["prob"].tolist()))


def sev_mean(stream):
    """The expected cost of one event in a severity stream, KRW, before any trend."""
    return sum(c * p for c, p in sev_points(stream))


# --- 급여 reimbursement — the main contract ---------------------------------

def oop_incurred_ge(y):
    """C_ge(y): the 급여 본인부담금 incurred in policy year y, before any truncation.

    The insured's own share under 국민건강보험법 요양급여 or 의료급여법 의료급여, both
    일부본인부담금 and 전액본인부담금 [S1 기본형 제3조] [REG-R53], across admissions and
    outpatient visits.  This is the quantity the 본인부담상한제 caps.
    """
    return (adm_rate(y) * sev_mean("ge_in") + visit_rate_ge(y) * sev_mean("ge_out")) \
        * trend_ge(y)


def oop_ceiling():
    """S: the 본인부담상한액 for the model point's income decile, KRW [R10].

    국민건강보험법 제44조제2항 creates the 본인부담상한제: the NHIS refunds the excess of
    a member's annual 본인일부부담금 over an income-graded ceiling [REG-R53], operated as
    사전급여 and 사후환급 over the **calendar** year.  On the 2026 scale the ceiling runs
    from ₩900,000 at 1분위 to ₩8,430,000 at 10분위.  Infinite where the insured is
    outside the scheme, since nothing is refunded to a life the scheme does not cover.
    """
    if not nhi_covered():
        return float("inf")
    return float(data.oop_ceiling_table().loc[oop_decile(),          # noqa: F821
                                             "ceiling"])


def oop_trunc(y):
    """tau(y): the 본인부담상한제 truncation factor on the 급여 covered loss in year y.

    **The single most important interaction in the product, and the one a model built
    from the policy wording alone will miss.**  The 표준약관 excludes the refundable
    amount twice over — 제5조제3항 limits the reimbursement to what the insured actually
    bore net of any amount refundable ex ante or ex post, and 제4조제3항제1호 excludes
    outright 「국민건강보험공단으로부터 사전 또는 사후 환급이 가능한 금액(본인부담금
    상한제)」 [S1].  So the 급여 half of the claim is bounded above, per insured per
    year, at roughly ``0.80 x 본인부담상한액`` — ₩720,000 for a 1분위 insured in 2026 and
    ₩6,744,000 for a 10분위 one, **a nine-fold spread driven by income and nothing
    else**.

    ``min(1, ceiling / incurred)`` is a **[std]** deterministic representation: a
    proportional truncation of an expectation is not the same thing as truncating each
    realisation, and it understates the truncation's bite for the same reason a limit
    applied to a mean understates a limit's.  It is applied **first**, as an exclusion
    from covered loss, and the ₩2,000,000 inpatient cap second on what remains — the
    order matters, because both reduce the insured's retention on heavy 급여 use and a
    model that applies them in the wrong order double-counts the relief.
    """
    c = oop_incurred_ge(y)
    if c <= 0.0 or c <= oop_ceiling():
        return 1.0
    return oop_ceiling() / c


def claims_ge_in_pp(y):
    """paid_in(y): 급여 입원 reimbursement per policy in year y, before the annual limit.

    ``0.80 x 본인부담금`` [S1 기본형 제3조], plus the top-up: where the 20% retained on
    **inpatient** treatment exceeds ₩2,000,000 in a policy year, the excess is reimbursed
    within the annual limit [S1 제5조제4항] [REG-R17 제7-63조제2항제2호], so that beyond
    ₩2,000,000 of retained inpatient co-payment the 자기부담률 on further inpatient 급여
    cost is effectively nil for the rest of the year.  The cap is not a 4세대 novelty —
    the identical ₩2,000,000 appears in a 2세대 carrier document [S4].  It applies to
    inpatient treatment only; there is no annual cap on the outpatient deductible.
    """
    cost = adm_rate(y) * sev_mean("ge_in") * trend_ge(y) * oop_trunc(y)
    retained = cost * retain_rate_ge()
    top_up = max(0.0, retained - cap_inpatient_retain)               # noqa: F821
    return cost * (1.0 - retain_rate_ge()) + top_up


def paid_out_per_visit(stream, floor, retain, trend):
    """The expected reimbursement of one outpatient visit of a severity stream.

    ``E[ min( max(0, c - max(floor, retain x c)), visit_cap ) ]`` over the stream's own
    cost distribution.  The deductible is a **flat floor that becomes a percentage**: at
    the 급여 clinic tier it is ₩10,000 until the covered cost reaches ₩50,000 and 20%
    thereafter, at the hospital tier ₩20,000 until ₩100,000, and on the 비급여 side a
    flat ₩30,000 until ₩100,000 and 30% thereafter.  Above the crossing point the
    payment is a straight percentage of cost until the per-visit cap binds — at
    ₩250,000 of covered cost on the 급여 side, the same point at both tiers.
    """
    tot = 0.0
    for c, p in sev_points(stream):
        cost = c * trend
        ded = max(floor, retain * cost)
        tot += p * min(max(0.0, cost - ded), visit_cap())
    return tot


def claims_ge_out_pp(y):
    """paid_out(y): 급여 통원 reimbursement per policy in year y, before the annual limit.

    Per visit, the covered cost less ``max(d_tier, 20% x cost)``, then capped at the
    per-visit limit [S1 기본형 제3조 <표1>], blended over the two provider tiers by
    :func:`clinic_share`.  Where two or more visits fall on one day for the same
    treatment purpose they count as one, and 「공제금액은 2회 이상의 중복방문 의료기관 중
    가장 높은 공제금액을 적용합니다」 — the highest applicable deductible
    [S1 제3조제8항]; the visit counts here are already of merged visits **[std]**.
    """
    tr = trend_ge(y) * oop_trunc(y)
    r = retain_rate_ge()
    clinic = paid_out_per_visit("ge_out", ded_clinic, r, tr)         # noqa: F821
    hosp = paid_out_per_visit("ge_out", ded_hospital, r, tr)         # noqa: F821
    return visit_rate_ge(y) * (clinic_share() * clinic
                               + (1.0 - clinic_share()) * hosp)


def ge_limit_factor(y):
    """The proportion of the raw 급여 claim that survives the annual limit in year y.

    상해급여형 and 질병급여형 carry **separate** ₩50,000,000 limits [S1 제5조], so the
    raw claim is split by ``share_injury`` and each part capped at
    :func:`annual_limit`.  The split is **[std]**: nothing published gives it, and it
    matters only where the limit binds, which on a deterministic expectation is nowhere.
    """
    raw = claims_ge_in_pp(y) + claims_ge_out_pp(y)
    if raw <= 0.0:
        return 1.0
    lim = annual_limit()
    capped = min(share_injury * raw, lim) \
        + min((1.0 - share_injury) * raw, lim)                       # noqa: F821
    return capped / raw


def claims_ge_pp(y):
    """The whole 급여 claim per policy in policy year y, after the annual limit."""
    return (claims_ge_in_pp(y) + claims_ge_out_pp(y)) * ge_limit_factor(y)


# --- 비급여 reimbursement — the rider ---------------------------------------

def claims_np_in_pp(y):
    """paid_np_in(y): 비급여 입원 reimbursement per policy in year y, before the limit.

    Two limbs [S1 특별약관 제3조].  ``0.70 x 비급여 의료비`` excluding the room charge;
    and the 상급병실료 차액 at **50% of the non-covered room charge, capped at ₩100,000
    per day averaged over the whole admission** — the average being total non-covered
    room charge divided by total days, which is why :func:`los_days` is carried and why
    a per-night implementation of the cap understates the benefit.
    """
    tr = trend_np(y)
    base = sev_mean("np_in") * tr * (1.0 - retain_rate_np())
    room = 0.0
    for c, p in sev_points("np_room"):
        room += p * min(room_rate * c * tr,                          # noqa: F821
                        room_cap_day * los_days(y))                  # noqa: F821
    return adm_rate(y) * (base + room)


def visits_np_eff(y):
    """The 비급여 통원 visits actually covered in policy year y.

    Capped at **100 visits a policy year** [S1 특별약관] — the count cap the 급여 side
    does not have, and the only count limit outside the 3대비급여 classes.
    """
    return min(visit_rate_np(y), visit_limit_np)                     # noqa: F821


def claims_np_out_pp(y):
    """paid_np_out(y): 비급여 통원 reimbursement per policy in year y, before the limit.

    Per visit, the covered cost less ``max(₩30,000, 30% x cost)``, then capped
    [S1 특별약관 <표1>].  The floor is **flat at every provider**, not tiered as on the
    급여 side, which is why the wording does not repeat the 급여 side's
    highest-applicable-deductible rule for multiple same-day visits.

    The **injection carve-out** is added here.  비급여 injections of 항암제, 항생제
    (항진균제 포함) and 희귀의약품, each defined by a 식품의약품안전처 classification
    instrument, leave the ₩2,500,000 injection sub-limit and are reimbursed inside the
    main ₩50,000,000 비급여 limit [S1 특별약관 제3조(3)제2항].  So the sub-limit bites on
    the discretionary end of injection use — the 영양제 and 비타민제 the same wording
    restricts by licensed indication — and not on oncology.  Where the carve-out sits is
    a first-order calibration question and not a detail: non-covered injections were
    18.5% of all claims in 2024 [R8].
    """
    tr = trend_np(y)
    r = retain_rate_np()
    out = visits_np_eff(y) * paid_out_per_visit("np_out", ded_np_out, r, tr)  # noqa: F821
    carve = 0.0
    if three_np():
        acts = min(act_rate_inject(y), act_limit_three)              # noqa: F821
        carve = acts * inject_carve_share * paid_per_act("inject", tr)  # noqa: F821
    return out + carve


def np_limit_factor(y):
    """The proportion of the raw main 비급여 claim that survives the annual limit.

    상해비급여형 and 질병비급여형 carry separate ₩50,000,000 limits
    [S1 특별약관 제5조], split by ``share_injury`` exactly as on the 급여 side.  The
    3대비급여 classes are **outside** this limit and carry their own.
    """
    raw = claims_np_in_pp(y) + claims_np_out_pp(y)
    if raw <= 0.0:
        return 1.0
    lim = annual_limit()
    capped = min(share_injury * raw, lim) \
        + min((1.0 - share_injury) * raw, lim)                       # noqa: F821
    return capped / raw


def claims_np_main_pp(y):
    """The main 비급여 claim per policy in policy year y, after the annual limit.

    Zero when the 특별약관 is not held.
    """
    if not np_rider():
        return 0.0
    return (claims_np_in_pp(y) + claims_np_out_pp(y)) * np_limit_factor(y)


# --- 3대비급여 — sub-limits, shared counters and hard annual gates -----------

def paid_per_act(stream, trend):
    """The expected reimbursement of one act of a 3대비급여 class.

    ``E[ max(0, c - max(₩30,000, 30% x c)) ]`` [S1 특별약관 제3조(3) <표1>].  There is no
    per-visit cap on these classes: what caps them is the annual money limit and, on two
    of the three, the act counter.
    """
    tot = 0.0
    for c, p in sev_points(stream):
        cost = c * trend
        tot += p * max(0.0, cost - max(ded_np_out,                   # noqa: F821
                                       retain_rate_np() * cost))
    return tot


def acts_physio_eff(y):
    """a_ph_eff(y): physical-therapy acts actually covered in policy year y.

    Two gates.  The **50-act counter** is shared by 도수치료, 체외충격파치료 and
    증식치료 together [S1 특별약관 제3조(3) <표1>].  And cover beyond the first ten acts
    is **conditional**: 「각 치료횟수를 합산하여 최초 10회 보장하고, 이후 객관적이고
    일반적으로 인정되는 검사결과 등을 토대로 증상의 개선, 병변호전 등이 확인된 경우에
    한하여 10회 단위로 연간 50회까지 보상합니다」, on a named clinical test set — 관절가동
    (ROM), 통증평가척도, 자세평가 및 근력검사(MMT) and 초음파 검사 — with the insurer
    bearing the whole cost of the assessment [S1] [R2].  **This is the only place in
    ``krlib`` where a benefit is gated on a clinical review rather than on a
    definition**, and a projection can only represent it as a continuation probability
    at each ten-act boundary: ``physio_cont_prob``, **[std]**, with no observed
    range because none is published.
    """
    a = min(act_rate_physio(y), act_limit_three)                     # noqa: F821
    return min(a, physio_gate_acts) \
        + max(0.0, a - physio_gate_acts) * physio_cont_prob          # noqa: F821


def acts_inject_eff(y):
    """a_in_eff(y): injection acts actually covered in policy year y, net of the
    carve-out.

    Capped at the same **50 acts** a policy year as the physical-therapy trio, but on
    its own counter [S1 특별약관 제3조(3) <표1>].  The share carved out to the main
    비급여 limit — 항암제, 항생제 and 희귀의약품 — is removed here and added in
    :func:`claims_np_out_pp`, so no act is counted twice.
    """
    return min(act_rate_inject(y), act_limit_three) \
        * (1.0 - inject_carve_share)                                 # noqa: F821


def claims_physio_pp(y):
    """The 도수·체외충격파·증식치료 claim per policy in year y, after its sub-limit.

    Capped at **₩3,500,000** a policy year [S1 특별약관 제3조(3) <표1>].  **Both gates
    are hard and neither is pro-rated**, and the wording works both cases: where
    ₩3,500,000 is exhausted after 30 treatments on 2022-10-31 cover is excluded for the
    following 151 days and resumes at the 계약해당일 2023-04-01; where 50 treatments are
    used but only ₩3,000,000 paid, cover is excluded for the following 182 days.  The
    limit that binds first stops cover for the rest of the policy year and only the
    anniversary restores it — a **censored counting process with an annual reset**, not
    a rate.
    """
    if not three_np():
        return 0.0
    return min(acts_physio_eff(y) * paid_per_act("physio", trend_np(y)),
               limit_physio)                                         # noqa: F821


def claims_inject_pp(y):
    """The 주사료 claim per policy in year y, after its sub-limit.

    Capped at **₩2,500,000** a policy year [S1 특별약관 제3조(3) <표1>], on the acts left
    after the 항암제·항생제·희귀의약품 carve-out.
    """
    if not three_np():
        return 0.0
    return min(acts_inject_eff(y) * paid_per_act("inject", trend_np(y)),
               limit_inject)                                         # noqa: F821


def claims_mri_pp(y):
    """The 자기공명영상진단 claim per policy in year y, after its sub-limit.

    Capped at **₩3,000,000** a policy year and at **no** act count [S1 특별약관
    제3조(3) <표1>] — the only one of the three classes without a counter.
    """
    if not three_np():
        return 0.0
    return min(act_rate_mri(y) * paid_per_act("mri", trend_np(y)),
               limit_mri)                                            # noqa: F821


def claims_np_three_pp(y):
    """paid_3(y): the whole 3대비급여 claim per policy in policy year y.

    These sit inside the 특별약관 but carry their own money and count limits **instead
    of** the ₩50,000,000 aggregate, which is why they are summed apart from
    :func:`claims_np_main_pp` and never pass through :func:`np_limit_factor`.
    """
    return claims_physio_pp(y) + claims_inject_pp(y) + claims_mri_pp(y)


def claims_np_pp(y):
    """All rider claims per policy in policy year y: the main limb and the 3대비급여."""
    return claims_np_main_pp(y) + claims_np_three_pp(y)


def claims_ann_pp(y, kind=None):
    """The claim per policy in policy year y, by kind, after every limit.

    ``"GE_IN"``, ``"GE_OUT"``, ``"NP_IN"``, ``"NP_OUT"``, ``"NP_THREE"``.  The 급여 and
    main 비급여 limbs carry their own annual-limit factor so that the printed columns
    still add to the limited total; the 3대비급여 limb is already at its own sub-limits.
    With no ``kind`` the sum over all five.
    """
    if kind is None:
        return sum(claims_ann_pp(y, k) for k in
                   ("GE_IN", "GE_OUT", "NP_IN", "NP_OUT", "NP_THREE"))
    if kind == "GE_IN":
        return claims_ge_in_pp(y) * ge_limit_factor(y)
    if kind == "GE_OUT":
        return claims_ge_out_pp(y) * ge_limit_factor(y)
    if kind == "NP_IN":
        return claims_np_in_pp(y) * np_limit_factor(y) if np_rider() else 0.0
    if kind == "NP_OUT":
        return claims_np_out_pp(y) * np_limit_factor(y) if np_rider() else 0.0
    if kind == "NP_THREE":
        return claims_np_three_pp(y)
    raise ValueError("invalid kind")


def loss_incurred_pp(y):
    """The 보장대상 의료비 incurred per policy in policy year y, before any reduction.

    The supervisor's own identity, and it is worth writing down because it is not the
    identity a fixed-sum health product obeys:
    ``covered_loss = 급여 본인부담금 + 비급여 의료비`` [R7].  Both terms are set outside
    the contract — the first by the public fee schedule and the co-payment schedule made
    under 국민건강보험법 제44조제1항, the second by the provider, since 요양급여 covers
    everything **except** what the 보건복지부장관 designates 비급여대상 under 제41조제4항
    and 비급여 is therefore a residual defined by exclusion from a list that moves
    [REG-R53].

    The 급여 limb is net of the 본인부담상한제, which is an exclusion from covered loss
    and not a reduction of the benefit.  This is the quantity the indemnity principle
    bounds the claim by: 「동일한 위험을 보장하는 2개 이상의 계약에 중복 가입 하더라도
    실제 발생한 손해(비용)를 초과하여 보험금을 지급하지 않습니다」 [S1 제37조·제38조].
    """
    ge = oop_incurred_ge(y) * oop_trunc(y)
    if not np_rider():
        return ge
    tr = trend_np(y)
    np_cost = adm_rate(y) * (sev_mean("np_in") + sev_mean("np_room")) * tr \
        + visit_rate_np(y) * sev_mean("np_out") * tr
    if three_np():
        np_cost += (act_rate_physio(y) * sev_mean("physio")
                    + act_rate_inject(y) * sev_mean("inject")
                    + act_rate_mri(y) * sev_mean("mri")) * tr
    return ge + np_cost


# --- 비급여 할인·할증 — the experience-rated renewal -------------------------

def claims_np_rated_pp(y):
    """C(y): the 비급여 claim of policy year y that counts for the 요율 상대도.

    Two exclusions from the count [S1 특별약관 제6조제3항] [REG-R54]: 비급여 claims
    arising from a 국민건강보험법 산정특례 condition — 암질환, 뇌혈관질환, 심장질환,
    희귀난치성질환 등 — and **all** claims of an insured graded 장기요양 1등급 or 2등급
    under 노인장기요양보험법.  **The severely ill are exempt from the experience
    rating**, and that is a direct statutory cross-reference between this model and
    ``LTC_KR_S``, the only such link in the library.  ``reld_exempt_share`` is the
    **[std]** share struck out, anchored on the 15.0% of 2025 claims the supervisor
    attributes to 암 and 뇌·심혈관질환 [R7].

    The window itself is 「보험료 갱신 전 12개월 이내 기간」 [S1 특별약관 제6조제3항],
    with an operational three-month offset because renewal notices go out about a month
    ahead — 「계약해당일이 속한 달의 3개월 전 말일부터 직전 1년간」 [R12] — which 5세대
    writes into the standard text.  On an annual grid the offset is invisible; on a model
    that tried to resolve it, the point would be that a claims-to-renewal lag of zero
    over-states the responsiveness of the loop.
    """
    return (1.0 - reld_exempt_share) * claims_np_pp(y)               # noqa: F821


def shape_buckets():
    """The bucket ids of the annual rated 비급여 claim distribution."""
    return list(data.claim_shape_table().index)                      # noqa: F821


def shape_share(bucket):
    """The share of contracts in a bucket of the claim-shape distribution.

    Bucket 0 is the no-claim mass, 72.9% of contracts assessed at commencement [R12],
    and it is what becomes 1단계.
    """
    return float(data.claim_shape_table().loc[bucket, "share"])      # noqa: F821


def shape_mean():
    """The mean annual rated 비급여 claim of the shape table as tabulated, KRW.

    The table is tabulated at the anchor cell's first-year level; the model reads it as
    a **shape** and rescales it, so this is the divisor that turns a tabulated amount
    into a multiple of the mean.
    """
    tbl = data.claim_shape_table()                                   # noqa: F821
    return float((tbl["share"] * tbl["claim_amount"]).sum())


def shape_rel(bucket):
    """The bucket's annual rated 비급여 claim as a multiple of the distribution's mean.

    Dimensionless by construction, so the same shape serves every model point and every
    projection year: the level comes from :func:`claims_np_rated_pp` and only the
    dispersion comes from the table.
    """
    m = shape_mean()
    if m <= 0.0:
        return 0.0
    return float(data.claim_shape_table().loc[bucket,                # noqa: F821
                                              "claim_amount"]) / m


def band_of(amount):
    """The 요율 상대도 band of an annual rated 비급여 claim [S1 특별약관 제6조제3항].

    1단계 at ₩0 with no claim; 2단계 above zero and below ₩1,000,000; 3단계 to
    ₩1,500,000; 4단계 to ₩3,000,000; 5단계 at or above it.  A hard floor sits under the
    surcharge — 「할증은 … 보험금 지급실적이 연간 100만원 이상인 계약에 한하여 적용」
    [S1 특별약관 제6조제4항] — which is why 2단계 has a relativity of exactly 100%.
    """
    if amount <= 0.0:
        return 1
    if amount < band_thr_3:                                          # noqa: F821
        return 2
    if amount < band_thr_4:                                          # noqa: F821
        return 3
    if amount < band_thr_5:                                          # noqa: F821
        return 4
    return 5


def band_relativity(b):
    """r_b: the 요율 상대도 of band b, for b in 2..5 [S1 특별약관 제6조제3항].

    100% / 200% / 300% / 400%.  The 표준약관 states the factor as a 요율 상대도 and the
    press releases as a 할인·할증율 of − / +100% / +200% / +300% [R1] [R3]; they are the
    same numbers, and band 3 pays twice the base rate, band 4 three times and band 5 four
    times.  Band 1's factor is not a constant — it is solved, at :func:`reld_one`.
    """
    if b == 2:
        return reld_r2                                               # noqa: F821
    if b == 3:
        return reld_r3                                               # noqa: F821
    if b == 4:
        return reld_r4                                               # noqa: F821
    if b == 5:
        return reld_r5                                               # noqa: F821
    raise ValueError("band 1 is solved, not tabulated")


def band_share(y, b):
    """w_b(y): the share of contracts in band b at the renewal opening policy year y.

    **The band is memoryless**: 「보험금 지급(사고) 이력이 1년마다 초기화됩니다」 [R2], so
    the band at renewal ``y`` depends on the claim experience of year ``y - 1`` alone.
    There is no no-claims ladder and no chain to carry — the distribution is simply the
    claim-shape distribution rescaled to that year's mean rated claim, read against the
    fixed money thresholds.  In the first policy year there is no prior year, so every
    contract sits at 2단계, which is the 100% base.

    Because the thresholds are **fixed money amounts** and the claim level trends, the
    mix migrates into the surcharge bands year by year with nothing in the model
    changing.  That migration is the loop.
    """
    if y <= 1:
        return 1.0 if b == 2 else 0.0
    m = claims_np_rated_pp(y - 1)
    tot = 0.0
    for k in shape_buckets():
        if band_of(shape_rel(k) * m) == b:
            tot += shape_share(k)
    return tot


def reld_surcharge(y):
    """The surcharge pool at renewal y: the sum of ``w_b r_b`` over bands 2 to 5.

    This is the revenue the wording requires be distributed to the 1단계 contracts.
    """
    return sum(band_share(y, b) * band_relativity(b) for b in (2, 3, 4, 5))


def reld_solved(y):
    """r_1 solved from revenue neutrality at renewal y, before the discount cap.

    **The wording does not fix the discount; it fixes the constraint that determines
    it**: 「매년 상대도 적용 전·후의 총 보험료 수준이 일치하도록 3~5단계의 할증대상자의
    할증재원을 1단계(할인) 대상자들에게 분배할 경우 산출됨」 [S1].  The scheme is
    revenue-neutral **within the rider**, so ``Sum_b w_b r_b = 1`` and
    ``r_1 = (1 - Sum_{b>=2} w_b r_b) / w_1``.

    On the commencement band distribution 72.9 / 25.3 / 0.8 / 0.7 / 0.3 [R12] that gives
    ``0.302`` of surcharge pool and ``r_1 = 0.698 / 0.729 = 0.9575``, a **4.25%**
    discount.  The published values bracket it and one is outside: 「5% 내외」 at launch
    [R1], −5% 잠정 at commencement [R3], a 95% relativity in the wording's own
    illustration [S1], and a carrier writing it as 「α%」 rather than a number [S3].
    Solving rather than hard-coding is deliberate: it makes the scheme self-financing
    inside the model, which is what the wording requires, and it means a change to the
    band distribution propagates correctly instead of silently breaking neutrality.  On
    the FSC's alternative distribution 62.1 / 36.6 / 1.3 [R3] the same identity gives
    0.9791, a discount of only 2.1% — the sensitivity is material, which is why the two
    distributions are recorded rather than averaged.
    """
    w1 = band_share(y, 1)
    if w1 <= 0.0:
        return 1.0
    return (1.0 - reld_surcharge(y)) / w1


def reld_one(y):
    """r_1: the band-1 relativity actually applied at renewal y, after the discount cap.

    ``reld_disc_cap`` is a **[std]** floor under the discount at 5%, from the two
    published values [R1] [R3].  It does not bind at commencement, where the solved
    figure is 4.25%; it binds once the claim level has trended far enough that contracts
    have migrated into the surcharge bands and the pool would fund more than 5%.  From
    that point the scheme stops being revenue-neutral and the **average** rider premium
    rises above the base — which is the loop reaching the aggregate, and a feature of the
    design rather than of this implementation.
    """
    return max(reld_solved(y), 1.0 - reld_disc_cap)                  # noqa: F821


def reld_active(y):
    """Whether the 요율 상대도 is applied at the renewal opening policy year y.

    Off unless the rider is held and the model point elects it, and off for the first
    ``reld_start_year`` − 1 policy years: the clause was in the 4세대 wording from
    launch but its application was deferred three years 「충분한 통계 확보 등을 위하여」
    and commenced 2024-07-01 [R3] [R1], so a policy written in 2021 had three renewals at
    flat relativity before the loop switched on.  The same two-year deferral is being
    repeated on 5세대, whose differential starts 2028-05-06 [S3].
    """
    return reld_on() and y >= reld_start_year                        # noqa: F821


def reld_avg(y):
    """The average 요율 상대도 applied to the rider's premium in policy year y.

    ``w_1 r_1 + Sum_{b>=2} w_b r_b``.  Exactly 1 while the discount cap is slack, because
    that is what revenue neutrality means; above 1 once the cap binds.  The relativity
    applies to the **순보험료** — 「순보험료(특별약관의 순보험료 총액을 대상으로
    합니다)」 [S1] — and this model applies it to the rider's office premium and re-grosses
    at the same expense ratio, which is arithmetically identical **[std]** unless the
    rider's expense loading contains a fixed per-policy amount, which no retrieved
    document states either way.
    """
    if not reld_active(y):
        return 1.0
    return band_share(y, 1) * reld_one(y) + reld_surcharge(y)


def noclaim_share(y):
    """nc(y): the share of contracts earning the 무사고 할인 in policy year y.

    「직전 2년간 비급여 보험금(4대 중증질환 치료를 위한 보험금은 제외) 미수령시 차기
    1년간 보험료(급여(주계약) + 비급여(특약))의 10%를 할인」 [R1].  A **two-year**
    lookback where the relativity has one, applied to the **whole** office premium where
    the relativity touches only the rider, and it **stacks** with the band-1 discount:
    the launch release prints a three-year timeline in which years 1 and 2 give only the
    rider discount and year 3 adds the 10%.

    The two years are treated as independent **[std]** — nothing published gives the
    persistence of claiming from one year to the next — so the share is the product of
    the two years' no-claim shares.
    """
    if not noclaim_on() or y < 3:
        return 0.0
    return band_share(y - 1, 1) * band_share(y, 1)


# --- Premium ----------------------------------------------------------------

def basis_incr_ge(y):
    """b_ge(y): the 급여 unit's basis change at the renewal opening policy year y.

    **Not an input.**  Each priced unit is re-rated at its own claim trend, clipped to
    the ±25% corridor: 「갱신계약의 보험료는 매년 최대 25% 범위(나이의 증가로 인한
    보험료 증감분은 제외) 내에서 인상 또는 인하될 수 있습니다」 [S1 제30조제2항], now in
    the regulation itself at 감독규정 제7-63조제2항제3호 [REG-R17].  The corridor binds
    **per 위험구분단위**, not on the portfolio average, which is why the two units are
    clipped separately.  The rule is **[std]**; it is what keeps each unit's loss ratio
    stable unless the corridor clips it.
    """
    return max(-renewal_corridor,                                    # noqa: F821
               min(renewal_corridor,                                 # noqa: F821
                   med_trend_ge * trend_mult()))                     # noqa: F821


def basis_incr_np(y):
    """b_np(y): the 비급여 unit's basis change at the renewal opening policy year y.

    The same rule on the 비급여 trend.  At :func:`trend_mult` of 4.5 the unclipped
    re-rate would be 36.45% and the corridor holds it to 25%, so the rider's premium
    falls behind its own claim trend year after year — which is model point 10, and is
    the shape of the problem the supervisor's corridor creates for the insurer.
    """
    return max(-renewal_corridor,                                    # noqa: F821
               min(renewal_corridor,                                 # noqa: F821
                   med_trend_np * trend_mult()))                     # noqa: F821


def prem_ge_base(y):
    """base_ge(y): the 급여 주계약 기준보험료 a month in policy year y, KRW.

    ``base(y) = base(y-1) x (1 + a) x (1 + b_ge(y))``.  **The order of operations is the
    thing to get right**: the 표준약관's illustration labels its basis increment
    「전년도 기준보험료 x 25%」, but 3,640 is 25% of ``14,000 x 1.04`` and not of 14,000,
    so the corridor applies to the **age-adjusted** prior premium [S1 제30조].
    Reproducing the printed row 14,000 → 18,200 → 23,660 → 30,758 → 39,985 → 51,980
    requires it, and getting it wrong costs 4% of the corridor every year and compounds.
    """
    if y <= 1:
        return premium_mth_pp() * (1.0 - np_share())
    return prem_ge_base(y - 1) * (1.0 + age_load) \
        * (1.0 + basis_incr_ge(y))                                   # noqa: F821


def prem_np_base(y):
    """base_np(y): the 비급여 특약 기준보험료 a month in policy year y, KRW.

    The same recursion on the rider's own trend and its own corridor.  Zero where the
    특별약관 is not held.  This is the **base** premium, before the 요율 상대도: the
    corridor applies to the pre-relativity premium — 「요율 상대도 적용 전 보험료」
    [S1 특별약관 제6조제2항] [REG-R17 제7-63조제2항제3의2호] — so a band-5 policyholder
    can face ``1.25 x 4.00 = 5.00x`` the previous year's base rider rate in a single
    step.  That is the sharpest number in the product.
    """
    if not np_rider():
        return 0.0
    if y <= 1:
        return premium_mth_pp() * np_share()
    return prem_np_base(y - 1) * (1.0 + age_load) \
        * (1.0 + basis_incr_np(y))                                   # noqa: F821


def prem_gross_mth(y):
    """gross(y): the office premium a month in policy year y, KRW.

    ``[ base_ge(y) + base_np(y) x reld_avg(y) ] x (1 - 0.10 x nc(y))``.  Three things
    compose here and each is on a different clock: the annual attained-age re-rate inside
    the corridor, the one-year-lookback experience relativity on the rider alone, and the
    two-year-lookback 무사고 할인 on the whole premium.

    The 표준약관 extends its own illustration across the five bands and every row is
    reproduced by this formula at ``s = 0.4875``: at renewal +1,
    ``18,200 x (0.5125 + 0.4875 x 2) = 27,073``; at +2,
    ``23,660 x (0.5125 + 0.4875 x 4) = 58,263`` [S1].  That reproduction is the check
    that the composition is the right one, and it is where the 48.75% rider share
    implied by the wording comes from.
    """
    gross = prem_ge_base(y) + prem_np_base(y) * reld_avg(y)
    return gross * (1.0 - noclaim_disc * noclaim_share(y))           # noqa: F821


# --- Cash flows -------------------------------------------------------------

def premiums(t):
    """Premium income at the **start** of policy month t, an inflow.

    ``gross(y(t)) x l(t)``.  월납 (monthly) and level within the policy year, which is
    the only mode retrieved and the mode the whole published FSS premium series is
    quoted on [R7] [R8] [S3] [S4]; no 연납 or 일시납 variant was found and none is
    modelled.  Premiums cease on termination — the premium-paying period is coterminous
    with the one-year 보험기간 and renews with it — and there is **no 납입면제**: no
    premium-waiver clause appears in either retrieved 실손 wording, which is
    [unverified] as an absence rather than proved.
    """
    return prem_gross_mth(policy_year(t)) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo at the end of policy month t, by kind.

    ``"GE_IN"`` 급여 입원, ``"GE_OUT"`` 급여 통원, ``"NP_IN"`` 비급여 입원 including the
    상급병실료 차액, ``"NP_OUT"`` 비급여 통원 including the injection carve-out, and
    ``"NP_THREE"`` the three sub-limited 3대비급여 classes.  With no ``kind``, the sum.

    The annual claim of the policy year is spread **evenly across its twelve months**
    **[std]**.  Nothing published gives a within-year seasonality for this product, and
    the contract's own machinery — every limit, every counter, the co-payment cap and the
    relativity window — runs on the policy year, so the month is a presentation grid for
    an annual quantity rather than a unit of account.
    """
    if kind is None:
        return sum(claims(t, k) for k in
                   ("GE_IN", "GE_OUT", "NP_IN", "NP_OUT", "NP_THREE"))
    return pols_if(t) * claims_ann_pp(policy_year(t), kind) / 12.0


def expenses(t):
    """Maintenance expense at the end of policy month t.

    ``expense_maint_rate x premiums(t)``.  The only expense datum retrieved for this
    product is the aggregate: 손해조사비 plus 사업비 of about ₩2.9조 on ₩18.0조 of 2025
    premium — **16.1%** — which reconciles with the FSS's stated break-even loss ratio of
    about 85% [R7].  No 상품요약서 with a 사업비 disclosure was obtained for any
    generation, so the split into 6% acquisition and renewal commission, 7% maintenance
    and 3% claim handling is **[std]**, and :func:`check_expense_split` ties the three
    back to the published total.

    There is **no month-0 acquisition strain** here, and that is a product fact rather
    than an omission: on a one-year renewable contract renewed on a rolling basis the
    acquisition/renewal distinction has no content after year one, and what a sister
    library would call acquisition expense is carried in :func:`commissions` as a level
    rate on every premium.
    """
    return expense_maint_rate * premiums(t)                          # noqa: F821


def claim_expenses(t):
    """Claim handling expense at the end of policy month t, on its own line.

    ``expense_claim_rate x claims(t)``.  It stands beside :func:`expenses` rather than
    inside it because 손해조사비 is the component the FSS itself separates out [R7], and
    because the experience-rating machinery makes claim **frequency** a driver of expense
    as well as of benefit.  Nothing published splits the aggregate: the 3% is a **[std]**
    decomposition of a figure the FSS quotes as a percentage of *premium*, and the two
    bases coincide at a loss ratio of 100% — about where this line has actually run, 101.0%
    in 2025 [R7].  Making it proportional to claims is the **[std]** choice because that is
    what drives it.
    """
    return expense_claim_rate * claims(t)                            # noqa: F821


def commissions(t):
    """Commission outgo at the end of policy month t.

    ``comm_rate x premiums(t)``, level.  감독규정 제4-32조제5항 caps first-year
    commission on a 보장성보험 at the first year's premium, which is nowhere near binding
    at this level [REG-R22].  This limb carries the acquisition element of the 16%
    aggregate; see :func:`expenses` for why there is no separate first-year strain.
    """
    return comm_rate * premiums(t)                                   # noqa: F821


def net_cf(t):
    """net_cf(t): the net cash flow of policy month t, **income positive**.

    Premiums less every benefit limb, less maintenance expense, less claim handling
    expense, less commission.  The library-wide sign and the notes' own, so there is no
    outgo-positive ``liability_cf`` companion to publish.

    The shape to expect is not a sister library's.  There is **no new-business strain**:
    a one-year renewable contract with no reserve accumulation and a level expense rate
    starts positive and stays positive while the premium keeps pace with the claim.  What
    moves the margin is the interaction of three things on different clocks — the claim
    trend, which the two priced units re-rate against inside a corridor that can clip it;
    the age curve of utilisation, which the stylised 4% age loading does not track; and
    the experience relativity, which is neutral until the discount cap binds and then
    adds to the premium.  Year-1 claims on the anchor cell are 82.8% of year-1 premium,
    which reproduces the published 4세대 2022 combined loss ratio exactly.
    """
    return (premiums(t) - claims(t) - expenses(t)
            - claim_expenses(t) - commissions(t))


# --- Checks -----------------------------------------------------------------

def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - deaths - lapses - suspensions - renewal declines
    - maturities``.  Five decrements, and the middle two are what make this product's
    roll-forward different from a term assurance's: the 개인실손 중지 facility is a
    supervisory requirement rather than a product feature, and the annual renewal is an
    option the policyholder holds and the insurer does not.  Without them the
    roll-forward would appear to lose lives with no cause.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_lapse(t) - pols_suspend(t)
            - pols_renewal_decline(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the
    signed residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def check_net_cf_resid(t):
    """The cash flow statement residual in policy month t; zero everywhere.

    :func:`net_cf` against ``premiums - claims - expenses - claim_expenses -
    commissions``, with :func:`claims` summing over its own kinds exactly as
    ``result_cf()`` prints them.  A benefit limb present in the total but missing from
    the printed statement, or counted twice, shows up here; so does a claim expense
    folded back into :func:`expenses` instead of standing on its own line.
    """
    return net_cf(t) - (premiums(t) - claims(t) - expenses(t)
                        - claim_expenses(t) - commissions(t))


def check_net_cf():
    """True when the printed cash flow statement adds to ``net_cf`` in every month."""
    return all(abs(check_net_cf_resid(t)) <= cash_tol                # noqa: F821
               for t in range(proj_len()))


def check_claim_shape_resid():
    """The claim-shape distribution's two normalisation residuals; zero.

    The shares must sum to 1 and the relative amounts must average to 1 under those
    shares, or the band mix is a distribution over something other than the contracts in
    force and :func:`reld_solved` divides by the wrong denominator.  A negative share
    would pass both sums and is caught separately.
    """
    ks = shape_buckets()
    s = sum(shape_share(k) for k in ks)
    m = sum(shape_share(k) * shape_rel(k) for k in ks)
    neg = sum(max(0.0, -shape_share(k)) for k in ks)
    return abs(s - 1.0) + abs(m - 1.0) + neg


def check_claim_shape():
    """True when the claim-shape distribution is a proper distribution with mean 1."""
    return check_claim_shape_resid() <= shape_tol                    # noqa: F821


def check_band_shares_resid(y):
    """The 요율 상대도 band-share residual at renewal y; zero everywhere.

    The five band shares partition the in-force contracts, so they sum to 1 and none is
    negative.  A bucket that fell through :func:`band_of` — an amount that matched no
    band — would show here as a shortfall.
    """
    s = sum(band_share(y, b) for b in (1, 2, 3, 4, 5))
    neg = sum(max(0.0, -band_share(y, b)) for b in (1, 2, 3, 4, 5))
    return (s - 1.0) + neg


def check_band_shares():
    """True when the band shares partition the contracts in every policy year."""
    return all(abs(check_band_shares_resid(y)) <= roll_fwd_tol       # noqa: F821
               for y in range(1, policy_year(proj_len() - 1) + 1))


def check_relativity_neutral_resid(y):
    """The revenue-neutrality residual of the 요율 상대도 at renewal y; zero everywhere.

    The wording requires 「매년 상대도 적용 전·후의 총 보험료 수준이 일치하도록」 [S1] —
    the rider collects the same net premium before and after the relativity — so while
    the discount cap is slack ``Sum_b w_b r_b`` must be exactly 1.  Once the cap binds
    the scheme is *more* than neutral and the sum rises above 1; what must never happen
    is a scheme that funds a discount it has not collected, so the residual there is the
    shortfall below 1 rather than the excess above it.  Where the relativity is not in
    operation the average must be exactly 1, which is the third case.
    """
    if not reld_active(y):
        return reld_avg(y) - 1.0
    if reld_one(y) > reld_solved(y):
        return max(0.0, 1.0 - reld_avg(y))
    return reld_avg(y) - 1.0


def check_relativity_neutral():
    """True when the experience relativity is self-financing in every policy year."""
    return all(abs(check_relativity_neutral_resid(y)) <= roll_fwd_tol  # noqa: F821
               for y in range(1, policy_year(proj_len() - 1) + 1))


def check_renewal_corridor_resid(y):
    """The ±25% renewal corridor residual at renewal y; zero everywhere.

    Measured **per 위험구분단위** — separately on the 급여 unit and the 비급여 unit,
    because that is how 감독규정 제7-63조제2항제3호 states it [REG-R17] — and measured
    against the **age-adjusted** prior premium, which is the order of operations the
    표준약관's own illustration obeys [S1 제30조].  A residual here means either that the
    clip is missing or that the age loading has been applied on the wrong side of it.
    """
    if y <= 1:
        return 0.0
    resid = 0.0
    prev_ge = prem_ge_base(y - 1) * (1.0 + age_load)                 # noqa: F821
    if prev_ge > 0.0:
        resid += max(0.0, abs(prem_ge_base(y) / prev_ge - 1.0)
                     - renewal_corridor - 1e-12)                     # noqa: F821
    prev_np = prem_np_base(y - 1) * (1.0 + age_load)                 # noqa: F821
    if prev_np > 0.0:
        resid += max(0.0, abs(prem_np_base(y) / prev_np - 1.0)
                     - renewal_corridor - 1e-12)                     # noqa: F821
    return resid


def check_renewal_corridor():
    """True when neither priced unit moves more than 25% in a year, age effect excluded."""
    return all(check_renewal_corridor_resid(y) <= roll_fwd_tol       # noqa: F821
               for y in range(1, policy_year(proj_len() - 1) + 1))


def check_annual_limits_resid(y):
    """The contractual-limit residual in policy year y; zero everywhere.

    Every money and count limit the contract carries, tested at once: the two
    ₩50,000,000 annual aggregates across their 상해/질병 split, the three 3대비급여 money
    sub-limits, the 100-visit 비급여 통원 cap, the two 50-act counters and the per-visit
    cap on both outpatient limbs.  On every shipped model point the residual is zero
    because **none of these binds on a deterministic expectation** — see the Space
    docstring on ``E[min(X, L)] != min(E[X], L)`` — so what this check proves is that the
    machinery is wired, not that it is exercised.  Do not delete a limit because it reads
    slack.
    """
    resid = 0.0
    lim2 = 2.0 * annual_limit()
    resid += max(0.0, claims_ge_pp(y) - lim2 - 1e-6)
    resid += max(0.0, claims_np_main_pp(y) - lim2 - 1e-6)
    resid += max(0.0, claims_physio_pp(y) - limit_physio - 1e-6)     # noqa: F821
    resid += max(0.0, claims_inject_pp(y) - limit_inject - 1e-6)     # noqa: F821
    resid += max(0.0, claims_mri_pp(y) - limit_mri - 1e-6)           # noqa: F821
    resid += max(0.0, visits_np_eff(y) - visit_limit_np)             # noqa: F821
    resid += max(0.0, acts_physio_eff(y) - act_limit_three)          # noqa: F821
    resid += max(0.0, acts_inject_eff(y) - act_limit_three)          # noqa: F821
    tr_ge = trend_ge(y) * oop_trunc(y)
    resid += max(0.0, paid_out_per_visit(
        "ge_out", ded_clinic, retain_rate_ge(), tr_ge)               # noqa: F821
        - visit_cap() - 1e-6)
    resid += max(0.0, paid_out_per_visit(
        "ge_out", ded_hospital, retain_rate_ge(), tr_ge)             # noqa: F821
        - visit_cap() - 1e-6)
    resid += max(0.0, paid_out_per_visit(
        "np_out", ded_np_out, retain_rate_np(), trend_np(y))         # noqa: F821
        - visit_cap() - 1e-6)
    return resid


def check_annual_limits():
    """True when no contractual money or count limit is exceeded in any policy year."""
    return all(check_annual_limits_resid(y) <= roll_fwd_tol          # noqa: F821
               for y in range(1, policy_year(proj_len() - 1) + 1))


def check_indemnity_resid(y):
    """The indemnity residual in policy year y; zero everywhere.

    **The defining constraint of this product and of no other in the repository**: the
    contract reimburses an incurred cost, so the claim can never exceed the 보장대상
    의료비 that produced it — 「실제 발생한 손해(비용)를 초과하여 보험금을 지급하지
    않습니다」 [S1 제37조·제38조] [S3].  A co-payment applied as a multiplier instead of a
    retention, a deductible subtracted twice, or a per-visit cap applied to the wrong
    side of the deduction would all show here.
    """
    return max(0.0, claims_ann_pp(y) - loss_incurred_pp(y) - 1e-6)


def check_indemnity():
    """True when the claim never exceeds the incurred covered loss in any policy year."""
    return all(check_indemnity_resid(y) <= roll_fwd_tol              # noqa: F821
               for y in range(1, policy_year(proj_len() - 1) + 1))


def check_oop_ceiling_resid(y):
    """The 본인부담상한제 residual in policy year y; zero everywhere.

    The 급여 covered loss after truncation may not exceed the insured's own
    본인부담상한액, because anything above it is refunded by the NHIS and is excluded
    from cover outright [S1 제4조제3항제1호] [R10] [REG-R53].  On model point 8 the
    truncation binds and this is the check that says the exclusion was applied to the
    covered loss rather than to the benefit.
    """
    if not nhi_covered():
        return 0.0
    return max(0.0, oop_incurred_ge(y) * oop_trunc(y) - oop_ceiling() - 1e-6)


def check_oop_ceiling():
    """True when the truncated 급여 covered loss stays inside the public annual ceiling."""
    return all(check_oop_ceiling_resid(y) <= roll_fwd_tol            # noqa: F821
               for y in range(1, policy_year(proj_len() - 1) + 1))


def check_expense_split_resid():
    """The expense-split residual; zero.

    The 6% commission, 7% maintenance and 3% claim handling are a **[std]** split of one
    published aggregate — 손해조사비 plus 사업비 of about 16.1% of premium in 2025 [R7] —
    and the split must reconcile to it, or the model's margin is not the market's.
    """
    return (comm_rate + expense_maint_rate                           # noqa: F821
            + expense_claim_rate - expense_total_rate)               # noqa: F821


def check_expense_split():
    """True when the three expense components reconcile to the published aggregate."""
    return abs(check_expense_split_resid()) <= roll_fwd_tol          # noqa: F821


# --- Result tables ----------------------------------------------------------

def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is the start-of-month in-force probability, which is the weight applied
    to every cash flow on the same row.  ``net_cf`` carries the library's income-positive
    sign.  ``expenses`` is maintenance only and the claim handling expense stands beside
    it in its own ``claim_expenses`` column, which is what the two names mean
    library-wide.  The five ``claims_*`` columns are the split the contract itself makes
    — the two 급여 limbs of the 주계약, the two main 비급여 limbs of the 특약 and the
    3대비급여 classes with their own sub-limits — and they sum to the whole benefit
    outgo; there is deliberately no ``claims`` subtotal column beside them.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_ge_in": [claims(t, "GE_IN") for t in ts],
            "claims_ge_out": [claims(t, "GE_OUT") for t in ts],
            "claims_np_in": [claims(t, "NP_IN") for t in ts],
            "claims_np_out": [claims(t, "NP_OUT") for t in ts],
            "claims_np_three": [claims(t, "NP_THREE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements and decrement rates, indexed by policy month t."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_suspend": [pols_suspend(t) for t in ts],
            "pols_renewal_decline": [pols_renewal_decline(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_prem():
    """Result table of the renewal and experience-rating ledger, indexed by policy year.

    One row a policy year, because that is the clock the whole mechanism runs on.  The
    five band shares, the surcharge pool, the solved and the applied band-1 relativity,
    the average relativity, the 무사고 share and the two base premiums are all here, so
    that the loop can be read off a single frame rather than reconstructed from the cash
    flow statement.
    """
    ys = list(range(1, policy_year(proj_len() - 1) + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "claims_np_rated_pp": [claims_np_rated_pp(y) for y in ys],
            "band_1": [band_share(y, 1) for y in ys],
            "band_2": [band_share(y, 2) for y in ys],
            "band_3": [band_share(y, 3) for y in ys],
            "band_4": [band_share(y, 4) for y in ys],
            "band_5": [band_share(y, 5) for y in ys],
            "reld_surcharge": [reld_surcharge(y) for y in ys],
            "reld_solved": [reld_solved(y) for y in ys],
            "reld_one": [reld_one(y) for y in ys],
            "reld_avg": [reld_avg(y) for y in ys],
            "noclaim_share": [noclaim_share(y) for y in ys],
            "prem_ge_base": [prem_ge_base(y) for y in ys],
            "prem_np_base": [prem_np_base(y) for y in ys],
            "prem_gross_mth": [prem_gross_mth(y) for y in ys],
        },
        index=pd.Index(ys, name="policy_year"),                      # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

reentry_period = 5

reentry_cycles = 2

max_cover_age = 100

renewal_decline_rate = 0.01

retain_rate_ge_base = 0.20

retain_rate_np_base = 0.30

retain_rate_nonhi = 0.60

ded_clinic = 10000.0

ded_hospital = 20000.0

ded_np_out = 30000.0

cap_inpatient_retain = 2000000.0

room_rate = 0.50

room_cap_day = 100000.0

visit_limit_np = 100.0

act_limit_three = 50.0

physio_gate_acts = 10.0

physio_cont_prob = 0.60

limit_physio = 3500000.0

limit_inject = 2500000.0

limit_mri = 3000000.0

inject_carve_share = 0.25

share_injury = 0.15

med_trend_ge = 0.010

med_trend_np = 0.081

age_load = 0.04

renewal_corridor = 0.25

band_thr_3 = 1000000.0

band_thr_4 = 1500000.0

band_thr_5 = 3000000.0

reld_r2 = 1.0

reld_r3 = 2.0

reld_r4 = 3.0

reld_r5 = 4.0

reld_disc_cap = 0.05

reld_start_year = 4

reld_exempt_share = 0.15

noclaim_disc = 0.10

comm_rate = 0.06

expense_maint_rate = 0.07

expense_claim_rate = 0.03

expense_total_rate = 0.16

roll_fwd_tol = 1e-10

cash_tol = 1e-06

shape_tol = 1e-09

pd = ("Module", "pandas")
