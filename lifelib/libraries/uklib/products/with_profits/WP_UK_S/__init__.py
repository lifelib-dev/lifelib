# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for UK with-profits business.

:mod:`~.WP_UK_S` is the executable counterpart of
``products/with_profits/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for single-policy model points on the
two composite chassis those notes specify — a **unitised with-profits bond** and a
**conventional with-profits endowment** — through the machinery that makes with-profits
what it is: a retrospective asset share, an annually declared bonus that hardens into a
guarantee, a smoothed payout inside a target corridor, a market value reduction on
non-guaranteed exits, and a 90:10 shareholder transfer.

**The asset share is a state variable, not a cash flow.** That sentence is the model.
The policy's cash flows are premiums, claims, withdrawals, expenses and shareholder
transfers; the asset share is a *shadow* retrospective accumulation that nobody owns and
nobody is paid, and it drives claim amounts only through the bonus, smoothing and MVR
rules. The difference between what is paid and what the asset share says is absorbed by
the estate.

That makes this the one product in the library with **no account value in the library's
sense**. There is no ``av_pp_at`` here: the asset share is not a policyholder fund, and
the guaranteed benefit — a unit face value on the bond chassis, a sum assured plus
attaching reversionary bonuses on the endowment — is not a fund either. Both are
modelled, under their own names, and the gap between them is where the whole product
lives.

**Spaces.** The model contains two:

:mod:`~.WP_UK_S.Data`
    Reads the three input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.WP_UK_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.WP_UK_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps, with the bonus declaration left on its annual
cycle. The time index ``t`` is **0-based** and counts policy months from issue:
``t = 0`` is the issue month, month ``t`` runs from time ``t`` to time ``t + 1``, the
contractual policy year containing it is the 1-based label ``t // 12 + 1``, and the
attained age is ``age_at_entry() + t // 12``, advancing on the anniversary. An in-force
model point opens its frame at its elapsed months, ``proj_start() =
12 x duration_inforce()``, and carries its state in as the opening balances of that
month; ``proj_len()`` is the number of policy months projected from issue, so the frame
is ``range(proj_start(), proj_len())``. Premiums and partial withdrawals fall at the
start of the month; the fund return accrues over it; charges, the shareholder transfer
and the mortality charge fall at the end, in that order; claims and decrements follow.
Age is age nearest birthday.

**The declaration stays annual, and that is the point.** The bonus declaration is the
governing act of discretion on this product, it happens once a policy year, and it
permanently hardens the guarantee. So it fires in the twelfth month of each policy year
and nowhere else: the unit price and the guaranteed benefit are step functions, flat for
eleven months and stepping in the twelfth, and the cost of bonus and the shareholder
transfer are nil in those eleven. Everything continuous — the fund return, the annual
management and guarantee charges, the mortality charge, the decrements, the smoothed
payout, the final bonus and the market value reduction — runs monthly around it. Annual
assumptions are converted with the effective ``(1 + r)^(1/12)`` and
``1 - (1 - r)^(1/12)`` forms, including the smoothing cap, whose twelfth root keeps the
notes' ±10% year-on-year discipline intact. ``check_declaration_is_annual`` asserts the
cycle, because compounding an annual bonus rate twelve times a year is a failure that
leaves every roll-forward closing and the guarantee an order of magnitude too large.

What the monthly grid buys is the **guarantee date**. An exit in a guarantee-date month
is MVR-free and an exit in the other eleven months of the same policy year is not, and
the anti-selective encashment that follows is a dated exercise rather than a year-long
elevation of the surrender rate. That last change moves an assumption's shape and not
only its frequency; ``guarantee_exercise`` says so in its own docstring.

**What is deterministic, and what that costs.** This is a deterministic
single-scenario projection, and the notes are emphatic that a deterministic base run
**materially understates the cost of guarantees**, because guarantee cost is convex in
the fund return. The model produces exactly the per-scenario cash flows a
market-consistent stochastic valuation consumes; the stochastic layer is out of scope
and the ``c_g`` charge in the asset share recursion is a *charging* proxy, not a
valuation of anything.

**What is sourced and what is not.** The mechanics are sourced: the asset share item
list and its regulatory codification, bonus hardening, the unit-price floor, the
guarantee-date and death MVR exemptions, the MVR's contractual bound, the target
corridor, the smoothing cap, the lifetime guarantee-charge cap and the 90:10 split.
Every *rate* is a standardization: bonus declarations are not published in the
principles and practices documents, no MVR scale is public, the CMI's tables are
restricted to Authorised Users, and no UK with-profits lapse experience was retrieved.
**This model is a mechanics demonstration, not a pricing or reserving result.**

**Verification.** ``tests/test_with_profits_uk.py`` asserts both scenarios of the
notes' worked example step by step to the penny — the asset share recursion, the bonus
cost and shareholder transfer, the mortality charge, the smoothing cap and corridor,
the final bonus, the MVR and its regulatory bound, and all three payout bases.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/with_profits/WP_UK_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "WP_UK_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

