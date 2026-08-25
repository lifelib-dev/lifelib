# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese level term life insurance.

:mod:`~.Term_JP_A` is the executable counterpart of
``products/term_life/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single-policy model point of 定期保険
(*teiki hoken*, level term life) in the two term shapes the representative composite
offers — 年満了 (*nen manryō*, a fixed number of years, automatically **renewable** at
attained-age rates up to a ceiling) and 歳満了 (*sai manryō*, to a stated age, which
never renews) — with 高度障害 (*kōdo shōgai*, severe disability) inside the death
decrement, and **no tail states of any kind**: there is no 満期保険金 (maturity
benefit), no 解約返戻金 (*kaiyaku-henreikin*, surrender value) and no paid-up value
at any duration [S1][S4][S6][S8][S9][S10][S13][S14].

This is the library's **protection chassis**: the decrement recursion, the premium
chassis and the expense and commission structure specified here are inherited by
``IncomeTerm_JP_S`` (収入保障保険) rather than restated.

Two mechanics have no analogue in this repository's U.S. or UK term models and drive
the shape of the answer:

**更新 (*kōshin*, automatic renewal).** A 年満了 contract renews automatically at the
end of each 保険期間 unless the policyholder declines, with **no 告知 and no fresh
underwriting**, and the premium is recomputed on attained age at the scale then in
force [S1][S4][S8][S12]. On the anchor cell the monthly premium multiplies by 1.87 at
the first renewal, then 2.16, 2.34 and 2.88 — so the premium is a function of the
*term index*, not of the policy year, and the projection horizon is the renewal
ceiling of attained age 80 rather than the ten-year term. A UK term assurance
guarantees its premium for the whole term; this one guarantees it only within the
current 保険期間, which is why ``contract_boundary`` is a model point column and not a
detail.

**The renewal decline.** At each renewal boundary a proportion of survivors leave
rather than accept the repriced contract. It is a different event from a mid-term
lapse, it applies only in boundary years and only after mortality and ordinary lapse,
and it dominates both: in year 10 of the anchor cell it is 0.08235591 of 0.11175249
total exits. A model that folds it into the lapse rate cannot see the boundary at all.

**Spaces.** The model contains two:

:mod:`~.Term_JP_A.Data`
    Reads the four input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Term_JP_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.Term_JP_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Annual steps, the notes' base grid — nothing in the composite has
intra-year contractual structure, and the one intra-year mechanic that matters, the
猶予期間 (*yūyo kikan*, grace period of about one month), sits inside a decrement the
annual grid represents as a rate [S1][S8]. Policy year ``t`` runs 1, 2, ...,
``proj_len()``. Premiums and maintenance expense fall at the start of the year;
acquisition expense and initial commission at issue; death and 高度障害 claims and
their claim expense at the end of the year; ordinary lapse at the end of the year after
deaths; the renewal decline at the end of a boundary year after lapse.

**One decrement, one benefit.** 生保標準生命表2018（死亡保険用）includes 高度障害 inside
its death rate [REG-R20], and the contract pays one sum assured and terminates on
whichever event comes first [S1][S8]. There is therefore no ``disability_rate`` and no
second decrement anywhere in this model; adding one would double-count the benefit.

**What is sourced and what is not.** The contractual mechanics are sourced: the
attained-age repricing at 更新 and its absence of 告知, truncation at the ceiling into
an 80歳満了 term, the 歳満了 shape never renewing, the absence of any 解約返戻金 and
hence of 自動振替貸付, and the リビング・ニーズ特約 discount and its per-insured cap.
**The monthly premium is sourced too** — ¥974 for the anchor cell, from a published
rate card [S2] — which is the sharpest documentary contrast with this repository's UK
term model, where no premium basis is observable at all. Everything else is a
standardization: the best-estimate mortality factor, the lapse curve, the
renewal-decline rate, the expense and commission levels, and the premium scale beyond
the published age-50 cell. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the assumption tables with company data before drawing any
conclusion from the output.

**The mortality table shipped here is a proxy, not the published table.**
標準生命表2018 is freely readable at a stable public URL [REG-R18][R3][R4], but its
publisher prohibits reproduction and transmission to third parties without written
consent [REG-R21], so ``mort_table.csv`` is a **[std]** construction anchored on the
handful of rates the worked example quotes and log-linearly interpolated between them.
It reproduces the notes' own rates exactly and nothing else should be read from it.
See :mod:`~.Term_JP_A.Data` for the construction.

**Model points.** Nine, covering both sexes, both term shapes, the renewal ladder to
the ceiling, truncation of the final term, both contract boundaries, all three optional
riders, and the extremes of the issue-age and sum-assured envelopes. Model point 1 is
the anchor cell of the worked example in the technical notes.

**Verification.** ``tests/test_term_life_jp.py`` asserts the notes' worked example to
the yen and the in-force column to six decimals: ``CF(1) = -18,612.32``,
``l(11) = 0.466683``, the renewal ladder ¥974 → ¥1,823 → ¥3,933 → ¥8,976 → ¥23,881,
and undiscounted totals of ¥470,348.54 of premium and +¥50,400.25 of net cash flow over
the fifty years.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/term_life/Term_JP_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Term_JP_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
