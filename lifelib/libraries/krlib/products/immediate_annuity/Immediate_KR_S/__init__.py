# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the Korean immediate annuity, 즉시연금.

:mod:`~.Immediate_KR_S` is the executable counterpart of
``products/immediate_annuity/technical-notes.md`` in the ``krlib`` library. It projects
gross best-estimate liability cash flows for a single-premium immediate annuity written
on Korean terms: the 생존연금 (*saengjon yeongeum*, survival annuity) paid out of the
계약자적립액 (*gyeyakja jeongnimaek*, the policyholder's account balance), the
사망보험금 (death benefit) on the two shapes that keep one, the 만기보험금 (maturity
benefit) on the inheritance shape, the 해약환급금 paid on surrender where surrender is
permitted at all, the 모집수수료 (commission) and the expense load.

**This is the library's payout-phase chassis.** A single premium is paid at inception, the
insurer deducts the 계약체결비용, the 계약관리비용 and — on the shapes that carry a death
benefit — the 위험보험료, all once, and the residue becomes the opening 계약자적립액. There
is therefore no premium term, no accumulation phase, no lapse decrement driven by an unpaid
premium, and **no acquisition strain after t = 0**: the charge taken from the fund at
inception exactly meets the outgo at inception, which is the structural difference between
this product and every other model in ``krlib``. The accumulation half of the same
machinery is ``Pension_KR_S``'s subject.

**Korea writes the product in three shapes and they are three different liabilities, not
variants of one.** The shape is a model point column of one projection:

``shape = "life"`` — 종신연금형
    The fund is divided once by an annuity factor built from the 개인연금사망률 and the
    declared rate, and the annuity runs for life with a 보증지급기간 (guaranteed payment
    period) of ten years on the representative terms. It pays no death benefit once the
    annuity has begun and it cannot be surrendered at any time. **This is the only shape
    that reads the mortality table for its annuity.**

``shape = "inheritance"`` — 상속연금형 만기형
    Interest only: the annuity is the interest on the fund less the 만기보험금 지급재원,
    the retention that rebuilds the fund to the maturity benefit. No mortality enters the
    annuity at all. The retention is the term at the centre of the **즉시연금 과소지급
    분쟁**, and it is carried here as an explicit switch — ``retention_basis`` is
    ``as_designed`` for the 산출방법서's liability and ``as_ordered`` for the one the
    금융분쟁조정위원회 ordered in 조정결정 제2017-17호, with :func:`~.Immediate_KR_S.Projection.retention_shortfall_pp`
    reporting what the second costs the insurer.

``shape = "certain"`` — 확정기간연금형
    The fund is divided over a fixed term at the declared rate and paid irrespective of
    survival. Pure interest arithmetic again, which is what makes it the sharpest available
    test of the expense load.

**Spaces.** The model contains two:

:mod:`~.Immediate_KR_S.Data`
    Reads the four input CSVs and holds their filename References. It takes no parameters,
    so each file is read **once per model** however many contracts are projected.

:mod:`~.Immediate_KR_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the technical notes' worked-example anchor. It
    reaches the input tables through its ``data`` Reference, which resolves to the single
    :mod:`~.Immediate_KR_S.Data` Space.

The split is not tidiness. ``Projection`` is parameterized, so every ``Projection[N]`` is a
separate ItemSpace with its own cells cache; readers placed there would re-read every file
for every contract.

Input data is **external**: plain CSVs in the model folder's parent directory,
``products/immediate_annuity/``, read at run time rather than stored inside the model. The
model folder holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
the model and its inputs must travel together. This follows ``annuallife.TradLife_A``.

**Projection basis.** Monthly steps on a **0-based** time index: ``t = 0`` is the first
policy month. Period ``t`` runs from time ``t`` to time ``t + 1``, row ``t`` of
``result_cf()`` carries the cash flows of month ``t``, and the annuity is payable **in
arrears** on each 연금지급일, so the payment shown on row ``t`` falls at the end of month
``t``. ``proj_len()`` is the **number of projected months**, ``12 x proj_years()``, so the
frame is ``range(proj_len())`` and runs ``t = 0 … proj_len() - 1``; the contractual policy
year is the derived label ``policy_year(t) = t // 12 + 1``. Ages are **보험나이** throughout,
and because 보험나이 increments on the 계약해당일 the attained age is
``age(t) = x + t // 12`` exactly. **This is the mode the market actually writes**: the
default election is a 연금월액 paid 매월 — 「미지급된 연금월액을 매월 연금지급일에
드립니다」 — so the monthly grid pays what the contract pays and needs no reconciliation
between a projected annual instalment and a contractual monthly one.

**The contract terms and the assumptions stay annual; only the grid is monthly.** The
보증지급기간, the 보험기간 and the 연금지급기간 are whole years, converted where the grid
needs a month count by ``annuity_term_mths()``; the 개인연금사망률 is an annual table by
age; the 공시이율 and the stepped 최저보증이율 are annual rates; and the [std] surrender
assumption is an annual rate. Each carries a uniform-force monthly companion —
``mort_rate_mth``, ``lapse_rate_mth`` and ``crediting_rate_mth`` — level inside a policy
year and stepping on each 계약해당일, with twelve of each compounding back to exactly the
year's figure.

**What is sourced and what is not.** The contractual mechanics are sourced: the premium
split into 보장계약 보험료, 사업비 and the 연금계약 순보험료 that becomes the opening fund;
the accumulation recursion at Max[공시이율, 최저보증이율]; the retention identity and its
decomposition into interest less 만기보험금 지급재원; the death benefit of 10% of the single
premium plus the fund; the nil 해약공제액 at every duration; the prohibition on surrendering
a 종신연금형 in payment; and the guarantee period's effect, which is that the payment
obligation survives the annuitant. Every **rate** is a standardization. The 경험생명표 is
produced by 보험개발원 and is **not published**, so the shipped ``mort_table.csv`` is a
``[std]`` construction anchored on the only carrier-published 개인연금사망률 rates in the
corpus and on the published 기대여명 summary, with a ``provenance`` column on every row; it
must never be presented as the 경험생명표. The 공시이율 and the 최저보증이율 are exposed as
scalars because 감독규정 제7-65조 makes the declared rate the product of a 공시기준이율
majority-weighted to the insurer's own 운용자산이익률, which no model can derive.
**This model is a mechanics demonstration, not a pricing or reserving result.** Replace the
basis with a filed same-schema one before drawing any conclusion from the output.

**Verification.** ``tests/test_immediate_annuity_kr.py`` asserts the technical notes' worked
example row by row, and ``tests/test_model_conventions_kr.py`` asserts the house style over
every model point in ``model_point_table.csv``.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/immediate_annuity/Immediate_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Immediate_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
