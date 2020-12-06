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


def Factor(risk=None, shock=None, scope=None, extrakey=None):
    return FactorData[risk, shock, scope, extrakey]


# ---------------------------------------------------------------------------
# References

PolicyData = ("Pickle", 2325077945160)

MortalityTables = ("Pickle", 2325095460104)

AssumptionTables = ("Pickle", 2325101521608)

Scenarios = ("Pickle", 2325101521416)

DiscountRate = ("Pickle", 2325101684424)

PremWaiverCost = ("Pickle", 2325101684232)

Assumption = ("Pickle", 2325102163848)

ProductSpec = ("Pickle", 2325102164616)

CorrData = ("Pickle", 2325102165768)

FactorData = ("Pickle", 2325102235144)