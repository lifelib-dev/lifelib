"""Space for cashflow projection.

This Space is for projecting cashflows.
Most Cells in this Spaces return calculation results for all model points as
pandas Series objects indexed by Policy ID.

This Space has child Spaces,
:mod:`~fastlife.model.Projection.Policy` and :mod:`~fastlife.model.Projection.Assumptions`.
The :mod:`~fastlife.model.Projection.Policy` Space contains Cells representing policy attributes, such as
product type, issue age, sum assured, etc.
It also contains Cells for calculating policy values such as premium rates and
cash surrender value rates.

This Space has a base Space, :mod:`~fastlife.model.PV`, in which
Cells for taking present values of cashflows are defined.

.. rubric:: Composition Structure

.. figure:: /images/projects/fastlife/model/Projection/diagram1.png

.. rubric:: Inheritance Structure

.. figure:: /images/projects/fastlife/model/Projection/diagram2.png

.. rubric:: References

The following attributes defined in this Space.

Attributes:
    pol: Alias for :mod:`~fastlife.model.Projection.Policy` child Space
    asmp: Alias for :mod:`~fastlife.model.Projection.Assumptions` child Space
    scen: Alias for :mod:`~fastlife.model.Economic` Space
    ScenID: Scenario ID (``1`` by default)


"""

from modelx.serialize.jsonvalues import *

_formula = lambda PolicyID, ScenID=1: None

_bases = [
    ".PV"
]

_allow_none = None

_spaces = [
    "Policy",
    "Assumptions"
]

# ---------------------------------------------------------------------------
# Cells

def DiscRate(t):
    """Rates for discount cashflows

    Refers to :func:`Economic[ScenID].DiscRate<simplelife.model.Economic.DiscRate>`
    """
    return scen[ScenID].DiscRate(t)


def InflFactor(t):
    """Inflation factors to adjust expense cashflows

    Refers to :func:`Economic[ScenID].InflFactor<simplelife.model.Economic.InflFactor>`
    """
    return scen[ScenID].InflFactor(t)


def InvstRetRate(t):
    """Rate of investment return

    Refers to :func:`Economic[ScenID].InvstRetRate<simplelife.model.Economic.InvstRetRate>`
    """
    return scen[ScenID].InvstRetRate(t)


def BaseMortRate(t):
    """Base mortality rate"""

    exist = (t <= last_t())

    keys = pd.concat([asmp.MortTableID(), pol.Sex(), AttAge(t), exist],
                      axis=1, keys=["ID", "Sex", "Age", "exist"])

    def find_rate(key):
        if key["exist"]:
            return asmp.MortalityTables()[key["ID"], key["Sex"]][key["Age"]]
        else:
            return 0

    result = keys.apply(find_rate, axis=1)
    result.name = "BaseMortRate"

    return result


def last_t():

    result = np.minimum(asmp.LastAge() - pol.IssueAge(), pol.PolicyTerm())
    result.name = "last_t"

    return result


def AccumCF(t):
    """Accumulated cashflows"""
    if t == 0:
        return 0
    else:
        return (AccumCF(t-1)
                + IntAccumCF(t-1)
                + NetInsurCF(t-1))


def AttAge(t):
    """Attained age at time ``t``"""
    return pol.IssueAge() + t


def BenefitAccDth(t):
    """Accidental death benefits"""
    return SizeBenefitAccDth(t) * PolsAccDeath(t)


def BenefitAccHosp(t):
    """Accidental hospitalization benefits"""
    return SizeBenefitAccHosp(t) * PolsAccHosp(t)


def BenefitAnn(t):
    """Annuity benefits"""
    return SizeBenefitAnn(t) * PolsAnnuity(t)


def BenefitDeath(t):
    """Death benefits"""
    return SizeBenefitDeath(t) * PolsDeath(t)


def BenefitLiving(t):
    """Living benefits"""
    return SizeBenefitLiving(t) * PolsLiving(t)


def BenefitMat(t):
    """Matuirty benefits"""
    return SizeBenefitMat(t) * PolsMaturity(t)


def BenefitOther(t):
    """Other benefits"""
    return SizeBenefitOther(t) * PolsOther(t)


def BenefitSickHosp(t):
    """Sickness hospitalization benefits"""
    return SizeBenefitSickHosp(t) * PolsSickHosp(t)


def BenefitSurg(t):
    """Surgery benefits"""
    return SizeBenefitSurg(t) * PolsSurg(t)


def BenefitSurr(t):
    """Surrender benefits"""
    return SizeBenefitSurr(t) * PolsSurr(t)


def BenefitTotal(t):
    """Benefit Total"""
    return (BenefitMat(t)
            + BenefitDeath(t)
            + BenefitAccDth(t)
            + BenefitSurr(t)
            + BenefitAnn(t)
            + BenefitAccHosp(t)
            + BenefitSickHosp(t)
            + BenefitSurg(t)
            + BenefitLiving(t)
            + BenefitOther(t))


def ChangeRsrv(t):
    """Change in reserve"""
    return ReserveTotal_End(t+1) - ReserveTotal_End(t)


def ExpsAcq(t):
    """Acquisition expenses"""
    return SizeExpsAcq(t) * (PolsNewBiz(t) + PolsRenewal(t))


def ExpsAcqTotal(t):
    """Commissions and acquisition expenses"""
    return ExpsCommTotal(t) + ExpsAcq(t)


def ExpsCommInit(t):
    """Initial commissions"""
    return SizeExpsCommInit(t) * PolsIF_Beg1(t)


def ExpsCommRen(t):
    """Renewal commissions"""
    return SizeExpsCommRen(t) * PolsIF_Beg1(t)


def ExpsCommTotal(t):
    """Commissions Total"""
    return ExpsCommInit(t) + ExpsCommRen(t)


def ExpsMaint(t):
    """Maintenance expenses"""
    return SizeExpsMaint(t) * PolsIF_Beg1(t)


def ExpsMaintTotal(t):
    """Total maintenance expenses including other expenses"""
    return ExpsMaint(t) + ExpsOther(t)


def ExpsOther(t):
    """Other expenses"""
    return 0


def ExpsTotal(t):
    """Total expenses"""
    return (ExpsCommInit(t)
            + ExpsCommRen(t)
            + ExpsAcq(t)
            + ExpsMaint(t)
            + ExpsOther(t))


def IncomeTotal(t):
    """Income Total"""
    return PremIncome(t) + InvstIncome(t)


def InsurIF_Beg1(t):
    """Insurance in-force: Beginning of period 1"""
    return PolsIF_Beg1(t) * SizeSumAssured(t)


def InsurIF_End(t):
    """Insurance in-force: End of period"""
    return PolsIF_End(t) * SizeSumAssured(t)


def IntAccumCF(t):
    """Intrest on accumulated cashflows"""
    return (AccumCF(t)
            + PremIncome(t)
            - ExpsTotal(t)) * DiscRate(t)


def InvstIncome(t):
    """Investment income"""
    return SizeInvstIncome(t) * PolsIF_Beg1(t)


def NetInsurCF(t):
    """Net liability cashflow"""
    return (PremIncome(t)
            - BenefitTotal(t)
            - ExpsTotal(t))


def PolsAccDeath(t):
    """Number of policies: Accidental death"""
    return 0


def PolsAccHosp(t):
    """Number of policies: Accidental Hospitalization"""
    return 0


def PolsAnnuity(t):
    """Number of policies: Annuity"""
    return 0


def PolsDeath(t):
    """Number of policies: Death"""
    return PolsIF_Beg1(t) * BaseMortRate(t) * asmp.MortFactor(t)


def PolsIF_AftMat(t):
    """Number of policies: Maturity"""
    return PolsIF_End(t) - PolsMaturity(t)


def PolsIF_Beg(t):
    """Number of policies: Beginning of period"""
    return PolsIF_AftMat(t)


def PolsIF_Beg1(t):
    """Number of policies: Beginning of period 1"""
    return PolsIF_Beg(t) + PolsRenewal(t) + PolsNewBiz(t)


def PolsIF_End(t):
    """Number of policies: End of period"""
    if t == 0:
        return 0 # pol.PolicyCount()
    else:
        return PolsIF_Beg1(t-1) - PolsDeath(t-1) - PolsSurr(t-1)


def PolsLiving(t):
    """Number of policies: Living benefits"""
    return 0


def PolsMaturity(t):
    """Number of policies: Maturity"""
    return (pol.PolicyTerm() == t) * PolsIF_End(t)


def PolsNewBiz(t):
    """Number of policies: New business"""
    return pol.PolicyCount() if t == 0 else 0


def PolsOther(t):
    """Number of policies: Other benefits"""
    return 0


def PolsRenewal(t):
    """Number of policies: Renewal policies"""
    return 0


def PolsSickHosp(t):
    """Number of policies: Sickness Hospitalization"""
    return 0


def PolsSurg(t):
    """Number of policies: Surgery"""
    return 0


def PolsSurr(t):
    """Number of policies: Surrender"""
    return PolsIF_Beg1(t) * asmp.SurrRate(t)


def PremIncome(t):
    """Premium income"""
    return SizePremium(t) * PolsIF_Beg1(t)


def ProfitBefTax(t):
    """Profit before Tax"""

    return (PremIncome(t)
            + InvstIncome(t)
            - BenefitTotal(t)
            - ExpsTotal(t)
            - ChangeRsrv(t))


def ReserveHospRsrvEnd(t):
    """Hospitalization reserve: End of period"""
    return 0


def ReservePremRsrvEnd(t):
    """Premium reserve: End of period"""
    return SizeReservePremRsrvEnd(t) * PolsIF_End(t)


def ReserveTotal_End(t):
    """Total reserve: End of period"""
    return (ReservePremRsrvEnd(t)
            + ReserveUernPremEnd(t)
            + ReserveHospRsrvEnd(t))


def ReserveUernPremEnd(t):
    """Unearned Premium: End of period"""
    return 0


def SizeAnnPrem(t):
    """Annualized premium per policy at time ``t``"""
    return SizeSumAssured(t) * pol.AnnPremRate()


def SizeBenefitAccDth(t):
    """Accidental death benefit per policy"""
    return 0


def SizeBenefitAccHosp(t):
    """Accidental hospitalization benefit per policy"""
    return 0


def SizeBenefitAnn(t):
    """Annuity benefit per policy"""
    return 0


def SizeBenefitDeath(t):
    """Death benefit per policy"""
    return SizeSumAssured(t)


def SizeBenefitLiving(t):
    """Living benefit per policy"""
    return 0


def SizeBenefitMat(t):
    """Maturity benefit per policy"""
    return 0


def SizeBenefitOther(t):
    """Other benefit per policy"""
    return 0


def SizeBenefitSickHosp(t):
    """Sickness hospitalization benefit per policy"""
    return 0


def SizeBenefitSurg(t):
    """Surgery benefit per policy"""
    return 0


def SizeBenefitSurr(t):
    """Surrender benefit per policy"""
    return SizeSumAssured(t) * (pol.CashValueRate(t)
                                + pol.CashValueRate(t+1)) / 2


def SizeExpsAcq(t):
    """Acquisition expense per policy at time t"""
    if t == 0:
        return (SizeAnnPrem(t) * asmp.ExpsAcqAnnPrem()
                + (SizeSumAssured(t) * asmp.ExpsAcqSA() + asmp.ExpsAcqPol())
                * InflFactor(t) / InflFactor(0))
    else:
        return 0


def SizeExpsCommInit(t):
    """Initial commission per policy at time t"""
    if t == 0:
        return SizePremium(t) * asmp.CommInitPrem() * (1 + asmp.CnsmpTax())
    else:
        return 0


def SizeExpsCommRen(t):
    """Renewal commission per policy at time t"""
    if t == 0:
        return 0
    elif (t < asmp.CommRenTerm()).any():
        return (t < asmp.CommRenTerm()) * SizePremium(t) * asmp.CommRenPrem() * (1 + asmp.CnsmpTax())
    else:
        return 0


def SizeExpsMaint(t):
    """Maintenance expense per policy at time t"""
    return (SizeAnnPrem(t) * asmp.ExpsMaintAnnPrem()
            + (SizeSumAssured(t) * asmp.ExpsMaintSA() + asmp.ExpsMaintPol())
            * InflFactor(t))


def SizeExpsOther(t):
    """Other expenses per policy at time t"""
    return 0


def SizeInvstIncome(t):
    """Investment Income per policy from t to t+1"""
    return (SizeReserveTotalAftMat(t) + SizePremium(t)) * InvstRetRate(t)


def SizePremium(t):
    """Premium income per policy from t to t+1"""
    return SizeSumAssured(t) * pol.GrossPremRate() * pol.PremFreq()


def SizeReservePremRsrvAftMat(t):
    """Premium reserve per policy: After maturity"""
    return SizeSumAssured(t) * pol.ReserveNLP_Rate('VAL', t)


def SizeReservePremRsrvEnd(t):
    """Premium reserve per policy: End of period"""
    return SizeSumAssured(t) * pol.ReserveNLP_Rate('VAL', t)


def SizeReserveTotalAftMat(t):
    """Total reserve per policy: After maturity"""
    return (SizeReservePremRsrvAftMat(t)
           + SizeReserveUernPremAftMat(t))


def SizeReserveUernPremAftMat(t):
    """Unearned premium: After maturity"""
    return 0 # SizeSumAssured(t) * polset.UnernPremRate(polset, tt, True)


def SizeReserveUernPremEnd(t):
    """Unearned reserve per policy: End of period"""
    return 0 # SizeSumAssured(t) * pol.UnernPremRate(polset, tt)


def SizeSumAssured(t):
    """Sum assured per policy at time ``t``"""
    return  pol.SumAssured()


def InterestNetCF(t):
    """Interest accreted on pv of net cashflows"""
    if t > last_t():
        return 0
    else:
        return (PV_NetCashflow(t)
                - PremIncome(t)
                + ExpsTotal(t)) * DiscRate(t)


def PV_BenefitDeath(t):
    """Present value of death benefits"""
    if t > last_t():
        return 0
    else:
        return (-BenefitDeath(t) + PV_BenefitDeath(t+1)) / (1 + DiscRate(t))


def PV_BenefitMat(t):
    """Present value of matuirty benefits"""
    if t > last_t():
        return 0
    else:
        return (-BenefitMat(t) + PV_BenefitMat(t+1)) / (1 + DiscRate(t))


def PV_BenefitSurr(t):
    """Present value of surrender benefits"""
    if t > last_t():
        return 0
    else:
        return (-BenefitSurr(t) + PV_BenefitSurr(t+1)) / (1 + DiscRate(t))


def PV_ExpsAcq(t):
    """Present value of acquisition expenses"""
    if t > last_t():
        return 0
    else:
        return - ExpsAcq(t) + PV_ExpsAcq(t+1) / (1 + DiscRate(t))


def PV_ExpsCommTotal(t):
    """Present value of commission expenses"""
    if t > last_t():
        return 0
    else:
        return - ExpsCommTotal(t) + PV_ExpsCommTotal(t+1) / (1 + DiscRate(t))


def PV_ExpsMaint(t):
    """Present value of maintenance expenses"""
    if t > last_t():
        return 0
    else:
        return - ExpsMaint(t) + PV_ExpsMaint(t+1) / (1 + DiscRate(t))


def PV_NetCashflowForCheck(t):
    """Present value of net cashflow"""
    if t > last_t():
        return 0
    else:
        return (PremIncome(t)
                - ExpsTotal(t)
                - BenefitTotal(t) / (1 + DiscRate(t))
                + PV_NetCashflow(t+1) / (1 + DiscRate(t)))


def PV_SumInsurIF(t):
    """Present value of insurance in-force"""
    if t > last_t():
        return 0
    else:
        return InsurIF_Beg1(t) + PV_SumInsurIF(t+1) / (1 + DiscRate(t))


# ---------------------------------------------------------------------------
# References

pol = ("Interface", (".", "Policy"), "auto")

asmp = ("Interface", (".", "Assumptions"), "auto")

scen = ("Interface", ("..", "Economic"), "auto")

ScenID = 1