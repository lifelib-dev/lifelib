# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese whole life assurance (終身保険).

:mod:`~.WholeLife_JP_A` is the executable counterpart of
``products/whole_life/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single-policy model point of the
standardized composite 終身保険 (*shūshin hoken*) — level premium for a stated
保険料払込期間, a death and 高度障害 benefit level for life, no maturity date and no
満期保険金, and therefore a 保険料積立金 and a 解約返戻金 that carry the whole economics of
the product.

This is the library's **savings chassis**. Four mechanics are specified once here and
inherited by ``Endowment_JP_A`` and ``FXWholeLife_JP_S``: the closed-form policy value,
the 解約返戻金 built from it, the 低解約返戻金型 (*tei-kaiyaku-henreikin-gata*)
suppression and its **cliff** at 払込満了, and the 自動振替貸付 (*jidō furikae
kashitsuke*, automatic premium loan, APL) that makes lapse on this chassis a funded
event rather than a behavioural one.

Two structural facts separate it from the protection models in the same library. There
are **no tail states and no expiry**: the projection runs to the terminal age of the
mortality table, ω = 109 (M) / 113 (F), every remaining life dies in the final year, and
nothing is paid at the horizon but the death benefit. And **premiums stop at 払込満了
while nothing else does** — maintenance expense, death claims, surrender benefits and
the cash value all continue for life, so a projection truncated at the end of the
premium term misses the majority of the liability.

**Spaces.** The model contains two:

:mod:`~.WholeLife_JP_A.Data`
    Reads the three input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.WholeLife_JP_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the technical notes' worked-example anchor
    cell. It reaches the input tables through its ``data`` Reference, which resolves to
    the single :mod:`~.WholeLife_JP_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Annual steps on policy years running anniversary to anniversary,
which is the notes' grid: the composite has no intra-year contractual structure, and the
one date that matters inside a year — the 払込満了日 — is an anniversary by construction.
Premium, maintenance expense and renewal commission fall at the start of the year;
acquisition expense and initial commission at issue; death claims and claim expense at
the end of the year of death; surrenders at the end of the year, **after** deaths, on
the surrender value at that anniversary.

**What is sourced and what is not.** The contractual mechanics are sourced: the level
whole-of-life benefit, 高度障害 paid at the same amount and inside the same decrement,
the 0.70 suppression factor and its identity with the premium-paying period, the step at
払込満了, the APL continuation test and its interest ceiling, the 契約者貸付 fractions and
the clawback that keeps the suppressed basis in force where low-period premiums went
unpaid. The quantitative basis is not. The 予定利率, 予定死亡率 and 予定事業費率 live in
the filed but unpublished 算出方法書, so the cash-value construction is calibrated to one
carrier's published surrender table instead; no carrier publishes an expense basis at
all; and no carrier publishes a lapse curve by duration. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the assumption tables with
company data, and ``pol_val_pp`` with a real 算出方法書, before drawing any conclusion
from the output.

**Mortality.** ``mort_table.csv`` is a **[std]** construction, not the published table.
生保標準生命表2018（死亡保険用）is free to read at a stable public URL, but the publisher's
terms restrict reproduction and transmission, so the shipped file quotes the individual
rates the worked example needs and fills the rest by log-linear interpolation between
them, tagging every row in its ``provenance`` column. See
:mod:`~.WholeLife_JP_A.Data` for what that costs.

**Model points.** Ten, covering the suppressed and ordinary forms, a 終身払 point on
which the cliff cannot happen, a female short-pay point with a 払済保険 election, the
premium-default and APL module in both the suppressed and the ordinary configuration, a
契約者貸付 drawdown, dynamic surrender with the cliff spike switched off, a 5年ごと利差配当
variant with a mortality adjustment, and the oldest issue age in the envelope. Model
point 1 is the anchor cell of the worked example in the technical notes.

**Verification.** ``tests/test_whole_life_jp.py`` asserts the notes' worked example to
the yen and the in-force column to six decimals, the exact ``1 / k`` ratio at the cliff,
the APL advance counts on both forms, and every ``check_*`` roll-forward identity on
every shipped model point.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/whole_life/WholeLife_JP_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "WholeLife_JP_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
