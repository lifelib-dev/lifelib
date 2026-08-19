# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for UK whole of life assurance.

:mod:`~.WOL_UK_S` is the executable counterpart of
``products/whole_of_life/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for single-policy model points of the
two cells those notes specify, which share one engine:

**RefWOL-UW** — underwritten guaranteed whole of life. Full underwriting, guaranteed
level premiums payable for life, the sum assured paid once on death or earlier terminal
illness, suicide inside twelve months refunding premiums instead.

**RefWOL-O50** — over-50s guaranteed acceptance. No underwriting at all, a fixed cash
sum, a **twelve-month moratorium** during which non-accidental death returns the
premiums paid rather than the cash sum, premiums ceasing at the anniversary on or after
the 90th birthday while cover continues, and a **crossover** past which cumulative
premiums exceed the cash sum.

**Neither cell has an account value, a unit fund or a surrender value.** Both are pure
decrement protection models: premiums in, death benefits and expenses out, weighted by
survivorship. That is the deliberate contrast with :mod:`.WholeLife_US_A`, the U.S.
whole life model in the same library, which is built around a guaranteed cash value
schedule, three-factor dividends, paid-up additions and policy loans. None of that
machinery exists here, and a lapse on either UK cell pays exactly nothing.

The arithmetic consequence is the product's defining economics: **every lapse
extinguishes a liability for nothing**. The FCA records that without the
continuing-payer cross-subsidy insurers would need to rely on lapses to remain
profitable, so the best estimate falls as assumed lapses rise — which makes lapse the
assumption to govern hardest, and makes one plan's *pro-rata paid-up value* variant [S9], which
converts late lapses into paid-up liabilities instead of forfeitures, a different
product rather than a small adjustment.

**Spaces.** The model contains two:

:mod:`~.WOL_UK_S.Data`
    Reads the three input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.WOL_UK_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.WOL_UK_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps. Policy month ``t`` runs 1, 2, ..., ``proj_len()``,
where ``proj_len() = 12 x (omega_age - entry_age)``: whole of life has no maturity, so
the projection is truncated at a limiting age rather than ending at a contractual date.
Premiums and expenses fall at the beginning of the month; deaths at the end, against the
beginning-of-month in-force; lapses at the end after deaths. Escalation steps at policy
anniversaries. Age is **age last birthday**, unlike every other model in this library —
the underwritten cell's specimen defines entry age that way.

**What is sourced and what is not.** The contractual mechanics are sourced: the
moratorium and its return-of-premiums benefit, accidental death paying the full cash sum
from day one, premium cessation at 90 with cover continuing, the absence of any
surrender value, the suicide clause, the escalation ratios and the pro-rata paid-up value
formula. Every rate is a standardization. The CMI's current tables are restricted to
Authorised Users, so the two mortality bases shipped here are **[std]** proxies shaped
like the tables the notes name, and no insurer publishes premium rate tables, so the
premium is a model point input. **This model is a mechanics demonstration, not a pricing
or reserving result.** Replace the basis with licensed tables and company experience
first.

**Verification.** ``tests/test_whole_of_life_uk.py`` asserts the notes' eleven-row
worked example to the penny and the in-force column to five decimals, including the
month-12/13 moratorium discontinuity and the month-167 crossover.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/whole_of_life/WOL_UK_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "WOL_UK_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

