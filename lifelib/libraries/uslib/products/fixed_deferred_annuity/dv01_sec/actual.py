"""One policy on one generated path, from the valuation date (t = 0, ESG month 0)."""


def point_indices():
    return tuple(range(len(data.point_id())))


def market(t):
    return Market(t, scen_id, -1)


def market_rate(t):
    return market(t).rate(competitor_tenor(t), t)


def renewal_quote(t):
    tenor = 12 if is_annual_redeclare() else 60
    return market(t).rate(tenor, t)


def mva_ref_yield(t):
    return market(t).rate(mva_term_months(t), t)


def mva_fixing_yield(t):
    return market(t).rate(60, t)


def net_cf(t):
    return contract_net_cf(t) if 0 <= t < proj_len() else 0.0


# The opening state entering month t, before any month-t event: MYGA_US_SEC's ten opening
# columns and its count in force, as its model point table holds them for a point valued at t.
def pols_if_open(t):
    return pols_if_at(t, BEF_NB)


def av_pp_open(t):
    return av_pp(t - 1) if t > t_entry() else av_pp_init()


def mgsv_pp_open(t):
    return mgsv_pp(t - 1) if t > t_entry() else mgsv_pp_init()


def prem_accum_gmir_pp_open(t):
    return prem_accum_gmir_pp(t - 1) if t > t_entry() else prem_accum_gmir_pp_init()


def interest_credited_pp_open(t):
    return interest_credited_pp(t - 1) if t > t_entry() else interest_credited_pp_init()


def interest_credited_pp_prev_anniv_open(t):
    a = 12 * duration(t) - duration_mth_init()     # the month the contract year under way opened
    if a > t_entry():
        return interest_credited_pp(a - 1)
    if a == t_entry():
        return interest_credited_pp_init()
    return interest_credited_pp_prev_anniv_init()


def free_wd_allow_open(t):
    return free_wd_allow(policy_year(t))


def free_wd_remain_open(t):
    return free_wd_avail(t)


def tax_basis_pp_open(t):
    return tax_basis_pp(t - 1) if t > t_entry() else tax_basis_pp_init()


def credit_rate_open(t):
    return credit_rate(t - 1) if t > t_entry() else credit_rate_init()


def mva_ref_yield_locked_open(t):
    return mva_ref_yield_locked(t - 1) if t > t_entry() else mva_ref_yield_locked_init()
