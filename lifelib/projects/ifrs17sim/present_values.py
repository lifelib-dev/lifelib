# -*- coding: utf-8 -*-
"""Present Values modules

"""

def PV_SumInsInForce(t):
    if t > last_t:
        return 0
    else:
        return prj_InsInForce_BoP1(t) + PV_SumInsInForce(t + 1) / (1 + DiscRate(t))

def PV_IncomePremium(t):
    """Present value of premium income"""
    if t > last_t:
        return 0
    else:
        return prj_incm_Premium(t) + PV_IncomePremium(t + 1) / (1 + DiscRate(t))


def PV_BenefitSurrender(t):
    """Present value of surrender benefits"""
    if t > last_t:
        return 0
    else:
        return (-prj_bnft_Surrender(t) + PV_BenefitSurrender(t + 1)) / (1 + DiscRate(t))


def PV_BenefitDeath(t):
    """Present value of death benefits"""
    if t > last_t:
        return 0
    else:
        return (-prj_bnft_Death(t) + PV_BenefitDeath(t + 1)) / (1 + DiscRate(t))


def PV_ExpsCommTotal(t):
    """Present value of total expenses"""
    if t > last_t:
        return 0
    else:
        return - prj_exps_CommTotal(t) + PV_ExpsCommTotal(t + 1) / (1 + DiscRate(t))   


def PV_ExpsAcq(t):
    """Present value of total expenses"""
    if t > last_t:
        return 0
    else:
        return - prj_exps_Acq(t) + PV_ExpsAcq(t + 1) / (1 + DiscRate(t))
    

def PV_ExpsMaint(t):
    """Present value of total expenses"""
    if t > last_t:
        return 0
    else:
        return - prj_exps_Maint(t) + PV_ExpsMaint(t + 1) / (1 + DiscRate(t))   

    
def PV_ExpsTotal(t):
    """Present value of total expenses"""
    if t > last_t:
        return 0
    else:
        return - prj_exps_Total(t) + PV_ExpsTotal(t + 1) / (1 + DiscRate(t))    
    

def PV_NetCashflows(t):
    """Present value of net liability cashflow"""
    if t > last_t:
        return 0
    else:
        return (prj_incm_Premium(t)
                - prj_exps_Total(t)
                - prj_bnft_Total(t) / (1 + DiscRate(t))
                + PV_NetCashflows(t + 1) / (1 + DiscRate(t)))
