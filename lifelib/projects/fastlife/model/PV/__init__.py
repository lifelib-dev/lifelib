"""Present Value mix-in Space

This Space serves as a base Space for :mod:`~simplelife.model.Projection`
Space, and it contains Cells to take the present value of projected cashflows.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     BaseProj[style=dotted]
     BaseProj <- Projection [hstyle=generalization]
     PV[style=dotted]
     PV <- Projection [hstyle=generalization];
   }

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def InterestNetCF(t):
    """Interest accreted on pv of net cashflows"""
    if t > last_t:
        return 0
    else:
        return (PV_NetCashflow(t)
                - PremIncome(t)
                + ExpsTotal(t)) * DiscRate(t)


def PV_BenefitDeath(t):
    """Present value of death benefits"""
    if t > last_t:
        return 0
    else:
        return (-BenefitDeath(t) + PV_BenefitDeath(t+1)) / (1 + DiscRate(t))


def PV_BenefitMat(t):
    """Present value of matuirty benefits"""
    if t > last_t:
        return 0
    else:
        return (-BenefitMat(t) + PV_BenefitMat(t+1)) / (1 + DiscRate(t))


def PV_BenefitSurr(t):
    """Present value of surrender benefits"""
    if t > last_t:
        return 0
    else:
        return (-BenefitSurr(t) + PV_BenefitSurr(t+1)) / (1 + DiscRate(t))


def PV_BenefitTotal(t):
    """Present value of total benefits"""

    exist = (t <= last_t())

    if not exist.any():
        return 0
    else:
        result = -BenefitTotal(t) + PV_BenefitTotal(t+1) / (1 + DiscRate(t))
        result.name = "PV_BenefitTotal"
        return result


def PV_Check(t):
    return PV_NetCashflow(t) - PV_NetCashflowForCheck(t)


def PV_ExpsAcq(t):
    """Present value of acquisition expenses"""
    if t > last_t:
        return 0
    else:
        return - ExpsAcq(t) + PV_ExpsAcq(t+1) / (1 + DiscRate(t))


def PV_ExpsCommTotal(t):
    """Present value of commission expenses"""
    if t > last_t:
        return 0
    else:
        return - ExpsCommTotal(t) + PV_ExpsCommTotal(t+1) / (1 + DiscRate(t))


def PV_ExpsMaint(t):
    """Present value of maintenance expenses"""
    if t > last_t:
        return 0
    else:
        return - ExpsMaint(t) + PV_ExpsMaint(t+1) / (1 + DiscRate(t))


def PV_ExpsTotal(t):
    """Present value of total expenses"""

    exist = (t <= last_t())

    if not exist.any():
        return 0
    else:
        result = exist * (-ExpsTotal(t)) + PV_ExpsTotal(t+1) / (1 + DiscRate(t))
        result.name = "PV_ExpsTotal"
        return result


def PV_NetCashflow(t):
    """Present value of net cashflow"""
    return (PV_PremIncome(t)
            + PV_ExpsTotal(t)
            + PV_BenefitTotal(t))


def PV_NetCashflowForCheck(t):
    """Present value of net cashflow"""
    if t > last_t:
        return 0
    else:
        return (PremIncome(t)
                - ExpsTotal(t)
                - BenefitTotal(t) / (1 + DiscRate(t))
                + PV_NetCashflow(t+1) / (1 + DiscRate(t)))


def PV_PremIncome(t):
    """Present value of premium income"""
    if t > last_t:
        return 0
    else:
        return PremIncome(t) + PV_PremIncome(t+1) / (1 + DiscRate(t))


def PV_SumInsurIF(t):
    """Present value of insurance in-force"""
    if t > last_t:
        return 0
    else:
        return InsurIF_Beg1(t) + PV_SumInsurIF(t+1) / (1 + DiscRate(t))


last_t = lambda: None

