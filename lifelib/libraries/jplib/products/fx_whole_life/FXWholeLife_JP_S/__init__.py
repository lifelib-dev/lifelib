# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese foreign-currency whole life.

:mod:`~.FXWholeLife_JP_S` is the executable counterpart of
``products/fx_whole_life/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single-policy model point of
外貨建終身保険 (*gaika-date shūshin hoken*, foreign-currency-denominated whole life
assurance) in its 積立利率変動型 form, on a **monthly** grid, in the two shapes the
representative product carries:

``LEVEL``
    平準払 積立利率変動型 — a level US-dollar premium, a 積立利率 redeclared monthly and
    floored at the contract's own 予定利率, a 増加死亡保険金額 uplift over the 基本保険金額, and
    **no** 市場価格調整.

``SINGLE``
    一時払 積立利率更改型 — one premium, a rate fixed for a 15-year 積立利率適用期間, a death
    benefit of ``max(積立金, 解約返戻金)`` with no sum assured above the fund, a 市場価格調整
    on surrender inside the period, and the 目標到達時円建終身保険移行特約 as an election.

**Everything the model computes is in US dollars.** The policy currency is the model
currency; the yen columns are a *translation* of the dollar ledger, and the translation
is three separate rates — premiums at ``e + s``, benefits at ``e - s``, expenses and
commission at ``e`` — so ``net_cf_jpy(t)`` is not ``net_cf(t)`` times anything. The
difference is the insurer's 為替手数料 spread income and the model publishes it as its own
column, ``fx_spread_jpy``.

**Spaces.** The model contains two:

:mod:`~.FXWholeLife_JP_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.FXWholeLife_JP_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.FXWholeLife_JP_S.Data`
    Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps. ``t`` counts completed policy months from 契約日,
``t = 0 ... proj_len() - 1``, and ``t = 0`` is the month beginning at issue. Stepping
is on the 月単位の契約応当日, not the calendar month end: the 約款 credits the 積立利率 from
the monthly policy anniversary while the 重要事項説明書 says the rate is *declared* on the
1st, and crediting on calendar month ends would be wrong by the anniversary offset for
the whole life of the contract. There is no maturity date and no 満期保険金; the horizon
is the terminal age of the mortality table, ``12 x (omega - x + 1)`` months, and there
are no tail states.

**What is sourced and what is not.** The contractual mechanics are sourced: the
surrender-value formula ``AV (1 - mva - sc) kl``, the 解約控除 scale and its base (the
積立金, not the 基本保険金額), the symmetry of the 市場価格調整, the 増加死亡保険金額's definition
against a 予定利率 basis, the 低解約返戻金割合 ramp, the ±50銭 conversion spread, the one-year
dead zone on the target test and the fact that the test runs on the *surrender* value.
The charge stack is not: every carrier in the source set refuses to quantify its
mortality-and-expense charge, so ``prem_charge_early``, ``prem_charge_late`` and
``maint_rate`` are **back-solved** from one carrier's published guaranteed
surrender-value run and carry the whole surrender-benefit stream. The mortality basis
is a **[std]** construction anchored to published rates, not a copy of a table whose
publisher restricts redistribution. **This model is a mechanics demonstration, not a
pricing or reserving result.** Replace the assumption tables with company data before
drawing any conclusion from the output.

**Model points.** Eight, covering both shapes, the 低解約返戻金特則 cliff, the 自動振替貸付,
a crediting rate above the guaranteed floor (which is what makes the uplift and the
特別積立金 non-zero), the prospective uplift basis, a loaded mortality assumption, an FX
path, dynamic surrender, both target elections, a negative 市場価格調整, a female life at
the female terminal age and a policy settling in US dollars throughout. Model point 1
is the anchor cell of the worked example in the technical notes.

**Verification.** ``tests/test_fx_whole_life_jp.py`` asserts the notes' worked example
to the precision the notes print it — the first three months to four decimal places,
the account and surrender values to the cent, the nine-duration calibration table, the
whole-run totals, the yen ledger and its ¥125.17 spread, the ``mva(36)`` row across
five rate moves and the month-52 target hit with its three counterfactuals.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/fx_whole_life/FXWholeLife_JP_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "FXWholeLife_JP_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
