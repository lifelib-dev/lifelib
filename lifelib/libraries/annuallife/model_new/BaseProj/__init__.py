# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Base Space for the :mod:`~simplelife.model.Projection` Space.

This Space serves as a base Space for :mod:`~simplelife.model.Projection`
Space, and it contains Cells for cashflow projection.

.. rubric:: Inheritance Structure

.. figure:: /images/projects/simplelife/model/BaseProj/diagram1.png


``Pols``:
    Cells whose names start with ``Pols`` deal with number of policies.
    For example, ``PolsDeath(t)`` represents number of deaths between
    time ``t`` and ``t+1``.

``Size``:
    Cells whose names start with ``Size`` represents an amount per policy.
    For example, ``SizeBenefitDeath`` represents sum assured per policy.

``Exps``:
    Cells whose names start with ``Exps`` represents expense cashflows.
    For example, ``ExpsCommRen`` means the renewal commission cashflow.

``Benefit``:
    Cells whose names start with ``Benefit`` represents benefit cashflows.
    For example, ``BenefitDeath(t)`` death benefits incurred
    between ``t`` and ``t+1``.

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

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
    return pol.IssueAge()[PolicyID] + t


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
    return PolsIF_Beg1(t) * BaseMortRate(AttAge(t)) * MortFactor(t)


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
        return 0 # pol.PolicyCount
    else:
        return PolsIF_Beg1(t-1) - PolsDeath(t-1) - PolsSurr(t-1)


def PolsLiving(t):
    """Number of policies: Living benefits"""
    return 0


def PolsMaturity(t):
    """Number of policies: Maturity"""
    if t == pol.PolicyTerm()[PolicyID]:
        return PolsIF_End(t)
    else:
        return 0


def PolsNewBiz(t):
    """Number of policies: New business"""
    return pol.PolicyCount()[PolicyID] if t == 0 else 0


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
    return PolsIF_Beg1(t) * SurrRate(t)


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
    return SizeSumAssured(t) * AnnPremRate()


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
    return SizeSumAssured(t) * (CashValueRate(t)
                                + CashValueRate(t+1)) / 2


def SizeExpsAcq(t):
    """Acquisition expense per policy at time t"""
    if t == 0:
        return (SizeAnnPrem(t) * asmp.ExpsAcqAnnPrem()[PolicyID]
                + (SizeSumAssured(t) * asmp.ExpsAcqSA()[PolicyID] + asmp.ExpsAcqPol()[PolicyID])
                * InflFactor(t) / InflFactor(0))
    else:
        return 0


def SizeExpsCommInit(t):
    """Initial commission per policy at time t"""
    if t == 0:
        return SizePremium(t) * asmp.CommInitPrem()[PolicyID] * (1 + asmp.CnsmpTax())
    else:
        return 0


def SizeExpsCommRen(t):
    """Renewal commission per policy at time t"""
    if t == 0:
        return 0
    elif t < asmp.CommRenTerm()[PolicyID]:
        return SizePremium(t) * asmp.CommRenPrem()[PolicyID] * (1 + asmp.CnsmpTax())
    else:
        return 0


def SizeExpsMaint(t):
    """Maintenance expense per policy at time t"""
    return (SizeAnnPrem(t) * asmp.ExpsMaintAnnPrem()[PolicyID]
            + (SizeSumAssured(t) * asmp.ExpsMaintSA()[PolicyID] + asmp.ExpsMaintPol()[PolicyID])
            * InflFactor(t))


def SizeExpsOther(t):
    """Other expenses per policy at time t"""
    return 0


def SizeInvstIncome(t):
    """Investment Income per policy from t to t+1"""
    return (SizeReserveTotalAftMat(t) + SizePremium(t)) * InvstRetRate(t)


def SizePremium(t):
    """Premium income per policy from t to t+1"""
    return SizeSumAssured(t) * GrossPremRate() * pol.PremFreq()[PolicyID]


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
    return  pol.SumAssured()[PolicyID]


def last_t():
    return min(LastAge() - pol.IssueAge()[PolicyID], 
               pol.PolicyTerm()[PolicyID])


def BaseMortRate(x):
    """Bae mortality rate"""

    return asmp.MortalityTables()[x, asmp.MortArrayIndex()[PolicyID]]


def GrossPremRate():
    """Gross Premium Rate per Sum Assured per payment"""

    alpha = pol.LoadAcqSA()[PolicyID]
    beta = pol.LoadMaintPrem()[PolicyID]
    gamma = pol.LoadMaintSA()[PolicyID]
    gamma2 = pol.LoadMaintSA2()[PolicyID]
    delta = pol.LoadMaintPremWaiverPrem()[PolicyID]

    x, n, m = pol.IssueAge()[PolicyID], pol.PolicyTerm()[PolicyID], pol.PremTerm()[PolicyID]

    freq = pol.PremFreq()[PolicyID]

    comf = comm_table[
        pol.Sex()[PolicyID], 
        pol.IntRate(RateBasisID.PREM)[PolicyID], 
        pol.TableID(RateBasisID.PREM)[PolicyID]]

    if pol.Product()[PolicyID] == ProductID.TERM or pol.Product()[PolicyID] == ProductID.WL:
        return (comf.Axn(x, n) + alpha + gamma * comf.AnnDuenx(x, n, freq)
                + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / (1-beta-delta) / freq / comf.AnnDuenx(x, m, freq)

    elif pol.Product()[PolicyID] == ProductID.ENDW:
        return (comf.Exn(x, n) + comf.Axn(x, n) + alpha + gamma * comf.AnnDuenx(x, n, freq)
                + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / (1-beta-delta) / freq / comf.AnnDuenx(x, m, freq)
    else:
        raise ValueError('invalid product')


def MortFactor(y):
    """Mortality factor"""
    return asmp.AsmpTables()[min(y, asmp.AsmpTableLen() - 1), asmp.MortFactorIndex()[PolicyID]]


def SurrRate(y):
    """Surrender Rate"""
    return asmp.AsmpTables()[min(y, asmp.AsmpTableLen() - 1), asmp.LapseRateIndex()[PolicyID]]


def AnnPremRate():
    """Annualized Premium Rate per Sum Assured"""
    return GrossPremRate() * (1/10 if pol.PremFreq()[PolicyID] == 0 else pol.PremFreq()[PolicyID])


def CashValueRate(t):
    """Cash Value Rate per Sum Assured"""
    return max(ReserveNLP_Rate(RateBasisID.PREM, t) - SurrCharge(t), 0)


def NetPremRate(basis):
    """Net Premium Rate"""

    gamma2 = pol.LoadMaintSA2()[PolicyID]
    # comf = LifeTable[Sex(), IntRate(basis), TableID(basis)]


    comf = comm_table[
        pol.Sex()[PolicyID], 
        pol.IntRate(basis)[PolicyID], 
        pol.TableID(basis)[PolicyID]]


    # x, n, m = IssueAge(), PolicyTerm(), PremTerm()

    x, n, m = pol.IssueAge()[PolicyID], pol.PolicyTerm()[PolicyID], pol.PremTerm()[PolicyID]


    if pol.Product()[PolicyID] == ProductID.TERM or pol.Product()[PolicyID] == ProductID.WL:
        return (comf.Axn(x, n) + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / comf.AnnDuenx(x, n)

    elif pol.Product()[PolicyID] == ProductID.ENDW:
        return (comf.Axn(x, n) + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / comf.AnnDuenx(x, n)

    else:
        raise ValueError('invalid product')


def ReserveNLP_Rate(basis, t):
    """Net level premium reserve rate"""

    gamma2 = pol.LoadMaintSA2()[PolicyID]

    # lt = LifeTable[Sex(), IntRate(basis), TableID(basis)]
    comf = comm_table[
        pol.Sex()[PolicyID], 
        pol.IntRate(basis)[PolicyID], 
        pol.TableID(basis)[PolicyID]]


    x, n, m = pol.IssueAge()[PolicyID], pol.PolicyTerm()[PolicyID], pol.PremTerm()[PolicyID]

    if t <= m:
        return comf.Axn(x+t, n-t) + gamma2 * comf.AnnDuenx(x+t, n-m, 1, m-t) \
                - NetPremRate(basis) * comf.AnnDuenx(x+t, m-t)
    else:
        return comf.Axn(x+t, n-t) + gamma2 * comf.AnnDuenx(x+t, n-m, 1, m-t)


def SurrCharge(t):
    """Surrender Charge Rate per Sum Assured"""
    m = pol.PremTerm()[PolicyID]
    return pol.InitSurrCharge()[PolicyID] * max((min(m, 10) - t) / min(m, 10), 0)


def LastAge():
    """Age at which mortality becomes 1"""
    x = 0
    while True:
        if BaseMortRate(x) == 1:
            return x
        x += 1


def InflFactor(t):
    """Inflation factors to adjust expense cashflows"""
    if t == 0:
        return 1
    else:
        return InflFactor(t-1) / (1 + asmp.InflRate())


def DiscRate(t):
    return scen.DiscRate(t)


