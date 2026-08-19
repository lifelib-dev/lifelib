# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.IP_UK_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the active-lives anchor cell
    >>> Projection.point_id = 2            # the claims-in-payment worked example

``t`` counts **policy months**, 1-based: ``t = 1`` is the first projected month and
``t = proj_len() = 12 (expiry_age - entry_age)`` the last. The notes index the state
probabilities ``l_H(t)`` and ``l_S(t, z)`` at the **end** of month ``t`` with
``l_H(0) = 1``; the library indexes at the **start** of the month, so
``pols_active(t)`` is the notes' ``l_H(t-1)`` and ``pols_sick_dur(t, z)`` its
``l_S(t-1, z)``. That is deliberate: every cash flow on a ``result_cf()`` row is then
weighted by a state count on the same row.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/income_protection/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``IP_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.IP_UK_S.Data`,
reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
inception_file          data.inception_table()          inception_table.csv
termination_file        data.termination_table()        termination_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for population counts, plural nouns
for cash flows, ``*_rate`` for annual rates and ``*_rate_mth`` for monthly ones,
``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind`` string.
The technical notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
entry_age                  age_at_entry()                  Entry age (ANB)
a                          age(t)                          Attained age (ANB) in month t
y = ceil(t/12)             policy_year(t)                  Policy year containing month t
(none)                     duration(t)                     Completed policy years, y - 1
(none)                     duration_mth(t)                 Months elapsed at end of month t
expiry_age                 expiry_age()                    Age all cover ceases
T = 12(expiry - entry)     proj_len()                      Last projected month
d                          deferred_weeks()                Deferred period in weeks
occ_class                  occ_class()                     CMI occupation class OC1-OC4
status                     status()                        active or in_claim cell
z                          (the duration argument)         Claim duration in months
(none)                     claim_dur_year(z)               Duration year containing z
(none)                     max_dur()                       Longest claim duration tracked
B(y)                       benefit_pp(t)                   Escalated monthly benefit
P(y)                       premium_pp(t)                   Escalated monthly premium
AP(y)                      amount_payable_pp(t)            Amount payable per month
(max benefit formula)      benefit_max_pp()                Contractual maximum benefit
k                          claim_severity                  Severity factor, 1.0
AP/B                       ap_ratio                        Offset/guarantee effect, 1.0
j                          esc_rate()                      Escalation rate
M_esc(y)                   esc_lapse_factor(t)             Premium-shock lapse multiplier
iota_a(a)                  inception_rate(t)               Annual claim inception rate
iota_m(a)                  inception_rate_mth(t)           The same, monthly
M_cycle                    cycle_factor                    Economic-cycle overlay, 1.0
q_H_a(a)                   mort_rate(t)                    Active-life annual mortality
q_H_m(a)                   mort_rate_mth(t)                The same, monthly
w_a(y)                     lapse_rate(t)                   Annual lapse rate in month t
(table)                    lapse_rate_base(t)              Table lapse rate before shock
w_m(y)                     lapse_rate_mth(t)               Monthly lapse rate
rho_a(z)                   rec_rate(z)                     Annual recovery rate
rho_m(z)                   rec_rate_mth(z)                 Monthly recovery rate
q_S_a(z)                   mort_rate_sick(z)               Annual in-claim mortality
q_S_m(z)                   mort_rate_sick_mth(z)           Monthly in-claim mortality
s_S(z)                     claim_surv_step(z)              Monthly in-claim survival
(the three vectors)        claim_rate_vectors()            rho_m, q_S_m and s_S as lists
l_H(t-1)                   pols_active(t)                  In state H at start of month t
l_S(t-1, z)                pols_sick_dur(t, z)             In claim at duration z
l_S(t-1)                   pols_sick(t)                    Total in claim payment
(the whole vector)         sick_cohorts(t)                 l_S(t-1, .) as a list
(none)                     pols_if(t)                      H + S: policies in force
(none)                     pols_if_at(t, timing)           BEF_DECR / AFT_DECR
n(t)                       pols_inception(t)               New claim inceptions
rec(t)                     pols_recovery(t)                Recoveries out of S
dth_S(t)                   pols_death_sick(t)              Deaths in claim
dth_H(t)                   pols_death_active(t)            Deaths in state H
lps(t)                     pols_lapse(t)                   Lapses out of H
(none)                     pols_exit(t)                    Recoveries leaving the model
(none)                     pols_maturity(t)                In force at the policy end date
(none)                     pols_sick_surv(t)               In claim at the end of month t
PREM(t)                    premiums(t)                     Premium income
BEN(t)                     claims(t, "BENEFIT")            Income benefit outgo
0                          claims(t, "DEATH")              Death benefit; always zero
0                          claims(t, "LAPSE")              Surrender outgo; always zero
EXP(t)                     expenses(t)                     Maintenance + claim management
e_m(y), ec_m(y)            expense_maint, expense_claim    Expense levels p.a.
(none)                     inflation_factor(t)             Expense inflation factor
CF(t)                      net_cf(t)                       Net cash flow, income positive
v(t)                       disc_factor(t)                  Worked-example discount factor
(none)                     pv_benefits()                   PV of benefit outgo
a_dis(a0, z0)              annuity_dis()                   Disabled-life annuity factor
=========================  ==============================  ==========================

Three names needed care.

The notes use ``q_H`` and ``q_S`` for the two mortality rates. :func:`mort_rate` is the
**active-life** one, because that is what ``mort_rate`` means in every other model in
this library — the rate applying to the population the projection starts with — and the
in-claim rate is :func:`mort_rate_sick`, keyed by claim duration rather than by month.
Reading a claimant mortality rate out of ``mort_rate`` is the kind of mistake the naming
is there to prevent.

``BEN(t)`` is an income stream, not a lump sum, but it is reached as
``claims(t, "BENEFIT")`` so that the library's one benefit-outgo cells covers it. The
other two kinds are zero and say so: this composite carries **no death benefit** — the
£5,000-£10,000 death benefits two sampled insurers offer are out of scope — and **no
surrender value** at any time.

``z`` is the claim duration in months and ``t`` the policy month. They are different
clocks and the model never mixes them: rates out of state S take ``z``, rates out of
state H take ``t``.

.. rubric:: Three states, and why the model needs all of them

Healthy and active (H), sick and in claim payment (S), dead (D), with lapse as a further
exit from H and **recovery flowing back from S to H**. That is the structure of the
CMI's own graduations, and it is why income protection has two experience bases rather
than one: claim *inception* rates out of H, and claim *termination* rates out of S, the
latter split into recovery and death.

The deferred period is embedded **in the inception basis**, not modelled as a fourth
state. ``iota`` is a claim *payment* inception rate specific to the policy's deferred
period — exactly the quantity the CMI publishes per deferred period — so a sickness
spell that recovers inside the deferred period never leaves H, and a life sick but not
yet in payment stays in H and keeps paying premiums, which is what the contract's
waiver-from-payment-start convention says. No separate "sick, not yet in payment" state
is needed and the lag between onset and payment is absorbed into the calibration of
``iota``. Dual deferred periods and sick-pay-linked deferreds would need spell-level
modelling and are out of scope.

.. rubric:: The in-claim population is two-dimensional

Termination rates depend on how long the claim has already run: 40% a year at duration
one falling to 5% from duration five in the shipped **[std]** basis. So the model tracks
``l_S(t, z)`` cohort by cohort. Collapsing that to a single bucket with a
duration-independent termination rate materially misstates claim run-off, and is the
notes' first-listed pitfall — the duration gradient *is* the defining feature of income
protection terminations.

:func:`sick_cohorts` holds the whole vector for one month and is the model's only
list-valued cells. The alternative — a two-argument ``pols_sick_dur(t, z)`` recursion —
would be ``proj_len() x max_dur()`` separate cells, 130,000 of them on the anchor cell,
each with its own cache entry. Keeping the vector in one cells per month makes it
``proj_len()`` cells with a loop inside, and :func:`pols_sick_dur` then reads an element
out of it so that the notes' two-dimensional object is still addressable by name. The
list is rebuilt rather than mutated on each step, so a caller cannot corrupt the cache
by holding one.

The shipped termination basis suppresses the **age** dimension **[std]**. IP11 is
two-dimensional in age and duration, with claimant mortality duration-dependent to five
years and age-only beyond, and it also has a "run-in" of *increasing* recovery rates
over the first weeks of claim for the shorter deferred periods, which annual duration-year
granularity smooths away. A licensee restoring both dimensions changes
``termination_table.csv`` and the two lookups, and nothing else.

.. rubric:: Where recoveries go, and the two kinds of model point

The notes give two calculations, and the model point's ``recovery_basis`` column says
which one a cell runs:

``recovery_basis = "return_to_h"``
    The notes' processing order step 5: recovered lives re-enter H, resume paying
    premiums and are again exposed to inception. This is the **active-lives** basis and
    every ``active`` model point uses it.

``recovery_basis = "exit"``
    Recovered lives leave the model. This is the **disabled-life annuity** the notes'
    claims-in-payment section values — the expected present value of the benefit until
    recovery, death or expiry — and it is the basis the worked example is computed on.
    Both ``in_claim`` model points use it.

Keeping it a column rather than deriving it from ``status`` matters, because the choice
is a valuation question and not a property of the cell: a claims-in-payment reserve is
the disabled-life annuity, but a full contract-boundary best estimate for the same
policy would carry the post-recovery active phase as well. Running an ``in_claim`` cell
on ``return_to_h`` gives the second reading, and gives a materially different answer,
because recovered lives can and do claim again.

One limitation the notes name and this model inherits: contractually a same-cause
recurrence within 52 weeks restarts payment with **no new deferred period**, and
returning recovered lives to the standard inception basis ignores that. It understates
re-inception at short horizons. The refinement is a post-recovery flag carrying a loaded
inception rate for twelve months, and it is not implemented.

.. rubric:: Premiums come from H alone

Premiums are waived from the start of benefit payment, so :func:`premiums` is carried on
:func:`pols_active` and never on :func:`pols_if`. Projecting premium income from lives in
claim is the notes' second-listed pitfall and overstates income by the whole in-claim
population. Note the asymmetry it creates with escalation: the benefit escalates in
claim and the premium that would have paid for it does not, which is why the escalation
option is inflation-sensitive on exactly the claims that are longest.

.. rubric:: Benefit in arrears, and the month a claim starts

A claim incepting at the end of month ``t`` seeds cohort ``z = 1`` and receives its first
payment at the end of month ``t + 1``. So the benefit is paid on
:func:`pols_sick_surv` — the cohorts that were already in payment at the start of the
month and survived it — and not on :func:`pols_sick` plus new inceptions. Paying the new
inceptions would hand over a full month's benefit at the instant payment starts and
break the equivalence with the inception-annuity decomposition of the same projection.

The contractual daily pro-rating of partial claim months is replaced by whole-month
payment **[std]**: a life recovering mid-month receives nothing for that month here and
a pro-rated amount in reality.

.. rubric:: Expiry truncates everything

All cover and any claim in payment terminate at the policy end date with no value.
:func:`pols_maturity` is that termination, non-zero only in the last month, and it is
what makes the in-force roll-forward close. An untruncated disabled-life annuity
materially overstates the liability for claims incepting near expiry — model point 5 is
a claim at duration 30 months on a policy with 15 years to run, and its benefit stream
stops dead at ``proj_len()``.

.. rubric:: Amount payable is not the same thing as the chosen benefit

Offsets against other income, the minimum benefit guarantee and proportionate benefits
on a partial return to work all move the amount actually paid away from the benefit the
policyholder chose. The base run sets ``AP = B`` through ``ap_ratio`` and the
severity factor ``claim_severity`` to 1 **[std]**, which **overstates** outgo
wherever the maximum-benefit formula bites and understates nothing, since ``AP <= B``
always. A portfolio calibration sets one or both below 1 from claims experience.
:func:`benefit_max_pp` implements the contractual two-band maximum so that
:func:`check_benefit_max` can assert every shipped model point is inside it.

.. rubric:: Discounting, which the rest of the library does not do

Every other model in this library projects **undiscounted** gross liability cash flows
and leaves discounting to the layer that consumes them. This one carries
:func:`disc_factor`, :func:`pv_benefits` and :func:`annuity_dis` as well, because the
notes' worked example is a present value and because the disabled-life annuity is the
object a claims-in-payment reserve is quoted as. They are a **companion**, not part of
the cash flow projection: no line of :func:`result_cf` is discounted, and
``disc_rate`` is the worked example's flat 3% **[std]**, not a valuation basis. A
Solvency UK best estimate discounts these same cash flows on the PRA risk-free term
structure, and the claims-in-payment element is matching-adjustment eligible where it is
organised and managed separately.
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


def age_at_entry():
    """The entry age (ANB) of the selected model point.

    On an ``in_claim`` cell this is the **attained age at the valuation date**, and the
    policy-year clock restarts there **[std]**: the notes give no anniversary offset for
    an in-force claim, so escalation steps at ``t = 13, 25, ...`` from the valuation
    date rather than from the contractual anniversary.  The worked example is level
    cover, where the distinction does not arise.
    """
    return int(model_point()["entry_age"])


def sex():
    """The sex (M / F) of the selected model point.

    Not a smoker split: the IP11 rate structure is sex, deferred period and occupation
    class, and any smoker differentiation sits in insurer pricing, which is not public.
    """
    return model_point()["sex"]


def occ_class():
    """The CMI occupation class, OC1 to OC4 [R1]; 1 is the lightest."""
    v = int(model_point()["occ_class"])
    if v not in (1, 2, 3, 4):
        raise ValueError("invalid occ_class")
    return v


def deferred_weeks():
    """d: the deferred period in weeks, from the 4/8/13/26/52 menu [S6].

    It is not a state in this model: the inception basis is deferred-period-specific, so
    the deferred period enters through :func:`inception_rate` and nowhere else.  See the
    Space docstring.
    """
    v = int(model_point()["deferred_weeks"])
    if v not in (4, 8, 13, 26, 52):
        raise ValueError("invalid deferred_weeks")
    return v


def benefit_mth():
    """B(1): the chosen monthly benefit at issue **[std]**, £2,000 on the base cell."""
    return float(model_point()["benefit_mth"])


def earnings_annual():
    """The annual earnings on the underwriting record, which cap the benefit."""
    return float(model_point()["earnings_annual"])


def expiry_age():
    """The age at which all cover and any claim in payment cease, 50-70 [S1][S3][S5]."""
    return int(model_point()["expiry_age"])


def escalation():
    """``RPI`` or ``none``: whether the escalation option is elected [S1][S2]."""
    v = model_point()["escalation"]
    if v not in ("RPI", "none"):
        raise ValueError("invalid escalation")
    return v


def premium_mth():
    """P(1): the monthly premium at issue **[std]**, a placeholder.

    UK income protection premium rates are not public, so any reference premium is
    constructed.  It is guaranteed level apart from the escalation uplift
    [S1][S3][S5][S7].
    """
    return float(model_point()["premium_mth"])


def premium_basis():
    """``guaranteed``.  Reviewable and age-costed premiums are out of scope.

    A reviewable variation exists - fixed for five years, then reviewed with no
    contractual cap - but the review formulas are insurer-discretionary and undisclosed,
    so any reviewable model would need a **[std]** review rule that no source supports.
    """
    v = model_point()["premium_basis"]
    if v != "guaranteed":
        raise ValueError("invalid premium_basis")
    return v


def status():
    """``active`` (the population starts in H) or ``in_claim`` (it starts in S).

    An in-force portfolio needs both kinds of cell: active lives, and claims already in
    payment carrying their claim duration as an attribute.
    """
    v = model_point()["status"]
    if v not in ("active", "in_claim"):
        raise ValueError("invalid status")
    return v


def recovery_basis():
    """Where recovered lives go: back to H, or out of the model.

    ``return_to_h``
        the notes' processing order step 5 - recovered lives re-enter H,
        resume paying premiums and are again exposed to inception.  The
        **active-lives** basis.

    ``exit``
        recovered lives leave the model, which is the **disabled-life
        annuity** the claims-in-payment valuation uses, and the basis the
        notes' worked example is computed on.

    A column rather than something derived from :func:`status`, because it is a
    valuation question: a claims-in-payment reserve is the disabled-life annuity, but a
    full contract-boundary best estimate for the same policy carries the post-recovery
    active phase too.  See the Space docstring.
    """
    v = model_point()["recovery_basis"]
    if v not in ("return_to_h", "exit"):
        raise ValueError("invalid recovery_basis")
    return v


def claim_duration_months():
    """z0: the claim duration already elapsed on an ``in_claim`` cell; 0 at inception.

    The seeded population enters cohort ``z0 + 1``, since cohort 1 is a claim that has
    just started paying.
    """
    return int(model_point()["claim_duration_months"])


def pols_if_init():
    """Initial number of policies; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_len():
    """Projection length in months: ``12 (expiry_age - entry_age)``.

    All cover and any claim in payment terminate at the policy end date with no value
    [S1][S3][S5][S7][S10], so there is nothing after it.  This is what truncates the
    disabled-life annuity, and an untruncated one materially overstates the liability
    for claims incepting near expiry.
    """
    return 12 * (expiry_age() - age_at_entry())


def duration(t):
    """Completed policy years at the start of month t: ``(t - 1) // 12``."""
    return (t - 1) // 12


def duration_mth(t):
    """Months elapsed from the start of the projection at the end of month t; equal to t.

    ``t`` is 1-based, so the identity is trivial - the cells exists so the monthly
    models in this library share one vocabulary.
    """
    return t


def policy_year(t):
    """y = ceil(t/12): the policy year containing month t; 1 for t = 1..12."""
    return duration(t) + 1


def age(t):
    """a: the attained age (ANB) in the policy year containing month t."""
    return age_at_entry() + duration(t)


def max_dur():
    """The longest claim duration the cohort vector has to carry.

    ``proj_len() + z0 + 1``: a claim seeded at duration ``z0 + 1`` reaches
    ``z0 + proj_len()`` by the last month, and a claim incepting in month 1 reaches
    ``proj_len()``.  Cohorts beyond this are structurally zero.
    """
    return proj_len() + claim_duration_months() + 1


def claim_dur_year(z):
    """The claim duration year containing claim month z: ``(z - 1) // 12 + 1``.

    Duration years beyond the termination table take its last row, which is the shipped
    table's "5+" row.
    """
    return (z - 1) // 12 + 1


def inception_rate(t):
    """iota_a(a): the annual claim payment inception rate out of state H.

    Read from ``inception_table.csv`` at the policy's sex, occupation class and deferred
    period, **linearly** interpolated between pivot ages and linearly extrapolated
    beyond them, then multiplied by the economic-cycle overlay ``cycle_factor``.
    Floored at zero, since linear extrapolation below the first pivot can go negative.

    The rate is a *claim payment* inception rate specific to the deferred period, which
    is exactly what the CMI publishes per deferred period - so the deferred period needs
    no state of its own.  The shipped values are **[std]** proxies shaped like IP11 and
    carry no CMI authority; IP11's own inception rates are additionally known to be
    understated through exposure errors, and licensees must apply the CMI's indicative
    adjustments.
    """
    sub = data.inception_table().loc[                                # noqa: F821
        (sex(), occ_class(), deferred_weeks())]
    ages = sorted(int(a) for a in sub.index)
    x = age(t)
    if x <= ages[0]:
        lo, hi = ages[0], ages[1]
    elif x >= ages[-1]:
        lo, hi = ages[-2], ages[-1]
    else:
        lo = max(a for a in ages if a <= x)
        hi = min(a for a in ages if a > x)
    r_lo = float(sub.loc[lo, "inception_rate"])
    r_hi = float(sub.loc[hi, "inception_rate"])
    r = r_lo + (r_hi - r_lo) * (x - lo) / (hi - lo)
    return max(0.0, r) * cycle_factor                                # noqa: F821


def inception_rate_mth(t):
    """iota_m(a) = 1 - (1 - iota_a)^(1/12): the monthly inception rate **[std]**."""
    return 1.0 - (1.0 - inception_rate(t)) ** (1.0 / 12.0)


def mort_rate(t):
    """q_H_a(a): the **active-life** annual mortality rate.

    A minor decrement in income protection, and a **[std]** proxy shaped like the ONS
    national life tables scaled by ``mort_active_factor``.  Claimant mortality is a
    different rate on a different clock - see :func:`mort_rate_sick`.
    """
    return float(data.mort_table().loc[                              # noqa: F821
        (sex(), age(t)), "mort_rate"]) * mort_active_factor          # noqa: F821


def mort_rate_mth(t):
    """q_H_m(a) = 1 - (1 - q_H_a)^(1/12): the monthly active-life mortality **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def rec_rate(z):
    """rho_a(z): the annual recovery rate at claim duration z months.

    From the duration year containing z, divided by the economic-cycle overlay - a
    recession is believed to slow recoveries as well as raise inceptions, and the
    overlay is a scenario axis rather than a calibrated assumption, held at 1 in the base
    run.  The declining gradient, 40% in year one to 5% from year five, is the defining
    feature of income protection terminations; the values are **[std]** proxies.
    """
    tbl = data.termination_table()                                   # noqa: F821
    y = min(claim_dur_year(z), int(tbl.index.max()))
    return min(1.0, float(tbl.loc[y, "recovery_rate"]) / cycle_factor)  # noqa: F821


def rec_rate_mth(z):
    """rho_m(z) = 1 - (1 - rho_a)^(1/12): the monthly recovery rate **[std]**."""
    return 1.0 - (1.0 - rec_rate(z)) ** (1.0 / 12.0)


def mort_rate_sick(z):
    """q_S_a(z): the annual mortality of a life in claim at duration z months.

    Flat across durations in the shipped **[std]** proxy.  IP11 makes it
    duration-dependent to five years and age-dependent beyond, so this is the crudest
    part of the shipped basis; it is also the smaller of the two termination causes.
    """
    tbl = data.termination_table()                                   # noqa: F821
    y = min(claim_dur_year(z), int(tbl.index.max()))
    return float(tbl.loc[y, "mort_rate_sick"])


def mort_rate_sick_mth(z):
    """q_S_m(z) = 1 - (1 - q_S_a)^(1/12): the monthly in-claim mortality **[std]**."""
    return 1.0 - (1.0 - mort_rate_sick(z)) ** (1.0 / 12.0)


def claim_surv_step(z):
    """s_S(z) = (1 - rho_m)(1 - q_S_m): monthly survival in claim at duration z.

    Recovery first, then death among the non-recovered, as independent decrements
    **[std]** - the notes' processing order for exits from state S.
    """
    return (1.0 - rec_rate_mth(z)) * (1.0 - mort_rate_sick_mth(z))


def claim_rate_vectors():
    """The three per-duration rate vectors, ``(rho_m, q_S_m, s_S)``, built once.

    Element ``z - 1`` of each list is the value at claim duration ``z``, for
    ``z = 1 ... max_dur()``.  Purely a performance shape: :func:`pols_recovery`,
    :func:`pols_death_sick` and :func:`pols_sick_surv` each walk the whole cohort vector
    in every projected month, and reading the rates out of a list rather than calling
    :func:`rec_rate_mth` and friends per element turns ``proj_len() x max_dur()``
    cells lookups into ``max_dur()`` of them - on the anchor cell, four hundred thousand
    down to four hundred.  The scalar cells stay, because they are what a reader looks
    up and what a test asserts against; this is built *from* them, so there is still one
    definition of each rate.
    """
    zs = range(1, max_dur() + 1)
    rec = [rec_rate_mth(z) for z in zs]
    dth = [mort_rate_sick_mth(z) for z in zs]
    return rec, dth, [(1.0 - r) * (1.0 - d) for r, d in zip(rec, dth)]


def esc_rate():
    """j = min(max(RPI, 0), 10%): the escalation rate [S1][S2].

    Zero when the option is not elected.  A flat 3% RPI snapshot **[std]** - future RPI
    is an economic input, not insurer discretion - so the benefit grows 3% a year and
    the premium 4.5%, the x1.5 multiplier.  The 10% cap is an embedded inflation option
    the insurer has written.
    """
    if escalation() != "RPI":
        return 0.0
    return min(max(rpi_rate, 0.0), esc_cap)                          # noqa: F821


def benefit_pp(t):
    """B(y): the escalated monthly benefit in the policy year containing month t.

    Escalates on policy anniversaries and **continues to escalate in claim** [S1][S2],
    which is what makes the disabled-life annuity inflation-sensitive exactly when it is
    longest.  Some contracts instead escalate in-claim amounts on *claim* anniversaries
    with index-lag rules; align the convention with the contract being modelled.
    """
    return benefit_mth() * (1.0 + esc_rate()) ** (policy_year(t) - 1)


def premium_pp(t):
    """P(y): the escalated monthly premium in the policy year containing month t.

    Guaranteed level apart from the escalation uplift of ``1 + 1.5 j`` a year
    [S1][S2][S3][S5][S7].  The premium side compensates for escalation only x1.5 on
    active lives and not at all on lives in claim, where premiums are waived.
    """
    step = 1.0 + esc_prem_mult * esc_rate()                          # noqa: F821
    return premium_mth() * step ** (policy_year(t) - 1)


def benefit_max_pp():
    """The contractual maximum monthly benefit from the two-band earnings formula.

    65% of earnings to the £60,000 breakpoint and 50% above it, capped at £20,000 a
    month and floored at the £1,500 guarantee [S1][S2][S5][S7].  Nothing in the
    projection consumes it - the base run pays :func:`amount_payable_pp` - but
    :func:`check_benefit_max` asserts every model point's chosen benefit is inside it,
    which is the check the underwriting record exists to support.
    """
    e = earnings_annual()
    gross = (ben_band1_rate * min(e, ben_breakpoint)                 # noqa: F821
             + ben_band2_rate * max(0.0, e - ben_breakpoint))        # noqa: F821
    m = min(gross / 12.0, ben_cap_mth)                               # noqa: F821
    return max(m, ben_guarantee_mth)                                 # noqa: F821


def amount_payable_pp(t):
    """AP(y): the amount actually payable per month of full incapacity.

    ``ap_ratio x B(y)`` with ``ap_ratio`` at 1 **[std]**.  Offsets against other
    income, the minimum benefit guarantee and proportionate benefits on a partial return
    to work all push the amount paid below the chosen benefit, so ``AP <= B`` always and
    the base run **overstates** outgo wherever the maximum-benefit formula bites.  A
    portfolio calibration sets ``ap_ratio`` or ``claim_severity`` below 1 from claims
    experience.
    """
    return ap_ratio * benefit_pp(t)                                  # noqa: F821


def esc_lapse_factor(t):
    """M_esc(y): the premium-shock lapse multiplier **[std]**; 1 in the base run.

    ``1 + 2 max(0, 1.5 j - 0.05)`` once the escalation uplift has started, so a 3% RPI
    snapshot gives 4.5% premium growth and no shock, while the 10% cap would give 15%
    growth and a multiplier of 1.2.  Sampled insurers let policyholders decline
    escalation increases, with the option lapsing after two or three consecutive
    refusals; declines are a portfolio-level phenomenon that a single-cell model cannot
    represent, so this multiplier is the aggregate proxy for them.
    """
    if escalation() != "RPI" or policy_year(t) < 2:
        return 1.0
    return 1.0 + esc_lapse_slope * max(                              # noqa: F821
        0.0, esc_prem_mult * esc_rate() - esc_lapse_threshold)       # noqa: F821


def lapse_rate_base(t):
    """The table annual lapse rate in month t **[std]**, before the escalation shock.

    10 / 8 / 6 / 6 / 6 / 4 percent by policy year.  No public UK income protection lapse
    study was retrieved, so the table has no anchor at all and is a pure placeholder.
    Policy years beyond the table take its last row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = policy_year(t)
    return float(tbl.loc[min(y, int(tbl.index.max())), "lapse_rate"])


def lapse_rate(t):
    """w_a(y): the **annual** lapse rate out of state H in month t.

    Applied to lives in H only.  Lives in claim never lapse **[std]**: their premiums are
    waived and the benefit in payment is the most valuable thing they own.
    """
    return min(1.0, lapse_rate_base(t) * esc_lapse_factor(t))


def lapse_rate_mth(t):
    """w_m(y) = 1 - (1 - w_a)^(1/12): the monthly lapse rate **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def sick_cohorts(t):
    """l_S(t-1, .): the in-claim population by claim duration, as a list.

    Element ``z - 1`` is the population in claim payment at the start of month t with
    claim duration ``z`` months, for ``z = 1 ... max_dur()``.  The model's only
    list-valued cells, and the reason is cost: a two-argument recursion would be
    ``proj_len() x max_dur()`` separate cells - 130,000 on the anchor cell - where this
    is ``proj_len()`` cells with a loop inside.  :func:`pols_sick_dur` reads an element
    out of it, so the notes' two-dimensional object is still addressable by name.

    At ``t = 1`` the vector is the seeded state: all zeros on an ``active`` cell, and
    ``pols_if_init()`` at cohort ``z0 + 1`` on an ``in_claim`` one.  Thereafter cohort 1
    is the previous month's inceptions and every other cohort is the previous cohort
    survived one month.  A new list is built on each step rather than the previous one
    mutated, so holding a returned list cannot corrupt the cache.

    Past ``proj_len()`` the vector is all zeros: every claim in payment terminates at the
    policy end date without value, so there is no run-off tail for the roll-forward to
    reconcile against.
    """
    n = max_dur()
    if t > proj_len():
        return [0.0] * n
    if t <= 1:
        seed = pols_if_init() if status() == "in_claim" else 0.0
        z0 = claim_duration_months() + 1
        return [seed if z == z0 else 0.0 for z in range(1, n + 1)]
    prev = sick_cohorts(t - 1)
    surv = claim_rate_vectors()[2]
    out = [pols_inception(t - 1)]
    for z in range(1, n):
        out.append(prev[z - 1] * surv[z - 1])
    return out


def pols_sick_dur(t, z):
    """l_S(t-1, z): the population in claim at the start of month t at duration z."""
    v = sick_cohorts(t)
    return v[z - 1] if 1 <= z <= len(v) else 0.0


def pols_sick(t):
    """l_S(t-1): the total population in claim payment at the start of month t."""
    return sum(sick_cohorts(t))


def pols_sick_surv(t):
    """The population still in claim at the **end** of month t, before new inceptions.

    ``sum over z of l_S(t-1, z) s_S(z)``.  This is what the benefit is paid on: the
    benefit is monthly in arrears, so a claim incepting at the end of month t is not paid
    until the end of month ``t + 1``.
    """
    v = sick_cohorts(t)
    surv = claim_rate_vectors()[2]
    return sum(a * b for a, b in zip(v, surv) if a != 0.0)


def pols_recovery(t):
    """rec(t): recoveries out of state S at the end of month t.

    ``sum over z of l_S(t-1, z) rho_m(z)``.  Where they go depends on
    :func:`recovery_basis`.
    """
    v = sick_cohorts(t)
    rec = claim_rate_vectors()[0]
    return sum(a * b for a, b in zip(v, rec) if a != 0.0)


def pols_death_sick(t):
    """dth_S(t): deaths in claim at the end of month t.

    ``sum over z of l_S(t-1, z)(1 - rho_m(z)) q_S_m(z)`` - recovery first, then death
    among the non-recovered.
    """
    v = sick_cohorts(t)
    rec, dth, _ = claim_rate_vectors()
    return sum(a * (1.0 - r) * d
               for a, r, d in zip(v, rec, dth) if a != 0.0)


def pols_exit(t):
    """Recoveries that leave the model at the end of month t.

    Equal to :func:`pols_recovery` on the ``exit`` recovery basis and zero on
    ``return_to_h``, where the same lives reappear in :func:`pols_active`.  It exists so
    that the population identity closes on both bases.
    """
    return pols_recovery(t) if recovery_basis() == "exit" else 0.0


def pols_active(t):
    """l_H(t-1): the population in state H at the start of month t.

    ``pols_if_init()`` at ``t = 1`` on an ``active`` cell and zero on an ``in_claim``
    one, then the notes' state update: survivors of mortality, lapse and inception, plus
    the month's recoveries where the recovery basis returns them.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return pols_if_init() if status() == "active" else 0.0
    prev = pols_active(t - 1)
    stay = (prev * (1.0 - mort_rate_mth(t - 1)) * (1.0 - lapse_rate_mth(t - 1))
            * (1.0 - inception_rate_mth(t - 1)))
    back = 0.0 if recovery_basis() == "exit" else pols_recovery(t - 1)
    return stay + back


def pols_death_active(t):
    """dth_H(t): deaths out of state H at the end of month t.

    The notes' processing order out of H is **death, then lapse, then inception among
    the survivors** **[std]**.
    """
    return pols_active(t) * mort_rate_mth(t)


def pols_lapse(t):
    """lps(t): lapses out of state H at the end of month t.

    Taken from the survivors of mortality.  Pays nothing: the contract has no cash-in
    value at any time [S4][S5][S7].  Lives in claim never lapse.
    """
    return pols_active(t) * (1.0 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_inception(t):
    """n(t): new claim inceptions at the end of month t, seeding cohort z = 1.

    Taken from the survivors of both mortality and lapse.  Each inception starts a new
    duration cohort, and is not paid until the end of the following month.
    """
    return (pols_active(t) * (1.0 - mort_rate_mth(t))
            * (1.0 - lapse_rate_mth(t)) * inception_rate_mth(t))


def pols_if(t):
    """The number of policies in force at the start of month t: H plus S.

    The weight on the maintenance expense, and the count a reader of ``result_cf()``
    reconciles the rest of the row against.  Note that it is **not** the weight on
    premium income, which comes from :func:`pols_active` alone because premiums are
    waived in claim.
    """
    return pols_active(t) + pols_sick(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside month t.

    ``"BEF_DECR"``
        the start of the month, before any transition; the same number as
        :func:`pols_if`.

    ``"AFT_DECR"``
        the end of the month, once deaths, lapses, recoveries leaving the
        model and - in the last month - the expiry have been taken.  Equal
        to ``pols_if(t + 1)`` everywhere but the last month, where it is
        zero.

    The intermediate points of the other models have no single-population meaning here,
    because two states are moving at once; :func:`pols_active` and :func:`pols_sick`
    expose them instead.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DECR":
        if t < 1 or t >= proj_len():
            return 0.0
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_maturity(t):
    """The population still in force when cover ceases at the policy end date.

    Non-zero only in the last projected month, where all cover and any claim in payment
    terminate without value [S1][S3][S5][S7][S10].  Not a decrement and not a benefit -
    but without it the last month appears to lose lives with no cause, and
    :func:`check_pols_roll_fwd` would not close.
    """
    if t != proj_len():
        return 0.0
    stay = (pols_active(t) * (1.0 - mort_rate_mth(t))
            * (1.0 - lapse_rate_mth(t)) * (1.0 - inception_rate_mth(t)))
    back = 0.0 if recovery_basis() == "exit" else pols_recovery(t)
    return stay + back + pols_inception(t) + pols_sick_surv(t)


def pols_dead_cum(t):
    """Cumulative deaths, from both states, before the start of month t."""
    if t <= 1:
        return 0.0
    return pols_dead_cum(t - 1) + pols_death_active(t - 1) + pols_death_sick(t - 1)


def pols_lapse_cum(t):
    """Cumulative lapses out of state H before the start of month t."""
    if t <= 1:
        return 0.0
    return pols_lapse_cum(t - 1) + pols_lapse(t - 1)


def pols_exit_cum(t):
    """Cumulative recoveries that left the model before the start of month t.

    Zero throughout on the ``return_to_h`` basis, where recoveries never leave.
    """
    if t <= 1:
        return 0.0
    return pols_exit_cum(t - 1) + pols_exit(t - 1)


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y - 1)`` **[std]**.

    Steps on policy anniversaries, not monthly, which is how the notes write it.
    """
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def premiums(t):
    """PREM(t): premium income at the beginning of month t, an inflow.

    Carried on :func:`pols_active` and **never** on :func:`pols_if`.  Premiums are
    waived from the start of benefit payment [S5][S7][S10][S11], so projecting income
    from lives in claim overstates it by the whole in-claim population - the notes'
    second-listed pitfall.  Lives sick but still inside the deferred period do pay, and
    they are in H, so they are counted correctly without a state of their own.
    """
    return premium_pp(t) * pols_active(t)


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"BENEFIT"``
        ``k x AP(y) x`` :func:`pols_sick_surv`, the monthly income benefit,
        paid in arrears at the end of the month to lives in claim throughout
        it.  New inceptions are excluded: a claim incepting at the end of
        month t is not paid until the end of month ``t + 1``.

    ``"DEATH"``
        zero.  This composite carries no death benefit; the £5,000-£10,000
        death benefits two sampled insurers offer are out of scope, and would
        add a ``deaths x DB`` term here.

    ``"LAPSE"``
        zero.  There is no cash-in value at any time [S4][S5][S7].

    The two zero kinds are published rather than omitted so that the product facts are
    stated instead of inferred from a missing column.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("BENEFIT", "DEATH", "LAPSE"))
    if kind == "BENEFIT":
        return claim_severity * amount_payable_pp(t) * pols_sick_surv(t)  # noqa: F821
    if kind in ("DEATH", "LAPSE"):
        return 0.0
    raise ValueError("invalid kind")


def expenses(t):
    """EXP(t): maintenance and claim-management expense in month t **[std]**.

    £60 per policy a year on every policy in force, plus £300 a year on every claim in
    payment, both a twelfth at a time and both inflating at 3%.  The claim-management
    load is what makes a long claim expensive to administer as well as to pay.
    """
    maint = expense_maint / 12.0 * inflation_factor(t) * pols_if(t)   # noqa: F821
    claim_mgmt = (expense_claim / 12.0 * inflation_factor(t)          # noqa: F821
                  * pols_sick(t))
    return maint + claim_mgmt


def net_cf(t):
    """CF(t) = PREM(t) - BEN(t) - EXP(t): the net cash flow of month t, income positive.

    The notes' own sign, and the library-wide one, so there is no outgo-positive
    ``liability_cf`` companion.  Death and lapse generate no payment at all on this
    product.
    """
    return premiums(t) - claims(t) - expenses(t)


def disc_factor(t):
    """v(t) = (1 + i)^(-t/12): the worked example's flat discount factor **[std]**.

    A **companion to** the cash flow projection, not part of it: no line of
    :func:`result_cf` is discounted, and every other model in this library projects
    undiscounted gross cash flows and leaves discounting to the layer that consumes them.
    It exists because the notes' worked example is a present value and because the
    disabled-life annuity is the object a claims-in-payment reserve is quoted as.  A
    Solvency UK best estimate discounts these same cash flows on the PRA risk-free term
    structure instead of a flat 3%.
    """
    return (1.0 + disc_rate) ** (-t / 12.0)                          # noqa: F821


def pv_benefits():
    """The present value of benefit outgo over the whole projection, at ``disc_rate``.

    On an ``in_claim`` cell run on the ``exit`` recovery basis this is the
    claims-in-payment liability the notes value.  See :func:`disc_factor` for why
    discounting appears in this model and nowhere else in the library.
    """
    return sum(claims(t, "BENEFIT") * disc_factor(t)
               for t in range(1, proj_len() + 1))


def annuity_dis():
    """a_dis: the disabled-life annuity factor per £1 a month of amount payable.

    ``pv_benefits() / AP(1)``, which on an ``in_claim`` cell run on the ``exit`` basis is
    the notes' ``a_dis(a0, z0)`` exactly: the expected present value of the escalating
    benefit until recovery, death or expiry, truncated at the policy end date.  On an
    ``active`` cell the same expression is the inception-annuity decomposition of the
    active-lives projection - the value of all *future* claims per unit of benefit - and
    is a different object with the same units.
    """
    return pv_benefits() / amount_payable_pp(1)


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1)`` less deaths from both states, lapses, recoveries
    leaving the model and the expiry.  Inceptions and returning recoveries are absent
    because they move lives *between* states rather than out of the policy count - which
    is the point of running the check on ``H + S`` rather than on either state alone.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death_active(t) - pols_death_sick(t) - pols_lapse(t)
            - pols_exit(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives
    the signed residual of the month that failed.  The tolerance scales with
    ``pols_if_init()``, since the residual accumulates rounding on that many policies.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(1, proj_len() + 1))


def check_states_resid(t):
    """The three-state population identity residual at the start of month t; zero.

    ``H + S + cumulative deaths + cumulative lapses + cumulative exits`` must equal the
    starting population in every month.  This is the check that catches a leak in the
    cohort machinery: a mis-indexed duration shift drops population out of S with no
    corresponding exit, and nothing else in the model would notice.
    """
    return (pols_active(t) + pols_sick(t) + pols_dead_cum(t)
            + pols_lapse_cum(t) + pols_exit_cum(t) - pols_if_init())


def check_states():
    """True when the three-state population identity holds in every projected month.

    No argument, one bool over all t, the library-wide shape of a ``check_*`` cells;
    :func:`check_states_resid` gives the signed residual of the month that failed.
    """
    return all(abs(check_states_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(1, proj_len() + 1))


def check_benefit_max():
    """True when the chosen benefit is inside the contractual maximum.

    ``B(1) <= benefit_max_pp() / tolerance``, the two-band earnings formula with the 90%
    tolerance that stops a small fall in earnings cutting an in-force benefit
    [S1][S2][S5][S7].  Unlike the other two checks this is a **validation of the model
    point** rather than an identity of the projection: a benefit above the maximum is a
    policy that could not have been written, and the underwriting record is on the model
    point precisely so that it can be checked.
    """
    return benefit_mth() <= benefit_max_pp() / ben_tolerance + 1e-9   # noqa: F821


def result_cf():
    """Result table of cashflows, indexed by policy month t.

    ``pols_if`` is H plus S at the start of the month.  ``pols_active`` is published
    beside it because it, and not ``pols_if``, is the weight on premium income - the
    difference between the two columns is the population whose premiums are waived.
    Nothing here is discounted; see :func:`disc_factor`.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_active": [pols_active(t) for t in ts],
            "pols_sick": [pols_sick(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_benefit": [claims(t, "BENEFIT") for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_states():
    """Result table of state movements and rates, indexed by policy month t."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_active": [pols_active(t) for t in ts],
            "pols_sick": [pols_sick(t) for t in ts],
            "pols_inception": [pols_inception(t) for t in ts],
            "pols_recovery": [pols_recovery(t) for t in ts],
            "pols_death_active": [pols_death_active(t) for t in ts],
            "pols_death_sick": [pols_death_sick(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "inception_rate": [inception_rate(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

cycle_factor = 1.0

mort_active_factor = 1.0

ap_ratio = 1.0

claim_severity = 1.0

rpi_rate = 0.03

esc_cap = 0.1

esc_prem_mult = 1.5

esc_lapse_slope = 2.0

esc_lapse_threshold = 0.05

ben_band1_rate = 0.65

ben_band2_rate = 0.5

ben_breakpoint = 60000.0

ben_cap_mth = 20000.0

ben_guarantee_mth = 1500.0

ben_tolerance = 0.9

expense_maint = 60.0

expense_claim = 300.0

inflation_rate = 0.03

disc_rate = 0.03

pd = ("Module", "pandas")