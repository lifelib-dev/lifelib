# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. variable annuities with guarantees.

:mod:`~.VA_US_SEC` projects the contracts :mod:`~.VA_US_S` projects from a **valuation
date** rather than from issue. Each is a single-contract model point of an individual
deferred variable annuity carrying two written options: a **guaranteed lifetime
withdrawal benefit** (GLWB) tracked on a Guaranteed Withdrawal Balance that grows by a
bonus and ratchets to contract value, and a **guaranteed minimum death benefit** (GMDB)
tracked on a roll-up Benefit Base. Contract value follows separate-account fund
performance with no insurer guarantee; both benefit bases are shadow accounts that never
fall with the market. A model point may be a contract already in force at that date, in
any month of its contract year, before or after its first withdrawal and with its account
value exhausted or not, one issued at it, or one to be issued in the ten years after it,
as in lifelib's ``basiclife/BasicTerm_SE``, which extends ``basiclife/BasicTerm_S`` the
same way. Its formulas are the executable counterpart of
``products/variable_annuity/technical-notes.md``, and
``products/variable_annuity/model-sec.md`` explains what running in force changes.

**Relation to the chassis.** The deferred annuity chassis of this library is
:mod:`.MYGA_US_S`, and the naming, the Data/Projection split and the
timing-argument vocabulary follow it. Its *mechanics* deliberately do not carry across,
and the chassis notes say so in terms: a VA's separate account is outside NAIC Model
#805, which reaches a VA only through its fixed account under Model #250 §7.B
[REG-R42][REG-R43] — and electing the Roll-up GMDB removes the Fixed Account Options
altogether [S1]. There is therefore **no minimum guaranteed surrender value, no market
value adjustment and no declared credited rate** in this model. What replaces them is a
unit ledger, a four-base charge stack and two path-dependent guarantees.

**Spaces.** The model contains two:

:mod:`~.VA_US_SEC.Data`
    Reads the five assumption CSVs it shares with :mod:`~.VA_US_S`, its own model point
    table and its own two scenarios, and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.VA_US_SEC.Projection`
    The by-contract projection, parameterized by ``idx``, a model point's position in the
    table: ``Projection[0]`` is an ItemSpace projecting the first row, model point 1. It
    reaches the input tables through its ``data`` Reference, which resolves to the single
    :mod:`~.VA_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps on two clocks. ``t`` counts months from the valuation
date, 0-based, as ``basiclife/BasicTerm_SE`` counts them: ``t = 0`` is the valuation month
for every model point, however old the contract, month ``t`` runs from time ``t`` to time
``t + 1``, and the frame runs ``t = 0, 1, ..., proj_len() - 1``, where ``proj_len()``
counts the months from the valuation date to the end of cover, and
``len(result_cf()) == proj_len()``. ``duration_mth(t)`` counts the policy months
**elapsed** at the start of month ``t``, ``duration_mth_init() + t`` from the model
point's ``duration_mth`` at ``t = 0``, and the contract runs on it: 0 in its issue month,
``policy_year(t) = duration_mth(t)//12 + 1`` the 1-based contract year, Contract
Anniversaries at the **end** of the months with 11, 23, 35, ... elapsed policy months and
Contract Quarterly Anniversaries at the end of those with 2, 5, 8, ... **[std]**. The
transaction programmes, the GAWA% grid, the withdrawal charge scale and the mortality read
that clock. The fund returns, the VIX-squared averages and the CMT rate run on ``t``
instead, a market path shared by every point of a block, and so does expense inflation,
which keeps maintenance expense in valuation-date dollars. On a point issued at ``t = 0``
the two clocks coincide, and the model computes what :mod:`~.VA_US_S` computes. Every
model in this library runs on a monthly grid; here it is not merely the house convention
but forced, because the base contract charge accrues daily on separate-account value, the
rider charges are assessed quarterly on benefit bases, and the roll-up and bonus are
credited annually — three different clocks, and changing any one changes the answer.

Within a month: at the beginning of the month (BOM) the premium buys units at the prior
unit value and raises ``GWB``, ``BB``, ``NP``, ``RP``, ``RB``, ``GAWA`` and ``ADJ``, then
the withdrawal is taken — fixing the GAWA% if it is the first, splitting into excess and
non-excess portions, charging the CDSC and updating ``GWB``, ``GAWA`` and ``BB``. Unit
values then grow over the month. At the end of the month (EOM) the two rider fees are
assessed at a Contract Quarterly Anniversary and the annual contract fee at a Contract
Anniversary, both by pro-rata unit cancellation; then, at a Contract Anniversary only,
the seven guarantee events in the notes' order; then the depletion test; then decrements,
**death first, then surrender** **[std]**. If the contract is already depleted the whole
of that is skipped and the post-depletion GLWB payment routine runs instead.

Cover runs to attained age ``omega_age`` = 120 **[std]**, the terminal age of the
mortality table, because once the account is exhausted the For Life Guarantee is a pure
life-contingent annuity at GAWA. The last covered month is therefore
``t = proj_len() - 1``, and the survivors there are carried out through
``pols_maturity()`` so the in-force roll-forward closes.

``pols_if(t)`` is the count in force at the **start** of month ``t``, after the month's
new business — the notes' ``l(t-1)`` — and is the weight carried by every cash flow on that
row, so the in-force column of ``result_cf()`` reconciles with the cash flows printed
beside it. A point in force at the valuation date opens with its ``policy_count``, and
one issued at or after it takes its ``policy_count`` as ``pols_new_biz`` in its issue
month; ``result_pols()`` sets the counts out. The notes' own end-of-month ``l(t)`` is
``pols_if_at(t, AFT_DECR)``. Two other names follow the library rather than the notes:
``lapse_rate(t)`` is the **annual** surrender rate and ``lapse_rate_mth(t)`` the monthly
one, matching ``mort_rate`` / ``mort_rate_mth``; and the net premium credited to the
account value is ``prem_to_av_pp(t)``, the per-contract form of ``prem_to_av(t)``.

**The opening state.** There is no issue-instant row: the single premium, the guarantee
bases' initialization and the acquisition expense are beginning-of-month flows of the
issue month, and :mod:`~.VA_US_S`'s issue values are credited there by its own rules. A
contract in force at the valuation date opens instead from twenty columns of its row, per
contract, as it stands at the start of month 0, before any month-0 event, each exactly
what :mod:`~.VA_US_S` carries into the month the contract is valued at: the value of each
subaccount, which :mod:`~.VA_US_S` would split from one account value by the target
allocation; the GWB, the Bonus Base, the GAWA, the GMDB Benefit Base, the cumulative Net
Premiums, the Remaining Premium and the GWB Adjustment; the locked GAWA%, the end of the
Bonus Period and whether a withdrawal has been taken; for the contract year under way, the
withdrawals to date, the free allowance they used, the GMDB's dollar-for-dollar reduction
and proportional factor so far, and whether the year has taken a withdrawal; the GMDB
Benefit Base at the anniversary that opened the year; the year's highest quarterly
account value before the valuation month; and, on the VIX-linked fee, the rate of the
quarter before. A contract whose opening account value is exhausted is depleted from
month 0, which no column states. ``Data`` refuses, as it reads the table, an opening state
no contract can be in, and ``proj_len()`` one that a ``Projection`` Reference shows to be
so, the depletion threshold or the VIX fee's rates, each naming the point.
``result_cf()`` has exactly ``proj_len()`` rows, ``t = 0 .. proj_len() - 1``, and row
``t`` is the same month on every point.

**Undiscounted.** Like every model in this library, this one projects *gross liability
cash flows* only. Reserves and discounting are a separate layer: the notes cite VM-21's
CTE70 stochastic reserve, C-3 Phase II's CTE(98), VM-22/VM-V §1 for the post-depletion
stream, IRC §807 and LDTI market risk benefits rather than reproducing any of them.
**Guarantee cost cannot be valued deterministically** — VM-21 makes that structural, the
Alternative Methodology being unavailable to any GLWB block [R1]. The base deterministic
run implemented here verifies the recursion, not the value of the guarantees.

**What is sourced and what is not.** The contractual elements come from the composite
specimen: the 1.30% base contract asset charge and the $35 contract fee waived at $50,000
[S2]; the 8.5%/7.5%/6.5%/5.5%/5.0%/4.0%/2.0%/0.0% withdrawal charge scale on Remaining
Premium by completed years since receipt, and the 10%-of-Remaining-Premium free
withdrawal with earnings out first [S1][S2]; the excess-withdrawal algebra —
dollar-for-dollar then pro rata — and the GMDB withdrawal adjustment applied at Contract
Year end [S1]; the $10,000,000 benefit base cap, the age-81 GMDB growth cutoff and the
59 1/2 For Life trigger [S1]; and the rate-sheet parameters dated 2026-04-27: GLWB charge
1.25%, GMDB charge 0.90%, bonus 6.00%, roll-up 6.00%/5.00%, GWB Adjustment 105% and the
GAWA% grid [S2][S3]. The dynamic lapse multiplier, the base surrender table, the
withdrawal-year factor, the zero surrender rate at ``AV = 0`` and the prescribed
maintenance expense are VM-21 [R1].

Everything else is a standardization: the monthly discretization of the daily asset
charge and of the decrements; the quarterly anniversary calendar; the M&E/administrative
split of the 1.30% total; the pro-rata deduction of the rider charges, extended from the
cited contract-fee rule; the 3.00% guaranteed maximum GLWB charge; the bonus-then-step-up
ordering; the 60/40 two-subaccount allocation and its fund expense ratios; the
reverse-engineered illustrative return path; activation at age 70 at 100% of GAWA; the
illustrative mortality table; the premium portion of a withdrawal for the Remaining
Premium roll-forward; the contract-value base for the GMDB proportional adjustment; the
reading that lets the ``basic`` GMDB election's proportional withdrawal reduction bite
against the notes' unreduced ``NP`` floor — the two tables contradict each other and the
elected form is taken to govern, which the README sets out in full; the capping of
charges and withdrawals at the available account value; and the attained age 120
horizon. Running in force changes none of them: the five assumption tables are
:mod:`~.VA_US_S`'s, read in place, and the two scenarios are its scenarios moved onto the
valuation clock.

**This model is a mechanics demonstration, not a pricing or reserving result.** Replace
the assumption tables with company data before drawing any conclusion from the output.

**Not implemented.** Named here so the gaps cannot be mistaken for oversights.
The **stochastic scenario interface** — real-world and risk-neutral scenario sets, proxy
fund mapping, and the CTE70/CTE(98) layers that consume them — is out of scope: returns
come from a deterministic scenario table, and the notes are explicit that a deterministic
run cannot value the guarantees. The **Withdrawal Delay Cohort Method** and the
never-withdraw cohort (weights 0.20 non-qualified and 0.05 tax-qualified [R1]) need a
revised-GAPV construction the notes do not supply, and would require blending parallel
projections. The **RMD module**: ``L = max(GAWA, RMD)`` carries the RMD term but no
divisor table is given and the base cell is non-qualified. The **combination GMDB**
``max(roll-up, ratchet)`` needs two parallel benefit bases and the notes state neither
which component carries the charge nor how the withdrawal adjustment splits between them.
The **highest-quarterly step-up basis** is implemented as the highest of the four most
recent quarterly contract values, *without* the source's adjustment of each for
subsequent premiums and withdrawals. The **two-table post-depletion payout** [S8] has no
Table B values in the sources. The **Latest Income Date** at owner age 95 [S2] is not a
forced annuitization: the prescribed annuitization assumption is 0% at all projection
intervals for a contract with no GMIB [R1], and no retrieved document carries an annuity
rate table. **Premium-tranche CDSC aging** is absent: Remaining Premium is carried as one
undifferentiated pool and the charge band is read off the contract duration, so a
subsequent premium does not restart its own charge clock. The notes key the band on
completed years since receipt of the premium being withdrawn [S2], which coincides with
the contract duration only while the contract is single premium — model point 4 is not,
and a test pins the divergence. The **charge-increase opt-out**, the terminal illness and
extended care waivers, spousal continuation, joint-life elections and the transfer charge
are all described in the sources and not modelled. And ``check_margin()`` is absent: the
model projects no asset side, so there is no charge-versus-cost decomposition to check;
``check_av_roll_fwd()``, ``check_pols_roll_fwd()`` and ``check_charge_split()`` are
implemented and all three close to floating point. Each takes **no argument and returns
a bool** covering every projected month, as ``savings.CashValue_SE`` does, with the
signed per-month residual available as ``check_av_roll_fwd_resid(t)`` and its two
counterparts for when one of them fails.

**Model points.** ``model_point_table_sec.csv``, ``return_scenario_sec.csv`` and
``rate_scenario_sec.csv`` are generated from :mod:`~.VA_US_S` and its inputs, and the
tests regenerate all three and compare, so no row is typed by hand. Points 1 to 9 are the
twins of :mod:`~.VA_US_S`'s nine contracts on the same anchor cell — male 60 ANB, single
Designated Life, non-qualified, $100,000 single premium, 60/40 allocation, the single-life
Core GLWB and the Roll-up GMDB — that differ only in the switches the technical notes make
first-class parameters. Point 1 is the worked-example anchor, issued at the valuation date
on a return path reverse-engineered so that the notes' own carried state at the beginning
of the 27th policy month — ``t = 26`` there — falls out of the projection exactly. Point 2
is the same carried state in force at the valuation date with 26 elapsed policy months,
so the worked-example month is its ``t = 0``, on its scenario re-based by 26 months; the
two readings agree to the cent and a test pins both. Points 3 to 9 are issued at the
valuation date: a declining market to exhaustion, the excess-withdrawal algebra and a
subsequent premium, the highest-quarterly step-up basis and the annual-ratchet GMDB, the
VIX-squared fee reset and the CMT-linked roll-up, two never-withdraw cells, on the
included return-of-premium death benefit and on the Roll-up GMDB, and the return of
premium withdrawing from age 70. Points 10 to 22 are S points restated in force at an S
month, each opened with the state :mod:`~.VA_US_S` carries into that month: the anchor in
its first policy year at month 6, at the year's start that takes its first withdrawal at
month 120 and in that year's last month at 131; the declining point depleted at a year's
start at month 144; the excess programme in the month of its excess withdrawal and five
months after, at 60 and 65; the highest-quarterly point mid-year at 40; the VIX-fee point
at 41, in a quarter's last month; the never-withdrawing Roll-up point depleted without a
withdrawal, at 560; the never-withdrawing return of premium in its last policy month at
719 and before its GWB Adjustment Date at 100; S's in-force point 2 at its month 14,
policy month 40; and the withdrawing return of premium mid-year at 125. Point 23 is the
anchor issued 15 months after the valuation date. A test asserts that every point in the
table projects.

**Verification.** On the eight twins issued at the valuation date every cell this model
shares with :mod:`~.VA_US_S` agrees with it at every argument the S model evaluates in its
sweep, but for those whose meaning changed — ``model_point``, ``pols_if_init`` and
``result_pols``, which gains the month's new business — so every golden
``tests/test_variable_annuity_us.py`` asserts on a cell that sweep reaches holds here too,
with no number restated; ``tests/test_model_conventions.py`` asserts it. The worked
example's goldens sit on point 1 at ``t = 26`` and on point 2 at ``t = 0``.
``tests/test_variable_annuity_us_sec.py`` splices: an S point restated in force at month
``d``, opened with S's own state there, continues the S projection from ``d`` on, cell by
cell, S's own in-force point among them; a point issued ``k`` months late is the S
projection ``k`` months on; and the committed tables are what S generates.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/variable_annuity/VA_US_SEC")
    >>> model.Projection[0].result_cf()            # by month from the valuation date
    >>> model.Projection[1].result_cf()            # the worked example's month at t = 0

The model compiles, as ``basiclife/BasicTerm_SC`` does, with modelx-cython: the
repository's ``tools/build_sec_cy.py`` builds it from ``products/variable_annuity``'s
``sample_sec.py`` and ``spec_sec.py``, and ``run_sec.py --cython`` runs the compiled model
(``products/variable_annuity/model-sec.md``).
"""

from modelx.serialize.jsonvalues import *

_name = "VA_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

