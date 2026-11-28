"""Portfolio results and key-rate sensitivities, summed policy by policy through the ItemSpaces."""


def scenario_ids():
    return tuple(range(1, ESG.scen_size() + 1))


def actual_cashflows(scen_id):
    result = {t: 0.0 for t in Actual.projection_months}
    for i in Actual.point_indices():
        projection = Actual[i, scen_id]
        for t in Actual.projection_months:
            result[t] += projection.net_cf(t)
    return result


def liability_pv(month, scen_id, key):
    total = 0.0
    for i in Valuation.point_indices():
        total += Valuation(month, i, scen_id, key).liability_pv()
    return total


def base_liability_pv(month, scen_id):
    return liability_pv(month, scen_id, -1)


def base_cashflows(month, scen_id):
    offsets = Valuation.projection_months(month)
    result = {k: 0.0 for k in offsets}
    for i in Valuation.point_indices():
        projection = Valuation(month, i, scen_id, -1)
        for k in offsets:
            result[k] += projection.cashflow_at_offset(k)
    return result


def shocked_liability_pv(month, scen_id, key):
    return liability_pv(month, scen_id, key)


def dv01(month, scen_id, key):
    return base_liability_pv(month, scen_id) - shocked_liability_pv(month, scen_id, key)


def cs01(month, scen_id, key):
    base_cashflow = base_cashflows(month, scen_id)
    market = Market(month + 1, scen_id, key)
    discounts = [market.price(month + k + 2) for k in base_cashflow]
    liability = float(-np.dot(tuple(base_cashflow.values()), discounts))
    return base_liability_pv(month, scen_id) - liability


def annual_risk_report(num_scenarios, annual_steps):
    """Return (dv01, cs01) DataFrames for ESG paths 1..N and years 0..annual_steps."""
    for name, value, minimum in (
        ('num_scenarios', num_scenarios, 1), ('annual_steps', annual_steps, 0)
    ):
        if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < minimum:
            raise ValueError(f'{name} must be an integer >= {minimum}')
    if num_scenarios > ESG.scen_size():
        raise ValueError('num_scenarios exceeds the number of generated ESG paths')
    if 12 * int(annual_steps) >= ESG.step_size():
        raise ValueError('last annual close is outside the generated ESG time grid')

    index = pd.MultiIndex.from_product(
        [range(1, num_scenarios + 1), range(annual_steps + 1)], names=['scenario', 'year']
    )
    tenors = pd.Index(data.shock_key_months(), name='tenor_months')
    dv01_rows, cs01_rows = [], []
    for scenario, year in index:
        # The cut is the last completed policy month. At issue none has closed.
        month = 12 * year - 1
        dv01_rows.append([dv01(month, scenario, key) for key in range(len(tenors))])
        cs01_rows.append([cs01(month, scenario, key) for key in range(len(tenors))])
    return (pd.DataFrame(dv01_rows, index=index, columns=tenors),
            pd.DataFrame(cs01_rows, index=index, columns=tenors))
