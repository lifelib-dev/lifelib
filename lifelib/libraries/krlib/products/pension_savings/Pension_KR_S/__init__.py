# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for a Korean tax-qualified pension savings contract.

:mod:`~.Pension_KR_S` is the executable counterpart of
``products/pension_savings/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single-policy model point of
연금저축보험 (*yeongeum jeochuk boheom*, tax-qualified pension savings insurance) — the
insurance leg of the statutory 연금저축계좌 wrapper of 소득세법 제20조의3제1항제2호: a
deferral phase in which a level monthly 기본보험료, net of two published percentage
charges, accumulates into a 계약자적립액 credited at the 공시이율 over a stepped
최저보증이율 floor; an annuitisation step at the 연금개시일 with a 100.1%-of-premiums
minimum fund; and a payout phase of 종신연금형 (life annuity with a guarantee period) or
확정기간연금형 (annuity-certain) instalments.

**The product is an account, not a net-level-premium reserve, and the model is built that
way.** The 계약자적립액 is a contractual balance: charges come off the premium, the
remainder is credited at the declared rate, and nothing else moves. There is no
survivorship release, because there is no mortality risk to release — every retrieved
life-insurer 연금저축보험 pays the fund and nothing more on death before annuitisation,
and the composite's surrender charge is nil, so **death and surrender pay the same amount
at every deferral duration**. Mortality enters this contract in exactly one place: the
annuity factor struck at the 연금개시일 on the annuitant basis (연금사망률), which the
model also uses as the in-force decrement.

**Spaces.** The model contains two:

:mod:`~.Pension_KR_S.Data`
    Reads the nine input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Pension_KR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Pension_KR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated **once per
model**, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps, on 보험나이 (*boheom nai*, insurance age). ``t``
counts completed policy **months** since issue, 0-based: the 기본보험료 falls at
``t = 0 .. m - 1`` where ``m = 12 x`` the 납입기간 in years, the 계약자적립액 accumulates
over ``t = 0 .. n`` where ``n =`` :func:`~.Pension_KR_S.Projection.annuitisation_t`, the
annuity instalment is paid monthly from ``t = n``, and
:func:`~.Pension_KR_S.Projection.proj_len` is the **number** of projected periods — the
exclusive end of the frame, ``12 x`` :func:`~.Pension_KR_S.Projection.proj_years` — so
``result_cf()`` runs ``t = 0 .. proj_len() - 1``. The contractual policy year is the
derived 1-based label ``policy_year(t) = t // 12 + 1`` and the 보험나이 is
``age(t) = issue_age() + t // 12``, exact because 보험나이 increments on the 계약해당일.
Contract terms stay in years: the 납입기간, the 납입유예 and the 연금개시나이 are annual
quantities the model converts to month counts where the grid needs one, and the annual
assumptions stay annual — ``credit_rate(t)``, ``mort_rate(t)`` and ``lapse_rate(t)`` are
the yearly figures the technical notes tabulate, with ``credit_rate_mth``,
``mort_rate_mth`` and ``lapse_rate_mth`` companions that compound back to them over
twelve months. Statutory annual figures stay annual too — the 별표 14 표준해약공제액 is
struck on the 연납보험료 and the 소득세법 세액공제 limit and 연금수령한도 are per-year
amounts, each apportioned across the twelve months of the year rather than restated.

**The tax layer is carried but is not a cash flow.** 연금저축 relief is a **세액공제** —
a tax credit of 16.5% or 13.2% of contributions up to ₩6,000,000 a year — and a
withdrawal that misses the statutory 연금수령 conditions bears **16.5% 기타소득세**.
Neither is an insurer cash flow, so neither enters :func:`~.Pension_KR_S.Projection.net_cf`; both are published as
their own cells and in ``result_tax()``, because between them they are what drives the
lapse assumption and the annuitisation election on this product.

**What is sourced and what is not.** The contractual mechanics are sourced: the charge
schedule as percentages of the 기본보험료, the nil 해약공제액, the death benefit as the
fund, the 100.1% minimum fund at annuitisation, the two annuity forms and their bases, the
0.5% 연금수령기간 관리비용 and the 공시이율 / 최저보증이율 machinery. The mortality basis
is **not** a published table: the 경험생명표 is produced by 보험개발원 and released only
as summary statistics, so ``mort_table.csv`` is a **[std]** Makeham construction fitted to
the six annuitant rates two carriers publish in their 상품요약서 and calibrated to the
annuity factors implied by a published illustration, with a ``provenance`` column on every
row. The lapse curve, the best-estimate mortality factor, the cash expenses and the policy
loan rate are standardizations introduced for the reference implementation. **This model
is a mechanics demonstration, not a pricing or reserving result.** Replace the assumption
tables with company data, and the mortality basis with the filed 산출방법서 basis, before
drawing any conclusion from the output.

**Model points.** Nine. Point 1 is the anchor cell of the worked example in the technical
notes. The other eight exercise the female basis, a 20-year guarantee with no deferral
gap, three 확정기간연금형 terms, the low and high ends of the issue-age envelope, the
minimum 연금개시나이 of 55 on the guaranteed-rate scenario, the 연금개시시점 mortality
vintage, the 연금저축추가납입특약 with the postal insurer's front-end 해지공제액 on a
hybrid crediting-rate scenario, and — on one point — a 납입유예 payment holiday with the
100.1% guarantee withdrawn, a 보험계약대출, a participating contract with a declared
dividend and the annuitant-mortality ratchet.

**Verification.** ``tests/test_pension_savings_kr.py`` asserts the notes' worked example —
the annuitisation quantities, the deferral rows, the fund and surrender value at
납입완료, and the payout rows — to the precision the notes display, and every product fact
the notes list as a modelling pitfall.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/pension_savings/Pension_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Pension_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
