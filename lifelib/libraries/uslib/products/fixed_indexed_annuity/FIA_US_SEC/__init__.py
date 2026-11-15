# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. fixed indexed annuities (GLWB).

:mod:`~.FIA_US_SEC` projects the contracts :mod:`~.FIA_US_S` projects from a **valuation
date** rather than from issue. Each is a single-contract model point of a single-premium
fixed indexed annuity carrying a guaranteed lifetime withdrawal benefit: a 7% premium
bonus vesting over ten years, one annual point-to-point indexed account credited at
``max(0%, min(cap, index return))``, a notional benefit base growing by a guaranteed
simple rollup **plus** 150% of realised dollar credits, a 0.95% rider charge on that base,
a lifetime withdrawal locked at the attained age of first exercise, and — the economic
centre of the product — a guaranteed income stream that survives account-value exhaustion
and pays for life. A model point may be a contract already in force at that date, in any
month of its contract year and in any phase, one issued at it, or one to be issued in the
ten years after it, as in lifelib's ``basiclife/BasicTerm_SE``, which extends
``basiclife/BasicTerm_S`` the same way. Its formulas are the executable counterpart of
``products/fixed_indexed_annuity/technical-notes.md``, and
``products/fixed_indexed_annuity/model-sec.md`` explains what running in force changes.

The base contract is the deferred annuity chassis of
:mod:`.MYGA_US_S`: the surrender-benefit composition order and the NAIC
Model #805 floor construction are the chassis's. **Everything else here is restated by
the FIA notes with its own parameters and must not be carried across from the chassis** —
the account-value roll-forward is index-credit driven rather than interest-accretion
driven, the MVA is the ratio form ``[(1+i0)/(1+it)]^(n/12) - 1`` rather than the linear
``(i0 - it) x T``, the death benefit is ``max(AV, MGV)``, and the lapse architecture is
rider-suppressed rather than a plain shock at surrender-charge expiry. The chassis's
``MGSV`` and these notes' ``MGV`` are **one quantity under two source labels**; this
model uses the chassis name :func:`~.FIA_US_SEC.Projection.mgsv_pp`
throughout.

**Spaces.** The model contains two:

:mod:`~.FIA_US_SEC.Data`
    Reads the five assumption CSVs it shares with :mod:`~.FIA_US_S`, its own model point
    table and its own rate scenarios, and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.FIA_US_SEC.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.FIA_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Monthly steps on two clocks. ``t`` counts months from the valuation
date, 0-based, as ``basiclife/BasicTerm_SE`` counts them: ``t = 0`` is the valuation
month for every model point, however old the contract, month ``t`` runs from time ``t``
to time ``t + 1``, and the frame runs ``t = 0, 1, ..., proj_len() - 1``, where
``proj_len()`` counts the months from the valuation date to the end of cover.
``duration_mth(t)`` counts the months the contract has been in force,
``duration_mth_init() + t`` from the model point's ``duration_mth`` at ``t = 0``, and the
contract runs on it: ``duration(t) = duration_mth(t) // 12`` is the completed contract
years, ``policy_year(t) = duration(t) + 1`` the contractual label, and the anniversary
month, where every contractual event lands, the one with ``duration_mth(t) % 12 == 11``.
The surrender charge, the vesting, the rollup schedule, the growth window, the MVA term,
the shock-lapse year, the withdrawal programme, the payout bands and the mortality read
that clock. The rate scenario and expense inflation run on ``t`` instead, shared by every
point of a block: the index level and the MVA reference yield are read at the valuation
month each anniversary falls in, and maintenance expense is in valuation-date dollars. On
a point issued at ``t = 0`` the two clocks coincide, and the model computes what
:mod:`~.FIA_US_S` computes.

**Every mechanic of the contract is still annual.** Annual point-to-point crediting
[S2][S4][S10], the rider charge at the end of each contract year [S9], the benefit base
update [S9] and the lifetime withdrawal are all annual, and the notes make the anniversary
the single event date — so each of them happens once a year, in the **anniversary month**
``is_anniv(t)``, and the contract moves no cash between anniversaries. What the finer grid
resolves is everything that is not a contractual event: mortality and surrender fall in the
month they happen, the Model #805 floor and the fixed account accrue month by month so a
mid-year death or surrender is valued on the balance it actually has, and maintenance
expense accrues where it is incurred. The excluded variants stay excluded — monthly-sum
crediting, one carrier's monthly charge deduction, daily interim values, mid-year
withdrawal crediting are all still absent, and the indexed account is deliberately flat
between anniversaries.

Because the monthly decrement rates compound to the annual ones and every contractual step
is unmoved, **every state value at an anniversary equals the annual-step model's**: account
value, benefit base, rollup base, lifetime withdrawal, Model #805 floor, phase and
``pols_if`` in the month opening each contract year. The cash differs, and that is the
point — ``result_cf_annual()`` sums the monthly frame into contract years and agrees
exactly on ``pols_if``, ``premiums``, ``commissions`` and ``premium_taxes``, but not on the
withdrawals, the claims or the expenses.

``age(t) = age_at_entry() + duration(t)`` is the attained age opening the contract year of
month ``t``, so that year's mortality reads ``age(t)`` itself; ``mort_rate_mth(t)`` converts
it for the month. The transactions at the closing anniversary are one year older:
``exercise_age(t)`` is the age that reads the lifetime-withdrawal percentage table and
clears the minimum exercise age.

The anniversary's processing order is the notes' own, and every quantity that changes
inside it is exposed through a ``timing`` argument rather than being buried:

1. index credit and fixed interest --- ``av_pp_at(t, "BEF_FEE")``
2. rider charge on the *opening* benefit base --- ``av_pp_at(t, "BEF_WD")``
3. benefit base: rollup, stack, step-up --- ``benefit_base_pp_at(t, "BEF_WD")``
4. lifetime and excess withdrawal --- ``lw_pp_at(t, "BEF_WD")``, ``wd_pp(t)``
5. charges on the excess and the proportional reduction of the guarantee ---
   ``wd_reduction_rate(t)``, ``benefit_base_pp(t)``
6. guaranteed minimum value roll --- ``mgsv_pp(t)``
7. phase transition including the depletion test --- ``phase(t)``
8. decrements --- ``pols_if_at(t, "AFT_DECR")``

``pols_if(t)`` is the in-force count at the **start** of month ``t``, after the month's
new business — ``pols_if_at(t, "BEF_DECR")``, the library-wide convention set by
:mod:`.Term_US_S` and ``savings.CashValue_SE`` — and it is the weight carried by every
cash flow reported on the same row of ``result_cf()``. In the month opening contract year
``k + 1`` it is the technical notes' own ``l(k)``, the probability in force at the end of
contract year ``k``, and the equality is exact. At an anniversary month it is the count
that **reaches** the anniversary, which is the weight that month's withdrawal and charges
carry — where the annual grid could only weight them by the count that entered the year.
A point in force at the valuation date opens with its ``policy_count``, and one issued at
or after it takes its ``policy_count`` as ``pols_new_biz`` in its issue month;
``result_pols()`` sets the counts out.

Steps 1--3 are skipped in ``DEPLETED`` and steps 1--7 in ``TERMINATED``; step 8 is the one
that runs every month. The phase is an int code, ``ACCUM`` 1 to ``TERMINATED`` 4, with
``PRE_ISSUE`` 0 before issue and ``MATURED`` 5 after cover, and ``result_glwb()`` reports
it by its label.

**The opening state.** There is no issue-instant row: the single premium, the premium
bonus and the acquisition expense are beginning-of-month flows of the issue month, and
:mod:`~.FIA_US_S`'s issue values are credited there by their rules — ``P x (1 + b)`` to
the account value, its fixed share to the fixed account, and 87.5% of the premium, the
bonus excluded, to the Model #805 floor. A contract in force at the valuation date opens
instead from twelve columns of its row, per contract, as it stands at the start of month
0, before any month-0 event: the account value, the fixed account, the benefit base, the
rollup base, the lifetime withdrawal, the Model #805 floor and the gross withdrawals to
date entering month 0; and, at the anniversary on or before the valuation date, the one
that opened the contract year under way, the account value and the fixed account the
year's credit, fixed interest and free withdrawal are computed on, the phase as a code,
the locked payout percentage and the index level the year's segment started at. Each is
exactly what :mod:`~.FIA_US_S` carries into the month the contract is valued at, which
:mod:`~.FIA_US_S` itself can say only on an anniversary, and of which it derives the
fixed account from the allocation at issue. ``result_cf()`` has exactly ``proj_len()``
rows, ``t = 0 .. proj_len() - 1``, and row ``t`` is the same month on every point.

**Undiscounted.** Like every model in this library, this one projects *gross liability
cash flows* only; reserves and discounting are a separate layer, and the notes' own
Valuation and reserve pointers section cites AG 33, AG 35 and VM-22 rather than
reproducing them. The contractual discounting that lives *inside* a benefit formula —
the ratio-form MVA — is part of the product and stays.

**What is sourced and what is not.** The contractual elements come from the composite
specimen: the 0% index credit floor [S1][S4][S10][R1]; the 5.25% declared cap and 2.30%
fixed rate [S2] against the 0.25% guaranteed minimum cap [S4] and 1.00% guaranteed
minimum fixed rate [S10]; the 9.1%-to-0% surrender charge schedule and the 0-to-100%
bonus vesting vector [S5]; the 7% premium bonus [S5] and the ``b/(1+b)`` clawback [S10];
the 10% free withdrawal [S1][S3][S5][S6][S9][S10]; the ratio-form MVA and its
nonforfeiture collar [S10]; the 5.00%/2.00% guaranteed simple rollup [S2]; the 150%
stacking factor [S8][S9]; the 0.95% rider charge on the benefit base, deducted after
index credits [S9]; the lifetime withdrawal percentage bands [S3]; the cause-dependent
treatment of account-value exhaustion [S1][S5][S9]; and the Model #805 construction —
87.5% of premium **excluding the bonus** accumulated at a nonforfeiture rate inside the
0.15%-3% corridor, whose statutory floor is **15 basis points, not 1%** [R2][R3].

Everything behavioural and expense-related is a standardization: the anniversary-only
event date; the annual step-up (no retrieved document describes an
automatic ratchet during deferral); the 1.00% flat nonforfeiture rate inside the
corridor; the insurer-favourable reading under which the guaranteed withdrawal consumes
the free withdrawal amount; the base surrender vector 2/3/4/5/6% and the three-way shock
lapse 33%/10%/5%; the rider moneyness multiplier; the locking of the payout percentage
at first exercise; the 6.0%-of-premium acquisition expense; the $80 per contract per
year maintenance expense inflating at 2.5%; the 0% premium tax; the illustrative
mortality table; and the attained age 120 projection horizon. Two crediting parameters
belong on that list rather than on the sourced one: the notes give the index-margin and
performance-trigger *forms* but declare no level for either, so ``spread_rate`` = 2.00%
and ``trigger_rate`` = 4.50% are illustrative **[std]** levels that exercise those
branches and nothing more. The cap (5.25% [S2]) and the participation rate (80%, from
[R1]'s worked ``min(80% x 10%, 6%) = 6%``) are the sourced ones. Running in force changes
none of them: the five assumption tables are :mod:`~.FIA_US_S`'s, read in place, and the
rate scenarios are its scenarios moved onto the valuation clock.

**Exhaustion pays differently depending on its cause.** On the anniversary the account
value runs out, the withdrawal requested exceeds the balance available to meet it. In
``DEPLETED`` the insurer funds the whole shortfall, because the guarantee survives and
that stream *is* the product. On the ``TERMINATED`` branch it funds none of it: the
balance is gone and the rider that would have covered the rest was destroyed by the very
withdrawal being paid, [S5] treating the contract "as well as the rider" as surrendered
at that point. Paying the request in full on both branches would honour the guarantee in
the year the excess withdrawal kills it. The cap sits on the *payment* only — ``wd_pp``
still carries the amount requested, so the excess still sets ``depletion_cause``, still
drives the proportional reduction to 1 and still takes the benefit base to zero — and
``wd_unfunded_pp`` is the part kept out of the ledger.

**This model is a mechanics demonstration, not a pricing or reserving result.** Replace
the assumption tables with company data before drawing any conclusion from the output.

**Where the notes are silent, both readings are shipped.** The MVA collar is stated on
the *gross withdrawal* but justified as a *surrender-value* test, which the worked
example only ever exercises at a full surrender. Read literally it gives a partial
withdrawal below the nonforfeiture floor no adjustment at all; read as a test on the
contract it gives the adjustment the rate produces. ``mva_collar_basis`` selects, the two
agree on the surrender path so the worked example reproduces under either, and a test
pins the gap open rather than closing it in either direction.

**Not implemented.** Named here so the gaps cannot be mistaken for oversights. The
monthly-sum crediting method ``max(f, sum_k min(R_k, c_m))``, which needs a **monthly
index path** — a grid of months is not the same thing, and the scenarios state index
levels at anniversaries only [S4][R1]; interim values in either documented form, both
daily marks of the embedded option rather than interpolations [S10][S11]; the cap
re-declaration rule, because the notes state the *target* (set the cap so the one-year
call-spread cost equals the option budget) but give no option-pricing function, so the
base projection holds the snapshot scale level [R1][R6]; stochastic GLWB activation on the
``h(a)`` incidence table, which cannot be applied to a single deterministic cell —
:func:`~.FIA_US_SEC.Projection.activation_rate` reports the
table and the base run activates at the model point's ``income_start_age`` instead;
generational mortality projection with Scale G2, because the 2012 IAM/IAR family and the
G2 scale may not be redistributed here [REG-R59][REG-R60]; joint-life survivorship, the
notes specifying the joint *payout percentage* but no second-life mortality; the income
doubler, confinement and terminal illness waivers, and annuitization, all described and
put out of scope by the notes themselves; additional premium; and ``check_margin()``,
because the notes define no margin decomposition and the model projects no asset side.

**Model points.** ``model_point_table_sec.csv`` and ``rate_scenario_sec.csv`` are
generated from :mod:`~.FIA_US_S` and its inputs, and the tests regenerate both and
compare, so no row is typed by hand. Points 1 to 9 are the twins of :mod:`~.FIA_US_S`'s
nine contracts on the anchor configuration — male 62 ANB, non-qualified, $100,000 single
premium, GLWB elected at issue, income from attained age 70. Points 1, 3 and 7 are in
force at the valuation date at anniversary 7, on the balances the notes state there, as
:mod:`~.FIA_US_S` enters them: the worked example, the notes' "Where the step-up binds"
block, and the anchor overdrawing at 105% of the maximum. Points 2, 4, 5, 6, 8 and 9 are
issued at the valuation date: the anchor, pure stacking with the only non-zero fixed
allocation, joint life, no rider, a pre-exercise withdrawal, and income deferred to
attained age 85. Points 10 to 17 are S points restated in force at an S month, each
opened with the state S carries into that month: the stacking point on its anniversary at
month 60, with its fixed account; the anchor at month 95, the last month of contract year
8, whose anniversary carries its first lifetime withdrawal; the joint-life point in income
at month 150, mid-year; the overdrawing anchor near exhaustion at month 216; the anchor
depleted at month 240, its account value 0 and its income paid by the rider; the
pre-exercise point in its first policy year, at month 6; the no-rider point in its last
policy year, the one entered at attained age 120, at month 696; and the stacking point in
income at month 100, mid-year, its fixed account accrued since the anniversary. Point 18
is the anchor issued 15 months after the valuation date. A test asserts that every point
in the table projects.

**Verification.** On the six twins issued at the valuation date every cell this model
shares with :mod:`~.FIA_US_S` agrees with it at every argument the S model evaluates in
its sweep, the phases compared as their codes, but for those whose meaning changed —
``model_point``, ``pols_if_init``, the five ``_init`` cells whose issue values are
credited in the issue month instead, and ``result_pols``, which gains the month's new
business — so every golden ``tests/test_fixed_indexed_annuity_us.py`` asserts on a cell
that sweep reaches holds here too, with no number restated;
``tests/test_model_conventions.py`` asserts it. The worked example's goldens sit on the
in-force point 1, at policy month 95, which is ``t = 11`` here.
``tests/test_fixed_indexed_annuity_us_sec.py`` splices: an S point restated in force at
month ``d``, opened with S's own state there, continues the S projection from ``d`` on,
cell by cell, S's own in-force points among them; a point issued ``k`` months late is the
S projection ``k`` months on; and the committed tables are what S generates.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/fixed_indexed_annuity/FIA_US_SEC")
    >>> model.Projection[1].result_cf()            # by month from the valuation date
    >>> model.Projection[1].result_cf_annual()     # summed into contract years
"""

from modelx.serialize.jsonvalues import *

_name = "FIA_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

