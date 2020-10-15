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

PolicyData = ("Pickle", 2449873593416)

MortalityTables = ("Pickle", 2449876034440)

AssumptionTables = ("Pickle", 2449883322440)

Scenarios = ("Pickle", 2449883321480)

DiscountRate = ("Pickle", 2449883493448)

PremWaiverCost = ("Pickle", 2449883492488)

Assumption = ("Pickle", 2449883976968)

ProductSpec = ("Pickle", 2449883977736)

CorrData = ("Pickle", 2449883979080)

FactorData = ("Pickle", 2449877034440)