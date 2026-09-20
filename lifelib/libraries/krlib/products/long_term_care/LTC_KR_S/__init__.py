# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Korean long-term-care insurance.

:mod:`~.LTC_KR_S` is the executable counterpart of
``products/long_term_care/technical-notes.md`` in the ``krlib`` library. It projects
gross best-estimate liability cash flows for a single-policy model point of 간병보험
(*ganbyeong boheom*), the 제3보험 contract of 보험업법 제4조제1항제3호 whose trigger is
the **public** scheme's own 장기요양등급 under the 노인장기요양보험법: office premiums,
a 장기요양진단급여금 (lump sum) on the first award of a grade at or above the contractual
threshold, a 간병연금 (care annuity) metered by an annual survival test with a twelve-month
guarantee and a 120-month cap, the 납입면제 (premium waiver) firing on that same award,
the 계약자적립액 paid on death from a cause the contract does not cover, the 해약환급금 of
the 해약환급금 미지급형 form, an optional 치매진단급여금 rider, maintenance and claim
expenses, and commission.

**The delta against ``Cancer_KR_S``, the fixed-benefit (정액) 제3보험 chassis, is the
trigger and with it the shape of the liability.** Cancer cover pays on a pathological
event with a date. Long-term-care cover pays on an **administrative determination of a
state**: a 등급판정위원회 sitting inside 국민건강보험공단 awards a grade, the insured then
*lives* in that state drawing an annuity, having stopped paying premiums, and dying at a
rate well above that of a healthy life of the same age. ``LTC_KR_S`` is therefore a
**three-state model** — healthy, in long-term care, dead — with the care state absorbing
and carrying its own mortality basis, and with a fourth compartment inside it: the light
grades (3~5등급 and 인지지원등급) that sit *below* the contractual threshold, from which
most severe-grade lives arrive. ``Cancer_KR_S`` needs no such basis, and it reads an
**incidence** straight off 보험개발원's published 장기손해보험 참조순보험요율 display, whose
「기타피부암 및 갑상선암 이외의 암 발생률」 grid is stated on the insured definition. Nothing
on that display reaches this trigger.

**The basis is a prevalence, and converting it is the modelling work.** The one large
public dataset — the 국민건강보험공단 노인장기요양보험 통계연보 연령별 인정률 — counts
people *holding* a certification, not people entering one. The conversion is done in
:mod:`~.LTC_KR_S.Projection`, in the open, by a compartment identity that carries the
care state's own mortality in it; it is not an assumed incidence rate.

**Spaces.** The model contains two:

:mod:`~.LTC_KR_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.LTC_KR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.LTC_KR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps on **만나이** (*man nai*, age last birthday).  ``t``
is the policy month, 0-based: month ``t`` runs from ``t`` to ``t + 1`` months after the
계약일, so ``t = 0`` is the first projected month. ``proj_len()`` is the **number** of
projected months — the frame's exclusive end, ``range(proj_len())`` — so the last row is
``t = proj_len() - 1``, the 계약해당일 on which the contract matures, carrying the
surviving in-force count and no cash flow. Office premium and maintenance expense fall at
the start of the month; the lump sum, the annuity instalment, the 계약자적립액 on death, the
해약환급금 on lapse and the claim-handling expense at the end. Within the month the order
is **certification, then mortality, then lapse** — lapse is taken from the survivors of
the month's mortality, and the care population is exposed to neither lapse nor premium.
Acquisition expense and initial commission fall at ``t = 0``.

**What is sourced and what is not.** The contractual mechanics are sourced: the
grade-only trigger with no company-basis limb, the 최초 1회한 lump sum that extinguishes
its own benefit line without terminating the contract, the survival-tested annuity with
its twelve-month guarantee and 120-month cap, the amount and the 감액 both frozen at first
certification, the waiver firing on the same event as the benefit, the bar on surrender
once the annuity has started, the nil 해약환급금 during the premium-paying period and the
50% of a notional 기본형 after it, and the statutory 계약자적립액 on non-covered death.
Almost everything quantitative is a standardization. **보험개발원 publishes neither a
장기요양 incidence table nor a post-onset mortality table, and the 경험생명표 is not
published in full**, so the mortality table shipped here is a [std] construction anchored
on published summary 기대여명 and the morbidity basis is built in public from the
certification statistics and calibrated against the one disclosed 예정위험률.  **This
model is a mechanics demonstration, not a pricing or reserving result.** Replace the
assumption tables with company data before drawing any conclusion from the output.

**Model points.** Nine, covering both sexes, issue ages 30 to 70, all six contractual
thresholds from 1등급 to 1~인지지원등급, 90 / 95 / 100세만기, 10 / 20 / 30년납, the three
surrender-value forms, the 간병연금 on and off, the 치매진단급여금 rider on and off, the
간편심사 premium loading, the 우체국 180-day waiting period with its two-year 감액, and the
표준형 lapse comparison vector. Model point 1 is the anchor cell of the worked example in
the technical notes.

**Verification.** ``tests/test_long_term_care_kr.py`` asserts the notes' worked example
and its policy-year-1 aggregate, the roll-forward and nesting identities, the annuity
ledger and the surrender-value cliff.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/long_term_care/LTC_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "LTC_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
