# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. deferred income annuities and QLACs.

:mod:`~.DIA_US_S` is the executable counterpart of
``products/deferred_income_annuity/technical-notes.md`` in the lifelib-products
library. It projects gross liability cash flows for a single flexible-premium deferred
income annuity: premiums in, each one buying a fully guaranteed paid-up income slice at
the then-current purchase rate; a return-of-premium death benefit during the deferral;
then, from the income start date, the immediate-annuity payout chassis — life-contingent
instalments with a certain floor, refund guarantees, survivor reduction and COLA.

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

:mod:`~.DIA_US_S.Data`
    Reads the six input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.DIA_US_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.DIA_US_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every contract. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Monthly steps. ``t`` counts **policy months from issue and is
0-based** — ``t = 0, 1, 2, …, proj_len()`` — exactly as the technical notes index it
("Projection frequency. Monthly, indexed ``t = 0, 1, 2, …`` from issue"). This is a
deliberate departure from the 1-based ``t`` of :mod:`.Term_US_A` and
:mod:`.SPIA_US_S`: the notes' income start month ``T = 240`` and premium months
0 and 60 are month *indices* in the 0-based scheme, and renumbering would silently make
``T = 240`` mean the 241st month. ``l(t)`` is the survival probability at the **start**
of month ``t`` with ``l(0) = 1``, so ``lives_if(t)`` still means "has survived ``t``
elapsed months" and carries the same meaning as in :mod:`.SPIA_US_S`; what does
shift is the death density, ``lives_death(t) = lives_if(t) - lives_if(t + 1)``, because
month ``t`` spans elapsed ``[t, t+1)`` here and ``[t-1, t)`` there.

The monthly processing order follows the notes: roll the attained age and look up
``q(t)``; take any premium at the **start** of the month, price it by equation (4) and
add its income slice to ``B`` and its amount to ``CP``; apply any option exercise;
pay the income instalment at the **end** of the month under the default arrears
convention, weighted by the form's payment survivorship; pay the death benefit — the
return of ``CP(t)`` in deferral, the form's refund benefit in payout — at the end of the
month of death; accrue the maintenance expense; then decrement. Contractual
transactions precede the decrement, and the end-of-month instalment is contingent on
survival to that point, which is what arrears means. All cash flows are
**undiscounted**; the only discounting in the model is contractual — inside the purchase
rate, the repricing of a start-date adjustment and a commuted value.

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
insurer cash flow; and every valuation layer — CARVM, AG 33, VM-22 CTE70 and the 2012
IAR valuation table with its no-compound-rounding rule.

**Model points.** ``model_point_table.csv`` carries seventeen contracts. Point 1 is the
notes' anchor cell — Female 60 ANB, nonqualified, Life with Cash Refund, monthly in
arrears, return-of-premium death benefit in deferral, no COLA, $100,000 at issue plus
$50,000 at the start of policy year 6, income start at attained age 80 (``T = 240``).
Points 2 and 3 are the same cell on the two readings the notes leave open (see
``Verification``); point 4 is the death-benefit fork; points 5 to 10 walk the payout
forms, the joint triggers and the COLA; points 11 and 12 are a compliant and a breaching
QLAC; points 13 to 15 exercise the start-date adjustment, payment acceleration and
commutation; point 16 runs the generational mortality construction; point 17 pays in
advance. The premium schedule is a separate table, ``premium_schedule.csv``, because a
flexible-premium contract takes an unbounded number of slices. A test asserts every
model point projects.

**Verification.** ``tests/test_deferred_income_annuity_us.py`` asserts every row and
column of the notes' worked example: the two slice purchase rates and the income they
buy, the derived guarantee period, the 21.2% death-benefit fork, and all nine rows of
the projection table — in-force to six decimals, money to the cent. It also pins the two
places the notes are internally inconsistent, on model points 2 and 3, rather than
choosing between them.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/deferred_income_annuity/DIA_US_S")
    >>> model.Projection[1].result_annual()
"""

from modelx.serialize.jsonvalues import *

_name = "DIA_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

