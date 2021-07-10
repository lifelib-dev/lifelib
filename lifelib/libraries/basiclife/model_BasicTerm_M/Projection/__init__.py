from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    return model_point_table


def sum_assured(): return model_point()["sum_assured"]


def age_at_entry(): return model_point()["age_at_entry"]


def policy_term(): return model_point()["policy_term"]


def pols_if_init(): return pd.Series(1, index=model_point().index)


def sex(): return model_point()["sex"]


def proj_len(): return 12 * policy_term() + 1


def disc_factors():
    return np.array(list((1 + disc_rate_mth()[t])**(-t) for t in range(max_proj_len())))


def net_cf(t):
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


def premium_pp(t):
    """Monthly premium per policy

    Monthly premium amount per policy defined as::

        round((1 + loading_prem()) * net_premium(), 2)

    .. seealso::

        :func:`loading_prem`
        :func:`net_premium_pp`

    """
    return np.around((1 + loading_prem()) * net_premium_pp(), 2)


def claim_pp(t):
    return sum_assured()


def inflation_factor(t):
    """annual"""
    return (1 + inflation_rate())**(t//12)


def premiums(t):
    return premium_pp(t) * pols_if(t)


def duration(t):
    """duration in force in years"""
    return t//12


def claims(t):
    return claim_pp(t) * pols_death(t)


def expenses(t):
    if t == 0:
        return expense_acq() * pols_if(t)
    else:
        return pols_if(t) * expense_maint()/12 * inflation_factor(t)


def pols_if(t):
    """number of policies in force"""
    # if t==0:
    #     return pols_if_init()
    # elif t > policy_term() * 12:
    #     return 0
    # else:
    #     return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)

    if t==0:
        return pols_if_init()
    elif t < max_proj_len():

        return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1) - pols_maturity(t)
        # raise KeyError("t out of range")
    else:
        # return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)
        raise KeyError("t out of range")


def pols_lapse(t):
    """exits occurring at time t"""
    return pols_if(t) * (1-(1 - lapse_rate(t))**(1/12))


def pols_death(t):
    """deaths occurring at time t"""
    return pols_if(t) * mort_rate_mth(t)


def age(t):
    return age_at_entry + t//12


def mort_rate(t):
    # if smoker_status == "N":
    #     return qx_non_smoker(t)
    # elif smoker_status == "S":
    #     return qx_smoker(t)
    # result = np.where(smoker_status() == "N", qx_non_smoker(t), qx_smoker(t))
    result = mort_table[str(min(5, duration(t)))][age(t)]
    # return pd.Series(result, index=smoker_status().index)
    result.index = model_point().index
    return result


def commissions(t): 
    return (duration(t) == 0) * premiums(t)


def pv_claims():
    # return sum(list(claims(t) for t in range(proj_len())) * disc_factors()[:proj_len()])

    cl = np.array(list(claims(t) for t in range(max_proj_len()))).transpose()

    return cl @ disc_factors()[:max_proj_len()]


def pv_expenses():
    # return sum(list(expenses(t) for t in range(proj_len())) * disc_factors()[:proj_len()])

    result = np.array(list(expenses(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_commissions():
    # return sum(list(commissions(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


    result = np.array(list(commissions(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_premiums():
    # return sum(list(premiums(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


    result = np.array(list(premiums(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def annual_risk_premium():
    return (pv_claims() + pv_expenses() + pv_commissions()) / pv_premiums()


def monthly_risk_premium():
    return np.around(annual_risk_premium() / 12, 2)


max_proj_len = lambda: max(proj_len())

def mort_rate_mth(t):
    return 1-(1- mort_rate(t))**(1/12)


def disc_rate_mth():
    return np.array(list((1 + disc_rate_ann[t//12])**(1/12) - 1 for t in range(max_proj_len())))


def inflation_rate(): return 0.01


def loading_prem():
    return 0.5


def net_premium_pp():
    """Net premium per policy"""
    return pv_claims() / pv_pols_if()


def pv_pols_if():

    result = np.array(list(pols_if(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pols_maturity(t):
    """number of policies in force"""
    return (policy_term() * 12 == t) *  (pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1))


def expense_acq(): return 300


def expense_maint(): return 60


def pv_net_cf():
    """Present value of net cashflows"""

    return pv_premiums() - pv_claims() - pv_expenses() - pv_commissions()


def lapse_rate(t): 
    return np.maximum(0.1 - 0.02 * duration(t), 0.02)


def result_cf():

    t_len = range(max_proj_len())

    data = {
        "Premiums": [sum(premiums(t)) for t in t_len],
        "Claims": [sum(claims(t)) for t in t_len],
        "Expenses": [sum(expenses(t)) for t in t_len],
        "Commissions": [sum(commissions(t)) for t in t_len],
        "Net Cashflow": [sum(net_cf(t)) for t in t_len]
    }

    return pd.DataFrame(data, index=t_len)


def result_pv ():

    data = {
        "PV Premiums": pv_premiums(),
        "PV Claims": pv_claims(),
        "PV Expenses": pv_expenses(),
        "PV Commissions": pv_commissions(),
        "PV Net Cashflow": pv_net_cf()
    }

    return pd.DataFrame(data, index=model_point().index)


# ---------------------------------------------------------------------------
# References

disc_rate_ann = ("DataClient", 2014729409480)

model_point_table = ("DataClient", 2014729351432)

mort_table = ("DataClient", 2014717001352)

np = ("Module", "numpy")

pd = ("Module", "pandas")