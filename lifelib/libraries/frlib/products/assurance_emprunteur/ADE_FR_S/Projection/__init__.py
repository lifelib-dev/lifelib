# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.ADE_FR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked-example anchor cell
    >>> Projection.point_id = 9            # a claim in payment at duration 18 months

``t`` counts **policy months**, 0-based: ``t = 0`` is the first projected month and
``t = proj_len() - 1 = loan_term_months() - 1`` the last, so the frame is
``range(proj_len())``. Month ``t`` runs from time ``t`` to time ``t + 1``: the premium
falls at its beginning, and the instalment, the transitions and all benefit at its end.
The technical notes carry the loan balance and the state probabilities at a **time
point**, on their own 0-based index ``k`` with ``k = 0`` at adhesion — ``crd(k)``,
``l_h(k)``, ``l_itt(k, z)`` and ``l_ipt(k)``, with ``crd(0) = capital_initial`` and
``l_h(0) = 1``. Month ``t`` therefore **opens** on ``crd(t)`` and ``l_h(t)`` and
**closes** on ``crd(t + 1)`` and ``l_h(t + 1)``, so :func:`pols_healthy` ``(t)`` is the
notes' ``l_h(t)`` and :func:`pols_itt_dur` ``(t, z)`` its ``l_itt(t, z)``. That is
deliberate: every cash flow on a :func:`result_cf` row is then weighted by a state count
on the same row. The notes' end-of-month quantities are published too — the ``l(t + 1)``
values — as :func:`pols_healthy_close`, :func:`pols_itt_close` and
:func:`pols_ipt_close`, so the worked-example table can be read off directly.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/assurance_emprunteur/``, read at run time rather than stored inside the model.
The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``ADE_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.ADE_FR_S.Data`,
reached here through the ``data`` Reference:

========================  ==================================  ==========================
Reference                 Cells                               File
========================  ==================================  ==========================
model_point_file          data.model_point_table()            model_point_table.csv
mort_table_file           data.mort_table()                   mort_table.csv
itt_inception_file        data.itt_inception_table()          itt_inception_table.csv
itt_termination_file      data.itt_termination_table()        itt_termination_table.csv
franchise_file            data.franchise_table()              franchise_table.csv
lapse_table_file          data.lapse_table()                  lapse_table.csv
crd_rate_file             data.crd_rate_table()               crd_rate_table.csv
========================  ==================================  ==========================

There is no loan schedule file: the *échéancier* is computed here and checked.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for population counts, plural nouns
for cash flows, ``*_rate`` for annual rates and ``*_rate_mth`` for monthly ones,
``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind`` string.
The technical notes use compact actuarial symbols and French terms of art instead. The
mapping is:

=========================  ==================================  ==========================
Notes symbol               Cells                               Meaning
=========================  ==================================  ==========================
(the model point row)      model_point()                       The selected model point
entry_age                  age_at_entry()                      Age at adhesion
a                          age(t)                              Attained age in month t
y                          policy_year(t)                      Policy year containing t
(none)                     duration(t)                         Completed policy years, t // 12
(none)                     duration_mth(t)                     Months elapsed at the start of t
T = loan_term_months       proj_len()                          Months projected; last t is T - 1
i                          loan_rate_mth()                     Monthly loan rate, nominal/12
ech                        echeance()                          Level monthly instalment
crd(k)                     crd(k)                              Capital restant du at time k
(none)                     loan_interest_total()               T x ech - capital initial
Q                          quotite()                           Insured share of the loan
IR                         indemnity_ratio()                   1, or the income loss ratio
z                          (the duration argument)             Months since payment start
(none)                     itt_max_months()                    The 1 095-day cap, in months
(none)                     claim_dur_year(z)                   Duration year containing z
D(t)                       cover_deces(t)                      Deces guarantee in force
P(t)                       cover_ptia(t)                       PTIA guarantee in force
I(t)                       cover_itt(t)                        ITT/IPT guarantee in force
mort_rate(a)               mort_rate(t)                        Healthy-life annual mortality
q_h                        mort_rate_mth(t)                    The same, monthly
ptia_rate(a)               ptia_rate(t)                        PTIA annual incidence
q_ptia                     ptia_rate_mth(t)                    The same, monthly
itt_inception_rate(a)      itt_inception_rate(t)               Annual ITT payment inception
iota                       itt_inception_rate_mth(t)           The same, monthly
lapse_rate(y)              lapse_rate(t)                       Annual resiliation rate
(the table)                lapse_rate_base(t)                  Before the substitution uplift
w                          lapse_rate_mth(t)                   The same, monthly
gap(y)                     prem_gap(t)                         Premium gap to the market
market_prem_pp(y)          market_prem_pp(t)                   The substitute's price
rho(z)                     itt_recovery_rate_mth(z)            Monthly ITT recovery
tau(z)                     itt_to_ipt_rate_mth(z)              Monthly ITT to IPT transition
q_s(z)                     itt_mort_rate_mth(z)                Monthly death in ITT
s_itt(z)                   itt_surv_step(z)                    Monthly ITT persistency
(the three vectors)        itt_rate_vectors()                  rho, tau, q_s and s_itt
S(z)                       itt_surv(z)                         In ITT at duration z
(the supplementary sum)    itt_annuity_months()                Expected months paid
ipt_mort_factor x mort     mort_rate_ipt(t)                    Annual mortality in IPT
q_ipt                      mort_rate_ipt_mth(t)                The same, monthly
crd_rate(a)                crd_rate(t)                         CRD-basis annual premium rate
prem_pp(y)                 prem_pp(t)                          Monthly premium per policy
prem(t)                    premiums(t)                         Premium income
l_h(t)                     pols_healthy(t)                     In healthy at start of t
l_h(t+1)                   pols_healthy_close(t)               In healthy at end of t
l_itt(t, z)                pols_itt_dur(t, z)                  In ITT at duration z
l_itt(t)                   pols_itt(t)                         Total in ITT at start of t
l_itt(t+1)                 pols_itt_close(t)                   Total in ITT at end of t
(the whole vector)         itt_cohorts(t)                      l_itt(t, .) as a list
(before the transfer)      itt_cohorts_raw(t)                  The same, un-transferred
l_ipt(t)                   pols_ipt(t)                         In IPT at start of t
l_ipt(t+1)                 pols_ipt_close(t)                   In IPT at end of t
(before the transfer)      pols_ipt_raw(t)                     The same, un-transferred
(none)                     pols_if(t)                          healthy + ITT + IPT
(none)                     pols_if_at(t, timing)               BEF_DECR / AFT_DECR
(none)                     pols_if_init()                      Policies at issue, 1.0
dth_h(t)                   pols_death_healthy(t)               Deaths out of healthy
ptia_h(t)                  pols_ptia(t)                        PTIA claims out of healthy
lapses(t)                  pols_lapse(t)                       Resiliations out of healthy
n_itt(t)                   pols_itt_inception(t)               New ITT payment inceptions
h_stay(t)                  pols_healthy_stay(t)                Staying in healthy
rec_itt(t)                 pols_itt_recovery(t)                Recoveries back to healthy
trn_ipt(t)                 pols_itt_to_ipt(t)                  ITT to IPT transitions
dth_itt(t)                 pols_itt_death(t)                   Deaths in ITT
stay(t, .) summed          pols_itt_stay(t)                    ITT mass paid for month t
cap_itt(t)                 pols_itt_cap(t)                     Reaching the 1 095-day cap
ipt_share x cap_itt        pols_cap_to_ipt(t)                  Assessed into IPT at the cap
(1 - share) x cap_itt      pols_cap_return(t)                  Returned to healthy at the cap
(none)                     pols_ipt_entry(t)                   All entrants to IPT
dth_ipt(t)                 pols_ipt_death(t)                   Deaths in IPT
ipt_stay(t)                pols_ipt_stay(t)                    Surviving in IPT
(the BOM transfer)         pols_itt_transfer(t)                ITT mass moved at cover end
(the BOM transfer)         pols_ipt_transfer(t)                IPT mass moved at cover end
(none)                     pols_ipt_capital(t)                 Leaving on the crd IPT basis
(none)                     pols_exit(t)                        All exits from the model
(none)                     pols_exit_cum(t)                    Cumulative exits before t
(none)                     pols_maturity(t)                    In force at loan expiry
crd(t+1) x Q               benefit_deces_pp(t)                 Deces / PTIA capital
ech x Q x IR               benefit_itt_pp()                    Monthly ITT / IPT amount
ben_deces(t)               claims(t, "DEATH")                  Death benefit outgo
ben_ptia(t)                claims(t, "PTIA")                   PTIA benefit outgo
ben_itt(t)                 claims(t, "ITT")                    ITT benefit outgo
ben_ipt(t)                 claims(t, "IPT")                    IPT benefit outgo
0                          claims(t, "LAPSE")                  Surrender outgo; always zero
0                          claims(t, "MATURITY")               Maturity outgo; always zero
e_m(y), ec_m(y)            expense_maint, expense_claim        Expense levels p.a.
(none)                     inflation_factor(t)                 Expense inflation factor
expenses(t)                expenses(t)                         Maintenance + claim expense
liability_cf(t)            liability_cf(t)                     The notes' outgo-positive CF
net_cf(t)                  net_cf(t)                           The same, income positive
v(t)                       disc_factor(t)                      Worked-example discount factor
(none)                     pv_premiums(), pv_claims()          Present values in Checks
=========================  ==================================  ==========================

Four names needed care.

The notes' ``ben_deces`` and ``ben_ptia`` are reached as ``claims(t, "DEATH")`` and
``claims(t, "PTIA")``, in English, because ``claims`` is the library's one benefit-outgo
cells and the ``kind`` argument names the column it produces. The French terms stay in
the prose, where they are the name of the thing.

``mort_rate`` is the **healthy-life** rate, because that is what ``mort_rate`` means in
every other model in this library. Mortality in claim is :func:`itt_mort_rate`, keyed by
claim duration, and mortality in IPT is :func:`mort_rate_ipt`, keyed by month. Three
mortality rates on two clocks, and the model never mixes them.

``t`` is the policy month, 0-based, and ``z`` the claim duration, running
``1 ... itt_max_months()``. Rates out of ``healthy`` take ``t``; rates out of ITT take
``z``. They are different clocks and the model never mixes them.

:func:`crd` is **not** on the month index. It is a time-point cells: ``crd(k)`` is the
balance at time ``k``, the *capital restant dû* after the ``k``-th instalment, with
``crd(0) = capital_initial`` at adhesion and ``crd(T) = 0``. Month ``t`` therefore opens
on ``crd(t)`` and closes on ``crd(t + 1)``, and the two differ by that month's capital
repayment — EUR 609.20 over the first month on the anchor cell. The Décès and PTIA
capital of month ``t`` is the **closing** balance ``crd(t + 1)``, the instalment falling
on the day of death being deemed due, and whichever convention is chosen must be used
everywhere.

.. rubric:: Four states, and why the model needs all of them

Healthy, ITT (*incapacité temporaire totale*), IPT (*invalidité permanente et totale*)
and dead, with *résiliation* and PTIA as further exits from healthy and **recovery
flowing back from ITT to healthy**::

        inception iota            recovery rho
   healthy ───────────────▶ ITT ───────────────▶ healthy
      │                      │  ╲ tau
      │ mortality q_h        │   ╲
      │ PTIA q_ptia          │    ▼
      │ resiliation w        │   IPT ──── q_ipt ───▶ dead
      ▼                      │            (no recovery)
   dead / claimed / lapsed   └──── q_s ───▶ dead

This is the ``income_protection`` / ``IP_UK_S`` three-state chassis with a fourth state
and one extra mechanism: **IPT has no recovery**. Once a life is assessed above the 66 %
*barème croisé* threshold the only exits are death and the guarantee's age limit, so the
IPT annuity can run to the end of the loan while the ITT one is capped at three years.
That asymmetry is what makes ``ipt_share_at_cap`` a first-order assumption.

.. rubric:: The in-claim population is two-dimensional, and the cap assesses it

ITT termination rates depend on how long the claim has already run — recovery falls
0.55 to 0.15 across the three duration years while the IPT transition rises 0.02 to 0.12
— so the model tracks ``l_itt(t, z)`` cohort by cohort. :func:`itt_cohorts` holds the
whole vector for one month and is the model's only list-valued cells; :func:`pols_itt_dur`
reads an element out of it so the notes' two-dimensional object is still addressable by
name. The vector is rebuilt rather than mutated on each step, so a month already computed
is never rewritten by a later one.

At ``z = itt_max_months()`` — 36 months, the sourced 1 095-day cap — the surviving cohort
is **assessed, not advanced**: ``ipt_share_at_cap`` of it passes to IPT and the rest
returns to healthy. If cohort 36 simply advanced to cohort 37 the ITT claim would run for
ever and IPT would never be fed from the cap. On the anchor cell that is 0.198077 of every
inception still in ITT at three years, of which 0.069327 consolidates.

.. rubric:: The guarantees end at different ages, and the premium does not

:func:`cover_deces`, :func:`cover_ptia` and :func:`cover_itt` are three separate
indicators because the three cover-end ages differ — 85, 70 and 70 on the anchor cell,
against a loan of 240 months. Collapsing Décès and PTIA into one decrement is
tempting, since they pay the identical ``crd(t + 1) x quotite``, and it is wrong: a collapsed
decrement either pays PTIA after 70 or stops paying death before 85.

At the first month where the ITT/IPT cover has ceased, any claim in payment is **moved**
into healthy at the beginning of the month, before any transition: :func:`pols_itt_transfer`
and :func:`pols_ipt_transfer` are that movement. Those lives are alive, still death
covered and still paying — deleting them instead would break the state identity and
destroy the death cover they still hold. The premium is *nivelé* and does **not** fall
when the cover shrinks: on the anchor cell that is 24 months x EUR 140.00 of premium
against death cover alone.

.. rubric:: Premiums come from healthy alone

:func:`premiums` is carried on :func:`pols_healthy` and never on :func:`pols_if`.
Premiums are waived in claim, so projecting income from lives in ITT or IPT overstates it
by the whole in-claim population. Symmetrically, the *résiliation* decrement applies to
healthy only: lapsing a life in claim silently cancels a claim in payment.
:func:`result_cf` publishes :func:`pols_healthy` beside :func:`pols_if` for exactly this
reason — the difference between the two columns is the population whose premiums are
waived.

.. rubric:: Benefit in arrears, and the month a claim starts

A claim incepting at the end of month ``t`` seeds cohort ``z = 1`` and receives its first
payment at the end of month ``t + 1``. So :func:`pols_itt_stay` — the cohorts already in
payment at the start of the month that survived it — is what the benefit is paid on, and
new inceptions are excluded. A life in ITT throughout month ``t`` is paid for that month
whether it then stays, passes to IPT at the cap, or returns to healthy, and
:func:`claims` ``(t, "IPT")`` covers the lives that transitioned at end of month ``t``,
so the ITT to IPT move creates neither an unpaid month nor a doubled one.
:func:`check_benefit_split` asserts it.

.. rubric:: Two premium bases, two indemnity bases, two IPT benefit bases

All three are model point columns, not variants of the model.

``premium_basis``
    ``capital_initial`` is a level rate on the original capital; ``capital_restant_du``
    is a rate on the outstanding balance, re-read at each anniversary with the attained
    age. **The "decreasing" premium does not decrease**: on the anchor cell's life it
    rises from EUR 125.33 in year 1 to EUR 164.03 in year 10 before falling to EUR 31.65
    in year 20, because the attained-age rate climbs faster than the CRD falls.

``indemnity_basis``
    ``forfaitaire`` pays the *échéance* outright; ``indemnitaire`` caps it at the actual
    income loss through ``income_loss_ratio``. It is the **same formula** with
    :func:`indemnity_ratio` below 1, never a second benefit expression that could drift
    from the *forfaitaire* leg.

``ipt_benefit_basis``
    ``echeance`` keeps IPT as a state paying monthly; ``crd`` makes it a single payment
    of ``crd(t + 1) x quotite`` after which the life leaves the model, exactly as a death
    does — so on that basis :func:`pols_ipt_close` is zero throughout.

:func:`quotite` scales the benefit **and** the premium, once each. Applying it to the CRD
and again to the benefit is invisible at ``quotite = 1.00``, which is why model point 3
carries 0.60.

.. rubric:: Discounting, which the rest of the library does not do

Every other model in this library projects **undiscounted** gross liability cash flows
and leaves discounting to the layer that consumes them. This one also carries
:func:`disc_factor`, :func:`pv_premiums`, :func:`pv_claims` and :func:`pv_expenses`,
because the notes' Checks quote present values over the full 240 months. They are a
**companion**, not part of the cash flow projection: no line of :func:`result_cf` is
discounted, and ``disc_rate`` is the notes' flat 2.5 % **[std]**, not a valuation basis.
A Solvabilité II best estimate discounts these same cash flows on the EIOPA risk-free
term structure.
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
    return model_point()["policy_id"]


def age_at_entry():
    """The age at adhesion of the insured head.

    One insurer computes age by difference of calendar years and two set the rate by age
    at adhesion, so the annual step in :func:`age` is a pure convention **[std]**.
    """
    return int(model_point()["entry_age"])


def sex():
    """M or F.  Tariffs are sex-rated except where an insurer is deliberately unisex.

    Occupation class and smoker status are **not** model point attributes.  They are real
    tariff drivers, but no public French table is graded by them and no rate card was
    retrieved, so a column the shipped tables cannot serve would produce model points
    that do not project.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def capital_initial():
    """The original capital of the loan, in EUR."""
    return float(model_point()["capital_initial"])


def loan_rate_annual():
    """The loan's *taux nominal annuel*.

    A French loan quotes a nominal annual rate whose monthly rate is nominal / 12, **not**
    ``(1 + nominal)^(1/12) - 1``.  Using the effective conversion changes the *echeance*,
    and therefore every benefit - see :func:`loan_rate_mth`.
    """
    return float(model_point()["loan_rate_annual"])


def loan_rate_mth():
    """i: the monthly loan rate, ``loan_rate_annual / 12``.

    Nominal division, not an effective conversion.  This is the one place in the model
    where an annual rate is **not** converted with ``1 - (1 - r)^(1/12)``: that rule is
    for decrements, and a loan is not a decrement.
    """
    return loan_rate_annual() / 12.0


def loan_term_months():
    """T: the contractual term of the loan in months, over the sourced 1-35 year band."""
    return int(model_point()["loan_term_months"])


def quotite():
    """Q: the share of the loan this head insures, ``0 < quotite <= 1``.

    It scales the benefit **and** the premium, once each.  Applying it to the CRD and
    again to the benefit is invisible at 1.00, so model point 3 carries 0.60.
    """
    v = float(model_point()["quotite"])
    if not 0.0 < v <= 1.0:
        raise ValueError("invalid quotite")
    return v


def premium_basis():
    """``capital_initial`` (a level rate) or ``capital_restant_du`` (a rate on the CRD)."""
    v = model_point()["premium_basis"]
    if v not in ("capital_initial", "capital_restant_du"):
        raise ValueError("invalid premium_basis")
    return v


def premium_rate_annual():
    """The annual rate on the original capital, used on the ``capital_initial`` basis.

    0.84 % on the anchor cell **[std]**, calibrated so its present value matches the CRD
    scale over that cell.  On every other cell it is set so the margin on premium matches
    the anchor's 9.8 % **[std]**.  It is ignored on the CRD basis, where
    :func:`crd_rate` supplies the rate instead.
    """
    return float(model_point()["premium_rate_annual"])


def indemnity_basis():
    """``forfaitaire`` (the *echeance* outright) or ``indemnitaire`` (capped at income loss)."""
    v = model_point()["indemnity_basis"]
    if v not in ("forfaitaire", "indemnitaire"):
        raise ValueError("invalid indemnity_basis")
    return v


def income_loss_ratio():
    """The *indemnitaire* cap as a fraction of the *echeance*; used on that basis only.

    Modeling it properly needs a distribution of employer sick pay and *prevoyance* cover
    across the book, which nothing retrieved supplies, so it is a **[std]** lever the
    model exposes rather than a value it invents.  At 1.00 the *indemnitaire* cell equals
    the *forfaitaire* cell, which is the honest base.
    """
    return float(model_point()["income_loss_ratio"])


def indemnity_ratio():
    """IR: 1.0 on the *forfaitaire* basis, :func:`income_loss_ratio` otherwise.

    One ratio in one place, so *indemnitaire* is the same benefit formula with IR below 1
    and never a second expression that can drift from the *forfaitaire* leg.
    """
    return 1.0 if indemnity_basis() == "forfaitaire" else income_loss_ratio()


def franchise_days():
    """The *franchise* (deferred period) in days, over the sourced 30/60/90/120/180 menu.

    Not a state: the inception basis is a **claim payment** inception rate specific to
    the *franchise*, so a spell that recovers inside the *franchise* never leaves
    ``healthy`` and a life sick but not yet in payment keeps paying premiums.  The
    *franchise* enters through :func:`franchise_factor` and nowhere else.
    """
    v = int(model_point()["franchise_days"])
    if v not in [int(d) for d in data.franchise_table().index]:      # noqa: F821
        raise ValueError("invalid franchise_days")
    return v


def franchise_factor():
    """The multiplier on the inception rate for this *franchise*, from the table.

    1.60 / 1.25 / 1.00 / 0.85 / 0.65 for 30 / 60 / 90 / 120 / 180 days **[std]**; the
    inception table itself is written on the 90-day column, where the factor is 1.00.
    """
    return float(data.franchise_table().loc[                         # noqa: F821
        franchise_days(), "franchise_factor"])


def itt_max_days():
    """The contractual ITT duration cap in days; 1 095 across the sampled market."""
    return int(model_point()["itt_max_days"])


def itt_max_months():
    """The same cap in whole months, ``round(itt_max_days x 12 / 365.25)`` = 36.

    The number of ITT duration cohorts the model carries.  At this duration the surviving
    cohort is **assessed** against the 66 % *bareme croise* threshold rather than
    advanced - see :func:`pols_itt_cap`.
    """
    return int(round(itt_max_days() * 12.0 / 365.25))


def ipt_benefit_basis():
    """``echeance`` (IPT is a state paying monthly) or ``crd`` (a single capital).

    On the ``crd`` basis IPT is not a state at all: the mass that would enter it instead
    triggers one payment of ``crd(t + 1) x quotite`` and leaves the model, exactly as a death
    does, so :func:`pols_ipt_close` is zero throughout.
    """
    v = model_point()["ipt_benefit_basis"]
    if v not in ("echeance", "crd"):
        raise ValueError("invalid ipt_benefit_basis")
    return v


def deces_end_age():
    """The age at which the Décès guarantee ceases; 85 on the anchor cell."""
    return int(model_point()["deces_end_age"])


def ptia_end_age():
    """The age at which the PTIA guarantee ceases; 70 on the anchor cell."""
    return int(model_point()["ptia_end_age"])


def itt_ipt_end_age():
    """The age at which the ITT and IPT guarantees cease; 70 on the anchor cell.

    Lower than :func:`deces_end_age`, so a cover ends while the loan and the premium run
    on.  The published French claim-decline causes list "maximum cover age exceeded"
    among the commonest, which is this interaction seen from the claims register.
    """
    return int(model_point()["itt_ipt_end_age"])


def status():
    """``healthy``, ``itt`` or ``ipt``: the state the population starts in.

    An in-force portfolio needs all three - active lives, and claims already in payment
    carrying their claim duration as an attribute.  An ``itt`` or ``ipt`` cell run to the
    end of the loan is the disabled-life annuity a claims-in-payment reserve is quoted as,
    with the post-recovery active phase carried as well.
    """
    v = model_point()["status"]
    if v not in ("healthy", "itt", "ipt"):
        raise ValueError("invalid status")
    return v


def claim_duration_months():
    """z0: the claim duration already elapsed on an ``itt`` cell; 0 at inception.

    The seeded population enters cohort ``z0 + 1``, since cohort 1 is a claim that has
    just started paying.  Ignored on ``healthy`` and ``ipt`` cells.
    """
    return int(model_point()["claim_duration_months"])


def pols_if_init():
    """Initial number of policies; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_len():
    """The number of months projected: the loan's contractual term.

    The **exclusive end** of the frame, counted from ``t = 0``: the projection runs
    ``t = 0 ... proj_len() - 1``, which is lifelib's ``for t in range(proj_len())``, and
    ``proj_len()`` is also the time point of the last instalment, where ``crd`` is zero.
    All cover and any claim in payment terminate at the loan's expiry with no value, so
    there is nothing after it.  This is what truncates the IPT annuity, which otherwise
    would have no natural end.
    """
    return loan_term_months()


def duration(t):
    """Completed policy years at the start of month t: ``t // 12``.

    0-based, as ``duration`` is throughout lifelib: 0 through the first policy year.
    """
    return t // 12


def duration_mth(t):
    """Months elapsed from the start of the projection at the start of month t; equal to t.

    ``t`` is 0-based and counts from adhesion, so the identity is trivial - the cells
    exists so the monthly models in this library share one vocabulary.
    """
    return t


def policy_year(t):
    """y: the contractual policy year containing month t; 1 for t = 0..11.

    The 1-based label ``duration(t) + 1``, derived from the 0-based ``t`` and never
    indexed by.  It is what the *résiliation* table and the expense inflation are read on.
    """
    return duration(t) + 1


def age(t):
    """a: the attained age in the policy year containing month t.

    ``entry_age + floor(t / 12)``.  The annual step is a **[std]** convention: one
    sampled insurer computes age by difference of calendar years instead.
    """
    return age_at_entry() + duration(t)


# -- The loan spine ----------------------------------------------------------

def echeance():
    """The level monthly instalment, capital and interest.

    ``capital_initial x i / (1 - (1 + i)^(-T))``.  Computed, never read from a table: the
    whole product hangs off the *capital restant du*, and a pasted schedule cannot be
    checked.  EUR 1 109.1952 on the anchor cell.
    """
    i = loan_rate_mth()
    return capital_initial() * i / (1.0 - (1.0 + i) ** (-loan_term_months()))


def crd(k):
    """The *capital restant du* at **time k**: the balance after the k-th instalment.

    A time-point cells, not a month-index one, and already 0-based: ``k = 0`` is
    adhesion, so ``crd(0) = capital_initial``, and ``crd(T) = 0`` exactly at the last
    instalment.  ``ech x (1 - (1 + i)^(-(T - k))) / i``.  This is the sum insured for
    Décès and PTIA and the only thing linking the loan to the insurance.  Month ``t``
    **opens** on ``crd(t)`` and **closes** on ``crd(t + 1)``, the two differing by that
    month's capital repayment - EUR 609.20 over the first month on the anchor cell - and
    the benefit is written on the closing balance ``crd(t + 1)``; whichever convention is
    chosen must be used everywhere.  :func:`check_crd` asserts the schedule against its
    own roll-forward.
    """
    if k <= 0:
        return capital_initial()
    if k >= loan_term_months():
        return 0.0
    i = loan_rate_mth()
    return echeance() * (1.0 - (1.0 + i) ** (-(loan_term_months() - k))) / i


def loan_interest_total():
    """Total interest over the loan: ``T x ech - capital_initial``.

    EUR 66 206.85 on the anchor cell, against EUR 266 206.85 of instalments.  Nothing in
    the projection consumes it; it is the reader's check that the spine is the loan they
    think it is.
    """
    return loan_term_months() * echeance() - capital_initial()


def cover_deces(t):
    """D(t): 1 while the Décès guarantee is in force in month t, 0 after.

    ``age(t) < deces_end_age()``.  Separate from :func:`cover_ptia` because the two ages
    differ, even though the two guarantees pay the identical capital.
    """
    return 1 if age(t) < deces_end_age() else 0


def cover_ptia(t):
    """P(t): 1 while the PTIA guarantee is in force in month t, 0 after.

    Above :func:`ptia_end_age` the PTIA decrement switches off while Décès continues -
    which is the whole reason the two are modelled as separate decrements.
    """
    return 1 if age(t) < ptia_end_age() else 0


def cover_itt(t):
    """I(t): 1 while the ITT and IPT guarantees are in force in month t, 0 after.

    At the first month where this is 0, all ITT and IPT mass moves into ``healthy`` at the
    beginning of the month and before any transition, inception stops, and the benefit
    stops - but the lives remain alive, death covered and premium paying.  See
    :func:`pols_itt_transfer`.
    """
    return 1 if age(t) < itt_ipt_end_age() else 0


# -- Decrement rates ---------------------------------------------------------

def mort_rate(t):
    """The **healthy-life** annual mortality rate at the attained age.

    Read from ``mort_table.csv`` at the policy's sex, **linearly** interpolated between
    pivot ages and held flat outside them.  A **[std]** proxy: the homologated French
    tables for a non-annuity contract are TH 00-02 / TF 00-02 with the annexed *decalage
    d'age*, which are not redistributable, so the shipped values are shaped from INSEE
    population data.  Mortality in claim is :func:`itt_mort_rate` and mortality in IPT is
    :func:`mort_rate_ipt`; reading either out of this cells is the mistake the naming is
    there to prevent.
    """
    sub = data.mort_table().loc[sex()]                               # noqa: F821
    ages = sorted(int(a) for a in sub.index)
    x = age(t)
    if x <= ages[0]:
        return float(sub.loc[ages[0], "mort_rate"])
    if x >= ages[-1]:
        return float(sub.loc[ages[-1], "mort_rate"])
    lo = max(a for a in ages if a <= x)
    hi = min(a for a in ages if a > x)
    r_lo = float(sub.loc[lo, "mort_rate"])
    r_hi = float(sub.loc[hi, "mort_rate"])
    return r_lo + (r_hi - r_lo) * (x - lo) / (hi - lo)


def mort_rate_mth(t):
    """q_h = 1 - (1 - mort_rate)^(1/12): the monthly healthy-life mortality **[std]**.

    The uniform-force conversion used for every decrement in this model.  It makes each
    monthly rate strictly below its annual rate and keeps the twelve monthly survival
    factors multiplying back to the annual one.  No retrieved source states a conversion
    convention for any French decrement.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def ptia_rate(t):
    """The annual PTIA incidence rate: ``ptia_ratio x mort_rate``.

    **No public French PTIA incidence rate exists.**  PTIA pays the same capital as Décès
    and is a subset of severe morbidity, so it is carried as a fixed fraction of the death
    rate **[std]**.  The ratio matters mainly through the different cover-end ages.
    """
    return ptia_ratio * mort_rate(t)                                 # noqa: F821


def ptia_rate_mth(t):
    """q_ptia = 1 - (1 - ptia_rate)^(1/12): the monthly PTIA incidence **[std]**."""
    return 1.0 - (1.0 - ptia_rate(t)) ** (1.0 / 12.0)


def itt_inception_rate(t):
    """The annual ITT **claim payment** inception rate out of ``healthy``.

    Read from ``itt_inception_table.csv`` at the policy's sex, linearly interpolated
    between pivot ages and held flat outside them, then scaled by
    :func:`franchise_factor` and by the anti-selection lever ``selection_load``.

    It is a claim *payment* inception rate specific to the *franchise* - which is what a
    real disability basis publishes per deferred period - so the *franchise* needs no
    state of its own.  Every value is **[std]**: nothing in the retrieved corpus gives a
    French ITT inception rate.
    """
    sub = data.itt_inception_table().loc[sex()]                      # noqa: F821
    ages = sorted(int(a) for a in sub.index)
    x = age(t)
    if x <= ages[0]:
        r = float(sub.loc[ages[0], "itt_inception_rate"])
    elif x >= ages[-1]:
        r = float(sub.loc[ages[-1], "itt_inception_rate"])
    else:
        lo = max(a for a in ages if a <= x)
        hi = min(a for a in ages if a > x)
        r_lo = float(sub.loc[lo, "itt_inception_rate"])
        r_hi = float(sub.loc[hi, "itt_inception_rate"])
        r = r_lo + (r_hi - r_lo) * (x - lo) / (hi - lo)
    return r * franchise_factor() * (1.0 + selection_load)           # noqa: F821


def itt_inception_rate_mth(t):
    """iota = 1 - (1 - itt_inception_rate)^(1/12): the monthly inception rate **[std]**.

    The rate itself, before the guarantee indicator.  The notes' ``i_rate = iota x I(t)``
    is applied in :func:`pols_itt_inception`, so this cells stays a pure basis rate.
    """
    return 1.0 - (1.0 - itt_inception_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """The table annual *résiliation* rate in month t, before any substitution uplift.

    4 % in year 1, 12 % in years 2 and 3, 10 %, then a 7 % ultimate; policy years beyond
    the table take its last row.  Materially higher than a classic protection lapse
    because the cover does not stop, it moves.  The whole table is **[std]**: the
    published French series are counts of substitution *requests*, not lapse rates.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = policy_year(t)
    return float(tbl.loc[min(y, int(tbl.index.max())), "lapse_rate"])


def market_prem_pp(t):
    """The price of an equivalent contract in the substitution market **[std]**.

    ``market_prem_ratio x prem_pp(t)``, so the base run has the book priced at the market
    and :func:`prem_gap` is zero.  It is a scenario input rather than a projection: the
    published French tariff series show bank group prices falling 14 %-30 % across the age
    range over four years while medically-selected alternatives moved between -40 % and
    +16 %, so a book written at an older tariff faces a two-digit gap without doing
    anything, and this is the lever that expresses it.
    """
    return market_prem_ratio * prem_pp(t)                            # noqa: F821


def prem_gap(t):
    """gap(y) = max(0, prem_pp / market_prem_pp - 1): the premium gap driving substitution.

    Zero in the base run.  Only a *positive* gap matters - a borrower paying less than the
    market has no reason to move.
    """
    m = market_prem_pp(t)
    if m <= 0.0:
        return 0.0
    return max(0.0, prem_pp(t) / m - 1.0)


def lapse_rate(t):
    """w_a(y): the **annual** *résiliation* rate out of ``healthy`` in month t.

    ``min(lapse_rate_max, lapse_rate_base x (1 + lapse_beta x subst_acceptance x gap))``.
    The dynamic uplift is a **[std]** construction, not a calibration, and it is off in
    the base run because :func:`prem_gap` is zero there.  ``subst_acceptance`` multiplies
    the **uplift** rather than the whole rate: lenders accept 88 %-90 % of substitution
    requests through banking networks, and refused requests remain in force, so only the
    substitution-driven increment is exposed to acceptance.

    Applied to ``healthy`` only.  Lives in ITT or IPT never lapse **[std]**: their
    premiums are waived and the benefit is in payment.
    """
    uplift = 1.0 + lapse_beta * subst_acceptance * prem_gap(t)       # noqa: F821
    return min(lapse_rate_max, lapse_rate_base(t) * uplift)          # noqa: F821


def lapse_rate_mth(t):
    """w = 1 - (1 - lapse_rate)^(1/12): the monthly *résiliation* rate **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def claim_dur_year(z):
    """The claim duration year containing claim month z: ``(z - 1) // 12 + 1``.

    Duration years beyond the termination table take its last row, which is the shipped
    table's third year - the year the 1 095-day cap falls in.
    """
    tbl = data.itt_termination_table()                               # noqa: F821
    return min((z - 1) // 12 + 1, int(tbl.index.max()))


def itt_recovery_rate(z):
    """rho_a(z): the annual recovery rate out of ITT at claim duration z months.

    0.55 / 0.30 / 0.15 by duration year **[std]**.  Short claims mostly recover and long
    claims mostly consolidate; the declining gradient is why the in-claim population needs
    a duration dimension at all.
    """
    return float(data.itt_termination_table().loc[                   # noqa: F821
        claim_dur_year(z), "itt_recovery_rate"])


def itt_recovery_rate_mth(z):
    """rho(z) = 1 - (1 - rho_a)^(1/12): the monthly recovery rate **[std]**."""
    return 1.0 - (1.0 - itt_recovery_rate(z)) ** (1.0 / 12.0)


def itt_to_ipt_rate(z):
    """tau_a(z): the annual ITT to IPT transition rate at claim duration z months.

    0.02 / 0.06 / 0.12 by duration year **[std]**, rising as recovery falls: the longer a
    claim runs the likelier the medical assessment clears the 66 % *bareme croise*
    threshold.
    """
    return float(data.itt_termination_table().loc[                   # noqa: F821
        claim_dur_year(z), "itt_to_ipt_rate"])


def itt_to_ipt_rate_mth(z):
    """tau(z) = 1 - (1 - tau_a)^(1/12): the monthly IPT transition rate **[std]**."""
    return 1.0 - (1.0 - itt_to_ipt_rate(z)) ** (1.0 / 12.0)


def itt_mort_rate(z):
    """q_s_a(z): the annual mortality of a life in ITT at claim duration z months.

    0.02 / 0.03 / 0.04 by duration year **[std]**.  Claimant mortality above healthy-life
    mortality is universal in disability experience; these values have no French anchor.
    """
    return float(data.itt_termination_table().loc[                   # noqa: F821
        claim_dur_year(z), "itt_mort_rate"])


def itt_mort_rate_mth(z):
    """q_s(z) = 1 - (1 - q_s_a)^(1/12): the monthly death-in-ITT rate **[std]**."""
    return 1.0 - (1.0 - itt_mort_rate(z)) ** (1.0 / 12.0)


def itt_surv_step(z):
    """s_itt(z) = (1 - rho)(1 - tau)(1 - q_s): monthly ITT persistency at duration z.

    Recovery first, then transition to IPT among the non-recovered, then death among the
    rest - the notes' processing order out of ITT **[std]**.
    """
    return ((1.0 - itt_recovery_rate_mth(z))
            * (1.0 - itt_to_ipt_rate_mth(z))
            * (1.0 - itt_mort_rate_mth(z)))


def itt_rate_vectors():
    """The four per-duration rate vectors, ``(rho, tau, q_s, s_itt)``, built once.

    Element ``z - 1`` of each list is the value at claim duration ``z``, for
    ``z = 1 ... itt_max_months()``.  Purely a performance shape: the exit cells walk the
    whole cohort vector in every projected month, and reading the rates out of a list
    rather than calling the scalar cells per element turns ``proj_len() x
    itt_max_months()`` lookups into ``itt_max_months()`` of them.  The scalar cells stay,
    because they are what a reader looks up and what a test asserts against; this is
    built *from* them, so there is still one definition of each rate.
    """
    zs = range(1, itt_max_months() + 1)
    rho = [itt_recovery_rate_mth(z) for z in zs]
    tau = [itt_to_ipt_rate_mth(z) for z in zs]
    qs = [itt_mort_rate_mth(z) for z in zs]
    surv = [(1.0 - r) * (1.0 - x) * (1.0 - d) for r, x, d in zip(rho, tau, qs)]
    return rho, tau, qs, surv


def itt_surv(z):
    """S(z): the probability a claim incepting at duration 0 is still in ITT at month z.

    The survival column of the disabled-life annuity, and the notes' supplementary table:
    0.932478 at ``z = 1``, 0.432180 at 12, 0.275843 at 24 and 0.198077 at the 36-month
    cap, where 35 % of it consolidates into IPT.
    """
    if z <= 0:
        return 1.0
    return itt_surv(z - 1) * itt_surv_step(z)


def itt_annuity_months():
    """The expected number of months of ITT benefit per inception, ``sum of S(z)``.

    14.721231 on the anchor cell's basis.  A companion to the projection rather than part
    of it: it is the object a claims-in-payment reserve for a fresh ITT claim is quoted
    as, before the cap assessment feeds IPT.
    """
    return sum(itt_surv(z) for z in range(1, itt_max_months() + 1))


def itt_benefit_per_inception():
    """The expected ITT benefit per inception: ``benefit_itt_pp x itt_annuity_months``.

    EUR 16 328.72 on the anchor cell.  It excludes everything that follows the cap - the
    IPT annuity the 35 % share buys is a separate and much larger liability.
    """
    return benefit_itt_pp() * itt_annuity_months()


def mort_rate_ipt(t):
    """The annual mortality of a life in IPT: ``ipt_mort_factor x mort_rate``, capped at 1.

    A third mortality rate, on the policy-month clock rather than the claim-duration one.
    The x3.0 factor is **[std]** and has no French anchor.
    """
    return min(1.0, ipt_mort_factor * mort_rate(t))                  # noqa: F821


def mort_rate_ipt_mth(t):
    """q_ipt = 1 - (1 - mort_rate_ipt)^(1/12): the monthly IPT mortality **[std]**."""
    return 1.0 - (1.0 - mort_rate_ipt(t)) ** (1.0 / 12.0)


# -- Premium -----------------------------------------------------------------

def crd_rate(t):
    """The annual premium rate on the CRD at the attained age, from ``crd_rate_table.csv``.

    Linearly interpolated between pivot ages and **held flat** outside them - so a life
    past the last pivot keeps the last rate rather than extrapolating into an
    unsupported one.  Used only when ``premium_basis = capital_restant_du``.  A tariff,
    not a decrement, and **[std]**: calibrated so its present value over the anchor cell
    matches the level 0.84 % scale to about 0.11 %.
    """
    tbl = data.crd_rate_table()                                      # noqa: F821
    ages = sorted(int(a) for a in tbl.index)
    x = age(t)
    if x <= ages[0]:
        return float(tbl.loc[ages[0], "crd_rate"])
    if x >= ages[-1]:
        return float(tbl.loc[ages[-1], "crd_rate"])
    lo = max(a for a in ages if a <= x)
    hi = min(a for a in ages if a > x)
    r_lo = float(tbl.loc[lo, "crd_rate"])
    r_hi = float(tbl.loc[hi, "crd_rate"])
    return r_lo + (r_hi - r_lo) * (x - lo) / (hi - lo)


def prem_pp(t):
    """The monthly premium per policy in force in the policy year containing month t.

    ``capital_initial``
        ``capital_initial x Q x premium_rate_annual / 12``, level for the whole term.

    ``capital_restant_du``
        ``crd(12 (y - 1)) x Q x crd_rate(a) / 12``, re-read at each policy anniversary
        on the CRD **at the anniversary**, not at the month.

    The premium is *nivelé* and does **not** fall when the PTIA or ITT/IPT guarantees
    cease.  And the "decreasing" premium does not decrease: on the anchor cell's life the
    CRD basis rises from EUR 125.33 in year 1 to EUR 164.03 in year 10 before falling to
    EUR 31.65 in year 20, because the attained-age rate climbs faster than the CRD falls.
    """
    if premium_basis() == "capital_initial":
        return capital_initial() * quotite() * premium_rate_annual() / 12.0
    return crd(12 * (policy_year(t) - 1)) * quotite() * crd_rate(t) / 12.0


def premiums(t):
    """Premium income at the beginning of month t, an inflow.

    Carried on :func:`pols_healthy` and **never** on :func:`pols_if`.  Premiums are waived
    in claim, so projecting income from lives in ITT or IPT overstates it by the whole
    in-claim population - and it is easy to write by accident in a model that also tracks
    total lives in force.
    """
    return prem_pp(t) * pols_healthy(t)


# -- The four-state population -----------------------------------------------

def itt_cohorts_raw(t):
    """l_itt(t, .) as a list, **before** any cover-cessation transfer.

    Element ``z - 1`` is the population in ITT payment at the start of month t with claim
    duration ``z`` months, for ``z = 1 ... itt_max_months()``.  At ``t = 0`` it is the
    seeded state: all zeros except on an ``itt`` cell, where ``pols_if_init()`` sits in
    cohort ``claim_duration_months() + 1``.  Thereafter cohort 1 is the previous month's
    inceptions and every other cohort is the previous cohort survived one month - the
    cohort at ``itt_max_months()`` is **not** carried forward, because it is assessed at
    the cap instead.

    Defined one step past the last projected month, at ``t = proj_len()``, so
    :func:`pols_itt_close` can read the closing state of the last month out of the same
    recursion that produces every other month.  A new list is built on each step rather
    than the previous one mutated, so a month already computed is never rewritten by a
    later one.
    """
    n = itt_max_months()
    if t < 0 or t > proj_len():
        return [0.0] * n
    if t == 0:
        if status() != "itt":
            return [0.0] * n
        seed = min(claim_duration_months(), n - 1)
        return [pols_if_init() if z == seed else 0.0 for z in range(n)]
    prev = itt_cohorts(t - 1)
    surv = itt_rate_vectors()[3]
    out = [pols_itt_inception(t - 1)]
    for z in range(1, n):
        out.append(prev[z - 1] * surv[z - 1])
    return out


def itt_cohorts(t):
    """l_itt(t, .) as a list, **after** the cover-cessation transfer.

    Identical to :func:`itt_cohorts_raw` while the ITT/IPT cover is in force, and all
    zeros once it has ceased - the mass has moved into ``healthy``, and
    :func:`pols_itt_transfer` is that movement.  This is the vector every ITT exit and the
    ITT benefit are computed on, so the benefit is exactly zero from the cover-end month
    without any further gating.
    """
    n = itt_max_months()
    if t < 0 or t >= proj_len() or not cover_itt(t):
        return [0.0] * n
    return itt_cohorts_raw(t)


def pols_itt_dur(t, z):
    """l_itt(t, z): the population in ITT at the start of month t at claim duration z.

    A named lookup into :func:`itt_cohorts`, so the notes' two-dimensional object is
    addressable by name without the model carrying ``proj_len() x itt_max_months()``
    separate cells.  Out of range returns 0.0 rather than raising.
    """
    v = itt_cohorts(t)
    return v[z - 1] if 1 <= z <= len(v) else 0.0


def pols_itt(t):
    """l_itt(t): the total population in ITT payment at the start of month t."""
    return sum(itt_cohorts(t))


def pols_itt_transfer(t):
    """The ITT mass moved into ``healthy`` at the beginning of month t, at cover end.

    Non-zero only in the first month where :func:`cover_itt` is 0 and a claim is still in
    payment: EUR-free, 0.009266 of a policy on the anchor cell at ``t = 216``.  The mass
    is **moved**, not deleted - those lives are alive, still death covered and still
    premium paying, and deleting them would break :func:`check_states` and destroy cover
    they still hold.
    """
    if t < 0 or t >= proj_len() or cover_itt(t):
        return 0.0
    return sum(itt_cohorts_raw(t))


def pols_ipt_raw(t):
    """l_ipt(t) **before** any cover-cessation transfer.

    Defined one step past the last projected month for the same reason as
    :func:`itt_cohorts_raw`.  Seeded with ``pols_if_init()`` on an ``ipt`` cell.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init() if status() == "ipt" else 0.0
    return pols_ipt_close(t - 1)


def pols_ipt(t):
    """l_ipt(t): the population in IPT payment at the start of month t.

    Zero once the ITT/IPT cover has ceased, and zero throughout on the ``crd`` IPT
    benefit basis, where IPT is not a state at all.
    """
    if t < 0 or t >= proj_len() or not cover_itt(t):
        return 0.0
    return pols_ipt_raw(t)


def pols_ipt_transfer(t):
    """The IPT mass moved into ``healthy`` at the beginning of month t, at cover end.

    0.013982 of a policy on the anchor cell at ``t = 216``.  An IPT annuitant whose
    guarantee has expired is not dead and has not lapsed: the annuity stops and the life
    resumes paying for the death cover it still holds.
    """
    if t < 0 or t >= proj_len() or cover_itt(t):
        return 0.0
    return pols_ipt_raw(t)


def pols_healthy(t):
    """l_h(t): the population in ``healthy`` at the start of month t.

    ``pols_if_init()`` at ``t = 0`` on a ``healthy`` cell and zero on an in-claim one,
    then the previous month's closing healthy population plus anything the cover-cessation
    transfer moved in.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t == 0:
        return pols_if_init() if status() == "healthy" else 0.0
    return (pols_healthy_close(t - 1)
            + pols_itt_transfer(t) + pols_ipt_transfer(t))


def pols_death_healthy(t):
    """dth_h(t): deaths out of ``healthy`` at the end of month t.

    The notes' processing order out of ``healthy`` is **death, then PTIA, then
    *résiliation*, then ITT inception** among the survivors of each **[std]**.  The
    ordering is visible in the arithmetic: on the anchor cell
    ``claims(0, "PTIA") / claims(0, "DEATH")`` is 0.0998 rather than the ``ptia_ratio`` of
    0.10, the difference being the month of death exposure that precedes PTIA.
    """
    return pols_healthy(t) * mort_rate_mth(t)


def pols_ptia(t):
    """ptia_h(t): PTIA claims out of ``healthy`` at the end of month t.

    Taken from the survivors of mortality, and **zero once :func:`cover_ptia` is 0** while
    the death decrement continues.  PTIA is an acceleration of the same capital, never
    an addition to it: a life claiming PTIA leaves the model and cannot also die.
    """
    return pols_healthy(t) * (1.0 - mort_rate_mth(t)) * ptia_rate_mth(t) * cover_ptia(t)


def pols_lapse(t):
    """lapses(t): *résiliations* out of ``healthy`` at the end of month t.

    Taken from the survivors of mortality and PTIA.  Pays nothing: this contract has no
    surrender value at any time.  Applied to ``healthy`` only - applying it to ITT or IPT
    would silently cancel claims in payment.
    """
    return (pols_healthy(t) * (1.0 - mort_rate_mth(t))
            * (1.0 - ptia_rate_mth(t) * cover_ptia(t)) * lapse_rate_mth(t))


def pols_itt_inception(t):
    """n_itt(t): new ITT claim-payment inceptions at the end of month t, seeding z = 1.

    Taken from the survivors of mortality, PTIA and *résiliation*, and gated by
    :func:`cover_itt` - the notes' ``i_rate = iota x I(t)``.  Each inception starts a new
    duration cohort and is **not** paid until the end of the following month.
    """
    return (pols_healthy(t) * (1.0 - mort_rate_mth(t))
            * (1.0 - ptia_rate_mth(t) * cover_ptia(t))
            * (1.0 - lapse_rate_mth(t))
            * itt_inception_rate_mth(t) * cover_itt(t))


def pols_healthy_stay(t):
    """h_stay(t): the population staying in ``healthy`` through month t.

    The opening population less the four exits, so the five add back to it exactly.
    """
    return (pols_healthy(t) - pols_death_healthy(t) - pols_ptia(t)
            - pols_lapse(t) - pols_itt_inception(t))


def pols_itt_recovery(t):
    """rec_itt(t): recoveries out of ITT at the end of month t, back to ``healthy``.

    ``sum over z of l_itt(t, z) rho(z)``.  Recovered lives re-enter ``healthy`` and are
    again exposed to inception **[std]**.  A same-cause recurrence would contractually
    restart payment with no new *franchise*; returning them to the standard inception
    basis ignores that and understates re-inception at short horizons.
    """
    v = itt_cohorts(t)
    rho = itt_rate_vectors()[0]
    return sum(a * r for a, r in zip(v, rho) if a != 0.0)


def pols_itt_to_ipt(t):
    """trn_ipt(t): ITT claims consolidating into IPT at the end of month t.

    ``sum over z of l_itt(t, z) (1 - rho(z)) tau(z)`` - recovery first, then transition
    among the non-recovered.  These lives are paid for month t as ITT and enter IPT at the
    end of it, so the move creates neither an unpaid month nor a doubled one.
    """
    v = itt_cohorts(t)
    rho, tau, _, _ = itt_rate_vectors()
    return sum(a * (1.0 - r) * x for a, r, x in zip(v, rho, tau) if a != 0.0)


def pols_itt_death(t):
    """dth_itt(t): deaths in ITT at the end of month t.

    ``sum over z of l_itt(t, z) (1 - rho)(1 - tau) q_s``, the last of the three
    competing exits.  They carry the Décès benefit like any other death.
    """
    v = itt_cohorts(t)
    rho, tau, qs, _ = itt_rate_vectors()
    return sum(a * (1.0 - r) * (1.0 - x) * d
               for a, r, x, d in zip(v, rho, tau, qs) if a != 0.0)


def pols_itt_stay(t):
    """The ITT mass that was in payment throughout month t: ``sum over z of l_itt s_itt``.

    What the ITT benefit is paid on.  It includes the cohort reaching the cap - a life in
    ITT throughout the month is paid for it whether it then stays, consolidates or returns
    to ``healthy`` - and excludes the month's own inceptions, which are not paid until the
    following month.
    """
    v = itt_cohorts(t)
    surv = itt_rate_vectors()[3]
    return sum(a * b for a, b in zip(v, surv) if a != 0.0)


def pols_itt_cap(t):
    """cap_itt(t): the ITT mass reaching the 1 095-day assessment at the end of month t.

    The cohort at ``itt_max_months()`` that survived the month.  It is **assessed**, not
    advanced: :func:`pols_cap_to_ipt` of it clears the 66 % *bareme croise* threshold and
    :func:`pols_cap_return` goes back to ``healthy``.  Letting it advance to a
    thirty-seventh cohort would run ITT claims for ever and starve IPT of the feed that
    dominates its liability.
    """
    n = itt_max_months()
    return pols_itt_dur(t, n) * itt_surv_step(n)


def pols_cap_to_ipt(t):
    """The share of the capped cohort assessed into IPT: ``ipt_share_at_cap x cap_itt``.

    0.35 **[std]**.  It stands in for the medical assessment against the 66 % threshold,
    and nothing public quantifies what fraction of three-year ITT claims clears it.  The
    liability is roughly linear in this number, because it converts a bounded three-year
    claim into an annuity that can run to the end of the loan.
    """
    return ipt_share_at_cap * pols_itt_cap(t)                        # noqa: F821


def pols_cap_return(t):
    """The share of the capped cohort returning to ``healthy``: ``(1 - share) x cap_itt``.

    0.65 **[std]**.  These lives are paid their ITT benefit for the month of the
    assessment and then resume paying premiums, which is why
    :func:`check_benefit_split` carries this term.
    """
    return (1.0 - ipt_share_at_cap) * pols_itt_cap(t)                # noqa: F821


def pols_ipt_entry(t):
    """All entrants to IPT at the end of month t: the transitions plus the cap share.

    On the ``crd`` IPT basis these lives do not enter a state at all - they take a single
    payment of ``crd(t + 1) x quotite`` and leave, which is :func:`pols_ipt_capital`.
    """
    return pols_itt_to_ipt(t) + pols_cap_to_ipt(t)


def pols_ipt_death(t):
    """dth_ipt(t): deaths in IPT at the end of month t.

    The only exit from IPT other than the guarantee's age limit - **there is no recovery
    from IPT**, which is what lets the IPT annuity run to the end of the loan while the
    ITT one is capped at three years.
    """
    return pols_ipt(t) * mort_rate_ipt_mth(t)


def pols_ipt_stay(t):
    """ipt_stay(t): the IPT population surviving month t."""
    return pols_ipt(t) - pols_ipt_death(t)


def pols_ipt_capital(t):
    """The mass leaving the model with an IPT capital, on the ``crd`` basis; else zero.

    On that basis IPT is not a state: the entrants take ``crd(t + 1) x quotite`` once and are
    gone, exactly as a death is.  The cells exists so that :func:`check_states` closes on
    both bases without a special case.
    """
    return pols_ipt_entry(t) if ipt_benefit_basis() == "crd" else 0.0


def pols_healthy_close(t):
    """l_h(t + 1): the population in ``healthy`` at the **end** of month t.

    Those staying, plus the month's recoveries, plus the share of the capped cohort sent
    back.  This is the notes' own ``l_h(t + 1)``, the state at time ``t + 1`` - 0.995344
    at ``t = 0`` on the anchor cell - and it is :func:`pols_healthy` ``(t + 1)`` less
    anything the cover-cessation transfer moves in at the start of the next month.
    """
    return pols_healthy_stay(t) + pols_itt_recovery(t) + pols_cap_return(t)


def pols_itt_close(t):
    """l_itt(t + 1): the total population in ITT at the **end** of month t.

    Read out of :func:`itt_cohorts_raw` ``(t + 1)`` - the *next* month's un-transferred
    opening vector - so it travels through the cohort recursion rather than repeating its
    arithmetic.  That is what makes :func:`check_benefit_split` a real check rather than
    an identity: a mis-indexed duration shift moves this number and not the benefit.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    return sum(itt_cohorts_raw(t + 1))


def pols_ipt_close(t):
    """l_ipt(t + 1): the population in IPT at the **end** of month t.

    The survivors plus the month's entrants.  Zero throughout on the ``crd`` IPT basis.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if ipt_benefit_basis() == "crd":
        return 0.0
    return pols_ipt_stay(t) + pols_ipt_entry(t)


def pols_if(t):
    """The number of policies in force at the start of month t: healthy + ITT + IPT.

    The weight on the maintenance expense, and the count a reader of :func:`result_cf`
    reconciles the rest of the row against.  It is **not** the weight on premium income,
    which comes from :func:`pols_healthy` alone because premiums are waived in claim.
    """
    return pols_healthy(t) + pols_itt(t) + pols_ipt(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside month t.

    ``"BEF_DECR"``
        the start of the month, before any transition; the same number as
        :func:`pols_if`.

    ``"AFT_DECR"``
        the end of the month, once deaths, PTIA claims, *résiliations* and
        any IPT capital have been taken.  Equal to ``pols_if(t + 1)``
        everywhere but the last month, where it is zero.

    The intermediate points of the other models have no single-population meaning here,
    because four states are moving at once; the ``pols_*`` cells expose them instead.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DECR":
        if t < 0 or t >= proj_len() - 1:
            return 0.0
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_exit(t):
    """The population leaving the model altogether at the end of month t.

    Deaths from all three states, PTIA claims, *résiliations*, and - on the ``crd`` IPT
    basis - the lives that took an IPT capital.  Inceptions, recoveries, IPT transitions
    and the cover-cessation transfer are **moves between states** and are absent, which
    is the point of running the identity on the whole policy count.
    """
    return (pols_death_healthy(t) + pols_ptia(t) + pols_lapse(t)
            + pols_itt_death(t) + pols_ipt_death(t) + pols_ipt_capital(t))


def pols_exit_cum(t):
    """Cumulative exits from the model before the start of month t; zero at t = 0."""
    if t <= 0:
        return 0.0
    return pols_exit_cum(t - 1) + pols_exit(t - 1)


def pols_maturity(t):
    """The population still in force when the loan reaches its contractual expiry.

    Non-zero only in the last projected month, where all cover **and any claim in
    payment** terminate without value.  Not a decrement and not a benefit - but without
    it the last month appears to lose lives with no cause and
    :func:`check_pols_roll_fwd` would not close.
    """
    if t != proj_len() - 1:
        return 0.0
    return pols_healthy_close(t) + pols_itt_close(t) + pols_ipt_close(t)


# -- Benefits, expenses and net cash flow ------------------------------------

def benefit_deces_pp(t):
    """The Décès and PTIA capital per policy in month t: ``crd(t + 1) x quotite``.

    The benefit falls at the **end** of month t, so it is written on that month's closing
    balance ``crd(t + 1)`` - the instalment falling on the day of death being deemed due.
    One expression for both guarantees, because they pay the identical amount - what
    separates them is :func:`cover_deces` against :func:`cover_ptia`, not the benefit.
    """
    return crd(t + 1) * quotite()


def benefit_itt_pp():
    """The monthly ITT and IPT amount per policy: ``ech x Q x IR x claim_admission``.

    Level for the whole term, because the *échéance* it replaces is.  ``claim_admission``
    is 1.00 in the base run **[std]**: the model has no way to distinguish an admitted
    claim from a declined one, the only public French figures being portfolio decline
    rates by guarantee and contract type with no split between late notice, cover-age
    breach and medical dispute.  A portfolio calibration sets it from its own register.
    """
    return echeance() * quotite() * indemnity_ratio() * claim_admission  # noqa: F821


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"DEATH"``
        ``crd(t + 1) x Q`` on deaths from **all three states**, while
        :func:`cover_deces` holds.  A life dying in ITT or IPT is still a
        death claim.

    ``"PTIA"``
        ``crd(t + 1) x Q`` on PTIA claims out of ``healthy``.  The same
        capital as death, on a decrement that switches off fifteen years
        earlier.

    ``"ITT"``
        ``ech x Q x IR`` on the mass in payment throughout the month,
        monthly in arrears.

    ``"IPT"``
        on the ``echeance`` basis, ``ech x Q x IR`` on the IPT survivors
        **plus the month's ITT to IPT transitions** - so a life moving at
        the end of month t is paid exactly once for it.  On the ``crd``
        basis, ``crd(t + 1) x Q`` once on every entrant, after which they
        leave.

    ``"LAPSE"``, ``"MATURITY"``
        zero.  There is **no surrender value** at any time and **no
        maturity benefit**: *résiliation* and expiry both end the cover
        without payment.

    The two zero kinds are published rather than omitted so that the product facts are
    stated instead of inferred from a missing column.
    """
    if kind is None:
        return sum(claims(t, k) for k in
                   ("DEATH", "PTIA", "ITT", "IPT", "LAPSE", "MATURITY"))
    if kind == "DEATH":
        deaths = pols_death_healthy(t) + pols_itt_death(t) + pols_ipt_death(t)
        return benefit_deces_pp(t) * deaths * cover_deces(t)
    if kind == "PTIA":
        return benefit_deces_pp(t) * pols_ptia(t)
    if kind == "ITT":
        return benefit_itt_pp() * pols_itt_stay(t)
    if kind == "IPT":
        if ipt_benefit_basis() == "echeance":
            return benefit_itt_pp() * (pols_ipt_stay(t) + pols_itt_to_ipt(t))
        return (benefit_deces_pp(t) * pols_ipt_capital(t)
                * claim_admission)                                   # noqa: F821
    if kind in ("LAPSE", "MATURITY"):
        return 0.0
    raise ValueError("invalid kind")


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y - 1)`` **[std]**.

    Steps on policy anniversaries, not monthly, which is how the notes write it.
    """
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def expenses(t):
    """Maintenance and claim-management expense in month t **[std]**.

    EUR 30 per policy a year on every policy in force, plus EUR 250 a year on every claim
    in payment, both a twelfth at a time and both inflating at 1.8 %.  No French ADE
    expense study was retrieved; EUR 30 is about 1.8 % of the anchor cell's annual
    premium, and the claim load reflects that an incapacity claim is medically managed
    while a death claim is not.
    """
    maint = expense_maint / 12.0 * inflation_factor(t) * pols_if(t)   # noqa: F821
    claim_mgmt = (expense_claim / 12.0 * inflation_factor(t)          # noqa: F821
                  * (pols_itt(t) + pols_ipt(t)))
    return maint + claim_mgmt


def liability_cf(t):
    """The notes' outgo-positive liability cash flow of month t.

    ``ben_deces + ben_ptia + ben_itt + ben_ipt + expenses - prem``, printed in exactly
    that orientation in the technical notes.  It is published verbatim so that the notes
    and the model can be compared line by line, and :func:`net_cf` is its negative.
    """
    return claims(t) + expenses(t) - premiums(t)


def net_cf(t):
    """The net cash flow of month t, **income positive**: ``-liability_cf(t)``.

    The library-wide sign convention.  Death, PTIA, *résiliation* and expiry generate no
    payment beyond what :func:`claims` carries: there is no surrender value and no
    maturity benefit.
    """
    return -liability_cf(t)


# -- Checks ------------------------------------------------------------------

def check_crd_resid(t):
    """The amortisation roll-forward residual over month t; zero everywhere.

    ``crd(t + 1) - (crd(t) (1 + i) - ech)``: the instalment of month t falls at its end,
    carrying the opening balance ``crd(t)`` to the closing one ``crd(t + 1)``.  The loan
    spine, two ways: the annuity form against the recursion.  This is the check a pasted
    *échéancier* fails - and it also catches the wrong rate conversion, since computing
    ``i`` as ``(1 + nominal)^(1/12) - 1`` moves the *échéance* and breaks the
    roll-forward against the annuity form.
    """
    return crd(t + 1) - (crd(t) * (1.0 + loan_rate_mth()) - echeance())


def check_crd():
    """True when the loan amortises exactly: the roll-forward closes and crd(T) = 0.

    Three statements at once - ``crd(0) = capital_initial``, ``crd(T) = 0`` at the final
    instalment, and ``crd(k) = crd(k-1)(1 + i) - ech`` at every k.  The whole product
    hangs off the *capital restant du*, so this is the first thing that must be true.
    :func:`check_crd_resid` gives the signed residual of the month that failed.
    """
    tol = 1e-9 * max(capital_initial(), 1.0)
    if abs(crd(proj_len())) > tol:
        return False
    if abs(crd(0) - capital_initial()) > tol:
        return False
    return all(abs(check_crd_resid(t)) <= tol
               for t in range(proj_len()))


def check_states_resid(t):
    """The four-state population identity residual at the start of month t; zero.

    ``healthy + ITT + IPT + cumulative exits`` must equal the starting population in every
    month.  This is the check that catches a leak in the cohort machinery: a mis-indexed
    duration shift, or a cover-cessation transfer that deletes the in-claim mass instead
    of moving it, drops population with no corresponding exit and nothing else in the
    model would notice.
    """
    return (pols_healthy(t) + pols_itt(t) + pols_ipt(t) + pols_exit_cum(t)
            - pols_if_init())


def check_states():
    """True when the four-state population identity holds in every projected month.

    No argument, one bool over all t, the library-wide shape of a ``check_*`` cells;
    :func:`check_states_resid` gives the signed residual of the month that failed.
    """
    return all(abs(check_states_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(proj_len()))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1)`` less exits and, in the last month, the expiry.
    Inceptions, recoveries, IPT transitions and the cover-cessation transfer are absent
    because they move lives *between* states rather than out of the policy count - which
    is the point of running the check on the whole population rather than on one state.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_exit(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The tolerance scales with :func:`pols_if_init`, since the residual accumulates
    rounding on that many policies.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(proj_len()))


def check_benefit_split_resid(t):
    """The residual of the ITT / IPT paying-mass identity in month t; zero everywhere.

    The paying mass equals the **closing** disabled population, less the month's new
    inceptions, plus the share of the capped cohort that went back to ``healthy``::

        ben_itt + ben_ipt = ech Q IR (l_itt(t+1) - n_itt(t) + l_ipt(t+1) + cap_return(t))

    on the ``echeance`` IPT basis, and ``ben_itt = ech Q IR (l_itt(t+1) - n_itt(t) +
    cap_itt(t))`` on the ``crd`` one, where the entrants take a capital instead.

    The ``cap_return`` term is the one an implementation forgets: those lives were in ITT
    throughout the month and are paid for it, but they end the month in ``healthy`` and so
    appear in neither closing disabled state.  The check is **not** an identity by
    construction, because :func:`pols_itt_close` reads the next month's opening cohort
    vector out of the recursion while the benefit sums the survivals directly - a
    mis-indexed duration shift moves one and not the other.  It also catches paying the
    ITT to IPT movers twice, or not at all, and paying a claim in the month it incepts.
    """
    paid = claims(t, "ITT")
    if ipt_benefit_basis() == "echeance":
        paid = paid + claims(t, "IPT")
        mass = (pols_itt_close(t) - pols_itt_inception(t)
                + pols_ipt_close(t) + pols_cap_return(t))
    else:
        mass = pols_itt_close(t) - pols_itt_inception(t) + pols_itt_cap(t)
    return paid - benefit_itt_pp() * mass


def check_benefit_split():
    """True when the ITT / IPT paying-mass identity holds in every projected month."""
    scale = max(benefit_itt_pp(), 1.0) * max(pols_if_init(), 1.0)
    return all(abs(check_benefit_split_resid(t)) <= 1e-10 * scale
               for t in range(proj_len()))


def check_cover_end_resid(t):
    """ITT and IPT benefit and population after the ITT/IPT cover has ceased; zero.

    **Zero by construction in this implementation**, because :func:`itt_cohorts` and
    :func:`pols_ipt` return zero from the cover-end month and every ITT and IPT quantity
    is computed off them.  It is published anyway because the mis-implementation it names
    is the notes' fourth pitfall and is invisible from anywhere else: a model that gates
    only the *premium* on the guarantee, or that keeps paying the annuity to a life whose
    cover expired, produces a plausible-looking projection that is wrong by the whole
    post-70 in-claim liability.  The companion facts - that the mass is moved rather than
    deleted, and that the premium does **not** stop - are asserted by
    :func:`check_states` and by the premium column respectively.
    """
    if cover_itt(t):
        return 0.0
    return claims(t, "ITT") + claims(t, "IPT") + pols_itt(t) + pols_ipt(t)


def check_cover_end():
    """True when no ITT or IPT benefit is paid after the guarantee's age limit."""
    return all(abs(check_cover_end_resid(t)) <= 1e-12
               for t in range(proj_len()))


# -- Discounting: a companion, not part of the projection --------------------

def disc_factor(t):
    """v(t) = (1 + i)^(-(t + 1)/12): the notes' flat discount factor **[std]**.

    The cash flows of month t fall at its end, time ``t + 1`` months from adhesion, so
    ``disc_factor(0)`` discounts one month and ``disc_factor(11)`` exactly one year.

    A **companion to** the cash flow projection, not part of it: no line of
    :func:`result_cf` is discounted, and every other model in this library projects
    undiscounted gross cash flows and leaves discounting to the layer that consumes them.
    It exists because the notes' Checks quote present values.  A Solvabilité II best
    estimate discounts these same cash flows on the EIOPA risk-free term structure
    instead of a flat 2.5 %; no numeric EIOPA curve value was extracted anywhere in this
    library, which is why the reference rate here is a modeling convention.
    """
    return (1.0 + disc_rate) ** (-(t + 1) / 12.0)                    # noqa: F821


def pv_premiums():
    """The present value of premium income over the whole projection, at ``disc_rate``.

    EUR 12 602.19 on the anchor cell, against EUR 12 588.82 for the same cover on the CRD
    premium basis - a ratio of 1.001062, which is the calibration of the CRD scale.
    """
    return sum(premiums(t) * disc_factor(t)
               for t in range(proj_len()))


def pv_claims(kind=None):
    """The present value of benefit outgo, by kind; the total when kind is omitted.

    On the anchor cell: Décès 7 170.56, PTIA 635.87, ITT 1 932.71 and IPT 1 293.18, so
    death and PTIA are 70.8 % of the benefit present value and the incapacity side 29.2 %.
    """
    return sum(claims(t, kind) * disc_factor(t)
               for t in range(proj_len()))


def pv_expenses():
    """The present value of expenses over the whole projection, at ``disc_rate``.

    EUR 334.17 on the anchor cell - second-order for the total and first-order for the
    margin.
    """
    return sum(expenses(t) * disc_factor(t)
               for t in range(proj_len()))


def pv_outgo():
    """The present value of all outgo: benefits plus expenses.

    EUR 11 366.49 on the anchor cell against EUR 12 602.19 of premium, a margin of 9.81 %.
    """
    return pv_claims() + pv_expenses()


# -- Result tables -----------------------------------------------------------

def result_cf():
    """Result table of cashflows, indexed by policy month t.

    ``pols_if`` is healthy plus ITT plus IPT at the start of the month.  ``pols_healthy``
    is published beside it because it, and not ``pols_if``, is the weight on premium
    income - the difference between the two columns is the population whose premiums are
    waived.  ``crd`` is the loan balance at the **end** of the month, ``crd(t + 1)`` on
    the loan's own time-point index, which is the sum insured for the Décès and PTIA
    columns.  Nothing here is discounted; see :func:`disc_factor`.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_healthy": [pols_healthy(t) for t in ts],
            "pols_itt": [pols_itt(t) for t in ts],
            "pols_ipt": [pols_ipt(t) for t in ts],
            "crd": [crd(t + 1) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_ptia": [claims(t, "PTIA") for t in ts],
            "claims_itt": [claims(t, "ITT") for t in ts],
            "claims_ipt": [claims(t, "IPT") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_states():
    """Result table of state movements and rates, indexed by policy month t.

    The closing states are the notes' own ``l_h(t + 1)``, ``l_itt(t + 1)`` and
    ``l_ipt(t + 1)`` - the state at the end of month t - so the worked example's table
    can be read straight off this frame.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_healthy_close": [pols_healthy_close(t) for t in ts],
            "pols_itt_close": [pols_itt_close(t) for t in ts],
            "pols_ipt_close": [pols_ipt_close(t) for t in ts],
            "pols_death_healthy": [pols_death_healthy(t) for t in ts],
            "pols_ptia": [pols_ptia(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_itt_inception": [pols_itt_inception(t) for t in ts],
            "pols_itt_recovery": [pols_itt_recovery(t) for t in ts],
            "pols_itt_to_ipt": [pols_itt_to_ipt(t) for t in ts],
            "pols_itt_death": [pols_itt_death(t) for t in ts],
            "pols_itt_cap": [pols_itt_cap(t) for t in ts],
            "pols_ipt_death": [pols_ipt_death(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "itt_inception_rate": [itt_inception_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

ptia_ratio = 0.1

ipt_mort_factor = 3.0

ipt_share_at_cap = 0.35

selection_load = 0.0

claim_admission = 1.0

market_prem_ratio = 1.0

lapse_beta = 3.0

lapse_rate_max = 0.35

subst_acceptance = 0.88

expense_maint = 30.0

expense_claim = 250.0

inflation_rate = 0.018

disc_rate = 0.025

pd = ("Module", "pandas")
