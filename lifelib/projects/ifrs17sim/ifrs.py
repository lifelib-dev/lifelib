"""Source module for IFRS17 CSM amortization simulation

This module contains formulas to simulate amortization of
contract service margin (CSM) defined in IFRS17.

This module is a mix-in module to projection module in nestedlife project.
"""

def CSM_Unfloored(t):
    """Unfloored CSM (38, 44)"""
    if t == 0:
        # Initial recognition (38)
        return PV_CashFlows(t, 0, 0)
    else:
        # Subsequent recognition (44)
        return (CSM_Unfloored(t - 1)
                + IntAccrCSM(t - 1)
                + AdjCSM_FulCashFlows(t - 1)
                - TransServices(t - 1))


        
def IntAccrCSM(t):
    """Interest accreted on CSM (44(b))"""
    return CSM_Unfloored(t) * InnerProjection(0).scen.DiscRate(t)


def AdjCSM_FulCashFlows(t):
    """Adjustment to CSM for changes in fulfilment cashflows (44(c)->B96-B100)

    Warnings:
        Only B96(b) changes in PV of the future cashflows are implemented.

    TODO: Risk Adjustment is yet to be implemented. At the momement
    this adjustment only considers present value of future cashflows.

    TODO: Loss component for onerous contracts are yet to be implemented.
    At the momemnt this adjustment allows negative CSM.
    """

    return PV_CashFlows(t + 1, t + 1, 0) - PV_CashFlows(t, t + 1, 0)
        
    
def PV_CashFlows(t, t_at, t_rate):
    """Present value of future cashflows
    
    This formula takes 3 time parameters.
    The projection starts from `t`, and the projected cashflows are
    discounted back to `t_at`.
    The discount rates applied are the ones at `t_rate`.
    
    Args:
        t: Time from which the projection
        t_at: Time discount rates at which are used.
        t_rate: Time to which the cashflows are discounted.
    """
    return InnerProjection(t).PresentValues(t_rate).PV_NetCashflows(t_at)


def TransServices(t):
    """Transfer of services (44(e)->B119)
    """
    csm_pre_rel = (CSM_Unfloored(t)
                   + IntAccrCSM(t)
                   + AdjCSM_FulCashFlows(t))

    diff_covunits = CovUnits_BoP1(t) * (1 + InnerProjection(0).scen.DiscRate(t))
    pv_sumcovunits_end = PV_SumCovUnits(t + 1, 0)

    return csm_pre_rel * diff_covunits / (diff_covunits + pv_sumcovunits_end)

def CovUnits_BoP1(t):
    """The number of coverage units at `t` after new business"""
    return prj_InsInForce_BoP1(t)


def CovUnits_EoP(t):
    """The number of coverage units at `t`"""
    return prj_InsInForce_EoP(t)


def PV_SumCovUnits(t, t_rate):
    """Present value of cumulatvie coverage units

    The non-economic assumptions used for future estimation are the
    current estimate at time `t`.

    The discount rates used are the ones at time `t_rate`.
    """
    return InnerProjection(t).PresentValues(t_rate).PV_SumInsInForce(t)

