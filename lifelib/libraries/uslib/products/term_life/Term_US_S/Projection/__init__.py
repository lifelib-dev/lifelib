# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Term_US_S` model; holds all formulas.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the anchor cell
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/term_life/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_US_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation. A test asserts this by round-tripping the model together
with its inputs.

:func:`~.Term_US_S.Data.input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        data.model_point_table()         model_point_table.csv
premium_rates_file      data.premium_rates()             premium_rates.csv
mort_table_file         data.mort_table()                mort_table.csv
class_factor_file       data.class_factor_table()        class_factor_table.csv
shock_lapse_file        data.shock_lapse_table()         shock_lapse_table.csv
======================  ==========================  ==============================

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name. No formula changes.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_pp`` for per-policy amounts — and, for the monthly grid, the
``duration_mth`` / ``duration`` / ``policy_year`` triple that ``savings.CashValue_SE``
and the UL family in this library use. The technical notes use compact actuarial
symbols instead.

.. rubric:: The time index

``t`` counts **policy months**, 0-based, the same clock ``basiclife.BasicTerm_S``
runs on: ``t = 0`` is the issue month, period ``t`` runs from time ``t`` to time
``t + 1``, ``pols_if(t)`` is the count at time ``t`` (so ``pols_if(0) ==
pols_if_init()``), and the frame is ``t = 0 .. proj_len() - 1`` with
``proj_len() = 12 * (95 - age_at_entry())`` months to expiry at attained age 95.

Everything contractual about this product is nevertheless on an **annual** cycle —
the guaranteed premium schedule, the ART renewals, the shock lapse at the level-period
end — so the policy year is derived and used as a lookup key throughout:
``duration(t) = t // 12`` is the completed policy years at the start of month ``t``,
``policy_year(t) = duration(t) + 1`` is the contractual 1-based label, and the attained
age is ``age(t) = age_at_entry() + duration(t)``. The frame is indexed by ``t``; the
policy year is never indexed by.

The two-speed structure that follows is the library's convention, asserted by
``tests/test_model_conventions.py``: ``mort_rate(t)`` and ``lapse_rate(t)`` are the
**annual** rates of the policy year containing month ``t`` — the vectors the technical
notes tabulate — and ``mort_rate_mth(t)`` and ``lapse_rate_mth(t)`` are the monthly
rates actually applied, ``1 - (1 - q)^(1/12)``. The mapping is:

=================  ========================================================  ===============================
Notes symbol       Cells                                                     Meaning
=================  ========================================================  ===============================
x                  age_at_entry                                              Issue age (ANB)
x + dur            age(t)                                                    Attained age in month t
n                  policy_term                                               Level period in years
F                  sum_assured                                               Face amount
t = 0..12(95-x)-1  proj_len                                                  Number of months; frame ends at proj_len - 1
dur(t)             duration(t)                                               Completed policy years at month t
(t)                duration_mth(t)                                           Completed policy months at month t
dur(t) + 1         policy_year(t)                                            Policy year, the 1-based contractual label
l(t)               pols_if(t)                                                In-force at start of month t (time t)
(l(0))             pols_if_init                                              In-force at issue
d(t)               pols_death(t)                                             Deaths in month t
s(t)               pols_surv(t)                                              Survivors to end of month t
x(t)               pols_lapse(t)                                             Lapses at end of month t
c(t)               pols_conv(t)                                              Conversions at end of month t
(none)             pols_maturity(t)                                          Expiries at attained age 95
q(t)               mort_rate(t)                                              Annual mortality, all factors applied
q_m(t)             mort_rate_mth(t)                                          The monthly rate actually applied
(q_base)           mort_rate_base(t)                                         Base table rate before factors
w(t)               lapse_rate(t)                                             Annual lapse rate, incl. the shock
w_m(t)             lapse_rate_mth(t)                                         The monthly rate actually applied
w(n-1)             shock_lapse_rate                                          Shock lapse, in full at month 12n - 1
cv(t)              conv_rate(t)                                              Annual conversion rate
cv_m(t)            conv_rate_mth(t)                                          The monthly rate actually applied
M(d)               plt_mort_factor(d)                                        PLT mortality deterioration, d = policy_year - n
M(1)               plt_mort_factor_init                                      M(1) actually used
(M(1) rule)        plt_mort_factor_init_formula                              The notes' formula for M(1)
J                  jump_ratio                                                AP(12n)/AP(12n - 1), fee included
AP(t)              premium_pp_ann(t)                                         Guaranteed annualized premium, policy year of t
(modal)            premium_pp(t)                                             Premium per policy actually due in month t
(modal factor)     modal_factor                                              Modal factor of the model point's premium mode
(modal cycle)      prem_cycle                                                Months between instalments
(due month)        prem_due(t)                                               Whether a modal premium falls due in month t
G(t)               premiums(t)                                               Premium income
K(t)               commissions(t)                                            Commission
k(t)               comm_rate(t)                                              Commission rate
X(t)               premium_taxes(t)                                          Premium tax
E(t)               expenses(t)                                               Acquisition + maintenance
DC(t)              claims(t)                                                 Death claims
CV(t)              conv_credits(t)                                           Conversion credit outflow
NetCF(t)           net_cf(t)                                                 Net cash flow
phase(t)           phase(t)                                                  LEVEL / PLT / EXPIRED
conv_elig(t)       conv_elig(t)                                              Conversion eligibility
(none)             result_cf_annual()                                        result_cf() summed into policy years
=================  ========================================================  ===============================

Three notes on the mapping. The notes write deaths as ``d(t)`` while also using ``d``
as the post-level-term duration index in ``M(d)``; the ``pols_death`` / ``plt_mort_factor``
split removes that collision. The notes' ``x(t)`` (lapses) and ``X(t)`` (premium tax)
differ only by case, which ``pols_lapse`` and ``premium_taxes`` separate. And
``pols_maturity`` has no symbol in the notes at all — see below.

.. rubric:: The shock lapse is not spread

Every ordinary decrement is converted to a monthly rate at ``1 - (1 - q)^(1/12)``, so
twelve months of it compound back to exactly the annual rate the notes tabulate. The
shock lapse is the one exception the notes make explicitly: it is **not** spread, but
applied in full at the end of the final level-period month, ``t = 12n - 1``,
immediately before the first ART premium falls due at ``t = 12n``. Its policy year's
annual rate ``w(n-1)`` *is* the shock, so :func:`lapse_rate_mth` returns zero in the
other eleven months of that year and the shock itself in the last one.

That is what makes the two grids reconcile: because the ordinary monthly rates
compound to the annual ones and the shock falls at a year boundary, the in-force
**at every policy anniversary** is identical to the annual-step model's
— ``pols_if(12k)`` here equals ``pols_if(k)`` there, to floating-point. The cash flows
are not identical and are not meant to be: claims now fall at the end of the month of
death rather than the end of the policy year, maintenance expense accrues monthly, and
a modal premium is collected when it is contractually due. Those timing differences
are the reason for the monthly grid. :func:`result_cf_annual` sums the frame into
policy years so the two can be laid side by side.

.. rubric:: Premium mode

``premium_pp(t)`` is the premium **actually collected in month t**: the model point's
``premium_mode`` picks the modal factor (:func:`modal_factor`) and the payment months
(:func:`prem_cycle`) — annual in month 0 of each policy year, semi-annual every sixth
month, quarterly every third, monthly every month — and the annualized guaranteed
premium ``AP(t)`` the notes tabulate is :func:`premium_pp_ann`. Modal loading is
inside the factor (twelve monthly payments come to 0.99996 of the annual premium, six
two semi-annual instalments to 1.04 of it) exactly as the specimen prints it [S6]. The
jump ratio and the conversion credit are both on ``AP``, which is what keeps them
mode-independent; commission is a *rate* keyed by policy year applied to the premium
actually collected, so a modal payer earns it in instalments too.

.. rubric:: pols_maturity

The notes give the roll-forward as ``l(t+1) = l(t)(1-q_m)(1-cv_m)(1-w_m)`` and,
separately, the rule ``l(t) = 0 for x + duration(t) >= 95``. Those do not reconcile in
the final period of the frame, ``t = proj_len() - 1``: its survivors neither die, lapse
nor convert — their coverage simply runs out. Without a term for that, the roll-forward
appears to lose lives with no cause. ``pols_maturity(t)`` names it, zero in every period
but the last, so that

    pols_if(t) - pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_conv(t) + pols_maturity(t)

holds for every ``t`` in the frame. It is bookkeeping determined by the notes' own
rules, not an added assumption. The name follows ``BasicTerm_S.pols_maturity``.
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
    return data.model_point_table().loc[point_id]                          # noqa: F821


def age_at_entry():
    """The issue age (ANB) of the selected model point."""
    return int(model_point()["age_at_entry"])


def sex():
    """The sex of the selected model point."""
    return model_point()["sex"]


def rate_class():
    """The underwriting class of the selected model point."""
    return model_point()["rate_class"]


def plan():
    """The plan code of the selected model point (T10 / T20 / T30)."""
    return model_point()["plan"]


def sum_assured():
    """The face amount of the selected model point."""
    return float(model_point()["sum_assured"])


def pols_if_init():
    """Initial number of policies in-force."""
    return float(model_point()["pols_if_init"])


def premium_mode():
    """The premium mode of the selected model point: A, SA, Q or M [S6]."""
    return model_point()["premium_mode"]


def band():
    """Face-amount band 1-4 **[std]**; the anchor cell is band 1."""
    f = sum_assured()
    return 1 if f < 250000 else 2 if f < 500000 else 3 if f < 1000000 else 4


def policy_term():
    """The level premium period in years, from the plan code."""
    return int(plan()[1:])


def proj_len():
    """The number of policy **months** projected: coverage ends at attained age 95.

    ``12 * (95 - age_at_entry())``. The frame is ``t = 0, 1, ..., proj_len() - 1``;
    ``proj_len()`` is its exclusive end and the row count of :func:`result_cf`.
    """
    return 12 * (expiry_age - age_at_entry())                       # noqa: F821


def duration_mth(t):
    """Completed policy months at the start of month t.

    ``t`` itself, since every model point in this product is projected from issue.
    The cells exists so the monthly vocabulary reads the same here as in the UL family
    and ``savings.CashValue_SE``, where an in-force point can open mid-policy.
    """
    return t


def duration(t):
    """Completed policy years at the start of month t, ``duration_mth(t) // 12``.

    0 throughout the first policy year. Every contractual schedule in this product is
    annual, so this is what the attained age and the premium schedule are read at.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """The contractual policy year containing month t, ``duration(t) + 1``.

    A 1-based label derived from ``t``, never indexed by: the guaranteed premium
    schedule in ``premium_rates.csv`` is keyed by it, and so are the annual decrement
    vectors.
    """
    return duration(t) + 1


def age(t):
    """The attained age (ANB) in month t: ``age_at_entry() + duration(t)``.

    Age changes on the policy anniversary rather than on the birthday, which is the
    ANB convention the whole model is built on **[std]**.
    """
    return age_at_entry() + duration(t)


def modal_factor():
    """The model point's modal factor: the fraction of AP collected per instalment [S6].

    Annual 1.0, semi-annual 0.52, quarterly 0.27, monthly 0.08333 — the specimen's own
    scale, so the modal loading is inside the factor. Each is its own Reference, so a
    carrier's own scale drops in without a formula change.
    """
    m = premium_mode()
    if m == "A":
        return modal_factor_a                                        # noqa: F821
    elif m == "SA":
        return modal_factor_sa                                       # noqa: F821
    elif m == "Q":
        return modal_factor_q                                        # noqa: F821
    elif m == "M":
        return modal_factor_m                                        # noqa: F821
    else:
        raise ValueError("invalid premium mode")


def prem_cycle():
    """Months between premium instalments: A 12, SA 6, Q 3, M 1.

    Arithmetic of the mode rather than an assumption, so it is written here rather than
    held in a Reference.
    """
    return {"A": 12, "SA": 6, "Q": 3, "M": 1}[premium_mode()]


def prem_due(t):
    """Whether a modal premium falls due at the beginning of month t.

    Payments start at issue and repeat on the mode's own cycle: annual in month 0 of
    each policy year, semi-annual every sixth month, quarterly every third, monthly
    every month.
    """
    return duration_mth(t) % prem_cycle() == 0


def premium_pp_ann(t):
    """AP(t): the guaranteed **annualized** gross premium per policy, fee included.

    The notes' ``AP``, looked up in ``premium_rates.csv`` at ``policy_year(t)``. It is
    the base for the jump ratio and the conversion credit, neither of which should move
    with the premium mode; :func:`premium_pp` is what is actually collected in month t,
    and it is that instalment — not ``AP`` — that :func:`commissions` and
    :func:`premium_taxes` are charged on.
    """
    key = (plan(), sex(), rate_class(), band(), policy_year(t))
    return float(data.premium_rates().loc[key, "premium_pp"])               # noqa: F821


def premium_pp(t):
    """The premium per policy actually due at the beginning of month t.

    ``modal_factor() * AP(t)`` in a payment month, zero otherwise.
    """
    return modal_factor() * premium_pp_ann(t) if prem_due(t) else 0.0


def jump_ratio():
    """Initial premium jump ratio, fee included: the first ART annualized premium over
    the last level one, ``premium_pp_ann(12n) / premium_pp_ann(12n - 1)`` (policy years
    n+1 and n)."""
    n = policy_term()
    return premium_pp_ann(12 * n) / premium_pp_ann(12 * n - 1)


def plt_mort_factor_init_formula():
    """The notes' rule for M(1): min(8.0, 1 + 0.55*(J-1)) **[std]**.

    Returns 3.4514 for the anchor cell, where the worked example uses 3.50. Not used
    unless the model point leaves plt_mort_factor_override blank.
    """
    return min(8.0, 1.0 + 0.55 * (jump_ratio() - 1.0))


def plt_mort_factor_init():
    """M(1) actually used: the model point's override if given, else the formula."""
    o = model_point()["plt_mort_factor_override"]
    return plt_mort_factor_init_formula() if pd.isna(o) else float(o)  # noqa: F821


def plt_mort_factor(d):
    """Post-level-term mortality deterioration at PLT duration d; grades to 2.00 **[std]**.

    ``d`` is the notes' PLT duration in **years**, ``d = policy_year(t) - n``: ``d = 1``
    in the first post-level-term policy year (months ``t = 12n .. 12n + 11``). It is not
    the frame index ``t``.
    """
    return max(2.0, plt_mort_factor_init() - 0.15 * (d - 1)) if d >= 1 else 1.0


def class_factor():
    """Underwriting-class multiplier on the base mortality table **[std]**."""
    return float(data.class_factor_table().loc[rate_class(), "factor"])      # noqa: F821


def mort_rate_base(t):
    """Base-table **annual** mortality rate at the attained age in month t, ``age(t)``."""
    return float(data.mort_table().loc[age(t), "mort_rate"])                 # noqa: F821


def mort_rate(t):
    """The **annual** mortality rate of the policy year containing month t.

    Base x class factor x PLT deterioration. The PLT duration is
    ``d = policy_year(t) - n``, so the multiplier applies from ``t = 12n`` (``d = 1``)
    on. :func:`mort_rate_mth` is the rate actually applied in the month.
    """
    d = policy_year(t) - policy_term()
    return mort_rate_base(t) * class_factor() * (plt_mort_factor(d) if d >= 1 else 1.0)


def mort_rate_mth(t):
    """q_m(t): the monthly mortality rate applied in month t **[std]**.

    ``1 - (1 - q)^(1/12)`` on the policy year's annual rate, so twelve months of it
    compound back to exactly that rate — the notes' own conversion.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def shock_lapse_rate():
    """Shock lapse at the end of the level period, by jump-ratio bucket **[std]**."""
    j = jump_ratio()
    for _, r in data.shock_lapse_table().iterrows():                        # noqa: F821
        if r["jump_lo"] < j <= r["jump_hi"]:
            return float(r["shock_lapse_rate"])
    return float(data.shock_lapse_table().iloc[-1]["shock_lapse_rate"])     # noqa: F821


def lapse_rate(t):
    """The **annual** lapse rate of the policy year containing month t **[std]**.

    The notes' ``w`` vector, keyed by ``duration(t)``. Level period
    (``duration = 0 .. n-1``): 6% in policy year 1, 5% in year 2, 4% in years 3..n-2,
    6% anticipatory in year n-1, and the shock in year n. Post-level term: 30%, 15%,
    then 10% by PLT duration ``d = policy_year(t) - n``.

    :func:`lapse_rate_mth` is the rate actually applied in the month, and it treats the
    shock year specially — see there.
    """
    n = policy_term()
    y = duration(t)
    if y < n - 1:
        if y == 0:
            return 0.06
        if y == 1:
            return 0.05
        if y == n - 2:
            return 0.06
        return 0.04
    if y == n - 1:
        return shock_lapse_rate()
    d = policy_year(t) - n
    return 0.30 if d == 1 else 0.15 if d == 2 else 0.10


def lapse_rate_mth(t):
    """w_m(t): the lapse rate applied at the end of month t **[std]**.

    ``1 - (1 - w)^(1/12)`` on the policy year's annual rate in every month except those
    of the final level-period year. The notes are explicit that the shock is **not**
    spread: that year's annual rate *is* the shock, so it falls in full at the end of
    the final level-period month, ``t = 12n - 1`` — immediately before the first ART
    premium is due at ``t = 12n`` — and the other eleven months of the year carry no
    ordinary lapse at all.
    """
    n = policy_term()
    if duration(t) == n - 1:
        return shock_lapse_rate() if t == 12 * n - 1 else 0.0
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def conv_elig(t):
    """True while convertible: within the level period and attained age below 70."""
    return duration(t) < policy_term() and age(t) < 70


def conv_rate(t):
    """The **annual** conversion rate of the policy year containing month t **[std]**.

    Zero outside the eligibility window; ``conv_rate_final`` in the last eligible
    policy year, ``conv_rate_base`` before it. Both ship at 0, as the worked example
    requires.
    """
    if not conv_elig(t):
        return 0.0
    return conv_rate_final if not conv_elig(t + 12) else conv_rate_base  # noqa: F821


def conv_rate_mth(t):
    """cv_m(t): the monthly conversion rate applied at the end of month t **[std]**.

    ``1 - (1 - cv)^(1/12)`` on the policy year's annual rate, the same conversion the
    other voluntary decrement takes.
    """
    return 1.0 - (1.0 - conv_rate(t)) ** (1.0 / 12.0)


def phase(t):
    """LEVEL (``duration < n``), PLT (to expiry) or EXPIRED (``t >= proj_len()``)."""
    if t >= proj_len():
        return "EXPIRED"
    return "LEVEL" if duration(t) < policy_term() else "PLT"


def pols_if(t):
    """Number of policies in-force at the start of month t, i.e. at time t.

    ``pols_if(0) == pols_if_init()``; zero from ``t = proj_len()`` on, when coverage has
    expired at attained age 95.
    """
    if t == 0:
        return pols_if_init()
    if t >= proj_len():
        return 0.0
    return (pols_if(t - 1) * (1 - mort_rate_mth(t - 1))
            * (1 - conv_rate_mth(t - 1)) * (1 - lapse_rate_mth(t - 1)))


def pols_death(t):
    """Number of deaths occurring in month t."""
    return pols_if(t) * mort_rate_mth(t)


def pols_surv(t):
    """Number of policies surviving to the end of month t, before voluntary decrements."""
    return pols_if(t) * (1 - mort_rate_mth(t))


def pols_conv(t):
    """Number of conversions at the end of month t."""
    return pols_surv(t) * conv_rate_mth(t)


def pols_lapse(t):
    """Number of lapses at the end of month t, including the shock at ``t = 12n - 1``."""
    return pols_surv(t) * (1 - conv_rate_mth(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Number of policies whose coverage ends at attained age 95.

    Non-zero only in the final period of the frame, ``t = proj_len() - 1``. Not a
    decrement - the contract runs out - but needed for the in-force roll-forward to
    close; see the Space docstring.
    """
    if t != proj_len() - 1:
        return 0.0
    return (pols_if(t) * (1 - mort_rate_mth(t))
            * (1 - conv_rate_mth(t)) * (1 - lapse_rate_mth(t)))


def comm_rate(t):
    """Commission rate **[std]**: 80% in policy year 1 (``duration(t) == 0``), 5% to the
    end of the level period, 2% after. It is a rate on the premium collected, so a
    modal payer pays it in instalments too."""
    y = duration(t)
    return 0.80 if y == 0 else (0.05 if y < policy_term() else 0.02)


def inflation_factor(t):
    """The expense inflation factor in month t, ``(1 + inflation_rate) ** (t / 12)``.

    Compounded on the monthly grid rather than stepped at anniversaries: on an annual
    model the factor can only move once a year, and the monthly refinement is one of
    the things the finer grid buys.
    """
    return (1 + inflation_rate) ** (t / 12)                          # noqa: F821


def premiums(t):
    """Premium income in month t, at the beginning of the month."""
    return premium_pp(t) * pols_if(t)


def commissions(t):
    """Commission in month t **[std]**."""
    return comm_rate(t) * premiums(t)


def premium_taxes(t):
    """Premium tax in month t **[std]**."""
    return premium_tax_rate * premiums(t)                            # noqa: F821


def expenses(t):
    """Acquisition (``t = 0`` only) and inflating maintenance expenses in month t **[std]**.

    One twelfth of the annual maintenance charge accrues each month, so a policy that
    runs a full year carries the same charge as it did on the annual grid — but it is
    now borne by the in-force of each month rather than of the anniversary, which is
    what makes a decrementing block cost less.
    """
    acq = expense_acq if t == 0 else 0.0                             # noqa: F821
    return acq + expense_maint / 12 * inflation_factor(t) * pols_if(t)   # noqa: F821


def claims(t):
    """Death claims incurred in month t, paid at the end of the month.

    Face amount only: the notes' simplification (i) — the pro-rata unearned-premium
    refund and the due-unpaid-premium deduction on death [S6] are not modelled. On the
    monthly grid the item is bounded by one modal premium, so it is immaterial by
    construction for a monthly payer and at most one annual premium on the deceased
    cohort for an annual one.
    """
    return sum_assured() * pols_death(t)


def conv_credits(t):
    """Conversion credit outflow: one **annualized** premium per conversion, after the
    first policy year (``duration(t) >= 1``). The credit is contractual and stated on
    the annual premium [S6], so it does not move with the premium mode."""
    return premium_pp_ann(t) * pols_conv(t) if duration(t) >= 1 else 0.0


def net_cf(t):
    """Net cash flow in month t."""
    return (premiums(t) - commissions(t) - premium_taxes(t)
            - expenses(t) - claims(t) - conv_credits(t))


def result_cf():
    """Result table of cashflows, one row per **month** ``t = 0 .. proj_len() - 1``."""
    ts = list(range(proj_len()))
    return pd.DataFrame(
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims": [claims(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "conv_credits": [conv_credits(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),
    )


def result_cf_annual():
    """:func:`result_cf` summed into policy years, indexed by ``policy_year``.

    Every cash flow column is the total of its twelve months; ``pols_if`` is the count
    at the **start** of the policy year, ``pols_if(12 * (policy_year - 1))``, which is
    the number the annual-step model carried on the same row.

    On the shipped annual-mode points the two grids agree exactly on five columns —
    ``pols_if``, ``premiums``, ``commissions``, ``premium_taxes`` and ``conv_credits`` —
    because an annual premium is collected on the anniversary and weighted by the
    anniversary in force under either grid, and the other three are rates on it. They do
    **not** agree on ``claims`` or ``expenses``, which now fall where they happen rather
    than at the anniversary, and so not on ``net_cf``. That gap is the point of the finer
    grid — see the Space docstring.
    """
    df = result_cf()
    years = pd.Index([duration(t) + 1 for t in df.index], name="policy_year")
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

expiry_age = 95

modal_factor_a = 1.0

modal_factor_sa = 0.52

modal_factor_q = 0.27

modal_factor_m = 0.08333

premium_tax_rate = 0.02

expense_acq = 300.0

expense_maint = 30.0

inflation_rate = 0.02

conv_rate_base = 0.0

conv_rate_final = 0.0

pd = ("Module", "pandas")
