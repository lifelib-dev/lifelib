# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Korean level term life insurance.

:mod:`~.Term_KR_S` is the executable counterpart of
``products/term_life/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single-policy model point of 정기보험
(*jeonggi boheom*, level term life) in the composite the product specification builds:
개인, 무배당, 순수보장형, **해약환급금 미지급형** (무해지환급형), written 비갱신형 on a
전기납 basis, with 갱신형 as a first-class variant [S1] [S2] [S12] [S4].

This is the library's **protection chassis**. The decrement recursion, the premium
recursion and the 갱신형 / 비갱신형 split specified here are inherited by ``CI_KR_S``
(CI보험) and ``Cancer_KR_S`` (암보험) rather than restated. The savings machinery it
deliberately does not carry — the 계약자적립액 as a projected quantity, the 표준형
해약환급금 curve, the 보험계약대출 — belongs to ``WholeLife_KR_S``, the savings chassis.

Three mechanics drive the shape of the answer and none of them has a counterpart in this
repository's U.S. or UK term models.

**갱신형 (*gaengsinhyeong*, renewable) repricing.** A Korean renewal happens **without
fresh 고지 and without underwriting**, on the rate scale then in force, at attained
보험나이, on a new product code [S6] [S9] [S15]. So the premium is a function of the
**renewal index** and not of the policy year, and the horizon of the cash flows the
contract generates is the **renewal ceiling** — 보험나이 80 on the composite — and not
the 보험기간 of the contract in force, which is one cycle. On the anchor renewable cell
the published premium path is 9,000 -> 21,000 -> 56,000 -> 201,000 won a month, an index
of 1.00 / 2.33 / 6.22 / 22.33 [S7].

**The contract boundary, published both ways.** Nothing retrieved settles where a Korean
term renewal's IFRS 17 boundary falls [REG-R60], so the model does not rule. It
implements the **long reading** — the boundary at the ceiling — as its base, because that
is the reading that needs the machinery, and carries the short reading as
``contract_boundary = current_term``. Model points 3 and 4 are the same cell on the two
readings.

**The renewal decline is its own decrement.** At each renewal date a fraction of the
surviving in-force leaves rather than accept the repriced contract. It is discrete,
concentrated on one date and driven by the size of the repricing step, where ordinary
lapse is continuous; and it is applied **after** mortality and **after** ordinary lapse,
on the survivors of both. Folding it into the lapse rate hides the boundary and applies
it to lives that died or lapsed during the boundary month.

**Spaces.** The model contains two:

:mod:`~.Term_KR_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Term_KR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Term_KR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps, which is the step the contract is actually paid on:
월납 is the only premium mode on seven of the retrieved products and the disclosure's own
basis [S5], and the rate card is quoted per month [S12]. The time index ``t`` is
**0-based**, so ``t = 0`` is the first policy month, period ``t`` runs from time ``t`` to
time ``t + 1``, the contractual policy year is the derived 1-based label
``policy_year(t) = t // 12 + 1`` and is never indexed by, and ``proj_len()`` is the number
of projected months — ``12 x proj_years()``, so the frame is ``t = 0, 1, ...,
proj_len() - 1`` and a 20년만기 contract projects 240 rows.
Premiums and maintenance expense fall at the start of the month; acquisition expense and
initial commission at issue, which is the start of month ``t = 0``; death claims and
their claim expense at the end of the month;
ordinary lapse at the end of the month after deaths; the renewal decline at the end of the
**last month of a cycle** after ordinary lapse; the 만기보험금 of the 만기환급형 variant at
the end of the final month ``t = proj_len() - 1``. The age basis is **보험나이**, which
increments on the 계약해당일 and not on the birthday [S2 제22조], so the attained age is
``age_at_entry() + t // 12`` and the step is exact rather than an approximation of one.

The decrement basis stays annual and is converted: every Korean 예정 경험사망률 disclosure
and the supervisor's own 적용해지율 vector are published as annual rates by age and by
경과기간 [S12] [REG-R27], so ``mort_rate`` and ``lapse_rate`` carry the sourced annual
quantity and ``mort_rate_mth`` and ``lapse_rate_mth`` — ``1 - (1 - q)^(1/12)`` **[std]** —
are what the roll-forward applies. The premium, by contrast, needs no conversion at all:
``premium_mth_pp`` is the published monthly office premium and is now the month's cash
flow, so the annual grid's ``P_a = 12 P_m`` annualization survives only as a reporting
quantity and as the base of the commission scale.

**No surrender value, anywhere.** The representative form is 해약환급금 미지급형 on a
전기납 contract, and the 약관 pays nothing at any duration [S1] [S2 제33조제2항] [S12], so
an ordinary lapse is a pure decrement: it moves the in-force count and pays nothing.
``claims(t, "LAPSE")`` exists and returns zero so that the zero is stated rather than
inferred. There is likewise no 보험계약대출 and no 자동대출납입 in fact [S2 제34조]
[REG-R28], and no 감액완납 and no 연장정기 in any retrieved Korean document.

**What is sourced and what is not.** The contractual mechanics are sourced: attained-age
repricing at 갱신 and its absence of 고지, truncation of the final cycle at the ceiling,
the premium waiver not surviving a renewal, the nil surrender value, the acceleration
rider's 50% / 50,000,000-won cap, and the 부활 window. **The premiums are sourced too** —
15,080 won a month at the anchor cell, published twice independently [S12] [S4], and the
whole renewal ladder [S7] — which no other library in this repository can say of its
protection chassis. Everything else is a standardization: the mortality table's shape
beyond the three disclosed ages, the best-estimate mortality factor, the best-estimate
lapse level, the renewal-decline rate, the shortened-pay premium equivalence, and the
expense and commission levels. **This model is a mechanics demonstration, not a pricing
or reserving result.** Replace the assumption tables with company data before drawing any
conclusion from the output.

**The mortality table shipped here is a construction, not a published table.** The
industry table — the 제10회 경험생명표 (*gyeongheom saengmyeongpyo*), applied from April
2024 — is **not published**: only 평균수명 and 65세 기대여명 are released [REG-R33]
[REG-R34]. ``mort_table.csv`` is therefore a **[std]** Makeham fit through one carrier's
three disclosed 예정 경험사망률 [S12], tilted above age 60 so that the table reproduces
the published 65세 기대여명 exactly. See :mod:`~.Term_KR_S.Data`.

**Model points.** Ten, covering both sexes, both renewal structures, both contract
boundaries, the 순수보장형 and 만기환급형 maturity forms, 전기납 and shortened pay,
년만기 and 세만기 terms, all four rate classes, the issue-age envelope from 19 to 65 and
the sum-assured envelope from 30,000,000 to 500,000,000 won, and every optional module.
Model point 1 is the anchor cell of the worked example in the technical notes, and is the
cell that is doubly prescribed in Korea — the 감독규정 기준연령 요건 [REG-R9] and the
disclosure's 대표계약 [S5].

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/term_life/Term_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Term_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
