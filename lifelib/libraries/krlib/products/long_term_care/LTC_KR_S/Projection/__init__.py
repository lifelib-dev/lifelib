# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.LTC_KR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace projecting
model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

``t`` counts **policy months**, 0-based. Month ``t`` runs from ``t`` to ``t + 1`` months
after the 계약일, so ``t = 0`` is the first projected month. ``proj_len()`` is the **number
of projected months**, the frame's exclusive end — ``12 x (term_age - issue_age) + 1``, so
601 on the anchor cell and 601 rows in :func:`result_cf`, indexed 0 to 600, and the frame is
``range(proj_len())``. The last row, ``t = proj_len() - 1``, is the 계약해당일 at 만나이
``term_age`` on which the contract matures with nothing payable: it holds the surviving
in-force count and no cash flow.

.. rubric:: The age basis

The projection runs on **만나이** (*man nai*, age last birthday), incremented at each
계약해당일: ``age(t) = issue_age + t // 12``. The contract itself ages on **보험나이**
(*boheom nai*, insurance age — 계약일 현재 실제 만 나이 with a fraction under six months
discarded and six months or more rounded up, 표준약관 제21조 [REG-R25]), and the two differ
for roughly half of all issue dates. The 만나이 basis is not a concession here, as it is on
the cancer chassis; it is the right basis twice over. Every public series the decrements are
built from — the 노인장기요양보험 통계연보 연령별 인정률, the 치매역학조사 prevalence and
the 생명표 behind the mortality — is published on 만나이; and the benefit definition itself
contains a 만나이 test, 「만 65세 이상 노인」 or 「노인성 질병을 가진 만 65세 미만의 자」.
The 보험나이 offset therefore survives only in the premium, which enters this model as a
model point input, so no conversion is applied anywhere.

.. rubric:: Notes symbol map

The technical notes use compact actuarial symbols; the cells use lifelib names.

===============  ==================================  ======================================
Notes symbol     Cells                               Meaning
===============  ==================================  ======================================
—                ``model_point``                     the selected model point as a Series
n                ``proj_len``                        number of projected policy months
x                ``issue_age``                       만나이 at the 계약일
x + floor(t/12)  ``age``                             attained 만나이 in month t
P                ``premium_mth_pp``                  level monthly office premium
A_B              ``lump_amount``                     장기요양진단급여금 sum insured
A_1 / A_2        ``annuity_high`` / ``annuity_low``  간병연금 monthly amount by entry grade
G_B              ``benefit_grade``                   the contractual 등급 threshold
q(x)             ``mort_rate``                       healthy annual mortality
q_C(x)           ``mort_rate_care``                  care-state annual mortality
P(x)             ``prev_rate_at``                    all-grade certification prevalence
P_C(x)           ``prev_care_at``                    prevalence at or above G_B
P_L(x)           ``prev_light_at``                   prevalence below G_B
i_D(x)           ``inc_rate_direct_at``              healthy -> care, direct entry
i_L(x)           ``inc_rate_light_at``               healthy -> light grade
rho(x)           ``prog_rate_at``                    light grade -> care, progression
l(t)             ``pols_if``                         in force at the start of month t
AV(t)            ``av_pp``                           계약자적립액 per policy at the start of month t
CV(t)            ``cv_pp``                           해약환급금 per policy on a lapse in month t
CF(t)            ``net_cf``                          net cash flow, income positive
===============  ==================================  ======================================

.. rubric:: The four compartments, and why there are four

The contract is a three-state model — healthy, in long-term care, dead — but the care state
is not entered in one step, and pretending it is puts the cash flow years too early. Only
**13.3%** of current 1등급 certifications arose from a first application, against 69.5% from
a renewal, whereas at 인지지원등급 the first-application share is 69.8%: severe-grade lives
are, in the main, people who entered the scheme years earlier at a light grade and
deteriorated. So the in-force block is carried in three compartments and a fourth absorbing
one:

:func:`pols_healthy`
    never certified. Pays premium, is exposed to lapse, carries healthy mortality.

:func:`pols_light`
    certified at a grade **below** ``benefit_grade()``. The contract does nothing for these
    lives — no benefit, no waiver — so they still pay premium and are still exposed to
    lapse, but they carry an impaired mortality and they are the pool progression draws
    from.

:func:`pols_care`
    certified at or above ``benefit_grade()``. The lump sum has been paid, the annuity is
    running, the premium is waived, surrender is barred by the 약관 and the mortality is the
    care-state one. Absorbing: the amount and the 감액 are both frozen at first
    certification and the annuity is metered on **survival**, not on continued
    certification, so the contract itself makes the state absorbing for cash-flow purposes.

:func:`pols_act` is the first two together — the premium-paying, lapse-exposed population —
and :func:`pols_if` is all three.

.. rubric:: Prevalence to incidence, which is the modelling work

The public statistics are a **prevalence**. Writing ``P`` for the all-grade certification
prevalence at 만나이 ``x``, ``s_G(x)`` for the share of certified lives at grade ``G`` or
above, ``P_C = s_G P`` and ``P_L = P - P_C``, and ``mu_H``, ``mu_L``, ``mu_C`` for the three
forces of mortality with ``mu_bar`` the population average, the compartment identities in a
stationary population are

    inflow_C(x) = P_C'(x) + P_C(x) (mu_C(x) - mu_bar(x))
    inflow_L(x) = P_L'(x) + P_L(x) (rho(x) + mu_L(x) - mu_bar(x))

The excess-mortality term is **not a refinement**: a rising prevalence understates entry
because the certified population is being drained by its own excess mortality, and that
drain is what the 간병연금 is exposed to as well. Two equations carry three unknowns —
direct entry, progression and light-grade entry — and the closing assumption is the one the
sources leave open: ``direct_entry_share`` **[std]**, the share of gross inflow into the
care state arriving straight from health rather than by progression, set at 0.20 from the
13.3% / 69.8% first-application split above. Then

    i_D(x) = direct_entry_share x inflow_C(x) / (1 - P(x))
    rho(x) = (1 - direct_entry_share) x inflow_C(x) / P_L(x)
    i_L(x) = inflow_L(x) / (1 - P(x))

Three properties of this construction belong in front of a reader rather than in a footnote.
It rests on a **stationary-population assumption [std]**: the cross-sectional 인정률 by age
is read as the prevalence path a cohort will follow, and the Korean certified stock grew
71.8% in six years, so the cross-section is not a cohort path and the identity **understates**
entry. It treats the care compartment as leaving only by death, whereas 9.2% of current
certifications arose from a 등급변경신청 and grades move both ways, which understates entry
again. And **below 65 there is no prevalence data at all**: the statute admits an under-65
applicant only through the closed 노인성 질병 list, so below 65 the two entry rates are
carried down from their age-65 values on the log-gradient of the one disclosed 예정위험률 —
13.0% a year for men, 17.9% for women — which is the only Korean long-term-care incidence
anyone publishes.

The level that construction produces is about a fifth of that disclosed 예정위험률 at the
same age. :func:`disclosed_inc_ratio_at` publishes the ratio rather than hiding it: a
예정위험률 is a *loaded* rate for a select, underwritten, 180-day-waited population on
보험나이, and the three biases named above all run the same way, so the gap is expected —
but it is the largest single uncertainty in this model and the technical notes carry it as a
sensitivity.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/long_term_care/``, read at run time rather than stored inside the model. Each
table has a filename Reference and a reader Cells, both on :mod:`~.LTC_KR_S.Data`, reached
here through the ``data`` Reference. The consequence worth knowing: **the model is not
portable on its own.** Copying the ``LTC_KR_S`` folder without its parent's CSVs produces a
model that reads and then fails on first evaluation.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

# --- the model point ---

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The policy identifier of the selected model point."""
    return str(model_point()["policy_id"])


def issue_age():
    """x: the 만나이 (*man nai*, age last birthday) at the 계약일.

    The composite issues from 30 to 70, the modal envelope of the long-term-care benefit
    itself rather than of the chassis carrying it **[std]**.  The contract ages on 보험나이;
    see the Space docstring for why this model does not convert.
    """
    return int(model_point()["issue_age"])


def sex():
    """The sex (M / F) of the insured: a rating factor, and a key into every basis table.

    It is the only rating factor besides age.  No smoker class, occupation class or amount
    band was disclosed on any long-term-care cover in any retrieved document.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def term_age():
    """The 만나이 at which the 보험기간 ends: 90 on the composite **[std]**.

    Observed 85 / 90 / 95 / 100세만기 and 종신; 90세만기 is the modal Korean maturity and the
    term of both published rate cards.  It **truncates the exposure at exactly the band
    carrying the highest certification rate of all** — 41.7% at 85 and over, and still
    rising — so the choice is materially conservative on claim cost, and 95 and 100 are
    shipped as model points.
    """
    return int(model_point()["term_age"])


def prem_period_years():
    """The 납입기간 in years: 20 on the composite **[std]**.

    20년납 is the basis of both published rate cards, it is the 해약공제계수 cap of 별표 14
    [REG-R20], and it is structurally necessary to the 미지급형 form — the surrender value is
    a step at **납입완료**, and a 전기납 contract has no step because it has no 납입완료
    before maturity.
    """
    return int(model_point()["prem_period_years"])


def prem_period_mths():
    """n_P: the 납입기간 in policy months, ``12 x prem_period_years()``."""
    return 12 * prem_period_years()


def prem_mode():
    """The 납입주기: 월납 on every model point, which is why the grid is monthly.

    Monthly is the dominant retail mode and the mode of every published rate card in the
    file.  감독규정 제7-65조제2항 expressly permits the 계약자적립액 to be computed
    「연납보험료를 기준으로」 [REG-R18], which is how a Korean monthly-premium product
    reconciles a monthly grid with an annually-recursed account.
    """
    v = str(model_point()["prem_mode"])
    if v != "monthly":
        raise ValueError("only 월납 is in scope")
    return v


def benefit_grade():
    """G_B: the contractual 장기요양등급 threshold, cumulative from the top of the scale.

    ``g1`` is 1등급 only, ``g2`` is 1~2등급 (the composite), through to ``g6`` for
    1~인지지원등급.  Every retrieved contract draws its threshold downward from 1등급 and
    **no retrieved document sells a 3등급-only or 5등급-only benefit**.  Widening the gate is
    not a re-scaling: at 1~5등급 the benefit is exposed to a population about 7.5 times
    larger and arriving materially earlier, which the market prices at about 4.5 : 1.
    """
    v = str(model_point()["benefit_grade"])
    if v not in ("g1", "g2", "g3", "g4", "g5", "g6"):
        raise ValueError("invalid benefit_grade")
    return v


def lump_amount():
    """A_B: the 장기요양진단급여금, ₩10,000,000 on the composite.

    Paid **최초 1회한** on the first award at or above ``benefit_grade()``, extinguishing
    that benefit line but **not** the contract: the 간병연금 keeps running and the dementia
    rider stays in force.  The level is the unit of both published rate cards, and it is a
    third of the cancer chassis's ₩30,000,000 because a long-term-care benefit sits on top of
    a public scheme that already meets most of the direct service cost.
    """
    return float(model_point()["lump_amount"])


def annuity_on():
    """True where the 간병연금 rider is attached.  On in the base run."""
    return bool(model_point()["annuity_on"])


def annuity_high():
    """A_1: the monthly 간병연금 where the **entry** grade is 1등급, ₩500,000 [S1].

    Frozen at first certification — 「그 이후에 장기요양등급이 변경되더라도 지급액은 변경되지
    않습니다」 — so a life entering at 2등급 and deteriorating to 1등급 keeps the lower rate
    for all ten years.
    """
    return float(model_point()["annuity_high"])


def annuity_low():
    """A_2: the monthly 간병연금 at any other grade inside the gate, ₩300,000 [S1].

    The one carrier that grades its annuity by grade grades it in two steps only, so every
    grade below 1등급 inside the threshold is carried at the lower amount **[std]**.
    """
    return float(model_point()["annuity_low"])


def annuity_max_mths():
    """n_A: the 간병연금 ceiling in months — 「10년(120개월)을 최고한도로 지급」 [S1].

    The cap is the composite's protection against a post-onset mortality basis nobody
    publishes, and it is one reason this shape was preferred over the uncapped 종신 form on
    the shelf.  It binds jointly with maturity: the annuity is truncated at the earlier of
    the cap and the 보험기간, which is the conservative reading of a question no retrieved
    document resolves **[std]**.
    """
    return int(model_point()["annuity_max_mths"])


def annuity_guar_mths():
    """The guaranteed months of 간병연금, 「최초 1년(12개월) 보증지급」 [S1].

    Instalments inside the guarantee are paid whether or not the insured survives; after it
    each block of twelve is released only by the annual survival test on the anniversary of
    the 진단확정일, evidenced by a 주민등록등본.
    """
    return int(model_point()["annuity_guar_mths"])


def dementia_rider():
    """True where the 치매진단급여금 rider is attached.  Off on the anchor cell.

    A different trigger — the CDR 척도 assessed by a 치매 전문의, not the 등급판정위원회 —
    with a different sex basis and its own one-year waiting period, which is why it is off in
    the base run.  It is **not** an independent process: dementia is simultaneously a route
    into the public grade and a private trigger, so the rider's incidence is driven off the
    same underlying certification model.
    """
    return bool(model_point()["dementia_rider"])


def dementia_amount():
    """The 치매진단급여금 at CDR 1 이상 (경도치매상태), ₩10,000,000 where attached.

    Paid once only across the tier set, behind a **one-year** 보장개시일 and, inside the
    definition of the state itself, a **90-day persistence** test — together deferring a
    mild-dementia claim by at least fifteen months from inception.
    """
    return float(model_point()["dementia_amount"])


def wait_mths():
    """The 장기요양상태 보장개시일 in whole months: 3 on the composite **[std]**.

    「계약일부터 그 날을 포함하여 90일이 지난 날의 다음 날」, with a carve-back to the 계약일
    where the cause is 재해.  The observed market runs from **no waiting period at all**
    through 90 days to 180 days, and 90 days is the median and aligns this product with the
    cancer chassis's 암보장개시일, so the two ``krlib`` third-sector products share one
    waiting-period mechanic.  A certification inside the window does **not** defer the claim:
    it makes the benefit **무효** and the premiums paid for it come back — see
    :func:`pols_void`.
    """
    return int(model_point()["wait_mths"])


def red_mths():
    """The 감액기간 in months: 12 on the composite **[std]**.

    Where the certification is 질병-caused and the 판정일 falls inside the window the benefit
    is halved; where the cause is 상해/재해 it is paid in full.  The observed market runs
    from no reduction through one year at 50% to two years at 50%.  The 감액 decision is
    **frozen at first certification** for the whole life of the annuity — a claim starting
    inside the window stays halved for all ten years — which is the single most easily
    mis-modelled rule in the product.
    """
    return int(model_point()["red_mths"])


def cv_form():
    """The surrender-value form: ``mijigeup``, ``half_during`` or ``pyojun``.

    Four forms are on the shelf and they are **different products, not variants**, though
    the Korean names look almost identical.  ``mijigeup`` (해약환급금 미지급형) pays
    **nothing** during the premium-paying period and 50% of a notional 기본형 value
    afterwards, and is the composite: **63.8% of Korean 보장성 초회보험료 in 2024 H1 was
    written in a 무·저해지 form** [REG-R27], so a library modelling only 표준형 would be
    modelling a minority of the market.  ``half_during`` (납입중50%해약환급금지급형) pays 50%
    **during** and 100% after.  ``pyojun`` (표준형) pays the full 계약자적립액 less the
    해약공제액 from year 1.
    """
    v = str(model_point()["cv_form"])
    if v not in ("mijigeup", "half_during", "pyojun"):
        raise ValueError("invalid cv_form")
    return v


def lapse_form():
    """The lapse vector: ``mujihae`` (the regulated log-linear model) or ``pyojun``.

    The vector on a 무해지 form is **not free**.  Among models converging to zero lapse at
    완납 the 로그-선형 모형 is the **원칙모형** with a practical convergence point of 0.1%
    and a post-완납 ultimate of 0.8%; anything else is permitted only against disclosure in
    the audit report and the 경영공시, external actuarial verification, quarterly reporting
    of the difference to the FSS in CSM, best-estimate liability, K-ICS ratio and net income,
    and submission to an on-site inspection [REG-R27].  ``pyojun`` is the level comparison
    vector, carried so the two can be compared — which is the comparison the guidance
    requires an insurer to disclose.
    """
    v = str(model_point()["lapse_form"])
    if v not in ("mujihae", "pyojun"):
        raise ValueError("invalid lapse_form")
    return v


def uw_loading():
    """The 간편심사 premium multiplier: 1.0 fully underwritten, 1.40 simplified **[std]**.

    The cleanest published measure of the price of relaxed underwriting in Korean long-term
    care is 1.36-1.43x on the main contract at every age and sex.  It is carried as a
    **premium** multiplier only: no retrieved source gives the simplified pool's incidence
    separately, so on a loaded model point the extra premium is pure margin in this model and
    the true claim cost of that pool is understated.  Note that one carrier will not attach
    its 장기요양 riders to a simplified chassis at all, which is itself a statement about
    anti-selection on this trigger.
    """
    return float(model_point()["uw_loading"])


def premium_mth_pp():
    """P: the level monthly office premium per policy, a model point **input**.

    Not a computed quantity.  **No Korean carrier publishes a long-term-care rate card at
    the composite's specification**, so the anchor cell's ₩5,600 is constructed from two rows
    of the one published card — ₩3,300 for the 주계약 장기요양(1~2등급)급여금 at male 40 plus
    ₩2,320 for a 재가급여 support rider scaled to the composite's grade-weighted ₩400,000 a
    month — and the female cell's ₩8,400 the same way **[std]**.  On this model's own basis the
    anchor premium buys a benefit outgo whose present value at the 예정이율 is **46.0%** of the
    present value of premium income, and the female cell's 51.5%; the seven other model points
    carry premiums set at approximately that ratio, landing between **22% and 44%** once the
    threshold, the annuity cap, the term and the 간편심사 loading are applied — the 22% being
    model point 8, whose 1.40 loading is pure margin here because no retrieved source gives the
    simplified pool's own incidence.  :func:`uw_loading` multiplies it.
    """
    return uw_loading() * float(model_point()["premium"])


def pols_if_init():
    """l(0): the in-force count the projection opens on, one policy.

    Every model point is a single new-business policy at duration zero, so the opening
    exposure is 1 and :func:`result_cf` opens at ``t = 0``.
    """
    return 1.0


# --- the timeline ---

def proj_len():
    """n: the **number** of projected policy months, ``12 (term_age() - issue_age()) + 1``.

    601 on the anchor cell — a 만나이-40 life to the 90세 계약해당일.  ``proj_len()`` is the
    **exclusive end** of the frame and not the last index: ``result_cf()`` carries
    ``proj_len()`` rows indexed 0 to ``proj_len() - 1`` and the frame is
    ``range(proj_len())``.  The ``+ 1`` is the terminal row — the 600 months of cover are
    ``t = 0 ... proj_len() - 2`` and ``t = proj_len() - 1`` is the 90세 계약해당일 itself,
    the maturity instant: the contract ends there with **nothing payable**, there being no
    만기환급금 on a 순수보장성 contract.
    """
    return 12 * (term_age() - issue_age()) + 1


def age(t):
    """age(t): the attained **만나이** in policy month t, ``x + floor(t / 12)``."""
    return issue_age() + t // 12


def policy_year(t):
    """y(t): the policy year containing month t, ``t // 12 + 1``.

    The **contractual** policy-year label, which is 1-based by convention: month ``t = 0``
    falls in policy year 1.  It is derived from the 0-based index and is never the index
    itself; only :func:`lapse_rate` reads it, the 로그-선형 lapse model being written in
    policy years.
    """
    return t // 12 + 1


# --- mortality ---

def mort_rate_at_age(x):
    """The healthy-life annual mortality of this life's sex at 만나이 ``x``.

    A **[std] Makeham-Gompertz construction** calibrated on the published 제10회 경험생명표
    65세 기대여명 [REG-R33]; the table itself is not published [REG-R34].  Read at 만나이
    without adjustment, and with no best-estimate factor applied: the calibration anchor is
    an experience statistic, not a valuation margin, so there is nothing to unwind.  Keyed by
    age rather than by ``t`` because the morbidity construction has to evaluate the whole
    basis at 만나이 65 when the life is younger than that.
    """
    return float(data.mort_table().loc[(sex(), min(x, 120)),         # noqa: F821
                                       "mort_rate"])


def mort_rate(t):
    """q(x): the healthy-life annual mortality at ``age(t)``."""
    return mort_rate_at_age(age(t))


def mort_rate_mth(t):
    """q_H(t): monthly healthy mortality, ``1 - (1 - q)^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def mort_rate_light(t):
    """The annual mortality of a life certified **below** the benefit threshold.

    ``light_mort_mult x q(x)``, capped at 1, with ``light_mort_mult = 1.8`` **[std]**.  No
    retrieved source gives a post-certification mortality table by grade.  The multiple sits
    between healthy and care because the one retrieved study of certified decedents finds a
    mean 인정점수 at death of 82.1 — squarely inside 2등급 — so the deaths are concentrated
    in the severe grades and a light-grade life is materially healthier than the cohort that
    study observed.  There is **no observed range**.
    """
    return min(1.0, light_mort_mult * mort_rate(t))                  # noqa: F821


def mort_rate_light_mth(t):
    """q_L(t): monthly light-grade mortality **[std]**."""
    return 1.0 - (1.0 - mort_rate_light(t)) ** (1.0 / 12.0)


def mort_rate_care(t):
    """q_C(x): the annual mortality of a life in the certified care state at ``age(t)``.

    ``care_mort_mult x q(x)``, capped at 1, with ``care_mort_mult = 3.0`` **[std]**.  Anchored
    on two things and neither is a table.  The yearbook roll-forward and the application-route
    estimator agree that the mean duration of a certification is near **4 to 5.5 years**, and
    the mean 만나이 of a certified decedent is over 75; at 만나이 82 on the shipped mortality
    table a mean duration of 4.5 years implies a force of 0.222 against a healthy force of
    0.075, a multiple of 2.96.  The one retrieved study measuring time from certification to
    death — 516.2 days, 8.7% inside a month, 45.6% inside a year — is a **right-censored
    decedent cohort** and is a lower bound rather than an estimate of the duration, which is
    why it fixes the early shape here and not the level.

    ``care_mort_mult`` is **not** only a post-onset assumption: it is also the excess-mortality
    term of the incidence identity in :func:`inflow_care_at`, so it moves the entry rate and
    the annuity's run-off in opposite directions at once.  That coupling is the least obvious
    property of this model and the technical notes vary it in a sensitivity.
    """
    return min(1.0, care_mort_mult * mort_rate(t))                   # noqa: F821


def mort_rate_care_mth(t):
    """q_C(t): monthly care-state mortality **[std]**."""
    return 1.0 - (1.0 - mort_rate_care(t)) ** (1.0 / 12.0)


def mort_rate_dem_mth(t):
    """The monthly mortality carried by the dementia rider's own ledger **[std]**.

    ``dem_mort_mult x q(x)`` on an annual basis with ``dem_mort_mult = 2.5``, between the
    light-grade and the care-state multiples: a CDR 1 diagnosis is a lighter state than a
    1·2등급 certification and a heavier one than a 3~5등급.  No source gives it.
    """
    return 1.0 - (1.0 - min(1.0, dem_mort_mult * mort_rate(t))) ** (1.0 / 12.0)  # noqa: F821


# --- lapse ---

def lapse_param(name):
    """One parameter of the lapse vector, from *lapse_table.csv*."""
    return float(data.lapse_table().loc[name, "value"])              # noqa: F821


def lapse_rate(t):
    """The **annual** lapse rate in the policy year of month t.

    On the ``mujihae`` form the regulated **log-linear** principle model [REG-R27]: the
    first-year rate decays geometrically in policy year to the 0.1% convergence point in the
    year 납입완료 falls in, and the post-완납 ultimate rate is 0.8%.  On the ``pyojun`` form
    a level rate at every duration, carried for comparison.  The first-year level is **[std]**
    — no Korean durational persistency series was retrieved — while the shape and the two
    convergence values are the guidance's own.

    Note what the vector says on a contract that has **no soft landing**: with no surrender
    value there is no policy loan and therefore no 보험료 자동대출납입, so a missed premium
    lapses the contract outright, and the assumption nonetheless has lapse *falling* toward
    납입완료.
    """
    if lapse_form() == "pyojun":
        return lapse_param("lapse_level_std")
    y = policy_year(t)
    n = prem_period_years()
    if y > n:
        return lapse_param("lapse_ultimate")
    first = lapse_param("lapse_year1")
    last = lapse_param("lapse_completion")
    if n <= 1:
        return last
    return first * (last / first) ** ((y - 1) / (n - 1))


def lapse_rate_mth(t):
    """w(t): the monthly lapse rate, ``1 - (1 - lapse_rate(t))^(1/12)`` **[std]**.

    Applied to :func:`pols_healthy` and :func:`pols_light` only.  A life in the care state
    is not exposed: the premium is waived, and the 약관 bars surrender outright once the
    annuity has started — 「최초 지급사유가 발생한 후에는 이 특약을 해지할 수 없습니다」 —
    so zero lapse in that state is a **constraint** and not an assumption.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


# --- the morbidity basis: prevalence ---

def prev_param(name):
    """One parameter of the certification-prevalence logistic for this life's sex.

    ``prev_ceil``, ``prev_beta`` and ``prev_x_mid`` are the **[std]** parameters of the
    three-parameter logistic fitted to the five sourced 연령별 인정률 of the 2024
    노인장기요양보험 통계연보; the file also carries the five anchors themselves.
    """
    return float(data.prevalence_table().loc[(sex(), name), "value"])  # noqa: F821


def prev_rate_at(x):
    """P(x): the all-grade certification prevalence at 만나이 ``x``.

    A logistic in age **[std]**, ``prev_ceil / (1 + exp(-beta (x - x_mid)))``, fitted to the
    five sourced band rates — 1.98% at 65-69 rising to 28.6% at 85 and over for men, 1.63% to
    47.3% for women.  Two features of the sourced curve survive the fit and matter: the
    gradient is about **17% per year of age**, a factor of 23 over twenty years; and the
    **sex crossover is at about 70** — male certification exceeds female below it and female
    exceeds male above — which is the reverse of a death-benefit table and is independently
    confirmed by the disclosed 예정위험률, whose sex ratio crosses one between about 62 and 68.

    **Nothing above 88.5 is sourced, and that is where the claims are.**  The fitted ceiling
    is the parameter the tail is most sensitive to and the fit has one degree of freedom more
    than the data identifies; the technical notes carry the sensitivity.
    """
    ceil = prev_param("prev_ceil")
    beta = prev_param("prev_beta")
    x_mid = prev_param("prev_x_mid")
    return ceil / (1.0 + math.exp(-beta * (x - x_mid)))              # noqa: F821


def prev_slope_at(x):
    """P'(x): the derivative of :func:`prev_rate_at` in age, a rate per year.

    The **analytic** derivative of the logistic, ``beta P (1 - P / ceil)``, not a difference
    quotient: it is the leading term of the incidence identity and a numerical derivative
    would put noise straight into the claim rate.
    """
    ceil = prev_param("prev_ceil")
    beta = prev_param("prev_beta")
    p = prev_rate_at(x)
    return beta * p * (1.0 - p / ceil)


def share_ge_at(grade, x):
    """s_G(x): the share of certified lives at ``grade`` or above at 만나이 ``x``.

    Linear in age between the six sourced band representative ages — 60 for the under-65
    band, then 67, 72, 77, 82 and 88.5 — and flat outside them.  A **proportion of a
    population**, never a rate.  Carrying it by age rather than as one all-ages vector is
    load-bearing: the 1~2등급 share is **U-shaped**, 22.2% below 65, 11.1% at 80-84 and 14.8%
    at 85 and over, and a model applying a single vector at all ages mis-prices this benefit
    by up to a factor of two.
    """
    tbl = data.grade_share_table().loc[grade]                        # noqa: F821
    ages = sorted(float(a) for a in tbl.index)
    if x <= ages[0]:
        return float(tbl.loc[ages[0], "share_ge"])
    if x >= ages[-1]:
        return float(tbl.loc[ages[-1], "share_ge"])
    for lo, hi in zip(ages[:-1], ages[1:]):
        if lo <= x <= hi:
            v_lo = float(tbl.loc[lo, "share_ge"])
            v_hi = float(tbl.loc[hi, "share_ge"])
            return v_lo + (v_hi - v_lo) * (x - lo) / (hi - lo)
    raise ValueError("age out of range")


def share_slope_at(grade, x):
    """s_G'(x): the slope of :func:`share_ge_at` in age, per year.

    Exact for the piecewise-linear share: the constant slope of the bracketing segment, zero
    outside the sourced range.  It enters :func:`prev_care_slope_at` as the first half of the
    product rule, and it is **negative** over most of the range for a severe threshold, which
    is the U-shape doing its work.
    """
    tbl = data.grade_share_table().loc[grade]                        # noqa: F821
    ages = sorted(float(a) for a in tbl.index)
    if x < ages[0] or x >= ages[-1]:
        return 0.0
    for lo, hi in zip(ages[:-1], ages[1:]):
        if lo <= x < hi:
            v_lo = float(tbl.loc[lo, "share_ge"])
            v_hi = float(tbl.loc[hi, "share_ge"])
            return (v_hi - v_lo) / (hi - lo)
    return 0.0


def prev_care_at(x):
    """P_C(x): the prevalence of certification at or above ``benefit_grade()``.

    ``s_G(x) P(x)``.  On the composite's 1~2등급 gate this is only about a seventh of the
    all-grade prevalence — **1·2등급 are 13.28% of all certified lives**, against 50.8% for
    the comparable Japanese quantity, so a Korean 「1~2등급」 promise is a far narrower one
    than a Japanese 「要介護2以上」 promise.
    """
    return share_ge_at(benefit_grade(), x) * prev_rate_at(x)


def prev_care_slope_at(x):
    """P_C'(x): the full derivative of :func:`prev_care_at`, by the product rule.

    ``s_G'(x) P(x) + s_G(x) P'(x)``.  The first term is usually negative and the second
    always positive; dropping the first would overstate the entry rate wherever the severe
    share is falling with age, which is most of the range.
    """
    return (share_slope_at(benefit_grade(), x) * prev_rate_at(x)
            + share_ge_at(benefit_grade(), x) * prev_slope_at(x))


def prev_light_at(x):
    """P_L(x): the prevalence of certification **below** ``benefit_grade()``.

    ``P(x) - P_C(x)``, the pool progression draws from.  Zero by construction where the gate
    is ``g6``, since 1~인지지원등급 admits every certified life and there is no light state
    left outside it.
    """
    return prev_rate_at(x) - prev_care_at(x)


def prev_light_slope_at(x):
    """P_L'(x): the derivative of :func:`prev_light_at`, ``P'(x) - P_C'(x)``."""
    return prev_slope_at(x) - prev_care_slope_at(x)


# --- the morbidity basis: prevalence to incidence ---

def mort_force_at(x):
    """mu_H(x): the force of healthy mortality at 만나이 ``x``, ``-ln(1 - q(x))``.

    The compartment identities are written in forces rather than in annual rates, because a
    rate difference is not a hazard difference and the excess-mortality term of the identity
    is a difference of hazards.
    """
    return -math.log(1.0 - min(0.999999, mort_rate_at_age(x)))       # noqa: F821


def mort_force_light_at(x):
    """mu_L(x): the force of mortality of a light-grade life **[std]**."""
    q = min(0.999999, light_mort_mult * mort_rate_at_age(x))         # noqa: F821
    return -math.log(1.0 - q)                                        # noqa: F821


def mort_force_care_at(x):
    """mu_C(x): the force of mortality of a life in the care state **[std]**."""
    q = min(0.999999, care_mort_mult * mort_rate_at_age(x))          # noqa: F821
    return -math.log(1.0 - q)                                        # noqa: F821


def mort_force_avg_at(x):
    """mu_bar(x): the population-average force of mortality at 만나이 ``x``.

    ``(1 - P) mu_H + P_L mu_L + P_C mu_C``.  It is the term that turns a *count* identity
    into a *proportion* identity: prevalence is measured against a living population, and a
    population that is itself dying faster than a healthy life raises every prevalence it
    measures.  Using ``mu_C`` alone in place of ``mu_C - mu_bar`` overstates the entry rate,
    materially so at the ages where the certified share is large.
    """
    return ((1.0 - prev_rate_at(x)) * mort_force_at(x)
            + prev_light_at(x) * mort_force_light_at(x)
            + prev_care_at(x) * mort_force_care_at(x))


def inflow_care_at(x):
    """The gross rate of entry into the care compartment per unit of population at ``x``.

    ``P_C'(x) + P_C(x) (mu_C(x) - mu_bar(x))``, floored at zero.  The second term is where
    the care state's own mortality enters the **incidence** basis, and it is not a
    refinement: a prevalence that is rising understates entry, because the compartment it
    measures is being drained by an excess mortality the population around it does not carry.
    The same ``care_mort_mult`` that produces this term also runs the annuity off, so the two
    move together under a sensitivity and not independently.
    """
    return max(0.0, prev_care_slope_at(x)
               + prev_care_at(x) * (mort_force_care_at(x) - mort_force_avg_at(x)))


def prog_rate_at(x):
    """rho(x): the annual rate at which a light-grade life progresses to the benefit grade.

    ``(1 - direct_entry_share) x inflow_C(x) / P_L(x)``, capped at ``prog_rate_cap``, and
    zero where the gate admits every certified life so that there is no light state.

    ``direct_entry_share = 0.20`` is the **[std]** closing assumption of the conversion and
    the one number the sources leave genuinely open.  Its anchor is the yearbook's own
    application-route table: only **13.3%** of current 1등급 certifications arose from a
    first application (7,371 of 55,340) against 69.5% from a renewal, whereas at
    인지지원등급 — a grade nobody can progress *down* into — the first-application share is
    **69.8%**.  The ratio of the two is where 0.20 comes from.  Getting this wrong does not
    change the lifetime claim count much; it changes **when** the claim arrives, which on a
    contract priced at 2.0% over fifty years is most of the answer.
    """
    pl = prev_light_at(x)
    if pl <= 1e-12:
        return 0.0
    return min(prog_rate_cap,                                        # noqa: F821
               (1.0 - direct_entry_share) * inflow_care_at(x) / pl)  # noqa: F821


def inc_rate_direct_at(x):
    """i_D(x): the annual rate of **direct** entry into the care state from health.

    ``direct_entry_share x inflow_C(x) / (1 - P(x))`` where there is a light state, and the
    whole inflow where the gate leaves none.  Below 65 the rate is carried down from its
    age-65 value on :func:`sub65_factor_at`, because the statute admits an under-65 applicant
    only through the closed 노인성 질병 list and no prevalence data exists there at all.
    """
    xe = max(float(x), float(sub65_age))                             # noqa: F821
    pl = prev_light_at(xe)
    share = direct_entry_share if pl > 1e-12 else 1.0                # noqa: F821
    rate = share * inflow_care_at(xe) / (1.0 - prev_rate_at(xe))
    return rate * sub65_factor_at(x)


def inc_rate_light_at(x):
    """i_L(x): the annual rate of entry from health into a grade below the threshold.

    ``[P_L'(x) + P_L(x) (rho(x) + mu_L(x) - mu_bar(x))] / (1 - P(x))``, floored at zero and
    carried below 65 on :func:`sub65_factor_at` like the direct rate.  The floor binds only
    where the light-grade prevalence is falling faster than progression and mortality can
    account for, which the fitted curves do not do inside any shipped model point's range;
    it is there so that a replacement basis cannot produce a negative entry rate silently.
    """
    xe = max(float(x), float(sub65_age))                             # noqa: F821
    inflow = (prev_light_slope_at(xe)
              + prev_light_at(xe) * (prog_rate_at(xe) + mort_force_light_at(xe)
                                     - mort_force_avg_at(xe)))
    return max(0.0, inflow) / (1.0 - prev_rate_at(xe)) * sub65_factor_at(x)


def disclosed_inc_at(x):
    """The disclosed 예정위험률 for a combined 1·2등급 benefit at 만나이 ``x``.

    The sum of the 요양(1등급) and 요양(2등급) 발생률 of the one carrier that publishes them,
    log-linearly graduated between the three quoted ages and extrapolated on the end
    gradients outside them.  Summing the two rows is an **upper bound**, the two events being
    mutually exclusive at first certification.  This is a *pricing* rate for a select,
    underwritten, 180-day-waited population quoted on 보험나이 and it is **not** this model's
    level; it is read here for its gradient and its sex ratio, and published against the
    model's own rate by :func:`disclosed_inc_ratio_at`.
    """
    tbl = data.incidence_table().loc[sex()]                          # noqa: F821
    ages = sorted(int(a) for a in tbl.index)
    def rate(a):
        return float(tbl.loc[a, "rate_g1"]) + float(tbl.loc[a, "rate_g2"])
    lo, hi = ages[0], ages[-1]
    if x <= lo:
        a, b = ages[0], ages[1]
    elif x >= hi:
        a, b = ages[-2], ages[-1]
    else:
        a, b = next((p, q) for p, q in zip(ages[:-1], ages[1:]) if p <= x <= q)
    g = math.log(rate(b) / rate(a)) / (b - a)                        # noqa: F821
    return rate(a) * math.exp(g * (x - a))                           # noqa: F821


def sub65_gradient():
    """The log-gradient of the disclosed 예정위험률 per year of age, for this life's sex.

    ``ln(i(60) / i(40)) / 20`` on the combined 1·2등급 rate: **0.1222 for men (13.0% a year)**
    and **0.1648 for women (17.9%)**.  It is the only Korean evidence anywhere on how
    long-term-care incidence behaves below 65, and it carries the sex ratio with it — female
    over male on the combined rate runs 0.37 at 40, 0.58 at 50 and 0.87 at 60, so a curve
    built on this gradient crosses one in the late sixties, exactly where the population data
    finds the crossover.
    """
    tbl = data.incidence_table().loc[sex()]                          # noqa: F821
    ages = sorted(int(a) for a in tbl.index)
    lo, hi = ages[0], ages[-1]
    r_lo = float(tbl.loc[lo, "rate_g1"]) + float(tbl.loc[lo, "rate_g2"])
    r_hi = float(tbl.loc[hi, "rate_g1"]) + float(tbl.loc[hi, "rate_g2"])
    return math.log(r_hi / r_lo) / (hi - lo)                         # noqa: F821


def sub65_factor_at(x):
    """The factor carrying the entry rates below 65, ``exp(-g (65 - x))``; 1 at 65 and over.

    **[std]**, and it is a scope decision rather than a fitted quantity.  The 인정률 series
    is published for the 65-and-over population only; below 65 the scheme admits an applicant
    only with one of the 25 노인성 질병 the 시행령 lists — four dementia codes, one Alzheimer
    code, fourteen cerebrovascular codes, four Parkinson-family codes and four others — with
    **no cancer, no musculoskeletal condition and no frailty category** on the list.  So the
    under-65 exposure is both small and concentrated, and the only Korean evidence on its
    shape is the disclosed 예정위험률's own gradient, which is what this applies.  The
    progression rate is **not** scaled: it is a property of a life already certified, not of
    the gate.
    """
    if x >= sub65_age:                                               # noqa: F821
        return 1.0
    return math.exp(-sub65_gradient() * (sub65_age - x))             # noqa: F821


def disclosed_inc_ratio_at(x):
    """The model's own first-entry rate at ``x`` over the disclosed 예정위험률 at ``x``.

    Published rather than hidden, because it is the largest single uncertainty in this model.
    The model's first-entry rate is direct entry plus progression by lives already certified
    at a light grade, both read on the same sub-65 convention the projection uses — the whole
    basis is evaluated at ``xe = max(x, 65)`` and carried down on :func:`sub65_factor_at`::

        i_D(x) + P_L(xe) rho(xe) sub65_factor_at(x) / (1 - P_C(xe))

    Reading ``P_L`` and ``rho`` at ``x`` itself below 65 instead — the shorter form the
    identity suggests — mixes an unscaled light-grade prevalence with a scaled direct rate and
    returns 0.267 at 만나이 40 rather than the 0.240 published here.  On the shipped basis the
    ratio runs at roughly **one fifth** of the disclosed rate at ages 40 to 60.  Four things all
    point the same way and none of them is quantified by any retrieved source: a 예정위험률
    is a loaded pricing rate and not a best estimate; the conversion reads a **cross-section**
    as a cohort path in a scheme whose certified stock grew 71.8% in six years; the care
    compartment is treated as leaving only by death when 9.2% of certifications arose from a
    등급변경신청; and the disclosed card is quoted on 보험나이, about half a year older than
    this model's 만나이.  The technical notes carry the gap as a stated sensitivity rather
    than closing it with an invented factor.
    """
    xe = max(float(x), float(sub65_age))                             # noqa: F821
    model_rate = (inc_rate_direct_at(x)
                  + prev_light_at(xe) * prog_rate_at(xe) * sub65_factor_at(x)
                  / (1.0 - prev_care_at(xe)))
    return model_rate / disclosed_inc_at(x)


def inc_rate_direct(t):
    """i_D: the annual direct-entry rate into the care state in month t."""
    return inc_rate_direct_at(age(t))


def inc_rate_light(t):
    """i_L: the annual entry rate into a light grade in month t."""
    return inc_rate_light_at(age(t))


def prog_rate(t):
    """rho: the annual progression rate from a light grade to the benefit grade in month t."""
    return prog_rate_at(age(t))


def inc_rate_direct_mth(t):
    """The monthly direct-entry rate, ``i_D / 12`` **[std]**, uniform within the policy year."""
    return inc_rate_direct(t) / 12.0


def inc_rate_light_mth(t):
    """The monthly light-grade entry rate, ``i_L / 12`` **[std]**."""
    return inc_rate_light(t) / 12.0


def prog_rate_mth(t):
    """The monthly progression rate, ``rho / 12`` **[std]**."""
    return prog_rate(t) / 12.0


# --- the dementia rider's own basis ---

def dem_param(name):
    """One parameter of the dementia-prevalence logistic, from *dementia_table.csv*."""
    return float(data.dementia_table().loc[name, "value"])           # noqa: F821


def dem_prev_at(x):
    """The prevalence of dementia at CDR 1 or above at 만나이 ``x``, for this life's sex.

    A logistic **[std]** fitted to the five sourced band prevalences of the 2023 치매역학조사
    — 4.99% at 65-69, 5.03% at 70-74, 10.70% at 75-79, 15.57% at 80-84 and 21.18% at 85 and
    over — times the sourced 65+ sex factor, 0.957 for men and 1.035 for women.  Every
    dementia case is CDR 1 or above by definition, CDR 0.5 being 경도인지장애 and not
    dementia, so this is the prevalence the composite's 경도이상 tier is exposed to; a
    benefit written at CDR 3 이상 would reach about a third of it.

    Two weaknesses are named rather than smoothed.  The 65-69 and 70-74 anchors are almost
    equal, which no logistic can reproduce, and the fit is out by up to 31% at 70-74.  And
    the sex factor is **flat in age** while the sourced series has the male rate above the
    female at 65-79 and below it at 80 and over — which is why this model does not reproduce
    the market fact that 치매 covers are priced *cheaper* for women while 장기요양 covers are
    priced dearer.
    """
    ceil = dem_param("dem_ceil")
    beta = dem_param("dem_beta")
    x_mid = dem_param("dem_x_mid")
    factor = dem_param("dem_factor_m" if sex() == "M" else "dem_factor_f")
    return factor * ceil / (1.0 + math.exp(-beta * (x - x_mid)))     # noqa: F821


def dem_prev_slope_at(x):
    """The analytic derivative of :func:`dem_prev_at` in age."""
    ceil = dem_param("dem_ceil")
    beta = dem_param("dem_beta")
    factor = dem_param("dem_factor_m" if sex() == "M" else "dem_factor_f")
    p = dem_prev_at(x) / factor
    return factor * beta * p * (1.0 - p / ceil)


def dem_inc_rate_at(x):
    """The annual rate of a first CDR 1 이상 diagnosis at 만나이 ``x``.

    The same prevalence-to-incidence identity the certification basis uses, with the
    dementia state's own excess mortality in it, and carried below 65 on
    :func:`sub65_factor_at`.  Building the rider off a *sourced* prevalence rather than off a
    share of the certification rate matters, because the two triggers are correlated but not
    proportional: dementia is the **sole** qualifying condition for 5등급 and 인지지원등급 and
    is present in 42.3% of certified decedents, yet most CDR 1 lives are nowhere near a
    1·2등급 certification.
    """
    xe = max(float(x), float(sub65_age))                             # noqa: F821
    p = dem_prev_at(xe)
    q = min(0.999999, dem_mort_mult * mort_rate_at_age(xe))          # noqa: F821
    mu_d = -math.log(1.0 - q)                                        # noqa: F821
    mu_h = mort_force_at(xe)
    mu_bar = (1.0 - p) * mu_h + p * mu_d
    return max(0.0, dem_prev_slope_at(xe) + p * (mu_d - mu_bar)) / (1.0 - p) \
        * sub65_factor_at(x)


def dem_inc_rate_mth(t):
    """The monthly rate of a first CDR 1 이상 diagnosis in month t **[std]**.

    Zero unless the rider is attached, and zero for the first ``dementia_wait_mths`` months.
    Fifteen months is the **one-year 보장개시일 plus the 90-day persistence test written into
    the definition of the state itself** — 「진단일부터 90일 이상 계속되어 장래에 더 이상의
    호전을 기대할 수 없는」 — and the two together are why a naive prevalence-based pricing of
    a CDR 1 benefit is badly wrong at short durations.  The one-year waiting period is not a
    carrier choice: it is the settled market answer to the 2019 supervisory intervention that
    followed the 경증치매 boom.
    """
    if not dementia_rider() or t < dementia_wait_mths:               # noqa: F821
        return 0.0
    return dem_inc_rate_at(age(t)) / 12.0


# --- the four compartments ---

def pols_healthy(t):
    """h(t): in force and **never certified**, at the start of policy month t.

    ``h(0) = pols_if_init()``, then

        h(t+1) = ( h(t) - n_L(t) - n_D(t) ) (1 - q_H(t)) (1 - w(t))

    Premium-paying and lapse-exposed, on healthy mortality.  The lives leaving by
    :func:`pols_entry_care_direct` leave whether the certification triggers the benefit or
    voids it inside the 보장개시일 window, which is why the same term serves both.
    """
    if t <= 0:
        return pols_if_init() if t == 0 else 0.0
    if t >= proj_len():
        return 0.0
    s = t - 1
    return (pols_healthy_mid(s) * (1.0 - mort_rate_mth(s))
            * (1.0 - lapse_rate_mth(s)))


def pols_light(t):
    """l_L(t): in force and certified at a grade **below** ``benefit_grade()``.

    ``l_L(0) = 0``, then

        l_L(t+1) = ( l_L(t) + n_L(t) - n_P(t) ) (1 - q_L(t)) (1 - w(t))

    The contract does nothing for these lives — the benefit, the waiver and the annuity all
    fire at ``benefit_grade()`` and no retrieved Korean contract pays anything at a lower
    grade — so they keep paying premium and keep lapsing, on an impaired mortality.  They are
    the pool :func:`pols_entry_care_prog` draws from, and on the composite's 1~2등급 gate they
    are about six sevenths of all certified lives.
    """
    if t <= 0 or t >= proj_len():
        return 0.0
    s = t - 1
    return (pols_light_mid(s) * (1.0 - mort_rate_light_mth(s))
            * (1.0 - lapse_rate_mth(s)))


def pols_care(t):
    """l_C(t): in force and certified at or above ``benefit_grade()``.

    ``l_C(0) = 0``, then ``l_C(t+1) = ( l_C(t) + n_C(t) ) (1 - q_C(t))``.

    Absorbing, and the contract is drafted so that it is: the 진단급여금 cannot be
    re-triggered, the 간병연금's amount is fixed by the grade at **first** certification and
    「그 이후에 장기요양등급이 변경되더라도 지급액은 변경되지 않습니다」, and the instalments
    are metered on **survival** rather than on continued certification.  No lapse — the
    premium is waived and the 약관 bars surrender — and no recovery, which is a real
    simplification the *contract* makes rather than one this model imposes.
    """
    if t <= 0 or t >= proj_len():
        return 0.0
    s = t - 1
    return pols_care_mid(s) * (1.0 - mort_rate_care_mth(s))


def pols_healthy_mid(t):
    """The never-certified count after the month's certifications, before mortality."""
    return (pols_healthy(t) - pols_entry_light(t)
            - pols_entry_care_direct(t))


def pols_light_mid(t):
    """The light-grade count after the month's certifications, before mortality."""
    return pols_light(t) + pols_entry_light(t) - pols_entry_care_prog(t)


def pols_care_mid(t):
    """The care-state count after the month's certifications, before mortality.

    The month's voided certifications are **not** here: inside the 보장개시일 window the
    benefit is 무효 and the life leaves the model, so they appear in :func:`pols_void`.
    """
    return pols_care(t) + pols_entry_care(t)


def pols_act(t):
    """The **premium-paying, lapse-exposed** population: healthy plus light-grade.

    Premium income is charged on this, not on :func:`pols_if`.  Because the waiver fires at
    the same grade as the benefit rather than below it, there is **no band of lives paying
    nothing and claiming nothing** — the Japanese product's characteristic mis-modelled item
    does not exist here — but the waiver is still not free: it stops the premium for as long
    as the insured survives in the care state, which is exactly the quantity the
    prevalence-to-incidence conversion cannot pin down.
    """
    return pols_healthy(t) + pols_light(t)


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy month t.

    ``pols_act(t) + pols_care(t)``: alive, not lapsed, not voided and not matured, whether or
    not the premium is being waived.  ``pols_if(0) = pols_if_init() = 1``.  This is the
    weight on every cash flow of the same :func:`result_cf` row.  On the frame's last row,
    ``t = proj_len() - 1``, it is the count that reaches the 90세 계약해당일, and it is paid
    **nothing**: there is no 만기환급금 on a 순수보장성 contract.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    return pols_act(t) + pols_care(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after certification and mortality, before lapse — the processing order is
        **certification, then mortality, then lapse** **[std order]** — so this is the
        population lapses are taken from, plus the care lives that are not exposed to them.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return (pols_healthy_mid(t) * (1.0 - mort_rate_mth(t))
                + pols_light_mid(t) * (1.0 - mort_rate_light_mth(t))
                + pols_care_mid(t) * (1.0 - mort_rate_care_mth(t)))
    if timing == "AFT_DECR":
        return pols_if(t + 1)
    raise ValueError("invalid timing")


# --- certifications ---

def pols_entry_light(t):
    """n_L(t): expected entrants into a light grade in month t, ``h(t) i_L_m(t)``.

    Drawn from the never-certified population alone.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return pols_healthy(t) * inc_rate_light_mth(t)


def pols_entry_care_direct(t):
    """n_D(t): expected **direct** entrants into the care state, ``h(t) i_D_m(t)``.

    The catastrophic route — a major stroke, an early dementia — which is the only way in
    below 65 and is the minority route above it.  One fifth of gross inflow into the care
    state on the shipped ``direct_entry_share`` **[std]**.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return pols_healthy(t) * inc_rate_direct_mth(t)


def pols_entry_care_prog(t):
    """n_P(t): expected entrants into the care state **by progression**, ``l_L(t) rho_m(t)``.

    The dominant route above 65, and the reason this model has a light compartment at all: a
    single-decrement model that treats the 1·2등급 rate as a healthy-life incidence
    overstates direct entry, understates the delay, and puts the cash flow years too early.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return pols_light(t) * prog_rate_mth(t)


def pols_entry_care(t):
    """n_C(t): expected first certifications at or above the threshold that **pay**.

    ``n_D(t) + n_P(t)``, and **zero inside the 보장개시일 window**: a certification there does
    not defer the claim, it makes the benefit 무효 — 「특약을 무효로 하며, 이미 납입한
    보험료를 돌려드립니다」 — and unlike the cancer chassis there is no cancellation option and
    no revival, so the benefit is simply gone.  Those lives are :func:`pols_void`.
    """
    if t < 0 or t >= proj_len() - 1 or t < wait_mths():
        return 0.0
    return pols_entry_care_direct(t) + pols_entry_care_prog(t)


def pols_void(t):
    """Lives certified inside the 보장개시일 window, whose cover is void.

    The benefit is 무효 and **the premiums paid for it are returned**; the contract, whose
    main cover is that benefit, ends.  A distinct decrement rather than a claim refusal,
    because the two have different cash flows and the 약관 keep them apart: before the
    보장개시일 the contract is void and premiums come back, inside the 감액기간 cover has
    started and the benefit is merely halved.  On the composite the window is three months
    at an issue age of 40, so the decrement is of order 1e-7 of the cohort — carried because
    it is a product fact, not because it is material.
    """
    if t < 0 or t >= proj_len() - 1 or t >= wait_mths():
        return 0.0
    return pols_entry_care_direct(t) + pols_entry_care_prog(t)


# --- the other decrements ---

def pols_death_act(t):
    """Deaths in month t among lives that have **not** claimed: healthy and light-grade.

    These are the deaths that pay the **계약자적립액**: 감독규정 제7-63조제1항제1호 requires a
    제3보험 contract to pay it, plus the 미경과보험료, on death from a cause the policy does
    not cover, and terminate [REG-R17] [REG-R25 제22조].  Death is therefore not a pure
    decrement on this product, which is a direct consequence of the Korean third-sector
    design rule and has no counterpart in the Japanese contract.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return (pols_healthy_mid(t) * mort_rate_mth(t)
            + pols_light_mid(t) * mort_rate_light_mth(t))


def pols_death_care(t):
    """Deaths in month t among lives in the certified care state.

    These pay **nothing**: 「지급사유가 발생한 후 사망한 경우에는 별도로 책임준비금을 지급하지
    않습니다」.  On this product most deaths of claimants happen here, which is what makes the
    split from :func:`pols_death_act` a cash-flow distinction rather than a bookkeeping one.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return pols_care_mid(t) * mort_rate_care_mth(t)


def pols_death(t):
    """Expected deaths in month t across all three compartments."""
    return pols_death_act(t) + pols_death_care(t)


def pols_lapse(t):
    """Lapses at the end of month t, from the mortality survivors of the paying population.

    Care lives are not exposed — the premium is waived and the 약관 bars surrender.  What a
    lapse pays is :func:`cv_pp`, which on the composite's 미지급형 form is **nil for the whole
    premium-paying period** and 50% of a notional 기본형 value afterwards: a cliff, not a
    curve.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return ((pols_healthy_mid(t) * (1.0 - mort_rate_mth(t))
             + pols_light_mid(t) * (1.0 - mort_rate_light_mth(t)))
            * lapse_rate_mth(t))


def pols_maturity(t):
    """Policies reaching the 보험기간's end at ``t = proj_len() - 1``, nil at every other t.

    They are paid **nothing**: 「이 상품은 순수보장성보험으로 보험계약 만기시 지급받는
    금액(만기환급금)이 없습니다」.  The count is published because the roll-forward has to
    close on the last row, and because a maturity that pays nothing is still a maturity.
    """
    return pols_if(t) if t == proj_len() - 1 else 0.0


# --- the dementia rider's ledger ---

def pols_dem(t):
    """In force and already paid the 치매진단급여금; a first-event counter, not a compartment.

    Once only across the tier set.  Carried on the dementia state's own mortality and held at
    or below :func:`pols_if`, so that :func:`pols_entry_dem` always draws from a non-negative
    pool.  Nested inside the in-force block and **never added to** the three compartments.
    """
    if t <= 0 or t >= proj_len() or not dementia_rider():
        return 0.0
    s = t - 1
    carried = ((pols_dem(s) + pols_entry_dem(s))
               * (1.0 - mort_rate_dem_mth(s)))
    return min(pols_if(t), carried)


def pols_entry_dem(t):
    """Expected first CDR 1 이상 diagnoses under the rider in month t.

    ``(l(t) - pols_dem(t)) x dem_inc_rate_mth(t)``.  Zero unless the rider is attached.  The
    two triggers are **correlated, not independent**: a contract carrying both a 장기요양 and
    a 치매 benefit pays both on the same underlying event, at different times and on different
    evidence, and treating them as independent decrements understates the tail.  Driving both
    off the same life with a shared underlying state is what this model does about that.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return (pols_if(t) - pols_dem(t)) * dem_inc_rate_mth(t)


# --- the 간병연금 ledger ---

def care_surv(s, t):
    """S_C(s, t): survival in the care state from month s to month t.

    The **partial product** of ``(1 - q_C(u))`` over ``u = s ... t-1``, computed as a partial
    product and never as a ratio of cumulative products: ``q_C`` reaches 1 at the terminal age
    of the table, so a cumulative product underflows to zero and the ratio form divides by
    zero exactly where the tail of this liability lives.
    """
    if t <= s:
        return 1.0
    return care_surv(s, t - 1) * (1.0 - mort_rate_care_mth(t - 1))


def red_factor(t):
    """r(t): the 감액 factor applying to a certification dated in month t.

    ``1`` from ``red_mths()`` on; before that ``1 - (1 - red_fraction) x disease_share``.
    The 약관 test is on the **cause**, not on the grade: a 질병-caused certification inside
    the window is paid at ``red_fraction`` = 50%, an 상해/재해-caused one in full.  **The
    relative frequency of the two is given by no retrieved source**, so ``disease_share`` =
    0.95 is **[std]** and the accident carve-out is named rather than dropped; the blended
    factor is 0.525.  Frozen at first certification for the whole life of the annuity — see
    :func:`ann_amount_at`.
    """
    if t >= red_mths():
        return 1.0
    return 1.0 - (1.0 - red_fraction) * disease_share                # noqa: F821


def ann_amount_at(s):
    """A(s): the monthly 간병연금 of the cohort first certified in month s, frozen at entry.

    The blend of ``annuity_high()`` at 1등급 and ``annuity_low()`` at every other grade inside
    the gate, weighted by the **age-specific** grade shares at ``age(s)``, times the 감액
    factor at ``s``.  Both the amount and the reduction are frozen: 「최초 진단 확정일을
    기준으로 … 지급액이 결정되며 … 그 이후에 도래하는 매년 진단 확정일이 계약일부터 2년
    이상에 해당하더라도 … 지급액은 변경되지 않습니다」.  **A model that re-tests the 감액 at
    each instalment date overstates every claim arising in the first policy year**, which is
    the single most easily mis-modelled rule in the product.

    Below 만나이 65 the grade blend is read **at** 65, for the same reason the entry rates are:
    the whole sub-65 basis is the age-65 basis carried down on :func:`sub65_factor_at`, and
    mixing an age-65 incidence with the under-65 severity mix — which is genuinely more severe,
    22.2% of certified lives at 1·2등급 against 16.8% at 65 — would be internally inconsistent
    **[std]**.  It moves nothing: under-65 claims are of order 1e-5 of the anchor cell's.
    """
    if not annuity_on():
        return 0.0
    x = max(float(age(s)), float(sub65_age))                         # noqa: F821
    s_g1 = share_ge_at("g1", x)
    s_gb = share_ge_at(benefit_grade(), x)
    blended = (s_g1 * annuity_high() + (s_gb - s_g1) * annuity_low()) / s_gb
    return blended * red_factor(s)


def ann_count(t):
    """The expected number of 간병연금 instalments falling due in month t.

    Instalments are **monthly**; the cohort certified in month ``s`` is paid in months
    ``s ... s + n_A - 1``, of which the first ``annuity_guar_mths()`` are guaranteed against
    death and each later block of twelve is released only by the annual survival test on the
    anniversary of the 진단확정일::

        ann_count(t) = sum over u = 0 ... n_A-1 of  n_C(t - u) x weight(u)
        weight(u)    = 1                        for u < annuity_guar_mths()
                     = S_C(t - u, t - u + 12 floor(u / 12))   otherwise

    The first instalment falls in the **month of certification**, so the ``u = 0`` term is
    :func:`pols_entry_care` itself.  The cap and the maturity truncation bind jointly: nothing
    is paid on the maturity row ``t = proj_len() - 1`` or after it, which understates the
    benefit for a late entrant whose ten years of annuity outrun his five years of remaining
    term.
    """
    if not annuity_on() or t < 0 or t >= proj_len() - 1:
        return 0.0
    total = 0.0
    for u in range(0, min(t, annuity_max_mths() - 1) + 1):
        s = t - u
        if u < annuity_guar_mths():
            w = 1.0
        else:
            w = care_surv(s, s + 12 * (u // 12))
        total += pols_entry_care(s) * w
    return total


def ann_pay(t):
    """The 간병연금 outgo of month t, the instalment ledger valued at each cohort's own amount.

    The same sum as :func:`ann_count` with ``ann_amount_at(s)`` inside it, which is what
    carries the freeze: a cohort entering at 만나이 68 keeps its own grade-blended amount and
    its own 감액 decision for all ten years, whatever later cohorts are paid.
    """
    if not annuity_on() or t < 0 or t >= proj_len() - 1:
        return 0.0
    total = 0.0
    for u in range(0, min(t, annuity_max_mths() - 1) + 1):
        s = t - u
        if u < annuity_guar_mths():
            w = 1.0
        else:
            w = care_surv(s, s + 12 * (u // 12))
        total += ann_amount_at(s) * pols_entry_care(s) * w
    return total


def ann_tests(t):
    """The expected number of annual 간병연금 survival tests falling due in month t.

    One per surviving claimant on each anniversary of the 진단확정일 after the first, up to
    the cap.  It is an **administrative event**, not an actuarial abstraction — 「매년 진단
    확정일에 피보험자의 주민등록등본을 제출하여야 합니다」 — which is why the claim-handling
    expense is charged on it rather than on every monthly instalment.
    """
    if not annuity_on() or t <= 0 or t >= proj_len() - 1:
        return 0.0
    total = 0.0
    for k in range(1, annuity_max_mths() // 12):
        s = t - 12 * k
        if s < 0:
            continue
        total += pols_entry_care(s) * care_surv(s, t)
    return total


# --- the 계약자적립액 and the 해약환급금 ---

def cum_prem_pp(t):
    """The cumulative office premium paid per policy by the start of month t.

    ``P x min(t, n_P)`` — the premiums received at ``0 ... t-1``, that is, everything paid
    **before** month t's own premium.  It is the denominator of the published 환급률
    progression, which is quoted at policy anniversaries where no further premium has yet
    fallen due.

    The refund on a voided cover is **not** this quantity but ``cum_prem_pp(t + 1)``: the
    premium of month t is received at the *start* of the month and the void is recognised at
    the *end* of it, so a life voided in month t has paid ``t + 1`` premiums and 「이미 납입한
    보험료를 돌려드립니다」 returns all of them.  See :func:`claims`.
    """
    return premium_mth_pp() * min(t, prem_period_mths())


def prem_accum_factor(t):
    """The accumulated value at month t of t monthly payments of 1 in advance, at 예정이율.

    ``(1 + j) ((1 + j)^t - 1) / j`` with ``j = (1 + prem_int_rate)^(1/12) - 1``.
    ``prem_int_rate`` is **2.0% 연단위 복리** and is the one place in ``krlib`` where the
    pricing interest rate is a *retrieved* figure rather than a [std] one: one carrier states
    it in terms in a 기초서류 extract — 「주계약 및 특약에 적용한 예정이율은 연단위 복리
    2.0%입니다」 — where no Korean carrier publishes one for the cancer chassis.  Three
    cautions travel with it: it is a 2023-vintage rate, it is a 우정사업본부 rate written
    outside 보험업법, and it prices a different benefit mix.  It is preferred to an invented
    figure, and at 2.0% against the chassis's [std] 2.50% it is the more conservative of the
    two on a benefit payable forty years out.
    """
    if t <= 0:
        return 0.0
    j = (1.0 + prem_int_rate) ** (1.0 / 12.0) - 1.0                  # noqa: F821
    return (1.0 + j) * ((1.0 + j) ** t - 1.0) / j


def av_ratio_at(fraction):
    """The 계약자적립액 as a ratio to cumulative premiums, at ``fraction`` of the way from
    납입완료 to maturity.

    Linear between the four sourced anchors of *av_table.csv*: **0.974** at 납입완료, 1.088
    one third of the way on, 1.010 two thirds, and **0.000** at maturity.  They are the
    published 해약환급금 미지급형 환급률 progression — 48.7% / 54.4% / 50.5% / 0.0% at 20, 30,
    40 and 50 years on the anchor cell's own specification — doubled, because that form pays
    50% of the notional 기본형 value once the premiums are paid and the 해약공제 has expired.
    Indexing on the *fraction* rather than on the policy year is the **[std]** step that lets
    one published progression serve every term and every paying period.
    """
    tbl = data.av_table()                                            # noqa: F821
    xs = sorted(float(v) for v in tbl.index)
    if fraction <= xs[0]:
        return float(tbl.loc[xs[0], "av_ratio"])
    if fraction >= xs[-1]:
        return float(tbl.loc[xs[-1], "av_ratio"])
    for lo, hi in zip(xs[:-1], xs[1:]):
        if lo <= fraction <= hi:
            v_lo = float(tbl.loc[lo, "av_ratio"])
            v_hi = float(tbl.loc[hi, "av_ratio"])
            return v_lo + (v_hi - v_lo) * (fraction - lo) / (hi - lo)
    raise ValueError("fraction out of range")


def net_prem_ratio():
    """The net premium as a fraction of the office premium, **derived** not assumed.

    ``av_ratio_at(0) x n_P / prem_accum_factor(n_P)``: the fraction that, accumulated at the
    예정이율 over the premium-paying period, reproduces the sourced 계약자적립액 at 납입완료.
    On the anchor cell it is **0.7932**, implying a 예정사업비 loading of 20.7% — which no
    Korean 산출방법서 or 사업방법서 was retrieved to check, but which is what the published
    환급률 progression and the published 예정이율 imply between them.  Deriving it rather
    than assuming it is what makes the surrender-value cliff reproduce the carrier's own
    figures instead of merely resembling them.
    """
    n = prem_period_mths()
    return av_ratio_at(0.0) * n / prem_accum_factor(n)


def av_pp(t):
    """AV(t): the 계약자적립액 per policy at the start of month t.

    Two branches meeting at 납입완료.  Up to it, the accumulation of the net premium at the
    예정이율; after it, the sourced run-off carried on ``av_ratio_at``.  The quantity matters
    because 감독규정 제7-63조제1항제1호 makes it payable on death from a cause the contract
    does not cover [REG-R17], and on this product a third of the cohort dies that way before
    maturity — so **death is a decrement with a large cash flow attached**, which the Japanese
    counterpart does not have at all.

    Two reconstruction assumptions are named rather than buried.  The published progression is
    the *미지급형's* 환급률 against its own premiums, and the model reads the doubled figure as
    that contract's own 계약자적립액; the 기본형 comparator is a product that **cannot be
    bought** — 「'기본형'은 … 가입이 불가능하며 … 해지율을 적용하지 않고 계산합니다」 — and
    its premium is higher, so the two accounts are not in fact the same quantity **[std]**.
    And the run-off between the sourced anchors is linear **[std]**, where the real curve bends
    with the risk cost.
    """
    n = prem_period_mths()
    if t <= n:
        return net_prem_ratio() * premium_mth_pp() * prem_accum_factor(t)
    return (av_ratio_at((t - n) / (proj_len() - 1 - n))
            * premium_mth_pp() * n)


def surr_chg_pp(t):
    """The 해약공제액 per policy in month t, on the 표준형 form only.

    ``surr_chg_ratio x P`` running off straight-line over the 해약공제기간, which is the
    premium-paying period **capped at seven years** [REG-R19 제7-66조제1항].  The level is the
    supervisor's own rule of thumb for a 보장성보험 — a 표준해약공제액 of **13 times the
    monthly premium** — which is how 별표 14's formula in 연납순보험료 and 보험가입금액 is
    carried in Korean practice [REG-R29] [REG-R20].  The rule of thumb is used here rather
    than the formula because 별표 15 제9호 computes the notional 보험가입금액 of a contract with
    no death benefit as a ratio of risk premiums that **excludes** 「치매 또는 일상생활장해 등
    타인의 간병을 필요로 하는 상태」 — read literally, it excludes long-term-care risk premium
    from the very ratio that gives a care-only contract its 보험가입금액 [REG-R21].
    """
    n_chg = 12 * min(surr_chg_years, prem_period_years())            # noqa: F821
    if t >= n_chg:
        return 0.0
    return surr_chg_ratio * premium_mth_pp() * (1.0 - t / n_chg)     # noqa: F821


def cv_pp(t):
    """CV(t): the 해약환급금 per policy paid on a lapse in month t.

    ``mijigeup``
        **nil for the whole premium-paying period**, then 50% of the 계약자적립액 — a cliff,
        not a curve, and the strongest of the four forms on the Korean shelf.  The legal basis
        is 감독규정 제7-66조제4항, which lets a 순수보장성보험 priced on a **최적해지율** pay
        less than the ordinary 계약자적립액 − 해약공제액 floor [REG-R19].

    ``half_during``
        50% during the paying period, restored to the full account after it.

    ``pyojun``
        the statutory form, ``max(AV(t) - 해약공제액, 0)`` from year 1 [REG-R19 제7-66조제1항].

    Reading 「50%」 without reading which side of 납입완료 it attaches to puts the cliff upside
    down, which is why the form is a model point field and not a switch on a ratio.
    """
    a = av_pp(t)
    n = prem_period_mths()
    form = cv_form()
    if form == "mijigeup":
        return 0.0 if t < n else 0.5 * a
    if form == "half_during":
        return 0.5 * a if t < n else a
    return max(a - surr_chg_pp(t), 0.0)


# --- cash flows ---

def premiums(t):
    """Premium income at the start of month t: ``P x pols_act(t)``.

    **Not** ``P x pols_if(t)``: the 납입면제 waives the premium of the main contract and of
    every attached rider from the award of 1·2등급, and waived premiums are treated as paid.
    Nil from ``prem_period_mths()`` on, the contract being 비갱신형 with a fixed 납입기간 —
    which is the opposite of the Korean *medical* market's annual renewal, and is the right
    answer for a benefit whose claim arrives thirty years after issue.
    """
    if t < 0 or t >= prem_period_mths() or t >= proj_len() - 1:
        return 0.0
    return premium_mth_pp() * pols_act(t)


def claims(t, kind=None):
    """Benefit outgo at the end of month t, by ``kind``.

    ``"LUMP"``
        ``A_B r(t) n_C(t)``: the 장기요양진단급여금, **최초 1회한** on the first award at or
        above the threshold.  Paying it extinguishes that benefit line and leaves the
        contract, the annuity and the dementia rider running.

    ``"ANNUITY"``
        :func:`ann_pay` — a **living** benefit, paid monthly while the insured survives in
        the care state, guaranteed for the first twelve months and capped at 120.

    ``"DEMENTIA"``
        the 치매진단급여금 rider, once per contract.  Zero unless attached.

    ``"DEATH"``
        ``AV(t) x pols_death_act(t)``: the **계약자적립액** on death from a cause the contract
        does not cover, which 감독규정 제7-63조제1항제1호 requires of every 제3보험 product
        [REG-R17].  Deaths *in* the care state pay nothing — 「지급사유가 발생한 후 사망한
        경우에는 별도로 책임준비금을 지급하지 않습니다」 — so the split of :func:`pols_death`
        is a cash-flow distinction and not bookkeeping.

    ``"LAPSE"``
        ``CV(t) x pols_lapse(t)``: the 해약환급금, identically zero throughout the paying
        period on the composite's 미지급형 form.

    ``"VOID"``
        ``cum_prem_pp(t + 1) x pols_void(t)``: the premiums returned where a certification
        inside the 보장개시일 window makes the cover 무효.  The cover is void **ab initio**
        and 「이미 납입한 보험료를 돌려드립니다」, so every premium the life has paid comes
        back — and a life voided in month t has paid ``t + 1`` of them, month t's included,
        because premium falls at the start of the month and the void is recognised at the
        end of it.  ``cum_prem_pp(t)`` would leave the insurer holding one month's premium on
        a contract it has just declared never to have existed.  Tiny, and published because
        it is a different mechanism from a refused claim.

    ``"MATURITY"``
        identically **zero**, and published rather than dropped: 「이 상품은
        순수보장성보험으로 보험계약 만기시 지급받는 금액(만기환급금)이 없습니다」.

    With no ``kind``, the total of all seven.
    """
    if kind is None:
        return (claims(t, "LUMP") + claims(t, "ANNUITY") + claims(t, "DEMENTIA")
                + claims(t, "DEATH") + claims(t, "LAPSE") + claims(t, "VOID")
                + claims(t, "MATURITY"))
    if kind == "LUMP":
        return lump_amount() * red_factor(t) * pols_entry_care(t)
    if kind == "ANNUITY":
        return ann_pay(t)
    if kind == "DEMENTIA":
        return dementia_amount() * pols_entry_dem(t)
    if kind == "DEATH":
        return av_pp(t) * pols_death_act(t)
    if kind == "LAPSE":
        return cv_pp(t) * pols_lapse(t)
    if kind == "VOID":
        return cum_prem_pp(t + 1) * pols_void(t)
    if kind == "MATURITY":
        return 0.0
    raise ValueError("invalid kind")


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^floor(t/12)`` **[std]**.

    2.0% a year flat, stepping at each 계약해당일 rather than monthly.  No Korean expense
    inflation assumption was retrieved; the level is the Bank of Korea's inflation target and
    is a standardization.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense in month t **[std]**.

    ``expense_acq_mths x P`` at ``t = 0``, then ``expense_maint`` per policy per month
    inflating at :func:`inflation_factor`.  Maintenance is charged on :func:`pols_if`,
    **including lives on waiver**: the policy is still administered when nobody is paying for
    it, and on this product that is a fortieth of the projection.

    No 사업방법서 and no 산출방법서 was retrieved for any Korean long-term-care product, so
    every expense assumption here is [std] — but neither of the two levels is free.  The
    acquisition expense and the initial commission together are **13 times the monthly
    premium**, exactly the 표준해약공제액 of a 보장성보험 in the supervisor's own rule of thumb
    [REG-R29], split 5.2 : 7.8 so that the commission sits at the 60% cap the same release
    sets, and bounded from above by 별표 14 [REG-R20].  ``expense_maint`` is then set so that
    the present value of the whole expense and commission basis at the 예정이율 lands on the
    **20.7%** loading that :func:`net_prem_ratio` implies — the loading the published 환급률
    progression and the published 예정이율 imply between them.  It lands at 20.3% on the anchor
    cell.  So the expense basis is calibrated to the
    same two sourced facts as the account, rather than picked.

    The claim-handling expense is **not** here.  It is :func:`claim_expenses`, deducted on its
    own line and published in its own column, which is what ``expenses`` means everywhere in
    this library.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    acq = expense_acq_mths * premium_mth_pp() if t == 0 else 0.0     # noqa: F821
    return acq + expense_maint * inflation_factor(t) * pols_if(t)    # noqa: F821


def claim_expenses(t):
    """The claim-handling expense of month t **[std]**.

    ``expense_claim`` per claim **event**: the first certification, each **annual** 간병연금
    survival test, and a dementia diagnosis.  Not per monthly instalment — the proof of life
    the 약관 requires is annual — and not inflated.  The unit is higher than a cancer
    chassis's would be because the evidence is a 장기요양인정서 produced by a public body the
    insurer neither funds nor influences, and because the refusal grounds are administrative:
    「허위 또는 부당 판정사실이 확인되는 경우」 nothing is paid.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return expense_claim * (pols_entry_care(t) + ann_tests(t)        # noqa: F821
                            + pols_entry_dem(t))


def comm_init_pp():
    """c0: the initial commission per policy issued, ``comm_init_mths x P`` **[std]**.

    7.8 months' premium, which is **60% of the 13-month 표준해약공제액** — the cap the 2019
    사업비·모집수수료 reform sets on the annual commission of a 보장성보험, and the same 60%
    that now sits in 감독규정 제4-32조제8항 [REG-R29] [REG-R22].  Paid up front at ``t = 0``;
    with the acquisition expense it is what produces the deep new-business strain of the
    worked example's first row.
    """
    return comm_init_mths * premium_mth_pp()                         # noqa: F821


def commissions(t):
    """Commission outgo in month t **[std]**.

    The initial commission at ``t = 0``, then 3.0% of premium income from policy year 2.
    Renewal commission rides on :func:`premiums`, so it stops when the waiver stops the
    premium and when the 납입기간 ends.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    init = comm_init_pp() if t == 0 else 0.0
    renew = comm_renewal_rate * premiums(t) if t >= 12 else 0.0      # noqa: F821
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy month t, **income positive**.

    Premiums less the lump sum, the annuity, the dementia rider, the 계약자적립액 on death,
    the 해약환급금 on lapse, the premiums returned on a voided cover, acquisition and
    maintenance expense, the claim-handling expense and commission.  Income-positive is this
    library's sign and the technical notes' own, so there is no outgo-positive
    ``liability_cf`` companion to publish.

    The shape to expect is a deep month-0 strain, thin positive margins for twenty years while
    the premium runs, and then a long negative tail: the certification rate at 만나이 40 is of
    the order of one in forty thousand a year and at 85 it is one in twenty, so this contract
    prefunds a cost that essentially does not arise until the block is old.  That is what makes
    the **lapse assumption and the interest rate, not the incidence basis, the dominant levers**
    — and it is why 2024's supervisory attention on 무·저해지 lapse was aimed at exactly this
    kind of product.
    """
    return (premiums(t) - claims(t) - expenses(t) - claim_expenses(t)
            - commissions(t))


# --- checks ---

def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``l(t) - l(t+1) - deaths - lapses - voids - maturities``.  Those four are the only ways a
    life leaves this contract.  A lapse applied to the care population, a voided certification
    left inside the block, or a maturity not removed on the last row all show up here.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_void(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    No argument, one bool over all t, the library-wide shape of a ``check_*`` cells;
    :func:`check_pols_roll_fwd_resid` gives the signed residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def check_nesting_resid(t):
    """The smallest slack in the compartment structure at month t; non-negative everywhere.

    The three compartments must be non-negative and must add to :func:`pols_if`, and the
    dementia counter must stay inside the in-force block.  A negative value here would mean
    progression had drained more lives out of the light compartment than were in it, or that
    the rider's first-event ledger had outgrown the block it rides on.
    """
    return min(pols_healthy(t), pols_light(t), pols_care(t),
               pols_if(t) - pols_dem(t),
               -abs(pols_if(t) - pols_act(t) - pols_care(t)))


def check_nesting():
    """True when the compartments stay non-negative and add to the in-force count."""
    return all(check_nesting_resid(t) >= -roll_fwd_tol               # noqa: F821
               for t in range(proj_len()))


def check_ann_ledger_resid(t):
    """The 간병연금 ledger residual in month t; zero everywhere.

    :func:`ann_count` less an independent rebuild that scans **every** month ``s`` in the
    window ``t - n_A < s <= t`` and re-derives each cohort's weight from its own age, rather
    than stepping back through the same loop.  A ledger that paid the first instalment a year
    late, that ran past the cap, that lost the twelve-month guarantee or that used a ratio
    form of :func:`care_surv` would show up here.
    """
    if not annuity_on() or t < 0 or t >= proj_len() - 1:
        return 0.0
    built = 0.0
    for s in range(max(0, t - annuity_max_mths() + 1), t + 1):
        u = t - s
        if u < annuity_guar_mths():
            built += pols_entry_care(s)
        else:
            built += pols_entry_care(s) * care_surv(s, s + 12 * (u // 12))
    return ann_count(t) - built


def check_ann_ledger():
    """True when the 간병연금 ledger closes in every projected month."""
    return all(abs(check_ann_ledger_resid(t)) <= roll_fwd_tol        # noqa: F821
               for t in range(proj_len()))


def check_av_continuity_resid(t):
    """The residual between the two branches of :func:`av_pp` at 납입완료; zero, and zero
    elsewhere by construction.

    The account is an accumulation of net premiums up to 납입완료 and a sourced run-off after
    it, and the two have to agree at the join.  They do because :func:`net_prem_ratio` is
    *derived* from the run-off's first anchor rather than assumed — which is the point: the
    check fails the moment someone replaces the derivation with a round number.
    """
    n = prem_period_mths()
    if t != n:
        return 0.0
    return (net_prem_ratio() * premium_mth_pp() * prem_accum_factor(n)
            - av_ratio_at(0.0) * premium_mth_pp() * n)


def check_av_continuity():
    """True when the 계약자적립액's two branches meet at 납입완료."""
    return all(abs(check_av_continuity_resid(t)) <= val_tol          # noqa: F821
               for t in range(proj_len()))


def check_cv_form_resid(t):
    """The smallest slack in the surrender-value form at month t; non-negative everywhere.

    The 해약환급금 is never negative and never exceeds the 계약자적립액, and on the 미지급형
    form it is **exactly nil** for the whole premium-paying period.  That last clause is the
    cliff, and it is asserted with its sign because reading 「50%」 without reading which side
    of 납입완료 it attaches to puts the cliff upside down — which is the easiest available
    mistake in this product, four forms being on the shelf under three nearly identical names.
    """
    slack = min(av_pp(t) - cv_pp(t), cv_pp(t))
    if cv_form() == "mijigeup" and t < prem_period_mths():
        slack = min(slack, -abs(cv_pp(t)))
    return slack


def check_cv_form():
    """True when the surrender-value form behaves in every projected month."""
    return all(check_cv_form_resid(t) >= -val_tol                    # noqa: F821
               for t in range(proj_len()))


def check_net_cf_resid(t):
    """The residual between :func:`net_cf` and the published components; zero everywhere.

    ``net_cf`` less ``premiums - claims_lump - claims_annuity - claims_dementia -
    claims_death - claims_lapse - claims_void - claims_maturity - expenses - claim_expenses -
    commissions``, which are exactly the columns of :func:`result_cf`.  A cash flow that
    exists in ``net_cf`` but not in the statement, or the reverse, shows up here.
    """
    return net_cf(t) - (premiums(t)
                        - claims(t, "LUMP") - claims(t, "ANNUITY")
                        - claims(t, "DEMENTIA") - claims(t, "DEATH")
                        - claims(t, "LAPSE") - claims(t, "VOID")
                        - claims(t, "MATURITY")
                        - expenses(t) - claim_expenses(t) - commissions(t))


def check_net_cf():
    """True when the cash flow statement re-adds to :func:`net_cf` in every month.

    The house contract: no model's headline number is reconciled only in prose.
    """
    return all(abs(check_net_cf_resid(t)) <= val_tol                 # noqa: F821
               for t in range(proj_len()))


# --- result tables ---

def result_cf():
    """Result table of cash flows, indexed by policy month ``t``.

    ``pols_if`` is the start-of-month count, which is the weight applied to every cash flow on
    the same row; ``pols_act`` is the part of it still paying premium, and ``pols_care`` the
    part on waiver and drawing the annuity.  ``claims_annuity`` is a **living** benefit — the
    간병연금 is paid while the insured survives in the certified state and death stops it — so
    the name describes the benefit's form and not its contingency.  ``claims_death`` is the
    **계약자적립액**, not a death benefit: this contract has none, and what is paid is the
    account balance 감독규정 제7-63조제1항제1호 requires on a non-covered death.
    ``claims_maturity`` is a column of zeros by product design and is published rather than
    dropped, as is ``claims_lapse`` for every duration inside the premium-paying period.
    ``net_cf`` carries the library's income-positive sign.  The frame is ``range(proj_len())``
    and its last row, ``t = proj_len() - 1``, is the 계약해당일 on which the contract matures:
    an in-force count and no cash flow.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_act": [pols_act(t) for t in ts],
            "pols_healthy": [pols_healthy(t) for t in ts],
            "pols_light": [pols_light(t) for t in ts],
            "pols_care": [pols_care(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_lump": [claims(t, "LUMP") for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "claims_dementia": [claims(t, "DEMENTIA") for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_void": [claims(t, "VOID") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts, decrement rates and per-policy values, indexed by ``t``."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_healthy": [pols_healthy(t) for t in ts],
            "pols_light": [pols_light(t) for t in ts],
            "pols_care": [pols_care(t) for t in ts],
            "pols_dem": [pols_dem(t) for t in ts],
            "pols_entry_light": [pols_entry_light(t) for t in ts],
            "pols_entry_care": [pols_entry_care(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "ann_count": [ann_count(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "inc_rate_direct": [inc_rate_direct(t) for t in ts],
            "inc_rate_light": [inc_rate_light(t) for t in ts],
            "prog_rate": [prog_rate(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

care_mort_mult = 3.0

light_mort_mult = 1.8

dem_mort_mult = 2.5

direct_entry_share = 0.20

prog_rate_cap = 1.0

sub65_age = 65

disease_share = 0.95

red_fraction = 0.50

dementia_wait_mths = 15

prem_int_rate = 0.02

surr_chg_ratio = 13.0

surr_chg_years = 7

expense_acq_mths = 5.2

expense_maint = 200.0

expense_claim = 30000.0

inflation_rate = 0.02

comm_init_mths = 7.8

comm_renewal_rate = 0.03

roll_fwd_tol = 1e-12

val_tol = 1e-06

math = ("Module", "math")

pd = ("Module", "pandas")
