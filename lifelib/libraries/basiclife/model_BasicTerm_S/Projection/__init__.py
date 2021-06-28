"""Space for cashflow projection.

This the only Space in the :mod:`~basiclife.BasicTerm_S` model.



.. rubric:: Parameters

Attributes:
    point_id: The ID of the selected model point.

.. rubric:: References


Attributes:
    model_point_table: as
    disc_rate_ann: Alias for :mod:`~simplelife.model.Economic` Space
    mort_table: xxx
    np: The `numpy`_ module.
    pd: The `pandas`_ module.

.. _numpy:
   https://numpy.org/

.. _pandas:
   https://pandas.pydata.org/

"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The Selected Model Point

    The row labeled :attr:`point_id` in :attr:`model_point_data` as a Series.
    """
    return model_point_table.loc[point_id]


def sum_assured():
    """The sum assured of the selected model point

    The element labeled "sum_assured" of the Series returned by 
    :func:`model_point`.
    """
    return model_point()["sum_assured"]


def age_at_entry():
    """The age at entry of the selected model point

    The element labeled "age_at_entry" of the Series returned by 
    :func:`model_point`.
    """
    return model_point()["age_at_entry"]


def sex(): 
    """The sex of the selected model point

    The element labeled "sex" of the Series returned by 
    :func:`model_point`.
    """
    return model_point()["sex"]


def proj_len():
    """Projection length in months

    Projection length in months defined as::

        12 * policy_term() + 1

    .. seealso::

        :func:`policy_term`
    """
    return 12 * policy_term() + 1


def disc_factors():
    """Discount factors

    Discount factors as a Numpy array.
    """
    return np.array(list((1 + disc_rate_mth()[t])**(-t) for t in range(proj_len())))


def net_cf(t):
    """Net cashflow

    Net cashflow for the period from ``t`` to ``t+1`` defined as::

        premiums(t) - claims(t) - expenses(t) - commissions(t)

    .. seealso::

        * :func:`premiums`
        * :func:`claims`
        * :func:`expenses`
        * :func:`commissions`

    """
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


def premium_pp(t):
    """Monthly premium per policy

    Monthly premium amount per policy defined as::

        round((1 + loading_prem()) * net_premium(), 2)

    .. seealso::

        :func:`loading_prem`
        :func:`net_premium_pp`

    """
    return round((1 + loading_prem()) * net_premium_pp(), 2)


def claim_pp(t):
    """Claim per policy

    The claim amount per plicy. Defaults to :func:`sum_assured`.
    """
    return sum_assured()


def inflation_factor(t):
    """The inflation factor at time ``t``
    """
    return (1 + inflation_rate)**(t//12)


def premiums(t):
    """Premium income

    Premium income during the period from ``t`` to ``t+1`` defined as::

        premium_pp(t) * pols_if(t)

    .. seealso::

        * :func:`premium_pp`
        * :func:`pols_if`

    """
    return premium_pp(t) * pols_if(t)


def duration(t):
    """duration in force in years"""
    return t//12


def claims(t):
    """Claims

    Claims during the period from ``t`` to ``t+1`` defined as::

        claim_pp(t) * pols_death(t)

    .. seealso::

        * :func:`claim_pp`
        * :func:`pols_death`

    """
    return claim_pp(t) * pols_death(t)


def expenses(t):
    """Expenses

    Expense during the period from ``t`` to ``t+1``.
    At ``t=0``, it is defined as :func:`expense_acq`.
    For ``t=1`` and onwards, defined as::

        pols_if(t) * expense_maint()/12 * inflation_factor(t)

    .. seealso::

        * :func:`pols_if`
        * :func:`expense_maint`
        * :func:`inflation_factor`

    """
    if t == 0:
        return expense_acq()
    else:
        return pols_if(t) * expense_maint()/12 * inflation_factor(t)


def age(t):
    """The attained age at time ``t``"""

    return age_at_entry + t//12


def disc_rate_mth():
    """Monthly discount rate

    Nummpy array of monthly discount rates from time 0 to :func:`proj_len` - 1
    defined as::

        (1 + disc_rate_ann)**(1/12) - 1

    .. seealso::

        :func:`disc_rate_ann`

    """
    return np.array(list((1 + disc_rate_ann[t//12])**(1/12) - 1 for t in range(proj_len())))


def lapse_rate(t):
    """Lapse rate"""
    return max(0.1 - 0.02 * duration(t), 0.02)


def pv_pols_if():
    """Present value of policies in-force

    The discouted sum of the number of in-force policies.
    It is used for calculating :func:`net_premium_pp`.

    """
    return sum(list(pols_if(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def pv_net_cf():
    """Present value of net cashflows"""

    return pv_premiums() - pv_claims() - pv_expenses() - pv_commissions()


def check_pv_net_cf():
    """Check present value summation"""

    import math
    res = sum(list(net_cf(t) for t in range(proj_len())) * disc_factors()[:proj_len()])

    return math.isclose(res, pv_net_cf())


def commissions(t): 
    """Commissions"""
    return premiums(t) if duration(t) == 0 else 0


def inflation_rate():
    """Inflation rate"""
    return 0.01


def pols_death(t):
    """deaths occurring at time t"""
    return pols_if(t) * mort_rate_mth(t)


def pols_if(t):
    """Number of Policies In-force

    Number of in-force policies calculated recursively.
    The initial value is read from :func:`pols_if_init`
    """
    if t==0:
        return pols_if_init()
    elif t > policy_term() * 12:
        return 0
    else:
        return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1) - pols_maturity(t)


def pols_lapse(t):
    """exits occurring at time t"""
    return pols_if(t) * (1-(1 - lapse_rate(t))**(1/12))


def pv_claims():
    """Present value of claims"""
    return sum(list(claims(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def pv_commissions():
    """Present value of commissions"""
    return sum(list(commissions(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def pv_expenses():
    """Present value of expenses"""
    return sum(list(expenses(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def pv_premiums():
    """Present value of premiums"""
    return sum(list(premiums(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def expense_acq():
    """Acquisition expense per policy"""
    return 300


def expense_maint():
    """Annual maintenance expence per policy"""
    return 60


def loading_prem():
    """Loading per premium"""
    return 0.50


def mort_rate(t):
    """Mortality rate"""
    return mort_table[str(min(5, duration(t)))][age(t)]


def mort_rate_mth(t):
    """Monthly mortality rate"""
    return 1-(1- mort_rate(t))**(1/12)


def result_pv():
    """Result table of present value of cashflows"""

    cols = ["Premiums", "Claims", "Expenses", "Commissions", "Net Cashflow"]
    pvs = [pv_premiums(), pv_claims(), pv_expenses(), pv_commissions(), pv_net_cf()]
    per_prem = [x / pv_premiums() for x in pvs]

    return pd.DataFrame.from_dict(
            data={"PV": pvs, "% Premium": per_prem},
            columns=cols,
            orient='index')


def result_cf():
    """Result table of cashflows"""

    t_len = range(proj_len())

    data = {
        "Premiums": [premiums(t) for t in t_len],
        "Claims": [claims(t) for t in t_len],
        "Expenses": [expenses(t) for t in t_len],
        "Commissions": [commissions(t) for t in t_len],
        "Net Cashflow": [net_cf(t) for t in t_len], 
        "Policies IF": [pols_if(t) for t in t_len],
        "Policies Death": [pols_death(t) for t in t_len],
        "Policies Exits": [pols_lapse(t) for t in t_len]
    }
    return pd.DataFrame.from_dict(data)


def pols_if_init(): 
    """Initial Number of Policies In-force

    Number of in-force policies at time 0 referenced from :func:`pols_if`.
    Defaults to 1.
    """
    return 1


def policy_term():
    """The policy term of the model point"""

    return model_point()["policy_term"]


def net_premium_pp():
    """Net premium per policy"""
    return pv_claims() / pv_pols_if()


def pols_maturity(t):
    """Number of maturing policies"""
    if t == policy_term() * 12:
        return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)
    else:
        return 0


# ---------------------------------------------------------------------------
# References

disc_rate_ann = ("DataClient", 2060963941704)

model_point_table = ("DataClient", 2060969349256)

mort_table = ("DataClient", 2060951895112)

pd = ("Module", "pandas")

point_id = 1