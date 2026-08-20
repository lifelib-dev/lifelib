# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. variable annuities with guarantees.

:mod:`~.VA_US_S` is the executable counterpart of
``products/variable_annuity/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for a single-contract model point of an individual
deferred variable annuity carrying two written options: a **guaranteed lifetime
withdrawal benefit** (GLWB) tracked on a Guaranteed Withdrawal Balance that grows by a
bonus and ratchets to contract value, and a **guaranteed minimum death benefit** (GMDB)
tracked on a roll-up Benefit Base. Contract value follows separate-account fund
performance with no insurer guarantee; both benefit bases are shadow accounts that never
fall with the market.

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

:mod:`~.VA_US_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.VA_US_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.VA_US_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps. ``t`` counts **projection months**, ``t = 1, 2, ...,
proj_len()``, with ``t = 0`` the entry instant carrying the single premium and the
initial branch of every recursion. The *policy* month is
``duration_mth(t) = duration_mth_init() + t``; the two coincide for an at-issue cell and
differ for an in-force cell, and every calendar test is written on ``duration_mth``.
``policy_year(t) = ceil(duration_mth(t)/12)``, so Contract Anniversaries fall at the end
of policy months 12, 24, ... and Contract Quarterly Anniversaries at the end of policy
months 3, 6, 9, ... **[std]**. Note the contrast with :mod:`.Term_US_A`, where ``t``
counts years: monthly is required here because the base contract charge accrues daily on
separate-account value, the rider charges are assessed quarterly on benefit bases, and
the roll-up and bonus are credited annually — three different clocks, and changing any
one changes the answer.

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

``proj_len()`` runs to attained age ``omega_age`` = 120 **[std]**, the terminal age of
the mortality table, because once the account is exhausted the For Life Guarantee is a
pure life-contingent annuity at GAWA. The survivors at that horizon are carried out
through ``pols_maturity()`` so the in-force roll-forward closes.

``pols_if(t)`` is the count in force at the **start** of month ``t`` — the notes'
``l(t-1)`` — and is the weight carried by every cash flow on that row, so the in-force
column of ``result_cf()`` reconciles with the cash flows printed beside it. The notes'
own end-of-month ``l(t)`` is ``pols_if_at(t, "AFT_DECR")``. Two other names follow the
library rather than the notes: ``lapse_rate(t)`` is the **annual** surrender rate and
``lapse_rate_mth(t)`` the monthly one, matching ``mort_rate`` / ``mort_rate_mth``; and
the net premium credited to the account value is ``prem_to_av_pp(t)``, the per-contract
form of ``prem_to_av(t)``.

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
horizon. **This model is a mechanics demonstration, not a pricing or reserving
result.** Replace the assumption tables with company data before drawing any conclusion
from the output.

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
are all described in the sources and not modelled. And ``check_margin()`` is absent: the model
projects no asset side, so there is no charge-versus-cost decomposition to check;
``check_av_roll_fwd()``, ``check_pols_roll_fwd()`` and ``check_charge_split()`` are
implemented and all three close to floating point. Each takes **no argument and returns
a bool** covering every projected month, as ``savings.CashValue_SE`` does, with the
signed per-month residual available as ``check_av_roll_fwd_resid(t)`` and its two
counterparts for when one of them fails.

**Model points.** ``model_point_table.csv`` carries nine contracts on the same anchor
cell — male 60 ANB, single Designated Life, non-qualified, $100,000 single premium,
60/40 allocation, the single-life Core GLWB and the Roll-up GMDB — that differ only in the
switches the technical notes make first-class parameters. Point 1 is the worked-example
anchor, projected from issue on a return path reverse-engineered so that the notes' own
carried state at the beginning of month 27 falls out of the projection exactly. Point 2
is the same carried state entered directly as an **in-force cell**, so the worked-example
month reproduces without depending on that return path — the two readings agree to the
cent and a test pins both. Point 3 runs a declining market to exhaustion and exercises
depletion and the insurer-funded GLWB payment stream; point 4 the excess-withdrawal
algebra and a subsequent premium; point 5 the highest-quarterly step-up basis and the
annual-ratchet GMDB; point 6 the VIX-squared fee reset and the CMT-linked roll-up;
point 7 a never-withdraw cell on the included proportional return-of-premium death
benefit with no withdrawal charge, which is what exercises the GWB Adjustment Date and
the five-yearly discretionary fee increase; point 8 a never-withdraw cell on the Roll-up
GMDB, whose Benefit Base compounds cleanly to the age-81 cutoff with no withdrawal
adjustment to muddy it and whose rider fees on the two bases eventually exhaust the
account at policy month 555; and point 9 the same proportional return-of-premium death
benefit as point 7 but **withdrawing** from age 70, which is what makes that form's
``G <- G x (1 - W/AV_pre)`` reduction bite. A test asserts every point projects.

**Verification.** ``tests/test_variable_annuity_us.py`` asserts every row and column of
the notes' worked example: the two subaccount balances at each of the six printed steps,
the two growth factors to seven decimals, the pro-rata weights to six, the two rider
fees, the end-of-month balances, all three memo lines (M&E and admin inside the unit
value, the fund expense that is *not* insurer revenue, and total insurer charge income),
the GMDB test with its gross and net figures, the moneyness ratios and lapse multiplier,
the CDSC and free-withdrawal memo, and the GAWA memo — on **both** the at-issue and the
in-force reading of the anchor. It also asserts the carried state the notes narrate at
anniversaries 1 and 2, both roll-forwards at every month, and one test per entry in the
notes' "Known modeling pitfalls" list.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/variable_annuity/VA_US_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "VA_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

