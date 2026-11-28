"""A dated, scenario-specific zero-coupon curve and its implied forwards."""


def base_price(maturity_month):
    if (isinstance(maturity_month, bool) or not isinstance(maturity_month, (int, np.integer))
            or maturity_month < as_of_month):
        raise ValueError('maturity_month must be a whole month on or after as_of_month')
    if shock >= 0:
        return unshocked().base_price(maturity_month)
    return ESG.P_t_T_path(as_of_month, maturity_month, scen_id)


def unshocked():
    """The same close and ESG path with the original curve."""
    return Market(as_of_month, scen_id, -1)


def affected(maturity_month):
    """Whether the price changes under this key-rate shock."""
    return (shock >= 0 and shock_bp != 0.0 and maturity_month > as_of_month
            and shock_weight(maturity_month - as_of_month) != 0.0)


def shock_weight(tenor_month):
    """Weight of the selected key-rate bump on the maturity after the cut."""
    if shock == -1:
        return 0.0
    key_months = data.shock_key_months()
    node = key_months[shock]
    if tenor_month <= node:
        if shock == 0:
            return 1.0
        left = key_months[shock - 1]
        return max(0.0, (tenor_month - left) / (node - left))
    if shock == len(key_months) - 1:
        return 1.0
    right = key_months[shock + 1]
    return max(0.0, (right - tenor_month) / (right - node))


def price(maturity_month):
    """Bond price from the cut to an absolute maturity, with the selected bump."""
    base = base_price(maturity_month)
    tenor = maturity_month - as_of_month
    if tenor == 0 or shock == -1:
        return base
    bump = shock_bp * shock_weight(tenor)
    if bump == 0.0:
        return base
    annual_factor = base ** (-12.0 / tenor)
    return (annual_factor + bump) ** (-tenor / 12.0)


def rate(tenor_month, forward_month):
    """Use the observed spot fixing before the cut and the selected curve thereafter."""
    if (isinstance(forward_month, bool) or not isinstance(forward_month, (int, np.integer))
            or forward_month < 0):
        raise ValueError('forward_month must be a nonnegative whole month')
    if (isinstance(tenor_month, bool) or not isinstance(tenor_month, (int, np.integer))
            or tenor_month < 0):
        raise ValueError('tenor_month must be a nonnegative whole month')
    if tenor_month == 0:
        return 0.0
    if forward_month < as_of_month:
        maturity = forward_month + tenor_month
        start = ESG.P_t_T_path(forward_month, forward_month, scen_id)
        end = ESG.P_t_T_path(forward_month, maturity, scen_id)
        return (start / end) ** (12.0 / tenor_month) - 1.0
    maturity = forward_month + tenor_month
    if shock >= 0 and not affected(forward_month) and not affected(maturity):
        return unshocked().rate(tenor_month, forward_month)
    return (price(forward_month) / price(maturity)) ** (12.0 / tenor_month) - 1.0
