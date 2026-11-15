# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. deferred income annuities.

:mod:`~.DIA_US_SEC` projects the contracts :mod:`~.DIA_US_S` projects — a single flexible
premium deferred income annuity, a QLAC among them: premiums in, each one buying a fully
guaranteed paid-up income slice at the then-current purchase rate; a return-of-premium
death benefit during the deferral; then, from the income start date, the
immediate-annuity payout chassis — life-contingent instalments with a certain floor,
refund guarantees, survivor reduction and COLA — from a **valuation date** rather than
from issue. A model point may be a contract already in force at that date, in its
deferral or in its income phase, one issued at that date, or one issued in the ten years
after it, as in lifelib's ``basiclife/BasicTerm_SE``, which extends
``basiclife/BasicTerm_S`` the same way. Its formulas are the executable counterpart of
``products/deferred_income_annuity/technical-notes.md``, and
``products/deferred_income_annuity/model-sec.md`` explains what running in force changes.

**Two structural facts govern the whole design.** There is **no account value** — no
credited rate, no charge, no surrender value, no interim value — so there is **no lapse
decrement** and no annuitization decrement; VM-22 declares its standard-projection lapse
section "not applicable" to contracts with no account value or surrender benefit and
prescribes annuitization at 0% [R9]. Mortality is the only decrement. And the income
phase **is** the immediate-annuity payout chassis: the payment factor, the certain
floor, the survivor-reduction triggers and the COLA rule are the same objects as in
:mod:`.SPIA_US_S`, carrying the same cells names. The DIA-specific change is the
base of the guarantee — **cumulative** premiums ``CP(T)``, not a single premium.

**Spaces.** The model contains two:

:mod:`~.DIA_US_SEC.Data`
    Reads the four assumption CSVs it shares with :mod:`~.DIA_US_S`, its own model point
    table and its own premium schedule, and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.DIA_US_SEC.Projection`
    The by-contract projection, parameterized by ``idx``, a model point's position in the
    table: ``Projection[0]`` is an ItemSpace projecting the table's first row, model point
    1. It reaches the input tables through its ``data`` Reference, which resolves to the
    single :mod:`~.DIA_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every contract. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Monthly steps on two clocks. ``t`` counts months from the valuation
date, 0-based, as ``basiclife/BasicTerm_SE`` counts them: ``t = 0`` is the valuation month
for every model point, however long the contract has been in force, and the frame runs
``t = 0, 1, ..., proj_len() - 1``, where ``proj_len()`` counts the months from the
valuation date to the notes' stop rule. ``duration_mth(t)`` counts the months elapsed from
issue, ``duration_mth_init() + t`` from the model point's ``duration_mth`` at ``t = 0``,
and the contract runs on it: the policy year ``duration_mth(t) // 12 + 1``, the attained
ages, the premium months, the income start month ``T``, the option months, the payment
months, the COLA anniversaries and the certain period. Survival is indexed by a **time
point** on the valuation clock, ``lives_if(t, life)`` *at* time ``t``, the start of month
``t``, and the instalments scheduled to date by a policy month, ``cum_annuity_pp(k)``
through the end of policy month ``k``.

The stop rule is :mod:`~.DIA_US_S`'s, on the policy clock: the month the youngest covered
life attains the limiting age, or the end of the guarantee period if that is later. On
the anchor cell it is policy month 720: the life is 119 in the last projected month,
policy month 719, and a contract in force ``d`` months has ``720 - d`` months left to
project.

The monthly processing order follows the notes: roll the attained age and look up
``q``; take any premium at the **start** of the month, price it by equation (4) and
add its income slice to ``B`` and its amount to ``CP``; apply any option exercise;
pay the income instalment at the **end** of the month under the default arrears
convention, weighted by the form's payment survivorship; pay the death benefit — the
return of ``CP`` in deferral, the form's refund benefit in payout — at the end of the
month of death; accrue the maintenance expense; then decrement. All cash flows are
**undiscounted**; the only discounting in the model is contractual — inside the purchase
rate, the repricing of a start-date adjustment and a commuted value. Expense inflation
alone runs on ``t``, so the maintenance charge is in valuation-date dollars. Mortality
improvement is calendar-dated, through ``issue_year + duration(t)``, so it stays on the
policy clock: a contract reads the improvement of its own calendar years whatever the
valuation date. On a point issued at ``t = 0`` the two clocks coincide, and the model
computes what :mod:`~.DIA_US_S` computes, except that ``pols_if_init()`` is the count
already in force at the valuation date, 0 for such a point, whose contracts enter as new
business at ``t = 0``.

**Pricing stays at issue and premium dates.** :mod:`~.DIA_US_S` uses one survival curve
both to price each premium's slice at its own date and to project; on the valuation clock
the two part. The projection's survival opens at the valuation date from the contract's
opening state, while the pricing kernel prices each premium still due, and a start-date
adjustment still to come, on its own survival curve from issue, one loop over the monthly
rates, :mod:`~.DIA_US_S`'s recursion unrolled, so that every purchase rate is
:mod:`~.DIA_US_S`'s to the last bit. The payout schedule — the income, the refund base and
the instalments scheduled to date — is fixed at the income start month, where the income
becomes level, and read by policy month.

A contract in force carries an **opening state** beside its count and its policy clock:
each covered life's probability of being alive at the valuation date, 1 or 0 on a real
record, so that a joint contract may carry one life already dead; the premiums paid and
the guaranteed income they bought; on a refund form, the guarantee period with which the
pricing kernel prices every slice, a fixed point over the whole premium schedule; past the
income start month, the cohort that reached the income phase, ``l_last(T)``, which exceeds
the lives alive in a certain period, since the contract stays open for a beneficiary after
the last death; past a commutation, the cohort that commuted, ``l_last(t_c)``; and the
reference rate's change from issue to the valuation date, which moves the commutation
discount rate, the Reference ``ref_rate_shift`` being the change made at that date, on the
one path every point shares, which a contract issued later has not seen. The premiums still
due are in the model's own premium schedule.

**What is sourced and what is not.** The contractual elements come from the composite's
product documents and the Insurance Compact's uniform standard: the paid-up income slice
bought by each premium at then-current rates [R13 §3.B(1)(b)][S3], the 100%
return-of-premium deferral death benefit [S1][S2][S3][S4][R13 §3.I(1)(a)], the
one-time ±5-year income start date adjustment and its disclosed repricing inputs
[S1][S2], six months of payment acceleration [S1][S4], commutation of the guaranteed
payments with the life-contingent tail preserved [S4][S5], the QLAC restriction set and
its $210,000 2026 premium limit [R1][R2][R3][S4], the $50 maintenance expense escalated
at 2.5% [R9], and the absence of lapse and annuitization decrements [R9].
**No purchase-rate table exists**: the Compact expressly relieves the insurer of
disclosing the deferral-period mortality and interest basis [R13 §1.B(1)(a)], so the
whole pricing kernel — the 4.75% pricing rate, the 6.0% expense and profit load, the
mortality table, the illustrative payout and return-of-premium factors, the 100 bp
repricing spread and the 50 bp commutation margin — is a **[std]** construction.
**This model is a mechanics demonstration, not a pricing or reserving result.**

Not implemented, and named here so the omission is visible: the **incidence and
selection layer** of the in-force options — the 1.5% p.a. start-date-adjustment take-up
``h_adj`` with its 60/40 direction split and rate multipliers ``M_def``/``M_adv``, the
0.90/1.10 health-selection multiplier ``sel_mult``, the 2% p.a. acceleration take-up
``h_acc`` and the 1.5% p.a. commutation take-up ``h_com``, all of which split the model
point into exercised and unexercised cohorts (each option is instead exercised
deterministically at a month named on the model point, and is off by default);
the exact cash-refund pricing factor of equation (6), the notes blessing the equation
(5) certain-and-life approximation as the **[std]** base for both refund forms; the
convertible-joint pricing of equation (16), the base being non-convertible **[std]**;
spousal continuation on a death in deferral, the base being 100% election of the death
benefit **[std]**; premium admissibility limits and the 13-month premium cut-off, which
are validation rather than cash flow; the small-benefit termination right [R10 §3.B];
the exclusion-ratio tax split, which is a policyholder computation and generates no
insurer cash flow; a reference-rate path (``ref_rate_shift`` is a flat scalar); and every
valuation layer — CARVM, AG 33, VM-22 CTE70 and the 2012 IAR valuation table with its
no-compound-rounding rule.

**Model points.** ``model_point_table_sec.csv`` and ``premium_schedule_sec.csv`` are
generated from :mod:`~.DIA_US_S`, its model point table and its premium schedule, and the
tests regenerate them and compare, so no row is typed by hand. Points 1 to 17 are the twins
of :mod:`~.DIA_US_S`'s seventeen points, each issued at the valuation date, so the worked
example's anchor cell and its forks, forms, options and QLAC cases are here as there.
Points 18 to 25 are S points restated in force at an S month, each opened with the state S
carries into that month: the payment-acceleration contract in its deferral, the month
before its second premium; the anchor cell a month into its income phase, its cash refund
running; the 10-year period certain inside its guarantee, where the contract open exceeds
the life alive; the commuting contract a month after its commutation; the start-date
adjustment a month after it; the joint contract with its joint annuitant dead; the
installment refund inside its derived certain period; and the anchor cell in its last
month, a one-row frame. Point 26 is the joint contract issued 13 months after the valuation
date. Each row keeps :mod:`~.DIA_US_S`'s issue year, so the rows are test cases standing
at different calendar dates at their common ``t = 0``; a real block carries each contract's
actual issue year. A test asserts that every point in the table projects.

**Verification.** On the seventeen twins every cell this model shares with
:mod:`~.DIA_US_S` agrees with it at every argument the S model evaluates in its sweep,
``pols_if_init``, ``model_point`` and ``result_pols`` excepted, so the worked example
``tests/test_deferred_income_annuity_us.py`` asserts — the two slice purchase rates and the
income they buy, the derived guarantee period, the death-benefit fork and the projection
table — holds here too, with no number restated. The SEC tests splice: an S point restated
in force at month ``d``, opened with S's own state there, continues the S projection from
``d`` on, cell by cell, and a contract issued ``k`` months late is the S projection ``k``
months on.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/deferred_income_annuity/DIA_US_SEC")
    >>> model.Projection[18].result_cf()       # model point 19, at position 18
    >>> model.Projection[18].result_pols()
"""

from modelx.serialize.jsonvalues import *

_name = "DIA_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

