# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. participating whole life insurance.

:mod:`~.WholeLife_US_SEC` projects the policies :mod:`~.WholeLife_US_S` projects — the two
standardized composite designs ``products/whole_life/technical-notes.md`` specifies:
``RefWL-Par``, a participating level-premium whole life policy with a guaranteed cash
value schedule that endows at attained age 100, an annual three-factor dividend and
paid-up additions; and ``RefWL-FE``, the non-participating simplified-issue
final-expense variant with an explicit policy fee and, on the graded plan, a
return-of-premium death benefit in policy years 1-2 — from a **valuation date** rather
than from issue. A model point may be a policy already in force at that date, in any
month of its policy year, one issued at it, or one to be issued in the ten years after
it, as in lifelib's ``basiclife/BasicTerm_SE``, which extends ``basiclife/BasicTerm_S``
the same way. Its formulas are the executable counterpart of
``products/whole_life/technical-notes.md``, and ``products/whole_life/model-sec.md``
explains what running in force changes.

**Spaces.** The model contains two:

:mod:`~.WholeLife_US_SEC.Data`
    Reads the five assumption CSVs it shares with :mod:`~.WholeLife_US_S` and its own
    model point table, and holds their filename References. It takes no parameters, so
    each file is read **once per model**. It hands the projection what the files hold as
    numpy vectors and arrays of numbers, one element per model point, per key or per
    schedule.

:mod:`~.WholeLife_US_SEC.Projection`
    The by-policy projection, parameterized by ``idx``, the position of a model point in
    the ``Data`` vectors, as ``basiclife.BasicTerm_SC`` is: ``Projection[0]`` is an
    ItemSpace projecting the table's first row, model point 1, and its ``point_id()`` is
    that label. It reaches the inputs through its ``data`` Reference, which resolves to
    the single :mod:`~.WholeLife_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Compiled.** The model compiles under modelx-cython into C-typed code, as
``basiclife/BasicTerm_SC`` does, from the two inputs beside it: ``sample_sec.py``, the run
that types each cell, and ``spec_sec.py``, the length of each cell's cache.
``Projection``'s cells read every model point attribute a projection cell uses as a C
number from a ``Data`` vector at ``idx``, and every table as an array indexed by integers;
a timing, a kind, a premium period or a dividend option is an int code; and every cell but
the reports, ``model_point`` and six label accessors returns a C ``bint``,
``long long`` or ``double``, cached as a single value or in a C array sized from the
contract. The dividend alone keeps a Python call, ``round``. modelx reads and runs the
same formulas, and computes the same numbers. ``products/whole_life/model-sec.md`` says
how to compile and run it, and what the compiled model does not do as modelx does: it
clears no cache when a Reference is set, so every Reference is set on a model just
imported.

**Projection basis.** Monthly steps on two clocks. ``t`` counts months from the
valuation date, 0-based, as ``basiclife/BasicTerm_SE`` counts them: ``t = 0`` is the
valuation month for every model point, however old the policy, period ``t`` runs from
time ``t`` to time ``t + 1``, and the frame runs ``t = 0, 1, ..., proj_len() - 1``,
where ``proj_len()`` counts the months from the valuation date to maturity at attained
age 100. ``duration_mth(t)`` counts the months the policy has been in force,
``duration_mth_init() + t`` from the model point's ``duration_mth`` at ``t = 0``, and
the contract runs on it.

Everything contractual about this product is annual: the guaranteed cash value
schedule, the dividend declaration, the anniversary capitalization of loan interest,
the premium-paying period. The policy year is therefore derived and used as a lookup
key — ``duration(t) = duration_mth(t) // 12``, ``policy_year(t) = duration(t) + 1``,
``age(t) = age_at_entry() + duration(t)`` — and ``is_anniv(t)``, true in the last month
of a policy year, is where every annual event lands. Decrements run in two speeds, the
library's convention: ``mort_rate(t)`` and ``lapse_rate(t)`` are the **annual** rates
of the policy year containing month ``t``, and ``mort_rate_mth(t)`` and
``lapse_rate_mth(t)`` are the monthly rates actually applied, ``1 - (1 - q)^(1/12)``.
Twelve of those compound back to the annual rate, so the in-force at every anniversary
is exactly what an annual-step model would carry. Expense inflation alone runs on
``t``, so the maintenance charge is in valuation-date dollars; acquisition is charged
per policy issued, in the issue month, and is not inflated, as in
``basiclife/BasicTerm_SE``. On a point issued at ``t = 0`` the two clocks coincide, and
the model computes what :mod:`~.WholeLife_US_S` computes.

What the finer grid buys is everything that is *not* contractually annual: death
claims settle at the end of the month of death, maintenance expense accrues monthly,
the guaranteed cash value and the paid-up-additions cash value interpolate between
anniversaries so a mid-year surrender is valued where it happens, and a **modal premium
is collected when it is contractually due** — which retires the notes' "premium mode
modeled: annual" **[std]**, the modal factors being sourced for both designs.
``result_cf_annual()`` sums the frame into policy years so a monthly run can be laid
beside an annual one.

The **value** state variables are closing balances: ``cv_pp(t)``, ``pua_face(t)``,
``div_accum(t)`` and ``loan_bal(t)`` are all as at the **end of month t**. The value
entering a month is the closing value of the one before, and at ``t_entry()``, the
first month on the books, it is the model point's opening state, written inline as
``pua_face(t - 1) if t > t_entry() else pua_face_init()`` wherever an opening balance
is read, so that nothing is ever asked for a month before the valuation date. For a
point in force the opening state is seven columns of its row: the paid-up additions,
the loan and the accumulation balance entering month 0, the paid-up additions and the
loan at the anniversary that opened the policy year under way, the dividend credited
there, and the gross premium paid to date. For a point issued at or after the
valuation date every one of them is 0, as at issue. Annual quantities read the balance
entering the **policy year** instead, twelve months back, or the opening state's
anniversary values where that month is before the valuation date.

``pols_if(t)`` follows the same clock: the number in force at the **start** of month t,
after the month's new business — ``pols_if_at(t, BEF_DECR)``, the notes' ``l_t`` —
because that is the weight every cash flow on the same ``result_cf()`` row is computed
over, and because it is what ``pols_if`` means in every other model in this library. A
point in force at the valuation date opens with its ``policy_count``, and one issued at
or after it takes its ``policy_count`` as ``pols_new_biz`` in its issue month;
``result_pols()`` sets the counts out. The notes' end-of-period ``l_{t+1}`` is
``pols_if_at(t, AFT_DECR)``, the count carried into the next month before that month's
new business.

Within a month the order is the notes': premium, PUA rider premium, premium tax
and expenses at the **beginning**; then, at the **end**, deaths, the dividend credit
and loan interest capitalization where the month is an anniversary, surrenders, and —
in the final month only — maturity. Deaths are therefore valued on the paid-up
additions entering the month (``claim_pp(t, DEATH)``) while surrenders are valued on
the closing ones, including any dividend just credited.

The net flow is published under **both** signs, because these notes print ``NetCF_t``
with outgo positive while the rest of the library is income-positive.
``liability_cf(t)`` carries the notes' formula verbatim — premium income with a minus
sign, so a positive value is money leaving the insurer — and
``net_cf(t) = -liability_cf(t)`` carries the income-positive convention every model in
``products/`` shares, so the column can be summed or compared across products. Both are
columns of ``result_cf()``. Nothing is silently flipped and nothing is lost.

**What is sourced and what is not.** Very little of this product is public. The
contractual skeleton is sourced: the 4.00% guarantee interest rate, endowment of the
guaranteed cash value at face at age 100, the fixed 6.00% loan rate with direct
recognition, the union of dividend options with paid-up additions as the default, the
modal factors of both designs, and — for the final-expense variant — the per-$1,000
premium rates, the $36 policy fee and the 110%-of-premiums graded death benefit.
Everything else is a standardization introduced for the reference implementation and
marked **[std]**: the 6.00% dividend interest rate snapshot, the three-factor dividend
parametrization, the 0.70 experience factor that produces both the scale and the
best-estimate mortality, the $25 expense margin, the lapse schedules, expenses,
premium tax, the 10% PUA-rider load, the 2x term-blend target, the straight-line
interpolation of the cash value and the net single premium between anniversaries, and
every shipped table — the guarantee mortality, the net single premiums, the
nonforfeiture net level premiums and the guaranteed cash value schedules are all
illustrative curves calibrated to the worked example's anchors, **not** the 2017 CSO /
4% tables the notes name, which are licensed and may not be shipped here.
**This model is a mechanics demonstration, not a pricing or reserving result.**
Replace the assumption tables with company data before drawing any conclusion from the
output.

Those four tables are pinned to their worked-example anchors *independently*, which is
a documented divergence from the notes rather than an oversight: the notes' first
"known modeling pitfall" says to regenerate every guarantee-basis quantity from one
2017 CSO / 4% source, and the worked example's own steps 3 and 10 make that impossible
— ``NP_g = 13.00`` and ``NSP_55 = 0.42`` cannot both hold on any single mortality
table at 4%. The arithmetic is in the ``Projection`` docstring, in ``model.md`` and in
a test. What the shipped tables *do* preserve are the two endpoints whose failure the
pitfall is about: the net single premium is exactly 1 at attained age 100 and the cash
value schedule is exactly face in the final policy year, so neither block leaks at
maturity.

**Not implemented.** The notes describe, and this model deliberately omits: the
reduced paid-up and extended term nonforfeiture options and the automatic premium loan
(the notes name them but give no projection formula); partial surrender of paid-up
additions; terminal dividends and dividends credited at death; the variable/adjustable
loan rate regimes; the age 100-121 tail beyond the **[std]** truncation; and any
Sect. 7702 / 7702A policing — ``mec_flag()`` flags a model point that would need the
test rather than performing it, exactly as the notes prescribe. State variations are
not modeled.

**Model points.** ``model_point_table_sec.csv`` is generated from
:mod:`~.WholeLife_US_S` and its model point table, and the tests regenerate it and
compare, so no row is typed by hand. Points 1 to 15 are the twins of
:mod:`~.WholeLife_US_S`'s fifteen points. Point 1 is the worked example's anchor cell, a
male 45, $100,000, $1,800-premium policy in force 108 months at the valuation date,
which falls on the anniversary opening policy year 10, the year the notes walk through,
with its 4,100 of paid-up additions; points 2 to 15 are S's new business, issued at the
valuation date.
Points 16 to 21 are S points restated in force at an S month, each opened with the state
S carries into that month: the REDUCE_PREM and the ACCUM point at month 108, on the
anchor cell's anniversary, carrying last year's dividend and the accumulation balance;
the funded term blend at month 78 and the loan variant at month 114, both mid-year,
carrying the paid-up additions and the loan at the anniversary before; the graded
final-expense point at month 18, inside its graded years, carrying the premiums paid;
and the REDUCE_PREM point at month 659, its last covered month. Point 22 is point 2
issued three months after the valuation date. A test asserts that every point in the
table projects.

**Verification.** On the fourteen twins issued at the valuation date every cell this
model shares with :mod:`~.WholeLife_US_S` agrees with it at every argument the S model
evaluates in its sweep, ``pols_if_init``, ``model_point`` and ``result_pols`` excepted,
so the goldens ``tests/test_whole_life_us.py`` asserts on them hold here too, with no
number restated. ``tests/test_whole_life_us_sec.py`` splices: an S point restated in
force at month ``d``, opened with S's own state there, continues the S projection from
``d`` on, cell by cell, and so does the anchor cell's twin from S's month 108, which
carries the worked example's walk through policy year 10 over. A point issued ``k``
months late is the S projection ``k`` months on, and the committed table is what S
generates.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/whole_life/WholeLife_US_SEC")
    >>> model.Projection[18].result_cf()     # the nineteenth row: model point 19
    >>> model.Projection[18].result_pols()
"""

from modelx.serialize.jsonvalues import *

_name = "WholeLife_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
