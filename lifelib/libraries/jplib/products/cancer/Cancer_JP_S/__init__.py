# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese がん保険 (cancer insurance).

:mod:`~.Cancer_JP_S` is the executable counterpart of
``products/cancer/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single-policy model point of the
標準化された composite described in ``products/cancer/product-spec.md``: a whole-of-life,
無配当・無解約払戻金型 third-sector contract paying a repeating がん診断一時金, a reduced
上皮内新生物 tier, an unlimited-day がん入院給付金, がん手術給付金, a monthly がん治療給付金 under a
60-month ledger, がん通院給付金 and a 先進医療 reimbursement, with the premium waived from the
first invasive diagnosis.

**The structural difference from the third-sector chassis.** ``Medical_JP_S`` projects a
single in-force population and reads a hospitalisation incidence off it. A cancer model
cannot: the diagnosis benefit repeats on a two-year cycle, the inpatient benefit has no
day limit and the treatment benefit pays by the month, so all three run on how long the
insured lives *after* diagnosis. This model therefore carries three states — never
diagnosed, diagnosed and inside the two-year cycle, diagnosed and eligible again — and
needs a post-diagnosis survival basis as well as an incidence basis. There is no ``L1``
per-hospitalization day ledger, no 通算 lifetime day ledger and no benefit-driven
termination anywhere in it; importing them from the medical chassis caps a benefit every
retrieved source says is uncapped.

**Spaces.** The model contains two:

:mod:`~.Cancer_JP_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Cancer_JP_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.Cancer_JP_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Monthly steps, the notes' base grid, and monthly by construction
rather than by approximation: the 90-day waiting period is three months of the grid, the
treatment benefit's unit of payment *is* the calendar month, and the premium mode is 月払
at every carrier in the composite. ``t`` is the policy month, ``t = 0, 1, ...,
proj_len() - 1``. Premium and maintenance expense fall at the start of month ``t``; every
benefit and the claim-handling expense at the end; decrements at the end, mortality then
lapse. Acquisition expense and initial commission fall at ``t = 0``. Cover is whole of
life and runs to the terminal age of 第三分野標準生命表2018 — 116 male, 118 female — so the
anchor cell projects 924 months.

**What is sourced and what is not.** The contractual mechanics are sourced: the 90-day
waiting period as a hard zero, the two-year repeat cycle measured from the previous
payment trigger, 上皮内新生物 as a separate once-only tier that does not trigger the waiver,
the absence of any day limit and of any surrender value, and the premium waiver on first
invasive diagnosis. The incidence basis is genuinely sourced too — 全国がん登録 publishes
罹患率 by five-year age band — but its **sex split** is a two-point interpolation, and the
survival, relapse, treatment-month, outpatient and 先進医療 assumptions have no public
source at all. The mortality table shipped here is a **[std]** construction anchored on
第三分野標準生命表2018 男 q(40) = 0.00076 and is **not** a copy of that table, whose publisher's
terms prohibit redistribution. **This model is a mechanics demonstration, not a pricing
or reserving result.** Replace the assumption tables with company data before drawing any
conclusion from the output.

**Model points.** Eight. Point 1 is the anchor cell of the worked example in the
technical notes; the others exercise the female incidence limb and the 118 terminal age,
the 10年更新 定期 chassis flag with ``repeat_conditioned`` on, the ¥5,000 course with no
先進医療 rider and a treatment cap that binds early, both ends of the 20-75 issue-age range,
the 65歳払済 premium period, a no-waiver design in which premiums ride on ``pols_if`` and
diagnosed lives can lapse, and the がん退院一時金 rider.

**Verification.** ``tests/test_cancer_jp.py`` asserts the notes' six-row worked example
and its policy-year-1 aggregates, the ¥16,035.00 of benefit per diagnosed life-month, the
waiting period as a hard zero, the premium riding on ``pols_healthy`` rather than
``pols_if``, and the seven ``check_*`` roll-forward and ledger identities.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/cancer/Cancer_JP_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Cancer_JP_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
