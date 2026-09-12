# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Obseques_FR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the RefOBS-VIA worked-example anchor cell
    >>> Projection.point_id = 3            # the prime unique cell

``t`` counts **policy months**, 0-based: ``t = 0`` is the first policy month and the frame
is ``t = 0, 1, ..., proj_len() - 1``, so ``proj_len()`` is the **number** of projected
months. The policy year is the contractual 1-based label derived from it,
``policy_year(t) = t // 12 + 1``. The notes carry the in-force probability ``l(k)`` at time
``k`` months from issue with ``l(0) = 1``, and the library indexes :func:`pols_if` at the
**start** of the month, so ``pols_if(t)`` is exactly the notes' ``l(t)`` — which is the
column their worked-example table prints, and the weight on every cash flow of the same
``result_cf()`` row.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/obseques/``, read at run time rather than stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Obseques_FR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Obseques_FR_S.Data`, reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
mort_table_file         data.mort_table()                   mort_table.csv
select_table_file       data.select_table()                 select_table.csv
lapse_table_file        data.lapse_table()                  lapse_table.csv
surr_scale_file         data.surr_scale_table()             surr_scale_table.csv
single_prem_file        data.single_prem_table()            single_prem_table.csv
======================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for annual rates and ``*_rate_mth`` for monthly ones, ``*_pp`` for
per-policy amounts, ``claims(t, kind)`` and ``benefit_pp(t, kind)`` with an uppercase
``kind`` string. The technical notes use compact actuarial symbols instead. The mapping
is:

=========================  ==================================  ==========================
Notes symbol               Cells                               Meaning
=========================  ==================================  ==========================
(model point row)          model_point()                       The selected model point
cell                       cell()                              RefOBS-VIA / TMP / UNI
entry_age                  age_at_entry()                      Entry age, millesime basis
x(t)                       age(t)                              Attained age in month t
y                          policy_year(t)                      Policy year of month t
(none)                     duration(t)                         Completed policy years
(none)                     duration_mth(t)                     Months elapsed at BOM, = t
omega                      omega_age                           Limiting age, 112
(none)                     proj_len()                          Number of projected months
C_0                        capital_0()                         Capital at issue
C(y)                       capital_pp(t)                       Guaranteed capital in force
r                          reval_rate()                        Annual revalorisation rate
(simple/compound)          reval_simple()                      Simple uprating variant
(coupling)                 reval_prem_linked()                 Premiums uprated with it
P_a(y)                     prem_ann(t)                         Annual premium in year y
P(t)                       prem_due_pp(t)                      Premium due at BOM of t
(frequency)                prem_freq()                         Instalments a year
(none)                     is_premium_mth(t)                   An instalment falls in t
(paying period)            in_paying_period(t)                 Premiums are still due
K(t)                       cum_prem_pp(t)                      Premiums collected to BOM
n_car                      carence_months()                    Waiting period, months
(indicator)                in_carence(t)                       t < carence_months
(refund basis)             refund_pp(t)                        Waiting-period refund
i_ref                      carence_refund_rate()               Interest on the refund
DB_ill(t)                  benefit_pp(t, "ILL")                Non-accidental benefit
DB_acc(t)                  benefit_pp(t, "ACC")                Accidental benefit
(blended)                  benefit_pp(t, "DEATH")              Expected benefit per death
C_red(t)                   benefit_pp(t, "PAID_UP")            Paid-up capital on reduction
C_red(t)                   reduced_capital_pp(t)               The same amount, per policy
k_adb                      accident_mult()                     Accidental multiplier
d_acc                      acc_share                           Accidental share of deaths
V(t)                       surr_value_pp(t)                    Surrender value
surr_scale(t)              surr_scale_pp(t)                    Scale per 5000 EUR, read at t+1
pen(t)                     surr_penalty(t)                     Surrender penalty rate
u(x)                       single_prem_rate(x)                 Single premium per 1 EUR
rho                        reduction_share()                   Premium-stops made paid-up
q_base(x, sex)             mort_rate_base(x)                   Table mortality rate
f_as                       mort_antiselect_load                Anti-selection loading, 1.25
s(y)                       select_uplift(t)                    Select uplift by duration
(improvement)              mort_improve_factor(t)              Improvement factor, 1 in base
q(y)                       mort_rate(t)                        Annual mortality rate
q_m(y)                     mort_rate_mth(t)                    Monthly mortality rate
w(y)                       lapse_rate(t)                       Annual premium-stop rate
(table)                    lapse_rate_base(t)                  Table rate before the stress
beta                       lapse_overrun_beta                  Overrun lapse stress dial
w_m(y)                     lapse_rate_mth(t)                   Monthly premium-stop rate
l(t)                       pols_if(t)                          Premium-paying in force
l_r(t)                     pols_paid_up(t)                     Paid-up in force
(none)                     pols_all(t)                         pols_if + pols_paid_up
(none)                     capital_paid_up(t)                  Aggregate paid-up capital
(none)                     pols_death(t)                       Deaths, premium-paying
(none)                     pols_death_paid_up(t)               Deaths, paid-up
(none)                     pols_exit(t)                        Premium-stops of any kind
(none)                     pols_convert(t)                     Premium-stops made paid-up
(none)                     pols_lapse(t)                       Premium-stops surrendering
(none)                     crossover_mth(basis)                Month premiums pass capital
E[premium](t)              premiums(t)                         Premium income
E[death outgo](t)          claims(t, kind)                     Outgo by kind
E[expenses](t)             expenses(t)                         Acquisition + maintenance
(none)                     inflation_factor(t)                 Expense inflation factor
liability_cf(t)            liability_cf(t)                     The notes' outgo-positive CF
net_cf(t)                  net_cf(t)                           Net cash flow, income positive
=========================  ==================================  ==========================

Four names needed care.

The notes' ``l(t)`` and ``l_r(t)`` are two population strands: policies still **paying
premiums**, and policies made **paid-up** by *reduction*. :func:`pols_if` is the first —
the notes' ``l``, and what the worked example prints — :func:`pols_paid_up` the second,
and :func:`pols_all` their sum, which is what the maintenance expense is carried on. On
every model point but one the second strand is empty and the three coincide.

``C_red(t)`` appears twice because it is used twice. :func:`reduced_capital_pp` is the
paid-up capital a policy converting in month ``t`` is left with, ``V(t) / u(x(t))``, and
:func:`capital_paid_up` is the **aggregate** paid-up capital in force. Carrying the
aggregate alongside the count is what removes the need for a per-conversion cohort
dimension: the paid-up capital depends on *when* the policy converted, but every paid-up
policy thereafter rolls forward on the same survival factor, so the sum of their capitals
satisfies the same recursion as the count. Death outgo on that strand is then
``capital_paid_up(t) x q_m(t)``.

``surr_scale(t)`` in the notes is the external scale; here :func:`surr_scale` is the
model point's **choice of scale** — a string naming one insurer's published grid — and
:func:`surr_scale_pp` is the interpolated amount. The two are separate cells because
mixing one insurer's premium with another's surrender grid is the single easiest way to
produce a plausible-looking and wrong margin on this product.

``C(y)`` is a constant in most protection models and a function of ``t`` here, because
the *participation aux benefices* moves it every year.

.. rubric:: The delai de carence is two benefits, not one

For the first twelve months — ``t = 0`` to ``t = 11`` — a **non-accidental** death refunds
the premiums **collected**: a step function, constant at 336.03 through those twelve months
on the anchor cell, because the premium is annual and payable in advance. An **accidental**
death pays the **full guaranteed capital from day one**. From ``t = 12`` any death pays the
capital.

Paying the capital inside the waiting period is the central error available on this
product: it takes the first month's expected death outgo from 0.380884 to 3.345618 and
policy-year 1 from 4.4274 to 38.8893. Dropping the accident leg is the mirror-image error
and understates the first month by 41 %. Accruing the refund base monthly when the premium
is annual understates policy year 1 by 26 %. All three are asserted in the test module.

The accidental multiplier — ``2 x`` the capital at one insurer, capped at 20000 EUR —
applies **past** the waiting period only. Inside it the accidental benefit is already the
full capital, and doubling it there overstates outgo. :func:`accident_mult` is used in one
place, ``benefit_pp(t, "ACC")``, past the *carence* only.

.. rubric:: The capital is a state variable

The guaranteed capital is uprated annually out of the *participation aux benefices*, and
the uprating starts at the **first anniversary**, not at issue, because PB is allocated to
contracts in force at least a year. So ``capital_pp(t) == capital_0()`` for
``t < 12``, and the year-``y`` capital is ``C_0 x (1 + r)^(y-1)`` — or
``C_0 x (1 + r (y-1))`` where :func:`reval_simple` reads the contractual wording as a
simple uplift. Nothing is uprated inside the waiting period on the illness leg: that
benefit is a refund of premiums, not a capital, and :func:`carence_refund_rate` is a
different parameter that must not be confused with the revalorisation rate.

Whether the **premiums** are uprated with the capital is a first-order fork read from the
model point, never hard-coded: five of the seven retrieved insurers leave the premium
alone, one raises the remaining premiums in the same proportion. Applying the coupling to
the wrong cell moves premium income in the wrong direction.

.. rubric:: Lapse pays money, which is the whole contrast with the UK sibling

*Rachat* pays the *provision mathematique*, so ``claims_lapse`` — the ``"LAPSE"`` kind
of :func:`claims` — is non-zero from the first month and worth 1005.89 over the anchor
cell's horizon. On :mod:`.WOL_UK_S`, where a lapse pays exactly nothing, raising lapse
always lowers the liability; here removing the lapse decrement *raises* the undiscounted net
stream from 2236.92 to 3165.11, because the premiums a lapser stops paying are worth more
than the reserve handed back. Two consequences are wired in rather than left as prose:

- **No premium-stop decrement where no premium is due.** After ``prem_cease_age``, past
  the end of a temporary premium term, on a *prime unique* cell and in the paid-up state
  there is nothing to stop paying, so :func:`lapse_rate` is zero there.
  :func:`check_lapse_gate` asserts it.
- ***Reduction* is not termination.** Non-payment produces a **paid-up contract** wherever
  the surrender value is sufficient, so a share :func:`reduction_share` of premium-stops
  converts — a state change with no cash flow — and keeps a death liability the contract
  still owes. Routing every premium-stop to the exit removes that liability silently.

.. rubric:: The overrun

Under *primes viageres* cumulative premiums grow without bound while the capital grows at
most at the revalorisation rate, so the insured can and often does pay more than the
capital. :func:`crossover_mth` finds the month, and it finds **two** of them: against the
capital at issue, ``t = 168`` on the anchor cell, and against the revalorised capital,
``t = 204`` — three years apart. Reporting one without saying which is how a published
crossover moves by years. It is reported rather than acted on: the overrun-aware lapse
module that raises the rate past the tipping point is a pure stress dial, and
``lapse_overrun_beta`` is 0 in the base run.

.. rubric:: Sign convention

The notes print the stream **outgo-positive** as ``liability_cf``, so that orientation
survives verbatim in :func:`liability_cf` and :func:`net_cf` is its exact negative, which
is the library-wide sign. The notes' worked-example table omits expenses "for clarity" and
prints premium income and death outgo as separate positive columns, so neither
``liability_cf`` nor ``net_cf`` equals any column of it.
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


def cell():
    """``RefOBS-VIA``, ``RefOBS-TMP`` or ``RefOBS-UNI``: the premium-form cell.

    A label, not a switch.  Every cell runs the same engine, and what actually differs
    between them is :func:`premium_form` and the model point columns that go with it -
    which is the point the technical notes make about this product: the three cells are
    the same contract with one column changed.
    """
    v = model_point()["cell"]
    if v not in ("RefOBS-VIA", "RefOBS-TMP", "RefOBS-UNI"):
        raise ValueError("invalid cell")
    return v


def sex():
    """The sex (M / F) of the selected model point.

    Drives the shipped **[std]** mortality proxy and nothing contractual: no retrieved
    funeral rate card rates by sex, and acceptance is guaranteed with no medical
    selection of any kind.
    """
    return model_point()["sex"]


def age_at_entry():
    """The entry age, on the ***difference de millesime*** basis.

    Calendar year of subscription less calendar year of birth - **not** age last birthday
    and **not** age nearest birthday.  The true basis increments on 1 January; the model
    increments at the policy anniversary instead **[std]**, which is exact for January
    issues and is what every shipped model point is.  Using age last birthday instead
    shifts the whole mortality lookup by up to a year at entry.
    """
    return int(model_point()["entry_age"])


def capital_0():
    """C_0: the guaranteed capital at issue, in EUR.

    5000 EUR is the illustrative capital every retrieved standardised table is published
    at, and is close to the average cost of a French funeral excluding *marbrerie*.
    :func:`capital_pp` is the amount in force in a given month, which differs from this
    from the first anniversary on.
    """
    return float(model_point()["capital_0"])


def premium_form():
    """``single``, ``temporary`` or ``lifetime``: the premium form.

    This product's signature, and **final at inception** - the form cannot be changed
    later.  It decides the paying period, whether a premium-stop decrement applies at all,
    and whether the contract can overrun its own capital.
    """
    v = model_point()["premium_form"]
    if v not in ("single", "temporary", "lifetime"):
        raise ValueError("invalid premium_form")
    return v


def prem_term_y():
    """The premium-paying term in years; 1 on a single premium, 0 on a lifetime one."""
    return int(model_point()["prem_term_y"])


def prem_cease_age():
    """The attained age at which lifetime premiums stop; 0 means they never do.

    The retrieved tables disagree: one runs lifetime premiums to attained age 115 with no
    cessation, one to 95 with none shown, one implies cessation near 90 from equal
    cumulative figures at 90 and 95, and one sells an explicit "to age 80" form alongside
    the lifetime one.  Never-ceasing is the reference choice **[std]**, because it is the
    documented design that produces the overrun this product is criticised for; defaulting
    this to anything non-zero makes that overrun disappear.
    """
    return int(model_point()["prem_cease_age"])


def annual_premium():
    """The premium in EUR per year - or the whole single premium on a *prime unique* cell.

    A model point input, not a rate-table lookup.  The standardised tables are the only
    public rate card for this product, they state that they have no contractual value, and
    no insurer publishes the mortality table, technical rate, expense loading or margin
    behind them.  The lifetime premium for a 5000 EUR capital at entry 50 spans roughly
    2:1 across the retrieved set, so this and :func:`surr_scale` must come from the **same**
    document.
    """
    return float(model_point()["annual_premium"])


def prem_freq():
    """The number of premium instalments a year: 1, 2, 4 or 12.

    Premiums are contractually annual and payable in advance, and every published rate
    card is annual, so 1 is the reference **[std]**.  The instalment options are a
    documented 2.2 % loading on the annual premium rather than a re-tariffing, so a
    monthly point carries the loaded figure in :func:`annual_premium` and pays a twelfth
    of it each month.
    """
    v = int(model_point()["prem_freq"])
    if v not in (1, 2, 4, 12):
        raise ValueError("invalid prem_freq")
    return v


def carence_months():
    """n_car: the *delai de carence* in months, 12 in every retrieved contract.

    Since 1 July 2025 the market cap for new contracts is one year, against up to two
    previously.  It is the anti-selection device that replaces underwriting on a
    guaranteed-issue book whose entrants may be 84 years old and know their own health.
    """
    return int(model_point()["carence_months"])


def carence_refund_basis():
    """``gross``, ``net_assistance`` or ``net_instalment``: what the refund is net of.

    Three insurers, three bases: the premiums collected gross, net of the assistance
    premium, net of instalment charges.  Gross is the reference **[std]**; the other two
    are carried because they are what two retrieved contracts actually say.
    """
    v = model_point()["carence_refund_basis"]
    if v not in ("gross", "net_assistance", "net_instalment"):
        raise ValueError("invalid carence_refund_basis")
    return v


def carence_refund_rate():
    """i_ref: interest credited on the refunded premiums, zero in every retrieved contract.

    Not the revalorisation rate, and easy to confuse with it.  A different rule exists in
    statute and reaches a different product: the loi Sueur requires the capital paid by
    the subscriber of an advance-***prestations*** contract to bear interest at not less
    than the legal rate.  No retrieved *capital* contract pays interest on a waiting-period
    refund.
    """
    return float(model_point()["carence_refund_rate"])


def accident_mult():
    """k_adb: the accidental death multiplier **past** the waiting period, 1 or 2.

    1 at three insurers; 2 from year 2 subject to a 20000 EUR cap at one.  It applies past
    the waiting period only - inside it the accidental benefit is already the full capital,
    so doubling it there, or applying the multiplier to all deaths, overstates outgo.
    """
    return float(model_point()["accident_mult"])


def reval_rate():
    """r: the annual revalorisation of the guaranteed capital.

    1.00 % p.a. contractually guaranteed on the anchor cell - the only guaranteed rate
    retrieved anywhere - and discretionary at five of the seven insurers, set annually out
    of the *participation aux benefices* for contracts in force at least a year.  It is
    zero on the cells priced from tables published *sans participation aux benefices*,
    because a non-zero rate would be inconsistent with those tables' own surrender scales.
    No insurer's actually declared PB rate for a funeral contract in any year was found in
    any public source.
    """
    return float(model_point()["reval_rate"])


def reval_prem_linked():
    """Whether the remaining premiums are uprated with the capital.

    No at five insurers, **yes, in the same proportion on the remaining premiums**, at one.
    A first-order fork read from the model point and never hard-coded: applying the
    coupling to a cell that does not have it overstates premium income, and omitting it
    where it exists understates it.
    """
    return bool(model_point()["reval_prem_linked"])


def reval_simple():
    """Whether the uprating is simple on the subscribed capital rather than compound.

    The contractual wording is "1 % du capital souscrit", which reads naturally as a
    simple uplift, while the same document's surrender values pin down neither reading.
    Compounding on the current capital is the reference **[std]** because that is the form
    the other retrieved mechanisms take and because the one derivable rate in the file is
    demonstrably geometric.  Which reading the wording intends is [unverified].
    """
    return bool(model_point()["reval_simple"])


def surr_penalty_years():
    """The number of years a surrender penalty applies for; 0 in the reference cell."""
    return int(model_point()["surr_penalty_years"])


def surr_penalty_rate():
    """The surrender penalty rate inside that period; 0 in the reference cell.

    None at two insurers; 5 % in the first ten years, plus a further 5 % charge inside the
    mathematical provision in the first eight, at one.
    """
    return float(model_point()["surr_penalty_rate"])


def reduction_share():
    """rho: the share of premium-stops that become paid-up rather than surrendering.

    Zero in the base cell, 0.5 as the variation and 1.0 as the upper stress **[std]**.
    *Reduction* is contractually the normal consequence of non-payment wherever the
    surrender value is sufficient, and where a surrender value exists, stopping payment and
    taking nothing is strictly dominated by reducing - so the economically rational value
    is high.  But no public source gives any split between voluntary surrender and paid-up
    conversion, because none gives any decrement rate at all.  Zero keeps the worked
    example checkable; the parameter is the sensitivity dial, and it dominates the
    late-duration liability.  It must never be approximated by perturbing the lapse rate.
    """
    return float(model_point()["reduction_share"])


def surr_scale():
    """The name of the published surrender-value grid this model point is priced on.

    A key into *surr_scale_table.csv*, not an amount.  It must come from the same document
    as :func:`annual_premium` and :func:`reval_rate`: the anchor cell takes its premium,
    its guaranteed revalorisation rate and its surrender grid from one insurer precisely
    so that the three are consistent, and feeding one insurer's premium into another's
    grid produces plausible-looking and wrong margins.
    """
    return model_point()["surr_scale"]


def issue_month():
    """The calendar month of issue, 1 on every shipped model point.

    The *difference de millesime* age basis increments on 1 January; :func:`age` increments
    at the policy anniversary instead **[std]**, which is exact for a January issue and
    off by up to one policy year of mortality otherwise.  The column exists so that the
    approximation is visible in the data rather than buried in a formula.
    """
    v = int(model_point()["issue_month"])
    if not 1 <= v <= 12:
        raise ValueError("invalid issue_month")
    return v


def pols_if_init():
    """Initial number of policies in force; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_len():
    """Projection length in months: ``12 x (omega_age - entry_age + 1)``.

    The **number** of projected months, and the exclusive end of the frame: the projection
    runs over ``t = 0, 1, ..., proj_len() - 1`` and ``len(result_cf()) == proj_len()``.
    Whole life has no maturity date, so the horizon is a **limiting age** rather than a
    contractual one.  ``omega_age`` is 112, the tabulation limit of TH 00-02 in the annexe
    to art. A. 335-1 CA, and :func:`mort_rate` is forced to 1 there, so the population is
    exhausted inside the projection rather than truncated by it.  One insurer's tables run
    to attained age 115, so the horizon is a modelling convention and not a contractual
    one; :func:`check_truncation` asserts that nothing is left at the end of it.
    """
    return 12 * (omega_age - age_at_entry() + 1)                     # noqa: F821


def duration(t):
    """Completed policy years at the start of month t: ``t // 12``.

    0-based, as in lifelib: 0 through the whole of the first policy year.
    """
    return t // 12


def duration_mth(t):
    """Months elapsed from outset at the start of month t; equal to t.

    ``t`` is 0-based, so the identity is trivial - the cells exists so the monthly models
    in this library share one vocabulary.  Month ``t`` runs from time ``t`` to time
    ``t + 1``, so ``duration_mth(t) + 1`` months have elapsed by the end of it.
    """
    return t


def policy_year(t):
    """y = t // 12 + 1: the policy year containing month t; 1 for t = 0..11.

    The contractual, **1-based** label, derived from the 0-based index and never
    confused with it: it is what the premium, lapse and select schedules are keyed by.
    """
    return duration(t) + 1


def age(t):
    """x(t): the attained age in the policy year containing month t.

    ``entry_age + y - 1`` on the *difference de millesime* basis, stepping at the policy
    anniversary **[std]** rather than on 1 January - see :func:`issue_month`.
    """
    return age_at_entry() + duration(t)


def mort_rate_base(x):
    """q_base(x, sex): the table mortality rate at attained age x.

    Keyed by age rather than by month so that the lookup is evaluated once per attained
    age instead of once per projected month.  A **[std]** INSEE-shaped proxy anchored at
    ``q(M, 50) = 0.0040`` with 9 % p.a. age progression, which is the technical notes'
    walk-through basis exactly.  TH 00-02 and TF 00-02 are the homologated regulatory
    tables for this product; they are cited by name and never redistributed here.
    """
    return float(data.mort_table().loc[(sex(), x), "mort_rate"])     # noqa: F821


def select_uplift(t):
    """s(y): the select uplift on base mortality in the policy year containing month t.

    1.60 / 1.30 / 1.15 / 1.00 for policy years 1 / 2 / 3 / 4+ **[std]**.  Policy years
    beyond the table take its last row.  The excess belongs at short durations and the
    first-year factor is the largest **even though a first-year illness death costs only a
    refund** - the deaths still happen, they merely cost less, and moving the excess to
    year 2 would double-count the protection the waiting period already gives.  A flat
    loading understates the year-2 spike, which is the largest single step in the anchor
    cell's death-outgo series.
    """
    tbl = data.select_table()                                        # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "select_factor"])


def mort_improve_factor(t):
    """The mortality improvement factor in month t; 1 in the base run **[std]**.

    ``(1 - improvement)^(y - 1)``.  France has no publicly available insured-lives
    projection model comparable to the CMI's, so a flat annual reduction is the **[std]**
    sensitivity proxy rather than a basis.  Improvements lengthen the premium stream and
    defer the claim at once, which on a *viagere* cell pull in opposite directions.
    """
    return (1.0 - mort_improvement) ** (policy_year(t) - 1)          # noqa: F821


def mort_rate(t):
    """q(y): the annual mortality rate applied in the policy year containing month t.

    ``q_base(x, sex) x f_as x s(y)``, capped at 1 and forced to 1 at the limiting age.
    The anti-selection loading is **upward** relative to population mortality and that
    direction is the defensible part: acceptance is guaranteed, with no medical
    questionnaire and no examination, so the pool cannot be better than the population and
    self-selects worse, and the only device standing against an applicant who knows their
    prognosis is the twelve-month waiting period.  The magnitude has no public calibration
    of any kind.
    """
    if age(t) >= omega_age:                                          # noqa: F821
        return 1.0
    q = (mort_rate_base(age(t)) * mort_antiselect_load               # noqa: F821
         * select_uplift(t) * mort_improve_factor(t))
    return min(1.0, q)


def mort_rate_mth(t):
    """q_m(y) = 1 - (1 - q)^(1/12): the monthly mortality rate **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """The table annual premium-stop rate in month t **[std]**, before the overrun stress.

    6 % / 5 % / 3.5 % / 2.5 % for policy years 1 / 2 / 3-5 / 6+; policy years beyond the
    table take its last row.  Declining with duration, because a small-premium
    *prevoyance* contract bought for one purpose is stopped early or not at all, and
    because the surrender value is worth a fraction of the premiums paid for the first two
    decades - so an early lapser loses most of their money and a late one has nearly
    reached a full payout.  There is **no waiting-period completion spike**: nothing
    changes for the policyholder at ``t = 12`` except that the cover becomes worth having.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate"])


def lapse_rate(t):
    """w(y): the annual premium-stop rate applying at the end of month t.

    **Zero wherever no premium is due**: on a *prime unique* cell, past the end of a
    temporary premium term and past ``prem_cease_age``.  There is nothing left to stop
    paying, and a decrement there silently destroys liability.  Otherwise the table rate,
    optionally stressed by ``1 + beta`` once cumulative premiums have passed the capital,
    which is off in the base run.
    """
    if premium_form() == "single" or not in_paying_period(t):
        return 0.0
    w = lapse_rate_base(t)
    if lapse_overrun_beta > 0.0 and cum_prem_pp(t) > capital_pp(t):  # noqa: F821
        w = w * (1.0 + lapse_overrun_beta)                           # noqa: F821
    return min(1.0, w)


def lapse_rate_mth(t):
    """w_m(y) = 1 - (1 - w)^(1/12): the monthly premium-stop rate **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def is_premium_mth(t):
    """Whether an instalment falls due in month t: ``t = 0 (mod 12 / prem_freq)``.

    Months 0, 12, 24, ... on the annual default; every month at ``prem_freq = 12``.
    """
    step = 12 // prem_freq()
    return t % step == 0


def in_paying_period(t):
    """Whether month t is inside the premium-paying period of this premium form.

    Month 0 only on a *prime unique*; months 0 to ``12 x prem_term_y - 1`` on a
    *temporaire*; every month on a *viagere*, unbounded where ``prem_cease_age`` is 0 and
    otherwise until the anniversary at which the attained age reaches it.
    """
    form = premium_form()
    if form == "single":
        return t == 0
    if form == "temporary":
        return t < 12 * prem_term_y()
    return prem_cease_age() == 0 or age(t) < prem_cease_age()


def prem_ann(t):
    """P_a(y): the annual premium in the policy year containing month t.

    Level and fixed at inception unless :func:`reval_prem_linked`, in which case the
    remaining premiums rise in the same proportion as the capital - geometrically, or
    simply where :func:`reval_simple` reads the wording that way.
    """
    if not reval_prem_linked():
        return annual_premium()
    y = policy_year(t)
    if reval_simple():
        return annual_premium() * (1.0 + reval_rate() * (y - 1))
    return annual_premium() * (1.0 + reval_rate()) ** (y - 1)


def prem_due_pp(t):
    """P(t): the premium due per policy at the beginning of month t.

    One instalment, ``P_a(y) / prem_freq``, in a premium month inside the paying period,
    and zero otherwise.  Paid-up policies pay nothing and are carried as a separate
    population strand rather than as a premium of zero, so they do not appear here.
    """
    if not (is_premium_mth(t) and in_paying_period(t)):
        return 0.0
    return prem_ann(t) / prem_freq()


def cum_prem_pp(t):
    """K(t): the premiums collected per policy to the beginning of month t.

    The premium falls at the beginning of the month and death at the end, so a death in
    month t has had the month-t premium paid on it.  This is the **waiting-period refund
    base**, and with an annual premium in advance it is a **step function** - constant at
    one year's premium through months 0 to 11 - not a monthly accrual.  Accruing it
    monthly gives 28.00 rather than 336.03 in the first month on the anchor cell and
    understates policy-year-1 death outgo by 26 %.

    ``K(0) = P(0)``: the first month's premium is the whole of the base at ``t = 0``, and
    nothing is indexed below the frame.
    """
    if t == 0:
        return prem_due_pp(0)
    return cum_prem_pp(t - 1) + prem_due_pp(t)


def capital_pp(t):
    """C(y): the guaranteed capital in force in the policy year containing month t.

    ``C_0 x (1 + r)^(y-1)``, or ``C_0 x (1 + r (y-1))`` under :func:`reval_simple`.  The
    uprating starts at the **first anniversary**, not at issue, because the
    *participation aux benefices* is allocated to contracts in force at least a year - so
    ``capital_pp(t) == capital_0()`` for ``t < 12``, which :func:`check_capital_reval`
    asserts.  Uprating at issue would make it 5050.00 in the first year on the anchor cell
    and overstate the year-1 accidental leg.
    """
    y = policy_year(t)
    if reval_simple():
        return capital_0() * (1.0 + reval_rate() * (y - 1))
    return capital_0() * (1.0 + reval_rate()) ** (y - 1)


def surr_scale_anchors():
    """The selected surrender-value scale as a list of ``(month, value)`` anchors.

    Extracted once per model point and interpolated in pure Python by
    :func:`surr_scale_pp`, rather than indexing the DataFrame afresh in each of several
    hundred projected months.
    """
    tbl = data.surr_scale_table().loc[surr_scale()]                  # noqa: F821
    return [(int(m), float(v)) for m, v in zip(tbl.index, tbl["surr_value"])]


def surr_scale_pp(t):
    """The published surrender-value scale for a surrender in month t, per 5000 EUR.

    The CSV's ``month`` column is **elapsed months from issue**, 0 at issue and 60, 120,
    ... 540 at the published quinquennial anniversaries; it is not the frame's ``t`` and
    does not move with it.  Surrenders fall at the **end** of month t, by which time
    ``duration_mth(t) + 1`` months have elapsed, so that is the key this reads: the first
    projected month, ``t = 0``, is one month into the contract, and the published
    five-year anchor is reached in month ``t = 59``.

    Linearly interpolated in **elapsed months** between the published quinquennial anchors
    **[std]** and held flat beyond the last one.  The anchors are transcribed from one
    insurer's standardised table and already embed that insurer's own revalorisation,
    which is why :func:`surr_value_pp` is **not** additionally scaled by
    :func:`capital_pp`.

    The production alternative is a prospective *provision mathematique* on the tariff
    basis.  It is not the reference implementation because **no insurer publishes its
    tariff basis**: the whole retrieved set contains one technical rate with a table and
    one rate alone.
    """
    m_elapsed = duration_mth(t) + 1
    anchors = surr_scale_anchors()
    if m_elapsed >= anchors[-1][0]:
        return anchors[-1][1]
    lo = anchors[0]
    hi = anchors[-1]
    for m, v in anchors:
        if m <= m_elapsed:
            lo = (m, v)
        else:
            hi = (m, v)
            break
    return lo[1] + (hi[1] - lo[1]) * (m_elapsed - lo[0]) / (hi[0] - lo[0])


def surr_penalty(t):
    """pen(t): the surrender penalty rate applying in month t.

    ``surr_penalty_rate`` inside the first ``surr_penalty_years`` years - months
    ``t = 0`` to ``12 x surr_penalty_years - 1`` - and zero after: a flat window, not a
    decaying scale, which is how the one insurer that charges it writes it.
    """
    return surr_penalty_rate() if t < 12 * surr_penalty_years() else 0.0


def surr_value_pp(t):
    """V(t): the surrender value per policy in month t - the *provision mathematique*.

    The scale for this model point, pro-rated to the policy's own capital and net of any
    penalty.  It is a **real cash flow**, paid on every *rachat* from the first projected
    month, which is the whole difference from the UK guaranteed-acceptance sibling where a
    lapse pays nothing.  It is also what an excluded death is paid: suicide in year 1, war,
    nuclear and murder by a beneficiary do not extinguish the contract, and an exclusion
    modelled as a zero benefit understates outgo by exactly this amount per excluded death.
    """
    return (surr_scale_pp(t) * capital_0() / surr_scale_capital      # noqa: F821
            * (1.0 - surr_penalty(t)))


def single_prem_rate(x):
    """u(x): the single premium per 1 EUR of whole-life capital at attained age x.

    Keyed by age rather than by month so that the lookup is evaluated once per attained
    age.  Anchored on the published *prime unique* rate card and interpolated and
    extrapolated **[std]**.  It serves twice: it is the tariff behind the *prime unique*
    premium form, and it is what turns a mathematical provision into a *valeur de
    reduction*.
    """
    tbl = data.single_prem_table()                                   # noqa: F821
    x = min(max(x, int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[x, "single_prem_rate"])


def reduced_capital_pp(t):
    """C_red(t): the paid-up capital a policy converting in month t is left with.

    ``V(t) / u(x(t))`` - the whole-life cover that the accumulated provision buys as a
    single premium at the attained age.  Fixed at the date of *reduction* and not uprated
    afterwards; the aggregate in force is :func:`capital_paid_up`.
    """
    return surr_value_pp(t) / single_prem_rate(age(t))


def in_carence(t):
    """Whether month t falls inside the *delai de carence*: ``t < carence_months``.

    Months ``t = 0`` to ``t = carence_months - 1`` on the 0-based frame, so the twelve
    contractual waiting-period months are ``t = 0 .. 11`` and the cover changes at
    ``t = 12``.
    """
    return t < carence_months()


def refund_pp(t):
    """The waiting-period refund per policy in month t, on this cell's basis.

    ``K(t)`` gross; net of the assistance premium at one insurer, 12 EUR a year for each
    year begun - which is ``policy_year(t)`` on the 0-based frame; net of instalment
    charges at another, which strips the documented 2.2 % instalment loading and therefore
    does nothing on an annual-premium cell.  Then credited with ``carence_refund_rate``,
    which is zero in every retrieved contract, over the ``duration_mth(t) + 1`` months
    elapsed by the end of month t, when the death resolves.
    """
    base = cum_prem_pp(t)
    basis = carence_refund_basis()
    if basis == "net_assistance":
        years = policy_year(t)
        base = max(0.0, base - assistance_prem_pp * years)           # noqa: F821
    elif basis == "net_instalment" and prem_freq() > 1:
        base = base / (1.0 + instalment_load)                        # noqa: F821
    return base * (1.0 + carence_refund_rate()) ** ((duration_mth(t) + 1) / 12.0)


def benefit_pp(t, kind):
    """The benefit amount per policy in month t, by kind.

    ``"ILL"``
        the non-accidental death benefit: :func:`refund_pp` inside the
        *delai de carence* and the guaranteed capital after it.  It is a
        refund of premiums, not a capital, so it carries no
        revalorisation.

    ``"ACC"``
        the accidental death benefit: the **full guaranteed capital from
        day one**, and ``k_adb`` times it past the waiting period, capped
        at the contractual maximum.  The accident definition is narrow -
        cerebral and cardio-vascular events are never accidents whatever
        their origin, and the burden of proof is on the claimant.

    ``"DEATH"``
        the expected benefit per death on the premium-paying strand,
        blending the two above by ``acc_share``.  This is what
        :func:`claims` multiplies by.

    ``"PAID_UP"``
        the paid-up capital of a policy converting in month t, which is
        :func:`reduced_capital_pp`.  A paid-up policy is treated as past
        the waiting period and pays that amount for any cause.
    """
    if kind == "ILL":
        return refund_pp(t) if in_carence(t) else capital_pp(t)
    if kind == "ACC":
        if in_carence(t):
            return capital_pp(t)
        return min(accident_mult() * capital_pp(t), accident_cap)    # noqa: F821
    if kind == "DEATH":
        return ((1.0 - acc_share) * benefit_pp(t, "ILL")             # noqa: F821
                + acc_share * benefit_pp(t, "ACC"))                  # noqa: F821
    if kind == "PAID_UP":
        return reduced_capital_pp(t)
    raise ValueError("invalid kind")


def pols_if(t):
    """l(t): premium-paying policies in force at the **start** of policy month t.

    The notes' in-force probability at time t months from issue, and the column their
    worked-example table prints; ``pols_if(0) == pols_if_init()``.
    Paid-up policies are **not** counted here: they are a separate strand,
    :func:`pols_paid_up`, because they pay no premium and their benefit is a different
    amount.  Defined one month past the frame - at ``t = proj_len()`` - so that the
    roll-forward checks close in the last projected month, ``proj_len() - 1``.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    return (pols_if(t - 1) * (1.0 - mort_rate_mth(t - 1))
            * (1.0 - lapse_rate_mth(t - 1)))


def pols_paid_up(t):
    """l_r(t): paid-up (*reduit*) policies in force at the start of policy month t.

    Zero where ``reduction_share`` is zero, and zero at ``t = 0``: nothing is paid-up at
    issue.  Paid-up policies pay no premium, carry no
    premium-stop decrement - there is nothing left to stop paying - and their capital is
    fixed at the date of conversion, so they roll forward on mortality alone and take
    conversions in from the premium-paying strand.  Voluntary surrender by a paid-up
    policyholder is not modeled **[std]**.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return 0.0
    return pols_paid_up(t - 1) * (1.0 - mort_rate_mth(t - 1)) + pols_convert(t - 1)


def capital_paid_up(t):
    """The aggregate paid-up capital in force at the start of month t.

    Carrying the aggregate capital alongside the count is what removes the need for a
    per-conversion cohort dimension: the paid-up capital depends on *when* the policy
    converted, but every paid-up policy thereafter rolls forward on the same survival
    factor, so the sum of their capitals satisfies the same recursion as the count.  Death
    outgo on the strand is then ``capital_paid_up(t) x q_m(t)``.  Zero at ``t = 0``:
    nothing is paid-up at issue.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return 0.0
    return (capital_paid_up(t - 1) * (1.0 - mort_rate_mth(t - 1))
            + pols_convert(t - 1) * benefit_pp(t - 1, "PAID_UP"))


def pols_all(t):
    """All policies in force at the start of month t: premium-paying plus paid-up.

    The weight on the maintenance expense - a paid-up contract still costs money to
    administer - and the count the roll-forward closes on.
    """
    return pols_if(t) + pols_paid_up(t)


def pols_if_at(t, timing):
    """The number of premium-paying policies in force at a point inside month t.

    ``"BEF_DECR"``
        the start of the month, before any decrement; :func:`pols_if`.

    ``"BEF_LAPSE"``
        after deaths, before premium-stops - the processing order is
        **death before premium-stop** **[std]**.

    ``"AFT_DECR"``
        the end-of-month count, the notes' ``l(t + 1)``.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths on the premium-paying strand at the end of month t.

    Taken against the start-of-month in-force, which is the notes' ``l(t) x q_m(y)``.
    """
    return pols_if(t) * mort_rate_mth(t)


def pols_death_paid_up(t):
    """Deaths on the paid-up strand at the end of month t; zero where rho is zero."""
    return pols_paid_up(t) * mort_rate_mth(t)


def pols_exit(t):
    """Premium-stops at the end of month t, taken from the survivors of mortality.

    What happens to them is the ``reduction_share`` split: a share converts to paid-up and
    the rest surrenders and is paid the *provision mathematique*.  Neither is a
    forfeiture, which is the structural difference from the UK sibling.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_convert(t):
    """Premium-stops converted to paid-up at the end of month t: ``rho x pols_exit(t)``.

    A **state change, not a cash flow**.  The contract owes these policies a reduced
    capital for the rest of the insured's life, and routing them to the exit instead
    removes a death liability the contract still has.
    """
    return pols_exit(t) * reduction_share()


def pols_lapse(t):
    """Premium-stops that surrender at the end of month t: ``(1 - rho) x pols_exit(t)``.

    **Paid the surrender value**, unlike the UK guaranteed-acceptance sibling where a
    lapse pays nothing at all.  See ``claims(t, "LAPSE")``.
    """
    return pols_exit(t) - pols_convert(t)


def crossover_mth(basis):
    """The first month in which cumulative premiums exceed the capital, by basis.

    ``"ISSUE"``
        against the capital **at issue**, ``capital_0()``: ``t = 168``
        on the anchor cell, policy year 15.

    ``"CURRENT"``
        against the **revalorised** capital in force: ``t = 204``, policy
        year 18 - three years later, because the capital has been
        growing too.

    The month it returns is an index on the 0-based frame, so it is a valid answer at 0
    and the "never" sentinel is **-1**, not 0.  That case is the *prime unique* cell alone
    in the shipped table: the single premium is 85 % of the capital and nothing follows it.
    A *temporaire* cell can cross and two of the shipped ones do - a ten-year premium of
    651.26 passes 5000 at the eighth instalment - but it stops there, permanently, while a
    *viagere* cell goes on paying past the crossover for as long as the insured lives,
    which is the difference the product is criticised for.  Searched rather than
    closed-form so that the revalorised basis and the premium-linked variant both resolve.
    Reported rather than acted on - the
    overrun-aware lapse module is a pure stress dial and ``lapse_overrun_beta`` is 0 in
    the base run.

    Publishing one of these without saying which is a way to move a stated crossover by
    years.  The standardised tables add a second convention on top: they date their
    columns by the age at the **end** of the year, so their "age 65" column is this
    model's attained age 64.
    """
    if basis not in ("ISSUE", "CURRENT"):
        raise ValueError("invalid basis")
    for t in range(proj_len()):
        target = capital_0() if basis == "ISSUE" else capital_pp(t)
        if cum_prem_pp(t) > target:
            return t
    return -1


def premiums(t):
    """E[premium](t): premium income at the beginning of month t, an inflow.

    Carried on the premium-paying strand only: paid-up policies pay nothing, and neither
    does a policy past its cessation age or the end of its temporary term, where
    :func:`prem_due_pp` is already zero.
    """
    return prem_due_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"DEATH"``
        death outgo on the premium-paying strand,
        ``pols_death(t) x benefit_pp(t, "DEATH")``.

    ``"DEATH_PAID_UP"``
        death outgo on the paid-up strand, ``capital_paid_up(t) x q_m(t)``
        - the aggregate paid-up capital times the monthly mortality rate,
        which is why that strand carries a capital total as well as a
        count.

    ``"LAPSE"``
        surrender outgo, ``pols_lapse(t) x surr_value_pp(t)``.  **Not
        zero**, at any duration, on any cell: *rachat* pays the
        *provision mathematique*, and a whole-life contract sits in
        art. L. 132-23 CA's residual *autres assurances sur la vie*
        class, where the insurer may refuse neither *rachat* nor
        *reduction*.  The article withholds them from a closed list:
        temporary death assurance and immediate or in-payment annuities
        may carry neither; survivorship capitals, pure endowments and
        deferred annuities without return of premium may carry no
        *rachat*.
        Setting it to zero moves the anchor cell's undiscounted net
        stream from 2236.92 to 3242.81.

    There is no ``"MATURITY"`` kind, and that is a product fact rather than an omission:
    the contract ends only on death, on *rachat* or on lapse, and maturity outgo is
    identically zero because there is no maturity.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "DEATH_PAID_UP", "LAPSE"))
    if kind == "DEATH":
        return pols_death(t) * benefit_pp(t, "DEATH")
    if kind == "DEATH_PAID_UP":
        return capital_paid_up(t) * mort_rate_mth(t)
    if kind == "LAPSE":
        return pols_lapse(t) * surr_value_pp(t)
    raise ValueError("invalid kind")


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y - 1)`` **[std]**.

    Steps on policy anniversaries, not monthly.  Expense inflation has no source at all
    for this product, and over a horizon this long it runs against a premium that by
    construction cannot move - unless :func:`reval_prem_linked` is set, the one design in
    the retrieved set that indexes it.
    """
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense in month t **[std]**.

    The acquisition charge falls once, at issue - the first projected month, ``t = 0``;
    maintenance is carried on
    :func:`pols_all`, so a paid-up contract still costs money to administer even though it
    pays no premium.  No French source publishes a currency expense assumption for this
    product.  The anchors are the disclosed **charges**, which bound expenses from above
    and leave the margin: acquisition charges of 2.5 % to 5.38 % of the guaranteed capital
    and ongoing charges of 0.40 % p.a. of the capital plus 0.57 % p.a. while lifetime
    premiums are paid.  The shipped acquisition expense sits inside that range and the
    maintenance expense at about half the ongoing charge.  Claim handling is folded in
    here rather than charged per death, because no retrieved document separates them.
    """
    acq = expense_acq_pp * pols_if(t) if t == 0 else 0.0             # noqa: F821
    return acq + expense_maint_pp / 12.0 * inflation_factor(t) * pols_all(t)  # noqa: F821


def liability_cf(t):
    """The notes' outgo-positive cash flow in month t.

    ``claims_death + claims_death_paid_up + claims_lapse + expenses - premiums``.  This is
    the orientation the technical notes print, carried verbatim so that a reader can hold
    the two side by side; :func:`net_cf` is its exact negative and is the library-wide
    sign.
    """
    return (claims(t, "DEATH") + claims(t, "DEATH_PAID_UP")
            + claims(t, "LAPSE") + expenses(t) - premiums(t))


def net_cf(t):
    """CF(t): the net cash flow of month t, **income positive**.

    ``-liability_cf(t)`` exactly.  Note that the notes' worked-example table omits
    expenses "for clarity" and prints premium income and death outgo as separate positive
    columns, so this equals no column of that table.
    """
    return -liability_cf(t)


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_all(t) - pols_all(t+1)`` less deaths from both strands and the premium-stops
    that actually surrender.  Conversions to paid-up are absent because they move policies
    *between* strands rather than out of the population - which is the point of running
    the check on the total, and what makes it catch a *reduction* modelled as an exit.
    """
    return (pols_all(t) - pols_all(t + 1)
            - pols_death(t) - pols_death_paid_up(t) - pols_lapse(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the
    signed residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol      # noqa: F821
               * max(pols_if_init(), 1.0)
               for t in range(proj_len()))


def check_surv_annual_resid(t):
    """The residual of the annual survivorship identity at a policy-year start.

    The monthly decrements must compound back to the **annual** ones exactly, so the
    in-force at the start of policy year y+1 is available in closed form from the start of
    year y: ``l x (1 - q(y)) x (1 - w(y))``.  On the anchor cell that is
    ``0.992 x 0.94 = 0.93248`` at the end of policy year 1, which is the figure the notes'
    worked example prints against t = 12.

    This is the check that catches a misindexed recursion.  Rolling the in-force forward
    with the *next* month's rates, or with the rates of the policy year the month falls in
    rather than the one the decrement belongs to, leaves the monthly product no longer
    equal to the annual factor, and the residual is non-zero from the first anniversary.
    Zero except at policy-year starts, and at the last one where the following year would
    fall outside the projection.
    """
    if t % 12 != 0 or t + 12 > proj_len():
        return 0.0
    return (pols_if(t + 12)
            - pols_if(t) * (1.0 - mort_rate(t)) * (1.0 - lapse_rate(t)))


def check_surv_annual():
    """True when the monthly decrements compound back to the annual ones in every year."""
    return all(abs(check_surv_annual_resid(t)) <= roll_fwd_tol        # noqa: F821
               * max(pols_if_init(), 1.0)
               for t in range(proj_len()))


def check_capital_reval_resid(t):
    """The residual of the capital roll-forward in month t.

    Two statements in one signed residual.  Through the **first policy year** the capital
    must still be the capital at issue, because the *participation aux benefices* is
    allocated only to contracts in force at least a year - so the residual there is
    ``capital_pp(t) - capital_0()``, and an implementation that uprated at issue would
    report 50.00 on the anchor cell.  At every **later anniversary** the residual is the
    year's uprating less the rate it should be, which catches a capital that is uprated at
    the wrong frequency, or compounded where the model point asks for a simple uplift.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t < 12:
        return capital_pp(t) - capital_0()
    if t % 12 != 0:
        return 0.0
    step = (capital_0() if reval_simple() else capital_pp(t - 12)) * reval_rate()
    return capital_pp(t) - capital_pp(t - 12) - step


def check_capital_reval():
    """True when the capital is flat through year 1 and steps once a year after it."""
    return all(abs(check_capital_reval_resid(t)) <= roll_fwd_tol      # noqa: F821
               * max(capital_0(), 1.0)
               for t in range(proj_len()))


def check_lapse_gate_resid(t):
    """The premium-stop rate applied in a month in which no premium is payable at all.

    Zero everywhere, and the residual is the rate itself where it is not.  A policy that
    has no premium falling due anywhere in its current policy year has nothing left to
    stop paying, so a decrement there destroys liability silently rather than loudly.  The
    gate is re-stated here through :func:`prem_due_pp` rather than through
    :func:`in_paying_period`, so the check does not merely repeat the branch it is
    checking.
    """
    y = policy_year(t)
    first = 12 * (y - 1)
    last = min(first + 11, proj_len() - 1)
    if any(prem_due_pp(s) > 0.0 for s in range(first, last + 1)):
        return 0.0
    return lapse_rate_mth(t)


def check_lapse_gate():
    """True when no premium-stop decrement is applied where no premium is due."""
    return all(check_lapse_gate_resid(t) == 0.0
               for t in range(proj_len()))


def check_truncation_resid(t):
    """The population left in force when the projection is truncated; zero at the end.

    Non-zero only in the last projected month, where it is everything still alive on both
    strands.  Whole life has no maturity, so anything in force at the limiting age is
    liability dropped off the end of the projection.  :func:`mort_rate` is forced to 1 at
    ``omega_age``, so the population is exhausted inside the horizon; if this were not
    negligible the limiting age would be too low and the model would be understating the
    tail rather than merely rounding it.
    """
    return pols_all(t + 1) if t == proj_len() - 1 else 0.0


def check_truncation():
    """True when nothing is left in force at the limiting age."""
    return (abs(check_truncation_resid(proj_len() - 1))
            <= 1e-9 * max(pols_if_init(), 1.0))


def result_cf():
    """Result table of cashflows, indexed by policy month t = 0 ... proj_len() - 1.

    ``pols_if`` is the premium-paying count at the start of the month, which is the weight
    on premium income and on death outgo; ``pols_paid_up`` is the *reduit* strand, empty on
    every model point where ``reduction_share`` is zero.  ``claims_death`` and
    ``claims_death_paid_up`` are published separately, and the notes'
    single ``claims_death`` column is their sum.  ``liability_cf`` is the notes'
    outgo-positive orientation and ``net_cf`` its exact negative.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_paid_up": [pols_paid_up(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_death_paid_up": [claims(t, "DEATH_PAID_UP") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Policy counts, benefits and rates, indexed by policy month t = 0 ... proj_len()-1."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_paid_up": [pols_paid_up(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_convert": [pols_convert(t) for t in ts],
            "capital_pp": [capital_pp(t) for t in ts],
            "cum_prem_pp": [cum_prem_pp(t) for t in ts],
            "benefit_ill_pp": [benefit_pp(t, "ILL") for t in ts],
            "surr_value_pp": [surr_value_pp(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 112

mort_antiselect_load = 1.25

mort_improvement = 0.0

acc_share = 0.05

accident_cap = 20000.0

assistance_prem_pp = 12.0

instalment_load = 0.022

surr_scale_capital = 5000.0

lapse_overrun_beta = 0.0

expense_acq_pp = 150.0

expense_maint_pp = 24.0

inflation_rate = 0.018

roll_fwd_tol = 1e-10

pd = ("Module", "pandas")
