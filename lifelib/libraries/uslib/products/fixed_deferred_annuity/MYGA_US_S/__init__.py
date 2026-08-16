# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. fixed deferred annuities (MYGA).

:mod:`~.MYGA_US_S` is the executable counterpart of
``products/fixed_deferred_annuity/technical-notes.md`` in the lifelib-products
library. It projects gross liability cash flows for a single-contract model point of a
single-premium, book-value multi-year guaranteed annuity: one purchase payment credited
in full, an insurer-declared effective annual rate guaranteed for a five-year period, a
declining surrender charge, a 10% annual free-withdrawal allowance, a two-sided market
value adjustment, and underneath all of it the NAIC Model #805 minimum guaranteed
surrender value.

This is the **deferred annuity base chassis** of the library. The fixed-indexed annuity,
variable annuity and registered index-linked annuity notes reference the surrender
benefit composition order and the Model #805 floor construction specified here.

**Spaces.** The model contains two:

:mod:`~.MYGA_US_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.MYGA_US_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.MYGA_US_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Monthly steps. ``t`` counts **policy months**, ``t = 1, 2, ...,
proj_len()``, and the contract year is ``policy_year(t) = ceil(t / 12)``, so
anniversaries fall at ``t = 12, 24, ...``. Note the contrast with :mod:`.Term_US_A`,
where ``t`` counts **years**: monthly is the coarsest grid that hits every contract
anniversary exactly while still resolving the guarantee-period-end window and the
shock-lapse boundary to within one step **[std]**.

The month's processing order follows the technical notes exactly. At the beginning of
the month (BOM): roll the free-withdrawal counters; apply the guarantee-period boundary
(the 30-day window, the rate redeclaration and, under ``rollover``, a fresh surrender
charge and MVA schedule); take the elective withdrawal, giving ``av_pp_at(t,
"BEF_INV")``; take annuitization elections — valued on that same pre-crediting account
value, because the notes place the election at BOM while naming the post-crediting
``SV(t)`` for the transfer, and the two cannot both hold on a monthly grid **[std]**;
update the IRC 72 tax basis. At the end of
the month (EOM): credit interest, giving ``av_pp(t)``; roll the Model #805 floor
``mgsv_pp(t)``; and apply decrements in the order annuitization, mortality, surrender
**[std]**, with every decrement benefit valued on the post-crediting account value.

``t = 0`` is the issue instant. The single premium, the acquisition commission and the
premium tax all fall there, as they do in the notes' cash flow ledger, and ``av_pp(0)``,
``mgsv_pp(0)`` and ``pols_if(0)`` are the initial branches of the three recursions.
``result_cf()`` therefore starts at ``t = 0``, not at ``t = 1``.

``pols_if(t)`` is the count in force at the **start** of month ``t``, the library-wide
convention (``pols_if(1) == pols_if_init()``, as in :mod:`.Term_US_A`), and it is the
weight applied to that same month's cash flows, so the ``pols_if`` column of
``result_cf()`` reconciles with the row it sits on. The technical notes' end-of-month
``l(t)`` is unchanged and is read as ``pols_if_at(t, "AFT_DECR")``. Likewise
``lapse_rate(t)`` is the **annual** total surrender rate and ``lapse_rate_mth(t)`` the
monthly one, pairing as ``mort_rate`` / ``mort_rate_mth`` do.

``proj_len()`` is ``12 * (maturity_age - age_at_entry())`` months, running to the
contract anniversary at attained age 100 **[std]** — the last attained age in the sourced
cap band on the renewal surrender charge, tabulated as 4% at 94 down to 0% at 98-100
[S1][S2]. The cap *reaches* zero at 98; 100 is where the sourced band stops, which is why
it is the horizon. The technical notes state no projection horizon; the choice is the
model's, and the survivors at that point are annuitized out through ``pols_maturity()``
so the in-force roll-forward closes.

**Undiscounted.** Like every model in this library, this one projects *gross liability
cash flows* only. Reserves and discounting are a separate layer; the notes' Valuation and
reserve pointers section cites VM-22, A-820/AG 33 and IRC 807 rather than reproducing
them. The contractual discounting that lives *inside* a benefit formula — the geometric
MVA factor — is part of the product and stays.

**What is sourced and what is not.** The contractual elements come from the composite
specimen: the 4.45% initial declared rate, the 0.25% GMIR and the 2.80% GMSV rate [S11];
the 9/8/7/6/5 initial surrender charge schedule and the 10% free-withdrawal allowance
[S10]; the 5/4/3/2/1 renewal schedule and its attained-age cap [S1][S2]; the linear
duration MVA and its application base [S8][S9]; the symmetric cap at the surrender charge
[S2]; the 30-day guarantee-period-end window [S1][S2][S5][S6]; the death benefit at full
account value [S1][S2][S13]; and the Model #805 construction — 87.5% of gross
consideration accumulated at the contract GMSV rate, with the indexed statutory rate
floored at **15 basis points, not 1%** [R1 4.A, 4.B]. The prescribed base lapse table and
the dynamic lapse functional form are VM-22 [R2 6.B.5].

Everything behavioural and expense-related is a standardization: the mapping of VM-22
Table 6.5 onto a five-year architecture, the 1.0% annuitization take-up at each window,
the 0% partial withdrawal base run, the 2.00% acquisition commission, the $50 per contract
per year maintenance expense inflating at 2.5%, the 0% premium tax, the 0.35 best-estimate
MVA factor on dynamic lapse, the exogenous reference-yield and competitor-rate scenarios,
the illustrative mortality table, and the attained age 100 projection horizon.
**This model is a mechanics demonstration, not a pricing or reserving result.** Replace
the assumption tables with company data before drawing any conclusion from the output.

**Not implemented.** Named here so the gaps cannot be mistaken for oversights.
The RMD module (the notes give the charge and MVA exemption but no RMD amount formula);
the nursing-home and terminal-illness waiver withdrawals (no incidence basis is given);
the VM-22 Table 6.2 age-banded partial-withdrawal rates (the retrieved table is the
Qualified column only and its 80-and-over row was truncated, and the notes say not to
present it as a non-qualified assumption); the ``greatest_of`` free-withdrawal rule (the
notes describe it but give no formula); the gross-up solve for a contract promising a
stated net check (``wd_pp`` is gross by construction); the Model #805 section 6 paid-up
annuity leg (noted but not implemented in the notes themselves); and ``check_margin()``,
because the product carries no contract charges and the model projects no asset side, so
the notes define no margin decomposition to check. ``check_av_roll_fwd()`` and
``check_pols_roll_fwd()`` *are* implemented — no argument, returning a bool over every
projected month, with the signed per-month residual under
``check_av_roll_fwd_resid(t)`` / ``check_pols_roll_fwd_resid(t)``. Stochastic scenario
generation is out
of scope: the reference yield and competitor rate are read from a deterministic scenario
table.

**Model points.** ``model_point_table.csv`` carries seven contracts on the same anchor
cell — male 60 ANB, non-qualified, $100,000 single premium, 5-year guarantee period —
that differ only in the switches the technical notes make first-class parameters, because
the cross-carrier divergence in those switches is the notes' own headline finding. Point 1
is the worked example anchor; point 2 repeats it under the stress reference yield that
forces the symmetric cap and the nonforfeiture floor to bind; points 3 to 7 carry the
Camp B annual-redeclaration architecture, the registered-contract conventions, the Midland
conventions, the asymmetric cap and the declared-differential MVA. Between them they
exercise all three MVA families, all five cap rules, both renewal architectures, both
Model #805 withdrawal conventions and both free-withdrawal rules, so no branch of the
notes' parameter set is dead code. A test asserts every point projects.

**Verification.** ``tests/test_fixed_deferred_annuity_us.py`` asserts every row and column
of the notes' worked example table (all seven months, money to the cent), both surrender
traces line by line including the capped MVA and the binding Model #805 floor, the
geometric branch factors from the Nationwide contract, the in-force and account value
roll-forwards, and one test per entry in the notes' Known modeling pitfalls list.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/fixed_deferred_annuity/MYGA_US_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "MYGA_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

