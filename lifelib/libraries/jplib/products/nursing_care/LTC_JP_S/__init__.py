# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese private nursing-care insurance.

:mod:`~.LTC_JP_S` is the executable counterpart of
``products/nursing_care/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single-policy model point of
介護保険 (*kaigo hoken*) on the 公的介護保険連動型 (public-scheme-linked) design: office
premiums, a 介護一時金 (care lump sum) on first satisfaction of a 要介護 threshold, a
介護年金 (care annuity) paid annually in advance from a higher threshold and capped at a
stated number of instalments, a 保険料払込免除 (premium waiver) from a *lower* threshold
than either, maintenance and claim expenses, and commission.

The structural difference from ``Medical_JP_S``, the third-sector chassis these
notes state their deltas against, is what the model has to represent. ``medical`` is
**frequency x severity x limit** — a daily amount times paid days, capped per
hospitalization and again in aggregate. Nursing care is **incidence into an absorbing
state**: a three-state chain (healthy, in care, dead) whose entry is certified by a
municipality, whose exit in the base run is only death, and whose payment counter
genuinely binds. There is no day ledger of any kind here, no 支払限度日数 machinery, and
no ``agg_days_*`` cells. Four further absences are product facts rather than gaps:
**no surrender value**, so ``cv_pp`` does not exist and a lapse pays nothing; **no
自動振替貸付**, because there is nothing to lend against; **no death benefit**, so
``claims_death`` does not exist; and **no maturity**, because the cover is whole of
life.

**Spaces.** The model contains two:

:mod:`~.LTC_JP_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.LTC_JP_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.LTC_JP_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps. ``t`` is the policy month, ``t = 0, 1, ...,
proj_len() - 1``, and month ``t`` runs from ``t`` to ``t + 1`` months after the 契約日.
Office premium and maintenance expense fall at the start of the month, the lump sum,
the annuity instalment and the claim-handling expense at the end; then care incidence,
then mortality, then lapse, then the benefit-driven termination on the last permitted
annuity instalment. Acquisition expense and initial commission fall at ``t = 0``. The
annuity is paid **in advance**: its first instalment falls on the entry month itself.
Cover is whole of life, so the projection runs to the terminal age of the mortality
table — 116 for males and 118 for females.

**What is sourced and what is not.** The contractual mechanics are sourced: the
either/or public-certification and company-basis trigger, the once-only lump sum that
does not terminate the contract, the survival-tested annuity in advance with its
ten-instalment cap and retroactive extinction, the waiver firing one grade below the
lump sum and two below the annuity, and the outright nil surrender value. Everything
quantitative is a standardization. **No carrier publishes 予定発生率, 予定利率 or
予定死亡率 for this product, and the regulator confirms there is nothing standard to
publish for 第三分野 business**, so the office premium is a model point input rather
than a computed quantity, and the incidence basis shipped here is constructed in
public from the 認定率 and grade composition of 介護保険事業状況報告. The mortality table is
likewise a **[std] construction**: 第三分野標準生命表2018 is free to read but its
publisher's site terms prohibit reproduction, so ``mort_table.csv`` is a log-linear
graduation through the rates the library quotes and attributes, never a copy. **This model is a
mechanics demonstration, not a pricing or reserving result.** Replace the assumption
tables with company data before drawing any conclusion from the output.

**Model points.** Eight, covering both sexes, issue ages 40 to 79, the sub-65 特定疾病
gate with and without the company-basis limb, the state-tested annuity with a non-zero
recovery rate, the 認知症一時金特約, the simplified-underwriting 1-year 不担保期間, a
five-instalment annuity, a lower pair of benefit thresholds, and the anti-selective
lapse module switched on. Model point 1 is the anchor cell of the worked example in
the technical notes and reproduces it to the precision the notes display.

**Verification.** ``tests/test_nursing_care_jp.py`` asserts the notes' four-row worked
example and its policy-year-1 aggregate, the roll-forward and nesting identities, and
each of the notes' known modelling pitfalls.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/nursing_care/LTC_JP_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "LTC_JP_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
