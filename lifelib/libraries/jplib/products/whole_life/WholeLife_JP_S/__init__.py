# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese whole life assurance (終身保険).

:mod:`~.WholeLife_JP_S` is the executable counterpart of
``products/whole_life/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single-policy model point of the
standardized composite 終身保険 (*shūshin hoken*) — level premium for a stated
保険料払込期間, a death and 高度障害 benefit level for life, no maturity date and no
満期保険金, and therefore a 保険料積立金 and a 解約返戻金 that carry the whole economics of
the product.

This is the library's **savings chassis**. Four mechanics are specified once here and
inherited by ``Endowment_JP_S`` and ``FXWholeLife_JP_S``: the closed-form policy value,
the 解約返戻金 built from it, the 低解約返戻金型 (*tei-kaiyaku-henreikin-gata*)
suppression and its **cliff** at 払込満了, and the 自動振替貸付 (*jidō furikae
kashitsuke*, automatic premium loan, APL) that makes lapse on this chassis a funded
event rather than a behavioural one.

Two structural facts separate it from the protection models in the same library. There
are **no tail states and no expiry**: the projection runs to the terminal age of the
mortality table, ω = 109 (M) / 113 (F), every remaining life dies in the final period, and
nothing is paid at the horizon but the death benefit. And **premiums stop at 払込満了
while nothing else does** — maintenance expense, death claims, surrender benefits and
the cash value all continue for life, so a projection truncated at the end of the
premium term misses the majority of the liability.

**Spaces.** The model contains two:

:mod:`~.WholeLife_JP_S.Data`
    Reads the three input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.WholeLife_JP_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the technical notes' worked-example anchor
    cell. It reaches the input tables through its ``data`` Reference, which resolves to
    the single :mod:`~.WholeLife_JP_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** **Monthly steps.** The time index ``t`` is **0-based** and counts
policy months: ``t = 0`` is the first policy month, month ``t`` runs from time ``t`` to
time ``t + 1``, the frame is ``range(proj_len())`` so the last index is
``proj_len() - 1``, and the contractual policy year is the derived 1-based label
``policy_year(t) = 1 + t // 12``. Premium, maintenance expense and renewal commission fall
at the start of the month; acquisition expense and initial commission at issue; death
claims and claim expense at the end of the month of death; surrenders at the end of the
month, **after** deaths, on the surrender value at that instant.

**The contractual values stayed annual, and that is the point of the split.** Everything
this product guarantees is defined at a 年単位の契約応当日 — the 解約返戻金, the 解約控除,
the 責任準備金, the 保険料払込期間, the loan rate's capitalisation — so ``pol_val_pp``,
``cv_pp``, ``surr_charge_pp``, ``reserve_pp`` and ``loan_pp`` keep a second index, the
anniversary ``d = 0 … proj_years()`` with ``d = 0`` at issue, and **none of their numbers
moved**. The cash-value construction is calibrated to one carrier's published *annual*
surrender-value run, so re-deriving it monthly would have moved a fitted number rather
than a modelled one. What the monthly grid adds is ``cv_at_m(u)``, the value at an
elapsed month, by linear interpolation between those anniversaries **[std]**.

Three things the finer grid buys on this product. The premium is 年払, so it now falls in
**one month out of twelve** instead of being smeared across a year: the statement is a
sawtooth of one inflow a year against expense and claims every month, which is what a 年払
contract is. The 払込満了 **cliff is one month wide** rather than one year — the surrender
value steps up by ``1 / k`` at the anniversary and the 15% behavioural surge lands in the
month after the last premium, beside the step that provokes it. And the **[std ordering]**
the annual grid needed is retired: it had to pay every surrender in policy year ``m`` the
post-step value because the step and the grid landed on the same year, and here eleven of
those twelve months are inside the 保険料払込期間 and are paid the suppressed value, which
is what the contract says.

What did **not** change is survivorship at the anniversaries. Mortality and surrender
convert to the month on the effective convention ``r_m = 1 - (1 - r)^(1/12)``, so twelve
months compound back to the annual rate exactly and ``pols_if(12 j)`` reproduces the
annual model's ``pols_if(j)``. Every difference between the two runs is a timing
difference or the cliff ruling above, and never a change of decrement basis.

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
:mod:`~.WholeLife_JP_S.Data` for what that costs.

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
    >>> model = mx.read_model("products/whole_life/WholeLife_JP_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "WholeLife_JP_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
