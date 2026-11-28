"""Formulas Actual and Valuation share: MYGA_US_SEC's rate and MVA cells with the market quotes
of the DV01 example in place of the deterministic rate scenario. Each reads its month on the
valuation-date clock t; the quotes are Actual's or Valuation's own (market(t) or market())."""


def competitor_tenor(t):
    """Months left in the guarantee period; twelve once annual redeclaration has begun."""
    term = 12 * guar_period()
    d = duration_mth(t)
    if is_annual_redeclare() and d >= term:
        return 12
    return term * gp_index(t) - d


def mva_term_months(t):
    """The MVA term in whole months: 12 x mva_term(t), computed in ints."""
    if not is_active(t):
        return 0
    d = duration_mth(t)
    if is_annual_redeclare() and d >= 12 * guar_period():
        return 0
    return 12 * policy_year(t) - (d + 1) + 12 * mva_term_years(t)


def credit_rate(t):
    if not is_active(t):
        return 0.0
    if duration_mth(t) < 12 * guar_period():
        return declared_rate_initial()
    m = redeclare_month(t) - duration_mth_init()
    if m < t_entry():
        return credit_rate_init()
    floor_rate = gmir()
    renewal = renewal_quote(m) - renewal_spread
    return max(floor_rate, renewal)


def mva_ref_yield_locked(t):
    if not is_active(t):
        return 0.0
    if gp_index(t) <= 1:
        return mva_ref_yield_at_issue()
    m = gp_start_month(t) - duration_mth_init()
    return mva_fixing_yield(m) if m >= t_entry() else mva_ref_yield_locked_init()
