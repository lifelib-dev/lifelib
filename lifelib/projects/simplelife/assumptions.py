"""Source module to create "Assumptions" space from.

Space Args:
    PolicyID

References:
    PolicyData: Input.PolicyData
    prdSpec: Input.prdSpec
    LifeTable: LifeTable
"""

policy_attrs = []

# #--- Mortality ---

def MortTable():
    """Mortality Table"""
    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    result = asmp.BaseMort.match(prd, polt, gen).value

    if result is not None:
        return MortalityTables(result).MortalityTable
    else:
        raise ValueError('MortTable not found')


def LastAge():
    """Age at which mortality becomes 1"""
    x = 0
    while True:
        if BaseMortRate(x) == 1:
            return x
        x += 1
            

def BaseMortRate(x):
    """Bae mortality rate"""
    return MortTable()(pol.Sex, x)


def MortFactor(y):
    """Mortality factor"""
    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    table = asmp.MortFactor.match(prd, polt, gen).value

    if table is None:
        raise ValueError('MortFactor not found')

    result = asmp_tbl.cells[table](y)

    if result is None:
        return MortFactor(y - 1)
    else:
        return result

# --- Surrender Rates ---
def SurrRate(y):
    """Surrender Rate"""
    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    table = asmp.Surrender.match(prd, polt, gen).value

    if table is None:
        raise ValueError('Surrender not found')

    result =  asmp_tbl.cells[table](y)

    if result is None:
        return SurrRate(y - 1)
    else:
        return result

# --- Commissions ---
def CmsnInitPrem():
    """Initial commission per premium"""

    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    result = asmp.CmsnInitPrem.match(prd, polt, gen).value

    if result is not None:
        return result
    else:
        raise ValueError('CmsnInitPrem not found')


def CmsnRenPrem():
    """Renewal commission per premium"""

    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    result = asmp.CmsnRenPrem.match(prd, polt, gen).value

    if result is not None:
        return  result
    else:
        raise ValueError('CmsnRenPrem not found')

def CmsnRenTerm():
    """Renewal commission term"""

    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    result = asmp.CmsnRenTerm.match(prd, polt, gen).value

    if result is not None:
        return result
    else:
        raise ValueError('CmsnRenTerm not found')

# # --- Expenses ---
def ExpsAcqSA():
    """Acquisition expense per sum assured"""
    return asmp.ExpsAcqSA.match(prd, polt, gen).value

def ExpsAcqAP():
    """Acquisition expense per annualized premium"""
    return asmp.ExpsAcqAP.match(prd, polt, gen).value

def ExpsAcqPol():
    """Acquisition expense per policy"""
    return asmp.ExpsAcqPol.match(prd, polt, gen).value

def ExpsMaintSA():
    """Maintenance expense per sum assured"""
    return asmp.ExpsAcqSA.match(prd, polt, gen).value

def ExpsMaintAP():
    """Maintenance expense per annualized premium"""
    return asmp.ExpsMaintGP.match(prd, polt, gen).value

def ExpsMaintPol():
    """Maintenance expense per policy"""
    return asmp.ExpsMaintPol.match(prd, polt, gen).value

def CnsmpTax():
    """Consumption tax rate"""
    return asmp.CnsmpTax()

def InflRate():
    """Inflation rate"""
    return asmp.InflRate()




    
    












