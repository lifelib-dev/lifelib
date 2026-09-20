# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Korean children's insurance.

:mod:`~.Child_KR_S` is the executable counterpart of
``products/child/technical-notes.md`` in the ``krlib`` library. It projects gross
best-estimate liability cash flows for a single-policy model point of 어린이보험
(*eorini boheom*), the fixed-benefit (정액) 제3보험 contract of 보험업법
제4조제1항제3호 written on a child — very often **before the child is born** — and
running from birth to a 100세 만기: office premiums on three streams, a 상해후유장해
기본계약 paying 보험가입금액 × 장해지급률, a bundled 특별약관 stack of diagnosis,
surgery, hospital-cash, fracture, burn and third-party-liability limbs, a 태아 module
with two terms of its own, two premium waivers on two different lives, the 계약자적립액
paid on a death the contract does not cover, the 해약환급금 of the 표준형 and of the two
suppressed forms, maintenance and claim expenses, and commission.

.. rubric:: The deltas against ``Cancer_KR_S``, and the two that are new

``Cancer_KR_S`` is this library's fixed-benefit 제3보험 chassis: a diagnosis-triggered
lump sum on a tier ladder, a 90-day 면책기간, a 감액기간, a 유사암 reduced tier, a
premium waiver correlated with the diagnosis, and no death benefit. ``Child_KR_S``
inherits all six and changes six things, three of which have no counterpart anywhere in
this repository.

**태아가입 — the contract is written before the insured exists.** A 태아 has no legal
personality and cannot be the 피보험자 of an 인보험 contract, so the 태아가입특칙 makes
the foetus the insured **at birth**. The projection opens on a life that does not yet
exist: months ``t = 0`` to ``t = birth_month() - 1`` carry premium income on three
streams, a **void** decrement rather than a mortality one — 유산 or 사산 makes the
contract 무효 and every premium is returned — and the pre-birth limbs of the 태아 module,
and **no mortality and no morbidity on the insured at all**. ``Projection.born``
gates every cover on the child's own life and ``Projection.check_cover_at_birth``
asserts the gate.

**보험료 납입면제 on the 계약자 — a premium-waiver decrement on a life who is not the
insured.** The waiver fires on the child's own trigger set **or on the policyholder's
death or 50% 이상 장해**, so the model carries **two decrement lives** and the premium
stream stops on the earlier of two events drawn from two different rows of the mortality
table.

**Both of the chassis's anti-selection devices are switched off.** The 90-day 면책기간
is disapplied below 보험나이 15 and entirely on a 태아 cover, and the 감액기간 was
removed from foetal contracts by supervisory recommendation. The test is applied **at
the 계약일 and not at the claim date**, so a contract issued at 계약나이 0 has no cancer
waiting period at any point in its hundred-year life.

The horizon is the other structural fact. At 계약나이 0 to a 100세 만기 the projection
runs **1,200 monthly periods** — ``t = 0`` to ``t = 1,199``, plus the terminal 계약해당일
row at ``t = 1,200`` — the longest in ``krlib``, and the premium is paid over
the first 240 of them, so eighty of the hundred years are paid-up, and what happens in
them decides the contract.

**Spaces.** The model contains two:

:mod:`~.Child_KR_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Child_KR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Child_KR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Monthly steps. The contract's own clock is **보험나이** (*boheom
nai*, insurance age), which is what ``age(t)`` returns; the decrement tables are read at
**만나이** (*man nai*, age last birthday) through ``age_man(t)``, and on a 태아 contract
the offset between the two is the exact pre-birth period rather than an average. ``t``
is the policy month and is **0-based**: ``t = 0`` is the first projected month, month
``t`` runs from ``t`` to ``t + 1`` months after the 계약일, the policy year containing it
is ``t // 12 + 1``, and ``proj_len()`` is the **number** of projected months, so the frame
is ``t = 0 … proj_len() - 1`` and its last index is the 계약해당일 on which the contract
expires. Office premium
falls at the start of the month; benefits, the 계약자적립액 on death, the 해약환급금 on
lapse, the premium refund on a pre-birth void and the claim-handling expense at the end.
Within the month the order is **void, then the waiver, then mortality, then lapse**.
Acquisition expense and initial commission fall at ``t = 0``.

**What is sourced and what is not.** The contractual mechanics are sourced almost
throughout: the 태아가입특칙 verbatim, the two ages a foetal contract carries, the
under-15 disapplication of the 면책기간, the removal of the 감액 from foetal contracts,
the statutory bar on a death benefit below 만 15세 and the 계약자적립액 paid instead, the
two waivers with the P코드 carve-out, the 3년만기 갱신형 liability block, the published
해약환급금 grid and the 무해지 cliff. **Almost everything quantitative is a
standardization.** Nothing on Korean child incidence — cancer, cerebrovascular disease,
congenital anomaly, low birth weight, NICU admission — was retrieved from 보험개발원,
국가암정보센터 or 통계청, and the 경험생명표 is published only as summary statistics, so
the mortality table is a [std] construction and **every incidence assumption in this
model is a [std] construction and says so at the point of use**. The single exception is
the one 적용위험률 published anywhere in the research file — 일반상해 후유장해
발생률(3~100%) at 5세, 상해 1급 — which is the calibration point of the basic contract's
decrement. **This model is a mechanics demonstration, not a pricing or reserving
result.** Replace the assumption tables with company data before drawing any conclusion
from the output.

**Model points.** Ten, covering both sexes, 태아가입 and issue 보험나이 0, 5, 15 and 30,
100세 and 110세 and 30세 만기, 20년납 and 30년납, all three surrender-value forms, the
태아 module on and off, both waiver modules on and off, the 면책기간 and 감액기간
switches, the broad adult-disease definitions, the 2026 저출산 premium discount and the
three lapse bases. Model point 1 is the anchor cell of the worked example in the
technical notes: a 태아 contract, priced male, with birth at policy month 5.

**Verification.** ``tests/test_child_kr.py`` asserts the notes' worked example and its
first-year aggregate, the roll-forward and waiver-split identities, the pre-birth gate,
the once-only benefit ledgers, the 태아 module's own two terms and the surrender-value
grid.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/child/Child_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Child_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
