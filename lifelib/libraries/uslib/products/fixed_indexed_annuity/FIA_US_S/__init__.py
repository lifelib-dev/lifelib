# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. fixed indexed annuities with a GLWB.

:mod:`~.FIA_US_S` is the executable counterpart of
``products/fixed_indexed_annuity/technical-notes.md`` in the lifelib-products
library. It projects gross liability cash flows for a single-contract model point of a
single-premium fixed indexed annuity carrying a guaranteed lifetime withdrawal benefit:
a 7% premium bonus vesting over ten years, one annual point-to-point indexed account
credited at ``max(0%, min(cap, index return))``, a notional benefit base growing by a
guaranteed simple rollup **plus** 150% of realised dollar credits, a 0.95% rider charge
on that base, a lifetime withdrawal locked at the attained age of first exercise, and —
the economic centre of the product — a guaranteed income stream that survives
account-value exhaustion and pays for life.

The base contract is the deferred annuity chassis of
:mod:`.MYGA_US_S`: the surrender-benefit composition order and the NAIC
Model #805 floor construction are the chassis's. **Everything else here is restated by
the FIA notes with its own parameters and must not be carried across from the chassis** —
the account-value roll-forward is index-credit driven rather than interest-accretion
driven, the MVA is the ratio form ``[(1+i0)/(1+it)]^(n/12) - 1`` rather than the linear
``(i0 - it) x T``, the death benefit is ``max(AV, MGV)``, and the lapse architecture is
rider-suppressed rather than a plain shock at surrender-charge expiry. The chassis's
``MGSV`` and these notes' ``MGV`` are **one quantity under two source labels**; this
model uses the chassis name :func:`~.FIA_US_S.Projection.mgsv_pp`
throughout.

**Spaces.** The model contains two:

:mod:`~.FIA_US_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.FIA_US_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.FIA_US_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Annual steps. ``t`` counts **contract years**, and each ``t`` is
also the anniversary that ends contract year ``t``, because the notes make the
anniversary the single event date: every mechanic in the composite is annual — annual
point-to-point crediting [S2][S4][S10], the rider charge at the end of each contract
year [S9], the annual benefit base update [S9] and the annual lifetime withdrawal. Note
the contrast with :mod:`.MYGA_US_S`, whose ``t`` counts **months**: that
chassis credits daily and needs a grid fine enough to resolve a 30-day window, whereas
here a monthly grid would buy nothing but the excluded variants (monthly-sum crediting,
Athene's monthly charge deduction, daily interim values, mid-year withdrawal crediting).
**The product assignment table records this product as monthly; its own technical notes
state annual, and the notes govern.**

``age(t)`` is the attained age **at anniversary** ``t``, ``age_at_entry() + t``, exactly
as the notes define it — the age that reads the lifetime-withdrawal percentage table.
Mortality over contract year ``t`` is therefore read one year lower, at ``age(t - 1)``.

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

``pols_if(t)`` is the in-force count at the **start** of contract year ``t``, the
library-wide convention set by :mod:`.Term_US_A` and ``savings.CashValue_SE``, and it is
the weight carried by every cash flow reported on the same row of ``result_cf()``. The
technical notes define ``l(t)`` the other way round, as the probability at the *end* of
the year; that quantity is kept as ``pols_if_at(t, "AFT_DECR")``, which is also
``pols_if(t + 1)``. Neither reading is discarded and the two never share a name.

Steps 1--3 are skipped in ``DEPLETED`` and steps 1--7 in ``TERMINATED``. ``t = 0`` is
the issue instant for a new-issue model point and carries the premium, the acquisition
expense and the initial branch of every recursion. A model point may instead be entered
**in force** at anniversary ``entry_year()`` on stated balances, which is what the
worked example does and why ``result_cf()`` is indexed from ``entry_year()`` rather than
always from zero.

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

Everything behavioural and expense-related is a standardization: the annual grid and the
anniversary-only event date; the annual step-up (no retrieved document describes an
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
[R1]'s worked ``min(80% x 10%, 6%) = 6%``) are the sourced ones.

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
monthly-sum crediting method ``max(f, sum_k min(R_k, c_m))``, which needs a monthly grid
the notes deliberately exclude [S4][R1]; interim values, whether Nassau's Daily/Protected
Account Value or Nationwide's Balanced Allocation Value, both daily marks of the embedded
option rather than interpolations [S10][S11]; the cap re-declaration rule, because the
notes state the *target* (set the cap so the one-year call-spread cost equals the option
budget) but give no option-pricing function, so the base projection holds the snapshot
scale level [R1][R6]; stochastic GLWB activation on the ``h(a)`` incidence table, which
cannot be applied to a single deterministic cell — :func:`~.FIA_US_S.Projection.activation_rate` reports the
table and the base run activates at the model point's ``income_start_age`` instead;
generational mortality projection with Scale G2, because the 2012 IAM/IAR family and the
G2 scale may not be redistributed here [REG-R59][REG-R60]; joint-life survivorship, the
notes specifying the joint *payout percentage* but no second-life mortality; the income
doubler, confinement and terminal illness waivers, and annuitization, all described and
put out of scope by the notes themselves; additional premium; and ``check_margin()``,
because the notes define no margin decomposition and the model projects no asset side.

**Model points.** ``model_point_table.csv`` carries nine contracts on the anchor
configuration — male 62 ANB, non-qualified, $100,000 single premium, GLWB elected at
issue, income from attained age 70. Point 1 is the worked example, entered **in force**
at anniversary 7 on the balances the notes state there; point 2 is the same cell issued
at ``t = 0``; point 3 is the notes' "Where the step-up binds" block, growth mechanism (a);
point 4 is growth mechanism (b), pure stacking with only half of index credits reaching
the account value; point 5 is joint life; point 6 carries no rider, so its shock lapse is
33%; point 7 overdraws at 105% of the maximum and so loses the guarantee at exhaustion;
point 8 takes a pre-exercise withdrawal that attracts the charge, the clawback and the
MVA; and point 9 defers income to attained age 85, past both the year the surrender charge
expires and the end of the twenty-year growth window, so its shock lapse is the 10%
rider-in-force-but-not-activated rate, its benefit base stops growing on the
contract-year-20 leg of ``T_g`` rather than on the first withdrawal, and its payout
percentage locks in the 80+ band. Between them they exercise both benefit-base growth
mechanisms, all three shock-lapse rates, both legs of the growth window, both step-up
binding cases, all four phases, both proportional-reduction denominators and both
depletion attributions, so no branch of the notes' parameter set is dead code. A test
asserts every point projects.

**Verification.** ``tests/test_fixed_indexed_annuity_us.py`` asserts all sixteen rows of
the notes' worked example table and every line of its surrender trace, to the cent and to
the eight decimals the MVA factor is displayed at; the "Where the step-up binds" variant
block on point 3; the notes' statement that the step-up binds in contract year 1 on a
new issue with a zero index credit; the depletion arithmetic — $11,997.42 a year,
exhausted during contract year 19 at attained age 81 — and the survival of the income
stream after it; the verbatim [S9] excess-withdrawal reduction and the verbatim [S10]
clawback; the in-force and account-value roll-forwards, both through the no-argument
``check_pols_roll_fwd()`` and ``check_av_roll_fwd()`` and through the per-anniversary
``check_*_resid(t)`` residuals they are built on; that the ``pols_if`` column of
``result_cf()`` is the weight carried by the cash flows on its own row; the payment cap
on the terminating exhaustion branch; and one test per pitfall the notes state as a model
mechanic. Three of the thirteen entries in the notes' Known modeling pitfalls list are
not model mechanics and carry no test: that the behavioural assumptions must not be
reused in a CARVM valuation, that "efficient policyholder selection" is not AG 33's
language, and that the declared parameters are stale and state-varying are all statements
about how the projection may be *used* rather than about what it computes, and no
assertion can reach them. A fourth, "Interim values and index costs", is half covered —
the interim-value structures it names are not implemented at all, while the index-cost
haircut it also names is, and is asserted to come off ``R(t)`` ahead of both the cap and
the participation rate. One line of the notes does **not** reproduce and is
pinned both ways instead: the surrender trace's net proceeds of 115,741.64 is the sum of
the *displayed* cent-rounded components, and carried at full precision — which the notes'
own rounding convention asks for — the net is 0.55 cents lower. Every component
reproduces exactly.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/fixed_indexed_annuity/FIA_US_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "FIA_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

