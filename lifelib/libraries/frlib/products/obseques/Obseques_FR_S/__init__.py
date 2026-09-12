# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the French contrat obseques in capital form.

:mod:`~.Obseques_FR_S` is the executable counterpart of
``products/obseques/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for single-policy model points of the three
cells those notes specify, which share one engine and differ only in the
``premium_form`` column of the model point table:

**RefOBS-VIA** — *primes viageres*, a level premium payable **for life**. The anchor
cell: entry 50, guaranteed capital 5000 EUR, 336.03 EUR a year, revalorisation 1.00 %
p.a. guaranteed. Cumulative premiums pass the original capital in policy year 15 and the
revalorised capital in policy year 18, and the contract goes on collecting premiums after
both.

**RefOBS-TMP** — *primes temporaires*, a level premium payable for a stated term, after
which the contract runs on paid-up with the cover intact.

**RefOBS-UNI** — *prime unique*, a single payment at outset: one receipt followed by four
decades of pure outgo.

Two structural features separate this product from :mod:`.WOL_UK_S`, the UK
guaranteed-acceptance over-50s cell that is otherwise almost the same contract. The
**capital is a state variable, not a constant** — it is uprated annually out of the
*participation aux benefices*, so the benefit in force compounds for the whole of a whole
life contract. And **lapse pays money**: the surrender value is the *provision
mathematique*, so ``claims_lapse`` is non-zero from the first month and the UK design's
"every lapse extinguishes a liability for nothing" arithmetic does not carry over. On the
anchor cell removing the lapse decrement *raises* the undiscounted net stream, because the
premiums a lapser stops paying are worth more than the reserve handed back.

The *delai de carence* is **two benefits, not one**. For twelve months a non-accidental
death refunds the premiums collected while an accidental death pays the full capital from
day one, so the first month's expected death outgo is 0.380884 rather than the 3.345618 an
implementation that paid the capital inside the waiting period would report — and rather
than the 0.224846 an implementation that dropped the accident leg would report. Both
errors are in the model docstring because both are eight- and four-tenths-fold wrong on
the front end of the liability.

**Spaces.** The model contains two:

:mod:`~.Obseques_FR_S.Data`
    Reads the six input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Obseques_FR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Obseques_FR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps, which the twelve-month waiting period requires: its
boundary is a discontinuity — expected death outgo steps by a factor of 7.8080 between
``t = 11`` and ``t = 12`` on the anchor cell — and an annual grid would smooth it away.
Policy month ``t`` is **0-based**: it runs 0, 1, ..., ``proj_len() - 1``, so
``proj_len()`` is the number of projected months,
``proj_len() = 12 x (omega_age - entry_age + 1)`` with ``omega_age = 112``, the tabulation
limit of TH 00-02: whole life has no maturity, so the projection is truncated at a
limiting age rather than ending at a contractual date. The policy year is the contractual
1-based label derived from it, ``policy_year(t) = t // 12 + 1``, and is what the premium,
lapse and select schedules are keyed by. Premiums fall at the beginning of
the month, deaths at the end against the beginning-of-month in-force, surrenders and
*reductions* at the end after deaths. The capital, the premium and the attained age step
at policy anniversaries. Age is the *difference de millesime* — calendar year of
subscription less calendar year of birth — incremented at the anniversary rather than on
1 January, which is exact for January issues.

**What is sourced and what is not.** The contractual mechanics are sourced: the
twelve-month waiting period and its two benefits, the refund of premiums *collected*
rather than accrued, the 1.00 % guaranteed revalorisation of the capital and the
first-anniversary eligibility for it, the surrender value equal to the *provision
mathematique*, *reduction* to a paid-up capital on non-payment, the surrender-value and
single-premium scales, and the premium of every cell. Every **rate** is a
standardization. TH 00-02 / TF 00-02 are regulatory tables cited by name and never
redistributed, so the mortality shipped here is an INSEE-shaped **[std]** proxy anchored
so that the anchor cell's best-estimate factor is the notes' placeholder rate exactly,
and no public French source gives any lapse, surrender or paid-up rate for this product
at all. **This model is a mechanics demonstration, not a pricing or reserving result.**
Replace the basis with homologated tables and company experience first.

**Verification.** ``tests/test_obseques_fr.py`` asserts the notes' fifteen-row worked
example to the cent and the in-force column to five decimals, including the *carence*
discontinuity between ``t = 11`` and ``t = 12``, the two crossovers at ``t = 168`` and
``t = 204``, and the undiscounted totals over the full 756-month horizon.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/obseques/Obseques_FR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Obseques_FR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
