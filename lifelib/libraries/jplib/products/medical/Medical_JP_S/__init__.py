# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese third-sector medical insurance.

:mod:`~.Medical_JP_S` is the executable counterpart of
``products/medical/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single-policy model point of 医療保険
(*iryō hoken*): office premiums, 入院給付金 (the daily hospitalization benefit),
手術給付金 (surgery), 先進医療給付金 (advanced medicine), an optional 入院一時金
(hospitalization lump sum), maintenance and claim expenses, and commission.

**This is the ``jplib`` third-sector chassis.** ``Cancer_JP_S`` and ``LTC_JP_S`` state
their deltas against the machinery here — the day-limit ledgers above all — rather than
restating it.

.. rubric:: What makes this product a different shape

A death-benefit model prices a **sum assured**. This one prices
**frequency x severity x limit**: a hospitalization is a draw of a *duration* from a
length-of-stay distribution, truncated by a per-hospitalization day limit ``L1`` and
then by a lifetime 通算 day limit ``LA`` that has **memory**. Three consequences run
through the whole model and none of them has an analogue in the protection or savings
chassis:

* the two 通算 ledgers are carried **per surviving policy**, never weighted by
  ``pols_if`` — a ledger multiplied by the in-force probability measures the block's
  consumption rather than the policyholder's, and defers the limit indefinitely;
* exhausting **both** the 疾病 and 災害 limbs terminates the contract, so the model
  carries a *benefit-driven* decrement alongside mortality and lapse;
* there is **no death benefit**, **no surrender value** on the 終身払 anchor and hence
  **no 自動振替貸付**: mortality is a pure liability release, and a missed premium
  really does lapse the policy. Importing the ``WholeLife_JP_A`` automatic-premium-loan
  logic here would suppress lapses that genuinely happen.

.. rubric:: Spaces

The model contains two:

:mod:`~.Medical_JP_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Medical_JP_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the technical notes' worked-example anchor
    cell. It reaches the input tables through its ``data`` Reference, which resolves to
    the single :mod:`~.Medical_JP_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

.. rubric:: Projection basis

Monthly steps, the notes' base grid, and not a refinement of an annual one: the unit of
account is a **day**, the per-hospitalization limit is 60 days — about two months — and
the premium mode is 月払. ``t`` is the policy month, ``t = 0, 1, ..., proj_len() - 1``.
Premium and maintenance expense fall at the start of month ``t``; benefits and the claim
expense at the end; mortality then lapse then the benefit-driven termination at the end,
in that order. Acquisition expense and initial commission fall at ``t = 0``. A
hospitalization *starting* in month ``t`` is resolved in full in month ``t``.

The horizon is the whole of life: ``proj_len()`` runs to the terminal age of the
mortality table, 116 for males and 118 for females. There is no maturity benefit and no
満期保険金 — on the 終身 chassis the only thing that happens at the horizon is nothing.

.. rubric:: What is sourced and what is not

The contractual mechanics are sourced: the daily benefit, the 60/120-day
per-hospitalization limit, the 1,095-day 通算 limit applied separately to the two limbs,
termination on exhausting both, the 20x/5x surgery multiples, the ¥20,000,000 先進医療
lifetime cap, the five-day minimum expressed as an *amount* rather than as five days, and
the absence of any surrender value under 終身払.

Everything quantitative is a standardization. No carrier publishes a rate table — the
算出方法書 is a 基礎書類 filed with the 金融庁 and is not published — so the office
premium is a model point input. There is no published morbidity table in Japan at all:
incidence, the length-of-stay distribution and surgery frequency are constructions on
公開 患者調査 statistics. And 第三分野標準生命表2018, though public and free, may not be
redistributed, so ``mort_table.csv`` is a documented proxy anchored to it rather than a
copy of it. **This model is a mechanics demonstration, not a pricing or reserving
result.** Replace the assumption tables with company data before drawing any conclusion
from the output.

.. rubric:: Model points

Nine, covering both sexes, issue ages 20 to 80, both per-hospitalization limits, both
aggregate limits, the five-day minimum floor, the 10x and in-hospital-only surgery
structures, the 入院一時金 rider, the 三大疾病無制限 特則, the 特定三疾病 premium waiver,
the surgery-after-limit contradiction in both positions, a 65歳払済 short-pay point that
is the only one on which a surrender value ever exists, and a 定期 ten-year-renewable
point. Model point 1 is the anchor cell of the worked example in the technical notes and
reproduces it to the precision the notes display.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/medical/Medical_JP_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Medical_JP_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
