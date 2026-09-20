# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Korean indemnity medical insurance.

:mod:`~.Medical_KR_S` is the executable counterpart of
``products/indemnity_medical/technical-notes.md``. It projects gross best-estimate
liability cash flows for a single-policy model point of 4세대 실손의료보험
(*silson uiryo boheom*, fourth-generation indemnity medical insurance): office
premiums on the two separately re-rated priced units, the 급여 (*geubyeo*, covered by
National Health Insurance) reimbursement of the main contract, the 비급여
(*bigeubyeo*, non-covered) reimbursement of the rider, the three sub-limited
3대비급여 classes, maintenance and claim-handling expense, and commission.

**This product stands alone in ``krlib``.** It inherits nothing from
``WholeLife_KR_S``, ``Term_KR_S`` or ``Cancer_KR_S``, and nothing states a delta
against it. The reason is structural: it is the only contract in this repository
whose benefit is a **reimbursement of an incurred cost** — the 실손해 (*silsonhae*,
actual loss) branch of 보험업감독규정 제7-63조 — rather than a stated sum. There is no
보험가입금액 that determines a claim here, only an annual limit that caps one.

.. rubric:: What makes this product a different shape

A death-benefit model prices a **sum assured**. A fixed-benefit health model prices
**frequency x severity x day limit**. This one prices
**frequency x severity x a stack of co-payment percentages, per-visit deductibles,
per-act money and count caps and an annual aggregate** — and then feeds the resulting
claim back into next year's premium. Four consequences run through the whole model and
none of them has an analogue anywhere else in the library:

* **the 급여 / 비급여 split is two priced units, not one product.** The main contract
  retains 20% of the covered loss and the rider 30%; the two are re-rated separately at
  each renewal, and only the rider carries the experience relativity;
* **the 비급여 할인·할증 is a feedback loop from claims to premium.** The renewal
  premium of the rider is a function of the policyholder's own prior-year non-covered
  claim amount, through a five-band 요율 상대도 whose band-1 discount is **solved** from
  a revenue-neutrality constraint rather than fixed — so a change in the band
  distribution propagates correctly instead of silently breaking neutrality;
* **the contract is one year long and renews annually** at the attained age and the
  then-current basis, inside a supervisory corridor of plus or minus 25% per
  위험구분단위 applied to the **age-adjusted** prior premium; and it **re-enters** the
  then-current generation every five years, which is what fixes the projection horizon;
* **the public scheme truncates half the claim.** The 본인부담상한제 refunds a member's
  annual statutory co-payment above an income-graded ceiling, and the 표준약관 excludes
  the refundable amount from cover outright, so the 급여 half of the claim is bounded
  above and bounded differently by income decile. The 비급여 half is not bounded at all.

.. rubric:: Spaces

The model contains two:

:mod:`~.Medical_KR_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Medical_KR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the technical notes' worked-example anchor
    cell. It reaches the input tables through its ``data`` Reference, which resolves to
    the single :mod:`~.Medical_KR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

.. rubric:: Projection basis

Monthly steps, because the product is: 월납 is the only premium mode retrieved and the
whole published premium series is monthly. ``t`` is the policy month, 0-based:
``t = 0, 1, ..., proj_len() - 1``, and ``proj_len()`` is the **number** of projected
months — the exclusive end of the frame, so ``result_cf()`` has ``proj_len()`` rows.
The policy year ``policy_year(t) = t // 12 + 1`` is a contractual 1-based label derived
from ``t``.
Premium falls at the start of month ``t``; claims and expenses at the end; mortality,
then lapse, then suspension at the end of every month, and the renewal decline at the
end of the twelfth month of each policy year, in that order.

The contract's own mechanics are annual, so every benefit and premium quantity is
computed **per policy year** and spread evenly across the twelve months of that year.
The 연간 clock is the policy year, 「계약일로부터 매1년 단위로 도래하는 계약해당일
전일까지의 기간」, and every limit resets on it.

The horizon is two five-year 보장내용 변경주기 — ten policy years — or the run to
the maximum cover age if that comes first. It is a **stated** horizon rather than a
contractual one: a 4세대 contract has a contractual life of five years in its own form,
after which it re-enters whatever generation is then on sale, so no projection of this
contract past the first 재가입 is a projection of *this* contract's terms. The model
assumes re-entry on unchanged terms and says so rather than pretending the question
does not arise.

.. rubric:: What is sourced and what is not

Every **contractual** parameter is sourced, and to a precision no other product in this
repository reaches, because the benefit definition of a Korean 실손 contract is not
written by the carrier: it is the 표준약관 annexed to the 보험업감독업무시행세칙 at
별표 15, made under 제5-13조제1항. The co-payment percentages, the 통원 공제금액, the
₩2,000,000 annual inpatient co-payment cap, the ₩50,000,000 annual limits, the
₩200,000 per-visit cap, the 100-visit count, the three 3대비급여 sub-limits and their
shared 50-act counter, the 10-visit re-assessment rule, the five 요율 상대도 bands and
their ₩1,000,000 surcharge floor, the plus or minus 25% renewal corridor and the
five-year 재가입 cycle are all clause references.

Everything **quantitative** is a standardization. 보험개발원 is the statutory rate
bureau, and its published 장기손해보험 참조순보험요율 does not cover 실손의료보험 at
all; the 산출방법서, where the 예정위험률 and 예정사업비율 live, is a 기초서류 that is
filed and never published. There is consequently **no public Korean indemnity-medical
morbidity or severity basis**, and every frequency, severity, expense and persistency
parameter here is [std], constructed from the aggregate experience the supervisor does
publish and calibrated so that the anchor cell's first-year claim reproduces the
published 4세대 loss ratios on the published 2021 premium anchor. And no Korean
mortality table is published in full — 제10회 경험생명표 releases only summary
statistics — so ``mort_table.csv`` is a [std] Makeham construction on the 국가데이터처
완전생명표 summary rather than a transcription. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the assumption tables with
company data before drawing any conclusion from the output.

.. rubric:: Model points

Ten, covering both sexes, the 0-65 issue-age envelope, both 보험가입금액 rungs, the
급여-only election, the 3대비급여-off election, the experience relativity on and off,
the 무사고 할인 on and off, the 개인실손 중지 decrement, a high-utilisation cell on the
lowest 본인부담상한액 decile where the public truncation binds, the branch where
국민건강보험 entitlement does not apply and reimbursement falls to 40%, and a cell whose
claim trend runs the renewal corridor into its clip. Model point 1 is the anchor cell of
the worked example in the technical notes and reproduces it to the precision the notes
display.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/indemnity_medical/Medical_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Medical_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
