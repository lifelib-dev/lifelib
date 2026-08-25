# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese 収入保障保険 (survivor income term).

:mod:`~.IncomeTerm_JP_S` is the executable counterpart of
``products/income_guarantee/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows, on a **monthly** grid, for a
single-policy model point of 収入保障保険 (*shūnyū hoshō hoken*) — a death benefit paid as a
level monthly income from the insured event to a fixed expiry date, floored by the
最低支払保証期間 (*saitei shiharai hoshō kikan*, minimum payment guarantee period).

**This is a death product.** The insured event is death, or the contractual 高度障害状態
(*kōdo shōgai jōtai*, severe disability state) treated as its accelerated equivalent
and carried inside the same decrement, because 生保標準生命表2018（死亡保険用）already includes
高度障害 in its death rate. It is **not** income protection in ``uklib``'s sense, where
``IP_UK_S`` insures disability and pays while the insured cannot work: nothing here
models a disability decrement, and a reader arriving from that model should expect the
UK family income benefit shape instead.

**The structural fact this model exists to get right.** The projection horizon is
**longer than the policy term**. Where the insured event falls so late that fewer than
``guar_m()`` months remain, the annuity payment period is extended *past the expiry
date* until the guarantee has run, so ``proj_len() = term_m() + guar_m() - 1``. On the
anchor cell that is 443 months against a 420-month term: a death in policy month 420
pays its twenty-fourth instalment twenty-three months after cover ended. Terminating
the projection at the end of the term truncates real, contractual liability, and every
remaining number still looks reasonable — which is what makes it the easiest error to
make on this product.

**Spaces.** The model contains two:

:mod:`~.IncomeTerm_JP_S.Data`
    Reads the four input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.IncomeTerm_JP_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.IncomeTerm_JP_S.Data`
    Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps, and the grid is the contract rather than a
refinement: the benefit is one instalment per monthly payment date, the instalment
count is a month count, and the 最低支払保証期間 is quoted in years but binds in months.
Policy month ``t`` runs 1, 2, ..., ``proj_len()``. Premium, maintenance expense and
renewal commission fall at the start of the month on the in-force population;
acquisition expense and initial commission at issue; claims, claim expense, the
annuity instalments and the annuity administration expense at the end of the month;
ordinary lapse at the end of the month, after deaths.

**What is sourced and what is not.** The contractual mechanics are sourced: the
instalment count ``max(N - m + 1, G)``, the guarantee as a term extension past expiry
rather than as a benefit floor inside the term, the absence of any survival condition
on the instalments, the absence of any 解約返戻金 at any duration, premium cessation on
the annuity event, and the absence of 更新. The monthly office premium of the anchor
cell is a published rate. Everything else quantitative is a standardization: the
mortality basis, the rate-class factors, the lapse table, the expense and commission
levels, and the commutation discount rate. **This model is a mechanics demonstration,
not a pricing or reserving result.** Replace the assumption tables with company data
before drawing any conclusion from the output.

**Model points.** Nine, covering both sexes, all four rate classes, both guarantee
lengths on the composite's menu, three premium frequencies, each of the four optional
modules in its switched-on position, and one edge cell where the guarantee equals the
whole term so that every claim pays the same number of instalments. Model point 1 is
the anchor cell of the worked example in the technical notes and reproduces it to the
precision the notes display.

**Verification.** ``tests/test_income_guarantee_jp.py`` asserts the notes' worked
example, the guarantee identity ``ends_at(m) = max(N, m + G - 1)``, the run-off tail in
months 421-443 row by row, and the in-payment ledger against an independent rebuild.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/income_guarantee/IncomeTerm_JP_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "IncomeTerm_JP_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
