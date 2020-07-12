"""Source module for IFRS17 CSM amortization simulation

This module contains formulas to simulate amortization of
contract service margin (CSM) defined in IFRS17.

This module is a mix-in module to projection module in nestedlife project.
"""

def AccumCF(t):
    """Accumulated cashflows"""
    return -NetInsurAssets(t)

def ActualNetCF(t):
    """Acutal net cashflow"""
    return NetInsurCF(t) + IntAccumCF(t)

#%% The statement of Financial Posisition

def NetBalance(t):
    """Net insurance assets plus accumulated cashflows."""
    return NetInsurAssets(t) + AccumCF(t)

def NetInsurAssets(t):
    """Net Insurance Assets or Liabilities
    
    Warnings:
        The liabilities for incurred claims are not implemented. 
    """    
    return (PV_FutureCF(t)
            - RiskAdjustment(t)
            - CSM(t))
    

def PV_FutureCF(t):
    """Present value of future cashflows"""
    return PV_Cashflow(t, t, t)

    
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
        return PV_FutureCF(t) - RiskAdjustment(t)
    else:
        # Subsequent recognition (44)
        return (CSM_Unfloored(t-1)
                + IntAccrCSM(t-1)
                + AdjCSM_FlufCF(t-1)
                - TransServices(t-1))


def CSM(t):
    """floored CSM (38, 44)"""
    if t == 0:
        # Initial recognition (38)
        return max(0, PV_FutureCF(t) - RiskAdjustment(t))
    else:
        # Subsequent recognition (44)
        return max(0, (CSM(t - 1)
                + IntAccrCSM(t - 1)
                + AdjCSM_FlufCF(t - 1)
                - TransServices(t - 1)))


def LossComp(t):
    """Loss Component"""
    if t == 0:
        # Initial recognition
        return - min(0, PV_FutureCF(t) - RiskAdjustment(t))
    else:
        # Subsequent recognition
        return max(0, LossComp(t - 1) - AdjLCO_FulfCF(t - 1))


def Incr_LossComp(t):
    """Increase in Loss Component"""
    if t == 0:
        return LossComp(t)
    else:
        return max(0, LossComp(t) - LossComp(t - 1))


def AdjLCO_FulfCF(t):
    """Adjustment to Loss Component for changes in fulfilment cashflows"""
    if LossComp(t) > 0:
        return min(LossComp(t), EstClaim(t) + EstExps(t) + RelsRiskAdj(t))
    else:
        return 0

        
def IntAccrCSM(t):
    """Interest accreted on CSM (44(b))"""
    return CSM(t) * DiscRate(t, 0)


def AdjCSM_FlufCF(t):
    """Adjustment to CSM for changes in fulfilment cashflows (44(c)->B96-B100)

    Warnings:
        Only B96(b) changes in PV of the future cashflows are implemented.

    TODO: Risk Adjustment is yet to be implemented. At the momement
    this adjustment only considers present value of future cashflows.

    TODO: Loss component for onerous contracts are yet to be implemented.
    At the momemnt this adjustment allows negative CSM.
    """

    return PV_Cashflow(t + 1, t + 1, 0) - PV_Cashflow(t, t + 1, 0)
        
    
def PV_Cashflow(t, t_at, t_rate):
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
    return InnerProj(t).PresentValue(t_rate).PV_NetCashflow(t_at)


def TransServices(t):
    """Transfer of services (44(e)->B119)
    """
    csm_pre_rel = (CSM(t)
                   + IntAccrCSM(t)
                   + AdjCSM_FlufCF(t))

    diff_covunits = CovUnitsBeg1(t) * (1 + InnerProj(0).scen.DiscRate(t))
    pv_sumcovunits_end = PV_SumCovUnits(t + 1, 0)

    return csm_pre_rel * diff_covunits / (diff_covunits + pv_sumcovunits_end)

def CovUnitsBeg1(t):
    """The number of coverage units at `t` after new business"""
    return InsurIF_Beg1(t)


def CovUnitsEnd(t):
    """The number of coverage units at `t`"""
    return InsurIF_End(t)


def PV_SumCovUnits(t, t_rate):
    """Present value of cumulatvie coverage units

    The non-economic assumptions used for future estimation are the
    current estimate at time `t`.

    The discount rates used are the ones at time `t_rate`.
    """
    return InnerProj(t).PresentValue(t_rate).PV_SumInsurIF(t)


#%% The statement of Financial Performance
    
def ProfitBefTax(t):
    """IFRS Profit before tax"""
    return InsServiceResult(t) + InsurFinIncomeExps(t)

def InsServiceResult(t):
    """Insurance Service Result (80(a), 83-86)"""  
    return InsurRevenue(t) - InsurServiceExps(t)

def InsurFinIncomeExps(t):
    """Insurance Finance Income or Expenses (80(b), 87-92, B128-B136)
    
    Warning:
        Accounting Policy Choice 88(b) not implemented.
    """
    chg_discrate = (PV_Cashflow(t + 1, t + 1, t + 1)
                    - PV_Cashflow(t + 1, t + 1, t))
    
    return (EstIntOnCF(t) + chg_discrate 
            - IntAccrCSM(t) + IntAccumCF(t))
            

def InsurRevenue(t):
    """Insurance Revenue (82-85, B120-B125)"""
    return (EstClaim(t)
            + EstExps(t)
            + RelsRiskAdj(t)
            + TransServices(t)
            + AmortAcqCashflow(t)
            - AdjLCO_FulfCF(t))

def EstPremIncome(t):
    """Expected Premium Income"""
    return InnerProj(t).PremIncome(t)
    
def EstAcqCashflow(t):
    """Expected Acquisition Cashflow"""

    est = InnerProj(t)
    return (est.ExpsCommInit(t)
            + est.ExpsCommRen(t)
            + est.ExpsAcq(t))
    
def EstIntOnCF(t):
    """Expected Interest on future cashflows"""
    return InnerProj(t).PresentValue(t).InterestNetCF(t)
    
def EstClaim(t):
    """Expected Claims
    
    Warning:
        Using actuarl invest componets as proxy.
    """
    est = InnerProj(t)
    return est.BenefitTotal(t) - InvstComponent(t)


def EstExps(t):
    """Expected Expenses"""
    
    est = InnerProj(t)
    return (est.ExpsTotal(t)
            - est.ExpsCommInit(t)
            - est.ExpsCommRen(t)
            - est.ExpsAcq(t))
    

def AsmpChangeImpact(t):
    """Non-financial assumption changes"""
    return PV_Cashflow(t + 1, t + 1, 0) - PV_Cashflow(t, t + 1, 0)

    
def RelsRiskAdj(t):
    """Release of Risk Adjustment to Revenue
    
    Warning:
        To be implemented.
    """
    return 0

def InsurServiceExps(t):
    """Insurance Service Expense (103(b))"""
    return (IncurClaim(t)
            + IncurExps(t)
            + AmortAcqCashflow(t)
            + Incr_LossComp(t)
            - AdjLCO_FulfCF(t))

def IncurClaim(t):
    """Incurred Claims"""
    return BenefitTotal(t) - InvstComponent(t)

def InvstComponent(t):
    """Investment Components in Incur Claims
    
    Warning:
        To be implemented.
    """
    return 0

def IncurExps(t):
    """Incurred Expenses"""
    return (ExpsTotal(t) - ExpsCommTotal(t) - ExpsAcq(t))

#%% Acquisition Cashflow Amortization

def AcqPremRatio():
    """Ratio of PV Acquisiton Cashflows to PV Premiums.
    
    The ratio is determined by the expectation at issue.
    """
    pvs = InnerProj(0).PresentValue(0)
    
    return ((pvs.PV_ExpsCommTotal(0) + pvs.PV_ExpsAcq(0))
            / pvs.PV_PremIncome(0))

def AmortAcqCashflow(t):
    """Amortization of Acquisition Cash Flows
    
    Warning:
        Implemented as a constant percentage of actual premiums,
        thus not totalling the original amount if actual != expected.
    """
    return -AcqPremRatio * PremIncome(t)


