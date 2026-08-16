# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of :mod:`~.MYGA_US_S`.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the anchor cell
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/fixed_deferred_annuity/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec,
no embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``MYGA_US_S`` folder without its parent's CSVs produces a model that reads
and then fails on first evaluation.

The readers and the filename References live on the sibling
:mod:`~.MYGA_US_S.Data` Space, reached here through the ``data`` Reference, so
each file is read once per model rather than once per model point:

=========================  ==================================  ==========================
Reference (on Data)        Cells                               File
=========================  ==================================  ==========================
model_point_file           data.model_point_table()            model_point_table.csv
mort_table_file            data.mort_table()                   mort_table.csv
surr_charge_file           data.surr_charge_table()            surr_charge_table.csv
surr_charge_age_cap_file   data.surr_charge_age_cap_table()    surr_charge_age_cap.csv
rate_scenario_file         data.rate_scenario()                rate_scenario.csv
withdrawal_file            data.withdrawal_table()             withdrawal_table.csv
mva_factor_file            data.mva_factor_table()             mva_factor_table.csv
=========================  ==================================  ==========================

.. rubric:: Projection basis

``t`` counts **policy months**, 1-based, with ``t = 0`` the issue instant carrying the
premium, the acquisition commission, the premium tax and the initial branch of every
recursion. ``policy_year(t) = ceil(t / 12)`` is the contract year, so anniversaries fall
at ``t = 12, 24, ...`` and the five-year guarantee period ends at ``t = 60``.

Within a month: the free-withdrawal counters roll, the guarantee-period boundary is
applied, the elective withdrawal is taken and the tax basis updated — all at the beginning
of the month (BOM) — then interest is credited, the Model #805 floor rolls forward and
decrements are applied in the order annuitization, mortality, surrender at the end of the
month (EOM) **[std]**, with every decrement benefit valued on the post-crediting account
value.

Twelve monthly factors ``(1 + i_cr)^(1/12)`` reproduce the declared *effective annual*
rate exactly, so ``av_pp(12) = premium_pp() * (1 + i_cr)``. Do not additionally compound
daily; the discretization affects only the placement of interest *within* a month.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, ``av_*`` for
account values, plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for
per-contract amounts, ``*_at(t, timing)`` for a quantity read at a point inside the
month. The technical notes use compact actuarial symbols instead. The mapping is:

======================  ====================================================  ==========================================
Notes symbol            Cells                                                 Meaning
======================  ====================================================  ==========================================
t                       duration_mth(t)                                       Elapsed policy months
y = ceil(t/12)          policy_year(t)                                        Contract year containing month t
y - 1                   duration(t)                                           Completed contract years
x                       age_at_entry                                          Issue age (ANB)
x + y - 1               age(t)                                                Attained age in month t
n                       guar_period                                           Guarantee period in years
(none)                  policy_term                                           Years from issue to maturity_age
(none)                  proj_len                                              Last projection month
P                       premium_pp                                            Single purchase payment
i_cr(t)                 credit_rate(t)                                        Declared credited rate, eff. annual
f(t) - 1                credit_rate_mth(t)                                    Monthly credited rate
s_ren                   renewal_spread                                        Renewal declaration spread (Reference)
i_nf                    mgsv_rate                                             GMSV accumulation rate (2.80%)
g - 1                   mgsv_rate_mth                                         Monthly GMSV rate
i_stat                  mgsv_rate_statutory(cmt5)                             Model #805 indexed rate
GMIR                    gmir                                                  Guaranteed minimum interest rate
MR(t)                   market_rate(t)                                        Market competitor rate
AV(t)                   av_pp(t)                                              Account value at end of month t
AV(t-1), AV'(t), AV(t)  av_pp_at(t, timing)                                   BEF_WD / BEF_INV / EOM
l(t) x AV(t)            av_at(t, timing)                                      In-force weighted account value
(interest credited)     inv_income_pp(t)                                      Interest credited in month t
(cumulative interest)   interest_credited_pp(t)                               Interest credited to date
MGSV(t)                 mgsv_pp(t)                                            Model #805 floor at end of month t
c(t)                    mgsv_charge_pp(t)                                     Monthly slice of the contract charge
d(t)                    mgsv_wd_deduct_pp(t)                                  Withdrawal deducted from the floor
FWB(y)                  free_wd_base(y)                                       Free-withdrawal base at the anniversary
0.10 x FWB(y)           free_wd_allow(y)                                      Allowance for contract year y
FW(t)                   free_wd_avail(t)                                      Unused allowance at BOM of month t
(FW after W(t))         free_wd_remain(t)                                     Unused allowance after the withdrawal
W(t)                    wd_pp(t)                                              Gross amount removed from the AV
(free part of W)        wd_free_pp(t)                                         Free portion of W(t)
E(t) on a withdrawal    wd_excess_pp(t)                                       Withdrawal exposed to charge and MVA
E(t) on a surrender     surr_excess_pp(t)                                     Surrender exposed to charge and MVA
sc(y)                   surr_charge_rate(t)                                   Surrender charge rate in force
sc_clock(t)             surr_charge_year(t)                                   Year within the current schedule
(schedule key)          surr_charge_id(t)                                     initial / renewal / none
C(t)                    surr_charge_pp(t)                                     Charge on a full surrender
C(t) on a withdrawal    wd_charge_pp(t)                                       Charge on a partial withdrawal
mu(t)                   mva_rate(t)                                           MVA rate, signed
M(t)                    mva_pp(t)                                             Capped MVA on a full surrender
M(t) on a withdrawal    wd_mva_pp(t)                                          Capped MVA on a partial withdrawal
cap(.)                  mva_pp_on(t, base)                                    The capped MVA on any currency base
T(t)                    mva_term(t)                                           MVA duration in years
i0                      mva_ref_yield_locked(t)                               Reference yield locked at period start
it                      mva_ref_yield(t)                                      Reference yield at month t
Phi(t)                  mva_factor_geometric(a, b, tau) Geometric MVA factor
F_s                     mva_duration_factor(t)                                Declared-differential duration factor
P_accum@GMIR            prem_accum_gmir_pp(t)                                 Premium less prior withdrawals at the GMIR
s_adm                   mva_admin_spread                                      Geometric MVA expense adder (Reference)
SV(t)                   surr_value_pp(t)                                      Gross surrender value before the floor
SB(t)                   surr_benefit_pp(t)                                    Surrender benefit paid
gp_end(t)               gp_end(t)                                             Months left in the guarantee period
(the 30-day window)     in_gp_window(t)                                       True in the guarantee-period-end window
basis(t)                tax_basis_pp(t)                                       IRC 72 investment in the contract
(taxable part of W)     taxable_wd_pp(t)                                      Income-first taxable amount
l(t-1)                  pols_if(t)                                            In-force at the start of month t
l(0)                    pols_if_init                                          In-force at issue
l(t)                    pols_if_at(t, "AFT_DECR")                             In-force at the end of month t
(intra-month l)         pols_if_at(t, timing)                                 BEF_DECR / BEF_MORT / BEF_LAPSE / AFT_DECR
q(t)                    mort_rate_mth(t)                                      Monthly mortality rate
(annual q_x)            mort_rate(t)                                          Annual mortality at the attained age
w(t)                    lapse_rate_mth(t)                                     Monthly total surrender rate
w_annual(t)             lapse_rate(t)                                         Annual total surrender rate
Base(y)                 lapse_rate_base(t)                                    Prescribed base lapse by contract year
G                       gmir_factor                                           VM-22 GMIR factor
Market(t)               lapse_dyn_market(t)                                   Dynamic-lapse market term
Rate(t)                 lapse_dyn_rate(t)                                     Dynamic-lapse rate term
Phi_MVA(t)              mva_lapse_factor_at(t)                                MVA factor gating the dynamic term
BF                      lapse_buffer                                          Dynamic-lapse buffer factor (Reference)
X                       lapse_dyn_exponent(t)                                 Dynamic-lapse exponent
a(t)                    annuitization_rate(t)                                 Monthly annuitization election rate
l a                     pols_annuitization(t)                                 Annuitization elections
l (1-a) q               pols_death(t)                                         Deaths
l (1-a)(1-q) w          pols_lapse(t)                                         Full surrenders
(none)                  pols_maturity(t)                                      Deemed-maturity annuitizations
P at t = 0              premiums(t)                                           Premium income
(premium credited)      prem_to_av_pp(t)                                      Premium credited to the account value
W + M - C               withdrawals(t)                                        Withdrawal payments
(ledger benefit lines)  claims(t, kind)                                       Benefit outgo by kind
                        claim_pp(t, kind)                                     Benefit per contract by kind
                        claims_from_av(t, kind)                               Account value released by a claim
                        claims_over_av(t, kind)                               Benefit paid above the account value
0.02 x P                commissions(t)                                        Acquisition commission
(50/12) x 1.025^(y-1)   expenses(t)                                           Maintenance expense
premium tax             premium_taxes(t)                                      Premium tax
NetCF(t)                net_cf(t)                                             Net cash flow
======================  ====================================================  ==========================================

Six names needed care, and all six are collisions the notes themselves carry.

``d(t)`` in these notes is the **withdrawal deducted from the Model #805 floor** in
processing step 7, *not* deaths as in :mod:`.Term_US_A`; it becomes
:func:`mgsv_wd_deduct_pp`, leaving :func:`pols_death` unambiguous. ``c(t)`` is the monthly
slice of the annual contract charge, not conversions, and becomes
:func:`mgsv_charge_pp`. ``E(t)`` names two different currency bases — the excess of a
*withdrawal* over the free allowance and the excess of the whole *account value* over it
at a full surrender — which :func:`wd_excess_pp` and :func:`surr_excess_pp` separate; the
same symbol is expenses in :mod:`.Term_US_A`, which here is :func:`expenses`. ``X`` is
the dynamic-lapse exponent here and the premium tax in :mod:`.Term_US_A`, split into
:func:`lapse_dyn_exponent` and :func:`premium_taxes`. ``T(t)`` is the MVA duration in
*years* while ``t`` is the policy *month*, so it becomes :func:`mva_term`. And the floor
itself carries three labels in the sources — MGSV in this library, "GMSV" in the specimen
[S11], "MGV" in the fixed-indexed annuity notes — one concept, named :func:`mgsv_pp`
throughout.

Two further names carry a **library-wide** convention that differs from the notes' own
indexing, and in both cases the notes' quantity survives under a second name rather than
being dropped.

:func:`pols_if` is the count in force at the **start** of month ``t``, matching
:mod:`.Term_US_A` (``pols_if(1) == pols_if_init()``) and ``savings.CashValue_SE``, and it
is the weight applied to that same month's cash flows — :func:`withdrawals`,
:func:`expenses` and the ``pols_if`` column of :func:`result_cf` now reconcile row by row,
which they did not while ``pols_if`` was the closing count. The notes' end-of-month
``l(t)`` is unchanged and unmoved; it is read as ``pols_if_at(t, "AFT_DECR")``, and
``pols_if(t + 1) == pols_if_at(t, "AFT_DECR")`` in every month but the last, where
:func:`pols_maturity` empties the block.

:func:`lapse_rate` is the **annual** total surrender rate and :func:`lapse_rate_mth` the
monthly one, matching the :func:`mort_rate` / :func:`mort_rate_mth` pair and the eight
other models that spell it that way. The notes write the monthly rate ``w(t)`` and the
annual rate ``w_annual(t)``, so the pairing here is the notes' own — only the suffixes
move.

Three rows of the table above are **References, not Cells**, because the notes give each
as a single assumption number rather than a function of ``t``: ``s_ren`` is
``renewal_spread``, the spread in ``i_cr^ren(t) = max(GMIR, MR(t) - s_ren)`` (0.00% on the
base run, 1.00% in the notes' scenario **[std]**); ``BF`` is ``lapse_buffer``, the 50 bp
band inside which the dynamic-lapse response is exactly zero; and ``s_adm`` is
``mva_admin_spread``, the 25 bp administrative-expense adder in the geometric MVA's
denominator, which is 0 in Voya's variant [S3][S4]. Rebasing any of the three is an
assignment to the Reference, with no formula change. ``P_accum@GMIR``, by contrast, is a
recursion and so a Cells: :func:`prem_accum_gmir_pp` is the level the ``gmir_floor`` cap
holds ``AV + M`` above [S13].

Two quantities the notes list as *model point attributes* are computed here instead,
because each is fixed by a rule the notes also state: ``av_initial`` is
``premium_pp() * (1 - load_prem_rate)`` with no front-end load [S5][S10][S16], and
``mgsv_initial`` is ``net_consideration_ratio * premium_pp()`` — 87.5% of gross
consideration [R1 4.A(2)]. Only ``tax_basis_initial`` stays a model point column, because
it genuinely varies with tax status.

.. rubric:: Timing arguments

Account value, following ``CashValue_SE``'s ``av_pp_at``:

``"BEF_WD"``
    ``AV(t-1)``, at the start of month ``t`` before the elective withdrawal.
``"BEF_INV"``
    ``AV'(t)``, after the withdrawal and after annuitization elections, before crediting.
``"EOM"``
    ``AV(t)``, after crediting. Equal to :func:`av_pp`.

Policy counts, following ``CashValue_SE``'s ``pols_if_at``:

``"BEF_DECR"``
    ``l(t-1)``, in force at the start of month ``t``. Equal to :func:`pols_if`.
``"BEF_MORT"``
    after annuitization elections, ``l(t-1)(1 - a(t))``.
``"BEF_LAPSE"``
    after deaths, ``l(t-1)(1 - a(t))(1 - q(t))``.
``"AFT_DECR"``
    after surrenders, ``l(t)`` — the notes' end-of-month in-force.

Benefit ``kind`` arguments are ``"DEATH"``, ``"LAPSE"``, ``"ANNUITIZATION"`` and
``"MATURITY"``. Any other value of any of these raises ``ValueError``.

.. rubric:: pols_maturity and the projection horizon

The technical notes state no projection horizon: a MYGA under the ``rollover``
architecture renews indefinitely, and the notes' own base-lapse pattern is written as a
repeating five-year cycle with no terminal date. The model runs to the contract
anniversary at attained age ``maturity_age`` = 100 **[std]** — the last attained age in
the sourced cap band on the renewal surrender charge, which the notes tabulate as 4% at
94, 3% at 95, 2% at 96, 1% at 97 and 0% at 98-100 [S1][S2]. The cap *reaches* zero at 98;
100 is where the sourced band stops, and it is past the statutory deemed maturity date of
Model #805 section 8 [R1]. The survivors at that
anniversary are annuitized out through :func:`pols_maturity`, zero in every month but the
last, so that

    pols_if(t) - pols_if(t+1) = pols_annuitization(t) + pols_death(t)
                                + pols_lapse(t) + pols_maturity(t)

holds for every ``t`` — the start-of-month count opens the row, the four exits are taken
during it and the next month opens on what is left. Including the last month, where the
block would otherwise appear to
lose lives with no cause. The name follows ``BasicTerm_S.pols_maturity`` and the
construction follows :mod:`.Term_US_A`.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The contract identifier of the selected model point."""
    return model_point()["policy_id"]


def age_at_entry():
    """The issue age (ANB) of the selected model point."""
    return int(model_point()["age_at_entry"])


def sex():
    """The sex of the selected model point, M or F."""
    return model_point()["sex"]


def tax_status():
    """Tax status of the contract: NQ, IRA, Roth or inherited.

    Reported only. The base run is non-qualified **[std]**; no RMD module is implemented.
    """
    return model_point()["tax_status"]


def premium_pp():
    """P: the single purchase payment per contract."""
    return float(model_point()["premium"])


def pols_if_init():
    """l(0): in-force probability at issue, 1 for a single-contract model point."""
    return float(model_point()["pols_if_init"])


def guar_period():
    """n: the guarantee period in years; the surrender charge and MVA periods equal it."""
    return int(model_point()["guar_period"])


def declared_rate_initial():
    """The declared credited rate guaranteed for the initial term, 4.45% p.a. [S11]."""
    return float(model_point()["declared_rate_initial"])


def gmir():
    """The guaranteed minimum interest rate, 0.25% p.a. [S11]; a floor on any declared rate."""
    return float(model_point()["gmir"])


def mgsv_rate():
    """i_nf: the contract GMSV accumulation rate, 2.80% p.a. [S11].

    The Model #805 floor accretes at this rate. It must be at least the statutory indexed
    rate :func:`mgsv_rate_statutory`; crediting the floor at more is permitted and simply
    produces a higher floor [R1 4.B].
    """
    return float(model_point()["mgsv_rate"])


def mgsv_annual_charge():
    """The annual contract charge deducted from the Model #805 floor.

    $0 representative [S11]; the statutory maximum is $50 p.a. [R1 4.A].
    """
    return float(model_point()["mgsv_annual_charge"])


def mgsv_wd_convention():
    """How a withdrawal reduces the Model #805 floor: ``gross`` or ``net_of_charges``.

    ``gross`` [S11] deducts W(t) itself; ``net_of_charges`` [S9] deducts the cash actually
    paid, W(t) + M(t) - C(t), keeping the floor higher. Both are live in the market and
    the difference compounds at i_nf for the rest of the contract.
    """
    return model_point()["mgsv_wd_convention"]


def renewal_architecture():
    """``rollover`` (Camp A) or ``annual_redeclare`` (Camp B).

    ``rollover`` starts a fresh guarantee period, surrender charge schedule and MVA period
    at each boundary [S1][S2][S5][S11], so the shock lapse repeats every n years.
    ``annual_redeclare`` redeclares the rate each anniversary with no further surrender
    charge and no MVA [S13], so the shock happens once.
    """
    return model_point()["renewal_architecture"]


def free_wd_rule():
    """``pct_av`` or ``interest_only``.

    ``pct_av`` [S10] is the representative 10%-of-base allowance; ``interest_only``
    [S5][S6] is the prior contract year's credited interest. The notes' third value,
    ``greatest_of`` [S13], is **not implemented**: no formula is given for it.
    """
    return model_point()["free_wd_rule"]


def free_wd_rate():
    """The free-withdrawal percentage under ``pct_av``, 10% [S10]."""
    return float(model_point()["free_wd_rate"])


def free_wd_mva_exempt():
    """Whether the free allowance is exempt from the surrender charge **and** the MVA.

    True is the retail MYGA convention **[std]** [S8][S11] and gives
    ``E(t) = AV(t) - FW(t)``. False is the registered-contract convention [S3][S4] and
    gives ``E(t) = AV(t)``, collapsing the surrender benefit to the multiplicative form
    ``max(AV(t) x (1 + mu(t) - sc(y)), MGSV(t))``. The notes apply the flag to both the
    charge and the adjustment; in the market it strictly concerns the adjustment.
    """
    return bool(model_point()["free_wd_mva_exempt"])


def mva_family():
    """``linear_duration``, ``geometric`` or ``declared_differential``. All implemented."""
    return model_point()["mva_family"]


def mva_cap_rule():
    """``sym_sc``, ``min_sc_interest``, ``asym_sc_snfl``, ``gmir_floor`` or ``none``.

    The cap, not the formula family, is the largest cross-carrier divergence in the source
    set, so it is a first-class model parameter. See :func:`mva_pp_on`.
    """
    return model_point()["mva_cap_rule"]


def mva_ref_yield_at_issue():
    """i0 at issue: the MVA reference yield locked for the initial period, 5.00% **[std]**."""
    return float(model_point()["mva_ref_yield_at_issue"])


def premium_tax_rate():
    """Premium tax deducted from the contract, 0% **[std]** [S3][S16]."""
    return float(model_point()["premium_tax_rate"])


def tax_basis_pp_init():
    """basis(0): the IRC 72 investment in the contract at issue [R6]."""
    return float(model_point()["tax_basis_initial"])


def scenario_id():
    """The rate scenario the model point runs on, a key into *rate_scenario.csv*."""
    return model_point()["scenario_id"]


def wd_schedule_id():
    """The withdrawal programme, a key into *withdrawal_table.csv*."""
    return model_point()["wd_schedule_id"]


def policy_term():
    """Contract term in years: issue to the anniversary at ``maturity_age`` **[std]**."""
    return maturity_age - age_at_entry()                             # noqa: F821


def proj_len():
    """Projection length in policy months, ``12 * policy_term()``."""
    return 12 * policy_term()


def duration_mth(t):
    """Policy months elapsed at the end of month t. The projection index itself."""
    return t


def policy_year(t):
    """y(t) = ceil(t / 12): the contract year containing month t; 0 at issue."""
    return (t + 11) // 12


def duration(t):
    """Completed contract years at month t, ``policy_year(t) - 1`` and 0 at issue."""
    return max(0, policy_year(t) - 1)


def age(t):
    """The attained age (ANB) during month t."""
    return age_at_entry() + duration(t)


def gp_index(t):
    """The index of the guarantee period containing month t: 1 for months 1..12n."""
    return (t + 12 * guar_period() - 1) // (12 * guar_period())


def gp_start_month(t):
    """The month boundary at which the current guarantee period began; 0 for the first."""
    return 12 * guar_period() * (gp_index(t) - 1)


def gp_end(t):
    """Months remaining in the current guarantee period."""
    if t < 1:
        return 12 * guar_period()
    return 12 * guar_period() * gp_index(t) - t


def in_gp_window(t):
    """True in the 30-day guarantee-period-end window [S1][S2][S5][S6].

    The notes place the window in the month *after* a guarantee period closes, i.e. at
    ``t - 1 == 0 (mod 12n)`` with ``t > 1``, so for n = 5 it is months 61, 121, 181, ...
    In the window the full account value is available with **no surrender charge and no
    MVA**, and it is the only month in which annuitization is elected. Under
    ``annual_redeclare`` there is exactly one window, at the end of the initial term.
    """
    n12 = 12 * guar_period()
    if t <= 1 or (t - 1) % n12 != 0:
        return False
    if renewal_architecture() == "annual_redeclare":
        return t == n12 + 1
    return True


def redeclare_month(t):
    """The month at which the credited rate in force at month t was declared."""
    n12 = 12 * guar_period()
    if t <= n12:
        return 1
    if renewal_architecture() == "rollover":
        return n12 * (gp_index(t) - 1) + 1
    return 12 * (policy_year(t) - 1) + 1


def scenario_rate(t, name):
    """Step-function lookup of column ``name`` in the model point's rate scenario.

    Each row of *rate_scenario.csv* states the level that holds from its own month until
    the next row of the same scenario, so a flat path is one row.
    """
    sub = data.rate_scenario().loc[scenario_id()]                    # noqa: F821
    months = [i for i in sub.index if i <= max(t, 0)]
    return float(sub.loc[max(months), name])


def market_rate(t):
    """MR(t): the market competitor rate driving renewal declarations and dynamic lapse.

    VM-22 defines it for a 5 to 7 year guarantee period as the 7-year Treasury rate plus a
    50% A / 50% AA spread less the pricing spread [R2 6.B.5]; the model takes it as an
    exogenous input because the index is a state-filed variable **[std]**.
    """
    return scenario_rate(t, "market_rate")


def mva_ref_yield(t):
    """it: the MVA reference yield at month t, from the scenario table **[std]**.

    The source design is Barclay's US Credit Index with a state-varying formula [S8]; the
    model takes a scalar series rather than hard-coding an index.
    """
    return scenario_rate(t, "mva_ref_yield")


def credit_rate(t):
    """i_cr(t): the declared credited rate in force, effective annual.

    The initial declared rate for the whole initial term [S11], then the renewal rule
    ``max(GMIR, MR(m) - s_ren)`` **[std]** with ``m`` the redeclaration month. The base
    run sets ``renewal_spread = 0``, so the credited rate equals the competitor rate and
    the dynamic lapse term is exactly zero.
    """
    if t <= 12 * guar_period():
        return declared_rate_initial()
    return max(gmir(), market_rate(redeclare_month(t)) - renewal_spread)  # noqa: F821


def credit_rate_mth(t):
    """The monthly credited rate, ``(1 + i_cr(t))^(1/12) - 1``.

    Twelve of these factors reproduce the declared effective annual rate exactly, so the
    discretization moves interest only *within* a month. Do not compound daily as well.
    """
    return (1.0 + credit_rate(t)) ** (1.0 / 12.0) - 1.0


def mgsv_rate_mth():
    """The monthly GMSV accumulation rate, ``(1 + i_nf)^(1/12) - 1``."""
    return (1.0 + mgsv_rate()) ** (1.0 / 12.0) - 1.0


def mgsv_rate_statutory(cmt5):
    """The Model #805 indexed nonforfeiture rate at a 5-year CMT level [R1 4.B].

    ``max(0.0015, min(0.03, round(CMT5 to 1/20 of 1%) - 0.0125))``. Two traps the notes
    call out: the floor is **15 basis points, not the widely repeated 1%**; and the
    statute *defines* the minimum rate, it does not cap the contract rate — the contract
    must satisfy ``mgsv_rate() >= mgsv_rate_statutory(cmt5)``, which is what
    :func:`mgsv_rate_is_compliant` tests, not the reverse inequality.
    """
    step = mgsv_stat_step                                            # noqa: F821
    rounded = math.floor(cmt5 / step + 0.5) * step                   # noqa: F821
    return max(mgsv_stat_floor,                                      # noqa: F821
               min(mgsv_stat_cap, rounded - mgsv_stat_spread))       # noqa: F821


def mgsv_rate_is_compliant(cmt5):
    """True when the contract GMSV rate meets the statutory minimum at that CMT5 [R1 4.B]."""
    return mgsv_rate() >= mgsv_rate_statutory(cmt5)


def av_pp_init():
    """AV(0) = P: 100% of premium credited, no front-end load [S5][S10][S16]."""
    return premium_pp() * (1.0 - load_prem_rate)                     # noqa: F821


def prem_to_av_pp(t):
    """Premium credited to the account value per contract; the whole premium at t = 0."""
    return av_pp_init() if t == 0 else 0.0


def wd_scheduled_pp(t):
    """The gross withdrawal scheduled for month t in *withdrawal_table.csv*, else zero."""
    if t < 1:
        return 0.0
    table = data.withdrawal_table()                                  # noqa: F821
    key = (wd_schedule_id(), t)
    return float(table.loc[key, "wd_amount"]) if key in table.index else 0.0


def wd_pp(t):
    """W(t): the gross amount removed from the account value at BOM of month t.

    Gross by construction: a contract promising a stated *net* check needs a gross-up
    solve, which is **not implemented** [S3]. Two sources add up here — the amount
    scheduled in *withdrawal_table.csv*, and the free-withdrawal utilization variant
    ``free_wd_util x FW(y)`` taken in the first month of each contract year. Base run
    utilization is 0 **[std]**, so on model points other than the worked-example anchor
    the account value runs unbroken.
    """
    if t < 1:
        return 0.0
    util = 0.0
    if free_wd_util and (t == 1 or policy_year(t) != policy_year(t - 1)):  # noqa: F821
        util = free_wd_util * free_wd_allow(policy_year(t))          # noqa: F821
    return wd_scheduled_pp(t) + util


def av_pp(t):
    """AV(t): account value per contract at the end of policy month t.

    ``AV(t) = (AV(t-1) - W(t)) x (1 + i_cr(t))^(1/12)`` with ``AV(0) = P``
    [S4][S5][S16]. No charges are deducted from the account value: this chassis carries no
    front-end load, no annual fee and no rider charges [S5][S10][S13][S16].
    """
    if t <= 0:
        return av_pp_init()
    return (av_pp(t - 1) - wd_pp(t)) * (1.0 + credit_rate_mth(t))


def av_pp_at(t, timing):
    """Account value per contract at month t, read at the point given by ``timing``.

    ``"BEF_WD"`` is ``AV(t-1)``, ``"BEF_INV"`` is ``AV'(t) = AV(t-1) - W(t)`` and
    ``"EOM"`` is ``AV(t)``. At t = 0 all three are the premium.
    """
    if t < 1:
        return av_pp_init()
    if timing == "BEF_WD":
        return av_pp(t - 1)
    elif timing == "BEF_INV":
        return av_pp(t - 1) - wd_pp(t)
    elif timing == "EOM":
        return av_pp(t)
    else:
        raise ValueError("invalid timing")


def inv_income_pp(t):
    """Interest credited to one contract's account value at the end of month t."""
    if t < 1:
        return 0.0
    return av_pp_at(t, "BEF_INV") * credit_rate_mth(t)


def interest_credited_pp(t):
    """Cumulative interest credited to one contract from issue to the end of month t.

    Used by the ``min_sc_interest`` MVA cap, which limits the adjustment to the lesser of
    the surrender charge and the interest credited to date [S8][S9].
    """
    if t <= 0:
        return 0.0
    return interest_credited_pp(t - 1) + inv_income_pp(t)


def prem_accum_gmir_pp(t):
    """Premium less prior withdrawals accumulated at the GMIR.

    The reference level for the ``gmir_floor`` MVA cap, under which ``AV + M`` may not
    fall below it [S13]; the surrender charge may still breach that level.
    """
    if t <= 0:
        return premium_pp()
    return (prem_accum_gmir_pp(t - 1) - wd_pp(t)) * (1.0 + gmir()) ** (1.0 / 12.0)


def free_wd_base(y):
    """FWB(y): the free-withdrawal base fixed at the start of contract year y.

    Purchase payments in year 1, the account value at the most recent anniversary
    thereafter [S10]. Making the base a *fixed known amount* at each anniversary is what
    lets ``E(t) = AV(t) - FW(t)`` be evaluated without a fixed point.
    """
    return premium_pp() if y <= 1 else av_pp(12 * (y - 1))


def free_wd_allow(y):
    """The free-withdrawal allowance for contract year y, non-cumulative [S4][S16].

    ``pct_av``: ``free_wd_rate x FWB(y)`` [S10]. ``interest_only``: the interest credited
    over the prior contract year [S5][S6], hence zero in year 1. ``greatest_of`` [S13] is
    not implemented and raises.
    """
    rule = free_wd_rule()
    if rule == "pct_av":
        return free_wd_rate() * free_wd_base(y)
    elif rule == "interest_only":
        if y <= 1:
            return 0.0
        return (interest_credited_pp(12 * (y - 1))
                - interest_credited_pp(12 * max(0, y - 2)))
    else:
        raise ValueError("invalid free_wd_rule")


def free_wd_avail(t):
    """FW(t): the unused free-withdrawal allowance at BOM of month t, before W(t).

    Reset to the whole allowance in the first month of each contract year; carried
    forward within the year; never carried across an anniversary [S4][S16].
    """
    if t < 1:
        return 0.0
    if t == 1 or policy_year(t) != policy_year(t - 1):
        return free_wd_allow(policy_year(t))
    return free_wd_remain(t - 1)


def wd_free_pp(t):
    """The portion of W(t) covered by the free allowance, hence free of charge and MVA."""
    return min(wd_pp(t), free_wd_avail(t))


def free_wd_remain(t):
    """The unused free-withdrawal allowance after month t's withdrawal.

    This, not :func:`free_wd_avail`, is the allowance a full surrender at the end of month
    t may still shelter.
    """
    return free_wd_avail(t) - wd_free_pp(t)


def wd_excess_pp(t):
    """E(t) for a partial withdrawal: ``max(0, W(t) - FW(t))`` [S8][S9][S10].

    The whole of W(t) when ``free_wd_mva_exempt`` is False [S3][S4].
    """
    if free_wd_mva_exempt():
        return max(0.0, wd_pp(t) - free_wd_avail(t))
    return wd_pp(t)


def surr_excess_pp(t):
    """E(t) for a full surrender at the end of month t: ``AV(t) - FW(t)`` [S8][S11].

    The whole of AV(t) when ``free_wd_mva_exempt`` is False [S3][S4].
    """
    if free_wd_mva_exempt():
        return max(0.0, av_pp(t) - free_wd_remain(t))
    return av_pp(t)


def surr_charge_id(t):
    """The surrender charge schedule in force: ``initial``, ``renewal`` or ``none``.

    Under ``rollover`` a fresh renewal schedule attaches at each guarantee-period boundary
    [S1][S2][S11]; under ``annual_redeclare`` no charge applies after the initial term
    [S13]. Getting this clock wrong relocates the shock lapse by years.
    """
    if t < 1:
        return "none"
    if gp_index(t) <= 1:
        return "initial"
    if renewal_architecture() == "annual_redeclare":
        return "none"
    return "renewal"


def surr_charge_year(t):
    """sc_clock: the contract year within the schedule in force, 1..n.

    Resets to 1 at each renewal under ``rollover`` [S1][S2][S11]. Voya and Nationwide
    instead run the clock from the original purchase payment date so it never restarts
    [S3][S4]; that variant is not carried on this chassis.
    """
    return policy_year(t) - guar_period() * (gp_index(t) - 1)


def surr_charge_age_cap(t):
    """The attained-age cap on the surrender charge: 4% at 94 down to 0% at 98+ [S1][S2].

    Returns 1.0 below the sourced age band, i.e. no cap.
    """
    table = data.surr_charge_age_cap_table()                         # noqa: F821
    attained = age(t)
    lo, hi = int(table.index.min()), int(table.index.max())
    if attained < lo:
        return 1.0
    return float(table.loc[min(attained, hi), "surr_charge_cap"])


def surr_charge_rate(t):
    """sc(y): the surrender charge rate in force at month t.

    9/8/7/6/5 over the initial term [S10] and 5/4/3/2/1 over a renewal term [S2], capped
    by the attained-age scale [S1][S2], zero once a schedule runs out, and zero in the
    30-day guarantee-period-end window and before issue [S1][S2].
    """
    schedule = surr_charge_id(t)
    if schedule == "none" or in_gp_window(t):
        return 0.0
    key = (schedule, surr_charge_year(t))
    table = data.surr_charge_table()                                 # noqa: F821
    if key not in table.index:
        return 0.0
    return min(float(table.loc[key, "surr_charge_rate"]), surr_charge_age_cap(t))


def mva_term(t):
    """T(t): the MVA duration in years at the end of month t [S8].

    The notes write it as (days to the end of the current contract year / 365) + whole
    years remaining in the MVA period. On a monthly grid those two terms collapse
    algebraically to ``(12 n k - t) / 12`` — the time to the end of the current MVA
    period — and the same quantity serves as the geometric branch's ``tau``, which the
    notes define as days to maturity / 365.25. The two divisors differ in the sources; on
    exact twelfths they cannot.
    """
    if t < 1:
        return 0.0
    if renewal_architecture() == "annual_redeclare" and t > 12 * guar_period():
        return 0.0
    months_to_year_end = 12 * policy_year(t) - t
    whole_years_left = guar_period() * gp_index(t) - policy_year(t)
    return months_to_year_end / 12.0 + whole_years_left


def mva_in_force(t):
    """True when an MVA applies at month t.

    ``mu(t) = 0`` unconditionally once the MVA period has expired [S8][S13][S16] and in
    the 30-day guarantee-period-end window [S2]. It is also zero on a death benefit
    [S2][S4][S8][S13][S16], on annuitization [S16], and on RMD or waiver withdrawals
    [S2][S5][S13]; the first two are handled where those benefits are valued and the
    third is not implemented.
    """
    return mva_term(t) > 0.0 and not in_gp_window(t)


def mva_ref_yield_locked(t):
    """i0: the reference yield locked at the start of the current guarantee period.

    The model point's issue value for the initial term; re-locked at the prevailing
    reference yield at each renewal under ``rollover`` [S2][S11].
    """
    if gp_index(t) <= 1:
        return mva_ref_yield_at_issue()
    return mva_ref_yield(gp_start_month(t))


def mva_ref_term_years(tau):
    """The whole-year maturity at which the distribution yield is read [S4].

    Partial years round **up**, capped at the guarantee period: the Nationwide contract
    reads a 3-year yield for 985/365.25 = 2.69 years remaining while the exponent keeps
    the exact day count. With a single scalar reference yield per scenario this selection
    determines nothing; it is carried so a curve-valued extension has the rule in place.
    """
    return min(guar_period(), int(math.ceil(tau)))                   # noqa: F821


def mva_factor_geometric(i_deposit, i_dist, tau):
    """Phi: the geometric MVA factor ``((1+a)/(1+b+s_adm))^tau`` [S3][S4].

    ``s_adm`` is ``mva_admin_spread``, 25 bp in the Nationwide contract, covering the cost
    of liquidating fixed-income investments and structurally biasing the adjustment
    against the owner; Voya's variant sets it to zero [S3].
    """
    return ((1.0 + i_deposit) / (1.0 + i_dist + mva_admin_spread)) ** tau  # noqa: F821


def mva_duration_factor(t):
    """F_s: the declared-differential adjustment factor by years remaining [S14].

    A contractual table of modified durations, read on the ``Ic < 6%`` or ``Ic >= 6%``
    column and linearly interpolated between whole years, flat beyond the last row.
    """
    table = data.mva_factor_table()                                  # noqa: F821
    column = ("factor_lo" if credit_rate(t) < mva_factor_rate_split  # noqa: F821
              else "factor_hi")
    years = mva_term(t)
    last = int(table.index.max())
    lower = int(math.floor(years))                                   # noqa: F821
    if lower >= last:
        return float(table.loc[last, column])
    f0 = float(table.loc[lower, column])
    f1 = float(table.loc[lower + 1, column])
    return f0 + (f1 - f0) * (years - lower)


def mva_rate(t):
    """mu(t): the market value adjustment rate at month t, signed and dimensionless.

    ``linear_duration`` **[std]**: ``(i0 - it) x T(t)`` [S8][S9] — the first-order
    approximation of the geometric form, always in the contract holder's disfavour when
    rates rise. ``geometric``: ``Phi(t) - 1`` [S3][S4]. ``declared_differential``:
    ``(Ic - In) x F_s`` on the insurer's own new-money rate [S14], with ``In`` taken as
    the market rate **[std]**.
    """
    if not mva_in_force(t):
        return 0.0
    family = mva_family()
    if family == "linear_duration":
        return (mva_ref_yield_locked(t) - mva_ref_yield(t)) * mva_term(t)
    elif family == "geometric":
        return mva_factor_geometric(
            mva_ref_yield_locked(t), mva_ref_yield(t), mva_term(t)) - 1.0
    elif family == "declared_differential":
        return (credit_rate(t) - market_rate(t)) * mva_duration_factor(t)
    else:
        raise ValueError("invalid mva_family")


def mva_pp_on(t, base):
    """M: the capped MVA amount on a currency base at month t.

    Five cap rules, all first-class parameters because the cap is the largest single
    cross-carrier divergence in the source set:

    ``sym_sc`` **[std]**
        ``clamp(M_raw, -C, +C)`` [S2].
    ``min_sc_interest``
        ``clamp(M_raw, -K, +K)`` with ``K = min(C, interest credited to date)`` [S8][S9].
    ``asym_sc_snfl``
        ``M <= +C`` with no downside cap; only ``SB >= MGSV`` binds below [S12].
    ``gmir_floor``
        ``AV + M >=`` premium less prior withdrawals accumulated at the GMIR [S13]. The
        floor is stated for a full surrender; applying it to a partial withdrawal base is
        an extension of the source.
    ``none``
        Uncapped and fully two-sided [S3][S4].
    """
    raw = mva_rate(t) * base
    rule = mva_cap_rule()
    if rule == "none":
        return raw
    charge = surr_charge_rate(t) * base
    if rule == "sym_sc":
        return max(-charge, min(charge, raw))
    elif rule == "min_sc_interest":
        limit = min(charge, interest_credited_pp(t))
        return max(-limit, min(limit, raw))
    elif rule == "asym_sc_snfl":
        return min(charge, raw)
    elif rule == "gmir_floor":
        return max(raw, prem_accum_gmir_pp(t) - av_pp(t))
    else:
        raise ValueError("invalid mva_cap_rule")


def surr_charge_pp(t):
    """C(t): the surrender charge on a full surrender at the end of month t."""
    return surr_charge_rate(t) * surr_excess_pp(t)


def mva_pp(t):
    """M(t): the capped MVA on a full surrender at the end of month t."""
    return mva_pp_on(t, surr_excess_pp(t))


def wd_charge_pp(t):
    """The surrender charge on month t's partial withdrawal."""
    return surr_charge_rate(t) * wd_excess_pp(t)


def wd_mva_pp(t):
    """The capped MVA on month t's partial withdrawal."""
    return mva_pp_on(t, wd_excess_pp(t))


def wd_payment_pp(t):
    """The cash paid on month t's withdrawal, ``W(t) + M(t) - C(t)``."""
    return wd_pp(t) + wd_mva_pp(t) - wd_charge_pp(t)


def surr_value_pp(t):
    """SV(t): the gross surrender value, ``AV(t) + M(t) - C(t)``, before the floor.

    The composition order is **account value, then MVA, then surrender charge, then the
    nonforfeiture floor**, and it is not interchangeable: both M and C are computed on
    E(t) *before* either is deducted [S8]. Charging first and adjusting the net figure
    understates the adjustment by ``sc x |M|``; flooring before the MVA silently removes
    the downside protection.
    """
    return av_pp(t) + mva_pp(t) - surr_charge_pp(t)


def surr_benefit_pp(t):
    """SB(t): the surrender benefit actually paid, ``max(SV(t), MGSV(t))`` [S8][S9][S12].

    A binding floor is **not** a separate cash flow: it raises SB(t), and
    ``MGSV(t) - SV(t)`` is a reconciliation quantity only.
    """
    return max(surr_value_pp(t), mgsv_pp(t))


def mgsv_pp_init():
    """MGSV(0) = 87.5% of gross consideration [R1 4.A(2)][S11]."""
    return net_consideration_ratio * premium_pp()                    # noqa: F821


def mgsv_charge_pp(t):
    """c(t): the monthly slice of the annual contract charge deducted from the floor."""
    return 0.0 if t < 1 else mgsv_annual_charge() / 12.0


def mgsv_wd_deduct_pp(t):
    """d(t): the withdrawal deducted from the Model #805 floor in month t.

    W(t) under the ``gross`` convention [S11]; the cash actually paid,
    ``W(t) + M(t) - C(t)``, under ``net_of_charges`` [S9].
    """
    if t < 1:
        return 0.0
    convention = mgsv_wd_convention()
    if convention == "gross":
        return wd_pp(t)
    elif convention == "net_of_charges":
        return wd_payment_pp(t)
    else:
        raise ValueError("invalid mgsv_wd_convention")


def mgsv_pp(t):
    """MGSV(t): the Model #805 minimum guaranteed surrender value at end of month t.

    ``MGSV(t) = [MGSV(t-1) - d(t) - c(t)] x (1 + i_nf)^(1/12)`` with
    ``MGSV(0) = 0.875 x P`` [R1 4.A][S11]. Premium tax actually paid and indebtedness are
    further permitted deductions, accumulated at the same rate, and are zero here.
    """
    if t <= 0:
        return mgsv_pp_init()
    return ((mgsv_pp(t - 1) - mgsv_wd_deduct_pp(t) - mgsv_charge_pp(t))
            * (1.0 + mgsv_rate_mth()))


def taxable_wd_pp(t):
    """The income-first taxable portion of month t's withdrawal [R6 72(e)(3)(A)].

    Taxable to the extent the account value **gross of surrender charge** exceeds the
    basis. A reported quantity: it generates no insurer cash flow.
    """
    gain = max(0.0, av_pp_at(t, "BEF_WD") - tax_basis_pp(t - 1))
    return min(wd_pp(t), gain)


def tax_basis_pp(t):
    """basis(t): the IRC 72 investment in the contract at the end of month t [R6].

    Reduced only by the non-taxable remainder of a withdrawal. Reported, not a cash flow.
    """
    if t <= 0:
        return tax_basis_pp_init()
    return tax_basis_pp(t - 1) - (wd_pp(t) - taxable_wd_pp(t))


def mort_rate(t):
    """The annual mortality rate at the attained age and sex, from *mort_table.csv*.

    The shipped table is an illustrative Makeham curve **[std]**, *not* a published
    basis. The prescribed basis is the 2012 IAM Basic table with Projection Scale G2 and
    the VM-22 Table 6.7 factors [R2 6.B.8][R9], which may not be redistributed here;
    swap it in by repointing ``Data.mort_table_file``. Mortality is second-order on this
    product: death pays the full account value with no charge and no MVA.
    """
    return float(data.mort_table().loc[(age(t), sex()), "mort_rate"])   # noqa: F821


def mort_rate_mth(t):
    """q(t): the monthly mortality rate, ``1 - (1 - q_x)^(1/12)``."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def gmir_factor():
    """G: the VM-22 GMIR factor stepping the base lapse rate [R2 6.B.5].

    1.25 at a GMIR of 1.0% or less, 1.00 up to 2.5%, 0.70 above. The representative 0.25%
    GMIR [S11] therefore takes the **highest** multiplier, which is the conservative end
    of the prescribed scale.
    """
    rate = gmir()
    if rate <= gmir_band_low:                                        # noqa: F821
        return gmir_factor_low                                       # noqa: F821
    elif rate <= gmir_band_high:                                     # noqa: F821
        return gmir_factor_mid                                       # noqa: F821
    else:
        return gmir_factor_high                                      # noqa: F821


def lapse_rate_base(t):
    """Base(y): the prescribed base lapse rate for the contract year containing month t.

    VM-22 Table 6.5 mapped onto the five-year architecture as a **[std] extension**
    [R2][REG-R36]. ``rollover``: 1% inside each guarantee period and 75% in the contract
    year following each expiry, repeating with period n. ``annual_redeclare``: 1% to
    expiry, 75%, then 10%, 7.5% and 3% thereafter. **The architecture switch, not the
    level, is the first-order modeling decision** — Camp A creates a repeating shock,
    Camp B a single one.
    """
    year = policy_year(t)
    n = guar_period()
    if renewal_architecture() == "rollover":
        if year > n and (year - 1) % n == 0:
            return lapse_base_shock                                  # noqa: F821
        return lapse_base_igp                                        # noqa: F821
    if year <= n:
        return lapse_base_igp                                        # noqa: F821
    elif year == n + 1:
        return lapse_base_shock                                      # noqa: F821
    elif year == n + 2:
        return lapse_base_post1                                      # noqa: F821
    elif year == n + 3:
        return lapse_base_post2                                      # noqa: F821
    else:
        return lapse_base_ult                                        # noqa: F821


def lapse_dyn_exponent(t):
    """X: 2.0 during the initial surrender charge period, 2.5 at the shock and after [R2]."""
    if policy_year(t) <= guar_period():
        return lapse_exp_sc                                          # noqa: F821
    return lapse_exp_post                                            # noqa: F821


def lapse_dyn_market(t):
    """Market(t): the credited-minus-competitor response of the VM-22 dynamic lapse form.

    ``-1.25 (CR - MR)^X`` when the contract is competitive, zero inside the 50 bp buffer,
    ``+1.25 (MR - BF - CR)^X`` when it is not [R2 6.B.5]. The buffer and the power make
    the sensitivity strongly convex around ``CR = MR``.
    """
    cr, mr = credit_rate(t), market_rate(t)
    power = lapse_dyn_exponent(t)
    if cr >= mr:
        return -lapse_slope * (cr - mr) ** power                     # noqa: F821
    elif cr >= mr - lapse_buffer:                                    # noqa: F821
        return 0.0
    else:
        return lapse_slope * (mr - lapse_buffer - cr) ** power       # noqa: F821


def lapse_dyn_rate(t):
    """Rate(t): the dynamic term gated by the surrender-charge and negative-MVA haircut.

    ``Market(t) x max(0, 1 - 5 (1 - CSV/AV))`` with ``CSV/AV = SB(t)/AV(t)`` [R2 6.B.5],
    so the dynamic response switches off entirely once the combined haircut reaches 20%.
    The ITM factor is 1 for an Accumulation contract with no guaranteed living or death
    benefit, which the guideline states explicitly.
    """
    haircut = 1.0 - surr_benefit_pp(t) / av_pp(t)
    return lapse_dyn_market(t) * max(0.0, 1.0 - lapse_itm_gate * haircut)  # noqa: F821


def mva_lapse_factor_at(t):
    """Phi_MVA(t): the factor multiplying the dynamic term while an MVA is in force.

    The VM-22 prescribed values are 0 in force and 1 expired [R2], i.e. the regulator's
    view is that an in-force MVA *completely* neutralizes disintermediation. The model
    exposes the in-force value as ``mva_lapse_factor``, defaulting to the best-estimate
    **0.35 [std]** rather than the prescribed 0; set it to 0 for the statutory run. It is
    a judgement, not a calibration — sensitivity-test it.
    """
    return mva_lapse_factor if mva_in_force(t) else 1.0              # noqa: F821


def lapse_rate(t):
    """w_annual(t): ``clamp(Base(y) G + Rate(t) Phi_MVA(t), 0.005, 0.90)`` [R2 6.B.5].

    The **annual** total surrender rate, paired with :func:`lapse_rate_mth` exactly as
    :func:`mort_rate` is paired with :func:`mort_rate_mth`.

    On the base deterministic run ``MR = CR`` and ``renewal_spread = 0``, so
    ``Market(t) = Rate(t) = 0`` and this is ``Base(y) x 1.25``: contract years 1 to 5 at
    1.25% and the shock year at 90%, the 93.75% product capped.
    """
    rate = (lapse_rate_base(t) * gmir_factor()
            + lapse_dyn_rate(t) * mva_lapse_factor_at(t))
    return min(lapse_rate_max, max(lapse_rate_min, rate))            # noqa: F821


def lapse_rate_mth(t):
    """w(t): the monthly total surrender rate, ``1 - (1 - w_annual)^(1/12)``.

    This is the rate the monthly decrement actually applies; :func:`lapse_rate` is the
    annual rate it is derived from.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def annuitization_rate(t):
    """a(t): the monthly annuitization election rate.

    1.0% of in-force in each 30-day guarantee-period-end window after contract year 1 and
    zero elsewhere **[std]**. No public annuitization take-up study for deferred annuities
    was located; VM-22 prescribes 0% at all projection intervals for the standard
    projection [R2 6.B.6], which is a statutory simplification rather than an experience
    estimate. Set ``annuitization_rate_window = 0`` for the statutory alternative.
    """
    return annuitization_rate_window if in_gp_window(t) else 0.0     # noqa: F821


def pols_if(t):
    """l(t-1): the in-force probability at the **start** of policy month t.

    The library-wide convention, following ``Term_US_A`` and ``CashValue_SE``: this is
    the count that opens month t and the weight applied to that same month's cash flows,
    so the ``pols_if`` column of :func:`result_cf` reconciles with the row it sits on.
    ``pols_if(0) = pols_if(1) = pols_if_init()``, the issue instant carrying no decrement.

    The notes' end-of-month ``l(t) = l(t-1)(1 - a(t))(1 - q(t))(1 - w(t))`` is
    ``pols_if_at(t, "AFT_DECR")``; the two agree as ``pols_if(t + 1)`` in every month but
    ``proj_len()``, where :func:`pols_maturity` annuitizes the survivors out and the block
    opens the following month empty.
    """
    if t <= 0:
        return pols_if_init()
    if t > proj_len():
        return 0.0
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """In-force at month t read at the point given by ``timing``.

    ``"BEF_DECR"`` is ``l(t-1)``, equal to :func:`pols_if`; ``"BEF_MORT"`` is after
    annuitization elections; ``"BEF_LAPSE"`` is after deaths; ``"AFT_DECR"`` is after
    surrenders and is the notes' end-of-month ``l(t)``. The order is the notes'
    ``l(t) = l(t-1)(1 - a)(1 - q)(1 - w)`` **[std order]**.
    """
    if t < 1:
        return pols_if_init()
    pols = pols_if(t)
    if timing == "BEF_DECR":
        return pols
    pols = pols * (1.0 - annuitization_rate(t))
    if timing == "BEF_MORT":
        return pols
    pols = pols * (1.0 - mort_rate_mth(t))
    if timing == "BEF_LAPSE":
        return pols
    pols = pols * (1.0 - lapse_rate_mth(t))
    if timing == "AFT_DECR":
        return pols
    raise ValueError("invalid timing")


def pols_annuitization(t):
    """Annuitization elections in month t, taken at BOM before crediting."""
    return 0.0 if t < 1 else pols_if_at(t, "BEF_DECR") * annuitization_rate(t)


def pols_death(t):
    """Deaths in month t, on the in-force net of annuitization elections."""
    return 0.0 if t < 1 else pols_if_at(t, "BEF_MORT") * mort_rate_mth(t)


def pols_lapse(t):
    """Full surrenders in month t, on the survivors of annuitization and mortality."""
    return 0.0 if t < 1 else pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_maturity(t):
    """Deemed-maturity annuitizations, non-zero only at ``proj_len()``.

    Not a decrement — the projection horizon runs out — but needed for the in-force
    roll-forward to close; see the Space docstring.
    """
    return pols_if_at(t, "AFT_DECR") if t == proj_len() else 0.0


def pols_decr(t, kind):
    """The number of contracts leaving in month t by benefit ``kind``."""
    if kind == "DEATH":
        return pols_death(t)
    elif kind == "LAPSE":
        return pols_lapse(t)
    elif kind == "ANNUITIZATION":
        return pols_annuitization(t)
    elif kind == "MATURITY":
        return pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def annuitization_pp(t):
    """The amount transferred to the payout model on an annuitization election.

    The full account value ``AV'(t)`` in the 30-day window; outside it, ``AV'(t)`` less the
    surrender charge computed on ``AV'(t)``, with **no MVA** [S1][S2][S5][S16][std].

    The notes name ``SV(t)`` for the non-window case, and ``SV(t) = AV(t) + M(t) - C(t)``
    is composed on the *post*-crediting account value — but the same notes make
    annuitization an elective **BOM** transaction and set ``mu(t) = 0`` on it. The two
    cannot both hold on a monthly grid, and the model resolves it at BOM: annuitizers
    leave before the month's interest is credited, which is exactly what
    :func:`claim_from_av_pp` releases for them (``AV'(t)``, not ``AV(t)``). This cells is
    therefore the BOM analogue of ``SV(t)`` — the same composition on the account value
    the annuitant actually takes with them. Reading ``SV(t)`` literally would pay out one
    month of interest the block never credited to those contracts, and the difference
    ``(AV(t) - AV'(t)) * (1 - sc(y))`` would surface as a spurious
    :func:`claims_over_av`. The choice is inert on every shipped model point, where
    ``a(t)`` is zero outside the window; a test pins it open.

    No nonforfeiture floor is applied in either branch: ``SV(t)`` is the pre-floor value.
    Payout factors are out of scope: no retrieved product document contains an annuity
    rate table, so the accumulation model emits the transfer and hands the amount on.
    """
    account = av_pp_at(t, "BEF_INV")
    if in_gp_window(t):
        return account
    excess = (max(0.0, account - free_wd_remain(t)) if free_wd_mva_exempt()
              else account)
    return account - surr_charge_rate(t) * excess


def claim_pp(t, kind):
    """The benefit paid per contract in month t by ``kind``.

    ``"DEATH"`` is the full account value with no charge and no MVA [S1][S2][S13],
    floored at the cash surrender benefit and hence at MGSV(t) [R1 6]; on the base run the
    floor is inert because 4.45% exceeds 2.80%, but at a renewal rate down to the GMIR it
    overtakes the account value, so it is tested at every duration **[std]**.
    ``"LAPSE"`` is SB(t). ``"ANNUITIZATION"`` is :func:`annuitization_pp`.
    ``"MATURITY"`` is the account value floored at MGSV at the projection horizon.
    """
    if kind == "DEATH":
        return max(av_pp(t), surr_benefit_pp(t))
    elif kind == "LAPSE":
        return surr_benefit_pp(t)
    elif kind == "ANNUITIZATION":
        return annuitization_pp(t)
    elif kind == "MATURITY":
        return max(av_pp(t), mgsv_pp(t))
    else:
        raise ValueError("invalid kind")


def claim_from_av_pp(t, kind):
    """The account value released per contract by a claim of ``kind``.

    Equal to :func:`claim_pp` except where the Model #805 floor binds; the difference is
    :func:`claims_over_av`. Annuitizers leave at BOM and so release ``AV'(t)``, before the
    month's interest.
    """
    if kind == "ANNUITIZATION":
        return av_pp_at(t, "BEF_INV")
    elif kind in ("DEATH", "LAPSE", "MATURITY"):
        return av_pp(t)
    else:
        raise ValueError("invalid kind")


def premiums(t):
    """Premium income: the single purchase payment at t = 0."""
    return premium_pp() * pols_if_init() if t == 0 else 0.0


def prem_to_av(t):
    """Premium credited to the account value, in-force weighted."""
    return prem_to_av_pp(t) * pols_if_init() if t == 0 else 0.0


def withdrawals(t):
    """Withdrawal payments in month t: ``(W(t) + M(t) - C(t))`` weighted by ``l(t-1)``.

    The ledger separates the free part (``wd_free_pp``, never charged or adjusted) from
    the excess (``wd_excess_pp``); this line is the total cash paid. The weight is
    :func:`pols_if`, the start-of-month count printed on this same row of
    :func:`result_cf`, because the withdrawal is taken at BOM before any decrement.
    """
    return 0.0 if t < 1 else wd_payment_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in month t, for one ``kind`` or, with ``kind=None``, all four."""
    if kind is None:
        return (claims(t, "DEATH") + claims(t, "LAPSE")
                + claims(t, "ANNUITIZATION") + claims(t, "MATURITY"))
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The account value released by a claim of ``kind``, in-force weighted."""
    return claim_from_av_pp(t, kind) * pols_decr(t, kind)


def claims_over_av(t, kind=None):
    """Benefit paid less the account value released, ``claims - claims_from_av``.

    Signed, and normally **negative** on this chassis: a surrender pays out less than the
    account value it releases, by the surrender charge and any negative MVA. It turns
    positive exactly when the Model #805 floor binds and SB(t) exceeds AV(t). Either way
    it is a reconciliation quantity, not a cash flow of its own — a binding floor raises
    SB(t), it does not add a separate top-up line, and the charge and the MVA are
    internal accounting entries rather than ledger lines.
    """
    if kind is None:
        return (claims_over_av(t, "DEATH") + claims_over_av(t, "LAPSE")
                + claims_over_av(t, "ANNUITIZATION") + claims_over_av(t, "MATURITY"))
    return claims(t, kind) - claims_from_av(t, kind)


def commissions(t):
    """Acquisition commission: 2.00% of premium paid at issue **[std]**.

    No retrieved document discloses MYGA commission; this is a pure modeling assumption.
    """
    return comm_rate_acq * premiums(t)                               # noqa: F821


def premium_taxes(t):
    """Premium tax on the purchase payment, 0% **[std]** [S3][S16]."""
    return premium_tax_rate() * premiums(t)


def inflation_factor(t):
    """The expense inflation factor in the contract year containing month t."""
    return (1.0 + inflation_rate) ** duration(t)                     # noqa: F821


def expenses(t):
    """Insurer expenses: acquisition at issue and inflating maintenance monthly **[std]**.

    ``(50 / 12) x 1.025^(y-1)`` per contract per month, in-force weighted. VM-22
    prescribes $35 x 1.025^(offset) per contract for business the company does not
    administer [R2 6.B.3]; the $50 figure is a **[std]** uplift of that anchor to a
    self-administered block. ``expense_acq`` is 0 because this chassis's only acquisition
    cost is the commission.
    """
    if t == 0:
        return expense_acq * pols_if_init()                          # noqa: F821
    if t < 0 or t > proj_len():
        return 0.0
    return (expense_maint / 12.0) * inflation_factor(t) * pols_if(t)  # noqa: F821


def net_cf(t):
    """Net cash flow in policy month t.

    Interest credited, the surrender charge, the MVA and the movement of the Model #805
    floor are **internal accounting entries**, not ledger lines: they drive AV, MGSV and
    the benefit *amount* but are never cash flows of their own. Only amounts paid to or
    received from the contract holder, and the insurer's own expenses, appear here.
    """
    return (premiums(t) - withdrawals(t) - claims(t)
            - commissions(t) - expenses(t) - premium_taxes(t))


def av_at(t, timing):
    """The in-force weighted account value at month t; see :func:`av_pp_at` for ``timing``.

    Each timing carries the in-force appropriate to that point in the month: ``l(t-1)``
    before the withdrawal, ``l(t-1)(1 - a(t))`` once annuitizers have left, and at the end
    of the month the count that survives *every* exit — ``pols_if(t + 1)``, which is
    ``l(t)`` except at ``proj_len()``, where the deemed maturity empties the block. Using
    ``pols_if_at(t, "AFT_DECR")`` there would leave the matured account value standing in
    the block *and* released as a claim, and :func:`check_av_roll_fwd` would not close.
    """
    if t < 1:
        return av_pp_init() * pols_if_init() if t == 0 else 0.0
    if timing == "BEF_WD":
        return av_pp_at(t, "BEF_WD") * pols_if(t)
    elif timing == "BEF_INV":
        return av_pp_at(t, "BEF_INV") * pols_if_at(t, "BEF_MORT")
    elif timing == "EOM":
        return av_pp(t) * pols_if(t + 1)
    else:
        raise ValueError("invalid timing")


def inv_income(t):
    """Interest credited to the whole block in month t."""
    return 0.0 if t < 1 else av_at(t, "BEF_INV") * credit_rate_mth(t)


def wd_from_av(t):
    """The account value released by month t's withdrawals, gross of charge and MVA."""
    return 0.0 if t < 1 else wd_pp(t) * pols_if(t)


def av_change(t):
    """The change in the block's account value over month t."""
    return av_at(t, "EOM") - av_at(t - 1, "EOM")


def check_av_roll_fwd_resid(t):
    """Account value roll-forward residual in month t; zero to floating point.

    ``AV(t) - AV(t-1) = premium in - withdrawals out + interest credited - the account
    value released by each of the four claim kinds``. Note that the *cash* paid on a
    surrender may exceed the account value released when the Model #805 floor binds; that
    excess is :func:`claims_over_av` and is not part of this identity. t = 0 is the
    premium deposit itself and is excluded.

    The signed residual, for a debugging session that needs to know *where* and *by how
    much* :func:`check_av_roll_fwd` failed.
    """
    if t < 1:
        return 0.0
    expected = (prem_to_av(t) - wd_from_av(t) + inv_income(t)
                - claims_from_av(t, "ANNUITIZATION") - claims_from_av(t, "DEATH")
                - claims_from_av(t, "LAPSE") - claims_from_av(t, "MATURITY"))
    return av_change(t) - expected


def check_av_roll_fwd():
    """True when the account value roll-forward closes in every projected month.

    Takes no argument and returns a bool, following ``CashValue_SE.check_av_roll_fwd`` and
    the library convention, so one test can call the same check across every model.
    :func:`check_av_roll_fwd_resid` carries the per-month signed residual, and this is
    ``abs(resid) <= check_tol_av`` over ``t = 1 .. proj_len()``.
    """
    return all(abs(check_av_roll_fwd_resid(t)) <= check_tol_av      # noqa: F821
               for t in range(1, proj_len() + 1))


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual in month t; zero to floating point.

    ``pols_if(t) - pols_if(t+1) = annuitizations + deaths + surrenders + deemed
    maturities``: the start-of-month count opens the row, the four exits are taken during
    it and the next month opens on what is left. In the notes' own indexing that is
    ``l(t-1) - l(t)``, since :func:`pols_if` is the start-of-month count.

    The signed residual; :func:`check_pols_roll_fwd` is the bool over all ``t``.
    """
    if t < 1:
        return 0.0
    return (pols_if(t) - pols_if(t + 1) - pols_annuitization(t)
            - pols_death(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    No argument, returns a bool over ``t = 1 .. proj_len()``, matching
    :func:`check_av_roll_fwd` and the library convention.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= check_tol_pols  # noqa: F821
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cashflows, indexed by policy month t from 0 to ``proj_len()``.

    ``t = 0`` carries the purchase payment, the acquisition commission and the premium
    tax, exactly as the notes' cash flow ledger indexes them.

    The ``pols_if`` column is the **start**-of-month count, which is the weight applied to
    every cash flow on that same row, so the printed in-force reconciles with the printed
    flows: ``withdrawals(t) / wd_payment_pp(t)`` and
    ``expenses(t) / ((expense_maint / 12) * inflation_factor(t))`` both return it.
    """
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_annuitization": [claims(t, "ANNUITIZATION") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "commissions": [commissions(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements, indexed by policy month t.

    ``pols_if`` opens the row (the start-of-month count, the same column
    :func:`result_cf` prints), the four exit columns are taken during the month, and
    ``pols_if_aft_decr`` is the notes' end-of-month ``l(t)``. The closing balance is next
    month's ``pols_if``, which equals ``pols_if_aft_decr`` in every month but
    ``proj_len()``, where the deemed maturity empties the block.
    """
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_annuitization": [pols_annuitization(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, "AFT_DECR") for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of per-contract account value and surrender values, indexed by t.

    The first five columns are the worked example's table; the rest are its surrender
    trace, available at every duration.
    """
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp_bef_wd": [av_pp_at(t, "BEF_WD") for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "av_pp_bef_inv": [av_pp_at(t, "BEF_INV") for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "mgsv_pp": [mgsv_pp(t) for t in ts],
            "free_wd_avail": [free_wd_remain(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "mva_pp": [mva_pp(t) for t in ts],
            "surr_value_pp": [surr_value_pp(t) for t in ts],
            "surr_benefit_pp": [surr_benefit_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

maturity_age = 100

net_consideration_ratio = 0.875

load_prem_rate = 0.0

renewal_spread = 0.0

comm_rate_acq = 0.02

expense_acq = 0.0

expense_maint = 50.0

inflation_rate = 0.025

free_wd_util = 0.0

annuitization_rate_window = 0.01

lapse_base_igp = 0.01

lapse_base_shock = 0.75

lapse_base_post1 = 0.1

lapse_base_post2 = 0.075

lapse_base_ult = 0.03

lapse_rate_min = 0.005

lapse_rate_max = 0.9

lapse_slope = 1.25

lapse_buffer = 0.005

lapse_itm_gate = 5.0

lapse_exp_sc = 2.0

lapse_exp_post = 2.5

gmir_band_low = 0.01

gmir_band_high = 0.025

gmir_factor_low = 1.25

gmir_factor_mid = 1.0

gmir_factor_high = 0.7

mva_lapse_factor = 0.35

mva_admin_spread = 0.0025

mva_factor_rate_split = 0.06

mgsv_stat_step = 0.0005

mgsv_stat_spread = 0.0125

mgsv_stat_cap = 0.03

mgsv_stat_floor = 0.0015

check_tol_av = 1e-06

check_tol_pols = 1e-12

math = ("Module", "math")

pd = ("Module", "pandas")