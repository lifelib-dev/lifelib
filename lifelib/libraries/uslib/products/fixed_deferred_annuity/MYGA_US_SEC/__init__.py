# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. fixed deferred annuities (MYGA).

:mod:`~.MYGA_US_SEC` projects the contracts :mod:`~.MYGA_US_S` projects — a
single-contract model point of a single-premium, book-value multi-year guaranteed
annuity: one purchase payment credited in full, an insurer-declared effective annual rate
guaranteed for a five-year period, a declining surrender charge, a 10% annual
free-withdrawal allowance, a two-sided market value adjustment, and underneath all of it
the NAIC Model #805 minimum guaranteed surrender value — from a **valuation date** rather
than from issue. A model point may be a contract already in force at that date, in any
month of its contract year, one issued at it, or one to be issued in the ten years after
it, as in lifelib's ``basiclife/BasicTerm_SE``, which extends ``basiclife/BasicTerm_S``
the same way. Its formulas are the executable counterpart of
``products/fixed_deferred_annuity/technical-notes.md``, and
``products/fixed_deferred_annuity/model-sec.md`` explains what running in force changes
and how the model compiles.

This is the **deferred annuity base chassis** of the library. The fixed-indexed annuity,
variable annuity and registered index-linked annuity notes reference the surrender
benefit composition order and the Model #805 floor construction specified here.

**Spaces.** The model contains two:

:mod:`~.MYGA_US_SEC.Data`
    Reads the six assumption CSVs it shares with :mod:`~.MYGA_US_S` and its own model
    point table, and holds their filename References. It takes no parameters, so each
    file is read **once per model**, and it holds the model point table and the tables as
    numbers, one element per model point, per scenario, per programme, per schedule or
    per age.

:mod:`~.MYGA_US_SEC.Projection`
    The by-contract projection, parameterized by ``idx``, the position of a model point
    in the ``Data`` vectors, as ``basiclife.BasicTerm_SC`` is: ``Projection[0]`` is an
    ItemSpace projecting the table's first row, model point 1, and its ``point_id()`` is
    that label. It reaches the inputs through its ``data`` Reference, which resolves to
    the single :mod:`~.MYGA_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Compiled.** The model compiles under modelx-cython into C-typed code, as
``basiclife/BasicTerm_SC`` does, from the two inputs beside it: ``sample_sec.py``, the run
that types each cell, and ``spec_sec.py``, the length of each cell's cache.
``Projection``'s cells read every model point attribute a projection cell uses as a C
number from a ``Data`` vector at ``idx``, and every table, the rate scenario and the
withdrawal programmes among them, as an array indexed by integers; a timing, a kind, a
scenario column and a surrender schedule are int codes; and every cell but the reports,
``model_point``, the ten label accessors and the three cells kept as ``MYGA_US_S`` wrote
them, which no projection cell calls, returns a C ``bint``, ``long long`` or ``double``,
cached as a single value or in a C array sized from the contract. modelx reads and runs
the same formulas, and computes the same numbers.
``products/fixed_deferred_annuity/model-sec.md`` says how to compile and run it, and what
the compiled model does not do as modelx does: it clears no cache when a Reference is set,
so every Reference is set on a model just imported.

**Projection basis.** Monthly steps on two clocks. ``t`` counts months from the valuation
date, 0-based, as ``basiclife/BasicTerm_SE`` counts them: ``t = 0`` is the valuation
month for every model point, however old the contract, month ``t`` runs from time ``t``
to time ``t + 1``, and the frame runs ``t = 0, 1, ..., proj_len() - 1``, where
``proj_len()`` counts the months from the valuation date to the deemed maturity at
attained age 100. ``duration_mth(t)`` counts the months the contract has been in force,
``duration_mth_init() + t`` from the model point's ``duration_mth`` at ``t = 0``, and the
contract runs on it: the contract year ``policy_year(t) = duration_mth(t) // 12 + 1``,
whose anniversaries fall at the start of the months where ``duration_mth(t)`` is a
multiple of 12, the guarantee periods and their 30-day windows, the surrender charge
schedules, the MVA term, the base lapse years and the scheduled withdrawals. Monthly is
the library-wide grid, and for this product it is also the coarsest one that hits every
contract anniversary exactly while still resolving the guarantee-period-end window and
the shock-lapse boundary to within one step **[std]**. The rate scenario and expense
inflation run on ``t`` instead, shared by every point of a block; acquisition is charged
per contract issued, in the issue month, and is not inflated, as in
``basiclife/BasicTerm_SE``. On a point issued at ``t = 0`` the two clocks coincide, and
the model computes what :mod:`~.MYGA_US_S` computes.

The month's processing order follows the technical notes exactly. At the beginning of
the month (BOM): roll the free-withdrawal counters; apply the guarantee-period boundary
(the 30-day window, the rate redeclaration and, under ``rollover``, a fresh surrender
charge and MVA schedule); take the elective withdrawal, giving ``av_pp_at(t,
BEF_INV)``; take annuitization elections — valued on that same pre-crediting account
value, because the notes place the election at BOM while naming the post-crediting
``SV(t)`` for the transfer, and the two cannot both hold on a monthly grid **[std]**;
update the IRC 72 tax basis. At the end of the month (EOM): credit interest, giving
``av_pp(t)``; roll the Model #805 floor ``mgsv_pp(t)``; and apply decrements in the order
annuitization, mortality, surrender **[std]**, with every decrement benefit valued on the
post-crediting account value.

**The opening state.** The issue instant is not a row. A contract's single premium, its
acquisition commission and its premium tax are beginning-of-month flows of its issue
month — the notes' "at ``t = 0``" — and :mod:`~.MYGA_US_S`'s issue values are credited
there by their rules: the premium credited, ``P (1 - load)``, to the account value, and
87.5% of gross consideration to the Model #805 floor. A contract in force at the
valuation date opens instead from ten columns of its row, per contract, as it stands at
the start of month 0, before any month-0 event: the account value, the floor and
``P_accum@GMIR`` entering month 0; the interest credited to date, and to the anniversary
that opened the contract year under way; that year's free-withdrawal allowance and the
part of it unused; the IRC 72 basis; and the declared rate and the MVA reference yield
``i0`` in force, fixed in the past where the redeclaration or the start of the guarantee
period precedes the valuation date. Each is exactly what :mod:`~.MYGA_US_S` carries into
the month the contract is valued at. ``result_cf()`` has exactly ``proj_len()`` rows,
``t = 0 .. proj_len() - 1``, and row ``t`` is the same month on every point.

``pols_if(t)`` is the count in force at the **start** of month ``t``, after the month's
new business — ``pols_if_at(t, BEF_DECR)``, the library-wide convention, as in
:mod:`.Term_US_S` — and it is the weight applied to that same month's cash flows, so the
``pols_if`` column of ``result_cf()`` reconciles with the row it sits on. A point in force
at the valuation date opens with its ``policy_count``, and one issued at or after it takes
its ``policy_count`` as ``pols_new_biz`` in its issue month; ``result_pols()`` sets the
counts out. The technical notes' end-of-month ``l(t)`` is unchanged and is read as
``pols_if_at(t, AFT_DECR)``. Likewise ``lapse_rate(t)`` is the **annual** total
surrender rate and ``lapse_rate_mth(t)`` the monthly one, pairing as ``mort_rate`` /
``mort_rate_mth`` do.

Cover runs to the contract anniversary at attained age ``maturity_age`` = 100 **[std]**,
policy month ``maturity_mth() = 12 * (maturity_age - age_at_entry())`` — the last attained
age in the sourced cap band on the renewal surrender charge, tabulated as 4% at 94 down to
0% at 98-100 [S1][S2]. The cap *reaches* zero at 98; 100 is where the sourced band stops,
which is why it is the horizon. The technical notes state no projection horizon; the
choice is the model's, and the survivors at that point are annuitized out through
``pols_maturity()`` so the in-force roll-forward closes.

**Undiscounted.** Like every model in this library, this one projects *gross liability
cash flows* only. Reserves and discounting are a separate layer; the notes' Valuation and
reserve pointers section cites VM-22, A-820/AG 33 and IRC 807 rather than reproducing
them. The contractual discounting that lives *inside* a benefit formula — the geometric
MVA factor — is part of the product and stays.

**What is sourced and what is not.** The contractual elements come from the composite
specimen: the 4.45% initial declared rate, the 0.25% GMIR and the 2.80% GMSV rate [S11];
the 9/8/7/6/5 initial surrender charge schedule and the 10% free-withdrawal allowance
[S10]; the 5/4/3/2/1 renewal schedule [S2] and its attained-age cap [S1] [S2]; the
linear duration MVA and its application base [S8] [S9]; the symmetric cap at the surrender
charge [S2]; the 30-day guarantee-period-end window [S1] [S2] [S5] [S6]; the death benefit
at full account value [S1] [S2] [S13]; and the Model #805 construction — 87.5% of gross
consideration accumulated at the contract GMSV rate, with the indexed statutory rate
floored at **15 basis points, not 1%** [R1 4.A, 4.B]. The prescribed base lapse table and
the dynamic lapse functional form are VM-22 [R2 6.B.5].

Everything behavioural and expense-related is a standardization: the mapping of VM-22
Table 6.5 onto a five-year architecture, the 1.0% annuitization take-up at each window,
the 0% partial withdrawal base run, the 2.00% acquisition commission, the $50 per contract
per year maintenance expense inflating at 2.5%, the 0% premium tax, the 0.35 best-estimate
MVA factor on dynamic lapse, the exogenous reference-yield and competitor-rate scenarios,
the illustrative mortality table, and the attained age 100 projection horizon. Running in
force changes none of them: the six assumption tables are :mod:`~.MYGA_US_S`'s, read in
place. **This model is a mechanics demonstration, not a pricing or reserving result.**
Replace the assumption tables with company data before drawing any conclusion from the
output.

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
generation is out of scope: the reference yield and competitor rate are read from a
deterministic scenario table.

**Model points.** ``model_point_table_sec.csv`` is generated from :mod:`~.MYGA_US_S` and
its model point table, and the tests regenerate it and compare, so no row is typed by
hand. Points 1 to 7 are the twins of :mod:`~.MYGA_US_S`'s seven contracts, issued at the
valuation date: the worked example's anchor cell — male 60 ANB, non-qualified, $100,000
single premium, 5-year guarantee period — and its six variants on the switches the
technical notes make first-class parameters, which between them exercise all three MVA
families, all five cap rules, both renewal architectures, both Model #805 withdrawal
conventions and both free-withdrawal rules. Points 8 to 13 are S points restated in force
at an S month, each opened with the state S carries into that month: the anchor on its
first anniversary, month 12, where its $4,000 withdrawal is free under the year's
allowance; the interest-only, net-of-charges point at month 30, the month after its
excess withdrawal; the Camp B point at month 30, inside its initial term, carrying the
premium accumulated at the GMIR that its floored MVA reads; the registered-contract point
at month 60, in the 30-day window, where the rate is redeclared and ``i0`` re-locked; the
stress trace at month 61, in its first renewal period, whose rate and ``i0`` were fixed
the month before; and the Camp B point at month 479, its last covered month. Point 14 is
the anchor issued 15 months after the valuation date. A test asserts that every point in
the table projects.

**Verification.** On the seven twins issued at the valuation date every cell this model
shares with :mod:`~.MYGA_US_S` agrees with it at every argument the S model evaluates in
its sweep, ``pols_if_init``, ``model_point``, ``av_pp_init``, ``mgsv_pp_init``,
``result_pols``, and the three S cells it writes otherwise, ``mva_pp_on``,
``mva_factor_geometric`` and ``surr_charge_id``, excepted, S's ``claims(t, None)`` and
``claims_over_av(t, None)`` compared as ``(t, ALL)``, so every golden
``tests/test_fixed_deferred_annuity_us.py`` asserts on a cell that sweep reaches — the
worked example's table, both surrender traces line by line and the roll-forwards — holds
here too, with no number restated;
``tests/test_model_conventions.py`` asserts it.
``tests/test_fixed_deferred_annuity_us_sec.py`` splices: an S point restated in force at
month ``d``, opened with S's own state there, continues the S projection from ``d`` on,
cell by cell, the statutory nonforfeiture rate, which no report reads, among them; a point
issued ``k`` months late is the S projection ``k`` months on; and the committed table is
what S generates.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/fixed_deferred_annuity/MYGA_US_SEC")
    >>> model.Projection[7].result_cf()     # model point 8, the table's eighth row
"""

from modelx.serialize.jsonvalues import *

_name = "MYGA_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
