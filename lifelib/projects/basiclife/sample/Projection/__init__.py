from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    return model_point_data.loc[point_id]


def sum_assured(): return model_point()["sum_assured"]


def age_at_entry(): return model_point()["age_at_entry"]


def term_y(): return model_point()["term_y"]


def init_pols_if(): return 1


def sex(): return model_point()["sex"]


def proj_len(): return 12 * term_y() + 1


def disc_factors():
    return np.array(list((1 + disc_rate_mth()[t])**(-t) for t in range(proj_len())))


def net_cf(t):
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


def premium_pp(t):
    """monthly premium"""
    return round((1 + loading_prem()) * net_premium(), 2)


def claim_pp(t):
    # if t == 0:
    #     return sum_assured()
    # elif t > term_y() * 12:
    #     return 0
    # elif shape == "level":
    #     return sum_assured()
    # elif shape == "decreasing":
    #     r = (1+0.07)**(1/12)-1
    #     S = sum_assured()
    #     T = term_y() * 12
    #     outstanding = S * ((1+r)**T - (1+r)**t)/((1+r)**T - 1)
    #     return outstanding
    # else:
    #     raise ValueError("Parameter 'shape' must be 'level' or 'decreasing'")
    return sum_assured()


def inflation_factor(t):
    """annual"""
    return (1 + inflation_rate)**(t//12)


def premiums(t):
    return premium_pp(t) * pols_if(t)


def duration(t):
    """duration in force in years"""
    return t//12


def claims(t):
    return claim_pp(t) * pols_death(t)


def expenses(t):
    if t == 0:
        return expense_acq()
    else:
        return pols_if(t) * expense_maint()/12 * inflation_factor(t)


def age(t):
    return age_at_entry + t//12


def disc_rate_mth():
    return np.array(list((1 + disc_rate_ann[t//12])**(1/12) - 1 for t in range(proj_len())))


def lapse_rate(t):
    return max(0.1 - 0.02 * duration(t), 0.02)


def pv_pols_if():
    return sum(list(pols_if(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def net_premium():

    return pv_claims() / pv_pols_if()


def pv_net_cf():

    return pv_premiums() - pv_claims() - pv_expenses() - pv_commissions()


def check_pv_net_cf():

    import math
    res = sum(list(net_cf(t) for t in range(proj_len())) * disc_factors()[:proj_len()])

    return math.isclose(res, pv_net_cf())


def commissions(t): 
    return premiums(t) if duration(t) == 0 else 0


def inflation_rate(): return 0.02


def pols_death(t):
    """deaths occurring at time t"""
    return pols_if(t) * mort_rate_mth(t)


def pols_if(t):
    """number of policies in force"""
    if t==0:
        return init_pols_if()
    elif t > term_y() * 12:
        return 0
    else:
        return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)


def pols_lapse(t):
    """exits occurring at time t"""
    return pols_if(t) * (1-(1 - lapse_rate(t))**(1/12))


def pv_claims():
    return sum(list(claims(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def pv_commissions():
    return sum(list(commissions(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def pv_expenses():
    return sum(list(expenses(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def pv_premiums():
    return sum(list(premiums(t) for t in range(proj_len())) * disc_factors()[:proj_len()])


def expense_acq(): return 500


def expense_maint(): return 60


def loading_prem():
    return 0.30


def mort_rate(t):
    #if smoker_status == "N":
    #    return qx_non_smoker(t)
    #elif smoker_status == "S":
    #    return qx_smoker(t)
    return mort_table[str(min(5, duration(t)))][age(t)]


def mort_rate_mth(t):
    return 1-(1- mort_rate(t))**(1/12)


def result_pv():

    cols = ["Premiums", "Claims", "Expenses", "Commissions", "Net Cashflow"]
    pvs = [pv_premiums(), pv_claims(), pv_expenses(), pv_commissions(), pv_net_cf()]
    per_prem = [x / pv_premiums() for x in pvs]

    return pd.DataFrame.from_dict(
            data={"PV": pvs, "% Premium": per_prem},
            columns=cols,
            orient='index')


def result_cf():

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


# ---------------------------------------------------------------------------
# References

disc_rate_ann = ("DataClient", 1917973011848)

model_point_data = ("DataClient", 1917953347848)

mort_table = ("DataClient", 1917973010056)

pd = ("Module", "pandas")

point_id = 100