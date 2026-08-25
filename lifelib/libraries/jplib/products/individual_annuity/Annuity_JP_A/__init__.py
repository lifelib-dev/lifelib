# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for a Japanese fixed individual annuity.

:mod:`~.Annuity_JP_A` is the executable counterpart of
``products/individual_annuity/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single-policy model point of
定額個人年金保険 (*teigaku kojin nenkin hoken*, fixed individual annuity insurance) with the
税制適格特約 (*zeisei tekikaku tokuyaku*, tax-qualification rider) attached: a deferral
phase in which a level office premium accumulates into the 保険料積立金 with a survivorship
release, an annuitisation step at the 年金支払開始日, and a payout phase of 確定年金
(*kakutei nenkin*, annuity-certain) instalments — or, with the module switched on,
保証期間付終身年金 (a life annuity with a guarantee period).

**The product is two contracts joined at one date, and the model is built that way.**
Before the 年金支払開始日 the liability is a savings fund with a death benefit capped at
cumulative premiums and a surrender value capped at that; after it the liability is a
stream of instalments that does not depend on survival at all. The two phases read
different mortality tables — 生保標準生命表2018（死亡保険用）and 生保標準生命表2007（年金開始後用）— and
the best-estimate adjustment to those tables **reverses sign** at the join, because the
first is prudent against death and the second against longevity.

**Spaces.** The model contains two:

:mod:`~.Annuity_JP_A.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Annuity_JP_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.Annuity_JP_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated **once per
model**, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Annual steps, the notes' base grid. ``t`` counts completed policy
years since issue, 0-based: premiums fall at ``t = 0 .. m - 1``, the fund accumulates
over ``t = 0 .. n`` where ``n = m + d``, and the annuity is paid at
``t = n .. n + k - 1``. Premiums, annuity instalments, maintenance expense and
commission fall at the start of the year; death benefits and surrender payments at the
end; lapses act on the survivors of mortality, death before lapse. Acquisition expense
and initial commission fall at ``t = 0``. There are no tail states: the 確定年金 pays
exactly ``k`` instalments and the contract ends.

**What is sourced and what is not.** The contractual mechanics are sourced: the death
benefit as cumulative premiums, the surrender value capped at the death benefit, the
unavailability of surrender from the 年金支払開始日, the unconditional 確定年金 instalments,
and the published 年金の一括払 commutation factors. The mortality basis is **not** a
published table. 標準生命表2018 and the 2007 年金開始後用 table are readable at stable public
URLs but their publisher's terms prohibit reproduction and transmission, so this library
ships **no copy of either**: ``mort_table.csv`` is a [std] construction anchored to quoted
spot rates — the canonical library-wide 死亡保険用 table graduated log-linearly between its
sourced anchors, and a Makeham law on 年金開始後用 — and its ``provenance`` column says so on
every row.
The expense loading, the surrender charge, the lapse curve, the cash expenses and the
best-estimate mortality factors are standardizations introduced for the reference
implementation. **This model is a mechanics demonstration, not a pricing or reserving
result.** Replace the assumption tables with company data, and the mortality basis with
licensed tables, before drawing any conclusion from the output.

**Model points.** Nine. Point 1 is the anchor cell of the worked example in the technical
notes and reproduces every figure it displays. The other eight exercise the female basis,
a 15-year certain period, a zero 据置期間, the 保証期間付終身年金 election, full 年金の一括払
commutation, the 0.70 tontine death-benefit ratio, the 自動振替貸付 module, and the 契約者貸付
module run together with a non-zero declared dividend and dynamic lapse. Point 9 is the
anchor cell with nothing changed but the payout form, so the ¥281,300 life-annuity
instalment and the ¥638,100 certain one are bought out of the same 年金原資.

**Verification.** ``tests/test_individual_annuity_jp.py`` asserts the notes' worked
example — the annuitisation quantities, the four deferral rows, the fund and surrender
value at the crossover, and the payout rows — to the precision the notes display, and
every product fact the notes list as a modelling pitfall.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/individual_annuity/Annuity_JP_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Annuity_JP_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
