# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Korean whole life assurance (종신보험).

:mod:`~.WholeLife_KR_S` is the executable counterpart of
``products/whole_life/technical-notes.md`` in the ``krlib`` library. It projects gross
best-estimate liability cash flows for a single-policy model point of the standardized
composite 종신보험 (*jongsin boheom*) — a level premium payable for a stated 납입기간, a
사망보험금 level for life, no expiry date and no 만기보험금, and therefore a 계약자적립액
and a 해약환급금 that carry the whole economics of the product.

This is the library's **savings/protection chassis**. Five mechanics are specified once
here and inherited by ``CI_KR_S`` and ``Pension_KR_S``:

* the 계약자적립액 (*gyeyakja jeongnibaek*, the policyholder account) recursion, the
  contractual successor of the 보험료적립금 policy reserve;
* the 해약환급금 (*haeyak hwangeupgeum*, surrender value) and its 해약공제액, capped by
  the 표준해약공제액 of 보험업감독규정 별표 14;
* the **무해지환급형 / 저해지환급형** suppressed forms — the surrender value is a stated
  fraction ``k`` of the 표준형 twin's during 납입기간 and steps up to it at 납입완료. The
  suppression is a **model point column**, not a separate model, so the cliff and the
  ordinary curve appear side by side in one projection;
* the 보험계약대출 (policy loan) as a modelled state, unavailable during 납입기간 on a
  무해지환급형 contract because there is no value to lend against; and
* 보험료 납입면제 (premium waiver), a distinct in-force state in which premiums cease and
  are **deemed paid** for benefit and surrender-value purposes.

Three structural facts separate this model from its Japanese sister. There is **no
automatic premium loan**: no 자동대출납입 provision was found in any Korean document read
for this library, so lapse here is a behavioural decrement acting at the end of a 14-day
납입최고기간 rather than a funded event. There is **no severe-disability acceleration**;
the slot Japanese whole life fills with a 高度障害保険金 is filled in Korea by the premium
waiver, which continues the contract instead of extinguishing it. And there is **no
expiry**: the projection runs to the terminal age of the mortality table, every remaining
life dies in the last projected period, and nothing is paid at the horizon but the death
benefit.

**Spaces.** The model contains two:

:mod:`~.WholeLife_KR_S.Data`
    Reads the three input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.WholeLife_KR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the technical notes' worked-example anchor cell.
    It reaches the input tables through its ``data`` Reference, which resolves to the
    single :mod:`~.WholeLife_KR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps, on **보험나이** (*boheom nai*, insurance age). The
time index ``t`` is **0-based** and counts policy months: ``t = 0`` is the first policy
month, period ``t`` runs from month-end ``t`` to month-end ``t + 1``, the frame is
``range(proj_len())`` with ``proj_len() = 12 x proj_years()``, and the contractual policy
year is the derived 1-based label ``policy_year(t) = t // 12 + 1``. Contract terms stay in
years — the 납입기간, the 해약공제기간, the 보험계약대출 drawdown year and the 감액 year are
all annual quantities with month-count companions where the grid needs one. Values *at* a
point in time — the 계약자적립액, the 해약공제액, the two surrender values, cumulative
premiums and the 보험계약대출 balance — carry a second index, the month-end
``d = 0 … proj_len()`` with ``d = 0`` at issue, and the flows of month ``t`` read ``d = t``
as the opening month-end and ``d = t + 1`` as the closing one; a 계약해당일 is the month-end
``d = 12y``, which is where the published 해약환급금 grids are quoted. Premium, maintenance
expense and renewal commission fall at the start of the month; acquisition expense and
initial commission at issue, in month ``t = 0``; death claims at the end of the month of
death; surrenders and any 감액 at the end of the month, after deaths, on the value at the
month-end that closes it.

**What the monthly grid moved.** The sourced decrement basis stays annual — both disclosed
적용위험률 grids are annual by age and the FSS 원칙모형 lapse vector is annual by 경과기간 —
and ``mort_rate_mth`` and ``lapse_rate_mth`` are its ``1 - (1 - q)^(1/12)`` conversions, so
twelve monthly exits compound back to the year's rate exactly and **the in-force at every
계약해당일 is unchanged** from the annual-step model this replaced. The **계약자적립액 does
move, by about 1.2%**, and that is the conversion's substantive gain: 감독규정
제7-66조제1항제4호 provides that the account accrues **monthly** before 납입완료 and daily
afterwards, and an annual grid could carry this product only through 제7-65조제2항's separate
permission to compute it 「연납보험료를 기준으로 하여 산출할 수 있다」 — a permission the
model used to take and record as a [std] departure. The monthly grid does not need it: the
account accrues at ``(1 + i)^(1/12) - 1`` a month and is built from a **월납순보험료** struck
by monthly equivalence, which is not the 연납순보험료 divided by twelve. The 연납순보험료
survives beside it because 별표 14 names that quantity and the statutory 표준해약공제액 is
computed from it.

**What is sourced and what is not.** The contractual mechanics are sourced: the level
whole-of-life benefit, the identity 해약환급금 = 계약자적립액 − 해약공제액, the
표준해약공제액 formula and the seven-year 해약공제기간 cap, the fact that the suppression
multiplies a **표준형 comparison twin priced with the lapse assumption switched off** and
is not sold, the equality of the suppressed and 표준형 values from 납입완료, the policy
loan rate formula 예정이율 + 1.5% and the 50%-장해지급률 waiver with premiums deemed paid.
The quantitative basis is not. The 예정이율, the 적용위험률 and the 예정사업비율 live in
the filed but unpublished 산출방법서, and the 제10회 경험생명표 is not published in full,
so the mortality table is a **[std]** construction and every expense parameter is a
**[std]** standardization bounded above by the 표준해약공제액. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the assumption tables with
company data, and the account recursion with a real 산출방법서, before drawing any
conclusion from the output.

**What it does not compute.** No 책임준비금, no IFRS 17 CSM, no K-ICS 요구자본 and no
해약환급금준비금. ``result_cf()`` is a gross, undiscounted best-estimate stream and the
three Korean measurement bases that consume it are a separate layer.

**Model points.** Ten, covering both sexes, the issue-age envelope 30 to 65, sum assureds
from ₩10,000,000 to ₩1,000,000,000, the four suppression factors 1.00 / 0.50 / 0.30 /
0.00, payment terms of 7, 10, 20 and 30 years and 전기납, and each optional module: the
policy loan on a 저해지 and on a 무해지 contract, the premium waiver, the 단기납
유지보너스 with its mandatory lapse spike, the 금리연동형 crediting basis, 감액, 부활 and
the level lapse basis. Model point 1 is the anchor cell of the worked example in the
technical notes.

**Verification.** ``tests/test_whole_life_kr.py`` asserts the notes' worked example, the
exact ``1 / k`` step at 납입완료, the nil surrender value of the 무해지 form throughout
납입기간, the zero policy loan that follows from it, and every ``check_*`` identity on
every shipped model point.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/whole_life/WholeLife_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "WholeLife_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
