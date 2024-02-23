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

PolicyData = ("IOSpec", 1401484906208, 1401484906208)

MortalityTables = ("IOSpec", 1401491066256, 1401491066256)

AssumptionTables = ("IOSpec", 1401491065920, 1401491065920)

Scenarios = ("IOSpec", 1401491066160, 1401491066160)

DiscountRate = ("IOSpec", 1401491066112, 1401491066112)

PremWaiverCost = ("IOSpec", 1401491065968, 1401491065968)

Assumption = ("IOSpec", 1401497101040, 1401497101040)

ProductSpec = ("IOSpec", 1401497101232, 1401497101232)

CorrData = ("IOSpec", 1401497102096, 1401497102096)

FactorData = ("IOSpec", 1401497105264, 1401497105264)