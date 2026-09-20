# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Child_KR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 4            # or switch the default

``t`` counts **policy months**, 0-based: ``t = 0`` is the first projected month and month
``t`` runs from ``t`` to ``t + 1`` months after the 계약일. ``proj_len()`` is the **number
of projected months** — the exclusive end of the frame — so the projection runs over
``t = 0 … proj_len() - 1`` and ``result_cf()`` carries ``proj_len()`` rows. The last index
``t = proj_len() - 1`` is the 계약해당일 at 보험나이 ``term_age`` on which the contract
expires: a terminal row that holds the surviving in-force count, the residual 계약자적립액
and nothing else. On the anchor cell ``proj_len()`` is **1,201** — the longest projection
in ``krlib``, and the whole point of the product.

.. rubric:: The age basis, and the two ages a foetal contract carries

The contract's own clock is **보험나이** (*boheom nai*, insurance age): 계약일 현재 실제
만 나이 with a fraction under six months discarded and six months or more rounded up,
incrementing at each 계약해당일 (표준약관 제21조 [REG-R25], reproduced verbatim by every
carrier). That is what :func:`age` returns, and it governs the premium, the anniversary
on which the 갱신형 block renews and the 보험나이 15 threshold at which the 면책기간
switches on.

The decrement tables are read at **만나이** (*man nai*, age last birthday) through
:func:`age_man`, because every public series they are built from is published on 만나이 —
the 완전생명표 [REG-R38] [REG-R39], the 국가암등록통계 age bands [REG-R40] and the
국민건강보험 statistics [REG-R41]. Because of the six-month rule the two differ for
roughly half of all issue dates, and on an ordinary contract the offset is the [std]
half-year average, taken here as zero.

**On a 태아 contract the offset is not an average but a stated quantity.** The 계약나이 is
0 at the 계약일 [S8 제60조], the child's 만나이 is 0 at birth, and 「보험금 지급기준표에서
적용하는 피보험자 나이는 피보험자가 출생한 날부터 계산합니다」 [S8 제58조], so

    보험나이(t) = issue_age + t // 12
    만나이(t)   = (t - birth_month) // 12        for t >= birth_month, undefined before

and the two differ by exactly ``birth_month()`` months for the life of the contract — five
on the anchor cell, capped at six by [S8 제61조]. The contract therefore expires when the
insured is **99 years and 7 months** old, not 100.

.. rubric:: Notes symbol map

The technical notes use compact actuarial symbols; the cells use lifelib names.

====================  ============================  ==================================
Notes symbol          Cells                         Meaning
====================  ============================  ==================================
—                     ``model_point``               the selected model point as a Series
—                     ``proj_len``                  the number of projected policy months
n = proj_len - 1      —                             the terminal 계약해당일 month index
b                     ``birth_month``               the policy month of birth
m                     ``prem_period_mths``          the 납입기간 in months
x                     ``issue_age``                 보험나이 at the 계약일
x + floor(t/12)       ``age``                       attained 보험나이 in month t
y(t)                  ``age_man``                   attained 만나이 in month t
S_j                   ``sum_assured``               보험가입금액 of cover j
P                     ``premium_mth_pp``            monthly office premium, all streams
q(y)                  ``mort_rate``                 annual mortality of the insured
i_j(y)                ``inc_rate``                  annual incidence of cause j
w(t)                  ``lapse_rate``                annual lapse rate
v(t)                  ``void_rate_mth``             pre-birth 무효 rate
omega(t)              ``waiver_rate``               annual 납입면제 rate, both lives
l(t)                  ``pols_if``                   in force at the start of month t
l_P(t)                ``pols_pay``                  of which still paying premium
l_W(t)                ``pols_waived``               of which waived
AV(t)                 ``av_pp``                     계약자적립액 per policy, at time t
CV(t)                 ``cv_pp``                     해약환급금 per policy, at time t
X(t)                  ``surr_chg_pp``               unamortised 해약공제액, at time t
CF(t)                 ``net_cf``                    net cash flow, income positive
====================  ============================  ==================================

Every state variable in this model is a **time-point** value, at time ``t``, and not a
closing balance of period ``t``: ``av_pp``, ``cv_pp``, ``cv_std_pp``, ``surr_chg_pp``,
``refund_ratio``, ``cum_prem_pp`` and ``prem_foetal_paid_pp`` are read at the start of
month ``t``, before that month's premium, with ``t = 0`` at the 계약일 — hence
``cum_prem_pp(0) = 0`` and ``av_pp(0) = 0``, and twelve instalments stand at ``t = 12``.
The counts ``pols_if``, ``pols_pay`` and ``pols_waived`` are likewise at the start of
month ``t``.  The four exit payments of month ``t`` fall at its **end** and are valued on
those start-of-month quantities **[std]**.

.. rubric:: The pre-birth period, and what is in force in it

Months ``t < birth_month()`` are the part of this model that has no analogue anywhere in
this repository. Cover attaches **at birth and not at the 계약일** — 「제53조의 태아는
출생시에 피보험자가 됩니다」 [S8 제54조], and sixteen carriers were ordered in 2016 to
stop advertising otherwise [R2] — so :func:`born` is false, every cover on the child's own
life is identically zero, and there is neither mortality nor morbidity on the insured.

What is in force instead is the **태아보장기간**, whose limbs pay from the date of birth
even where the event preceded it [S8 제59조]; the premium, on all three streams; and a
**void decrement**. 유산 or 사산 makes the contract 무효 and every premium paid is
returned [S8 제56조] [S9], which is not a lapse: nothing is retained, and the cash flow is
a refund of premiums already collected rather than a surrender value. :func:`pols_void`
carries it and :func:`claims` pays it as the ``"VOID"`` kind.

.. rubric:: Two decrement lives

The premium stops on the earlier of two events drawn from two different rows of the
mortality table. The **child's** trigger is 50% 이상 후유장해, one of the 7대질병 or a
중대한특정상해수술 [S2]; the **계약자's** is his own death or a cumulative 장해지급률 of
50% or more [S10 제22조], which is lawful in one clause because that wording makes the
피보험자 of the contract 「계약자와 가입자녀」 [S10 제3조]. The two are treated as
independent **[std]** — nothing in the sources says otherwise and nothing the model can
see relates them — and the child's limb carries the **P코드 carve-out**: it does not
operate over the 1년만기 신생아 block on a 태아 contract, so the covers most likely to pay
in the first year of a foetal contract are precisely the ones that cannot stop the
premium.

.. rubric:: Processing order, and the roll-forward it closes

Within month ``t`` the order is **void, then the waiver, then mortality, then lapse**
**[std order]**. The void decrement applies only before birth and to the whole in-force
block; the waiver moves a policy from :func:`pols_pay` to :func:`pols_waived` without
changing :func:`pols_if`; mortality applies to both compartments; and lapse applies to the
paying compartment alone, a policy paying nothing having nothing to lapse for. The
identity :func:`check_pols_roll_fwd` closes exactly under that order, and
:func:`check_waiver_split` asserts that the two compartments still sum to the block.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/child/``, read at run time rather than stored inside the model. Each table has
a filename Reference and a reader Cells, both on :mod:`~.Child_KR_S.Data`, reached here
through the ``data`` Reference. The consequence worth knowing: **the model is not portable
on its own.** Copying the ``Child_KR_S`` folder without its parent's CSVs produces a model
that reads and then fails on first evaluation.
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


def sex():
    """The sex (M / F) of the insured: a rating factor and a key into every basis table.

    On a **태아** contract the sex is not known at issue and the contract is 「일단 남자
    아이를 기준으로」 priced, trued up after delivery [R3] [S8].  The composite adopts the
    male-rate convention and **does not model the true-up**, because the direction is no
    longer reliable: on the current published tables four carriers price the female above
    the male and seven below, the spread running 62% to 114% of the male rate [S11].
    """
    v = str(model_point()["sex"])
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """x: the **보험나이** of the insured at the 계약일.

    ``0`` on a 태아 contract, where 「계약일에 있어서의 피보험자의 계약나이는 0세로
    합니다」 [S8 제60조].  The current issue-age envelope is 태아 ~ 보험나이 15세
    [S2] [S4] [S5] [S6]; the pre-2023 generation of the same product lines accepted to 30
    [S1] [S7], and the 2023 감독행정 restricted the product **name** above 15 rather than
    the age itself [R1], so a 30-year-old issue is a documented historic variant and is
    shipped as one.
    """
    return int(model_point()["issue_age"])


def foetal():
    """True where the contract is a **태아가입** — written before the insured exists.

    The 태아가입특칙 is what makes it possible: a 태아 has no legal personality and cannot
    be the 피보험자 of an 인보험 contract, so 「제53조의 태아는 출생시에 피보험자가
    됩니다」 [S8 제54조] [R3].  It is not a fringe variant — 20.7% of new child contracts
    in FY2007 were written in utero [R3] — and every current 상품요약서 offers it, with
    가입나이 written as 「태아」 at the head of the issue-age grid [S2] [S3] [S4] [S5] [S6].
    """
    return bool(int(model_point()["foetal"]))


def birth_month():
    """b: the policy month in which the insured is born; 0 on an ordinary contract.

    **5 on the anchor cell [std].**  Three sources bound it: [S8 제61조] caps the pre-birth
    period at six months by moving the 계약일 back where the birth falls later than that;
    the neonatal riders close at 임신 22주 [S5], so a contract written inside that window
    still has **at least** 4.1 months of gestation to run; and the 태아 sub-term is written
    「1~10월만기」 at one carrier [S1].  Five is between those two bounds and is a whole
    number of grid steps.
    """
    return int(model_point()["birth_month"]) if foetal() else 0


def issue_age_man():
    """The 만나이 of the insured at the 계약일: 0 on a 태아 contract.

    On an ordinary contract the 만나이 is taken equal to the 보험나이, a **[std]**
    simplification: the six-month rounding rule puts the true 만나이 at ``issue_age()`` or
    ``issue_age() - 1`` with roughly equal probability, and no source supplies the
    distribution of issue dates within a policy year that a conversion would need.  On a
    **태아** contract no simplification is needed — the offset is exactly
    :func:`birth_month` months.
    """
    return 0 if foetal() else issue_age()


def term_age():
    """The 보험나이 at which the 보험기간 ends: **100** on the composite.

    Observed maxima: 100세 at four carriers [S1] [S2] [S5] [S6] and **110세** at one [S4],
    the longest term found anywhere in this research.  100 is the modal maximum, the term
    on which every published premium and cash-value grid in the file is quoted
    [S11] [S2] [S1], and the term whose arrival in 2011 made the product what it is [R5];
    110세 adds no mechanic and is shipped as a model point.
    """
    return int(model_point()["term_age"])


def prem_period_years():
    """The 납입기간 of the core covers in years: **20** on the composite.

    Observed 10 / 15 / 20 / 25 / 30년납 on the 100세만기 forms [S2] [S4].  20 years is the
    payment term the comparison board quotes every premium on [R12]; it is the
    해약공제계수 cap of 감독규정 [별표 14], 「보험기간(최대 20년)」 [REG-R20]; and it
    leaves **eighty years of paid-up cover** on the anchor cell — four times the payment
    period, and the reason a child policy's measurement is dominated by what happens long
    after the premium stops.
    """
    return int(model_point()["prem_period_years"])


def prem_period_mths():
    """m: the 납입기간 of the core covers in policy months, ``12 x prem_period_years()``."""
    return 12 * prem_period_years()


def prem_end():
    """The last policy month in which a core premium falls due, ``prem_period_mths() - 1``.

    The premium is payable **monthly in advance**, so a 20년납 contract pays in months 0 to
    239 and 납입완료 falls at ``t = 240`` — which is where the 무해지 surrender-value step
    sits and why it is a cliff rather than a curve [S2].
    """
    return prem_period_mths() - 1


def premium_mth():
    """P_core: the monthly office premium of the core covers, a **model point input**.

    **₩28,000 on the anchor cell [std]**, being ₩27,000 of core 보장보험료 and ₩1,000 for
    the 계약자 waiver module; **₩27,000 on the calibration cell**.  No Korean carrier
    publishes a rate table by age and duration — the 산출방법서 that holds each carrier's own
    적용위험률 and 예정사업비율 is an undisclosed 기초서류 [REG-R2], and the bureau's
    참조순보험요율 is filed with the FSC under 보험업법 제176조제4항 with no general
    publication obligation [REG-R4], the 장기손해보험 display published under 제176조제9항
    carrying risk rates rather than office premiums [REG-R61] — so the office premium enters
    as an input rather than being computed.  What *is* published
    is a specimen premium per product on a standardised basis (보험나이 5세, 상해 1급,
    100세만기 20년납, 월납, the 보장보험료 of the compulsory covers only [R12]), and the
    observed levels vary by a factor of seven, ₩21,502 to ₩148,250 for a male 5-year-old,
    because carriers include different compulsory sets in the quoted figure [S11].
    ₩27,000 is the tight cluster of the three mid-market carriers whose compulsory sets are
    closest to [R12]'s — ₩26,841, ₩26,999 and ₩27,480 [S11].  **Nothing in this model
    depends on it being a market rate**; :func:`equiv_premium_mth_pp` computes the premium
    the shipped basis actually implies, and where the two differ the computed figure
    governs.
    """
    return float(model_point()["premium_mth"])


def premium_foetal_mth():
    """P_foetal: the monthly premium of the 태아 module, 전기납 over its own short term.

    **₩3,000 on the anchor cell [std]**, giving ₩31,000 a month to ``t = 16`` and ₩28,000
    from ``t = 17``.  The second stream is not an artefact of the composite: a 태아 contract
    really does carry a second, short term with its own premium — 「계약체결일부터
    출생시점 … 까지의 기간을 보험기간으로 하여 아래의 보험기간 및 보험료 납입기간을
    추가로 부가합니다」 [S2], written elsewhere as a fixed 「1~10월만기 전기납 태아
    월납」 sub-term [S1].
    """
    return float(model_point()["premium_foetal_mth"]) if foetal() else 0.0


def foetal_cover_end():
    """The policy month at which the 태아 module's cover ends: ``birth_month() + 12``.

    The module merges two terms the sources state separately — the **태아보장기간**,
    「계약체결일부터 출생시점(출산 또는 분만 과정에서 보험금 지급사유가 발생하는 경우
    포함)까지」 [S2], and the **1년만기 전기납** 신생아 block that follows it, matching
    「출생 전후에 발생하는 질환에 대한 보장을 강화하려는 목적으로 출생 후 1년까지만 보장」
    [R5] [S2] [S5].  On the anchor cell that is ``t = 17``.
    """
    return birth_month() + 12 if foetal() else 0


def foetal_prem_end():
    """The last month in which a 태아 module premium falls due, one month before its term.

    The module's premium is 전기납 and payable monthly in advance, so a term ending at
    ``t = 17`` collects in months 0 to 16 — which is exactly what the published anchor
    premium says: ₩31,000 to ``t = 16``, ₩28,000 from ``t = 17`` [S2] [S1].
    """
    return foetal_cover_end() - 1 if foetal() else -1


def cv_form():
    """The surrender-value form: ``std``, ``susp`` or ``graded``.

    ``std``
        **표준형** — 해약환급금 = 순보험료식 계약자적립액 less the 해약공제액, floored at
        zero [S2] [S1] [REG-R19 제7-66조제1항제1호].  The base run, deliberately: every
        carrier on the board offers a suppressed form beside it [S11] and the market has
        moved there, but the 적립부분 credited at the 공시이율 exists **only** on the
        표준형 — the suppressed forms are 순수보장성 and show 「-」 for it [S11] [S2] — and
        the 표준형's value exceeds premiums paid from about year 30, a shape no other
        ``krlib`` protection product produces and only a hundred-year term can.

    ``susp``
        **해약환급금 미지급형** — nil during the 납입기간 and ``cv_floor_ratio()`` of the
        표준형 value afterwards [S2] [S11] [REG-R19 제7-66조제4항].

    ``graded``
        **해약환급금 미지급형Ⅲ** — the published ten-step ladder, 5% of the 표준형 value in
        the two years after 납입완료 rising in 5-point steps every two years to 50%
        eighteen years after it [S1].
    """
    v = str(model_point()["cv_form"])
    if v not in ("std", "susp", "graded"):
        raise ValueError("invalid cv_form")
    return v


def cv_floor_ratio():
    """k: the suppressed form's fraction of the notional 표준형 value after 납입완료.

    **0.50**, the regulatory floor of 감독규정 제7-66조제4항제2호 [REG-R19] [REG-R28] and
    the level every carrier writes to [S2] [S11].  **The 50% is 50% of a product nobody can
    buy**: the comparator is synthetic and both carriers say so — 「'해약환급금미지급형
    비교상품'은 … 해지율을 적용하지 않은 상품이며, 비교안내를 위한 종목으로 실제로 판매하지
    않음」 [S3] [S1].  So the suppressed form's post-completion value is half of a
    hypothetical cash value computed *without* the lapse assumption used to price the form
    itself, which is the whole reason that assumption became a supervisory matter
    [R11] [REG-R27].
    """
    return float(model_point()["cv_floor_ratio"])


def waiver_child():
    """True where the **child's** 보험료 납입면제 is attached.  On in the base run.

    Triggers: 50% 이상 후유장해 (상해 or 질병), diagnosis of one of the **7대질병** —
    암(유사암 제외), 뇌혈관질환, 중대한재생불량성빈혈, 양성뇌종양 and three 심혈관질환
    limbs — or a **중대한특정상해수술**, 「상해로 뇌손상, 내장손상을 입고 사고일로부터 180일
    이내에 받은 개두·개흉·개복수술」 [S2].
    """
    return bool(int(model_point()["waiver_child"]))


def waiver_payer():
    """True where the **계약자's** 보험료 납입면제 module is attached.  On in the base run.

    「보험료 납입기간 중 … 계약자가 사망 또는 … 장해지급률이 50% 이상인 장해상태가 되었을
    때에는 차회 이후의 보험료 납입을 면제하여 드립니다」 [S10 제22조제1항].  This is the
    mechanic with no counterpart in ``uslib``, ``uklib``, ``jplib``, ``frlib`` or
    ``delib``: a **decrement on a life who is not the insured**.  On the 손해보험 chassis
    the same economics arrive as a compulsory 부양자 death rider on the parent's own life
    [S5] [S11], which is a benefit and not a decrement, and modelling one as the other
    would be wrong in both level and shape.
    """
    return bool(int(model_point()["waiver_payer"]))


def payer_age():
    """The **만나이** of the 계약자 at the 계약일: 33 on the composite **[std]**.

    33 is the mid-point of the 20~47세 band the mother-side riders themselves state [S2],
    and the only sourced anchor for a parental age in the whole file; Korean statistics on
    mean age at first birth were not retrieved and are not relied on.  The waiver's whole
    value is concentrated in the twenty years in which a 33-to-53-year-old parent might die
    or become severely disabled, and Korean mortality at those ages is low, which is why
    the module is cheap enough to be compulsory.
    """
    return int(model_point()["payer_age"])


def payer_sex():
    """The sex of the 계약자, a key into the same mortality table as the insured.

    Male on the composite, so the waiver decrement runs on the male table, which is the
    conservative direction **[std]**; a female 계약자 is a model-point variant.  The
    계약자 **may be changed** during the contract, which would change the decrement life
    mid-projection; no retrieved wording states how the waiver responds, so the composite
    holds the 계약자 fixed and marks the point [unverified].
    """
    v = str(model_point()["payer_sex"])
    if v not in ("M", "F"):
        raise ValueError("invalid payer_sex")
    return v


def sum_assured(cover):
    """S_j: the 보험가입금액 of cover ``j``, read from the model point.

    The rider set is the 손해보험협회 comparison basis [R12] — the only standardised
    specification of a Korean child policy the market itself publishes, and the basis every
    published premium is quoted on — plus a 유사암 tier and a 태아 module that basis does
    not carry.  At the anchor cell: ``disability`` ₩100,000,000 (the 기본계약, paid as
    보험가입금액 × 장해지급률), ``disease_disab`` ₩10,000,000, ``cancer`` ₩10,000,000,
    ``minor_cancer`` ₩2,000,000 (20% of the general tier, the chassis ratio),
    ``cerebral`` and ``cardiac`` ₩10,000,000 each on the **narrow** 뇌출혈 and
    급성심근경색증 definitions, ``surgery`` ₩5,000,000 per named-disease operation,
    ``fracture`` ₩400,000, ``burn`` ₩200,000, ``liability`` ₩100,000,000 per occurrence and
    ``neonatal`` ₩10,000,000 as the 태아 module's own 가입금액.
    """
    return float(model_point()["sa_" + cover])


def hosp_daily():
    """The 입원일당 per day: **₩40,000**, on a 1~180일 per-stay basis [R12] [S2].

    The observed menu is wide — 1~180일, 1~120일, 1~30일, 1~10일 and 4일이상 bases, with
    종합병원 / 상급종합병원 / 중환자실 / 1인실 variants and 암직접치료 and 요양병원
    sub-limits [S1] [S2] — and the composite takes the comparison basis's single form.
    This is the cover a child policy actually pays on, an order of magnitude below the
    diagnosis benefits in amount and several orders above them in frequency.
    """
    return float(model_point()["hosp_daily"])


def broad_def():
    """True where the two adult-disease limbs are written on the **broad** KCD ranges.

    Two definitions are in the market for each: the narrow 뇌출혈 and 급성심근경색증 the
    comparison basis prices [R12], and the broad **뇌혈관질환** and **허혈성심장질환** most
    current products sell [S11] [S2].  The composite takes the narrow pair, against the
    grain of current practice, because every published premium in the file is quoted on
    [R12]'s specification — pricing the broad definitions against a premium collected for
    the narrow ones would make the anchor cell internally inconsistent.  The switch
    multiplies both incidences by ``broad_def_factor`` **[std]**.
    """
    return bool(int(model_point()["broad_def"]))


def waiting_mths():
    """The 면책기간 in months before the 암보장개시일: **0** on the anchor cell.

    ::

        암보장개시일 =
            the day the first premium is received     if 보험나이 < 15 at the 계약일
            the 91st day counting 계약일 as day 1      if 보험나이 >= 15 at the 계약일
            the day the first premium is received     if the cover is a 태아가입용 form

    Two independent primary statements, from two carriers and two document types: 「최초
    계약과 부활계약의 면책기간은 **보험나이 15세 이상인 경우에만 적용**」 [S3], and
    「보장개시일(계약일로부터 90일이 지난날의 다음날, **계약일 현재 보험나이 15세 미만
    피보험자의 경우 1회 보험료를 받은 때**)」 [S11].  The origin is 2006: there being no
    evidence of anti-selection or of a 위험률차손 at child ages, the 90-day 부담보 was
    deleted for 어린이보험 [R5]; a 태아가입용 cover has 「면책기간 없음」 at all [S3].

    The rule is tested **at the 계약일 and not at the claim date**, so a contract issued at
    계약나이 0 has **no cancer waiting period at any point in its hundred-year life**,
    including the eighty-five years during which the insured is an adult.  A model that
    re-tests the rule at each anniversary is wrong.
    """
    return int(model_point()["waiting_mths"])


def reduction_mths():
    """The 감액기간 in months, during which a diagnosis benefit pays half: **0**.

    The market has moved to 감액없음 and prints the word in the benefit names — 암진단비
    (유사암제외)**(감액없음)** — at five carriers [S1] [S3] [S11]; where a 감액 survives it
    is a first-year 50% [S6] [S11], which is the shipped switch.  And a **태아 contract may
    not be subject to 감액 at all**: a 변경권고 of 2015-06-17 inserted 「단, 피보험자가
    보험가입 당시 태아(胎兒)인 경우에는 보험금의 100%를 지급합니다」 across 17 carriers and
    56 products, on the reasoning that 「태아는 보험가입시 역선택 가능성이 거의 없는데도」
    [R2].  The disapplication is applied here rather than left to the model point.
    """
    return 0 if foetal() else int(model_point()["reduction_mths"])


def prem_discount_rate():
    """The 2026 저출산 premium discount, as a fraction of the office premium.  0 in base.

    From **2026-04-01** every Korean insurer operates a **1%–5% discount for one year** on
    a 보장성 어린이보험 where the policyholder or spouse is within a year of a birth, on
    육아휴직, or on 육아기 근로시간 단축 for a child of 12 or under [R6].  On the birth limb
    the discount applies to a **sibling's** policy and not the newborn's own.  It is limited
    to one use per contract, pre-existing contracts qualify, and the expected industry cost
    is about ₩1,200억원 a year [R6].  Whether it applies to the 영업보험료 or the
    보장보험료 is not stated and is [unverified]; the model applies it to the whole office
    premium.
    """
    return float(model_point()["prem_discount_rate"])


def prem_discount_mths():
    """The number of months over which the 2026 저출산 discount runs: 12 where on [R6]."""
    return int(model_point()["prem_discount_mths"])


def lapse_basis():
    """Which of the three shipped lapse vectors this model point uses.

    ``loglinear`` is the 2024 계리가정 guideline's 원칙모형 [REG-R27] [R11] and the base;
    ``disclosed`` is the 적용해지율 one carrier actually publishes [S1]; ``flat`` is a
    level comparison vector.  Shipping the first two side by side is exactly the comparison
    the guideline requires an insurer departing from the 원칙모형 to disclose.
    """
    v = str(model_point()["lapse_basis"])
    if v not in set(data.lapse_table().index):                       # noqa: F821
        raise ValueError("invalid lapse_basis")
    return v


def mort_be_factor():
    """The multiplicative adjustment from the shipped table to a best estimate.

    1.0 in the base run: the table is already a [std] construction on population data
    rather than a valuation table with a margin in it, so there is nothing to unwind.  It
    is carried so that a user replacing ``mort_table.csv`` with a company valuation table
    has the hook the sister libraries use, and one model point runs at 1.10.
    """
    return float(model_point()["mort_be_factor"])


def pols_if_init():
    """The number of policies in force at ``t = 0``: one.

    Every model point is a single policy, so the whole projection reads as an amount per
    policy issued.  On a **태아** contract "in force" at ``t = 0`` means the contract is on
    risk for the 태아보장기간 limbs and for the premium — not that the insured exists.
    """
    return 1.0


# --- the timeline ---

def proj_len():
    """The **number** of projected policy months, ``12 x (term_age() - issue_age()) + 1``.

    The **exclusive end** of the frame: the projection runs over ``t = 0`` to
    ``proj_len() - 1`` and ``result_cf()`` carries ``proj_len()`` rows.  **1,201 on the
    anchor cell**, the longest projection in ``krlib``: a 태아 contract at 계약나이 0
    running to the 100세 계약해당일.  The ``+ 1`` is that 계약해당일 itself: the 1,200
    months of the 보험기간 are ``t = 0 … 1,199``, and the last index ``n = proj_len() - 1
    = 1,200`` is the terminal row on which the contract expires — the surviving in-force
    count and the residual 계약자적립액, and no cash flow of its own.

    On a 태아 contract the terminal date is
    fixed by the **계약일** and not by the birth, so the insured's 만나이 at expiry is 100
    less the pre-birth period — 99 years and 7 months on the anchor cell.  That asymmetry
    runs the whole length of the projection and is a direct consequence of [S8 제60조]
    setting the 계약나이 to 0 before the child exists.
    """
    return 12 * (term_age() - issue_age()) + 1


def age(t):
    """The attained **보험나이** in policy month t, ``issue_age() + t // 12``.

    The contractual clock: it governs the premium, the anniversary on which the 갱신형
    block renews and the 보험나이 15 threshold of the 면책기간 [S3] [S11] [S7 제27조].  It
    increments at each 계약해당일 whether or not the insured has been born.
    """
    return issue_age() + t // 12


def age_man(t):
    """y(t): the attained **만나이** in policy month t; ``-1`` before birth.

    「보험금 지급기준표에서 적용하는 피보험자 나이는 **피보험자가 출생한 날부터**
    계산합니다」 [S8 제58조], so on a 태아 contract this runs from :func:`birth_month` and
    lags :func:`age` by exactly that many months for the life of the contract.  Every
    decrement table in this model is read at this age.
    """
    if t < birth_month():
        return -1
    return issue_age_man() + (t - birth_month()) // 12


def born(t):
    """True once the insured exists, ``t >= birth_month()``.

    The single most important gate in the model.  Cover attaches **at birth and not at the
    계약일** [S8 제54조] [R3], and in 2016 sixteen carriers and nineteen products were
    ordered to stop advertising 「태아 때부터 보장」 and 「엄마 뱃속에서부터 보장」 under
    보험업감독규정 제4-35조제3항 [R2].  Every benefit on the child's own life, and the
    child's own mortality, is zero while this is false; the only things in force before it
    are the premium, the void decrement and the 태아보장기간 limbs of the 태아 module,
    which pay **from the date of birth** even where the event preceded it [S8 제59조].
    """
    return t >= birth_month()


def policy_year(t):
    """The policy year containing policy month t, 1-based: ``t // 12 + 1``."""
    return t // 12 + 1


def duration_years(t):
    """The elapsed duration in years at policy month t, ``t / 12``, as a real number.

    The key into the ``build`` half of the 환급률 progression, which the 상품요약서
    publishes at 1, 3, 5, 10, 15, 20, 30, 40, 50 and 60 years [S2].
    """
    return t / 12.0


def runoff(t):
    """The fraction of the 보험기간 run off at policy month t, ``t / (proj_len() - 1)``.

    The denominator is the terminal 계약해당일 index ``n = proj_len() - 1``, so this is 0 at
    the 계약일 and exactly 1 on the last row of the frame.

    The key into the ``taper`` half of the 환급률 progression.  Indexing the terminal
    collapse on the fraction of the term rather than on a duration is what lets one shipped
    grid serve a 30세만기, a 100세만기 and a 110세만기 contract without re-basing the
    published figures.
    """
    return t / (proj_len() - 1)


# --- the basis: scalar parameters ---

def basis_param(name):
    """One scalar [std] parameter of the benefit basis, from *basis_table.csv*."""
    return float(data.basis_table().loc[name, "value"])              # noqa: F821


# --- mortality, on two lives ---

def mort_series(s):
    """The annual mortality rates of sex ``s`` as a Series indexed by 만나이.

    Held as a cells so the frame is sliced once per sex rather than once per lookup.
    """
    return data.mort_table().loc[s]["mort_rate"]                     # noqa: F821


def mort_rate_at_age(x, s):
    """q(x): the annual mortality of a life aged 만나이 ``x`` of sex ``s``.

    A **[std] construction** shaped on the Korean 완전생명표 age pattern
    [REG-R38] [REG-R39]; the 제10회 경험생명표 is published only as 평균수명 and 기대여명
    summary statistics [REG-R33] [REG-R34].  The shape a child policy is exposed to is the
    infant peak, the trough at about age 10 and the adolescent turn — none of which a table
    graduated from age 20 upwards would carry.
    """
    return float(mort_series(s).loc[min(max(x, 0), 120)])


def mort_rate(t):
    """q(t): the annual mortality of the **insured** in policy month t.

    Zero before birth: a 태아 has no mortality in this contract, because 「태아는 법적으로
    인격을 갖지 못하여 인보험의 보호대상이 될 수 없으므로 … 태아보험에서는 태아의 사망을
    직접적으로 보장하지는 아니함」 [R3].  What the pre-birth period carries instead is
    :func:`void_rate_mth`, which is a validity adjustment and not a decrement of the same
    kind.
    """
    if not born(t):
        return 0.0
    return mort_rate_at_age(age_man(t), sex()) * mort_be_factor()


def mort_rate_mth(t):
    """The monthly mortality of the insured, ``1 - (1 - q)^(1/12)``."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def mort_rate_payer(t):
    """The annual mortality of the **계약자** in policy month t.

    Read from the same table at the 계약자's own attained 만나이 and sex.  This is the
    second decrement life, and it is the reason this model differs structurally from every
    other in the six libraries: the premium stream stops on the earlier of two events drawn
    from two different rows of one table [S10 제22조].
    """
    return mort_rate_at_age(payer_age() + t // 12, payer_sex())


# --- lapse ---

def lapse_param(name):
    """One parameter of the selected lapse basis, from *lapse_table.csv*."""
    return float(data.lapse_table().loc[lapse_basis(), name])        # noqa: F821


def lapse_rate(t):
    """w(t): the **annual** lapse rate in policy month t.

    On the ``loglinear`` basis, the 2024-11-07 계리가정 guideline's 원칙모형: a log-linear
    decay from the first-year rate to **0.1% at 납입완료**, and **0.8%** thereafter
    [REG-R27] [R11].  The guideline's own functional form was never converted from HWP and
    is [unverified] at instrument level; the two endpoints are verified from the 보도자료.

    On the ``disclosed`` basis, the step function one carrier actually publishes for its
    suppressed forms — 5.0% for the first ten years, 3.0% from ten to fifteen, 1.0%
    thereafter during the payment period and 0.5% after 납입완료 [S1] — which is the
    comparison the guideline obliges an insurer departing from the 원칙모형 to disclose.

    On the ``flat`` basis, a level rate: the synthetic 표준형 the 환급률 comparison is made
    against is priced with **no** lapse assumption at all [S1] [S3], and a level rate is the
    nearest thing a projection can carry to that.

    Lapse is treated as **absorbing**.  부활 is available within three years even where
    there is no surrender value, and may not be refused merely because a claim event
    occurred before termination [REG-R25 제27조] [S8]; below 보험나이 15 there is no cancer
    waiting period to re-run [S3], so a reinstated child policy is very nearly the policy
    that lapsed.  The simplification is conservative on a protection product and is
    recorded as one **[std]**.
    """
    first = lapse_param("first_year_rate")
    completion = lapse_param("completion_rate")
    ultimate = lapse_param("ultimate_rate")
    if t >= prem_period_mths():
        return ultimate
    if lapse_basis() == "disclosed":
        if t < 120:
            return first
        if t < 180:
            return 0.03
        return completion
    if lapse_basis() == "flat":
        return first
    frac = t / prem_period_mths()
    import math
    return math.exp(math.log(first) + frac * (math.log(completion) - math.log(first)))


def lapse_rate_mth(t):
    """The monthly lapse rate, ``1 - (1 - w)^(1/12)``."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def void_rate_mth(t):
    """v(t): the monthly rate at which a 태아 contract is voided before birth.

    「태아가 유산 또는 사산에 의해 출생하지 못한 경우에는 **계약을 무효로 합니다** … 이미
    납입한 보험료를 돌려드립니다」 [S8 제56조] [S9].  This is **not a lapse**: nothing is
    retained, the contract is de-recognised rather than terminated, and the cash flow is a
    refund of premiums already collected — a validity adjustment, which is why it has its
    own decrement and its own ``"VOID"`` claim kind rather than sitting in the lapse column.

    **No Korean source retrieved gives a foetal-loss rate**; what the sources fix is the
    mechanic.  The level is a **[std]** annualised rate over the pre-birth months alone and
    is zero everywhere else.
    """
    if not foetal() or t >= birth_month():
        return 0.0
    return 1.0 - (1.0 - basis_param("void_rate_ann")) ** (1.0 / 12.0)


# --- morbidity incidence ---

def inc_pivots(cause):
    """The (age, rate) pivots of ``cause`` for this model point's sex, sorted by age.

    Held as a cells so *incidence_table.csv* is sliced once per cause rather than once per
    age.
    """
    s = data.incidence_table().loc[(cause, sex())]["rate"]           # noqa: F821
    return [(int(a), float(r)) for a, r in s.items()]


def inc_rate_at(x, cause):
    """i_j(x): the annual incidence of cause ``j`` at 만나이 ``x``, log-linearly graduated.

    Interpolated in the logarithm between the fourteen pivot ages of
    *incidence_table.csv*, held flat outside them and returned **exactly** at a pivot, so
    that the one published rate in the file reproduces to every digit it is printed with.
    A logarithmic interpolation is the
    right one here because every one of these rates spans two or more orders of magnitude
    across the age range — cancer incidence rises about two hundredfold from age 10 to age
    80 — and a linear interpolation between decade pivots would be wrong by a factor of
    two in the middle of every span.

    **Every rate is a [std] construction** save the ``disability`` pivot at age 5, which is
    the one 적용위험률 published anywhere in this file [S1].  The provenance column of each
    row names the authority its shape rests on.
    """
    pv = inc_pivots(cause)
    if x <= pv[0][0]:
        return pv[0][1]
    if x >= pv[-1][0]:
        return pv[-1][1]
    for a, r in pv:
        if a == x:
            return r
    import math
    for i in range(len(pv) - 1):
        x0, y0 = pv[i]
        x1, y1 = pv[i + 1]
        if x0 <= x <= x1:
            w = (x - x0) / (x1 - x0)
            return math.exp(math.log(y0) + w * (math.log(y1) - math.log(y0)))
    raise ValueError("age out of range")


def inc_rate(t, cause):
    """The annual incidence of cause ``j`` in policy month t; zero before birth.

    The two adult-disease limbs carry the broad-definition switch: where :func:`broad_def`
    is set, ``cerebral`` and ``cardiac`` are multiplied by ``broad_def_factor`` **[std]**,
    which is the difference between the narrow 뇌출혈 / 급성심근경색증 the comparison basis
    prices [R12] and the broad 뇌혈관질환 / 허혈성심장질환 most current products sell
    [S11] [S2].
    """
    if not born(t):
        return 0.0
    rate = inc_rate_at(min(age_man(t), 100), cause)
    if broad_def() and cause in ("cerebral", "cardiac"):
        rate = rate * basis_param("broad_def_factor")
    return rate


def inc_rate_mth(t, cause):
    """The monthly incidence of cause ``j``, ``1 - (1 - i)^(1/12)``.

    The ``hosp_acc`` and ``hosp_dis`` causes are expected **days** rather than
    probabilities, so they are divided by twelve instead; :func:`benefit_pp` handles them
    separately and does not call this.
    """
    return 1.0 - (1.0 - inc_rate(t, cause)) ** (1.0 / 12.0)


def frac_open(t, cause):
    """The probability that a policy in force at t has **not** yet claimed cause ``j``.

    The diagnosis benefits are **최초 1회한** each [S1] [S2] [S11], so the exposed
    population is not the in-force block but the part of it whose benefit line is still
    open.  ``frac_open(0) = 1`` and ``frac_open(t+1) = frac_open(t) (1 - i_m(t))``, the
    incidence being taken as independent of the exit decrements **[std]**.

    The quantity is worth watching on this product rather than on the chassis.  Paediatric
    cancer incidence is two orders of magnitude below the adult rate, so the ledger is
    almost untouched for thirty years and then drains fast: the general tier runs from
    1.0000 to **0.4023261296** over the term, so nearly 60% of that line has been used by
    the 100세 계약해당일, which is what a level premium on a 100세만기 child policy has to
    fund.
    """
    if t <= 0:
        return 1.0
    return frac_open(t - 1, cause) * (1.0 - inc_rate_mth(t - 1, cause))


# --- the two premium waivers ---

def waiver_rate_child(t):
    """The annual rate at which the **child's** 납입면제 fires in policy month t.

    ``cancer + cerebral + cardiac`` plus ``waiver_disab_share`` of the two 후유장해
    incidences, standing for the 7대질병 diagnosis limb, the 50% 이상 후유장해 limb and the
    중대한특정상해수술 limb of [S2] respectively **[std]**.

    **The P코드 carve-out is the sharpest interaction in the product** and is implemented
    rather than averaged away: 「출생전후기에 기원한 특정 병태(P코드) 진단시 납입면제를
    적용하지 않음」 [S2].  The 태아 module's whole reason for existing is the perinatal
    chapter of the KCD, so on a 태아 contract this limb does not operate at all over the
    1년만기 신생아 block — the covers most likely to pay in the first year are precisely the
    ones that cannot stop the premium.  That is coherent, a neonatal condition not being a
    lifelong impairment, and it is a **[std]** implementation of a sourced carve-out.
    """
    if not waiver_child() or not born(t) or t > prem_end():
        return 0.0
    if foetal() and t < foetal_cover_end():
        return 0.0
    share = basis_param("waiver_disab_share")
    return (inc_rate(t, "cancer") + inc_rate(t, "cerebral")
            + inc_rate(t, "cardiac")
            + share * (inc_rate(t, "disability") + inc_rate(t, "disease_disab")))


def waiver_rate_payer(t):
    """The annual rate at which the **계약자's** 납입면제 fires in policy month t.

    The 계약자's own death or a cumulative 장해지급률 of 50% or more from one cause
    [S10 제22조제1항], taken as mortality grossed up by ``payer_disab_ratio`` **[std]**, no
    Korean disability incidence table being public.  It runs from ``t = 0``, before the
    insured exists: the policyholder is an insured of the contract in his own right
    [S10 제3조], so his death is a contractual event from the 계약일 whether or not the
    child has been born.
    """
    if not waiver_payer() or t > prem_end():
        return 0.0
    return mort_rate_payer(t) * (1.0 + basis_param("payer_disab_ratio"))


def waiver_rate(t):
    """omega(t): the annual rate at which the premium stops, on either life.

    ``1 - (1 - child)(1 - payer)``.  The two decrements are **not independent** of each
    other in any way the model can see, and the composite treats them as independent — a
    **[std]** simplification.  Because the waiver on the main contract carries every rider
    with it — 「이 특약의 보험료 납입기간 중 주계약의 보험료 납입이 면제되었을 때에는 이
    특약의 차회 이후의 보험료 납입을 면제하여 드립니다」 [S8] — a single event stops the
    whole premium stream, the 태아 module included, and not merely the core.
    """
    return 1.0 - (1.0 - waiver_rate_child(t)) * (1.0 - waiver_rate_payer(t))


def waiver_rate_mth(t):
    """The monthly waiver rate, ``1 - (1 - omega)^(1/12)``."""
    return 1.0 - (1.0 - waiver_rate(t)) ** (1.0 / 12.0)


# --- the in-force block, in two compartments ---

def pols_pay(t):
    """l_P(t): in force and **still paying premium** at the start of policy month t.

    ``l_P(0) = pols_if_init()``, then

        l_P(t+1) = ( l_P(t) (1 - v(t)) - e(t) ) (1 - q(t)) (1 - w(t))

    where ``e(t)`` is :func:`pols_waiver_entry`.  Premium-paying and lapse-exposed.  The
    processing order is void, waiver, mortality, lapse **[std order]**.
    """
    if t <= 0:
        return pols_if_init() if t == 0 else 0.0
    if t >= proj_len():
        return 0.0
    s = t - 1
    base = pols_pay(s) * (1.0 - void_rate_mth(s)) - pols_waiver_entry(s)
    return base * (1.0 - mort_rate_mth(s)) * (1.0 - lapse_rate_mth(s))


def pols_waived(t):
    """l_W(t): in force with the premium **waived** at the start of policy month t.

    ``l_W(0) = 0``, then ``l_W(t+1) = ( l_W(t) (1 - v(t)) + e(t) ) (1 - q(t))``.

    Cover continues in full; payment of the 적립보험료 stops as well [S2].  These policies
    are **not exposed to lapse** — a policy paying nothing has nothing to lapse for, and a
    voluntary surrender out of a waived state is not something any retrieved wording
    describes — which is a **[std]** treatment and the one the sister libraries use for a
    waived or claiming cohort.  A waiver granted in one renewal cycle does not carry into
    the renewed contract on the 표준형 [S2]; the composite's renewals are inside a
    비갱신 core, so nothing here reverses.
    """
    if t <= 0 or t >= proj_len():
        return 0.0
    s = t - 1
    base = pols_waived(s) * (1.0 - void_rate_mth(s)) + pols_waiver_entry(s)
    return base * (1.0 - mort_rate_mth(s))


def pols_waiver_entry(t):
    """e(t): policies whose premium waiver fires in policy month t.

    Drawn from the paying compartment after the month's void decrement.  The waiver is a
    **correlated decrement**: it fires on the same events that pay the diagnosis and
    disability benefits and then runs for as long as the insured survives inside the
    납입기간, so its value is an incidence rate multiplied by a post-onset survival curve.
    On a child policy it is worth very little in the early years — paediatric cancer and
    cerebrovascular incidence are two orders of magnitude below the adult rates the chassis
    is calibrated on — and a great deal from about ``t = 180``, when the insured reaches an
    age at which the 7대질병 begin to occur and which is still sixty months inside the
    납입기간.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return pols_pay(t) * (1.0 - void_rate_mth(t)) * waiver_rate_mth(t)


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy month t.

    ``pols_pay(t) + pols_waived(t)``: not voided, not dead, not lapsed and not matured,
    whether or not the premium is being waived.  ``pols_if(0) = pols_if_init() = 1``.  This
    is the weight on every cash flow of the same :func:`result_cf` row.  Before birth it is
    the probability that the contract is still valid; from birth it is the probability that
    the insured is alive and the contract in force.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    return pols_pay(t) + pols_waived(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after the void decrement, the waiver and mortality, before lapse — the processing
        order is **void, waiver, mortality, lapse** **[std order]** — so this is the
        population lapses are taken from, plus the waived cohort, which is not exposed to
        them.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return (pols_if(t) - pols_void(t)) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_void(t):
    """Policies de-recognised in policy month t because the pregnancy did not go to term.

    Zero from birth, and zero on every contract that is not a 태아가입.  A void is not a
    termination: 「계약을 무효로 합니다 … 이미 납입한 보험료를 돌려드립니다」
    [S8 제56조] [S9], so the whole premium collected comes back and the contract is treated
    as never having existed.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return pols_if(t) * void_rate_mth(t)


def pols_death(t):
    """Deaths of the **insured** in policy month t, on the survivors of the void decrement.

    Zero before birth.  No 사망보험금 is payable below 만 15세 and the prohibition is
    statutory — 상법 제732조 makes such a contract 무효 [R7] [REG-R50] and 표준약관
    제19조제2호 restates it with 제19조제3호 refusing to extend the age-correction saving to
    it [REG-R25] — so what this decrement produces is not a death benefit but the
    계약자적립액 and the 미경과보험료; see :func:`claims`.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    return (pols_if(t) - pols_void(t)) * mort_rate_mth(t)


def pols_lapse(t):
    """Lapses in policy month t, from the **paying** compartment alone.

    Taken after the void decrement, the waiver and mortality.  A missed premium opens a
    납입최고 of at least 14 days [REG-R25 제26조], operated in practice as a calendar-month
    window running 「납입기일 다음날부터 납입기일이 속하는 달의 다음달 마지막 날까지」 [S8],
    which is why the monthly grid is the right one for it.
    """
    if t < 0 or t >= proj_len() - 1:
        return 0.0
    base = pols_pay(t) * (1.0 - void_rate_mth(t)) - pols_waiver_entry(t)
    return base * (1.0 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Policies reaching the 100세 계약해당일: the whole surviving block, at the last row.

    Non-zero only at ``t = proj_len() - 1``, the terminal 계약해당일 index.  They are paid
    whatever 계약자적립액 remains and nothing else — there is **no
    만기환급금** on the protection part [S1] [S2], and on the published grid the residual
    is 16.0% of premiums paid at 95 years and effectively nil at 만기 [S2].
    """
    return pols_if(t) if t == proj_len() - 1 else 0.0


# --- benefit amounts, per policy in force ---

def cover_open(t, cover):
    """1 where cover ``j`` is on risk in policy month t, otherwise 0.

    Three gates, in this order.  **Birth**: every cover on the child's own life is closed
    while :func:`born` is false [S8 제54조] [R2].  **Expiry**: nothing is on risk at
    ``t = proj_len() - 1``, the 계약해당일 on which the contract ends.  **The 면책기간**: the
    두 cancer limbs are closed for :func:`waiting_mths` months from the 계약일, which on the
    anchor cell and on every contract issued below 보험나이 15 is no months at all
    [S3] [S11] [R5].

    Waiting periods that survive and are **not** swept away with the cancer one: the 90-day
    보장개시일 on the 누수사고 limb of the liability rider, which resets at every renewal
    [S5] [S3], carried in :func:`benefit_pp`.
    """
    if not born(t) or t >= proj_len() - 1:
        return 0.0
    if cover in ("cancer", "minor_cancer") and t < waiting_mths():
        return 0.0
    return 1.0


def reduction_factor(t):
    """The 감액 factor on a diagnosis benefit in policy month t: 1.0 throughout the base.

    0.5 while ``t < reduction_mths()`` where the switch is on, being the first-year 50%
    that survives at two carriers [S6] [S11].  :func:`reduction_mths` returns zero on a
    태아 contract whatever the model point says, because a 변경권고 of 2015 removed the
    감액 from foetal contracts across 17 carriers and 56 products [R2].
    """
    return 0.5 if t < reduction_mths() else 1.0


def neonatal_cost_pp(timing):
    """The 태아 module's expected cost per birth, for one of its two timings.

    ``"birth"`` is the 태아보장기간 limbs — 출생위험 on its three tiers and 조산 진단 —
    which pay once, at birth, on an event of the pregnancy or the delivery [S1] [S2].
    ``"block"`` is the 1년만기 신생아 block — the incubator and perinatal day benefits, the
    two 선천이상 limbs and 신생아 뇌출혈 — spread evenly over its twelve months [S1] [S8].

    Two of the limbs are **day-capped rather than amount-capped** and are implemented as
    written::

        incubator benefit = 50,000 x max(0, min(days_used, 60) - 2)
        perinatal cash    = 10,000 x max(0, min(stay_days, 120) - 3), stay_days >= 4

    from 「최고 60일을 한도로 실제 사용일수에서 2일을 공제하고」 [S1] and 「3일 초과
    1일당, 1회 입원당 120일 한도」 [S8], so the ``units`` column of *neonatal_table.csv*
    holds expected paid days after the deduction and inside the cap.  The module's cost is
    a length-of-stay question rather than an amount question, which is why the supervisor's
    own worked claim — ₩16,836,420 on a birth at 32 weeks and 1.84 kg [R3] — is the useful
    datum.
    """
    if not foetal():
        return 0.0
    tab = data.neonatal_table()                                      # noqa: F821
    total = 0.0
    for item in tab.index:
        row = tab.loc[item]
        if str(row["timing"]) != timing:
            continue
        amount = (float(row["amount"])
                  + float(row["amount_ratio"]) * sum_assured("neonatal"))
        total += float(row["freq"]) * float(row["units"]) * amount
    return total


def benefit_pp(t, kind):
    """The expected benefit outgo of kind ``k`` in policy month t, **per policy in force**.

    ``"DISABILITY"``
        the 기본계약 and its 질병 twin: ``S x severity x i(t)`` on each.  The 기본계약 is
        a **percentage scale, not a lump sum** — 보험가입금액 × 장해지급률 on a continuous
        3~100% band, payable more than once with the percentages accumulating
        [R12] [S1] [S2] [S11] — and the modal 장해지급률 on a child accident is small, so a
        model treating the cover as a lump sum at ``S`` overstates the liability by about
        eight times.  장해 is a **settled** impairment, 「치유된 후 신체에 남아 있는
        영구적인」 [REG-R25], so its incidence lags the accident rather than coinciding
        with it.

    ``"DIAGNOSIS"``
        암(유사암 제외), 유사암, 뇌출혈 and 급성심근경색증, each **최초 1회한** and each
        weighted by its own :func:`frac_open` ledger, times :func:`reduction_factor`.  The
        유사암 tier is 20% of the general amount on the chassis ratio, and its shape is the
        clearest illustration of what a 100세만기 child policy is: 갑상선암 is
        overwhelmingly an adult cancer, so the tier costs almost nothing for thirty years
        and then becomes the most frequently paid diagnosis benefit in the contract.

    ``"SURGERY"``
        the 수술비 on the three named diseases, at ``surgery_rate_j`` given the diagnosis
        **[std]**.  It follows the first diagnosis rather than repeating, the model carrying
        no re-diagnosis mechanic; 재진단암 is an option and is out of the base [S1] [S3].

    ``"HOSPITAL"``
        ``hosp_daily() x (days_acc + days_dis) / 12 x hosp_cap_factor``.  The two ``hosp_*``
        causes are expected **days** per policy year rather than frequencies, and the cap
        factor is what survives the 1~180일 per-stay limit [R12] [S2].  **No 180-day
        one-hospitalization memory is implemented**: no retrieved Korean child wording
        states a re-admission grouping rule, and inventing one would be an unsourced
        benefit mechanic.

    ``"EVENT"``
        골절진단비 and 화상진단비, payable repeatedly.  Small and frequent, which is the
        opposite of the chassis.

    ``"LIABILITY"``
        가족일상생활배상책임, scaled by the ratio of the model point's limit to the
        ₩100,000,000 the comparison basis prices.  The **누수사고 limb's 90-day
        보장개시일 resets to the renewal date at every renewal** of the 3년만기 갱신형 block
        [S5] [S3], so ``leak_share`` of the cost is off for the first three months of each
        36-month cycle — the one place in this model where the renewal mechanic has a cash
        consequence.  It is also the only limb whose claim is a **third party's loss**
        rather than a state of the insured, and the cover only a non-life licence may write
        [R5] [S5].

    ``"NEONATAL"``
        the 태아 module, on its two terms.
    """
    if kind == "NEONATAL":
        if not foetal():
            return 0.0
        if t == birth_month():
            return neonatal_cost_pp("birth") + neonatal_cost_pp("block") / 12.0
        if birth_month() < t < foetal_cover_end():
            return neonatal_cost_pp("block") / 12.0
        return 0.0
    if not born(t) or t >= proj_len() - 1:
        return 0.0
    if kind == "DISABILITY":
        return (sum_assured("disability") * basis_param("disab_severity")
                * inc_rate_mth(t, "disability")
                + sum_assured("disease_disab")
                * basis_param("disease_disab_severity")
                * inc_rate_mth(t, "disease_disab"))
    if kind == "DIAGNOSIS":
        total = 0.0
        for cause in ("cancer", "minor_cancer", "cerebral", "cardiac"):
            total += (sum_assured(cause) * inc_rate_mth(t, cause)
                      * frac_open(t, cause) * cover_open(t, cause))
        return total * reduction_factor(t)
    if kind == "SURGERY":
        total = 0.0
        for cause in ("cancer", "cerebral", "cardiac"):
            total += (basis_param("surgery_rate_" + cause)
                      * inc_rate_mth(t, cause) * frac_open(t, cause)
                      * cover_open(t, cause))
        return sum_assured("surgery") * total
    if kind == "HOSPITAL":
        days = (inc_rate(t, "hosp_acc") + inc_rate(t, "hosp_dis")) / 12.0
        return hosp_daily() * days * basis_param("hosp_cap_factor")
    if kind == "EVENT":
        return (sum_assured("fracture") * inc_rate_mth(t, "fracture")
                + sum_assured("burn") * inc_rate_mth(t, "burn"))
    if kind == "LIABILITY":
        scale = sum_assured("liability") / 100000000.0
        gate = (1.0 - basis_param("leak_share")
                if t % liability_cycle_mths < 3 else 1.0)            # noqa: F821
        return (inc_rate_mth(t, "liability") * basis_param("liability_severity")
                * scale * gate)
    raise ValueError("invalid kind")


def benefit_cost_pp(t):
    """The whole morbidity benefit cost of policy month t, per policy in force.

    The sum of the seven :func:`benefit_pp` kinds — everything the contract pays on a state
    of the insured or on a third party's loss, and nothing it pays on the account.  This is
    the quantity :func:`risk_prem_ann_pp` accumulates over the first policy year to form the
    notional 보험가입금액 of 감독규정 [별표 15] 제9호 [REG-R21].
    """
    return sum(benefit_pp(t, k) for k in
               ("DISABILITY", "DIAGNOSIS", "SURGERY", "HOSPITAL", "EVENT",
                "LIABILITY", "NEONATAL"))


def claim_count_pp(t):
    """The expected number of benefit **events** in policy month t, per policy in force.

    Every discrete claim event — the two 후유장해 limbs, the four diagnosis limbs, 골절,
    화상 and 배상책임 — but not hospital days, which are metered rather than counted.  It
    is the exposure the claim handling expense is charged on.
    """
    if not born(t) or t >= proj_len() - 1:
        return 0.0
    n = inc_rate_mth(t, "disability") + inc_rate_mth(t, "disease_disab")
    for cause in ("cancer", "minor_cancer", "cerebral", "cardiac"):
        n += inc_rate_mth(t, cause) * frac_open(t, cause) * cover_open(t, cause)
    n += (inc_rate_mth(t, "fracture") + inc_rate_mth(t, "burn")
          + inc_rate_mth(t, "liability"))
    return n


# --- the account, the surrender charge and the surrender value ---

def cum_prem_pp(t):
    """The cumulative **scheduled** core office premium at time t, per policy.

    A **time-point** value, at time ``t`` (``t = 0`` at the 계약일), read as the opening
    value of period ``t`` — before that month's premium, so ``cum_prem_pp(0) = 0`` — and
    the exit payments of month ``t``, which fall at its end, are valued on it **[std]**.

    ``premium_mth() x min(t, prem_period_mths())``: the premium is payable monthly in
    advance, so twelve instalments have been paid by ``t = 12``.  It is the *scheduled*
    stream and not the collected one, because the 환급률 the 상품요약서 publishes is a
    ratio to 납입보험료 on a policy that stayed in force, and because a waived premium is
    **deemed paid** for every benefit purpose [S2].  The 태아 module's own premium is
    excluded: the 적립부분 belongs to the core contract, and the module is 순수보장성 over
    a seventeen-month term.
    """
    return premium_mth() * min(t, prem_period_mths())


def refund_build(d):
    """The published 표준형 환급률 at duration ``d`` years, linearly interpolated.

    The grid is the one a current 상품요약서 publishes on a named specimen contract — 0.0%
    at 1 year, 45.6% at 3, 62.5% at 5, 73.7% at 10, 78.3% at 15, 82.6% at 20, 101.2% at 30,
    122.5% at 40, 144.1% at 50 and 158.9% at 60, at 공시이율 1.7% (2026-07), 평균공시이율
    2.5% and 최저보증이율 0.3% [S2] — held flat beyond 60 years and taken down to maturity
    by :func:`refund_taper`.

    The shape has two features no other ``krlib`` protection product produces.  The value
    **crosses premiums paid at about year 30**, because the 적립부분 compounds at the
    공시이율 while the 보장부분 reserve is still building.  And only a hundred-year term
    can do it.
    """
    tab = data.av_table().loc["build"]["value"]                      # noqa: F821
    pv = [(float(k), float(v)) for k, v in tab.items()]
    if d <= pv[0][0]:
        return pv[0][1]
    if d >= pv[-1][0]:
        return pv[-1][1]
    for i in range(len(pv) - 1):
        x0, y0 = pv[i]
        x1, y1 = pv[i + 1]
        if x0 <= d <= x1:
            return y0 + (d - x0) / (x1 - x0) * (y1 - y0)
    raise ValueError("duration out of range")


def refund_taper(r):
    """The terminal collapse factor at runoff fraction ``r``, linearly interpolated.

    1.0 until 85% of the term has run, then down to zero at 만기.  **Both forms collapse at
    maturity** — the 표준형 to 16.0% of premiums paid at 95 years and the 미지급형 to 0.0%
    [S2] — because there is no 만기환급금 on the protection part and what remains is only
    the residual 적립부분.  The node at 0.95 is calibrated to reproduce that published
    16.0% on a 100세만기 contract; indexing on the fraction of the term rather than on a
    duration is what lets one shipped grid also serve the 30세만기 and 110세만기 points.
    """
    tab = data.av_table().loc["taper"]["value"]                      # noqa: F821
    pv = [(float(k), float(v)) for k, v in tab.items()]
    if r <= pv[0][0]:
        return pv[0][1]
    if r >= pv[-1][0]:
        return pv[-1][1]
    for i in range(len(pv) - 1):
        x0, y0 = pv[i]
        x1, y1 = pv[i + 1]
        if x0 <= r <= x1:
            return y0 + (r - x0) / (x1 - x0) * (y1 - y0)
    raise ValueError("runoff out of range")


def refund_ratio(t):
    """The 환급률 of the notional 표준형 at time t: build times taper.

    A **time-point** value, at time ``t`` (``t = 0`` at the 계약일), read as the opening
    value of period ``t`` **[std]**, on the same convention as :func:`cum_prem_pp`.

    The ratio the product is sold on and the one the supervisor regulates, and the ratio
    against which a suppressed form's 50% is measured [REG-R19 제7-66조제4항제2호].
    """
    return refund_build(duration_years(t)) * refund_taper(runoff(t))


def cv_std_pp(t):
    """The 해약환급금 of the notional 표준형 at time t, per policy.

    A **time-point** value, at time ``t`` (``t = 0`` at the 계약일), read as the opening
    value of period ``t`` **[std]**, on the same convention as :func:`cum_prem_pp`.

    ``refund_ratio(t) x cum_prem_pp(t)``.  「금융감독원장이 인가한 산출기준에 따라 계산한
    이 보험의 **순보험료식 계약자적립액에서 해약공제액을 공제한 금액**」 [S2] — so this is
    already net of the 해약공제액 and is the amount payable, not the account.  It is the
    comparator the suppressed forms are measured against, and it is **synthetic**: 「해지율을
    적용하지 않은 상품이며, 비교안내를 위한 종목으로 실제로 판매하지 않음」 [S3] [S1].
    """
    return refund_ratio(t) * cum_prem_pp(t)


def cv_grade_ratio(t):
    """The 미지급형Ⅲ ladder: the fraction of the 표준형 value payable at policy month t.

    Published in full, where M is the payment term in years: **5%** from the day after the
    end of year M to the day before the M+2 계약해당일, then 10, 15, 20, 25, 30, 35, 40, 45
    and finally **50%** from M+18 to the end of the term [S1].  Zero during the 납입기간.
    """
    if t < prem_period_mths():
        return 0.0
    step = (t - prem_period_mths()) // 24
    return min(0.05 * (step + 1), cv_floor_ratio())


def cv_pp(t):
    """CV(t): the 해약환급금 actually payable on surrender at time t, per policy.

    A **time-point** value, at time ``t`` (``t = 0`` at the 계약일), read as the opening
    value of period ``t``: the lapses of month ``t`` fall at its end and are paid
    ``cv_pp(t) + unearned_prem_pp(t)`` **[std]**.

    On the **표준형** it is :func:`cv_std_pp`.  On the **미지급형** it is nil through the
    entire 납입기간 and ``cv_floor_ratio()`` of the notional 표준형 value afterwards; on the
    **미지급형Ⅲ** it climbs the published ten-step ladder.  Floored at zero
    [REG-R19 제7-66조제1항제1호].

    **The suppressed form's value is a cliff, not a curve.**  The published grid shows it
    nil through the whole payment period — the 「60원」 and 「550원」 entries between are
    rounding on a nominally zero quantity — and then 64.0% of premiums paid ten years after
    완납 [S2].  That asymmetry is the whole difference between the two forms in a
    projection: the same lapse rate produces a very different cash flow depending on whether
    anything is paid on it, and on the 미지급형 there is also no 보험계약대출 and no
    automatic premium loan to break the fall [REG-R28].
    """
    if cv_form() == "std":
        return max(0.0, cv_std_pp(t))
    if cv_form() == "susp":
        if t < prem_period_mths():
            return 0.0
        return max(0.0, cv_floor_ratio() * cv_std_pp(t))
    return max(0.0, cv_grade_ratio(t) * cv_std_pp(t))


def risk_prem_ann_pp():
    """The expected benefit cost of the **first policy year**, per policy issued.

    The 위험보험료 term of 감독규정 [별표 15] 제9호 [REG-R21].  On a 태아 contract it
    carries the 태아 module, which is most of it: the module's whole cost falls inside the
    first thirteen months of a hundred-year contract.
    """
    return sum(benefit_cost_pp(t) for t in range(0, min(12, proj_len() - 1)))


def sa_notional_pp():
    """The **notional** 보험가입금액 of 감독규정 [별표 15] 제9호, per policy [REG-R21].

    This contract has no 일반사망보험금, so [별표 15] 제3호 does not apply and 제9호 does:
    「보험가입금액 = (위험보험료 / 정기보험의 위험보험료) × 정기보험의 보험가입금액」.  A
    제3보험 contract with no death benefit therefore gets a notional face amount by scaling
    a term policy's by the ratio of risk premiums, computed at the 기준연령 요건 — 남자 만
    40세 [REG-R9 제1-2조제2호].  Since a term policy's risk premium per unit of face is its
    mortality rate, the notional amount is the first year's risk premium divided by that
    rate.  It is that notional amount, and **not** the ₩100,000,000 of accidental
    disability cover, that enters the 10/1000 term of the 표준해약공제액.
    """
    return risk_prem_ann_pp() / mort_rate_at_age(ref_age, ref_sex)   # noqa: F821


def prem_net_ann_pp():
    """The 연납순보험료 of the 표준해약공제액 formula, per policy [REG-R20].

    ``12 x premium_mth() x net_prem_ratio`` **[std]**.  [별표 14] note 3 requires the
    연납순보험료 to be recomputed on a 전기납 basis, or on **20년납 where the term is 20
    years or more**, which binds here.  No Korean 예정사업비율 is published — the
    산출방법서 that holds it is an undisclosed 기초서류 [REG-R2] — so the 순보험료 share is
    a standardization.
    """
    return 12.0 * premium_mth() * basis_param("net_prem_ratio")


def surr_chg_coef():
    """The 해약공제계수 of 감독규정 [별표 14]: the policy term in years, capped at 20.

    「보험기간(최대 20년)」 for a 보장성보험 [REG-R20].  On every model point here the term
    is 30 years or more, so the coefficient is 20 throughout.
    """
    return min(term_age() - issue_age(), surr_chg_max_coef)          # noqa: F821


def surr_chg_cap_pp():
    """The **표준해약공제액** of 감독규정 [별표 14], per policy [REG-R20].

    ``5% x 연납순보험료 x 해약공제계수 + 보장성보험의 보험가입금액 x 10/1000``, the second
    term taken on the notional amount of :func:`sa_notional_pp` and at the schedule's own
    rate of **10/1000**, which is one per cent and not one per mille.

    **On this product the formula limb does not bind and that is the finding.**  The
    notional 보험가입금액 of [별표 15] 제9호 is ₩132,306,409 on the anchor cell, so the
    10/1000 term alone is ₩1,323,064 and the whole formula ₩1,575,064 — **56.3 months** of
    core office premium, against the FSC's 2019 statement of the *same* ceiling as
    **보장성보험 13배** of the monthly premium [REG-R29].  The two readings of one cap are
    that far apart because 제9호 divides this contract's whole first-year risk premium by a
    40-year-old's mortality rate, and a bundled child stack has a large risk premium and a
    small death rate.  The composite therefore takes the **lesser** of the two, which is the
    treatment ``Cancer_KR_S`` states for the same mechanic: ``surr_chg_cap_months`` is the
    13 of [REG-R29] and it binds on every shipped model point.  Both limbs rest on inputs
    that are themselves **[std]**, and :func:`acq_cost_months` publishes the ratio actually
    reached so the two readings can be compared rather than asserted equal.
    """
    formula = (surr_chg_prem_rate * prem_net_ann_pp() * surr_chg_coef()  # noqa: F821
               + surr_chg_sa_rate * sa_notional_pp())                 # noqa: F821
    return min(formula, surr_chg_cap_months * premium_mth())         # noqa: F821


def surr_chg_period():
    """The 해약공제기간 in months: the 납입기간, capped at **7 years** [REG-R19].

    감독규정 제7-66조제1항제2호 caps it at seven years, which on a 20년납 contract is what
    binds; on a shorter payment term the payment period does.
    """
    return 12 * min(prem_period_years(), surr_chg_max_years)         # noqa: F821


def surr_chg_pp(t):
    """X(t): the unamortised 해약공제액 at time t, per policy.

    A **time-point** value, at time ``t`` (``t = 0`` at the 계약일), read as the opening
    value of period ``t`` **[std]**: full at ``t = 0`` and nil from ``t = 84`` on a
    20년납 contract.

    Released linearly over the 해약공제기간 **[std]**, from the full 표준해약공제액 at
    issue to nil at the end of it.  It is the difference between the amount payable on
    surrender and the 계약자적립액 the contract is actually holding, which is what makes the
    death benefit of a 제3보험 contract larger than its surrender value in the early years.
    """
    n = surr_chg_period()
    if n <= 0:
        return 0.0
    return surr_chg_cap_pp() * max(0.0, 1.0 - t / n)


def av_pp(t):
    """AV(t): the 계약자적립액 at time t, per policy.

    A **time-point** value, at time ``t`` (``t = 0`` at the 계약일), read as the opening
    value of period ``t`` — before that month's premium, so ``av_pp(0) = 0`` and twelve
    instalments stand at ``t = 12`` — and the deaths and maturities of month ``t``, which
    fall at its end, are valued on it **[std]**.

    The quantity 감독규정 제7-63조제1항제1호 makes payable on a death the contract does not
    cover [REG-R17], 표준약관 제22조 implements — 「산출방법서에서 정하는 바에 따라 회사가
    적립한 **사망 당시의 계약자적립액**」 [REG-R25] — and 상법 제736조 floors [REG-R50].
    It accrues monthly before 납입완료 and daily afterwards, credited at the 공시이율 and
    floored at the 최저보증이율 [REG-R19 제7-66조제1항제4호]; the model reads the published
    progression rather than running the recursion, and does **not** implement the 공시이율
    reset, which it carries by reference to ``WholeLife_KR_S``.

    **The published grid does not determine it in the first two years and this is where the
    [std] enters.**  What the 상품요약서 publishes is 「순보험료식 계약자적립액에서
    해약공제액을 공제한 금액」 [S2] — the surrender value, already net of the charge and
    floored at zero — so the account can be recovered by adding the unamortised charge back
    only where the floor is not binding.  Where it is, the identity gives no more than
    ``0 <= AV <= 해약공제액``, and the account is capped instead at the cumulative **net**
    premium ``net_prem_ratio x cum_prem_pp(t)``, which is the most a 순보험료식 reserve can
    have accumulated before any interest or mortality.  The account therefore starts at nil,
    as it must, rather than at the surrender charge.
    """
    gross = cv_std_pp(t) + surr_chg_pp(t)
    cap = max(cv_std_pp(t), basis_param("net_prem_ratio") * cum_prem_pp(t))
    return min(gross, cap)


def unearned_prem_pp(t):
    """The 미경과보험료 refundable on a termination in policy month t, per policy.

    Half a month's premium **[std]**, deaths and terminations being taken as uniform within
    the month.  「이 계약이 소멸하는 경우 회사는 … 미경과보험료를 계약자에게 돌려드립니다」
    [REG-R19 제7-66조제5항], added to whatever surrender value is paid.
    """
    return 0.5 * premium_mth_pp(t)


def acq_cost_pp():
    """계약체결비용 at issue, per policy **[std]**.

    **No retrieved document quantifies any expense item for this product.**  Both
    상품요약서 in the set define 계약체결비용 and 계약관리비용 and then give no number, and
    the 산출방법서 that holds the 예정사업비율 is a filed but undisclosed 기초서류
    [REG-R2].  What is available is a statutory **ceiling**: 감독규정 [별표 14] caps the
    deductible acquisition cost at the 표준해약공제액 [REG-R20] and the FSC's 2019 expense
    reform states the same cap as thirteen months' premium for a 보장성보험 [REG-R29].  The
    composite sets it at ``acq_cost_ratio`` of the cap.
    """
    return acq_cost_ratio * surr_chg_cap_pp()                        # noqa: F821


def acq_cost_months():
    """The acquisition cost expressed in months of core office premium, as a diagnostic.

    The FSC's 2019 expense reform states the 표준해약공제액 cap as **thirteen months'
    premium** for a 보장성보험 [REG-R29], while the [별표 14] computation is driven by the
    notional 보험가입금액 of [별표 15] 제9호 [REG-R21] instead.  The two readings of one cap
    are far apart on this product — the formula limb reaches **56.25 months** of core premium
    on the anchor cell — so :func:`surr_chg_cap_pp` takes the lesser of them and the ratio
    actually reached is published rather than asserted.  The 13-month limb binds on every
    shipped model point, so this returns 0.9 x 13 = **11.7** on all ten of them.
    """
    return acq_cost_pp() / premium_mth()


def comm_init_pp():
    """First-year commission, per policy **[std]**.

    ``comm_init_share`` of :func:`acq_cost_pp`.  No Korean carrier publishes a commission
    scale; what regulation supplies instead is a cap — first-year remuneration within the
    first year's expected premium, and an obligation to offer an instalment structure paying
    no more than 60% of the 표준해약공제액 a year [REG-R22 제4-32조제5항·제8항] [REG-R29].
    """
    return comm_init_share * acq_cost_pp()                           # noqa: F821


# --- cash flows ---

def premium_mth_pp(t):
    """P: the monthly office premium due in policy month t, per policy, on all streams.

    Three streams on the anchor cell, and the third is a real feature of the contract
    rather than an artefact of the composite::

        core 보장보험료          KRW 27,000    t = 0 .. 239
        계약자 waiver module      KRW 1,000     t = 0 .. 239
        태아 module (전기납)      KRW 3,000     t = 0 .. 16

    — the first two entering as the single ``premium_mth`` input and the third as
    ``premium_foetal_mth``, so the office premium is **₩31,000 a month to ``t = 16`` and
    ₩28,000 from ``t = 17`` to ``t = 239``** [S2] [S1].  Level for the whole 납입기간 on the
    비갱신 core: the contract is 무배당, so there is no dividend and no premium review
    [S1] [S2] [S11] [REG-R12].
    """
    core = premium_mth() if t <= prem_end() else 0.0
    foet = premium_foetal_mth() if t <= foetal_prem_end() else 0.0
    return core + foet


def prem_discount_factor(t):
    """The factor applied to the office premium by the 2026 저출산 discount [R6].

    1.0 outside the discount window and in the base run.
    """
    if t < prem_discount_mths():
        return 1.0 - prem_discount_rate()
    return 1.0


def premiums(t):
    """Premium income at the start of policy month t, an inflow.

    Carried on :func:`pols_pay` alone: a waived policy pays nothing while its premiums are
    **deemed paid** for every benefit purpose, which is the whole point of the waiver and
    the reason it is a state rather than a rate adjustment.  It runs through the pre-birth
    period on all three streams — the contract is on risk for the 태아보장기간 and the
    premium is payable from the 계약일 — and stops at the earliest of 납입완료, death,
    lapse, the void, the operation of either waiver and, for the 태아 module, the end of its
    own seventeen-month term.
    """
    return premium_mth_pp(t) * prem_discount_factor(t) * pols_pay(t)


def claims(t, kind=None):
    """Benefit outgo in policy month t, by kind; the total when kind is omitted.

    The seven morbidity kinds of :func:`benefit_pp`, weighted by :func:`pols_if`, and four
    kinds that arise from the decrements:

    ``"DEATH"``
        **not a death benefit.**  There is no 사망보험금 below 만 15세 and the prohibition
        is statutory — 상법 제732조 makes such a contract 무효 [R7] [REG-R50] and 표준약관
        제19조 restates it [REG-R25] — so what is paid is the **계약자적립액 at the date of
        death plus the 미경과보험료**, which is what 감독규정 제7-63조제1항제1호 requires of
        a 제3보험 contract on a death it does not cover [REG-R17] and what 상법 제736조
        floors [REG-R50].  On the 미지급형 switch that sum is close to nil for the whole
        payment period, and a family whose child dies in year 10 receives almost nothing:
        a real and uncomfortable property of the suppressed form, stated rather than
        smoothed.

    ``"LAPSE"``
        the 해약환급금 on voluntary 해지, plus the 미경과보험료.  On a 무해지 contract
        inside the 납입기간 this is **identically zero**, which is precisely why the lapse
        assumption over that period is worth so much CSM and why it became a supervisory
        matter [R11] [REG-R27] [REG-R28].

    ``"MATURITY"``
        whatever 계약자적립액 remains at the 100세 계약해당일.  There is **no 만기환급금**
        on the protection part [S1] [S2], and on the shipped progression the residual is nil
        at 만기, so the column is a column of zeros — published rather than dropped, because
        the residual is a real quantity on a contract whose term ends earlier.

    ``"VOID"``
        the **return of every premium paid** where the pregnancy does not go to term
        [S8 제56조] [S9].  It is not a surrender: the contract is 무효 and is de-recognised,
        so the cash flow is a refund of premiums already collected and belongs in a validity
        adjustment rather than in the lapse column.
    """
    if kind is None:
        return sum(claims(t, k) for k in
                   ("DISABILITY", "DIAGNOSIS", "SURGERY", "HOSPITAL", "EVENT",
                    "LIABILITY", "NEONATAL", "DEATH", "LAPSE", "MATURITY",
                    "VOID"))
    if kind == "DEATH":
        return (av_pp(t) + unearned_prem_pp(t)) * pols_death(t)
    if kind == "LAPSE":
        return (cv_pp(t) + unearned_prem_pp(t)) * pols_lapse(t)
    if kind == "MATURITY":
        return av_pp(t) * pols_maturity(t)
    if kind == "VOID":
        return (cum_prem_pp(t) + prem_foetal_paid_pp(t)) * pols_void(t)
    return benefit_pp(t, kind) * pols_if(t)


def prem_foetal_paid_pp(t):
    """The cumulative 태아 module premium paid by time t, per policy.

    A **time-point** value, at time ``t`` (``t = 0`` at the 계약일), read as the opening
    value of period ``t`` **[std]**, on the same convention as :func:`cum_prem_pp`.

    Needed only by the ``"VOID"`` claim kind: where the pregnancy does not go to term the
    contract is 무효 and **every** premium paid comes back [S8 제56조], the module's own
    included, so the refund is the whole of both streams and not merely the core.
    """
    if not foetal():
        return 0.0
    return premium_foetal_mth() * min(t, foetal_prem_end() + 1)


def claim_expenses(t):
    """The claim handling expense on the month's benefit events **[std]**.

    ₩30,000 per event, uninflated, charged on :func:`claim_count_pp` and on the deaths and
    voids of the month.  **No Korean expense rate was obtained from any source**: the
    약관 name 계약체결비용 and 계약관리비용 and quantify neither, and the 산출방법서 that
    holds the 예정사업비율 is an undisclosed 기초서류 [REG-R2].  Published as its own
    column in :func:`result_cf` and deducted explicitly in :func:`net_cf`; it is **not**
    inside :func:`expenses`.
    """
    events = claim_count_pp(t) * pols_if(t) + pols_death(t) + pols_void(t)
    return expense_claim_pp * events                                 # noqa: F821


def inflation_factor(t):
    """The expense inflation factor at policy month t: ``(1 + pi)^(t/12)`` **[std]**.

    2.0% a year, the Bank of Korea's own inflation target, chosen because no Korean expense
    basis exists to anchor anything better.  **Over a hundred-year horizon 2% compounds to
    7.2**, so on this product the assumption is not a detail: per-policy maintenance over
    the eighty paid-up years is the largest single expense item in the projection, and it is
    held as its own parameter for that reason.
    """
    return (1.0 + inflation_rate) ** (t / 12.0)                      # noqa: F821


def expenses(t):
    """계약체결비용 and 계약관리비용 in policy month t **[std]** — acquisition and upkeep.

    At issue, the part of :func:`acq_cost_pp` not paid away as :func:`comm_init_pp`.
    Thereafter the 계약관리비용, which the 약관 subdivides into 유지관련비용 and 기타비용
    and quantifies nowhere: a per-policy monthly amount inflating at 2%, plus a percentage
    of premium income while premiums are paid.  Maintenance continues **for the whole
    hundred years**, not to 납입완료 — that is the structural point of this product, a
    contract on which the premium stops after twenty years and the obligations run for
    eighty more.  There is no separate surrender expense; it is folded into maintenance
    **[std]**.  The claim handling expense is **not** here: it is :func:`claim_expenses`,
    published in its own column.
    """
    if t >= proj_len() - 1:
        return 0.0
    acq = max(0.0, acq_cost_pp() - comm_init_pp()) * pols_if(t) if t == 0 else 0.0
    maint = expense_maint_pp * inflation_factor(t) * pols_if(t)      # noqa: F821
    return acq + maint + expense_maint_prem_rate * premiums(t)       # noqa: F821


def commissions(t):
    """Commission outgo in policy month t **[std]**.

    :func:`comm_init_pp` at issue, then a renewal percentage of premium income from the
    thirteenth month to 납입완료.  No renewal commission is paid after 납입완료: a
    projection that keeps charging it there is charging commission on a premium nobody pays,
    and on this product that would be eighty years of it.
    """
    if t >= proj_len() - 1:
        return 0.0
    init = comm_init_pp() * pols_if(t) if t == 0 else 0.0
    renew = (comm_renewal_rate * premiums(t)                         # noqa: F821
             if 12 <= t <= prem_end() else 0.0)
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy month t, **income positive**.

    Premiums less benefits, claim handling expense, acquisition and maintenance expense and
    commission.  The library-wide sign, which is also the notes' own, so there is no
    outgo-positive ``liability_cf`` companion.

    The shape to expect is the product in one line: a new business strain at ``t = 0``, a
    positive stretch of twenty years in which a level premium is collected against a
    morbidity that has barely begun, and then **eighty years of pure outgo** in which the
    premium has stopped, maintenance continues, and the diagnosis and hospital limbs reach
    the ages they were priced for.  Undiscounted, the total is heavily negative, and that is
    not a defect in the projection: it is what a hundred-year contract with a twenty-year
    premium term looks like before discounting.  :func:`equiv_premium_mth_pp` is where the
    two sides are made to balance.
    """
    return (premiums(t) - claims(t) - claim_expenses(t) - expenses(t)
            - commissions(t))


# --- pricing diagnostics ---

def pv_factor(t):
    """The discount factor at policy month t on the 보장부분 적용이율.

    **2.75% a year [std]**, the modal value of the 보장부분 적용이율 column of the
    comparison board, whose observed range is 2.50%–3.00% [S11].  A full-text search of the
    감독규정 returns **zero** occurrences of 예정이율: the regulation speaks only of the
    계약자적립액 적용이율 and of the 금리확정형 / 금리연동형 distinction [REG-R9] [REG-R48],
    and what the board publishes instead is the 보장부분 적용이율 — the pricing rate under
    another name.

    Used only by the equivalence diagnostics below.  **The projection itself does not
    discount**: every ``technical-notes.md`` in this library specifies gross liability cash
    flows and leaves discounting, the 책임준비금, the IFRS 17 CSM and the K-ICS 요구자본 to
    a separate layer that consumes them.
    """
    return (1.0 + prem_int_rate) ** (-t / 12.0)                      # noqa: F821


def epv_outgo_pp():
    """The expected present value of every outgo, per policy issued, at the 적용이율.

    Benefits, claim handling expense, acquisition and maintenance expense and commission.
    """
    return sum(pv_factor(t) * (claims(t) + claim_expenses(t) + expenses(t)
                               + commissions(t))
               for t in range(0, proj_len()))


def epv_prem_unit_pp():
    """The expected present value of **one unit** of monthly core premium, per policy.

    The discounted, in-force-weighted count of premium instalments actually collected —
    stopping at 납입완료, at death, at lapse, at the void and at either waiver.  It is the
    annuity the equivalence premium is divided by, and on a 20년납 hundred-year contract it
    is where the waiver and the lapse assumption do all their work.
    """
    return sum(pv_factor(t) * prem_discount_factor(t) * pols_pay(t)
               for t in range(0, prem_period_mths()))


def equiv_premium_mth_pp():
    """The level monthly core premium at which the discounted streams balance.

    ``epv_outgo_pp() / epv_prem_unit_pp()``, on the shipped basis and at the 보장부분
    적용이율.  It is a **first-order** equivalence: the expense basis is held at the level
    the shipped premium produces rather than re-scaled with the answer, so a premium that
    moves a long way moves the percentage-of-premium expense terms with it.

    This is the figure the technical notes' equivalence calculation reports, and **where it
    and the shipped ₩27,000 / ₩28,000 differ, this one governs** — nothing in the model
    depends on the model point's premium being a market rate.  Reading it against the
    published cluster is the only calibration of a Korean child policy this file can make:
    the board's own levels vary by a factor of seven on a nominally standardised basis
    [S11], because carriers include different compulsory sets in the quoted 보장보험료.
    """
    denom = epv_prem_unit_pp()
    if denom <= 0.0:
        return 0.0
    return epv_outgo_pp() / denom


# --- checks ---

def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy month t; zero everywhere.

    ``l(t) - l(t+1)`` less the voids, deaths, lapses and maturities of the month.  Four
    exits, not two, and the first of them is the one that makes this product different: a
    voided contract has not lapsed and has not died, and netting it into either would hide
    a decrement and mis-state the cash flow that goes with it.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_void(t) - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected policy month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so one
    test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the signed
    residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(0, proj_len()))


def check_waiver_split_resid(t):
    """The residual of the paying / waived split in policy month t; zero everywhere.

    ``pols_pay(t) + pols_waived(t) - pols_if(t)``.  The waiver moves a policy between the
    two compartments without changing the block, so this is what says the second decrement
    life has been carried without leaking policies into or out of the projection.
    """
    return pols_pay(t) + pols_waived(t) - pols_if(t)


def check_waiver_split():
    """True when the paying and waived compartments sum to the in-force block, every month."""
    return all(abs(check_waiver_split_resid(t)) <= roll_fwd_tol      # noqa: F821
               for t in range(0, proj_len()))


def check_exit_total_resid():
    """The residual of the exit identity over the whole projection; zero.

    Every policy issued leaves exactly once — by a void, a death, a lapse or the maturity —
    so the four decrements sum over the projection to ``pols_if_init()``.  This is the
    global companion to the per-month roll-forward, and it is what catches a decrement that
    closes locally at every t and still loses mass at the ends.
    """
    total = sum(pols_void(t) + pols_death(t) + pols_lapse(t) + pols_maturity(t)
                for t in range(0, proj_len()))
    return total - pols_if_init()


def check_exit_total():
    """True when the four decrements account for every policy issued."""
    return abs(check_exit_total_resid()) <= roll_fwd_tol * proj_len()  # noqa: F821


def check_cover_at_birth_resid(t):
    """The residual of the 태아가입 gate in policy month t; zero everywhere.

    The sum of every benefit written on the **child's own life** in months before birth.
    「제53조의 태아는 출생시에 피보험자가 됩니다」 [S8 제54조], and cover attaches at birth
    and not at the 계약일 [R2] [R3], so this must be identically zero for ``t <
    birth_month()``.  The 태아 module is deliberately **not** in the sum: its 태아보장기간
    limbs are the one thing that may pay in respect of an event before the insured legally
    exists, and they pay **from the date of birth** [S8 제59조], which is why they are
    tested separately by :func:`check_neonatal_term`.
    """
    if born(t):
        return 0.0
    return sum(claims(t, k) for k in
               ("DISABILITY", "DIAGNOSIS", "SURGERY", "HOSPITAL", "EVENT",
                "LIABILITY", "DEATH"))


def check_cover_at_birth():
    """True when no cover on the child's own life pays before the child is born.

    The identity that makes this a 태아가입 model rather than an ordinary one.  It is
    vacuous on a non-foetal model point, where ``birth_month()`` is zero, and that is the
    right behaviour: the same formula covers both.
    """
    return all(abs(check_cover_at_birth_resid(t)) <= val_tol         # noqa: F821
               for t in range(0, birth_month() + 1))


def check_once_only_resid(t):
    """The worst violation of the 최초 1회한 ledgers at policy month t; zero everywhere.

    Each diagnosis benefit is payable once [S1] [S2] [S11], so its :func:`frac_open` ledger
    must stay inside ``[0, 1]`` and must never rise.  The residual is the largest breach
    across the four causes at that t.
    """
    worst = 0.0
    for cause in ("cancer", "minor_cancer", "cerebral", "cardiac"):
        f = frac_open(t, cause)
        worst = max(worst, -min(f, 0.0), max(f - 1.0, 0.0))
        if t > 0:
            worst = max(worst, f - frac_open(t - 1, cause))
    return worst


def check_once_only():
    """True when every 최초 1회한 ledger is a valid, non-increasing probability."""
    return all(check_once_only_resid(t) <= roll_fwd_tol              # noqa: F821
               for t in range(0, proj_len()))


def check_neonatal_term_resid(t):
    """The 태아 module's outgo outside its own two terms at policy month t; zero everywhere.

    The module runs from the 계약일 to the 출생시점 and then for a 1년만기 block, so it must
    pay in ``birth_month() <= t < foetal_cover_end()`` and nowhere else [S2] [S5] [R5], and
    must pay nothing at all on a contract that is not a 태아가입.
    """
    if foetal() and birth_month() <= t < foetal_cover_end():
        return 0.0
    return claims(t, "NEONATAL")


def check_neonatal_term():
    """True when the 태아 module pays inside its own terms and nowhere else."""
    return all(abs(check_neonatal_term_resid(t)) <= val_tol          # noqa: F821
               for t in range(0, proj_len()))


def check_cv_floor_resid(t):
    """The surrender-value form's residual at policy month t; zero everywhere.

    Three things at once: the payable value is never negative
    [REG-R19 제7-66조제1항제1호]; on a suppressed form it is **exactly nil** through the
    whole 납입기간, the cliff being a contractual fact and not an approximation [S2]; and
    after 납입완료 it is at least ``cv_floor_ratio()`` of the notional 표준형 value on the
    미지급형 and at least 5% of it on the graded ladder
    [REG-R19 제7-66조제4항제2호] [S1].
    """
    if cv_pp(t) < 0.0:
        return -cv_pp(t)
    if cv_form() == "std":
        return 0.0
    if t < prem_period_mths():
        return cv_pp(t)
    floor = (cv_floor_ratio() if cv_form() == "susp"
             else cv_grade_ratio(t)) * cv_std_pp(t)
    return max(0.0, floor - cv_pp(t))


def check_cv_floor():
    """True when the surrender value obeys its form's floor in every projected month."""
    return all(check_cv_floor_resid(t) <= val_tol                    # noqa: F821
               for t in range(0, proj_len()))


def check_av_bounds_resid(t):
    """The residual of the account's own bounds at policy month t; zero everywhere.

    Three inequalities that together say the 계약자적립액 has been recovered from a
    published surrender value without inventing anything: the account is never below the
    amount payable on surrender, it never exceeds that amount grossed up by the whole
    unamortised 해약공제액, and it is never negative.  The first is what makes a death
    benefit on a 제3보험 contract larger than its surrender value in the early years; the
    second is the arithmetic limit of 「순보험료식 계약자적립액에서 해약공제액을 공제한
    금액」 [S2] read backwards.
    """
    gross = cv_std_pp(t) + surr_chg_pp(t)
    return (max(0.0, cv_pp(t) - av_pp(t)) + max(0.0, av_pp(t) - gross)
            + max(0.0, -av_pp(t)))


def check_av_bounds():
    """True when the 계약자적립액 stays inside the bounds its own derivation allows."""
    return all(check_av_bounds_resid(t) <= val_tol                   # noqa: F821
               for t in range(0, proj_len()))


def check_surr_chg_cap_resid(t):
    """The excess of the deducted 해약공제액 over the statutory cap at t; zero everywhere.

    감독규정 [별표 14] caps the surrender charge at the **표준해약공제액** [REG-R20] and
    제7-66조제1항제2호 caps the 해약공제기간 at seven years [REG-R19].  Both are structural
    here, and the check exists so that a user who replaces the [std] inputs of
    :func:`surr_chg_cap_pp` with a company basis finds out at once if the result breaches
    the cap.
    """
    return max(0.0, surr_chg_pp(t) - surr_chg_cap_pp())


def check_surr_chg_cap():
    """True when the surrender charge stays inside the 표준해약공제액 at every duration."""
    return all(check_surr_chg_cap_resid(t) <= val_tol                # noqa: F821
               for t in range(0, proj_len()))


def check_acq_cost_cap_resid():
    """The excess of the acquisition cost over the 표준해약공제액; zero.

    감독규정 [별표 14] caps the deductible 계약체결비용 at the 표준해약공제액 [REG-R20], and
    the thirteen-months-of-premium reading of the same cap [REG-R29] is the limb that binds
    on this product, :func:`surr_chg_cap_pp` taking the lesser of the two.  The ratio the
    acquisition cost actually reaches is published as :func:`acq_cost_months` rather than
    asserted.
    """
    return max(0.0, acq_cost_pp() - surr_chg_cap_pp())


def check_acq_cost_cap():
    """True when the acquisition cost is inside the statutory acquisition-cost cap."""
    return check_acq_cost_cap_resid() <= val_tol                     # noqa: F821


def check_refund_grid_resid(t):
    """The residual against the **published** 환급률 grid at policy month t; zero at nodes.

    At each duration the 상품요약서 publishes — 1, 3, 5, 10, 15, 20, 30, 40, 50 and 60 years
    [S2] — and while the terminal taper is still 1, the model's :func:`refund_ratio` must
    return the published figure exactly.  It is the one check in this model that ties a
    computed quantity to a number a reader can look up, and it is what catches an
    interpolation that is smooth and wrong.
    """
    nodes = (12, 36, 60, 120, 180, 240, 360, 480, 600, 720)
    if t not in nodes or t >= proj_len():
        return 0.0
    if refund_taper(runoff(t)) < 1.0:
        return 0.0
    return refund_ratio(t) - refund_build(duration_years(t))


def check_refund_grid():
    """True when the 환급률 progression reproduces every published node it reaches."""
    return all(abs(check_refund_grid_resid(t)) <= val_tol            # noqa: F821
               for t in range(0, proj_len()))


def check_equiv_premium_resid():
    """The residual of the equivalence identity; zero.

    ``equiv_premium_mth_pp() x epv_prem_unit_pp() - epv_outgo_pp()``.  It verifies the two
    summations rather than the pricing, and it is a real check on a hundred-year projection:
    the two sides accumulate 1,201 terms each, over quantities that span eight orders of
    magnitude, and a term dropped from either would not otherwise show anywhere.
    """
    return (equiv_premium_mth_pp() * epv_prem_unit_pp()
            - epv_outgo_pp())


def check_equiv_premium():
    """True when the equivalence premium reproduces the discounted outgo it was solved from."""
    tol = val_tol * max(epv_outgo_pp(), 1.0)                         # noqa: F821
    return abs(check_equiv_premium_resid()) <= tol


def check_net_cf_resid(t):
    """The published cash-flow statement's residual in policy month t; zero everywhere.

    :func:`net_cf` less the published ``result_cf()`` columns of the same row.  It closes
    the loop between the total benefit outgo and the eleven kinds that make it up, so a
    twelfth kind added to :func:`claims` and left out of the statement shows up here rather
    than silently vanishing from it.
    """
    return (net_cf(t) - premiums(t)
            + claims(t, "DISABILITY") + claims(t, "DIAGNOSIS")
            + claims(t, "SURGERY") + claims(t, "HOSPITAL")
            + claims(t, "EVENT") + claims(t, "LIABILITY")
            + claims(t, "NEONATAL") + claims(t, "DEATH")
            + claims(t, "LAPSE") + claims(t, "MATURITY") + claims(t, "VOID")
            + claim_expenses(t) + expenses(t) + commissions(t))


def check_net_cf():
    """True when the net cash flow equals the sum of its published columns, every month."""
    tol = val_tol * max(sum_assured("disability"), 1.0)              # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(0, proj_len()))


# --- results ---

def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is the start-of-month count, which is the weight applied to every cash flow
    on the same row.  ``net_cf`` carries the income-positive sign.  ``expenses`` is
    acquisition and maintenance; the claim handling expense is beside it in
    ``claim_expenses``, as in every model in the six libraries.  The benefit outgo is
    published as its eleven kinds and never as a subtotal, so the columns sum to ``net_cf``:
    ``claims_void`` is the pre-birth refund, ``claims_death`` the 계약자적립액 on a death
    the contract does not cover, and ``claims_maturity`` a column of zeros on the shipped
    progression, published rather than dropped because the residual 적립부분 is a real
    quantity on a contract whose term ends earlier.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_disability": [claims(t, "DISABILITY") for t in ts],
            "claims_diagnosis": [claims(t, "DIAGNOSIS") for t in ts],
            "claims_surgery": [claims(t, "SURGERY") for t in ts],
            "claims_hospital": [claims(t, "HOSPITAL") for t in ts],
            "claims_event": [claims(t, "EVENT") for t in ts],
            "claims_liability": [claims(t, "LIABILITY") for t in ts],
            "claims_neonatal": [claims(t, "NEONATAL") for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "claims_void": [claims(t, "VOID") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by policy month t.

    ``pols_pay`` and ``pols_waived`` are the two compartments of ``pols_if``; ``pols_void``
    is the pre-birth decrement, non-zero only on a 태아 model point and only before birth.
    ``age`` is 보험나이 and ``age_man`` 만나이, printed side by side so that the offset a
    foetal contract carries for its whole life can be read off the table.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_pay": [pols_pay(t) for t in ts],
            "pols_waived": [pols_waived(t) for t in ts],
            "pols_void": [pols_void(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "age": [age(t) for t in ts],
            "age_man": [age_man(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "waiver_rate": [waiver_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_val():
    """Result table of the account, the surrender charge and the surrender value, by t.

    ``cv_std_pp`` is the notional 표준형 value and ``cv_pp`` the amount this model point
    actually pays, so the 무해지 cliff at 납입완료 and the value an instant before it can be
    read off the same table.  ``refund_ratio`` is the 환급률 the product is sold on and the
    ratio the supervisor regulates; on the anchor cell it reproduces the published grid at
    every node.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "cum_prem_pp": [cum_prem_pp(t) for t in ts],
            "refund_ratio": [refund_ratio(t) for t in ts],
            "cv_std_pp": [cv_std_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "surr_chg_pp": [surr_chg_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

prem_int_rate = 0.0275

decl_rate = 0.017

min_guar_rate = 0.003

avg_decl_rate = 0.025

ref_age = 40

ref_sex = "M"

surr_chg_prem_rate = 0.05

surr_chg_sa_rate = 0.01

surr_chg_cap_months = 13.0

surr_chg_max_coef = 20

surr_chg_max_years = 7

acq_cost_ratio = 0.9

comm_init_share = 0.65

comm_renewal_rate = 0.03

expense_maint_pp = 400.0

expense_maint_prem_rate = 0.05

expense_claim_pp = 30000.0

inflation_rate = 0.02

liability_cycle_mths = 36

roll_fwd_tol = 1e-10

val_tol = 1e-07

pd = ("Module", "pandas")
