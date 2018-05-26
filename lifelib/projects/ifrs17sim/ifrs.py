"""Source module for IFRS17 CSM amortization simulation

This module contains formulas to simulate amortization of
contract service margin (CSM) defined in IFRS17.

This module is a mix-in module to projection module in nestedlife project.
"""


#%% The statement of Financial Posisition

def NetBalance(t):
    return NetInsAssets(t) + prj_AccumCashflow(t)

def NetInsAssets(t):
    """Net Insurance Assets or Liabilities
    
    Warnings:
        The liabilities for incurred claims are not implemented. 
    """    
    return (PV_FutureCashflow(t)
            - RiskAdjustment(t)
            - CSM_Unfloored(t))
    

def PV_FutureCashflow(t):
    """Present value of future cashflow"""
    return PV_CashFlows(t, t, t)

    
def RiskAdjustment(t):
    """Risk Adjustment
    
    Warnings:
        To be implemented
    """
    return 0

#%% CSM Calculations

def CSM_Unfloored(t):
    """Unfloored CSM (38, 44)"""
    if t == 0:
        # Initial recognition (38)
        return PV_FutureCashflow(t) - RiskAdjustment(t)
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


#%% The statement of Financial Performance
    
def InsServiceResult(t):
    """Insurance Service Result (80(a), 83-86)"""  
    return InsRevenue(t) - InsServiceExps(t)

def InsFinanceIncomeExps(t):
    """Insurance Finance Income or Expenses (80(b), 87-92, B128-B136)
    
    Warning:
        Accounting Policy Choice 88(b) not implemented.
    """
    chg_discrate = (PV_CashFlows(t + 1, t + 1, t + 1) 
                    - PV_CashFlows(t + 1, t + 1, t))
    
    return (ExpectedInterestCashflow(t) + chg_discrate 
            - IntAccrCSM(t) + prj_InterestAccumCashflow(t))
            

def InsRevenue(t):
    """Insurance Revenue (82-85, B120-B125)"""
    return (ExpectedClaims(t)
            + ExpectedExps(t)
            + RelsRiskAdj(t)
            + TransServices(t)
            + AmortAcqCashflow(t))


def ExpectedPremium(t):
    return InnerProjection(t).prj_incm_Premium(t)
    
def ExpectedAcqCashflow(t):
    """Expected Acquisition Cashflow"""

    est = InnerProjection(t)
    return (est.prj_exps_CommInit(t) 
            + est.prj_exps_CommRen(t)
            + est.prj_exps_Acq(t))
    
def ExpectedInterestCashflow(t):
    """Expected Interest on future cashflows"""
    return InnerProjection(t).PresentValues(t).InterestNetCashflows(t)
    
def ExpectedClaims(t):
    """Expected Claims
    
    Warning:
        Using actuarl invest componets as proxy.
    """
    est = InnerProjection(t)
    return est.prj_bnft_Total(t) - InvstComponents(t)


def ExpectedExps(t):
    """Expected Expense"""
    
    est = InnerProjection(t)
    return (est.prj_exps_Total(t)
            - est.prj_exps_CommInit(t) 
            - est.prj_exps_CommRen(t)
            - est.prj_exps_Acq(t))
    
def RelsRiskAdj(t):
    """Release of Risk Adjustment to Revenue
    
    Warning:
        To be implemented.
    """
    return 0

def InsServiceExps(t):
    """Insurance Service Expense (103(b))"""
    return (IncurredClaims(t)
            + IncurredExps(t)
            + AmortAcqCashflow(t))

def IncurredClaims(t):
    """Incurred Claims"""
    return prj_bnft_Total(t) - InvstComponents(t)

def InvstComponents(t):
    """Investment Components in Incurred Claims
    
    Warning:
        To be implemented.
    """
    return 0

def IncurredExps(t):
    """Incurred Expenses"""
    return (prj_exps_Total(t) - prj_exps_CommTotal(t) - prj_exps_Acq(t))

#%% Acquisition Cashflow Amortization

def AcqPremRatio():
    """Ratio of PV Acquisiton Cashflows to PV Premiums.
    
    The ratio is determined by the expectation at issue.
    """
    pvs = InnerProjection(0).PresentValues(0)
    
    return ((pvs.PV_ExpsCommTotal(0) + pvs.PV_ExpsAcq(0))
            / pvs.PV_IncomePremium(0))

def AmortAcqCashflow(t):
    """Amortization of Acquisition Cash Flows
    
    Warning:
        Implemented as a constant percentage of actual premiums,
        thus not totalling the original amount if actual != expected.
    """
    return AcqPremRatio * prj_incm_Premium(t)


