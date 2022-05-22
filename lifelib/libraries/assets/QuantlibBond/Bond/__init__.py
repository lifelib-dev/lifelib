from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def cashflows(bond_id):

    result = [0] * t_length()
    leg = fixed_rate_bond(bond_id).cashflows()
    i = 0   # cashflow index

    for t in range(t_length()):

        while i < len(leg):

            if i > 0:
                # Check if cashflow dates are in order.
                assert leg[i-1].date() <= leg[i].date()

            if dates(t) <= leg[i].date() < dates(t+1):
                result[t] += leg[i].amount()

            elif dates(t+1) <= leg[i].date():
                break

            i += 1


    return result


def cashflows_total():

    result = [0] * t_length()
    for t in range(t_length()):
        for i in bond_data.index:
            result[t] += cashflows(i)[t]

    return result


def dates(t):

    if t == 0:
        return ql.Date(date_init, "%Y-%m-%d")

    else:
        return dates(t-1) + ql.Period('1Y')


def discount_curve(bond_id):

    spread = bond_data.loc[bond_id]['z_spread']
    spread  = ql.QuoteHandle(ql.SimpleQuote(spread))    

    return ql.ZeroSpreadedTermStructure(
        ql.YieldTermStructureHandle(riskfree_curve()), spread,
                                        ql.Compounded, ql.Annual)


def fixed_rate_bond(bond_id):


    settlement_days = bond_data.loc[bond_id]['settlement_days']
    face_value = bond_data.loc[bond_id]['face_value']
    coupons = [bond_data.loc[bond_id]['coupon_rate']]


    bond = ql.FixedRateBond(
        int(settlement_days), 
        float(face_value), 
        schedule(bond_id), 
        coupons, 
        ql.Actual360(), # DayCount
        ql.Unadjusted)

    # Set discount curve
    bondEngine = ql.DiscountingBondEngine(
        ql.YieldTermStructureHandle(discount_curve(bond_id)))
    bond.setPricingEngine(bondEngine)

    return bond


def redemptions(bond_id):


    result = [0] * t_length()
    leg = fixed_rate_bond(bond_id).redemptions()
    i = 0   # cashflow index

    for t in range(t_length()):

        while i < len(leg):

            if dates(t) <= leg[i].date() < dates(t+1):
                result[t] += leg[i].amount()

            elif dates(t+1) <= leg[i].date():
                break

            i += 1


    return result


def redemptions_total():

    result = [0] * t_length()
    for t in range(t_length()):
        for i in bond_data.index:
            result[t] += redemptions(i)[t]

    return result


def riskfree_curve():

    ql.Settings.instance().evaluationDate = dates(0)

    spot_dates = [dates(0)] + list(dates(0) + ql.Period(dur) for dur in zero_curve.index)
    spot_rates = [0] + list(zero_curve['Rate'])

    return ql.ZeroCurve(
        spot_dates, 
        spot_rates, 
        ql.Actual360(),     # dayCount
        ql.UnitedStates(),    # calendar
        ql.Linear(),          # Interpolator
        ql.Compounded,      # compounding
        ql.Annual           # frequency
        )


def schedule(bond_id):

    d = bond_data.loc[bond_id]['issue_date']
    issue_date = ql.Date(d.day, d.month, d.year)

    d = bond_data.loc[bond_id]['maturity_date']
    maturity_date = ql.Date(d.day, d.month, d.year)

    tenor  = ql.Period(
        ql.Semiannual if bond_data.loc[bond_id]['tenor'] == '6Y' else ql.Annual)


    return ql.Schedule(
        issue_date, 
        maturity_date, 
        tenor, 
        ql.UnitedStates(),               # calendar
        ql.Unadjusted,                   # convention
        ql.Unadjusted ,                 # terminationDateConvention
        ql.DateGeneration.Backward,     # rule
        False   # endOfMonth
        )


def t_length():

    d_end = ql.Date(date_end, "%Y-%m-%d")

    t = 0
    while True:
        if dates(t) < d_end:
            t += 1
        else:
            return t


def z_spread_recalc(bond_id):

    return ql.BondFunctions.zSpread(
        fixed_rate_bond(bond_id), 
        fixed_rate_bond(bond_id).cleanPrice(), 
        riskfree_curve(),
        ql.Thirty360(), ql.Compounded, ql.Annual)


def market_values():

    bond = fixed_rate_bond

    return list(
        bond(i).notional() * bond(i).cleanPrice() / 100 
        for i in bond_data.index)


# ---------------------------------------------------------------------------
# References

zero_curve = ("DataSpec", 2228674145152, 2228646456432)

date_end = "2053-01-01"

date_init = "2022-01-01"

bond_data = ("DataSpec", 2228674252864, 2228649358288)