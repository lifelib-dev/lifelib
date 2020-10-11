from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = True

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def AsmpLookup(asmp, prod=None, polt=None, gen=None):
    return  Assumption.get((asmp, prod, polt, gen), None)


def SpecLookup(spec, prod=None, polt=None, gen=None):
    return  ProductSpec.get((spec, prod, polt, gen), None)


def CorrLife(row=None, col=None): pass


def Factor(risk=None, shock=None, scope=None, extrakey=None):
    return FactorData[risk, shock, scope, extrakey]


# ---------------------------------------------------------------------------
# References

PolicyData = ("Pickle", 1381372082120)

MortalityTables = ("Pickle", 1381371911560)

AssumptionTables = ("Pickle", 1381379646536)

Scenarios = ("Pickle", 1381379645576)

DiscountRate = ("Pickle", 1381379820616)

PremWaiverCost = ("Pickle", 1381379821192)

Assumption = ("Pickle", 1381380296008)

ProductSpec = ("Pickle", 1381380301832)

CorrData = ("Pickle", 1381380303176)

FactorData = ("Pickle", 1381373131592)