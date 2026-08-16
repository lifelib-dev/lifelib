# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The only Space in the :mod:`~.Term_US_A` model; holds all formulas and data.

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
``Term_US_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation. A test asserts this by round-tripping the model together
with its inputs.

:func:`~.Term_US_A.Data.input_dir` resolves the directory from ``_model.path.parent`` at run time, so
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
rates, ``*_pp`` for per-policy amounts. The technical notes use compact actuarial
symbols instead. The mapping is:

============  ========================================================  ===============================
Notes symbol  Cells                                                     Meaning
============  ========================================================  ===============================
x             age_at_entry                                              Issue age (ANB)
x + t - 1     age(t)                                                    Attained age in policy year t
n             policy_term                                               Level period in years
F             sum_assured                                               Face amount
t = 1..95-x   proj_len                                                  Last policy year
l(t)          pols_if(t)                                                In-force at start of year t
(l(1))        pols_if_init                                              In-force at issue
d(t)          pols_death(t)                                             Deaths in year t
s(t)          pols_surv(t)                                              Survivors to end of year t
x(t)          pols_lapse(t)                                             Lapses at end of year t
c(t)          pols_conv(t)                                              Conversions at end of year t
(none)        pols_maturity(t)                                          Expiries at attained age 95
q(t)          mort_rate(t)                                              Mortality, all factors applied
(q_base)      mort_rate_base(t)                                         Base table rate before factors
w(t)          lapse_rate(t)                                             Lapse rate, incl. the shock
w(n)          shock_lapse_rate                                          Shock lapse at level-period end
cv(t)         conv_rate(t)                                              Conversion rate
M(d)          plt_mort_factor(d)                                        PLT mortality deterioration
M(1)          plt_mort_factor_init                                      M(1) actually used
(M(1) rule)   plt_mort_factor_init_formula The notes' formula for M(1)
J             jump_ratio                                                AP(n+1)/AP(n), fee included
AP(t)         premium_pp(t)                                             Guaranteed annual premium
G(t)          premiums(t)                                               Premium income
K(t)          commissions(t)                                            Commission
k(t)          comm_rate(t)                                              Commission rate
X(t)          premium_taxes(t)                                          Premium tax
E(t)          expenses(t)                                               Acquisition + maintenance
DC(t)         claims(t)                                                 Death claims
CV(t)         conv_credits(t)                                           Conversion credit outflow
NetCF(t)      net_cf(t)                                                 Net cash flow
phase(t)      phase(t)                                                  LEVEL / PLT / EXPIRED
conv_elig(t)  conv_elig(t)                                              Conversion eligibility
============  ========================================================  ===============================

Three notes on the mapping. The notes write deaths as ``d(t)`` while also using ``d``
as the post-level-term duration index in ``M(d)``; the ``pols_death`` / ``plt_mort_factor``
split removes that collision. The notes' ``x(t)`` (lapses) and ``X(t)`` (premium tax)
differ only by case, which ``pols_lapse`` and ``premium_taxes`` separate. And
``pols_maturity`` has no symbol in the notes at all — see below.

.. rubric:: pols_maturity

The notes give the roll-forward as ``l(t+1) = l(t)(1-q)(1-cv)(1-w)`` and, separately,
the rule ``l(t) = 0 for x+t-1 >= 95``. Those do not reconcile in the final policy year:
its survivors neither die, lapse nor convert — their coverage simply runs out. Without
a term for that, the roll-forward appears to lose lives with no cause.
``pols_maturity(t)`` names it, zero in every year but the last, so that

    pols_if(t) - pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_conv(t) + pols_maturity(t)

holds for every ``t``. It is bookkeeping determined by the notes' own rules, not an
added assumption. The name follows ``BasicTerm_S.pols_maturity``.
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


def band():
    """Face-amount band 1-4 **[std]**; the anchor cell is band 1."""
    f = sum_assured()
    return 1 if f < 250000 else 2 if f < 500000 else 3 if f < 1000000 else 4


def policy_term():
    """The level premium period in years, from the plan code."""
    return int(plan()[1:])


def proj_len():
    """Projection length in policy years: coverage ends at attained age 95."""
    return expiry_age - age_at_entry()                              # noqa: F821


def age(t):
    """The attained age at the start of policy year t."""
    return age_at_entry() + t - 1


def premium_pp(t):
    """Guaranteed annual gross premium per policy in year t, policy fee included."""
    key = (plan(), sex(), rate_class(), band(), t)
    return float(data.premium_rates().loc[key, "premium_pp"])               # noqa: F821


def jump_ratio():
    """Initial premium jump ratio premium_pp(n+1)/premium_pp(n), fee included."""
    return premium_pp(policy_term() + 1) / premium_pp(policy_term())


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
    """Post-level-term mortality deterioration at PLT duration d; grades to 2.00 **[std]**."""
    return max(2.0, plt_mort_factor_init() - 0.15 * (d - 1)) if d >= 1 else 1.0


def class_factor():
    """Underwriting-class multiplier on the base mortality table **[std]**."""
    return float(data.class_factor_table().loc[rate_class(), "factor"])      # noqa: F821


def mort_rate_base(t):
    """Base-table mortality rate at the attained age in policy year t."""
    return float(data.mort_table().loc[age(t), "mort_rate"])                 # noqa: F821


def mort_rate(t):
    """Mortality rate applied in year t: base x class factor x PLT deterioration."""
    d = t - policy_term()
    return mort_rate_base(t) * class_factor() * (plt_mort_factor(d) if d >= 1 else 1.0)


def shock_lapse_rate():
    """Shock lapse at the end of the level period, by jump-ratio bucket **[std]**."""
    j = jump_ratio()
    for _, r in data.shock_lapse_table().iterrows():                        # noqa: F821
        if r["jump_lo"] < j <= r["jump_hi"]:
            return float(r["shock_lapse_rate"])
    return float(data.shock_lapse_table().iloc[-1]["shock_lapse_rate"])     # noqa: F821


def lapse_rate(t):
    """Lapse rate in policy year t **[std]**, including the shock at the level-period end.

    Level period: 6%, 5%, 4% for years 3..n-2, 6% anticipatory at n-1, shock at n.
    Post-level term: 30%, 15%, then 10%.
    """
    n = policy_term()
    if t < n:
        if t == 1:
            return 0.06
        if t == 2:
            return 0.05
        if t == n - 1:
            return 0.06
        return 0.04
    if t == n:
        return shock_lapse_rate()
    d = t - n
    return 0.30 if d == 1 else 0.15 if d == 2 else 0.10


def conv_elig(t):
    """True while convertible: within the level period and attained age below 70."""
    return t <= policy_term() and age(t) < 70


def conv_rate(t):
    """Conversion rate in policy year t **[std]**; zero outside the eligibility window."""
    if not conv_elig(t):
        return 0.0
    return conv_rate_final if not conv_elig(t + 1) else conv_rate_base  # noqa: F821


def phase(t):
    """LEVEL, PLT or EXPIRED in policy year t."""
    if t > proj_len():
        return "EXPIRED"
    return "LEVEL" if t <= policy_term() else "PLT"


def pols_if(t):
    """Number of policies in-force at the start of policy year t."""
    if t == 1:
        return pols_if_init()
    if t > proj_len():
        return 0.0
    return (pols_if(t - 1) * (1 - mort_rate(t - 1))
            * (1 - conv_rate(t - 1)) * (1 - lapse_rate(t - 1)))


def pols_death(t):
    """Number of deaths occurring in policy year t."""
    return pols_if(t) * mort_rate(t)


def pols_surv(t):
    """Number of policies surviving to the end of year t, before voluntary decrements."""
    return pols_if(t) * (1 - mort_rate(t))


def pols_conv(t):
    """Number of conversions at the end of policy year t."""
    return pols_surv(t) * conv_rate(t)


def pols_lapse(t):
    """Number of lapses at the end of policy year t, including the shock lapse."""
    return pols_surv(t) * (1 - conv_rate(t)) * lapse_rate(t)


def pols_maturity(t):
    """Number of policies whose coverage ends at attained age 95.

    Non-zero only in the final policy year. Not a decrement - the contract runs out -
    but needed for the in-force roll-forward to close; see the Space docstring.
    """
    if t != proj_len():
        return 0.0
    return (pols_if(t) * (1 - mort_rate(t))
            * (1 - conv_rate(t)) * (1 - lapse_rate(t)))


def comm_rate(t):
    """Commission rate **[std]**: 80% in year 1, 5% to the end of the level period, 2% after."""
    return 0.80 if t == 1 else (0.05 if t <= policy_term() else 0.02)


def inflation_factor(t):
    """The expense inflation factor in policy year t."""
    return (1 + inflation_rate) ** (t - 1)                           # noqa: F821


def premiums(t):
    """Premium income in policy year t, at the beginning of the year."""
    return premium_pp(t) * pols_if(t)


def commissions(t):
    """Commission in policy year t **[std]**."""
    return comm_rate(t) * premiums(t)


def premium_taxes(t):
    """Premium tax in policy year t **[std]**."""
    return premium_tax_rate * premiums(t)                            # noqa: F821


def expenses(t):
    """Acquisition (year 1) and inflating maintenance expenses in policy year t **[std]**."""
    acq = expense_acq if t == 1 else 0.0                             # noqa: F821
    return acq + expense_maint * inflation_factor(t) * pols_if(t)    # noqa: F821


def claims(t):
    """Death claims incurred in policy year t, paid at the end of the year."""
    return sum_assured() * pols_death(t)


def conv_credits(t):
    """Conversion credit outflow: one annual premium per conversion, after year 1."""
    return premium_pp(t) * pols_conv(t) if t > 1 else 0.0


def net_cf(t):
    """Net cash flow in policy year t."""
    return (premiums(t) - commissions(t) - premium_taxes(t)
            - expenses(t) - claims(t) - conv_credits(t))


def result_cf():
    """Result table of cashflows."""
    ts = list(range(1, proj_len() + 1))
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


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

expiry_age = 95

premium_tax_rate = 0.02

expense_acq = 300.0

expense_maint = 30.0

inflation_rate = 0.02

conv_rate_base = 0.0

conv_rate_final = 0.0

pd = ("Module", "pandas")