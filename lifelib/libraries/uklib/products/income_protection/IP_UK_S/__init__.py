# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for UK individual income protection.

:mod:`~.IP_UK_S` is the executable counterpart of
``products/income_protection/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single-policy model point of
full-term guaranteed-premium own-occupation income protection: a monthly income benefit
payable in arrears after a deferred period, escalating in claim, ceasing at recovery,
death or the policy end date.

**This is the only multiple-state model in the library.** Every other model here runs a
single in-force probability down through decrements; this one carries a **three-state**
population — healthy and active (H), sick and in claim payment (S), dead (D) — with
lapse as a further exit from H and **recovery flowing back from S to H**. That structure
is not decoration: it is the structure the CMI's own graduations use, and the reason IP
has two experience bases rather than one, claim *inception* rates out of H and claim
*termination* rates out of S.

The second structural feature is that the in-claim population is **two-dimensional**.
Termination rates depend on how long the claim has already run — 40% a year at duration
one, 5% from duration five in the shipped basis — so the model tracks ``l_S(t, z)``, the
population in claim at month ``t`` with claim duration ``z``, cohort by cohort.
Collapsing that to a single bucket with a duration-independent termination rate
materially misstates claim run-off, and is the notes' first-listed pitfall.

**Spaces.** The model contains two:

:mod:`~.IP_UK_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.IP_UK_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.IP_UK_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps, matching the monthly-in-arrears benefit. Policy
month ``t`` runs 1, 2, ..., ``proj_len()``, where
``proj_len() = 12 x (expiry_age - entry_age)``. Premiums fall at the beginning of the
month and are paid by lives in H only — premiums are waived from the start of benefit
payment. Transitions and benefit fall at the end of the month; a claim incepting at the
end of month ``t`` receives its first payment at the end of month ``t + 1``. All cover
and any claim in payment terminate at the policy end date with no value.

**Model points come in two kinds.** ``status = active`` cells start the whole population
in H; ``status = in_claim`` cells start it in S at a stated claim duration, and are the
disabled-life annuity the notes describe. An in-force portfolio needs both.

**What is sourced and what is not.** The contractual mechanics are sourced: the deferred
period menu, the two-band maximum-benefit formula, escalation capped at 10% with a x1.5
premium multiplier continuing in claim, waiver of premium from benefit start, linked
claims within 52 weeks, and expiry without value. Every rate is a standardization. The
CMI IP11 Series — claim inception rates by sex, deferred period and occupation class,
and termination rates split by recovery and death — is restricted to CMI Authorised
Users, so the inception, recovery and in-claim mortality rates shipped here are **[std]**
proxies shaped like IP11 and carry no CMI authority, and the premium is a placeholder.
**This model is a mechanics demonstration, not a pricing or reserving result.** Replace
the basis with licensed tables before drawing any conclusion from the output.

**Verification.** ``tests/test_income_protection_uk.py`` asserts the notes' three-month
claims-in-payment worked example to the penny, including its present values, and the
month-one active-lives figures alongside it.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/income_protection/IP_UK_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "IP_UK_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

