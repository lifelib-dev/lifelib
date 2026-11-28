"""MYGA_US_SEC restarted in force after the close of valuation_month, its opening state from Actual,
valued on one Market. t stays on Actual's clock; the first projected month is t_entry()."""


def market():
    return Market(valuation_month + 1, scen_id, shock)


def market_rate(t):
    return market().rate(competitor_tenor(t), t)


def renewal_quote(t):
    tenor = 12 if is_annual_redeclare() else 60
    return market().rate(tenor, t)


def mva_ref_yield(t):
    return market().rate(mva_term_months(t), t)


def mva_fixing_yield(t):
    return market().rate(60, t)


def t_entry():
    return max(valuation_month + 1, -duration_mth_init())


def pols_if_init():
    return act.pols_if_open(valuation_month + 1)


def av_pp_init():
    return act.av_pp_open(valuation_month + 1)


def mgsv_pp_init():
    return act.mgsv_pp_open(valuation_month + 1)


def prem_accum_gmir_pp_init():
    return act.prem_accum_gmir_pp_open(valuation_month + 1)


def interest_credited_pp_init():
    return act.interest_credited_pp_open(valuation_month + 1)


def interest_credited_pp_prev_anniv_init():
    return act.interest_credited_pp_prev_anniv_open(valuation_month + 1)


def free_wd_allow_init():
    return act.free_wd_allow_open(valuation_month + 1)


def free_wd_remain_init():
    return act.free_wd_remain_open(valuation_month + 1)


def tax_basis_pp_init():
    return act.tax_basis_pp_open(valuation_month + 1)


def credit_rate_init():
    return act.credit_rate_open(valuation_month + 1)


def mva_ref_yield_locked_init():
    return act.mva_ref_yield_locked_open(valuation_month + 1)


def cashflow_at_offset(k):
    """Future cash flow, counting from the first month after the close."""
    return net_cf(valuation_month + 1 + k) if 0 <= k < remaining_months() else 0.0


def remaining_months():
    return max(0, proj_len() - valuation_month - 1)


def projection_months(month):
    return range(max(0, data.book_projection_end() - month - 1))


def discount_factor(k):
    return market().price(valuation_month + k + 2)


def pv():
    """Present value of all remaining discounted cash flows."""
    total = 0.0
    for k in range(remaining_months()):
        total += cashflow_at_offset(k) * discount_factor(k)
    return total


def liability_pv():
    return -pv()
