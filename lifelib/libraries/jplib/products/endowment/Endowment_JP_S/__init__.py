# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese endowment and education assurance.

:mod:`~.Endowment_JP_S` is the executable counterpart of
``products/endowment/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single-policy model point of the
standardized composite in its two cells:

**endowment** (養老保険, *yōrō hoken*)
    a finite term with a maturity benefit 満期保険金 (*manki hokenkin*) equal to the death
    benefit, so the policy value converges on the sum assured by construction.

**education** (学資保険, *gakushi hoken*)
    a staged 学資金 (*gakushikin*, education money) schedule read from a table, a death
    payment that is a return of premiums rather than a sum assured, and 保険料払込免除
    (*hokenryō haraikomi menjo*, waiver of premium) on the 契約者 (*keiyakusha*,
    policyholder) — **a second decrement on a second life who is not the insured**. That
    last has no analogue in the U.S. or UK reference models.

The structural difference from a whole life chassis is that there is **no tail and no
terminal age**: the projection length is exactly the term, every state closes at the end
of the last month, and the closing cash flow is a certain payment of the sum assured to
the survivors rather than a decrement. Importing a terminal age here would project a
contract that has already matured.

**Spaces.** The model contains two:

:mod:`~.Endowment_JP_S.Data`
    Reads the four input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Endowment_JP_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Endowment_JP_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** **Monthly steps.** The index ``t`` is **0-based** and counts policy
months: ``t = 0`` is the first policy month and ``t = proj_len() - 1`` the last, where
``proj_len() = 12 policy_term()``, so the frame is ``range(proj_len())`` and the
contractual policy year is the 1-based label ``policy_year(t) = 1 + t // 12``. Premium,
maintenance expense and renewal commission fall at the start of the month; acquisition
expense and initial commission at issue; death claims and claim expense at the end of the
month of death; the staged benefit and the maturity benefit at the end of the single month
whose closing instant is the anniversary they fall on, to policies surviving that month's
mortality; surrenders at the end of the month, after deaths and after any staged benefit
just paid, valued on the surrender value net of that benefit.

**The contractual values stayed annual, and that is the point of the split.** Everything
this product guarantees is defined at a 年単位の契約応当日 — the 保険料積立金, the 解約返戻金,
the 解約控除, the 責任準備金, the staged 学資金 grid and the 満期保険金 — so a second index
``k`` counts anniversaries with ``k = 0`` at issue, the value construction
(``pol_val_pp``, ``cv_pp``, ``surr_charge_pp``, ``benefit_pct``, ``prem_cum_pp``,
``reserve_pp``, ``loan_pp``) is indexed by it, and **none of its numbers moved**. What
the monthly grid adds is the interpolating companions — ``pol_val_at_m``, ``cv_at_m`` and
their family — which a death or a surrender between two anniversaries is settled on
**[std]**, and which reproduce the annual cells at every anniversary.

Three things the finer grid buys here. The premium is 年払, so it falls in **one month out
of twelve** instead of being smeared across a year. Every payment that is a payment **on a
date** — each staged 学資金, and the 満期保険金 that is the largest single item in the whole
stream — now falls in the single month whose end is that date, so the maturity payment is
one month wide rather than one year. And ``lapse_rate``'s suppression of surrender in the
final period, which exists so that the maturity payment is not double-counted, shrinks
from a whole policy year to the one month whose end **is** the maturity date — which
returns eleven months of genuine surrender to the projection and moves the anchor cell's
maturing fraction from 0.5042 to 0.4949.

A fourth falls out of the same change and was invisible before: the education cell's
death benefit is the greater of deemed-paid premiums and the policy value, and read month
by month that ``max`` switches 85 times in 264 where at the anniversaries it never
switched at all.

What did **not** change is survivorship at the anniversaries: both mortality decrements and
voluntary surrender convert to the month on the effective convention
``r_m = 1 - (1 - r)^(1/12)``, so twelve months compound back to the annual rate exactly.

**What is sourced and what is not.** Both annual premiums on the two anchor cells are
12 times a published monthly premium for exactly those cells [S9][S11], and the 予定利率
(assumed interest rate) of 1.00% that the cash-value construction runs on is published
by product group before and after a dated revision [S9]. Everything else quantitative is
a standardization introduced for the reference implementation: no carrier publishes a
surrender-value formula or a numeric surrender-value table for either cell, no carrier
publishes an expense basis, and no carrier publishes a lapse curve by duration. The
mortality tables shipped in ``mort_table.csv`` are a **[std] construction** anchored so
that the model reproduces the rates the technical notes quote; the 日本アクチュアリー会
(Institute of Actuaries of Japan) tables they point at are cited by URL and never
reproduced, because the publisher's site terms prohibit it. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the assumption tables and
the cash-value basis with a company 算出方法書 before drawing any conclusion from the
output.

**Model points.** Nine, covering both cells, both staged-schedule shapes, the waiver in
both positions of its carve-out switch, a suppressed lapse rate on the waived state, a
loaded mortality basis, a shortened premium term, the automatic premium loan module and
a drawn policy loan. Model point 1 is the anchor cell of the worked example in the
technical notes; model point 2 is the education cell of the same worked example.

**Verification.** ``tests/test_endowment_jp.py`` asserts the notes' worked example to
the yen and the in-force columns to six decimals on both anchor cells, together with the
roll-forward identities exposed as ``check_*()`` cells.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/endowment/Endowment_JP_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Endowment_JP_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
