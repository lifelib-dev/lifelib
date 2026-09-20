# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Korean cancer insurance (암보험).

:mod:`~.Cancer_KR_S` is the executable counterpart of
``products/cancer/technical-notes.md`` in the lifelib-products library. It projects gross
best-estimate liability cash flows for a single-policy model point of 암보험 (*am boheom*)
in the composite the product specification builds: 개인, 무배당, **정액** (fixed-benefit)
제3보험 -- 질병보험 under 보험업법 제4조제1항제3호 -- written 비갱신형 to the 100세
계약해당일 on a 20년납 basis, on the **해약환급금 미지급형** form, paying a four-tier
diagnosis benefit with 암 입원급여금, 암 수술급여금 and 항암약물.방사선 치료급여금 attached
as independently switchable modules, with the premium waived from the first invasive
diagnosis and the 계약자적립액 payable on death.

This is the library's **fixed-benefit 제3보험 chassis**. Five mechanics are specified here
once and inherited rather than restated by ``LTC_KR_S`` (간병보험) and ``Child_KR_S``
(어린이보험): the diagnosis-triggered lump sum graded by a tier ladder keyed to a public
statistical classification; the **90일 면책기간** before invasive cover attaches; the
**감액기간**, a stated fraction of the benefit for the first one or two years; the **유사암**
reduced tier; and a **post-diagnosis survival model**. The indemnity machinery it
deliberately does not carry -- the 급여/비급여 split, 자기부담금, annual limits, 재가입 --
belongs to ``Medical_KR_S``, which is the library's only indemnity product.

Four mechanics drive the shape of the answer.

**The benefit vector has two start dates, not one.** Cover for an invasive cancer attaches
on the 암보장개시일, the 91st day counting the 보험계약일 as day 1, which on a monthly grid
is ``t = 3`` [S1] [S2] [S3] [S4] [S7]. The 유사암 tier has **no waiting period at all** --
「유사암의 보장개시일은 계약일임」 [S1] -- so it is in force from ``t = 0``. A model with one
waiting period gets one of the two tiers wrong for a quarter of a year, and the tier it gets
wrong is the one whose incidence at young ages exceeds the invasive rate.

**The premium waiver is a correlated decrement.** It fires on the *same event* that pays the
일반암 or 고액암 diagnosis benefit and then runs for as long as the insured survives inside
the 납입기간; 특정소액암 and every 유사암 member are expressly excluded [S3 제14조제1항]
[S1 제9조제1항]. So premium income rides on the never-invasively-diagnosed population plus
the 특정소액암 sub-population, and the benefit outgo rides on the diagnosed one; the two
weights are disjoint by construction, and multiplying the premium by ``pols_if`` is the
single largest arithmetic error available in this product.

**The contract goes on paying after the diagnosis benefit, so an incidence rate cannot price
it.** The inpatient, surgery and anti-cancer treatment limbs are incurred over the months and
years following diagnosis and the waiver runs to 납입완료 or death, so all four depend on
**how long the insured lives after diagnosis**. The model therefore carries a diagnosed state
resolved into **six select-duration cohorts** and a post-diagnosis excess hazard graded across
five select years, calibrated to Korea's published 5년 상대생존율.

**Paying a benefit neither terminates nor exhausts the contract.** Cover for the other tiers,
for the event modules and for the waiver runs on to the 100세 계약해당일 [S1] [S3] [S4], and
nothing is paid at expiry. That is the sharpest structural contrast with the accelerated
design of ``CI_KR_S``, where the critical-illness payment reduces the death benefit carrying
it.

**Spaces.** The model contains two:

:mod:`~.Cancer_KR_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no parameters,
    so each file is read **once per model**.

:mod:`~.Cancer_KR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Cancer_KR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however many
policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model and
its inputs must travel together.

**Projection basis.** Monthly steps, and monthly by construction rather than by
approximation: 월납 is the dominant retail mode and the mode named in the 감독규정's own
기준연령 요건 [REG-R9], the 90-day 면책기간 lands on the grid boundary ``t = 3`` and the
one-year 감액기간 on ``t = 12``. ``t`` is the policy month, 0-based:
``t = 0, 1, ..., proj_len() - 1``, and ``proj_len() = 12 x (100 - issue_age) + 1`` is the
**number** of projected months, the frame's exclusive end -- 721 on the anchor cell, so the
last projected month is ``t = 720``, the 100세 계약해당일, at which the contract expires and
nothing is paid. Policy year is the contractual label ``t // 12 + 1``.
Premium and maintenance expense fall at the start of month ``t``; diagnoses and every benefit
at the end; decrements at the end, the transition out of the healthy state first, then
mortality, then lapse. Acquisition expense and initial commission fall at ``t = 0``. The age
basis is **만나이**.

**What is sourced and what is not.** The contractual mechanics are sourced: the 90-day
면책기간 and the 유사암 carve-out from it, the one-year 50% 감액기간 measured from the
보험계약일 to the 진단확정일, the 200 / 100 / 60 / 20 tier ladder, the 최초 1회한 form of
every diagnosis benefit, the 고액암 tier adding to rather than replacing the general one, the
waiver's exclusion of 특정소액암 and 유사암, the absence of a death benefit and the payment of
the 계약자적립액 on death, and the nil surrender value of the 미지급형 form during the
납입기간. **The incidence basis is sourced too**, which no other morbidity model in this
library can say: 보험개발원 publishes a 「기타피부암 및 갑상선암 이외의 암 발생률」 grid by
age and sex on the insured definition [R5] [REG-R61]. What is standardized is the tier
decomposition of that grid, the post-diagnosis excess hazard, every care intensity, the lapse
level, the expense and commission scales, and the premium. **The mortality table shipped here
is a construction, not a published table**: the 제10회 경험생명표 is not published in full
[REG-R33] [REG-R34], so ``mort_table.csv`` is a Makeham fitted to the 국가데이터처 생명표's
published 기대여명 [REG-R38]. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the assumption tables with company data before drawing any
conclusion from the output.

**Model points.** Ten, covering both sexes, the 15-to-65 issue-age envelope, the
10,000,000-to-100,000,000-won sum-insured envelope, 10 / 20 / 30년납 and 전기납, the 비갱신형
and 10년 갱신형 chassis, the 0 / 12 / 24-month 감액기간, the 20% and pre-2022 70% 유사암
ratios, the 미지급형 and 표준형 surrender bases, the presence and absence of the premium
waiver, and every benefit module on and off -- including the diagnosis-only shape of [S3]
[S6] [S7] and the treatment-cost-only shape of [S5], which are configurations of one model
rather than different models. Model point 1 is the anchor cell of the worked example in the
technical notes, and is the cell Korean regulation itself computes at: 「남자가 만 40세에
보험에 가입하는 경우」, the 기준연령 요건 of 감독규정 제1-2조제2호 [REG-R9].

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/cancer/Cancer_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Cancer_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
