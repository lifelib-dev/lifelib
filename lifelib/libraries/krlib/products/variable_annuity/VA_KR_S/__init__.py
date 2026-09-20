# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for a Korean variable annuity (변액연금보험).

:mod:`~.VA_KR_S` is the executable counterpart of
``products/variable_annuity/technical-notes.md`` in ``krlib``. It projects gross
liability cash flows for a single-contract model point of an individual deferred
변액연금보험 (*byeonaek yeongeum boheom*) written on a **특별계정** (*teukbyeol
gyejeong*, separate account), through a two-period contract: the 연금개시 전 보험기간,
in which the premium net of a front-end deduction buys units and the policyholder
carries the whole investment risk, and the 연금개시 후 보험기간, in which the money has
moved to the **일반계정** (*ilban gyejeong*, general account) and is run at the 공시이율.

**The product is an investment wrapper plus two written options.** The
최저사망보험금보증 (GMDB) floors the death benefit at 이미 납입한 보험료 and is compulsory
under 감독규정 제7-60조제7호 [REG-R16]; the 최저연금적립금보증 (GMAB) floors the annuity
consideration at the 연금개시나이 계약해당일 and, since April 2016, is elective [R2], so
the model carries it as a switch and ships both forms. Neither guarantee reaches the
**해약환급금**, which carries no floor at any duration [S1] [S6] [S7 제50조제3항] — the
single most important fact about this product for a liability model.

**Spaces.** The model contains two:

:mod:`~.VA_KR_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model** however many contracts are
    projected.

:mod:`~.VA_KR_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the technical notes' anchor cell. It reaches the
    input tables through its ``data`` Reference, which resolves to the single
    :mod:`~.VA_KR_S.Data` Space.

The split is not tidiness. ``Projection`` is parameterized, so every ``Projection[N]``
is a separate ItemSpace with its own cells cache and readers placed there would re-read
every file for every model point.

Input data is **external**: plain CSVs in the model folder's parent directory, read at
run time rather than stored inside the model, following ``annuallife.TradLife_A``. The
model folder holds nothing but formulas, so a diff shows logic changes only — and the
model is not portable without its parent's CSVs.

**Projection basis.** Monthly steps on **보험나이** (*boheom nai*, insurance age). ``t``
counts projection months from ``t = 0``, the month containing the 계약일 and the first
premium, to ``t = proj_len() - 1``, the last month before attained age ``omega_age`` =
120 **[std]**; ``proj_len()`` is the **number** of projected months, so the frame is
``range(proj_len())`` and the policy year containing month ``t`` is ``t // 12 + 1``.
Ages increment on the policy anniversary, so ``age(t) = age_at_entry() + t // 12``.
Annuitisation falls at ``t_ann() = (annuity_age() - age_at_entry()) * 12``, the
연금개시나이 계약해당일; the 특별계정 exists for ``t < t_ann()`` and is empty after it.

Within a month, in the order the 약관 sets out [S7 제2조] [S7 제36조]: the premium is
paid and the 계약체결비용, the 납입 중 계약관리비용 and the 기타비용 are taken out of it
**in the 일반계정**, so they never enter the fund; what is left is the 특별계정 투입보험료
and it buys units. Then the **월공제액** — 위험보험료, 납입 후 계약관리비용 and both
guarantee charges — is cancelled out of the 계약자적립액 pro rata across the funds, and
any 중도인출 with it. Then, at the three annual 계약해당일 inside 「연금지급개시일 −
3년」, the mandatory pre-annuitisation de-risking tops the 채권형 fund up to 80% of the
account [S1]. Then each fund grows at its own gross asset return net of its 특별계정
운용보수, which is deducted **inside the 기준가격** rather than by cancelling units
[S7 제43조제2호]. Decrements close the month, **death first, then lapse** **[std]**.

**Which account each cash flow falls in.** The model states it rather than implying it.
:func:`~.VA_KR_S.Projection.net_cf` is the whole-contract external cash flow — what
crosses the boundary of the insurer, on either side of the 특별계정 / 일반계정 line — and
:func:`~.VA_KR_S.Projection.check_net_cf` reconstructs it as the sum of the two accounts'
own ledgers, :func:`~.VA_KR_S.Projection.net_cf_gen` and
:func:`~.VA_KR_S.Projection.net_cf_sep`, in which every internal transfer permitted by
감독규정 제5-7조 [REG-R15] appears twice with opposite signs and cancels. A model that
cannot do that has not represented the boundary.

**What one deterministic path can and cannot say.** The charges are exact on every path,
because they are contractual rates on modelled bases. The guarantee **costs** are not:
``max(0, K - AV(T))`` evaluated at one terminal account value is the option's intrinsic
value, a lower bound on its expected cost by Jensen's inequality, and it is exactly zero
whenever the path lands the account above the strike. At the base run's 투자수익률 of
2.50% the anchor cell's account is above premiums paid at annuitisation, so **the base
run reports a GMAB cost of zero while collecting the full guarantee charge**; model
points 4 and 5 run the two other mandated illustration returns, −1.00% and 3.75% [R2]
[REG-R48], so the reader sees the guarantee on both sides of the strike. The statutory
보증준비금 is a CTE(70) over a thousand scenarios or a standard factor, whichever is
greater [REG-R10] [REG-R26] [R1]; **this model publishes neither** and no number it
prints is a reserve. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the assumption tables with company data before drawing any
conclusion from the output.

**What is sourced and what is not.** The fee stack is one carrier's 상품요약서 [S2] —
계약체결비용 5.17%, 계약관리비용 3.50% inside the premium period and 1.33% after it, the
0.40%/0.60% 운용보수 and the ₩830,000 해약공제 — because the surrender charge is the
unamortised acquisition cost [R2] and the two may not come from different carriers. The
guarantee design and both guarantee charges are a second carrier's 상품안내장 [S1] —
GMDB 0.07% of the account, GMAB 0.25% of the account **plus 0.30% of 보험료총액 for at
most seven years** — with the mandatory 채권형 ladder and the 「개시일 − 3년」 de-risking
rule. The commission scale is the 2017 industry census [R1]. **Every return assumption
is [std]**: no Korean realised-return series was retrieved [R10] [S11], so the base run
sets the 투자수익률 to the 2026 평균공시이율 [REG-R48] and works back to a gross asset
return. The mortality table is a **[std]** Makeham construction anchored on the only
published 제10회 경험생명표 statistic, 65세 기대여명 23.7/27.1 [REG-R33]; the qx table
itself is not public [REG-R34] and this file must never be presented as it. The lapse
scale is calibrated to [R1]'s seven-year persistency of under 30%; the dynamic
(in-the-moneyness) form [R1] prescribes for reserving is **not** modelled, no functional
form having been published.

**Not implemented.** Named so the gaps cannot be mistaken for oversights. The
**고도재해장해급여금** of ₩10,000,000 [S1] [S2] is charged for — the 위험보험료 is a
modelled deduction — and never paid, because no 장해 incidence rate on this contract's
basis was retrieved: the 참조순보험요율 display is a 장기손해보험 one and does not reach
the life side [REG-R34] [REG-R61]. The **roll-up, step-up and
ratchet** GMAB bases are specified in ``product-spec.md`` and not run; only premium
refund at 100% is. The **GLWB / 실적배당 종신연금**, in which the money stays in the
separate account through the payout phase at a charge of 3.30% of the guarantee base
[S2], is a different product and is out of scope. The **daily 기준가격 and 좌수 ledger**
is collapsed onto a monthly grid, and with it the two-business-day pricing lag on every
transaction [S7 제39조] [S7 제50조제2항]. 펀드자동재배분, 펀드자동전환옵션, 조기연금개시,
일반계정 전환, 보험계약대출, 감액, 납입 일시중지 and the 성과·장기유지 보너스 are all
described in the specification and not modelled. The annuity is held **level** after it
starts, though the contract moves it with the 공시이율 [S5], and the 연금생명표 is not
re-struck at annuitisation though the contract permits it in the policyholder's favour
[S1].

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/variable_annuity/VA_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "VA_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
