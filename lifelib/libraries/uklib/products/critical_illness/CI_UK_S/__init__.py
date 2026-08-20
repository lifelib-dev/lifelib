# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for UK critical illness cover.

:mod:`~.CI_UK_S` is the executable counterpart of
``products/critical_illness/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single-policy model point of UK
critical illness cover: an **accelerated** life-or-CI contract paying the sum assured on
the first of death, terminal illness or diagnosis of a listed condition, with
non-terminating **additional-payment** and **children's-cover** benefits alongside it,
and a **standalone** variant on which death pays nothing.

The product sits on the term assurance chassis specified in
``products/term_assurance/`` and implemented as :mod:`.Term_UK_A`, and its notes state
only the CI-specific deltas. Two of those deltas change the model rather than a
parameter, and both are the notes' own first-listed pitfalls:

* the insured event is *death or first CI diagnosis, whichever first*, so the two rates
  cannot simply be added — the combined decrement nets out an overlap factor ``k``; and
* the additional-payment and children's benefits are **non-depleting and
  non-terminating**: they neither reduce the sum assured nor decrement the in-force.

**Spaces.** The model contains two:

:mod:`~.CI_UK_S.Data`
    Reads the three input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.CI_UK_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.CI_UK_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps, unlike the annual :mod:`.Term_UK_A` it inherits
from. The contract has no accumulation account and nothing in it needs monthiversary
processing; the notes choose monthly for parity with the rest of the library, and it is
what makes the 14-day survival period and the 5-yearly premium reviews expressible.
Policy month ``t`` runs 1, 2, ..., ``proj_len()``, where ``proj_len() = 12 x term``.
Premiums and maintenance expense fall at the beginning of the month; claims and
decrements at the end; lapses act on non-claiming survivors, claim before lapse. The
initial expense falls at ``t = 1``. Cover expires at the end of the term with no
maturity or surrender value.

**What is sourced and what is not.** The benefit structure is sourced: the accelerated
design, the additional-payment benefit at ``min(25% of SA, £25,000)``, children's cover
at ``min(50% of SA, £25,000)``, both non-depleting, the 14-day survival period, the
absence of any surrender value, and the 5-yearly review cycle of the reviewable
variant. Every rate is a standardization. The CMI's accelerated-CI diagnosis tables
(AC04, the "16" Series) are restricted to subscribers, so the diagnosis and mortality
rates shipped here are **[std]** proxies shaped like those tables and no more, and the
£55 monthly premium is a placeholder — no UK insurer publishes CI rate cards. **This
model is a mechanics demonstration, not a pricing or reserving result.** Profitability
conclusions drawn from it are meaningless; replace the basis with licensed tables and
company data first.

**Model points.** Seven: the anchor cell, the standalone variant, the reviewable
variant, an indexed policy, one without children's cover, a female smoker on a shorter
term, and a joint first-event policy. Model point 1 is the anchor cell of the worked
example in the technical notes.

**Verification.** ``tests/test_critical_illness_uk.py`` asserts the notes' three-month
worked example to the penny and the in-force column to six decimals, the combined
decrement arithmetic, and that the non-terminating benefits neither deplete the sum
assured nor decrement the in-force.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/critical_illness/CI_UK_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "CI_UK_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

