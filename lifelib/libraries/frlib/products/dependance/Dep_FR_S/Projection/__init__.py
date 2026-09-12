# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Dep_FR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 9            # or switch the default

``t`` counts **policy months**, 0-based, exactly as the technical notes index them:
``t = 0`` is the first policy month and ``t = proj_len() - 1`` the last, so
``result_cf()`` runs ``0 ... proj_len() - 1``. Cover is *viagère* with no age limit, so
what ends the projection is a **[std]** terminal age of 110 rather than the contract:
``proj_len() = 12 (terminal_age - entry_age)`` is the **number of projected months**,
480 on the base cell. The state ledgers are indexed at the **start** of the month, so
every cash flow on a ``result_cf()`` row is weighted by a state count on the same row.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/dependance/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Dep_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Dep_FR_S.Data`, reached here through the ``data`` Reference:

========================  ==================================  ==========================
Reference                 Cells                               File
========================  ==================================  ==========================
model_point_file          data.model_point_table()            model_point_table.csv
mort_table_file           data.mort_table()                   mort_table.csv
prevalence_file           data.prevalence_table()             prevalence_table.csv
severity_share_file       data.severity_share_table()         severity_share_table.csv
lapse_table_file          data.lapse_table()                  lapse_table.csv
cause_mix_file            data.cause_mix_table()              cause_mix_table.csv
reduction_file            data.reduction_table()              reduction_table.csv
revision_file             data.revision_table()               revision_table.csv
========================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for population counts, plural nouns
for cash flows, ``*_rate`` for annual rates and ``*_rate_mth`` for monthly ones,
``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind`` string.
The technical notes use compact actuarial symbols instead. The mapping is:

=========================  ================================  ==========================
Notes symbol               Cells                             Meaning
=========================  ================================  ==========================
(none)                     model_point()                     The selected model point
entry_age                  age_at_entry()                    Entry age, différence de
                                                             millésimes
x = age(t)                 age(t)                            Attained age in month t
y(t)                       policy_year(t)                    Policy year, t // 12 + 1
(none)                     duration(t)                       Completed policy years
(none)                     duration_mth(t)                   Months elapsed, equal to t
(none)                     terminal_age                      110, what ends the run
proj_len                   proj_len()                        The number of projected
                                                             months, exclusive end of t
z                          (the duration argument)           Months since first
                                                             recognition
fr                         franchise_months()                Franchise, 3 months
(none)                     max_dur()                         Longest duration tracked
G(y)                       rente_total_pp(t)                 Guaranteed rente totale
rho                        partial_ratio()                   Partial / total ratio, 0.50
rho G(y)                   rente_partial_pp(t)               Guaranteed rente partielle
G_pay(t, z)                rente_pay_pp(t, z)                Rente totale in payment for
                                                             the cohort at duration z
rho G_pay(t, z)            rente_pay_partial_pp(t, z)        The same, partial ledger
CAP(y)                     capital_pp(t)                     Capital d'équipement
P(y)                       premium_mth_pp(t)                 Monthly premium
12 P(y)                    premium_pp(t)                     The same, annualised
(none)                     premium_factor(y)                 Its compound index
g_G                        reval_guarantee                   Revalorisation des garanties
g_S                        reval_rente                       Revalorisation des rentes
                                                             en service
r(y)                       revision_rate(t)                  Scheduled tariff revision
M_rev(y)                   revision_lapse_factor(t)          Premium-shock lapse module
cum_prem(t)                cum_prem_pp(t)                    Premiums paid per policy
c(n)                       reduction_coeff(n)                Barème coefficient
S(t)                       carence_factor(t)                 Share of causes covered
(none)                     carence_months(cause)             The three carence lengths
mu_H(x)                    mort_force(t)                     Healthy force of mortality
mubar                      mort_force_avg(t)                 Population average force
(table)                    mort_rate(t)                      Healthy annual mortality
q_H(t)                     mort_rate_mth(t)                  The same, monthly
k_P, k_T                   mort_partial_mult,                State mortality multiples
                           mort_total_mult
(none)                     mort_rate_partial(t)              Partielle annual mortality
q_P(t)                     mort_rate_partial_mth(t)          The same, monthly
(none)                     mort_rate_total(t)                Totale annual mortality
q_T(t)                     mort_rate_total_mth(t)            The same, monthly
prev(x)                    prev_rate(t)                      APA prevalence
prev'(x)                   prev_slope(t)                     Its derivative in age
s_P, s_T                   severity_share(kind)              Public-to-insured shares
pi_P, pi_T                 prev_partial(t), prev_total(t)    Insured-state prevalence
i_P(x)                     inc_rate_partial(t)               Annual entry into partielle
i_Pm(t)                    inc_rate_partial_mth(t)           The same, monthly
i_T(x)                     inc_rate_total(t)                 Annual entry into totale
i_Tm(t)                    inc_rate_total_mth(t)             The same, monthly
i_A                        aggravation_rate                  Aggravation force
i_Am                       aggravation_rate_mth()            The same, monthly
(held at zero)             recovery_rate                     Return to autonomy
w(t)                       lapse_rate(t)                     Annual lapse rate
(table)                    lapse_rate_base(t)                Table rate before the shock
w(t) monthly               lapse_rate_mth(t)                 Monthly lapse rate
auto(t)                    pols_auto(t)                      Autonomous, premium-paying
red(t)                     pols_red(t)                       Paid-up on a reduced rente
(none)                     red_rente_pp(t)                   Its mean frozen rente
pols_part(t, z)            pols_part_dur(t, z)               In partielle at duration z
(sum over z)               pols_part(t)                      In partielle
pols_tot(t, z)             pols_tot_dur(t, z)                In totale at duration z
(sum over z)               pols_tot(t)                       In totale
pols_totr(t, z)            pols_totr_dur(t, z)               In totale on a reduced rente
(sum over z)               pols_totr(t)                      The same, total
(the four vectors)         dep_cohorts(t)                    The cohort ledgers as lists
pols_if(t)                 pols_if(t)                        Every ledger added
(none)                     pols_if_at(t, timing)             BEF_DECR / AFT_DECR
(none)                     pols_prem(t)                      Population paying premium
surv(t), base(t)           pols_surv(t), pols_base(t)        Autonomous survivors
n_P(t)                     pols_entry_partial(t)             Entrants into partielle
n_T(t)                     pols_entry_total(t)               Entrants into totale
n_Tr(t)                    pols_entry_total_red(t)           The same, from the reduced
n_A(t)                     pols_aggravation(t)               Aggravations partielle to
                                                             totale
(none)                     pols_aggravation_recog(t)         Those of them recognised
(none)                     pols_recognition(t)               First recognitions
(none)                     pols_death(t)                     Deaths, all five ledgers
lapse(t)                   pols_lapse(t)                     Lapses out of autonomy
(none)                     pols_lapse_exit(t)                Those that leave outright
(none)                     pols_reduction(t)                 Those that become paid-up
carence_exit(t)            pols_carence_exit(t)              Memberships terminated by
                                                             the carence
(none)                     pols_recovery(t)                  Returns to autonomy; zero
P x auto(t)                premiums(t)                       Premium income
claims_rente(t)            claims(t, "RENTE")                Rente outgo
claims_capital(t)          claims(t, "CAPITAL")              Capital d'équipement outgo
0                          claims(t, "LAPSE")                Surrender outgo; always zero
(none)                     instalments(t)                    Rente instalments paid
refunds_carence(t)         refunds_carence(t)                Premiums returned
e(y), a(y)                 expenses(t)                       Maintenance and assistance
ec_adj, ec_ren             claim_expenses(t)                 Adjudication and handling
(none)                     inflation_factor(t)               Expense inflation factor
net_cf(t)                  net_cf(t)                         Net cash flow, income
                                                             positive
(the calibration)          sojourn_total(x0)                 Expected sojourn in totale
(the calibration)          sojourn_partial(x0)               Expected sojourn in
                                                             partielle
=========================  ================================  ==========================

Four names needed care.

The notes write one symbol ``q`` with three subscripts for the three mortality rates.
:func:`mort_rate` is the **healthy-life** one, because that is what ``mort_rate`` means
in every other model in this library — the rate applying to the population the
projection starts with — and the two dependent-state rates are :func:`mort_rate_partial`
and :func:`mort_rate_total`. Reading a dependent's mortality out of ``mort_rate`` is
precisely this product's largest available error, and the naming is there to prevent it.

``t`` is the policy month and ``z`` the months since **first** recognition. They are
different clocks and the model never mixes them: the *carence* takes ``t`` and the
*franchise* takes ``z``.

The notes call the whole paid-up ledger ``red`` and the amount it carries a frozen
``G(y) c(n)``. The ledger is :func:`pols_red` and the amount :func:`red_rente_pp`, a
probability-weighted mean over reduction cohorts. That is exact in expectation, because
incidence does not depend on the amount, and it is what the notes license an
implementation to do instead of carrying a per-reduction-cohort amount.

``carence_exit(t)`` is spelled :func:`pols_carence_exit`. It is a policy count and every
other policy count in the library starts ``pols_``; the cash flow it drives keeps the
notes' own name, :func:`refunds_carence`, because it is a **refund of premiums and not a
claim** and belongs on its own line.

.. rubric:: Five ledgers, and why the model needs all of them

The health chain is *autonome* → *dépendance partielle* / *dépendance totale* → *décès*,
with lapse as a further exit from autonomy, and a fifth in-force but paid-up ledger,
*réduite*, reached only by lapse from eight full years of premiums::

                     +------------- i_T -----------------+
                     |                                   v
    autonome ---- i_P + ---> partielle ---- i_A ---> totale ----> deces
       |                         |                     |
       |                         v                     v
       |                       deces                 deces
       |
       +-- lapse before 8 years --> nothing at all
       |
       +-- lapse from 8 years ----> reduite --- i_T ---> totale (reduced rente)

Three absences are product facts, not gaps. There is **no account value and no surrender
value**, so no ``cv_pp`` exists and a lapse before eight years carries no cash flow at
all. There is **no death benefit** on this composite, so no ``claims_death`` exists.
And there is **no maturity**: the cover is *viagère*.

:func:`pols_red` is the one ledger a naive model omits, and omitting it is a first-order
error: lapse from year 8 does **not** release the liability, it converts it into a
smaller one that keeps running for life. On the base cell that ledger peaks at 8.27% of
the original policy at month 194, attained age 86 — the largest state in the model after
:func:`pols_auto` at that duration — and dropping it understates lifetime claims by
4.57%.

Recovery out of a covered state is a **named input held at zero**, not an omission:
``recovery_rate`` is wired into the ledger roll and into :func:`pols_recovery`, and the
base run sets it to zero, as the only retrieved actuarial reference on this product
does. The direction of error is one-sided — claims are overstated — and no retrieved
source quantifies it.

.. rubric:: The two dependent ledgers are two-dimensional

A cohort must be indexed by the months since first recognition, ``z``, for two reasons
that have nothing to do with each other. The **franchise** drops the first three
instalments, so a cohort is paid only from ``z >= franchise_months() + 1``. And the
*rente* in payment is the guarantee of the policy year in which the cohort was
recognised, indexed forward at ``reval_rente`` — a different rate from the one that
indexes the guarantee before claim — so the amount depends on the cohort's vintage,
which is what ``z`` records.

:func:`dep_cohorts` holds all four vectors for one month and is the model's only
list-valued cells. The alternative — four two-argument recursions — would be
``4 proj_len() max_dur()`` separate cells, nearly a million on the base cell, each
with its own cache entry. Keeping them in one cells per month makes it ``proj_len()``
cells with a loop inside, and :func:`pols_part_dur` and its siblings read elements out of
it so that the notes' two-dimensional objects are still addressable by name. The lists
are rebuilt rather than mutated on each step, so a caller cannot corrupt the cache by
holding one.

The fourth vector is the *value* ledger of the reduced-rente claims: element ``z - 1`` is
the population at duration ``z`` **times the reduced rente it is being paid**. It exists
because those amounts are frozen individually at each reduction date, not derivable from
the policy year the way the other two ledgers' amounts are.

.. rubric:: The carence and the franchise are different things

The *carence* runs from **inception**, is cause-specific, blocks the benefit **and
terminates the membership with a full refund of premiums**. The *franchise* runs from
**recognition**, is three months, and only delays payment. They are the two easiest
things in this product to apply in each other's place, and they cost different amounts:
removing the *carence* raises lifetime claims by 3.99% and removing the *franchise* by
7.09%.

:func:`carence_factor` is the share of causes already covered at month ``t``, read from
the **[std]** cause mix against the model point's own three *carence* lengths: 0.10 in
policy year 1, 0.65 in years 2 and 3, 1.00 thereafter on the base cell. Note what it
does **not** touch: :func:`pols_auto` at ``t + 1`` does not depend on it, because a
*carence* claim ends the membership rather than deferring it. The blocked lives leave
the in-force ledger exactly as the covered ones do, and they take a refund of every
premium paid with them — in policy year 1 of the base cell that refund is three quarters
of the year's *rente* and *capital* claims combined.

The *franchise* is **not a premium holiday**. *Exonération* runs from recognition, so a
life inside the three-month *franchise* pays no premium and receives no *rente*.

.. rubric:: State-dependent mortality is the largest lever on this product

A dependent life's mortality is far heavier than a healthy life's at the same age.
:func:`mort_rate_partial` and :func:`mort_rate_total` apply proportional hazards on the
force, ``mort_partial_mult`` 1.75 and ``mort_total_mult`` 4.27, so the annual rates at
attained age 85 are 0.06179, 0.10562 and 0.23841. Applying healthy mortality to
dependent lives while leaving the incidence basis unchanged raises lifetime claims by
**159.7%**.

``mort_total_mult`` is **calibrated, not guessed**: :func:`sojourn_total` returns 2.9989
years from exact age 84 at 4.27, against the mean duration of about three years the CCSF
reports for heavy dependents. At 2.75 the same calculation gives 4.19 years and at 3.50,
3.50 — the sojourn is far more sensitive to the multiple than a first look suggests.
``mort_partial_mult`` has **no such anchor**: it must exceed 1 and sit well below
``mort_total_mult``, and at 1.75 :func:`sojourn_partial` gives 3.14 years from age 82,
the same order as the 29.2-month mean duration of APA receipt across all GIRs.

.. rubric:: Prevalence is not incidence, and the identity that converts them

Every public French number about dependence measures **receipt of the *allocation
personnalisée d'autonomie***. It is a **prevalence**, not an incidence, and it is a
**public** classification rather than the insurer's. Both conversions are explicit steps
here.

:func:`severity_share` is the first: the fractions of APA prevalence read as insured
*partielle* and *totale*, keyed by the contract's trigger grid, **[std]** against two
indirect anchors. :func:`inc_rate_partial` and :func:`inc_rate_total` are the second, and
they are an **identity** rather than an approximation — differentiating the state
proportions along the age axis gives entry forces in terms of the prevalence slope, the
aggravation force and all three mortality forces.

Three properties of that identity an implementation must respect, and this one does. The
mortality terms are **not refinements**: a rising prevalence understates incidence
because the dependent population is simultaneously being drained by its own excess
mortality. ``aggravation_rate`` and :func:`inc_rate_total` are **not independent
inputs**: raising the aggravation force lowers the direct-to-*totale* incidence, because
the stock of *totale* lives is pinned by the assumed prevalence — consistently varying
the rate from 0 to 0.20 to 0.40 moves lifetime claims by only +0.54% / 0 / -0.52%, while
adding it *without* re-deriving the incidence raises them 0.84% and puts the lives in the
wrong state. And :func:`inc_rate_partial` **can go negative at extreme ages**, where the
prevalence slope flattens while excess mortality does not; both rates are floored at
zero **[std]**, which never binds on the female base cell — :func:`inc_rate_partial` is
still 0.0040 at attained age 109 — and binds at attained age 109 on the male basis.

.. rubric:: Two indexations, two ledgers

``reval_guarantee`` moves the guarantee and the premium in the same proportion.
``reval_rente`` moves every *rente* in payment, whatever its vintage. The reduced
guarantee moves with **neither**. Collapsing the two rates into one happens to work only
when they are equal, and the base configuration deliberately sets them different — 1.0%
against 1.5% — so that a test can tell.

.. rubric:: Premium income rides on pols_auto, never on pols_if

Lives in a recognised state are exonerated and reduced lives are paid up, so neither band
pays anything. :func:`pols_prem` is the premium-paying population and it is
:func:`pols_auto` on every model point except a ``total_only`` one, where the *partielle*
ledger is not a recognised state and therefore keeps paying. Charging premium to the
whole in-force block overstates income by the whole reduced ledger plus the whole claim
ledger: on the base cell, at attained age 90 those two bands together are 44.6% of the
in-force block.

.. rubric:: What cover_type does, and the one thing it standardizes

``cover_type = total_and_partial`` is the composite the notes specify and the basis of
the worked example. ``cover_type = total_only`` buys the *rente totale* alone, and the
model reads that as: *partielle* is **not a recognised state**, so it pays no *rente*, it
carries no *capital*, it does not exonerate the premium — and the *carence* and the
*franchise* both attach at entry into *totale*, whether direct or by aggravation, since
that is then the first recognition. The health chain is untouched, which is what keeps
the prevalence identity intact.

One consequence is a **[std]** departure worth naming: on a ``total_only`` cell an
aggravating life starts a **fresh** duration cohort and therefore serves a *franchise*,
where on a ``total_and_partial`` cell the duration index runs from first recognition and
deterioration does not restart it. Both readings follow from the same principle — the
clock runs from first recognition of a **covered** state — and no retrieved document
addresses either directly.

.. rubric:: The capital d'équipement is paid once per membership

It is paid on **first entry into a covered state**, never twice, and a reduced membership
has lost the option. So it rides on :func:`pols_recognition` less the entrants out of the
reduced ledger, and an aggravation produces no *capital* on a ``total_and_partial`` cell.
Paying it again on aggravation would inflate capital claims by the whole aggravation
flow.
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
    """The policy identifier of the selected model point."""
    return str(model_point()["policy_id"])


def age_at_entry():
    """The entry age of the selected model point, *différence de millésimes*.

    Sourced band 40 to 75 inclusive at signature.  On an in-force cell —
    ``status`` of ``partial``, ``total`` or ``reduced`` — this is the **attained age at
    the valuation date** and the policy-year clock restarts there **[std]**: the notes
    give no anniversary offset for an in-force membership, so the two indexations step
    at ``t = 12, 24, ...`` from the valuation date rather than from the contractual
    anniversary.
    """
    return int(model_point()["entry_age"])


def sex():
    """The sex (M / F) of the selected model point.

    The **decrements** are sex-split — both the mortality proxy and the prevalence
    logistic have a row per sex — while the **premium is unisex**, compulsory since the
    2004 EU directive, so ``premium_mth`` is a model point column and not a rate looked
    up by sex.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def cover_type():
    """``total_and_partial`` or ``total_only``: which states the contract covers.

    The composite of the technical notes is ``total_and_partial`` and it is what the
    worked example runs.  See the Space docstring for what ``total_only`` changes and
    for the one **[std]** departure it forces on the duration clock.
    """
    v = model_point()["cover_type"]
    if v not in ("total_and_partial", "total_only"):
        raise ValueError("invalid cover_type")
    return v


def cover_partial():
    """True when *dépendance partielle* is a covered, recognised state.

    The single switch the rest of the model consults, so that the four consequences of
    ``cover_type`` — the *rente*, the *capital*, the premium *exonération* and where the
    *carence* and the *franchise* attach — cannot drift apart.
    """
    return cover_type() == "total_and_partial"


def trigger_grid():
    """``avq5``, ``avq6`` or ``aggir``: the grid the contract triggers on.

    Three alternative *definitions of the same two states*, and the reference model has
    to price all three because its decrement basis is built from public GIR-graded APA
    data.  The grid enters through :func:`severity_share` and nowhere else: a stricter
    grid is a smaller share of public prevalence, not a different chain.
    """
    v = model_point()["trigger_grid"]
    if v not in ("avq5", "avq6", "aggir"):
        raise ValueError("invalid trigger_grid")
    return v


def rente_total_mth():
    """G(1): the guaranteed *rente totale* at issue, EUR a month.

    1,000 on the base cell, a **[std]** pick inside the sourced 500-3,000 band chosen
    because it is the cover for which the only age-graded French price point exists.  On
    an in-force dependent cell it is the amount **in payment at the valuation date**,
    and on a ``reduced`` cell it is the **full guarantee** before the *barème*
    coefficient is applied.
    """
    return float(model_point()["rente_total_mth"])


def partial_ratio():
    """rho: the *rente partielle* as a fraction of the *rente totale*.

    0.50, modal across five retrieved providers.  The two *rentes* are mutually
    exclusive: recognition of *totale* never opens partial rights.
    """
    return float(model_point()["partial_ratio"])


def partial_ratio_paid():
    """The ratio actually paid: :func:`partial_ratio`, or zero on a ``total_only`` cell.

    Kept separate from :func:`partial_ratio` so that the model point still records the
    contractual ratio on a cell that does not buy the *rente partielle*.
    """
    return partial_ratio() if cover_partial() else 0.0


def capital_option():
    """Whether the optional *capital d'équipement* is bought."""
    return bool(model_point()["capital_option"])


def capital_amount():
    """CAP(1): the *capital d'équipement* at issue, EUR, 3,500 on the base cell.

    Observed amounts run from 3,000 to 10,000 across the retrieved contracts; the base
    cell's 3,500 is the AXA figure.  Paid **once** per membership on first entry into a
    covered state, with no *franchise* **[std]**, and the guarantee is extinguished on
    payment regardless of later deterioration.
    """
    return float(model_point()["capital_amount"]) if capital_option() else 0.0


def premium_mth():
    """P(1): the monthly premium at issue, EUR, an **input and not a computed quantity**.

    No French insurer publishes a general individual LTC rate table.  The base cell's
    75 EUR a month is the CCSF's 2013 indicative price for exactly this cover at entry
    age 70 — dated and indicative, and used because inventing a premium would be worse.
    The premium is *viagère*: level for the entry age but payable for life, with no
    premium-paying term.
    """
    return float(model_point()["premium_mth"])


def premium_mode():
    """``monthly``, ``quarterly``, ``half_yearly`` or ``annual``; the base cell is monthly.

    Payment is always **in advance**.  No fractional-payment loading is applied
    **[std]**: no retrieved document discloses one, so an annual payer pays exactly
    twelve monthly premiums at the start of the policy year.
    """
    v = model_point()["premium_mode"]
    if v not in ("monthly", "quarterly", "half_yearly", "annual"):
        raise ValueError("invalid premium_mode")
    return v


def premium_months():
    """The number of months one premium instalment covers: 1, 3, 6 or 12."""
    return {"monthly": 1, "quarterly": 3, "half_yearly": 6, "annual": 12}[
        premium_mode()]


def premium_due(t):
    """True when a premium instalment falls due at the start of month t.

    Instalments fall on months 0, ``premium_months()``, ``2 premium_months()``, ... of
    the projection, so an annual payer pays at each policy anniversary.
    """
    return t % premium_months() == 0


def couple_discount():
    """Whether the 10% *réduction couple* applies; off on the base cell.

    Real and common — both spouses joining within three months, lost if either
    membership is resiliated or reduced — but a rating adjustment with no cash-flow
    mechanics beyond scaling the premium, conditional on facts about a second life the
    model point does not carry.
    """
    return bool(model_point()["couple_discount"])


def couple_factor():
    """The premium multiplier the couple discount applies, 0.90 or 1.00."""
    return 1.0 - couple_discount_rate if couple_discount() else 1.0  # noqa: F821


def carence_accident_months():
    """The *carence* for accident, 0 months on every retrieved contract."""
    return int(model_point()["carence_accident_months"])


def carence_illness_months():
    """The *carence* for illness other than neurological or psychiatric, 12 months."""
    return int(model_point()["carence_illness_months"])


def carence_neuro_months():
    """The *carence* for neurological, neurodegenerative or psychiatric illness.

    36 months, the longest of the three, on every retrieved contract — which is what an
    insurer does when a cause is both frequent and adversely selected, and every
    retrieved contract puts an MMSE overlay on exactly that cause.
    """
    return int(model_point()["carence_neuro_months"])


def carence_months(cause):
    """The *carence* length in months for one of the three causes.

    ``accident``, ``illness`` and ``neuro``, the three keys of
    ``cause_mix_table.csv``.  A membership on which dependence arises from a cause still
    inside its *carence* is **terminated and every premium refunded**; the benefit is
    not merely deferred.
    """
    if cause == "accident":
        return carence_accident_months()
    if cause == "illness":
        return carence_illness_months()
    if cause == "neuro":
        return carence_neuro_months()
    raise ValueError("invalid cause")


def franchise_months():
    """fr: the *franchise* in months, 3 on the base cell.

    Absolute and measured from recognition, so a cohort is paid from
    ``z >= fr + 1``: the cohort recognised at the end of month ``s`` is first paid at the
    end of month ``s + 4``.  This is a **[std]** monthly reading of "le 91e jour",
    corroborated rather than assumed — one retrieved contract restores exactly three
    instalments at the first payment.
    """
    return int(model_point()["franchise_months"])


def reduction_qualifying_years():
    """The full consecutive years of premiums that qualify for *mise en réduction*.

    Eight on the base cell; the observed range is five to eight across the retrieved
    contracts.  Below it a lapsed membership ends with no value at all.
    """
    return int(model_point()["reduction_qualifying_years"])


def status():
    """Which ledger the population starts in at ``t = 0``.

    ``autonomous``
        the whole population is autonomous and premium-paying.

    ``partial`` / ``total``
        a claim already in payment, seeded into the corresponding
        dependent ledger at :func:`claim_duration_months`.

    ``reduced``
        a paid-up membership on a reduced *rente totale*, seeded with
        :func:`years_paid` years of premiums behind it.

    An in-force portfolio needs all four kinds of cell.
    """
    v = model_point()["status"]
    if v not in ("autonomous", "partial", "total", "reduced"):
        raise ValueError("invalid status")
    return v


def claim_duration_months():
    """z0: the months since recognition already elapsed on an in-force claim cell.

    The seeded population enters cohort ``z0 + 1``, since cohort 1 is a state recognised
    at the end of the month before the valuation date.  A cell seeded at
    ``z0 = franchise_months()`` is therefore paid in its very first month.
    """
    return int(model_point()["claim_duration_months"])


def years_paid():
    """n: the completed years of premiums behind a ``reduced`` cell.

    It selects the *barème* coefficient the frozen reduced *rente* carries, and it is
    ignored on every other kind of cell.
    """
    return int(model_point()["years_paid"])


def pols_if_init():
    """Initial number of policies; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


# --- the policy clock ---

def proj_len():
    """The number of projected months: ``12 (terminal_age - age_at_entry())``.

    480 on the base cell, and it is the **exclusive end** of the frame: the projection
    runs ``t = 0 ... proj_len() - 1`` and ``result_cf()`` has ``proj_len()`` rows, which
    is lifelib's ``range(proj_len())``.  Cover is *viagère* with no age limit, so **what
    ends the projection is the terminal age of the decrement basis, not the contract** —
    there is no maturity, no expiry and no maturity benefit.  ``terminal_age`` is 110
    **[std]**, above which the mortality table forces the rate to 1.
    """
    return 12 * (terminal_age - age_at_entry())                      # noqa: F821


def duration(t):
    """Completed policy years at the start of month t: ``t // 12``.

    0-based, as ``duration`` is throughout lifelib: 0 through the first policy year.
    """
    return t // 12


def duration_mth(t):
    """Months elapsed from the start of the projection at the start of month t.

    Equal to ``t``, since ``t`` is 0-based.  The cells exists so that the monthly models
    in this library share one vocabulary.
    """
    return t


def policy_year(t):
    """y(t) = t // 12 + 1: the policy year containing month t; 1 for t = 0..11."""
    return duration(t) + 1


def age(t):
    """x: the attained age in the policy year containing month t.

    ``age_at_entry() + t // 12``, advancing at each policy anniversary **[std]** — the
    entry age is by *différence de millésimes* and the model advances it annually rather
    than on a birthday it does not carry.
    """
    return age_at_entry() + duration(t)


def max_dur():
    """The longest claim duration the cohort vectors have to carry.

    ``proj_len() + claim_duration_months() + 1``, 481 on the base cell: a cohort seeded
    at duration ``z0 + 1`` reaches ``z0 + proj_len()`` in the last month
    ``t = proj_len() - 1``, and one recognised in month 0 reaches ``proj_len()``.  The
    last element is therefore structurally zero, which is what makes the duration shift
    lossless.
    """
    return proj_len() + claim_duration_months() + 1


def seed_dur():
    """The duration cohort the initial population occupies, or 0 if it is not seeded."""
    return claim_duration_months() + 1 if status() in ("partial", "total") else 0


def cohort_len(t):
    """The number of duration cohorts that can be non-zero at the start of month t.

    The vectors are truncated to this length rather than carried at full
    :func:`max_dur` from month zero.  It is purely a cost decision — a full-length
    vector in every month is ``proj_len() max_dur()`` floats where this is half
    that — and :func:`pols_part_dur` returns zero past the end of the list, so nothing
    about the two-dimensional view changes.
    """
    return min(max_dur(), t + seed_dur() + 1)


# --- guarantees, premium and the two indexations ---

def rente_total_pp(t):
    """G(y): the guaranteed *rente totale* in the policy year containing month t.

    Indexed at ``reval_guarantee`` on each policy anniversary, **before** claim.  Once a
    *rente* is in payment it leaves this cells behind and moves at ``reval_rente``
    instead — see :func:`rente_pay_pp`.
    """
    return rente_total_mth() * (1.0 + reval_guarantee) ** duration(t)  # noqa: F821


def rente_partial_pp(t):
    """rho G(y): the guaranteed *rente partielle*; zero on a ``total_only`` cell."""
    return partial_ratio_paid() * rente_total_pp(t)


def capital_pp(t):
    """CAP(y): the guaranteed *capital d'équipement* in the policy year containing t.

    Indexed at ``reval_guarantee`` alongside the *rente*, and zero when the option is
    not bought.
    """
    return capital_amount() * (1.0 + reval_guarantee) ** duration(t)  # noqa: F821


def rente_pay_pp(t, z):
    """G_pay(t, z): the *rente totale* in payment at month t for the cohort at duration z.

    A cohort recognised at the end of month ``t - z`` entered on the guarantee of its own
    policy year ``y_e`` and has been indexed at ``reval_rente`` at every anniversary
    since, so the amount is ``G(y_e) (1 + reval_rente)^(y - y_e)``.  **Two indexations,
    two ledgers**: ``reval_guarantee`` set the amount at recognition and ``reval_rente``
    has moved it ever since.  Collapsing them into one rate happens to work only when
    they are equal, and the base configuration sets them different so that a test can
    tell.

    A cohort seeded at ``t = 0`` on an in-force claim cell reads as policy year 1, which
    is the same **[std]** restart of the policy-year clock that :func:`age_at_entry`
    describes.
    """
    y_e = max(1, policy_year(t - z))
    return (rente_total_mth() * (1.0 + reval_guarantee) ** (y_e - 1)  # noqa: F821
            * (1.0 + reval_rente) ** (policy_year(t) - y_e))          # noqa: F821


def rente_pay_partial_pp(t, z):
    """rho G_pay(t, z): the *rente partielle* in payment for the cohort at duration z."""
    return partial_ratio_paid() * rente_pay_pp(t, z)


def revision_rate(t):
    """r(y): the scheduled tariff revision in the policy year containing month t.

    Applied to the premium **on top of** ``reval_guarantee``, and capped at 10% a year
    excluding *revalorisation* by the only retrieved contract that states a cap.  Nil
    for five years then 1.5% a year on the shipped path, which is arbitrary inside that
    band: **a real tariff revision is a management action, not a projected assumption**,
    and it takes a deliberate substitution of ``revision_table.csv`` to project a
    repricing.
    """
    tbl = data.revision_table()                                      # noqa: F821
    return float(tbl.loc[min(policy_year(t), int(tbl.index.max())),
                         "revision_rate"])


def premium_factor(y):
    """The compound premium index in policy year y; 1.0 in policy year 1.

    ``(1 + reval_guarantee)(1 + r(y))`` per anniversary.  The premium rises **in the
    same proportion** as the *revalorisation* of the guarantees, which is contractual,
    and the tariff revision multiplies on top of that, which is discretionary.
    """
    if y <= 1:
        return 1.0
    return (premium_factor(y - 1) * (1.0 + reval_guarantee)          # noqa: F821
            * (1.0 + revision_rate(12 * (y - 1))))


def premium_mth_pp(t):
    """P(y): the **monthly** premium in the policy year containing month t.

    ``premium_mth() x couple_factor() x premium_factor(y)``.  An instalment of
    ``premium_months()`` of these falls due whenever :func:`premium_due` is true.

    The ``_mth_`` is load-bearing: library-wide ``premium_pp`` is the *annual*
    premium per policy and ``premium_mth_pp`` the monthly one.  Every recursion in
    this model works in months and so uses this cells, not :func:`premium_pp`.
    """
    return premium_mth() * couple_factor() * premium_factor(policy_year(t))


def premium_pp(t):
    """12 P(y): the **annual** premium per policy in the policy year containing month t.

    ``12 x premium_mth_pp(t)``.  A reporting convenience, not a cash flow: this
    contract is projected monthly and the instalments actually falling due are
    :func:`premiums`, built on :func:`premium_mth_pp` and :func:`premium_months`.  A
    quarterly or annual payer pays the same annual amount in fewer, larger
    instalments, there being no fractional-payment loading **[std]**.
    """
    return 12.0 * premium_mth_pp(t)


def cum_prem_pp(t):
    """cum_prem(t): premiums paid **per policy** up to and including the start of month t.

    The *contre-assurance* base: a membership terminated by the *carence* has every
    premium it ever paid refunded, and this is what is refunded.  It is a per-policy
    amount and not a population-weighted one, which is why :func:`refunds_carence`
    multiplies it by the terminating population rather than adding to it.

    The base case sits at ``t = 0``, the first projected month, and nothing is ever
    indexed below it: :func:`premium_due` is true at ``t = 0`` on every payment mode, so
    the first instalment always falls on the first row.
    """
    if t <= 0:
        return premium_mth_pp(0) * premium_months() if t == 0 else 0.0
    paid = premium_mth_pp(t) * premium_months() if premium_due(t) else 0.0
    return cum_prem_pp(t - 1) + paid


def years_premiums_paid(t):
    """n: the completed years of premiums at the **end** of month t, ``(t + 1) // 12``.

    Eight of them at ``t = 95``, which is the first month a lapse becomes a *mise en
    réduction* rather than an exit with nothing.
    """
    return (t + 1) // 12


def reduction_coeff(n):
    """c(n): the *barème* coefficient at n completed years of premiums.

    Zero below :func:`reduction_qualifying_years`, then the CNP Banque de France scale —
    25% at eight years rising about two points a year and capped at 70% from thirty.
    Years beyond the table take its last row.
    """
    if n < reduction_qualifying_years():
        return 0.0
    tbl = data.reduction_table()                                     # noqa: F821
    lo, hi = int(tbl.index.min()), int(tbl.index.max())
    if n < lo:
        return 0.0
    return float(tbl.loc[min(n, hi), "coefficient"])


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + inflation_rate)^(y - 1)`` **[std]**.

    Steps on policy anniversaries, not monthly, which is how the notes write it.  It
    applies to the maintenance and assistance levels and **not** to the two claim
    expenses, which are per-event amounts held flat **[std]**.
    """
    return (1.0 + inflation_rate) ** duration(t)                     # noqa: F821


# --- the decrement basis ---

def mort_rate(t):
    """The **healthy-life** annual mortality rate at the attained age in month t.

    A **[std]** Gompertz proxy shaped like a French population table, read from
    ``mort_table.csv`` by sex and age; **not** TH 00-02 / TF 00-02 or TGH05 / TGF05.
    The two dependent states carry heavier rates on different cells —
    :func:`mort_rate_partial` and :func:`mort_rate_total` — and reading a dependent's
    mortality out of this cells is the largest single error available on this product.
    """
    return float(data.mort_table().loc[(sex(), age(t)), "mort_rate"])  # noqa: F821


def mort_rate_mth(t):
    """q_H(t) = 1 - (1 - mort_rate)^(1/12): monthly healthy mortality **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def mort_force(t):
    """mu_H(x) = -ln(1 - mort_rate): the healthy force of mortality in month t.

    The identity behind :func:`inc_rate_partial` is written on forces, not on annual
    probabilities, and the two state multiples are proportional hazards **on this
    force** — which is what makes ``1 - (1 - q)^(k/12)`` the right monthly conversion for
    a dependent life and ``k q`` the wrong one.
    """
    q = mort_rate(t)
    return -math.log(1.0 - q) if q < 1.0 else float("inf")           # noqa: F821


def mort_rate_partial(t):
    """The annual mortality of a life in *dépendance partielle* at the attained age.

    ``1 - (1 - mort_rate)^k`` with ``k = mort_partial_mult``, a proportional hazard on
    the force **[std]**.  0.10562 at age 85 against 0.06179 healthy.  ``k`` has **no
    anchor**: it must exceed 1, because GIR 3-4 lives carry excess mortality, and sit
    well below ``mort_total_mult``; at 1.75 the expected sojourn in *partielle* entered
    at age 82 is 3.14 years, the same order as the 29.2-month mean duration of APA
    receipt across all GIRs.  No impaired-life table for either French dependence state
    exists in any retrieved source.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** mort_partial_mult           # noqa: F821


def mort_rate_partial_mth(t):
    """q_P(t) = 1 - (1 - mort_rate)^(k_P/12): monthly *partielle* mortality **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (mort_partial_mult / 12.0)  # noqa: F821


def mort_rate_total(t):
    """The annual mortality of a life in *dépendance totale* at the attained age.

    ``1 - (1 - mort_rate)^k`` with ``k = mort_total_mult`` **[std]**.  0.23841 at age 85
    against 0.06179 healthy, and 0.216 at 84 against 0.055 — the gap that makes flat
    state mortality this product's largest available error.  ``k`` is **calibrated**:
    see :func:`sojourn_total`.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** mort_total_mult             # noqa: F821


def mort_rate_total_mth(t):
    """q_T(t) = 1 - (1 - mort_rate)^(k_T/12): monthly *totale* mortality **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (mort_total_mult / 12.0)    # noqa: F821


def mort_force_at(x):
    """mu_H at an **exact**, possibly fractional, age x.

    Log-linear in age between the integer ages of ``mort_table.csv``, which reproduces
    the shipped Gompertz force exactly, since a Gompertz force is exponential in age.
    Only the two sojourn calibrations use it: the projection itself reads the force at
    integer attained ages through :func:`mort_force`.
    """
    tbl = data.mort_table()                                          # noqa: F821
    lo = int(math.floor(x))                                          # noqa: F821
    hi = lo + 1
    ages = [a for s, a in tbl.index if s == sex()]
    top = max(ages)
    if lo >= top:
        return float("inf")
    q_lo = float(tbl.loc[(sex(), lo), "mort_rate"])
    q_hi = float(tbl.loc[(sex(), min(hi, top)), "mort_rate"])
    if q_lo >= 1.0 or q_hi >= 1.0:
        return float("inf")
    m_lo = -math.log(1.0 - q_lo)                                     # noqa: F821
    m_hi = -math.log(1.0 - q_hi)                                     # noqa: F821
    return m_lo * (m_hi / m_lo) ** (x - lo)


def lapse_rate_base(t):
    """The table annual lapse rate in month t **[std]**, before the premium shock.

    8 / 6 / 5 / 4 / 3 percent by policy band.  No French LTC persistency study is
    public; the table's only anchor is that the individual book fell 9.9% in 2024 on
    28,400 new subscribers, so gross exits — deaths, claim entries and lapses together —
    ran at roughly 11% of the opening portfolio, and a 3-8% lapse table leaves the
    balance for mortality and incidence.  Policy years beyond the table take its last
    row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(policy_year(t), int(tbl.index.max())),
                         "lapse_rate"])


def revision_lapse_factor(t):
    """M_rev(y): the premium-shock lapse multiplier **[std]**; 1.0 in the base run.

    ``1 + revision_lapse_slope x max(0, r(y) - revision_lapse_threshold)``.  The member
    may refuse a tariff revision by resiliating within two months of notification, with a
    possible *mise en réduction* at the same date, so a revision at the 10% cap gives
    1.24.  It is off in the base run because the shipped revision path never exceeds
    1.5%, and it is the only place a projected repricing feeds back into the block.
    """
    return 1.0 + revision_lapse_slope * max(                         # noqa: F821
        0.0, revision_rate(t) - revision_lapse_threshold)            # noqa: F821


def lapse_rate(t):
    """w(t): the **annual** lapse rate out of the autonomous ledger in month t.

    Applied to :func:`pols_auto` **only**.  A recognised life pays no premium and a
    reduced membership pays none either, so neither can lapse for non-payment, and with
    no surrender value there is nothing to surrender for — a lapse here is genuinely a
    decision to walk away from everything.
    """
    return min(1.0, lapse_rate_base(t) * revision_lapse_factor(t))


def lapse_rate_mth(t):
    """w(t) monthly = 1 - (1 - lapse_rate)^(1/12) **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def aggravation_rate_mth():
    """i_Am = 1 - exp(-i_A/12): the monthly aggravation probability **[std]**.

    Flat in age, and **not an independent input**: the prevalence identity ties it to
    :func:`inc_rate_total`, so raising it lowers the direct-to-*totale* incidence.  There
    is no public transition law — the only retrieved actuarial reference models no such
    transition at all and prices two separate guarantees instead — and the contracts
    themselves do provide for deterioration, so this model carries it and states the cost
    of the missing law.
    """
    return 1.0 - math.exp(-aggravation_rate / 12.0)                  # noqa: F821


def recovery_rate_mth():
    """The monthly probability of returning to autonomy; **zero in the base run**.

    Contractually the *rente* stops on improvement out of a covered state, and one
    retrieved *notice* lets the level move in either direction.  The only retrieved
    actuarial reference nonetheless sets the probability of return to autonomy to zero,
    and so does this model — as a **named input held at zero**, wired into the ledger
    roll and into :func:`pols_recovery`, not as an omission.  Its direction of error is
    one-sided: claims are overstated, by an amount no retrieved source quantifies.
    """
    return 1.0 - math.exp(-recovery_rate / 12.0)                     # noqa: F821


def carence_factor(t):
    """S(t): the share of causes whose *carence* has already expired at month t.

    Read from the **[std]** cause mix against the model point's own three *carence*
    lengths: 0.10 in policy year 1, 0.65 in policy years 2 and 3, 1.00 thereafter on the
    base cell — the ``S1 <= S2 <= S3 <= S4 = 100%`` shape the actuarial reference asks
    for.  What it multiplies is the **claim**, not the decrement: a life whose dependence
    arises from a cause still inside its *carence* leaves the in-force ledger exactly as
    a covered one does, and takes :func:`refunds_carence` with it.
    """
    tbl = data.cause_mix_table()                                     # noqa: F821
    return float(sum(tbl.loc[c, "share"] for c in tbl.index
                     if carence_months(c) <= t))


def aggravation_carence(t):
    """The share of aggravations recognised at month t.

    1.0 on a ``total_and_partial`` cell, where the *carence* was already applied at
    first recognition into *partielle*.  On a ``total_only`` cell the aggravation **is**
    the first recognition of a covered state, so it carries the *carence* itself.
    """
    return 1.0 if cover_partial() else carence_factor(t)


# --- prevalence and the incidence identity ---

def prev_param(name):
    """One parameter of the APA-prevalence logistic for this model point's sex.

    ``prev_ceil``, ``prev_beta`` or ``prev_x_mid``.  The two slope parameters are pinned
    to sourced DREES rates; ``prev_ceil`` is **[std]**, unidentified by a two-anchor fit,
    and it governs the tail — where 65% of this product's lifetime claims fall.
    """
    return float(data.prevalence_table().loc[(sex(), name), "value"])  # noqa: F821


def prev_rate(t):
    """prev(x): APA prevalence at the attained age in month t.

    ``prev_ceil / (1 + exp(-beta (x - x_mid)))``.  This is a **prevalence of receipt of a
    public allowance**, not an incidence and not the insurer's definition of dependence.
    Multiplying it by a *rente* amount as though it were an annual claim frequency is the
    error that dominates this product; :func:`severity_share` and
    :func:`inc_rate_partial` are the two explicit steps that stand between them.

    APA is not available below age 60, so the curve has **no anchor at all** under 60 and
    every entry age below 60 runs on pure extrapolation.
    """
    return prev_param("prev_ceil") / (
        1.0 + math.exp(-prev_param("prev_beta")                      # noqa: F821
                       * (age(t) - prev_param("prev_x_mid"))))


def prev_slope(t):
    """prev'(x) = beta prev (1 - prev / prev_ceil): the prevalence slope in age.

    A **rate per year**, which is why it can be added to a prevalence times a force of
    mortality in the identity below.  The dimensional check this enforces is the one
    that catches the product's dominant error.
    """
    p = prev_rate(t)
    return prev_param("prev_beta") * p * (1.0 - p / prev_param("prev_ceil"))


def severity_share(kind):
    """s_P or s_T: the share of APA prevalence read as one insured state.

    ``"partial"`` or ``"total"``, keyed by the contract's :func:`trigger_grid`.  Public
    prevalence is APA take-up on GIR 1-4 and insurer definitions are deliberately
    stricter — the *notice* says the insurer is not bound by the decisions of the public
    services.  Two sourced anchors bound the haircut on the base grid and neither pins
    it: the GIR 1-2 share of APA beneficiaries, 34.9%, and the market's own count of
    *rentes* in payment against lives covered, about 0.44 against the shipped 0.45.

    Holding the shares constant across ages is a standardization with a known direction
    of error: severity mix worsens with age, so the model **understates** *totale*
    prevalence at old ages and overstates it at young ones.
    """
    if kind not in ("partial", "total"):
        raise ValueError("invalid kind")
    return float(data.severity_share_table().loc[                    # noqa: F821
        trigger_grid(), "share_" + kind])


def prev_partial(t):
    """pi_P = s_P prev(x): the proportion of living lives in insured *partielle*."""
    return severity_share("partial") * prev_rate(t)


def prev_total(t):
    """pi_T = s_T prev(x): the proportion of living lives in insured *totale*."""
    return severity_share("total") * prev_rate(t)


def mort_force_avg(t):
    """mubar: the mortality force averaged over the three living states.

    ``mu_H pi_H + mu_P pi_P + mu_T pi_T``.  It appears in the incidence identity because
    the state proportions are proportions of a **living** population, which is itself
    being drained at this rate.
    """
    pi_p, pi_t = prev_partial(t), prev_total(t)
    mu = mort_force(t)
    return mu * ((1.0 - pi_p - pi_t)
                 + mort_partial_mult * pi_p                          # noqa: F821
                 + mort_total_mult * pi_t)                           # noqa: F821


def inc_rate_partial(t):
    """i_P(x): the annual force of entry into *dépendance partielle* from autonomy.

    Derived, not assumed.  Differentiating the state proportions along the age axis
    gives the **identity**

        ``i_P = [pi_P' + (i_A + mu_P) pi_P - pi_P mubar] / pi_H``

    with ``pi_P' = s_P beta prev (1 - prev / prev_ceil)``.  The mortality terms are not
    refinements: dropping them understates incidence, because a rising prevalence is
    being fed against a dependent population that is simultaneously draining at its own
    excess mortality.  Floored at zero **[std]** — the identity can go negative at
    extreme ages, where the prevalence slope flattens while excess mortality does not.
    The floor never binds on the female base cell — the rate is still 0.0040 at attained
    age 109 — and binds at attained age 109 on the male basis.
    """
    pi_p, pi_t = prev_partial(t), prev_total(t)
    pi_h = 1.0 - pi_p - pi_t
    num = (severity_share("partial") * prev_slope(t)
           + (aggravation_rate + mort_partial_mult * mort_force(t))  # noqa: F821
           * pi_p - pi_p * mort_force_avg(t))
    return max(0.0, num / pi_h)


def inc_rate_partial_mth(t):
    """i_Pm(t) = 1 - exp(-i_P/12): the monthly entry probability into *partielle*."""
    return 1.0 - math.exp(-inc_rate_partial(t) / 12.0)               # noqa: F821


def inc_rate_total(t):
    """i_T(x): the annual force of entry into *dépendance totale* direct from autonomy.

    The second half of the same identity,

        ``i_T = [pi_T' - i_A pi_P + mu_T pi_T - pi_T mubar] / pi_H``

    and the ``- i_A pi_P`` term is why ``aggravation_rate`` and this rate are **not
    independent inputs**: the stock of *totale* lives is pinned by the assumed
    prevalence, so aggravations arriving from *partielle* displace direct entries one for
    one.  Adding an aggravation rate without re-deriving this one double-counts entries
    into *totale*.

    It overtakes :func:`inc_rate_partial` between ages 80 and 85 — the severity mix
    worsening with age, arriving through the mortality terms of the identity rather than
    through the constant severity shares, which cannot produce it.  Floored at zero
    **[std]**.
    """
    pi_p, pi_t = prev_partial(t), prev_total(t)
    pi_h = 1.0 - pi_p - pi_t
    num = (severity_share("total") * prev_slope(t)
           - aggravation_rate * pi_p                                 # noqa: F821
           + mort_total_mult * mort_force(t) * pi_t                  # noqa: F821
           - pi_t * mort_force_avg(t))
    return max(0.0, num / pi_h)


def inc_rate_total_mth(t):
    """i_Tm(t) = 1 - exp(-i_T/12): the monthly entry probability into *totale*."""
    return 1.0 - math.exp(-inc_rate_total(t) / 12.0)                 # noqa: F821


# --- the five ledgers ---

def pols_auto(t):
    """auto(t): the autonomous, premium-paying population at the start of month t.

    ``pols_if_init()`` at ``t = 0`` on an ``autonomous`` cell and zero on every other
    kind, then survivors of mortality, of lapse and of incidence among the survivors,
    plus any returns to autonomy.

    Note what is **absent** from the recursion: :func:`carence_factor`.  A *carence*
    claim terminates the membership rather than deferring it, so the blocked lives leave
    the in-force ledger exactly as the covered ones do and ``auto(t + 1)`` does not
    depend on ``S(t)`` at all.

    The guard lets the ledger answer **one month past the frame**, at ``t = proj_len()``,
    which is deliberate and not a leftover of a 1-based index: the population identity
    :func:`check_states` holds at the **start** of a month, and the last projected month,
    ``t = proj_len() - 1``, has one.  :func:`pols_red` and :func:`red_rente_value` carry
    the same guard for the same reason.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init() if status() == "autonomous" else 0.0
    base = pols_base(t - 1)
    stay = base * (1.0 - inc_rate_partial_mth(t - 1)
                   - inc_rate_total_mth(t - 1))
    return stay + pols_recovery(t - 1)


def pols_surv(t):
    """surv(t): autonomous lives surviving the month's mortality, before lapse."""
    return pols_auto(t) * (1.0 - mort_rate_mth(t))


def pols_lapse(t):
    """lapse(t): lapses out of the autonomous ledger at the end of month t.

    Taken from the survivors of mortality.  Pays **nothing**: there is no surrender value
    at any duration and the design is *fonds perdu*, so a lapse before the qualifying
    period destroys the whole accumulated value.  From the qualifying period the same
    flow becomes :func:`pols_reduction` instead of an exit.
    """
    return pols_surv(t) * lapse_rate_mth(t)


def pols_reduction(t):
    """The lapses of month t that become a *mise en réduction* rather than an exit.

    Zero until the membership has :func:`reduction_qualifying_years` full years of
    premiums behind it, and the whole of :func:`pols_lapse` thereafter.  It is the
    **second decrement, not the absence of one**.
    """
    if years_premiums_paid(t) < reduction_qualifying_years():
        return 0.0
    return pols_lapse(t)


def pols_lapse_exit(t):
    """The lapses of month t that leave the model outright, with no value at all."""
    return pols_lapse(t) - pols_reduction(t)


def pols_base(t):
    """base(t): autonomous lives exposed to incidence, after mortality and lapse.

    The notes' order out of the autonomous state is **mortality, then lapse, then
    incidence among the survivors** **[std]**.
    """
    return pols_surv(t) - pols_lapse(t)


def pols_entry_partial(t):
    """n_P(t): recognised entrants into *dépendance partielle* at the end of month t.

    ``base(t) i_Pm(t) S(t)``.  On a ``total_only`` cell the *carence* does not enter
    here, because *partielle* is not a recognised state on that cell: the whole
    incidence flow moves into the ledger and the *carence* attaches later, at the
    aggravation that first recognises a covered state.
    """
    s = carence_factor(t) if cover_partial() else 1.0
    return pols_base(t) * inc_rate_partial_mth(t) * s


def pols_entry_total(t):
    """n_T(t): recognised entrants into *dépendance totale* direct from autonomy.

    ``base(t) i_Tm(t) S(t)``.
    """
    return pols_base(t) * inc_rate_total_mth(t) * carence_factor(t)


def pols_entry_total_red(t):
    """n_Tr(t): entrants into *totale* out of the **reduced** ledger.

    The reduced cover is *dépendance totale* only, so there is no partial entry from it,
    and it carries **no *carence***: eight full years of premiums have been paid.  These
    lives take the reduced *rente* they froze at the reduction date and **not** the
    *capital d'équipement*, which a reduced membership has lost.
    """
    return pols_red(t) * (1.0 - mort_rate_mth(t)) * inc_rate_total_mth(t)


def pols_aggravation(t):
    """n_A(t): the gross flow *partielle* to *totale* at the end of month t.

    ``pols_part(t) (1 - q_P(t)) (1 - recovery) i_Am``, taken from the survivors of
    mortality and of recovery.  On a ``total_and_partial`` cell every one of them is
    recognised already, and the cohort keeps its duration index so it does **not** serve
    a second *franchise*.
    """
    return (pols_part(t) * (1.0 - mort_rate_partial_mth(t))
            * (1.0 - recovery_rate_mth()) * aggravation_rate_mth())


def pols_aggravation_recog(t):
    """The aggravations of month t that are recognised, after the *carence*."""
    return pols_aggravation(t) * aggravation_carence(t)


def pols_carence_exit(t):
    """carence_exit(t): memberships terminated because a *carence* was still running.

    A *carence* claim is a **decrement with a cash flow**, not a suppressed claim:
    modelling the *carence* as a multiplier on incidence alone leaves the terminated
    membership in force and omits the refund, and both errors run the same way — they
    overstate the liability at the front end and the premium income behind it.  See
    :func:`refunds_carence` for the cash flow.
    """
    blocked = 1.0 - carence_factor(t)
    out = pols_base(t) * inc_rate_total_mth(t) * blocked
    if cover_partial():
        out += pols_base(t) * inc_rate_partial_mth(t) * blocked
    else:
        out += pols_aggravation(t) * blocked
    return out


def pols_recognition(t):
    """First recognitions of a covered state at the end of month t.

    ``n_P + n_T + n_Tr`` on a ``total_and_partial`` cell, and the recognised
    aggravations in place of ``n_P`` on a ``total_only`` one.  It is what the claim
    adjudication expense rides on — a real, medically supervised process with a
    45-working-day deadline and an arbitration route.
    """
    out = pols_entry_total(t) + pols_entry_total_red(t)
    if cover_partial():
        return out + pols_entry_partial(t)
    return out + pols_aggravation_recog(t)


def pols_capital_claims(t):
    """The recognitions of month t that carry the *capital d'équipement*.

    :func:`pols_recognition` less the entrants out of the reduced ledger, which have lost
    the option.  It is paid **once per membership, not once per state**: a life that
    takes it on entering *partielle* takes nothing further on aggravating, which is why
    an aggravation appears here only on a ``total_only`` cell, where it is the first
    recognition.
    """
    return pols_recognition(t) - pols_entry_total_red(t)


def pols_red(t):
    """red(t): the paid-up population on a reduced *rente totale* at the start of month t.

    No premium, *rente totale* only, no *capital*, no assistance and no further
    *revalorisation* of the guarantee.  It is fed by :func:`pols_reduction` and drained
    by mortality and by entry into *totale*, and it never lapses, because there is no
    premium left to miss.

    **This is the ledger a naive model omits**, and omitting it turns every lapse from
    the qualifying period into a full release of liability.

    Answers one month past the frame, at ``t = proj_len()``, for the reason given under
    :func:`pols_auto`.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init() if status() == "reduced" else 0.0
    prev = pols_red(t - 1)
    surv = prev * (1.0 - mort_rate_mth(t - 1))
    return (surv - pols_entry_total_red(t - 1) + pols_reduction(t - 1)
            + pols_recovery_red(t - 1))


def red_rente_value(t):
    """The reduced ledger's population **times** the frozen *rente* it carries.

    Carried as a value rather than as a per-cohort amount: reductions happen in every
    month from the qualifying period and each freezes ``G(y) c(n)`` at its own date, so
    the ledger holds a distribution of amounts.  Tracking the probability-weighted total
    is **exact in expectation**, because incidence does not depend on the amount, and it
    is what the notes license an implementation to do instead of carrying a
    per-reduction-cohort amount.

    The frozen amount is never revalued **before** claim; it becomes a *rente en service*
    and starts moving at ``reval_rente`` only once it is in payment, which happens on the
    fourth vector of :func:`dep_cohorts`.

    Answers one month past the frame, at ``t = proj_len()``, for the reason given under
    :func:`pols_auto`.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        if status() != "reduced":
            return 0.0
        return (pols_if_init() * rente_total_mth()
                * reduction_coeff(years_paid()))
    carried = (red_rente_value(t - 1) * (1.0 - mort_rate_mth(t - 1))
               * (1.0 - inc_rate_total_mth(t - 1)))
    fresh = (pols_reduction(t - 1) * rente_total_pp(t - 1)
             * reduction_coeff(years_premiums_paid(t - 1)))
    return carried + fresh + red_value_recovered(t - 1)


def red_rente_pp(t):
    """The mean frozen reduced *rente* carried by the reduced ledger at month t.

    ``red_rente_value(t) / pols_red(t)``, and zero on an empty ledger.  It is the amount
    a life entering *totale* out of the reduced ledger takes into payment.
    """
    p = pols_red(t)
    return red_rente_value(t) / p if p > 0.0 else 0.0


def dep_cohorts(t):
    """The four dependent-ledger vectors at the start of month t, as lists.

    ``(partielle, totale, totale-on-a-reduced-rente, the value of that third ledger)``.
    Element ``z - 1`` of each is the state at duration ``z``, for
    ``z = 1 ... cohort_len(t)``; the fourth is a **population times amount** rather than
    a population, because the reduced *rentes* are frozen individually at each reduction
    date and cannot be recovered from the policy year the way the other amounts can.

    The model's only list-valued cells, and the reason is cost: four two-argument
    recursions would be ``4 proj_len() max_dur()`` separate cells — nearly a
    million on the base cell — where this is ``proj_len()`` cells with a loop inside.
    :func:`pols_part_dur` and its siblings read elements out of it, so the notes'
    two-dimensional objects are still addressable by name.

    At ``t = 0`` the vectors are the seeded state: all zeros on an ``autonomous`` or
    ``reduced`` cell, and ``pols_if_init()`` at cohort ``claim_duration_months() + 1`` on
    an in-force claim cell.  Thereafter cohort 1 is the previous month's recognitions and
    every other cohort is the previous cohort survived one month, aggravated and — at an
    anniversary — revalued.  A new list is built on each step rather than the previous
    one mutated, so holding a returned list cannot corrupt the cache.
    """
    n = cohort_len(t)
    part = [0.0] * n
    tot = [0.0] * n
    totr = [0.0] * n
    val = [0.0] * n
    if t <= 0:
        z0 = seed_dur()
        if z0 and z0 <= n:
            if status() == "partial":
                part[z0 - 1] = pols_if_init()
            else:
                tot[z0 - 1] = pols_if_init()
        return part, tot, totr, val
    prev_p, prev_t, prev_tr, prev_v = dep_cohorts(t - 1)
    surv_p = (1.0 - mort_rate_partial_mth(t - 1)) * (1.0 - recovery_rate_mth())
    surv_t = (1.0 - mort_rate_total_mth(t - 1)) * (1.0 - recovery_rate_mth())
    ia = aggravation_rate_mth()
    recog = aggravation_carence(t - 1)
    restart = not cover_partial()
    fresh = 0.0
    for z in range(1, min(len(prev_p), n - 1) + 1):
        ps = prev_p[z - 1] * surv_p
        na = ps * ia
        part[z] = ps - na
        carried = prev_t[z - 1] * surv_t
        if restart:
            tot[z] = carried
            fresh += na * recog
        else:
            tot[z] = carried + na * recog
        totr[z] = prev_tr[z - 1] * surv_t
        val[z] = prev_v[z - 1] * surv_t
    part[0] = pols_entry_partial(t - 1)
    tot[0] = pols_entry_total(t - 1) + fresh
    totr[0] = pols_entry_total_red(t - 1)
    val[0] = totr[0] * red_rente_pp(t - 1)
    if t % 12 == 0:
        g = 1.0 + reval_rente                                        # noqa: F821
        val = [v * g for v in val]
    return part, tot, totr, val


def pols_part_dur(t, z):
    """pols_part(t, z): the population in *partielle* at duration z at the start of t."""
    v = dep_cohorts(t)[0]
    return v[z - 1] if 1 <= z <= len(v) else 0.0


def pols_tot_dur(t, z):
    """pols_tot(t, z): the population in *totale* at duration z at the start of t."""
    v = dep_cohorts(t)[1]
    return v[z - 1] if 1 <= z <= len(v) else 0.0


def pols_totr_dur(t, z):
    """pols_totr(t, z): the reduced-rente *totale* population at duration z."""
    v = dep_cohorts(t)[2]
    return v[z - 1] if 1 <= z <= len(v) else 0.0


def pols_part(t):
    """The whole population in *dépendance partielle* at the start of month t."""
    return sum(dep_cohorts(t)[0])


def pols_tot(t):
    """The whole population in *dépendance totale* on a full *rente*, at the start of t."""
    return sum(dep_cohorts(t)[1])


def pols_totr(t):
    """The whole population in *totale* on a **reduced** *rente*, at the start of t.

    A separate ledger from :func:`pols_tot` because these lives entered from
    :func:`pols_red` and carry a frozen reduced amount rather than the policy year's
    guarantee.
    """
    return sum(dep_cohorts(t)[2])


def totr_rente_value(t):
    """The reduced-rente *totale* ledger's population times the amount it is paid."""
    return sum(dep_cohorts(t)[3])


def pols_recovery(t):
    """Returns to autonomy out of the two full-cover dependent ledgers; zero in the base.

    Taken from the survivors of the month's mortality.  See :func:`recovery_rate_mth` for
    why this is a named input held at zero rather than an omission.
    """
    r = recovery_rate_mth()
    if r == 0.0:
        return 0.0
    return (pols_part(t) * (1.0 - mort_rate_partial_mth(t))
            + pols_tot(t) * (1.0 - mort_rate_total_mth(t))) * r


def pols_recovery_red(t):
    """Returns out of the reduced-rente *totale* ledger; zero in the base run.

    They go back to :func:`pols_red` and not to :func:`pols_auto`, because a paid-up
    membership that recovers is still paid up.
    """
    r = recovery_rate_mth()
    if r == 0.0:
        return 0.0
    return pols_totr(t) * (1.0 - mort_rate_total_mth(t)) * r


def red_value_recovered(t):
    """The frozen-*rente* value returning to the reduced ledger on recovery.

    Zero in the base run.  A recovering life takes back the amount it was **being paid**
    rather than the amount it originally froze **[std]**: the value ledger does not
    carry the two separately, and the difference is immaterial while
    ``recovery_rate`` is zero.
    """
    r = recovery_rate_mth()
    if r == 0.0:
        return 0.0
    return totr_rente_value(t) * (1.0 - mort_rate_total_mth(t)) * r


def pols_if(t):
    """The number of policies in force at the start of month t: every ledger added.

    ``pols_auto + pols_red + pols_part + pols_tot + pols_totr``.  It is the weight on
    maintenance expense and the count a reader of ``result_cf()`` reconciles the rest of
    the row against.  It is **not** the weight on premium income, which is
    :func:`pols_prem`.
    """
    return (pols_auto(t) + pols_red(t) + pols_part(t) + pols_tot(t)
            + pols_totr(t))


def pols_prem(t):
    """The population actually paying premium at the start of month t.

    :func:`pols_auto` on every cell whose *partielle* is a covered state, because a
    recognised life is exonerated and a reduced membership is paid up.  On a
    ``total_only`` cell the *partielle* ledger is **not** recognised, so those lives keep
    paying and are added here.

    *Exonération* runs from **recognition**, not from the start of *rente* payment, so a
    life inside the three-month *franchise* pays no premium and receives no *rente*.
    Carrying the *franchise* the way an income-protection deferred period is carried —
    premium-paying, benefit-free — overstates premium income.
    """
    if cover_partial():
        return pols_auto(t)
    return pols_auto(t) + pols_part(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside month t.

    ``"BEF_DECR"``
        the start of the month, before any transition; the same number as
        :func:`pols_if`.

    ``"AFT_DECR"``
        the end of the month, once deaths, outright lapses and the
        *carence* terminations have been taken.  Equal to
        ``pols_if(t + 1)``.

    The intermediate points of the other models have no single-population meaning here,
    because five ledgers are moving at once; the ledgers themselves expose them.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DECR":
        if t < 0 or t >= proj_len():
            return 0.0
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths at the end of month t, from all five ledgers.

    Three different rates on the same clock: the healthy rate on the autonomous and
    reduced ledgers, ``q_P`` on *partielle*, ``q_T`` on both *totale* ledgers.  It is
    exact even though the dependent ledgers are cohort-indexed, because the mortality
    rates do not depend on the duration.
    """
    return ((pols_auto(t) + pols_red(t)) * mort_rate_mth(t)
            + pols_part(t) * mort_rate_partial_mth(t)
            + (pols_tot(t) + pols_totr(t)) * mort_rate_total_mth(t))


def pols_dead_cum(t):
    """Cumulative deaths from every ledger before the start of month t."""
    if t <= 0:
        return 0.0
    return pols_dead_cum(t - 1) + pols_death(t - 1)


def pols_lapse_cum(t):
    """Cumulative outright lapses before the start of month t.

    Lapses that became a *mise en réduction* are **not** here: they never left.
    """
    if t <= 0:
        return 0.0
    return pols_lapse_cum(t - 1) + pols_lapse_exit(t - 1)


def pols_carence_cum(t):
    """Cumulative memberships terminated by the *carence* before the start of month t."""
    if t <= 0:
        return 0.0
    return pols_carence_cum(t - 1) + pols_carence_exit(t - 1)


# --- cash flows ---

def premiums(t):
    """Premium income at the start of month t, an inflow.

    ``P(y) x premium_months() x pols_prem(t)`` when an instalment falls due.  Carried on
    :func:`pols_prem` and **never** on :func:`pols_if`: lives in a recognised state are
    exonerated and reduced lives are paid up, so charging premium to the whole in-force
    block overstates income by the whole of both bands.
    """
    if not premium_due(t):
        return 0.0
    return premium_mth_pp(t) * premium_months() * pols_prem(t)


def instalments(t):
    """The number of *rente* instalments paid at the end of month t.

    The population of every ledger past its *franchise* that survived the month.  It
    drives the per-instalment handling expense, which pays for the annual proof of life
    and of the persisting state.
    """
    part, tot, totr, _ = dep_cohorts(t)
    s_p = (1.0 - mort_rate_partial_mth(t)) if cover_partial() else 0.0
    s_t = 1.0 - mort_rate_total_mth(t)
    out = 0.0
    for z in range(franchise_months() + 1, len(part) + 1):
        out += part[z - 1] * s_p + (tot[z - 1] + totr[z - 1]) * s_t
    return out


def claims(t, kind=None):
    """Benefit outgo at the end of month t, by kind; the total when kind is omitted.

    ``"RENTE"``
        the monthly *rente*, paid **in arrears** to the cohorts past their
        *franchise* that survived the month.  Three ledgers contribute at
        three amounts: *partielle* at ``rho`` times its vintage's
        indexed guarantee, *totale* at the whole of it, and the
        reduced-rente ledger at its own frozen amounts.

    ``"CAPITAL"``
        the *capital d'équipement*, paid once per membership on
        :func:`pols_capital_claims`.

    ``"LAPSE"``
        zero, in every month of every model point.  **There is no
        surrender value at any duration**, and that zero is a product fact
        worth publishing rather than leaving to be inferred from a missing
        column.

    There is deliberately **no** ``"DEATH"`` kind: this composite carries no death
    benefit at all, and the optional *capital décès* rider is out of scope.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("RENTE", "CAPITAL", "LAPSE"))
    if kind == "RENTE":
        part, tot, totr, val = dep_cohorts(t)
        s_p = 1.0 - mort_rate_partial_mth(t)
        s_t = 1.0 - mort_rate_total_mth(t)
        rho = partial_ratio_paid()
        amounts = {}
        out = 0.0
        for z in range(franchise_months() + 1, len(part) + 1):
            p, o, v = part[z - 1], tot[z - 1], val[z - 1]
            if p == 0.0 and o == 0.0 and v == 0.0:
                continue
            y_e = max(1, policy_year(t - z))
            a = amounts.get(y_e)
            if a is None:
                a = rente_pay_pp(t, z)
                amounts[y_e] = a
            out += (rho * a * p * s_p + a * o * s_t + v * s_t)
        return out
    if kind == "CAPITAL":
        return capital_pp(t) * pols_capital_claims(t)
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def refunds_carence(t):
    """The premiums returned when a *carence* terminates a membership at month t.

    ``pols_carence_exit(t) x cum_prem_pp(t)``.  It is **not a claim** — it is a return of
    premium, and it belongs on its own line because it is the only cash flow that runs
    backwards through the *carence*.  In policy year 1 of the base cell it is 0.6141 EUR,
    three quarters of the year's *rente* and *capital* claims combined: during the
    *carence* the largest benefit-side cash flow is a premium refund.
    """
    return pols_carence_exit(t) * cum_prem_pp(t)


def expenses(t):
    """Maintenance, assistance and acquisition expense at the start of month t **[std]**.

    3.00 EUR a month on every policy in force plus 1.20 EUR a month on every policy in
    force **except the reduced ones**, both inflating at 1.5% a year, plus 150 EUR of
    acquisition at ``t = 0``.  There is **no observed range for any expense level on this
    product**: no retrieved document discloses an expense assumption, a loading or a
    commission rate.  Only the structure is sourced — *prestations d'assistance* end on
    *mise en réduction*, which is why the second base excludes :func:`pols_red`.

    The two per-event claim expenses are on :func:`claim_expenses`, published as a
    separate ``result_cf()`` column.
    """
    f = inflation_factor(t)
    out = (expense_maint * f * pols_if(t)                            # noqa: F821
           + expense_assist * f * (pols_if(t) - pols_red(t)))        # noqa: F821
    if t == 0:
        out += expense_acq                                           # noqa: F821
    return out


def claim_expenses(t):
    """Claim adjudication and *rente* handling expense at the end of month t **[std]**.

    250 EUR per first recognition and 10 EUR per instalment paid, both flat rather than
    inflating **[std]**.  The adjudication load is an order of magnitude above the
    per-instalment one because recognition is a real, medically supervised process — a
    medical attestation completed with the treating doctor, a *médecin-conseil* ruling
    within 45 working days of a complete file, and a medical arbitration route — while
    the handling load pays for an annual proof of life and of the persisting state.
    """
    return (expense_claim_adj * pols_recognition(t)                  # noqa: F821
            + expense_rente * instalments(t))                        # noqa: F821


def net_cf(t):
    """The net cash flow of month t, insurer perspective, **income positive**.

    ``premiums - claims - refunds_carence - expenses - claim_expenses``.  The notes' own
    sign and the library-wide one, so there is no outgo-positive ``liability_cf``
    companion.  Undiscounted: a market-consistent valuation applies EIOPA's monthly
    risk-free term structure to exactly this stream, and that is a layer above this
    model.
    """
    return (premiums(t) - claims(t) - refunds_carence(t)
            - expenses(t) - claim_expenses(t))


# --- calibration companions ---

def sojourn_total(x0):
    """The expected sojourn in *dépendance totale*, in years, entered at exact age x0.

    Mortality at ``mort_total_mult`` and no other decrement, in monthly steps, on a
    **continuously advancing exact age** — which is the calibration convention and not
    the projection's own age basis, where the attained age steps once a policy year.

    This is what calibrates ``mort_total_mult``: 2.9989 years from exact age 84 at 4.27,
    against the mean duration of receipt of about three years the CCSF reports for heavy
    dependents at a mean age at onset of 84 for women.  At 2.75 the same calculation
    gives 4.19 years and at 3.50, 3.50 — the sojourn is far more sensitive to the
    multiple than a first look suggests, which is why this is a calibration and not a
    pick.
    """
    p, s, m = 1.0, 0.0, 0
    while p > 1e-15:
        x = x0 + m / 12.0
        if x >= terminal_age:                                        # noqa: F821
            break
        p *= math.exp(-mort_total_mult * mort_force_at(x) / 12.0)    # noqa: F821
        s += p
        m += 1
    return s / 12.0


def sojourn_partial(x0):
    """The expected sojourn in *dépendance partielle*, in years, entered at exact age x0.

    Mortality at ``mort_partial_mult`` **and** aggravation at ``aggravation_rate``, since
    a life leaves *partielle* by dying or by deteriorating.  Same continuous-age
    convention as :func:`sojourn_total`.

    3.14 years from exact age 82 on the shipped basis — the same order of magnitude as
    the 29.2-month mean duration of APA receipt across all GIRs, which is the only
    comparator there is.  ``mort_partial_mult`` is **not** calibrated to it: it has no
    anchor at all, and this is a sanity check rather than a fit.
    """
    p, s, m = 1.0, 0.0, 0
    ia = aggravation_rate_mth()
    while p > 1e-15:
        x = x0 + m / 12.0
        if x >= terminal_age:                                        # noqa: F821
            break
        p *= math.exp(-mort_partial_mult * mort_force_at(x) / 12.0)  # noqa: F821
        p *= (1.0 - ia)
        s += p
        m += 1
    return s / 12.0


# --- checks ---

def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1)`` less deaths from all five ledgers, less the lapses that
    left outright, less the memberships the *carence* terminated.  Three flows are
    deliberately **absent** because they move lives between ledgers rather than out of
    the policy count: incidence, aggravation, and the *mise en réduction* — which is the
    whole point of running the check on the sum rather than on any one ledger.  A model
    that treated a qualifying lapse as an exit would fail this check, not merely
    understate the liability.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t)
            - pols_lapse_exit(t) - pols_carence_exit(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the
    signed residual of the month that failed.
    """
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return all(abs(check_pols_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_states_resid(t):
    """The five-ledger population identity residual at the start of month t; zero.

    ``pols_if + cumulative deaths + cumulative outright lapses + cumulative carence
    terminations`` must equal the starting population in every month.  This is the check
    that catches a leak in the cohort machinery: a mis-indexed duration shift drops
    population out of a dependent ledger with no corresponding exit, and nothing else in
    the model would notice.
    """
    return (pols_if(t) + pols_dead_cum(t) + pols_lapse_cum(t)
            + pols_carence_cum(t) - pols_if_init())


def check_states():
    """True when the five-ledger population identity holds in every projected month.

    No argument, one bool over all t, the library-wide shape of a ``check_*`` cells;
    :func:`check_states_resid` gives the signed residual of the month that failed.  The
    sweep runs ``t = 0 ... proj_len()``, one point past the frame, because the identity
    holds at the **start** of a month and the last projected month, ``proj_len() - 1``,
    still has one.
    """
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return all(abs(check_states_resid(t)) <= tol
               for t in range(proj_len() + 1))


def check_part_roll_fwd_resid(t):
    """The *partielle* ledger's aggregate roll-forward residual in month t; zero.

    ``pols_part(t+1)`` against ``pols_part(t) (1 - q_P)(1 - recovery)(1 - i_Am) + n_P``,
    which is the same population computed **without** the cohort machinery.  It is a real
    check and not an identity: the two sides are built differently, so a duration shift
    that dropped or duplicated a cohort would show up here even though the total policy
    count still closed.
    """
    expected = (pols_part(t) * (1.0 - mort_rate_partial_mth(t))
                * (1.0 - recovery_rate_mth())
                * (1.0 - aggravation_rate_mth())
                + pols_entry_partial(t))
    return pols_part(t + 1) - expected


def check_part_roll_fwd():
    """True when the *partielle* ledger closes against its aggregate recursion."""
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return all(abs(check_part_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_tot_roll_fwd_resid(t):
    """The two *totale* ledgers' aggregate roll-forward residual in month t; zero.

    ``pols_tot(t+1) + pols_totr(t+1)`` against the same population rolled forward without
    the cohort machinery: survivors of ``q_T`` and of recovery, plus the direct entrants,
    plus the entrants out of the reduced ledger, plus the recognised aggravations.  The
    aggravation term is what makes this check bite — an implementation that added
    aggravations to *totale* without removing them from *partielle*, or that recognised
    them twice, fails here.
    """
    expected = ((pols_tot(t) + pols_totr(t))
                * (1.0 - mort_rate_total_mth(t))
                * (1.0 - recovery_rate_mth())
                + pols_entry_total(t) + pols_entry_total_red(t)
                + pols_aggravation_recog(t))
    return pols_tot(t + 1) + pols_totr(t + 1) - expected


def check_tot_roll_fwd():
    """True when the two *totale* ledgers close against their aggregate recursion."""
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return all(abs(check_tot_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_model_point():
    """True when the selected model point is one the contract could have written.

    Unlike the three roll-forward checks this is a **validation of the input** rather
    than an identity of the projection: the *rente* inside its sourced 500-3,000 band,
    the entry age inside the sourced 40-75 band on a new-business cell, the three
    *carences* in the non-decreasing order the actuarial reference asks for, a reduced
    cell with enough years of premiums behind it to have qualified, and a cause mix that
    sums to one — without which :func:`carence_factor` would silently scale every claim.
    """
    tbl = data.cause_mix_table()                                     # noqa: F821
    if abs(float(tbl["share"].sum()) - 1.0) > 1e-9:
        return False
    if not 500.0 <= rente_total_mth() <= 3000.0:
        return False
    if not 0.0 <= partial_ratio() <= 1.0:
        return False
    if premium_mth() <= 0.0 or capital_amount() < 0.0:
        return False
    if franchise_months() < 0 or reduction_qualifying_years() < 1:
        return False
    if not (carence_accident_months() <= carence_illness_months()
            <= carence_neuro_months()):
        return False
    if status() == "autonomous" and not 40 <= age_at_entry() <= 75:
        return False
    if status() == "reduced" and years_paid() < reduction_qualifying_years():
        return False
    return age_at_entry() < terminal_age                             # noqa: F821


# --- result tables ---

def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is every ledger added at the start of the month, and the five ledgers are
    published beside it because the reader needs to know which of them is paying premium,
    which is receiving a *rente* and which is doing neither.  ``refunds_carence`` has its
    own column because it is a return of premium and not a claim, and ``claim_expenses``
    has its own because it is a per-event cost rather than a per-policy one.  Nothing
    here is discounted.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_auto": [pols_auto(t) for t in ts],
            "pols_red": [pols_red(t) for t in ts],
            "pols_part": [pols_part(t) for t in ts],
            "pols_tot": [pols_tot(t) for t in ts],
            "pols_totr": [pols_totr(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_rente": [claims(t, "RENTE") for t in ts],
            "claims_capital": [claims(t, "CAPITAL") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "refunds_carence": [refunds_carence(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_states():
    """Result table of state movements and rates, indexed by policy month t."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_entry_partial": [pols_entry_partial(t) for t in ts],
            "pols_entry_total": [pols_entry_total(t) for t in ts],
            "pols_entry_total_red": [pols_entry_total_red(t) for t in ts],
            "pols_aggravation": [pols_aggravation(t) for t in ts],
            "pols_carence_exit": [pols_carence_exit(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_reduction": [pols_reduction(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "instalments": [instalments(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_partial": [mort_rate_partial(t) for t in ts],
            "mort_rate_total": [mort_rate_total(t) for t in ts],
            "inc_rate_partial": [inc_rate_partial(t) for t in ts],
            "inc_rate_total": [inc_rate_total(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "carence_factor": [carence_factor(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

terminal_age = 110

mort_partial_mult = 1.75

mort_total_mult = 4.27

aggravation_rate = 0.20

recovery_rate = 0.0

reval_guarantee = 0.010

reval_rente = 0.015

couple_discount_rate = 0.10

revision_lapse_slope = 3.0

revision_lapse_threshold = 0.02

expense_acq = 150.0

expense_maint = 3.0

expense_assist = 1.2

expense_claim_adj = 250.0

expense_rente = 10.0

inflation_rate = 0.015

roll_fwd_tol = 1e-12

math = ("Module", "math")

pd = ("Module", "pandas")
