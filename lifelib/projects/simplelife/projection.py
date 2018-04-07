"""Source module to create ``Projection`` space from.

.. rubric:: Project Templates

This module is included in the following project templates.

* :mod:`simplelife`
* :mod:`nestedlife`

.. rubric:: References

Attributes:
    pol: Alias to :py:mod:`Policy<simplelife.policy>` space
    asmp: Alias to :py:mod:`Assumption<simplelife.assumptions>` space
    scen: Alias to :py:mod:`Economic<simplelife.economic>` space

"""

def last_t():
    return min(asmp.LastAge - pol.IssueAge, pol.PolicyTerm)

def ppl_Age(t):
    """Attained age at time ``t``"""
    return pol.IssueAge + t

def ppl_SumAssured(t):
    """Sum assured per policy at time ``t``"""
    return  pol.SumAssured

def ppl_AnnualizedPrem(t):
    """Annualized premium per policy at time ``t``"""
    return ppl_SumAssured(t) * pol.AnnualizedPremRate

# --- Income ---
def ppl_incm_Premium(t):
    """Premium income per policy from t to t+1"""
    return ppl_SumAssured(t) * pol.GrossPremRate * pol.PremFreq

def ppl_incm_Investment(t):
    """Investment Income per policy from t to t+1"""
    return (ppl_rsv_Total_AfterMat(t) + ppl_incm_Premium(t)) * scen.InvRetRate(t)

def ppl_incm_Total(t):
    """Income Total per policy"""
    return prj_incm_Premium(t) + prj_incm_Investment(t)

# --- Comissions ---
def ppl_exps_CommInit(t):
    """Initial commission per policy at time t"""
    if t == 0:
        return ppl_incm_Premium(t) * asmp.CmsnInitPrem * (1 + asmp.CnsmpTax)
    else:
        return 0

def ppl_exps_CommRen(t):
    """Renewal commission per policy at time t"""
    if t == 0:
        return 0
    elif t < asmp.CmsnRenTerm:
        return ppl_incm_Premium(t) * asmp.CmsnRenPrem * (1 + asmp.CnsmpTax)
    else:
        return 0


# --- Expenses ---
def ppl_exps_Acq(t):
    """Acquisition expense per policy at time t"""
    if t == 0:
        return ppl_AnnualizedPrem(t) * asmp.ExpsAcqAP \
            + (ppl_SumAssured(t) * asmp.ExpsAcqSA + asmp.ExpsAcqPol) \
            * scen.InflFac(t) / scen.InflFac(0)
    else:
        return 0


def ppl_exps_Maint(t):
    """Maintenance expense per policy at time t"""
    return ppl_AnnualizedPrem(t) * asmp.ExpsMaintAP  \
      + (ppl_SumAssured(t) * asmp.ExpsMaintSA + asmp.ExpsMaintPol) \
      * scen.InflFac(t)


def ppl_exps_Other(t):
    """Other expenses per policy at time t"""
    return 0


# --- Benfeits ---
def ppl_bnft_Death(t):
    """Death benefit per policy"""
    return ppl_SumAssured(t)

def ppl_bnft_AccDeath(t):
    """Accidental death benefit per policy"""
    return 0

def ppl_bnft_Surrender(t):
    """Surrender benefit per policy"""
    return ppl_SumAssured(t) * (pol.CashValueRate(t) + pol.CashValueRate(t + 1)) / 2

def ppl_bnft_Annuity(t):
    """Annuity benefit per policy"""
    return 0

def ppl_bnft_Maturity(t):
    """Maturity benefit per policy"""
    return 0

def ppl_bnft_AccHosp(t):
    """Accidental hospitalization benefit per policy"""
    return 0

def ppl_bnft_SickHosp(t):
    """Sickness hospitalization benefit per policy"""
    return 0

def ppl_bnft_Surgery(t):
    """Surgery benefit per policy"""
    return 0

def ppl_bnft_Living(t):
    """Living benefit per policy"""
    return 0

def ppl_bnft_Other(t):
    """Other benefit per policy"""
    return 0


# --- Reserve ---
def ppl_rsv_PremReserve_AfterMat(t):
    """Premium reserve per policy: After maturity"""
    return ppl_SumAssured(t) * pol.NLPReserveRate('VAL', t)

def ppl_rsv_UnearnedPrem_AfterMat(t):
    """Unearned premium: After maturity"""
    return 0 # ppl_SumAssured(t) * polset.UnernPremRate(polset, tt, True)

def ppl_rsv_Total_AfterMat(t):
    """Total reserve per policy: After maturity"""
    return ppl_rsv_PremReserve_AfterMat(t) \
           + ppl_rsv_UnearnedPrem_AfterMat(t)

def ppl_rsv_PremReserve_EoP(t):
    """Premium reserve per policy: End of period"""
    return ppl_SumAssured(t) * pol.NLPReserveRate('VAL', t)

def ppl_rsv_UnearnedPrem_EoP(t):
    """Unearned reserve per policy: End of period"""
    return 0 # ppl_SumAssured(t) * pol.UnernPremRate(polset, tt)

def ppl_rsv_HospReserve_EoP(t):
    """Hospitalization reserve per policy: End of period"""
    return 0

# --------------------------------------------------------------------------
# Number of Policies

def nop_BoP(t):
    """Number of policies: Beginning of period"""
    return nop_AfterMat(t)

def nop_Renewal(t):
    """Number of policies: Renewal policies"""
    return 0

def nop_NewBiz(t):
    """Number of policies: New business"""
    return pol.PolicyCount if t == 0 else 0

def nop_BoP1(t):
    """Number of policies: Beginning of period 1"""
    return nop_BoP(t) + nop_Renewal(t) + nop_NewBiz(t)

def nop_Death(t):
    """Number of policies: Death"""
    return nop_BoP1(t) * asmp.BaseMortRate(ppl_Age(t)) * asmp.MortFactor(t)

def nop_AccDeath(t):
    """Number of policies: Accidental death"""
    return 0

def nop_Surrender(t):
    """Number of policies: Surrender"""
    
    if 'SurrRateMult' in globals():
        surr_rate_mult = SurrRateMult
    else:
        surr_rate_mult = 1
    
    return nop_BoP1(t) * asmp.SurrRate(t) * surr_rate_mult

def nop_Annuity(t):
    """Number of policies: Annuity"""
    return 0

def nop_AccHosp(t):
    """Number of policies: Accidental Hospitalization"""
    return 0

def nop_SickHosp(t):
    """Number of policies: Sickness Hospitalization"""
    return 0

def nop_Surgery(t):
    """Number of policies: Surgery"""
    return 0

def nop_Living(t):
    """Number of policies: Living benefits"""
    return 0

def nop_Other(t):
    """Number of policies: Other benefits"""
    return 0

def nop_EoP(t):
    """Number of policies: End of period"""
    if t == 0:
        return 0 # pol.PolicyCount
    else:
        return nop_BoP1(t - 1) - nop_Death(t - 1) - nop_Surrender(t - 1)

def nop_Maturity(t):
    """Number of policies: Maturity"""
    if t == pol.PolicyTerm:
        return nop_EoP(t)
    else:
        return 0

def nop_AfterMat(t):
    """Number of policies: Maturity"""
    return nop_EoP(t) - nop_Maturity(t)


#--- Per Policy * Policy Counts ---
def prj_incm_Premium(t):
    """Premium income"""
    return ppl_incm_Premium(t) * nop_BoP1(t)
    
def prj_incm_Investment(t):
    """Investment income"""
    return ppl_incm_Investment(t) * nop_BoP1(t)

def prj_incm_Total(t):
    """Income Total"""
    return prj_incm_Premium(t) + prj_incm_Investment(t)
    
def prj_exps_CommInit(t):
    """Initial commissions"""
    return ppl_exps_CommInit(t) * nop_BoP1(t)
    
def prj_exps_CommRen(t):
    """Renewal commissions"""
    return ppl_exps_CommRen(t) * nop_BoP1(t)

def prj_exps_CommTotal(t):
    """Commissions Total"""
    return prj_exps_CommInit(t) + prj_exps_CommRen(t)

def prj_exps_Acq(t):
    """Acquisition expenses"""
    return ppl_exps_Acq(t) * (nop_NewBiz(t) + nop_Renewal(t))
    
def prj_exps_Maint(t):
    """Maintenance expenses"""
    return ppl_exps_Maint(t) * nop_BoP1(t)

def prj_exps_Other(t):
    """Other expenses"""
    return 0
    
def prj_exps_Total(t):
    """Total expenses"""
    return prj_exps_CommInit(t) + prj_exps_CommRen(t) \
            + prj_exps_Acq(t) + prj_exps_Maint(t) + prj_exps_Other(t)
            
def prj_bnft_Death(t):
    """Death benefits"""
    return ppl_bnft_Death(t) * nop_Death(t)
    
def prj_bnft_AccDeath(t):
    """Accidental death benefits"""
    return ppl_bnft_AccDeath(t) * nop_AccDeath(t)

def prj_bnft_Surrender(t):
    """Surrender benefits"""
    return ppl_bnft_Surrender(t) * nop_Surrender(t)

def prj_bnft_Annuity(t):
    """Annuity benefits"""
    return ppl_bnft_Annuity(t) * nop_Annuity(t)

def prj_bnft_Maturity(t):
    """Matuirty benefits"""
    return ppl_bnft_Maturity(t) * nop_Maturity(t)
    
def prj_bnft_AccHosp(t):
    """Accidental hospitalization benefits"""
    return ppl_bnft_AccHosp(t) * nop_AccHosp(t)

def prj_bnft_SickHosp(t):
    """Sickness hospitalization benefits"""
    return ppl_bnft_SickHosp(t) * nop_SickHosp(t)

def prj_bnft_Surgery(t):
    """Surgery benefits"""
    return ppl_bnft_Surgery(t) * nop_Surgery(t)

def prj_bnft_Living(t):
    """Living benefits"""
    return ppl_bnft_Living(t) * nop_Living(t)

def prj_bnft_Other(t):
    """Other benefits"""
    return ppl_bnft_Other(t) * nop_Other(t)

def prj_bnft_Total(t):
    """Benefit Total"""

    return \
        prj_bnft_Maturity(t) \
        + prj_bnft_Death(t) \
        + prj_bnft_AccDeath(t) \
        + prj_bnft_Surrender(t) \
        + prj_bnft_Annuity(t) \
        + prj_bnft_AccHosp(t) \
        + prj_bnft_SickHosp(t) \
        + prj_bnft_Surgery(t) \
        + prj_bnft_Living(t) \
        + prj_bnft_Other(t)


def prj_NetLiabilityCashflow(t):
    """Net liability cashflow"""
    return \
        prj_incm_Premium(t) \
        - prj_bnft_Total(t) \
        - prj_exps_Total(t)

def pv_incm_Premium(t):
    """Present value of premium income"""
    if t > last_t:
        return 0
    else:
        return prj_incm_Premium(t) + pv_incm_Premium(t + 1) / (1 + scen.DiscRate(t))


def pv_bnft_Surrender(t):
    """Present value of surrender benefits"""
    if t > last_t:
        return 0
    else:
        return (-prj_bnft_Surrender(t) + pv_bnft_Surrender(t + 1)) / (1 + scen.DiscRate(t))


def pv_bnft_Death(t):
    """Present value of death benefits"""
    if t > last_t:
        return 0
    else:
        return (-prj_bnft_Death(t) + pv_bnft_Death(t + 1)) / (1 + scen.DiscRate(t))

def pv_exps_CommTotal(t):
    """Present value of total expenses"""
    if t > last_t:
        return 0
    else:
        return - prj_exps_CommTotal(t) + pv_exps_CommTotal(t + 1) / (1 + scen.DiscRate(t))   

def pv_exps_Acq(t):
    """Present value of total expenses"""
    if t > last_t:
        return 0
    else:
        return - prj_exps_Acq(t) + pv_exps_Acq(t + 1) / (1 + scen.DiscRate(t))
    

def pv_exps_Maint(t):
    """Present value of total expenses"""
    if t > last_t:
        return 0
    else:
        return - prj_exps_Maint(t) + pv_exps_Maint(t + 1) / (1 + scen.DiscRate(t))   

    
def pv_exps_Total(t):
    """Present value of total expenses"""
    if t > last_t:
        return 0
    else:
        return - prj_exps_Total(t) + pv_exps_Total(t + 1) / (1 + scen.DiscRate(t))    
    

def pv_NetLiabilityCashflow(t):
    """Present value of net liability cashflow"""
    if t > last_t:
        return 0
    else:
        return pv_NetLiabilityCashflow(t + 1) / (1 + scen.DiscRate(t)) \
            + prj_incm_Premium(t) \
            - prj_bnft_Total(t) / (1 + scen.DiscRate(t)) \
            - prj_exps_Total(t)


def prj_ChangeInReserve(t):
    """Change in reserve"""
    return prj_rsv_Total_EoP(t + 1) - prj_rsv_Total_EoP(t)

                        
def prj_ProfitBeforeTax(t):
    """Profit before Tax"""

    return \
          prj_incm_Premium(t) \
        + prj_incm_Investment(t) \
        - prj_bnft_Total(t) \
        - prj_exps_Total(t) \
        - prj_ChangeInReserve(t)


def prj_rsv_PremReserve_EoP(t):
    """Premium reserve: End of period"""
    return ppl_rsv_PremReserve_EoP(t) * nop_EoP(t)


def prj_rsv_UnearnedPrem_EoP(t):
    """Unearned Premium: End of period"""
    return 0


def prj_rsv_HospReserve_EoP(t):
    """Hospitalization reserve: End of period"""
    return 0

def prj_rsv_Total_EoP(t):
    """Total reserve: End of period"""
    return prj_rsv_PremReserve_EoP(t) \
           + prj_rsv_UnearnedPrem_EoP(t)\
           + prj_rsv_HospReserve_EoP(t)

def prj_InsInForce_EoP(t):
    """Insurance in-force: End of period"""
    return nop_EoP(t) * ppl_SumAssured(t)

def prj_InsInForce_BoP1(t):
    """Insurance in-force: Beginning of period 1"""
    return nop_BoP1(t) * ppl_SumAssured(t)