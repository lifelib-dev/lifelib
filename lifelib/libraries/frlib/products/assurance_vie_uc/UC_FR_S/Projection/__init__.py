# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.UC_FR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_av()          # the worked-example table, column for column
    >>> Projection[2].result_cf()          # the base run, 360 months
    >>> Projection.point_id = 3            # the indexee floor on the same path

``t`` counts **policy months** and is **0-based**: ``t = 0`` is the issue month, period
``t`` runs from time ``t`` to time ``t + 1``, and the frame is ``t = 0 … proj_len() - 1``.
Every balance is read at the **end** of month ``t`` after that month's levy — so
``av_euro_pp(t)`` is the opening euro balance of month ``t + 1``, exactly as the notes'
worked-example table prints it.

The balances **at issue** — time 0, before month 0 opens, the notes' `init` row — are not a
frame row. They are the ``*_init`` cells (:func:`unit_price_init`, :func:`units_init`,
:func:`av_euro_init_pp`, :func:`cum_prem_net_init`, :func:`uc_cost_basis_init`,
:func:`prem_to_av_pp`), and each month reaches its own opening balance through an opening
cells — :func:`unit_price_open`, :func:`units_open`, :func:`av_euro_open_pp` and
``av_pp_at(t, "OPENING")`` — which is the issue value when ``t = 0`` and the previous
month's close thereafter. Nothing is ever indexed at ``t = -1``.

The in-force count is read the other way round — :func:`pols_if` ``(t)`` is the count at
the **start** of month ``t``, so the frame opens at ``pols_if(0) = pols_if_init()``; see
below.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/assurance_vie_uc/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``UC_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.UC_FR_S.Data`,
reached here through the ``data`` Reference:

=========================  ==================================  ==========================
Reference                  Cells                               File
=========================  ==================================  ==========================
model_point_file           data.model_point_table()            model_point_table.csv
mort_table_file            data.mort_table()                   mort_table.csv
lapse_table_file           data.lapse_table()                  lapse_table.csv
plancher_rate_table_file   data.plancher_rate_table()          plancher_rate_table.csv
uc_scenario_table_file     data.uc_scenario_table()            uc_scenario_table.csv
=========================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``savings.CashValue_SE`` and the account-value vocabulary
this library settled on — ``av_pp_at(t, timing)`` for the account value read at a point
inside the month, ``check_av_roll_fwd`` for its identity, ``_pp`` for a per-policy amount
and no suffix for the same amount weighted by the in-force count. The technical notes use
compact symbols instead. The mapping is:

=========================  ==================================  ==========================
Notes symbol               Cells                               Meaning
=========================  ==================================  ==========================
t                          (the cells argument)                Policy month, 0-based
y = t//12 + 1              policy_year(t)                      Policy year containing t
a                          age(t)                              Attained age (ALB)
(none)                     duration(t)                         Completed policy years
(none)                     duration_mth(t)                     Months elapsed at start of t
(the model point row)      model_point()                       The selected model point
(number of periods)        proj_len()                          Months projected
P, e                       premium(), prem_charge_rate()       Single premium and charge
P(1-e)                     prem_to_av_pp()                     Net premium allocated
alpha                      uc_alloc()                          Share allocated to UC
1 - alpha                  euro_alloc()                        Share allocated to euro
p_init                     unit_price_init()                   Liquidation value at issue
p(t)                       unit_price(t)                       Liquidation value, end of t
p(t-1)                     unit_price_open(t)                  The same, start of t
(scenario)                 uc_return_mth(t)                    Monthly UC return
n_init                     units_init()                        Unit count at issue
n(t)                       units(t)                            Unit count held, end of t
n(t-1)                     units_open(t)                       The same, start of t
n(t-1) c_m                 fee_units(t)                        Units cancelled by the fee
c, c_m                     mgmt_fee_rate_uc(),
                           mgmt_fee_rate_uc_mth()              UC management charge
mgmt_fee_uc(t)             mgmt_fee_uc_pp(t)                   Charge collected, per policy
U(t)                       av_uc_pp(t)                         UC account value
V_init                     av_euro_init_pp()                   Euro balance at issue
V(t)                       av_euro_pp(t)                       Euro account value, end of t
V(t-1)                     av_euro_open_pp(t)                  The same, start of t
i_e                        euro_credit_rate()                  Euro credited rate, net
(1+i_e)^(1/12)             euro_credit_factor_mth()            Its monthly factor
av_pp_at(t, timing)        av_pp_at(t, timing)                 Total account value
(x in force)               av_at(t, timing)                    The same, weighted
A(t), phi                  arb_amount_pp(t),
                           arbitrage_fee_rate()                Arbitrage and its fee
W(t)                       wd_amount_pp(t)                     Partial surrender
W_uc(t), W_eur(t)          wd_uc_pp(t), wd_eur_pp(t)           Its pro-rata split
S_init                     cum_prem_net_init()                 Floor base at issue
S(t)                       cum_prem_net(t)                     Floor base
R(t)                       plancher_ratchet(t)                 Ratchet level (cliquet)
F(t)                       plancher_amount(t)                  The floor
K(t)                       nar(t)                              Capital sous risque
pi(a)                      plancher_rate(t)                    Tariff / 10,000
pi(a)/12                   plancher_rate_mth(t)                Its monthly step
K pi/12                    plancher_charge_pp(t)               Rider premium, per policy
B_init                     uc_cost_basis_init()                Levy base at issue
B(t)                       uc_cost_basis(t)                    Prelevements sociaux base
tau                        social_levy_rate                    17.2%
q_a, q_m(t)                mort_rate(t), mort_rate_mth(t)      Mortality rates
w_base(y)                  lapse_rate_base(t)                  Table surrender rate
M_perf(t)                  perf_factor(t)                      Performance multiplier
M_pl(t)                    plancher_factor(t)                  Moneyness multiplier
w_ann(y,t), w_m(t)         lapse_rate(t), lapse_rate_mth(t)    Surrender rates applied
l(t)                       pols_if(t)                          In force at the start of t
l(t+1)                     pols_if_at(t, "AFT_DECR")           End of t, after decrements
(none)                     pols_death(t), pols_lapse(t)        Decrements in month t
E(t)                       expenses(t)                         Acquisition + maintenance
(benefit outgo)            claims(t, kind)                     Gross benefit outgo by kind
(unit and euro releases)   av_releases(t)                      Account value released
K x l q_m                  plancher_strain(t)                  Non-unit cost of deaths
net_cf(t)                  net_cf(t)                           Non-unit cash flow
=========================  ==================================  ==========================

Five names needed care.

``mgmt_fee_uc(t)`` in the notes is a **per-policy** amount, and the library reserves the
unsuffixed name for the in-force-weighted flow. The notes' quantity is
:func:`mgmt_fee_uc_pp`; :func:`mgmt_fee_uc` is ``pols_if(t)`` times it, and the same rule
splits :func:`plancher_charge_pp` from :func:`plancher_charge` and
:func:`arb_fee_pp` from :func:`arbitrage_fee`. The notes' worked-example table prints the
``_pp`` quantities; the notes' insurer-side extraction prints the weighted ones, which is
why its year-1 management charge is 621.33 € against the table's 630.20 €.

``pols_if(t)`` is the in-force probability at the **start** of month ``t``, so
``pols_if(0) = pols_if_init()`` and ``result_cf()`` opens on it. It is therefore
**exactly the weight carried by the flows on its own row**, which is the one thing a
reader of the frame needs it to be: dividing any cash flow on row ``t`` by that row's
``pols_if`` recovers the per-policy amount.

This model was first written the other way round, publishing the **end**-of-month count
under the name ``pols_if`` while weighting each row's flows at ``pols_if(t - 1)``.
Nothing raised and nothing went NaN — the published exposure column was simply the correct
series shifted one month, and a per-policy amount recovered from it was one month stale.
The rename fixes it and collides with nothing, because the end-of-month quantity is
still here: it is **``pols_if_at(t, "AFT_DECR")``**, the ``CashValue_SE`` timing form the
shared vocabulary prescribes, equal to ``pols_if(t) (1 - q_m)(1 - w_m)`` and to
``pols_if(t + 1)`` everywhere the projection runs on. ``"BEF_DECR"`` and ``"BEF_LAPSE"``
expose the two points inside the month. Every cash-flow number in ``result_cf()`` is
unchanged by the rename; only the ``pols_if`` column moved.

The account value is a stock read at the end of the month, so :func:`av_at`,
:func:`av_uc_at` and :func:`av_euro_at` weight it by ``pols_if_at(t, "AFT_DECR")`` — the
notes' ``l(t + 1)``, the policies the balance is still carried for once the month's
decrements have gone — which is what makes ``av_at(11, "BEF_DECR") = 77,330.08 x 0.968240``
on the anchor cell's last month.

``net_cf`` on this product is the **non-unit** cash flow of the UC leg and the rider, not
a gross liability total and not the contract's margin. Every benefit is funded by
cancelling units and by drawing the euro balance, so a gross presentation adds the same
money to both sides; and the euro leg's own margin is ``Euro_FR_S``'s output, which must
be added from outside. The gross flows are still published — ``claims_death``,
``claims_lapse``, ``withdrawals`` and ``av_releases`` are ``result_cf`` columns — and
:func:`check_benefit_funding` asserts that they net exactly against the account value plus
the death strain.

``withdrawals`` is a partial surrender, an owner election rather than a claim, so it
carries its own name and its own column and is never one of the ``claims`` kinds.

``social_levy_uc`` is the `prélèvements sociaux` **withheld and remitted** on the UC leg.
It is a pass-through, not insurer income and not an expense, and it is published as its
own column precisely so that its exclusion from :func:`net_cf` is visible rather than
merely asserted.

.. rubric:: The month, in the order it happens

Per policy, within month ``t``::

    p(t)  = p(t-1) (1 + r_uc(t))                      the liquidation value moves
    V     = V(t-1) (1 + i_e)^(1/12)                   the euro leg accrues
    n     = n(t-1) - n(t-1) c_m                       the charge cancels units
    V    -= A(t) ;  n += A(t)(1 - phi)/p(t)           the arbitrage settles
    W(t) split pro rata ;  n -= W_uc/p(t) ;  V -= W_eur
    F(t), K(t) observed on U + V                      the floor and the risk
    plancher premium levied, euro first
    decrements at end of month, deaths before surrenders

``p(t-1)``, ``n(t-1)`` and ``V(t-1)`` above are the *opening* balances of month ``t``,
which in the first month, ``t = 0``, are the balances at issue: they are read through
:func:`unit_price_open`, :func:`units_open` and :func:`av_euro_open_pp` rather than by
indexing a month that does not exist.

Two points in that order are load-bearing and both are listed pitfalls. **The management
charge is taken on the opening unit count**, ``n(t-1)``, not the closing one: in a month
with an arbitrage the two differ by the arbitrage's units, 52.28 € against 59.54 € at
``t = 2`` on the anchor cell. And **the monthly charge rate is ``c/12``**, not
``1 - (1 - c)^(1/12)``: the insurers compound the *periodic* rate, so 0.25% a quarter
gives an annual factor of ``(1 - 0.0025)^4 = 0.99003744`` rather than ``1 - 1.00%``.
:func:`av_pp_at` exposes ``"BEF_FEE"``, ``"BEF_WD"``, ``"BEF_LEVY"`` and ``"BEF_DECR"``
so the ordering is inspectable rather than buried in one expression, and
:func:`check_av_roll_fwd` asserts the identity every month against independently computed
growth.

.. rubric:: The garantie plancher

The floor ``F(t)`` follows the elected :func:`plancher_basis`: ``simple`` is the running
base of premiums net of the premium charge less partial surrenders; ``indexee`` indexes
that base at 3.50% a year and deducts the **nominal** withdrawal; ``cliquet`` locks in
account-value highs at each ratchet date and adjusts for a partial surrender
**proportionally**, because a ratchet is a value level rather than a premium tally. On the
same path the three give 94,000.00, 97,378.25 and 94,216.29 at ``t = 11``.

The `capital sous risque` is ``min(cap, max(0, F - AV))``, and everything about the rider
follows from that one expression:

- it is **floored at zero**, so the rider costs nothing out of the money and the death
  strain never becomes a rebate booked as insurance profit;
- it is the **charge base**, not the account value — the charge on the account value would
  be 4.6 times larger at ``t = 11`` on the anchor cell;
- it is **capped on the risk**, not on the benefit, so the excess reduces the floor
  rather than truncating what the beneficiary is paid; and
- it is the insurer's **cost per death**, exactly, because the rest of the death benefit
  is the policyholder's own account value.

An **arbitrage never moves the floor.** It is neither a premium nor a surrender: it moves
value between the legs and pays a fee, and :func:`check_floor_base` asserts that the floor
base is the net premium less cumulative withdrawals and nothing else.

The levy source matters to the unit count. Under ``euro_first`` the premium is taken from
the euro support and the unit count is untouched — 745.036125 units at ``t = 11`` on the
anchor cell against 744.044774 under ``uc_units`` — which is what makes the count a
deterministic function of the event schedule alone. Where the euro balance cannot cover
the premium the remainder cancels units, which is the branch a 100%-UC allocation runs
down.

.. rubric:: Prélèvements sociaux, and the asymmetry that is statutory

Art. L. 136-7 II, 3°, a) levies the contribution on the euro component **annually**, as
interest is credited; II, 3°, c) levies it on the unit-linked component only at
`dénouement`. So the UC leg is taxed on a **gain**, at surrender, partial surrender or
death, and on a loss it is zero — at ``t = 11`` on the anchor cell the UC leg is
17,284.34 € under water and the levy is nil. Accruing it annually on the UC leg is a
listed pitfall: it would understate the account value throughout and shrink the base the
management charge is levied on. The euro leg's annual component belongs to ``Euro_FR_S``,
where - on the same monthly grid as this model - it lands whole in the anniversary month
beside the interest it is struck on.
Whether the plancher top-up above the account value sits inside the levy base is stated in
no retrieved document; the model puts it outside.

.. rubric:: Behaviour

Two dynamic overlays sit on the base surrender table, both **[std]** and both elected per
model point through :func:`lapse_dynamic`, which is ``none`` on the worked-example anchor:

- :func:`perf_factor`, ``min(2, 1 + 2 max(0, g_ref - R_12m))``, raising surrender after
  poor performance. It reads a **completed** trailing year, so it is 1 through the first
  twelve months whatever the path does, which is why the anchor cell's decrements are the
  flat 2% a year the notes' worked example states.
- :func:`plancher_factor`, halving surrender while the floor is in the money. A
  policyholder holding an in-the-money guarantee has a reason not to surrender that a UK
  bondholder does not, because surrendering forfeits it. It is the one behavioural
  assumption specific to this product, it is a pure invention with no evidence behind it,
  and it should be the first thing a user replaces — which is why it is elected rather
  than wired in.

There is no paid-up state: the contract is single premium, so there is no premium
obligation to stop. The 30-day `renonciation` is carried inside the year-1 surrender rate
rather than as a separate decrement.
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
    """The policy identifier of the selected model point, for reporting."""
    return str(model_point()["policy_id"])


def issue_age():
    """The issue age of the selected model point, **age last birthday**.

    ALB is a **[std]** choice.  The published plancher tariffs are quoted by the insured's
    attained age at the calculation date [S4 Annexe I] and are read at :func:`age`, so the
    tariff steps at each policy anniversary rather than on the insured's birthday.
    """
    return int(model_point()["issue_age"])


def sex():
    """The sex (M / F) of the selected model point.

    It enters the **mortality assumption** only.  The plancher tariff is published by
    attained age alone and is not sex-distinct, so the sex of the life changes the
    insurer's expected strain and never the price it charges - which is one half of the
    reason the sign of the rider's margin at any age is genuinely unknown.
    """
    return str(model_point()["sex"])


def premium():
    """P: the single premium, before the `frais sur versement`.

    `Versements libres` and `versements programmes` exist on every retrieved contract and
    are excluded from the base projection **[std]**: a later premium adds to
    :func:`cum_prem_net` and to :func:`uc_cost_basis` on the same date and changes no
    recursion.
    """
    return float(model_point()["premium"])


def prem_charge_rate():
    """e: the `frais sur versement`, 1.00% **[std]**.

    Observed levels run from nil to a 4.50% maximum across the retrieved contracts.  A
    non-zero mid-range level is chosen deliberately, because a zero premium charge makes
    the net-premium and gross-premium floor bases indistinguishable and hides the question
    the plancher definition turns on.
    """
    return float(model_point()["prem_charge_rate"])


def uc_alloc():
    """alpha: the share of the net premium allocated to the UC leg, 0.70 **[std]**."""
    return float(model_point()["uc_alloc"])


def euro_alloc():
    """1 - alpha: the share of the net premium allocated to the `fonds en euros`.

    Derived rather than a column, so the two shares cannot drift apart in the input file.
    """
    return 1.0 - uc_alloc()


def unit_price_init():
    """p_init: the liquidation value of the composite UC support at issue, 100.00 **[std]**.

    A scaling convention, not a fact: the unit count and the liquidation value are
    reciprocal, and only their product enters the liability.
    """
    return float(model_point()["unit_price_init"])


def mgmt_fee_rate_uc():
    """c: the annual UC `frais de gestion sur encours`, 0.88% p.a. **[std]**.

    Anchored on the market average - France Assureurs reports an encours-weighted 0.88%
    on UC supports, 0.82% under `gestion libre` and 1.17% under `gestion sous mandat` -
    and not on the retrieved sample, which is weighted towards broker and mutual contracts
    and is cheaper than the market.  Contract rates retrieved span 0.475% to 1.50%, a
    factor of three on the dominant income line, and **no statutory ceiling on any French
    life charge appears in the retrieved texts**.
    """
    return float(model_point()["mgmt_fee_rate_uc"])


def euro_credit_rate():
    """i_e: the annual rate credited to the euro leg, **net** of its own charge, 2.50%.

    A **[std]** pointer, not a model.  `Taux minimum garanti`, `participation aux
    benefices`, the `provision pour participation aux benefices` and the `effet cliquet`
    are specified and implemented in ``Euro_FR_S``, and the euro leg therefore produces no
    margin line here at all.
    """
    return float(model_point()["euro_credit_rate"])


def arbitrage_fee_rate():
    """phi: the `frais d'arbitrage`, 0.50% of the amount switched.

    The PRO BTP level; observed rates run from nil to 2%, several contracts allowing a
    number of free arbitrages a year.  Flat-fee minima - 30 EUR by post, 15 EUR online -
    are administrative and do not scale, so they are not modeled.
    """
    return float(model_point()["arbitrage_fee_rate"])


def plancher_flag():
    """Whether the `garantie plancher` rider is elected; True on the anchor cell.

    It is elected **at subscription only** and cannot be restarted, so it is a model point
    attribute rather than a switch that can turn on mid-projection.  The charge is a
    deduction from an existing account and not a new premium, which matters for contract
    boundaries.
    """
    return bool(model_point()["plancher_flag"])


def plancher_basis():
    """``simple``, ``indexee`` or ``cliquet``: what the floor is measured against.

    ``simple`` and ``indexee`` are both sourced - a running base of premiums, flat or
    indexed at 3.50% a year.  ``cliquet`` is a **[std]** construction: **no retrieved
    document offers a ratchet**, and its existence in the French market is unverified.  It
    is carried so the model holds the three-way column and so the proportional-versus-
    nominal surrender adjustment can be asserted.
    """
    v = str(model_point()["plancher_basis"])
    if v not in ("simple", "indexee", "cliquet"):
        raise ValueError("invalid plancher_basis")
    return v


def plancher_index_rate():
    """The annual indexation of an ``indexee`` floor, 3.50%.

    Generali's option 2 sets it contractually at 3.50%; PRO BTP sets it annually at the
    insurer's discretion, which makes it a class-(b) element the model holds as a
    snapshot.
    """
    return float(model_point()["plancher_index_rate"])


def plancher_ratchet_months():
    """The ratchet period of a ``cliquet`` floor in months, 12 **[std]**.

    A one-month ratchet is the same recursion observed twelve times as often, and on the
    anchor path it locks in the pre-fall high: 98,476.25 against 94,216.29 at ``t = 11``.
    """
    return int(model_point()["plancher_ratchet_months"])


def plancher_gross_basis():
    """Whether the floor base is **gross** rather than net premiums; False on the anchor.

    Both bases are sourced and they differ by exactly the premium charge.  Net is chosen
    for the anchor because it makes the floor equal the account value at issue, so
    the net amount at risk **at issue** is zero - an assertable fact rather than an accident
    of the premium charge; on
    the gross basis the rider starts 1,000 EUR in the money on a 100,000 EUR premium.
    """
    return bool(model_point()["plancher_gross_basis"])


def plancher_end_age():
    """The attained age at which the cover ceases, 75.

    The majority value; 70 and 80 are both observed.  The choice matters more than it
    looks: on the shipped Spirica tariff the rate at 74 is 408/17 = 24 times the rate at
    30, so the last five years carry a large share of the lifetime charge - and moving the
    cessation age to 80 runs past the last published age, which is why
    :func:`plancher_rate` raises rather than extrapolates.
    """
    return int(model_point()["plancher_end_age"])


def plancher_cap():
    """The cap on the `capital sous risque`, 300,000 EUR.

    The cap is on the **risk**, and any excess reduces the floor; capping the death benefit
    instead is a different and much cruder contract.  It never binds on the anchor cell and
    binds precisely in the deep drawdowns where the guarantee is worth something.
    """
    return float(model_point()["plancher_cap"])


def plancher_levy_source():
    """``euro_first`` or ``uc_units``: where the plancher premium is taken from.

    ``euro_first`` is the sourced design - the euro support first, then the largest UC
    support by cancelling units - and it is what keeps the unit count independent of the
    rider.  Where the euro balance cannot cover the premium the remainder cancels units
    whatever the election, which is the branch a 100%-UC allocation runs down.
    """
    v = str(model_point()["plancher_levy_source"])
    if v not in ("euro_first", "uc_units"):
        raise ValueError("invalid plancher_levy_source")
    return v


def wd_pattern():
    """``none``, ``one_off`` or ``programmed``: the partial-surrender pattern.

    ``one_off`` takes ``wd_amount`` in month ``wd_month``; ``programmed`` takes
    ``wd_rate`` of the account value a year, monthly.  Both are **[std]**: no retrieved
    document gives a partial-surrender pattern.  ``programmed`` is the pattern the
    eight-year tax design encourages, and it keeps the floor base falling in step with the
    account.
    """
    v = str(model_point()["wd_pattern"])
    if v not in ("none", "one_off", "programmed"):
        raise ValueError("invalid wd_pattern")
    return v


def arb_pattern():
    """``none``, ``one_off`` or ``progressive``: the arbitrage pattern.

    ``progressive`` is the `investissement progressif` design - a fixed monthly amount out
    of the euro fund into UC.  Trigger-based options (`securisation des plus-values`,
    `limitation des moins-values`) are specified in ``product-spec.md`` and are **not**
    implemented: they matter because they systematically move value out of UC after a
    rise, shrinking the management-charge base and the plancher exposure at the same time.
    """
    v = str(model_point()["arb_pattern"])
    if v not in ("none", "one_off", "progressive"):
        raise ValueError("invalid arb_pattern")
    return v


def lapse_dynamic():
    """``none`` or ``full``: whether the two behavioural multipliers are applied.

    ``none`` runs the base table alone and is what the notes' worked example states - a
    flat 2.00% a year through the anchor cell's twelve months.  ``full`` applies
    :func:`perf_factor` and :func:`plancher_factor`.  The election exists because both
    multipliers are **[std]** inventions with no evidence behind them, and a user
    replacing them should be able to see the base run underneath.
    """
    v = str(model_point()["lapse_dynamic"])
    if v not in ("none", "full"):
        raise ValueError("invalid lapse_dynamic")
    return v


def uc_return_scenario():
    """The id of the UC return path in *uc_scenario_table.csv* this model point runs on."""
    return str(model_point()["uc_return_scenario"])


def pols_if_init():
    """l(0): the in-force probability at issue; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_len():
    """The **number of projected months**, from the model point.

    The exclusive end of the 0-based frame: ``result_cf()`` runs ``t = 0 … proj_len() - 1``
    and has ``proj_len()`` rows.  12 on the worked-example anchor and 360 on the base run.
    The contract is written `viagere` and has no maturity date, so the horizon is a
    modelling choice rather than a contractual one and it is a per-policy column.
    """
    return int(model_point()["proj_len"])


def duration(t):
    """Completed policy years at the start of month t: ``t // 12``.

    0-based, as everywhere in lifelib: 0 through the first policy year.
    """
    return t // 12


def duration_mth(t):
    """Months elapsed from issue at the start of month t; equal to t.

    ``t`` is 0-based and counts from issue, so the identity is trivial - the cells exists
    so the monthly models in this library share one vocabulary.
    """
    return t


def policy_year(t):
    """y: the 1-based contractual policy year containing month t; 1 for t = 0..11.

    ``duration(t) + 1``.  A contractual label, derived and never indexed by - it is what
    the `policy_year` column of *lapse_table.csv* is keyed on.
    """
    return duration(t) + 1


def age(t):
    """a: the attained age (ALB) in the policy year containing month t.

    ``issue_age + duration(t)``, so the tariff steps at each policy anniversary.
    """
    return issue_age() + duration(t)


def prem_to_av_pp():
    """P(1 - e): the premium credited to the account value, net of `frais sur versement`.

    The whole of it is allocated between the two legs, and on the net-premium floor basis
    it is also the floor at issue - which is why the net amount at risk at issue,
    ``cum_prem_net_init() - prem_to_av_pp()``, is zero exactly.
    """
    return premium() * (1.0 - prem_charge_rate())


def units_init():
    """n_init = P(1-e) alpha / p_init: the unit count bought at issue.

    Unit conversion is contractually to four decimal places, `au dix millieme`.  The model
    carries full precision and reports to four, because rounding the count at every
    cancellation is an administration-system behaviour rather than a liability one.
    """
    return prem_to_av_pp() * uc_alloc() / unit_price_init()


def av_euro_init_pp():
    """V_init = P(1-e)(1 - alpha): the euro balance at issue."""
    return prem_to_av_pp() * euro_alloc()


def cum_prem_net_init():
    """S_init: the floor base at issue.

    ``P(1 - e)`` on the sourced net-premium basis, ``P`` where
    :func:`plancher_gross_basis` elects the gross variant.
    """
    return premium() if plancher_gross_basis() else prem_to_av_pp()


def uc_cost_basis_init():
    """B_init = P(1-e) alpha: the `prelevements sociaux` cost basis of the UC leg at issue."""
    return prem_to_av_pp() * uc_alloc()


def mgmt_fee_rate_uc_mth():
    """c_m = c/12: the monthly UC management charge **[std 1/12 convention]**.

    ``c/12`` and **not** ``1 - (1 - c)^(1/12)``.  The insurers compound the *periodic*
    rate: 0.25% a quarter gives an annual factor of ``(1 - 0.0025)^4 = 0.99003744``, not
    ``1 - 1.00%``, and Suravenir's own published table prints ``100 x (1 - 0.60%) =
    99.4000`` after a year where a monthly 1/12 levy gives 99.4016.  The two conventions
    differ in the fourth decimal of the unit count, which is exactly the precision the
    contract guarantees.
    """
    return mgmt_fee_rate_uc() / 12.0


def euro_credit_factor_mth():
    """(1 + i_e)^(1/12): the monthly accrual factor of the euro leg **[std]**.

    A smoothing of an annual credit across the months of the year, and it is a
    **[std]** simplification rather than a grid artefact: ``Euro_FR_S`` runs on this same
    monthly grid and does *not* smooth, crediting the whole of the year's `taux servi` in
    the anniversary month with the `effet cliquet`.  The euro leg here is a per-model-point
    rate and not a model, so the twelfth-of-a-year accrual is the cheapest reading that
    keeps the two legs on one clock; the real crediting machinery - the `participation aux
    benefices`, the PPB and its eight-year vintage ledger - is ``Euro_FR_S``'s.  Twelve of
    these factors compound to exactly ``1 + i_e``, so a full policy year of the euro leg is
    unaffected by the smoothing and only a mid-year exit sees it.
    """
    return (1.0 + euro_credit_rate()) ** (1.0 / 12.0)


def uc_return_mth(t):
    """r_uc(t): the UC support's return in month t, from the elected scenario.

    The scenario table holds **segments**: a monthly return applying from ``from_month``
    to ``to_month`` inclusive, both written in the model's own 0-based months, so the first
    segment of every shipped scenario opens at ``from_month = 0``.  A month outside every
    segment of the elected scenario raises, rather than falling back on a last-row default -
    a projection that has run off the end of its scenario is not projecting anything.
    """
    tbl = data.uc_scenario_table().loc[[uc_return_scenario()]]       # noqa: F821
    for lo, hi, r in zip(tbl["from_month"], tbl["to_month"], tbl["uc_return_mth"]):
        if int(lo) <= t <= int(hi):
            return float(r)
    raise ValueError("no scenario segment covers this month")


def unit_price_open(t):
    """p(t-1): the liquidation value at the **start** of month t.

    The close of month ``t - 1``, and :func:`unit_price_init` in the first month - the
    opening timing that keeps the price recursion off a month ``t = -1`` that does not
    exist.
    """
    if t <= 0:
        return unit_price_init()
    return unit_price(t - 1)


def unit_price(t):
    """p(t): the liquidation value of the composite UC support at the end of month t.

    **Exogenous.**  Art. A. 132-5 makes the unit count the thing guaranteed and the value
    the thing that is not, so the price path is an input and never a result.  Fund-level
    recurring costs, 1.60% a year on the market average, are inside it and accrue to the
    fund manager: they reduce the account value and are **not** insurer income.
    """
    return unit_price_open(t) * (1.0 + uc_return_mth(t))


def units_open(t):
    """n(t-1): the unit count held at the **start** of month t.

    The close of month ``t - 1``, and :func:`units_init` in the first month.  It is the
    count the management charge is taken on, which is the whole point of naming it.
    """
    if t <= 0:
        return units_init()
    return units(t - 1)


def fee_units(t):
    """n(t-1) c_m: the units cancelled by the management charge in month t.

    Taken on the **opening** unit count.  In a month with an arbitrage the opening and
    closing counts differ by the arbitrage's units, so charging on the closing count
    overstates the fee by 52.28 EUR against 59.54 EUR at ``t = 2`` on the anchor cell -
    immaterial monthly, systematic over decades, and a common source of a persistent
    reconciliation break against an administration system.
    """
    return units_open(t) * mgmt_fee_rate_uc_mth()


def mgmt_fee_uc_pp(t):
    """The UC management charge collected in month t, per policy, in EUR.

    ``fee_units(t) x p(t)``.  The dominant income line on this product, and the one whose
    level is a market average rather than a contractual rate.
    """
    return fee_units(t) * unit_price(t)


def arb_sched_pp(t):
    """The gross amount scheduled to be arbitraged out of the euro leg in month t.

    Before the cap at what the euro balance can actually release; see
    :func:`arb_amount_pp`.
    """
    p = arb_pattern()
    if p == "none":
        return 0.0
    if p == "one_off":
        return (float(model_point()["arb_amount"])
                if t == int(model_point()["arb_month"]) else 0.0)
    return float(model_point()["arb_amount"])


def arb_amount_pp(t):
    """A(t): the gross amount arbitraged from the euro leg into UC in month t.

    Capped at the euro balance after the month's accrual, so a `progressive` arbitrage
    stops of its own accord once the euro support is empty rather than driving it
    negative.  An arbitrage is **neither a premium nor a surrender**: it changes both legs
    and leaves :func:`cum_prem_net` untouched.
    """
    return min(arb_sched_pp(t), av_euro_aft_credit_pp(t))


def arb_fee_pp(t):
    """A(t) phi: the `frais d'arbitrage` collected in month t, per policy.

    Insurer income.  The amount leaving the euro leg is ``A``; the amount reaching the UC
    leg is ``A(1 - phi)``; the difference is this fee.
    """
    return arb_amount_pp(t) * arbitrage_fee_rate()


def arb_units(t):
    """A(t)(1 - phi)/p(t): the units bought by the month's arbitrage."""
    return arb_amount_pp(t) * (1.0 - arbitrage_fee_rate()) / unit_price(t)


def av_euro_open_pp(t):
    """V(t-1): the euro balance at the **start** of month t, before the accrual.

    The close of month ``t - 1``, and :func:`av_euro_init_pp` in the first month.
    """
    if t <= 0:
        return av_euro_init_pp()
    return av_euro_pp(t - 1)


def av_euro_aft_credit_pp(t):
    """The euro balance after the month's accrual and before any event.

    ``V(t-1) x (1 + i_e)^(1/12)``.  On the anchor cell ``29,700.00 x 1.025^(2/12) =
    29,822.48`` at ``t = 1``, which is the notes' own euro-leg check.
    """
    return av_euro_open_pp(t) * euro_credit_factor_mth()


def units_bef_wd(t):
    """The unit count after the management charge and the arbitrage, before a withdrawal.

    ``n(t-1) - fee_units(t) + arb_units(t)``.
    """
    return units_open(t) - fee_units(t) + arb_units(t)


def av_uc_bef_wd_pp(t):
    """U(t) before the withdrawal: the UC account value the pro-rata split is taken on."""
    return units_bef_wd(t) * unit_price(t)


def av_euro_bef_wd_pp(t):
    """V(t) before the withdrawal: the euro balance after the arbitrage has left it."""
    return av_euro_aft_credit_pp(t) - arb_amount_pp(t)


def wd_sched_pp(t):
    """The partial surrender scheduled in month t, before the cap at the account value."""
    p = wd_pattern()
    if p == "none":
        return 0.0
    if p == "one_off":
        return (float(model_point()["wd_amount"])
                if t == int(model_point()["wd_month"]) else 0.0)
    return av_pp_at(t, "BEF_WD") * float(model_point()["wd_rate"]) / 12.0


def wd_amount_pp(t):
    """W(t): the partial surrender settled in month t, per policy.

    An **owner election**, not a claim, which is why it has its own name and its own
    ``result_cf`` column.  Capped at the account value, so a programmed pattern draws the
    contract down to nothing rather than through it.  It reduces the floor base by its
    nominal amount, and it is the only event other than a premium that does.
    """
    return min(wd_sched_pp(t), av_pp_at(t, "BEF_WD"))


def wd_uc_pp(t):
    """W_uc(t): the UC component of the month's partial surrender.

    Split **pro rata across the supports**, which is the only default stated in a
    retrieved contract.  At ``t = 5`` on the anchor cell the UC share is 0.80665095, so
    4,033.25 EUR of the 5,000 EUR comes off the units and 966.75 EUR off the euro balance.
    An election that emptied the loss-making support first would change
    :func:`uc_cost_basis` and therefore the `prelevements sociaux`.
    """
    total = av_pp_at(t, "BEF_WD")
    if total <= 0.0:
        return 0.0
    return wd_amount_pp(t) * av_uc_bef_wd_pp(t) / total


def wd_eur_pp(t):
    """W_eur(t): the euro component of the month's partial surrender."""
    return wd_amount_pp(t) - wd_uc_pp(t)


def wd_units(t):
    """W_uc(t)/p(t): the units cancelled to fund the month's partial surrender."""
    return wd_uc_pp(t) / unit_price(t)


def units_bef_levy(t):
    """The unit count after the withdrawal and before the plancher premium."""
    return units_bef_wd(t) - wd_units(t)


def av_uc_bef_levy_pp(t):
    """U(t) after the withdrawal and before the plancher premium."""
    return units_bef_levy(t) * unit_price(t)


def av_euro_bef_levy_pp(t):
    """V(t) after the withdrawal and before the plancher premium."""
    return av_euro_bef_wd_pp(t) - wd_eur_pp(t)


def cum_prem_net(t):
    """S(t): the floor base - premiums net of the premium charge, less surrenders.

    It moves on a **premium or a surrender and on nothing else**.  An arbitrage moves
    value between the legs, pays a fee and leaves the guarantee untouched; letting it move
    the floor is a listed pitfall, and :func:`check_floor_base` asserts against it.

    The opening base of the first month is :func:`cum_prem_net_init`, the floor base at
    issue.
    """
    opening = cum_prem_net_init() if t <= 0 else cum_prem_net(t - 1)
    return opening - wd_amount_pp(t)


def wd_cum_pp(t):
    """Cumulative partial surrenders to the end of month t, accumulated independently.

    Exists so :func:`check_floor_base` can rebuild the floor base from the withdrawal
    series rather than from its own recursion.
    """
    opening = 0.0 if t <= 0 else wd_cum_pp(t - 1)
    return opening + wd_amount_pp(t)


def plancher_ratchet(t):
    """R(t): the ratchet level of a ``cliquet`` floor.

    Reduced **proportionally** by a partial surrender, because a ratchet is a value level
    rather than a premium tally - the ``simple`` base is reduced nominally, and on the same
    path at ``t = 11`` the two rules give 94,216.29 and 94,000.00.  Raised to the account
    value at each ratchet date, observed just before the plancher premium is levied.

    A ratchet date falls at the **end** of month ``t``, which is ``t + 1`` months from
    issue, so the ``n``-month ratchet fires where ``(t + 1) % n == 0``: the first annual
    ratchet is the end of ``t = 11``, the twelfth month.  The opening level of the first
    month is the account value at issue.
    """
    r = prem_to_av_pp() if t <= 0 else plancher_ratchet(t - 1)
    total = av_pp_at(t, "BEF_WD")
    if wd_amount_pp(t) > 0.0 and total > 0.0:
        r = r * (1.0 - wd_amount_pp(t) / total)
    n = plancher_ratchet_months()
    if n > 0 and (t + 1) % n == 0:
        r = max(r, av_pp_at(t, "BEF_LEVY"))
    return r


def plancher_amount(t):
    """F(t): the floor the death benefit is guaranteed not to fall below.

    ``simple``
        ``S(t)``, the running base of net premiums less surrenders.

    ``indexee``
        ``F(t-1) (1 + i_x)^(1/12) - W(t)``, the opening floor of the first month
        being :func:`cum_prem_net_init`, the floor at issue.  Indexing the
        running floor and then deducting the **nominal** withdrawal is
        arithmetically identical to indexing the withdrawal forward from its own
        date and deducting it later, which is the sources' rule that surrenders
        are indexed on the same basis as the floor [S1] [S3].

    ``cliquet``
        ``max(S(t), R(t))``, so the ratchet can only ever improve the sourced
        floor.
    """
    b = plancher_basis()
    if b == "simple":
        return cum_prem_net(t)
    if b == "indexee":
        opening = cum_prem_net_init() if t <= 0 else plancher_amount(t - 1)
        return (opening
                * (1.0 + plancher_index_rate()) ** (1.0 / 12.0)
                - wd_amount_pp(t))
    return max(cum_prem_net(t), plancher_ratchet(t))


def plancher_rate(t):
    """pi(a): the annual plancher tariff at the attained age, as a rate on the risk.

    The published premium per 10,000 EUR of `capital sous risque`, divided by 10,000:
    ``pi(65) = 0.0196``.  Zero once the cover has ceased - the rider is not elected, or the
    attained age has reached :func:`plancher_end_age`.

    An attained age **inside** the cover but outside the table raises.  That is
    deliberate: the tariff stops at 74 because the cover stops at 75, and an
    implementation that extrapolated it to a later cessation age would silently invent a
    price the sources do not contain.
    """
    if not plancher_flag() or age(t) >= plancher_end_age():
        return 0.0
    tbl = data.plancher_rate_table()                                 # noqa: F821
    a = age(t)
    if a not in tbl.index:
        raise ValueError("no plancher tariff at this attained age")
    return float(tbl.loc[a, "premium_per_10000"]) / 10000.0


def plancher_rate_mth(t):
    """pi(a)/12: the monthly step of the plancher tariff **[std]**.

    The published formula is weekly, ``Pr = K x (PA / 10 000) x 1/52`` observed each
    Friday; ``PA/12`` is the same annual cost applied once against a `capital sous risque`
    observed once instead of four or five times.  What is lost is the intra-month path of
    the net amount at risk.
    """
    return plancher_rate(t) / 12.0


def nar(t):
    """K(t): the `capital sous risque` - the net amount at risk.

    ``min(cap, max(0, F(t) - AV))``, observed once a month on the account value after the
    fee, the arbitrage and the withdrawal and before the levy.  Zero where the rider is
    not elected or the cover has ceased.

    The ``max(0, .)`` is not decoration.  Without it the rider pays a **negative** charge
    in every rising month and the death strain turns negative, which books the gain on the
    units as insurance profit.  And the cap is on the risk: the excess reduces the floor
    rather than truncating the beneficiary's benefit.
    """
    if not plancher_flag() or age(t) >= plancher_end_age():
        return 0.0
    return min(plancher_cap(),
               max(0.0, plancher_amount(t) - av_pp_at(t, "BEF_LEVY")))


def plancher_charge_pp(t):
    """The plancher premium levied in month t, per policy.

    ``K(t) x pi(a)/12`` - levied on the **net amount at risk** and never on the account
    value.  On the anchor cell at ``t = 11`` the correct charge is 27.18 EUR; on the account
    value it would be 126.35 EUR, a factor of 4.6.  It is nil whenever the account value
    is at or above the floor, which is the whole of the rider being a put.

    Capped at the account value it is taken from, so a levy cannot drive the contract
    negative.  The 15-20 EUR monthly thresholds below which the real levy is deferred to
    the following month have no expected-value consequence and are not modeled.
    """
    return min(nar(t) * plancher_rate_mth(t), av_pp_at(t, "BEF_LEVY"))


def plancher_levy_eur_pp(t):
    """The part of the month's plancher premium taken from the euro support.

    The whole of it under ``euro_first`` while the euro balance can cover it, and nothing
    under ``uc_units``.
    """
    if plancher_levy_source() != "euro_first":
        return 0.0
    return min(plancher_charge_pp(t), max(0.0, av_euro_bef_levy_pp(t)))


def plancher_levy_uc_pp(t):
    """The part of the month's plancher premium taken by cancelling units.

    Zero under ``euro_first`` while the euro support can pay, which is what keeps the unit
    count a deterministic function of the event schedule.  Where the euro balance runs out
    the remainder falls on the units whatever the election - and the count then becomes
    path-dependent, which is the mechanism by which a lower euro credited rate reaches the
    UC leg.
    """
    return plancher_charge_pp(t) - plancher_levy_eur_pp(t)


def plancher_levy_units(t):
    """The units cancelled to pay the month's plancher premium."""
    return plancher_levy_uc_pp(t) / unit_price(t)


def units(t):
    """n(t): the unit count held at the end of month t.

    ``n(t-1) - fee_units + arb_units - wd_units - plancher_levy_units``, the opening count
    being :func:`units_open`.  This is the quantity art. A. 132-5 makes the insurer's
    commitment: every charge is a cancellation of units and never a deduction of euros, so
    with the plancher premium taken from the euro support the count is
    **market-independent** - with no events at all it collapses to
    ``units_init() (1 - c_m)^(t + 1)``, which is the sequence the insurers publish in their
    own statutory tables.
    """
    return units_bef_levy(t) - plancher_levy_units(t)


def av_uc_pp(t):
    """U(t) = n(t) p(t): the UC account value per policy at the end of month t."""
    return units(t) * unit_price(t)


def av_euro_pp(t):
    """V(t): the euro account value per policy at the end of month t, after the levy.

    The notes' worked-example table prints this column post-levy, so each row's value is
    the next row's opening euro balance - :func:`av_euro_open_pp` reads it back.
    """
    return av_euro_bef_levy_pp(t) - plancher_levy_eur_pp(t)


def av_pp_at(t, timing):
    """The total account value per policy at a point inside policy month t.

    ``"OPENING"``
        the balance the month opens on, before the liquidation value has moved
        and before the euro leg accrues: ``av_pp(t - 1)``, and
        :func:`prem_to_av_pp` - the premium net of the `frais sur versement` -
        in the first month, ``t = 0``.  It is the term the roll-forward check
        starts from.

    ``"BEF_FEE"``
        after the liquidation value has moved and the euro leg has accrued,
        before the management charge.

    ``"BEF_WD"``
        after the management charge and the arbitrage; **this is the base the
        partial surrender is split pro rata on**.

    ``"BEF_LEVY"``
        after the withdrawal; **this is the base the `capital sous risque` is
        observed against**.

    ``"BEF_DECR"``
        after the plancher premium: the end-of-month account value, and the
        column the notes' worked-example table prints.  It is the surrender
        benefit per lapse and, with ``K(t)`` added, the death benefit.

    All five points are exposed so the ordering is inspectable rather than buried in one
    expression.
    """
    if timing == "OPENING":
        return (units_open(t) * unit_price_open(t)) + av_euro_open_pp(t)
    if timing == "BEF_FEE":
        return units_open(t) * unit_price(t) + av_euro_aft_credit_pp(t)
    if timing == "BEF_WD":
        return av_uc_bef_wd_pp(t) + av_euro_bef_wd_pp(t)
    if timing == "BEF_LEVY":
        return av_uc_bef_levy_pp(t) + av_euro_bef_levy_pp(t)
    if timing == "BEF_DECR":
        return av_uc_pp(t) + av_euro_pp(t)
    raise ValueError("invalid timing")


def av_pp(t):
    """The total account value per policy at the end of month t.

    ``av_pp_at(t, "BEF_DECR")`` under the house account-value name, and the column
    :func:`result_cf` publishes.  Note that on this product it is an **end**-of-month
    value, matching the notes' row t, and not the start-of-month reading some other models
    in the library give the same name.
    """
    return av_pp_at(t, "BEF_DECR")


def av_at(t, timing):
    """The in-force account value: ``av_pp_at(t, timing) x pols_if_at(t, "AFT_DECR")``.

    The account value is a **stock**, so it is weighted by the count the balance is still
    carried for once the month's decrements have gone — the notes' ``l(t + 1)`` — and not
    by the start-of-month exposure :func:`pols_if` that weights the month's *flows*.  At
    ``t = 11`` on the anchor cell ``77,330.08 x 0.968240 = 74,874.07``.
    """
    return av_pp_at(t, timing) * pols_if_at(t, "AFT_DECR")


def av_uc_at(t):
    """The in-force UC account value.

    The unit count at the liquidation value, weighted - arithmetic, and reproduced here
    without a valuation assumption of any kind.  On the conventional reading this is the
    French statutory `provision mathematique` for the UC engagement, and MACSF's notice is
    the one retrieved document that writes a `provision mathematique` recursion in units
    [S10 ART 11-12].  Art. R. 343-3 itself enumerates the eleven provisions and defines the
    provision mathematique generically; it says nothing about `unites de compte`, so the
    placement is **[unverified]** against any retrieved statutory or ACPR text.  The
    plancher liability is a separate engagement and **no retrieved document states how it
    is provisioned**, so this library asserts nothing about it.
    """
    return av_uc_pp(t) * pols_if_at(t, "AFT_DECR")


def av_euro_at(t):
    """The in-force euro account value.

    Published for completeness; the euro engagement's own reserve and its `provision pour
    participation aux benefices` belong to ``Euro_FR_S``.
    """
    return av_euro_pp(t) * pols_if_at(t, "AFT_DECR")


def uc_cost_basis_bef_wd(t):
    """B(t) before the month's withdrawal, after any investment into the UC leg.

    ``B(t-1) + A(t)(1 - phi)``, the opening basis of the first month being
    :func:`uc_cost_basis_init`.  An arbitrage into UC is an investment and adds to the
    cost basis; the arbitrage fee does not, because it never reaches the support.
    """
    opening = uc_cost_basis_init() if t <= 0 else uc_cost_basis(t - 1)
    return opening + arb_amount_pp(t) * (1.0 - arbitrage_fee_rate())


def uc_cost_basis(t):
    """B(t): the cumulative cost of the UC leg, the `prelevements sociaux` base.

    Investments add to it; an outflow removes its **pro-rata** share.  At ``t = 5`` on the
    anchor cell it falls from 79,250.00 to 75,420.62 on a 4,033.25 EUR UC surrender.
    """
    b = uc_cost_basis_bef_wd(t)
    u = av_uc_bef_wd_pp(t)
    if wd_uc_pp(t) > 0.0 and u > 0.0:
        b = b * (1.0 - wd_uc_pp(t) / u)
    return b


def wd_uc_gain_pp(t):
    """The taxable UC gain component of the month's partial surrender, per policy.

    ``W_uc (1 - B / U)``: the amount surrendered less its pro-rata cost.  At ``t = 5`` on
    the anchor cell ``4,033.25 x (1 - 79,250.00/83,469.22) = 203.87``.  **[std]**: no retrieved
    document sets out the arithmetic for a multisupport partial surrender.
    """
    u = av_uc_bef_wd_pp(t)
    if u <= 0.0:
        return 0.0
    return wd_uc_pp(t) * (1.0 - uc_cost_basis_bef_wd(t) / u)


def social_levy_wd_pp(t):
    """The `prelevements sociaux` withheld on the month's partial surrender, per policy.

    ``17.2% x max(0, gain)`` - 35.07 EUR at ``t = 5`` on the anchor cell.  **Withheld and
    remitted**: a pass-through, not insurer income and not an expense.
    """
    return social_levy_rate * max(0.0, wd_uc_gain_pp(t))             # noqa: F821


def social_levy_decr_pp(t):
    """The `prelevements sociaux` withheld per exiting policy at the month's decrements.

    The UC leg is taxed **only at `denouement`** - surrender, term or death - so the levy
    is contingent on a gain and is zero on a loss.  At ``t = 11`` on the anchor cell the UC
    leg is 17,284.34 EUR under water and the levy is nil, and any excess already levied
    year by year on the euro leg is restituted at final liquidation under art. L. 136-7
    III bis.  The plancher top-up above the account value is treated as outside the levy
    base; no retrieved document states whether it is, and the alternative reading changes
    the beneficiary's net proceeds and not the insurer's cash flow.
    """
    return social_levy_rate * max(0.0, av_uc_pp(t) - uc_cost_basis(t))  # noqa: F821


def mort_rate(t):
    """q_a: the annual best-estimate mortality rate at the attained age **[std]**.

    The shipped table rate times ``mort_be_factor``, which is anchored so the male rate at
    age 65 reproduces the notes' placeholder 1.20% a year exactly.  It is an
    **assumption** and the plancher tariff is a **price**; their difference is the rider's
    margin, and because no insurer publishes the mortality, the loading or the margin
    behind a tariff, the sign of that margin at any age is genuinely unknown.  Sensitivity
    test the two independently, never as a single "plancher basis".
    """
    x = min(age(t), omega_age)                                       # noqa: F821
    return min(1.0, float(data.mort_table().loc[                     # noqa: F821
        (sex(), x), "mort_rate"]) * mort_be_factor)                  # noqa: F821


def mort_rate_mth(t):
    """q_m = 1 - (1 - q_a)^(1/12): the monthly mortality rate **[std]**.

    Derived **geometrically** and not by dividing by twelve, which is what makes
    ``[(1 - q_m)(1 - w_m)]^12 = (1 - q_a)(1 - w_a)`` hold exactly - the notes' decrement
    check, and the only sensible test of the conversion.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """w_base(y): the table annual total-surrender rate in month t **[std]**.

    2 / 4 / 6 / **12** / 6 percent by band, the 12% falling in policy year 8.  Policy
    years beyond the table take its last row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate"])


def return_12m(t):
    """R_12m: the trailing twelve-month UC return driving the performance multiplier.

    Measured over the twelve **completed** months ending at the start of month ``t``, so it
    needs twelve months of history and is undefined before ``t = 12``.  Where it is
    undefined it returns the reference return, which makes the multiplier exactly 1 - and
    that is why the anchor cell's twelve months carry the flat 2.00% a year the notes'
    worked example states even though its path falls 21.97% over the year.
    """
    if t <= 11:
        return uc_return_ref                                         # noqa: F821
    return unit_price_open(t) / unit_price_open(t - 12) - 1.0


def perf_factor(t):
    """M_perf(t) = min(2, 1 + 2 max(0, g_ref - R_12m)): the performance multiplier **[std]**.

    Poor recent performance raises surrender.  It is 1 on any deterministic run at the
    reference return, and 1 through the first twelve months of every run.
    """
    shortfall = max(0.0, uc_return_ref - return_12m(t))              # noqa: F821
    return min(perf_factor_cap,                                      # noqa: F821
               1.0 + perf_factor_slope * shortfall)                  # noqa: F821


def plancher_factor(t):
    """M_pl(t): the plancher moneyness multiplier, 0.5 while the floor is in the money.

    A policyholder holding an in-the-money guarantee has a reason not to surrender that a
    UK bondholder does not: surrendering forfeits it.  This is the one behavioural
    assumption specific to this product, it is a pure **[std]** invention with no evidence
    behind it, and it should be the first thing a user replaces - which is why
    :func:`lapse_dynamic` elects it rather than the model wiring it in.  1.0 wherever the
    rider is not elected, the cover has ceased or the units are above the floor.
    """
    if lapse_dynamic() != "full" or not plancher_flag() or nar(t) <= 0.0:
        return 1.0
    return plancher_lapse_mult                                       # noqa: F821


def lapse_rate(t):
    """w_ann: the annual total-surrender rate applied in month t.

    The base table alone where :func:`lapse_dynamic` is ``none``, and
    ``min(cap, w_base x M_perf x M_pl)`` where it is ``full``.  A surrender costs the
    insurer nothing at the point of exit - the surrender value is the account value across
    all supports, with no exit charge - while truncating the entire future charge stream
    **and** extinguishing an in-the-money guarantee, which is why persistency dominates
    this product's value and why the two effects pull in opposite directions.
    """
    if lapse_dynamic() == "none":
        return lapse_rate_base(t)
    return min(lapse_rate_cap,                                       # noqa: F821
               lapse_rate_base(t) * perf_factor(t) * plancher_factor(t))


def lapse_rate_mth(t):
    """w_m = 1 - (1 - w_ann)^(1/12): the monthly total-surrender rate **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if(t):
    """l(t): the in-force probability at the **start** of policy month t.

    ``pols_if(0) = pols_if_init()``, and thereafter
    ``pols_if(t) = pols_if(t-1)(1 - q_m(t-1))(1 - w_m(t-1))``, deaths before surrenders
    **[std]**.  It is the weight on every flow of month t and the first column of
    :func:`result_cf`, so the two agree row by row: a cash flow divided by its own row's
    ``pols_if`` is the per-policy amount.

    The notes' ``l(t + 1)`` — the count once month t's decrements have gone — is
    :func:`pols_if_at` ``(t, "AFT_DECR")``.
    """
    if t <= 0:
        return pols_if_init()
    return pols_if(t - 1) * (1.0 - mort_rate_mth(t - 1)) * (1.0 - lapse_rate_mth(t - 1))


def pols_if_at(t, timing):
    """The in-force probability at a point inside policy month t.

    ``"BEF_DECR"``
        the start of the month, before any decrement; :func:`pols_if` ``(t)``.

    ``"BEF_LAPSE"``
        after the month's deaths and before its surrenders — the order is
        **deaths before surrenders** **[std]**.

    ``"AFT_DECR"``
        the notes' ``l(t + 1)``: the count still in force once the month's
        decrements have gone.  Equal to ``pols_if(t + 1)`` wherever the
        projection runs on, and computed here directly so it also resolves in
        the horizon month.

    The three timings are the ``CashValue_SE`` forms the library's shared vocabulary
    prescribes.  They exist so that the end-of-month count has a name of its own rather
    than borrowing the start-of-month one, which is exactly the confusion this model
    shipped with before.
    """
    pols = pols_if(t)
    if timing == "BEF_DECR":
        return pols
    pols = pols * (1.0 - mort_rate_mth(t))
    if timing == "BEF_LAPSE":
        return pols
    pols = pols * (1.0 - lapse_rate_mth(t))
    if timing == "AFT_DECR":
        return pols
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths in policy month t, against the in-force count at the start of it."""
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Total surrenders in month t, from the survivors of that month's mortality."""
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def claims(t, kind=None):
    """Gross benefit outgo in policy month t, by kind; the total when kind is omitted.

    ``"DEATH"``
        ``AV + K`` per death - the account value plus the `capital sous
        risque`, which is ``max(F, AV)`` written the way the model uses it.
        At ``t = 11`` on the anchor cell that is ``77,330.08 + 16,642.74 =
        93,972.82``, of which only the 16,642.74 is the insurer's.

    ``"LAPSE"``
        ``AV`` per surrender: the account value across all supports, with no
        exit charge.

    These are **gross** flows.  They are published so the reader can see the whole picture,
    but they are not in :func:`net_cf`, because :func:`av_releases` cancels them against
    the account value - all except the death strain.  See the Space docstring.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE"))
    av = av_pp_at(t, "BEF_DECR")
    if kind == "DEATH":
        return pols_death(t) * (av + nar(t))
    if kind == "LAPSE":
        return pols_lapse(t) * av
    raise ValueError("invalid kind")


def withdrawals(t):
    """Partial-surrender outgo in month t, funded from both legs pro rata.

    An owner election rather than a claim, which is why it has its own name and its own
    ``result_cf`` column.
    """
    return pols_if(t) * wd_amount_pp(t)


def av_releases(t):
    """The account value released to fund the month's death and surrender benefits.

    ``AV x (deaths + surrenders)``.  The gross benefit outgo less this is exactly the
    plancher death strain, which is the only part the insurer funds from its own
    resources.
    """
    return av_pp_at(t, "BEF_DECR") * (pols_death(t) + pols_lapse(t))


def prem_charge(t):
    """The `frais sur versement` collected at issue; 1,000.00 EUR on the anchor cell.

    Booked in the **first projected month**, ``t = 0``, which is where the notes book it
    too: the issue instant is not a row of its own, so the premium charge and the
    acquisition expense both fall in month ``t = 0``, weighted at ``pols_if(0) = 1``.
    """
    if t != 0:
        return 0.0
    return premium() * prem_charge_rate() * pols_if(0)


def mgmt_fee_uc(t):
    """The UC management charge collected in month t; **insurer income**.

    ``pols_if(t) x mgmt_fee_uc_pp(t)``, the notes' ``l(t)`` start-of-month weight.  The notes'
    worked-example table prints the per-policy column, which sums to 630.20 EUR over
    year 1; this weighted line sums to 621.33 EUR.
    """
    return pols_if(t) * mgmt_fee_uc_pp(t)


def arbitrage_fee(t):
    """The `frais d'arbitrage` collected in month t; **insurer income**."""
    return pols_if(t) * arb_fee_pp(t)


def plancher_charge(t):
    """The plancher premium collected in month t; **insurer income**.

    Zero in every month the account value is at or above the floor, which is seven of the
    anchor cell's twelve.
    """
    return pols_if(t) * plancher_charge_pp(t)


def plancher_strain(t):
    """The non-unit cost of the month's deaths: the `capital sous risque`, exactly.

    ``pols_if(t) q_m(t) K(t)``, the notes' ``l(t) q_m K(t)``.  The whole of the account
    value is funded by cancelling units and
    by the euro balance, so the insurer's cost per death is ``K(t)`` and nothing else.
    """
    return pols_death(t) * nar(t)


def social_levy_uc(t):
    """The `prelevements sociaux` withheld on the UC leg in month t.

    Partial surrenders plus the exits at the month's decrements.  A **pass-through**:
    withheld from the policyholder and remitted, so it is neither insurer income nor an
    expense and it is **not** in :func:`net_cf`.  It is published as its own column so
    that its exclusion is visible rather than merely asserted.
    """
    return (pols_if(t) * social_levy_wd_pp(t)
            + (pols_death(t) + pols_lapse(t)) * social_levy_decr_pp(t))


def expenses(t):
    """Acquisition and maintenance expense in month t **[std]**.

    400 EUR per policy of acquisition expense in the first projected month, ``t = 0``,
    which is the issue month - then 40 EUR per policy a year, level, taken monthly at the
    start-of-month exposure.  No retrieved document gives an expense basis of any kind.
    """
    acq = expense_acq * pols_if(0) if t == 0 else 0.0                # noqa: F821
    return acq + expense_maint / 12.0 * pols_if(t)                   # noqa: F821


def net_cf(t):
    """The **non-unit** cash flow of month t, income positive.

    ``premium charge + management charge + arbitrage fee + plancher premium - expenses -
    plancher death strain``.  Not a gross liability total, and that is a product fact
    rather than a departure: every benefit is funded by cancelling units and by drawing the
    euro balance, so a gross presentation would add the same money to both sides.

    Three amounts that move on this contract are deliberately **not** here.  The
    `prelevements sociaux` are withheld and remitted.  The fund-level recurring costs sit
    inside the liquidation value and accrue to the fund manager - adding the 1.60% to
    year 1 of the anchor cell would put 1,136.76 EUR against a true ``net_cf`` of
    1,262.66 EUR, both weighted at the same start-of-month exposure.  (The unweighted
    per-policy sum is 1,152.86 EUR and is not comparable with a weighted ``net_cf``.)  And
    the euro leg's credited interest is a policyholder credit whose margin is
    ``Euro_FR_S``'s output: reading this stream as the contract's total margin is a listed
    pitfall.
    """
    return (prem_charge(t) + mgmt_fee_uc(t) + arbitrage_fee(t) + plancher_charge(t)
            - expenses(t) - plancher_strain(t))


def uc_growth_pp(t):
    """The month's UC investment return, per policy: ``n(t-1) x (p(t) - p(t-1))``.

    Computed from the **opening** unit count and the price move alone, independently of
    every charge, so that :func:`check_av_roll_fwd` is an identity the recursion has to
    satisfy rather than a restatement of it.
    """
    return units_open(t) * (unit_price(t) - unit_price_open(t))


def euro_interest_pp(t):
    """The month's euro credited interest, per policy: ``V(t-1) x ((1+i_e)^(1/12) - 1)``.

    A **policyholder credit**, not an insurer cash flow: ``i_e`` is already net of the euro
    management charge, so the euro leg produces no margin line in this model.
    """
    return av_euro_open_pp(t) * (euro_credit_factor_mth() - 1.0)


def check_av_roll_fwd_resid(t):
    """The account value roll-forward residual in month t; zero everywhere.

    ``AV(t) - [AV opening + UC return + euro interest - management charge - arbitrage fee
    - withdrawal - plancher premium]``, per policy, the opening balance being
    ``av_pp_at(t, "OPENING")`` - the premium net of the `frais sur versement` in the first
    month.  The growth terms are built from the
    opening unit count and the opening euro balance, so this is a genuine identity and not
    a restatement: charging the management fee on the closing unit count, applying last
    month's price to it, forgetting that the arbitrage fee leaves the contract, or netting
    the withdrawal twice all show up here.
    """
    built = (av_pp_at(t, "OPENING") + uc_growth_pp(t) + euro_interest_pp(t)
             - mgmt_fee_uc_pp(t) - arb_fee_pp(t) - wd_amount_pp(t)
             - plancher_charge_pp(t))
    return av_pp_at(t, "BEF_DECR") - built


def check_av_roll_fwd():
    """True when the account value roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call the same check across every account-value model in the library.
    """
    tol = roll_fwd_tol * max(1.0, premium())                         # noqa: F821
    return all(abs(check_av_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_unit_roll_fwd_resid(t):
    """The unit count roll-forward residual in month t; zero everywhere.

    ``n(t) - [n(t-1)(1 - c_m) + arbitrage units - withdrawal units - levy units]``.  The
    fee term is written as a **factor on the opening count** rather than reusing
    :func:`fee_units`, so a fee taken on the closing count breaks it; and the levy term is
    what makes the check say something about the rider - under ``euro_first`` it is zero
    and the count is market-independent, and where the euro support cannot pay it is not.
    """
    built = (units_open(t) * (1.0 - mgmt_fee_rate_uc_mth())
             + arb_units(t) - wd_units(t) - plancher_levy_units(t))
    return units(t) - built


def check_unit_roll_fwd():
    """True when the unit count closes in every projected month."""
    tol = roll_fwd_tol * max(1.0, units_init())                      # noqa: F821
    return all(abs(check_unit_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if_at(t, "AFT_DECR") - deaths - surrenders``, the notes'
    ``l(t) - l(t+1) - deaths - surrenders``.  There is no maturity term: the contract is
    written `viagere`, so the projection simply stops at :func:`proj_len` with a positive
    in-force count rather than running the population out.
    """
    return (pols_if(t) - pols_if_at(t, "AFT_DECR")
            - pols_death(t) - pols_lapse(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month."""
    return all(abs(check_pols_roll_fwd_resid(t)) <= pols_tol         # noqa: F821
               for t in range(proj_len()))


def check_floor_base_resid(t):
    """The floor-base residual in month t; zero everywhere.

    ``S(t) - [S_init - cumulative withdrawals]``.  :func:`cum_prem_net` reaches month t by
    its own recursion and :func:`wd_cum_pp` accumulates the withdrawals by another, so a
    model that let an **arbitrage** move the floor - the listed pitfall - would show it
    here as a residual of the arbitraged amount.  On the anchor cell the 10,000 EUR switch
    at ``t = 2`` leaves the floor at 99,000.00.
    """
    return cum_prem_net(t) - (cum_prem_net_init() - wd_cum_pp(t))


def check_floor_base():
    """True when the floor base moves on premiums and surrenders alone."""
    tol = roll_fwd_tol * max(1.0, premium())                         # noqa: F821
    return all(abs(check_floor_base_resid(t)) <= tol
               for t in range(proj_len()))


def check_nar_bounds_resid(t):
    """How far the `capital sous risque` falls outside ``[0, cap]``; zero everywhere.

    Signed: negative where ``K(t)`` has gone below zero, positive where it has run past
    the cap.  A net amount at risk that goes negative turns the rider into a rebate and
    books the gain on the units as insurance profit, and one that runs past the cap prices
    a risk the contract does not carry.
    """
    k = nar(t)
    if k < 0.0:
        return k
    if k > plancher_cap():
        return k - plancher_cap()
    return 0.0


def check_nar_bounds():
    """True when the `capital sous risque` stays inside ``[0, cap]`` in every month."""
    return all(check_nar_bounds_resid(t) == 0.0
               for t in range(proj_len()))


def check_benefit_funding_resid(t):
    """How much of the month's benefit outgo the account value does **not** fund.

    ``claims(t) - av_releases(t) - plancher_strain(t)``, which is **zero by
    construction**: the death benefit is written as ``AV + K`` and the surrender benefit as
    ``AV``, so the identity holds by the way :func:`claims` is spelled.  It is published
    anyway, because the construction it asserts is the one thing about this product that is
    easy to get wrong in a different place - a model that paid the death benefit as
    ``max(F, AV)`` and *also* released the account value, or that took the strain as the
    whole benefit rather than as ``K``, would be inconsistent with these three cells and
    the residual would move.
    """
    return claims(t) - av_releases(t) - plancher_strain(t)


def check_benefit_funding():
    """True when every benefit is funded by the account value plus the death strain."""
    tol = roll_fwd_tol * max(1.0, premium())                         # noqa: F821
    return all(abs(check_benefit_funding_resid(t)) <= tol
               for t in range(proj_len()))


def result_cf():
    """Result table of cashflows, indexed by policy month t = 0, 1, ..., proj_len() - 1.

    ``pols_if`` is the in-force probability at the **start** of the month, which is the
    weight carried by every flow on its own row - divide a flow by it and the per-policy
    amount comes back.  ``av_pp`` beside it is the **end**-of-month account value per
    policy; weighted, that balance is :func:`av_at`, which uses
    ``pols_if_at(t, "AFT_DECR")`` instead.
    ``net_cf`` is the **non-unit** stream - what accrues to the insurer on the UC leg and
    the rider - while ``claims_death``, ``claims_lapse``, ``withdrawals`` and
    ``av_releases`` show the gross picture they net against.  ``social_levy_uc`` is
    published precisely because it is **not** in ``net_cf``: it is withheld from the
    policyholder and remitted.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "prem_charge": [prem_charge(t) for t in ts],
            "mgmt_fee_uc": [mgmt_fee_uc(t) for t in ts],
            "arbitrage_fee": [arbitrage_fee(t) for t in ts],
            "plancher_charge": [plancher_charge(t) for t in ts],
            "plancher_strain": [plancher_strain(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "av_releases": [av_releases(t) for t in ts],
            "social_levy_uc": [social_levy_uc(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of the account value recursion, indexed by t = 0, 1, ..., proj_len() - 1.

    The notes' worked-example table, column for column: the liquidation value, the unit
    count, the two legs, the end-of-month account value, the floor, the `capital sous
    risque`, and the two per-policy charges.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "unit_price": [unit_price(t) for t in ts],
            "units": [units(t) for t in ts],
            "av_uc_pp": [av_uc_pp(t) for t in ts],
            "av_euro_pp": [av_euro_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "plancher_amount": [plancher_amount(t) for t in ts],
            "nar": [nar(t) for t in ts],
            "mgmt_fee_uc_pp": [mgmt_fee_uc_pp(t) for t in ts],
            "plancher_charge_pp": [plancher_charge_pp(t) for t in ts],
            "cum_prem_net": [cum_prem_net(t) for t in ts],
            "uc_cost_basis": [uc_cost_basis(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

mort_be_factor = 0.8

uc_return_ref = 0.049

perf_factor_slope = 2.0

perf_factor_cap = 2.0

plancher_lapse_mult = 0.5

lapse_rate_cap = 0.35

social_levy_rate = 0.172

expense_acq = 400.0

expense_maint = 40.0

roll_fwd_tol = 1e-9

pols_tol = 1e-12

pd = ("Module", "pandas")
