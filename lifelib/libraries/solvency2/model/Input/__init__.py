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

PolicyData = ("IOSpec", 2715314537776, 2715314537776)

MortalityTables = ("IOSpec", 2715323893280, 2715323893280)

AssumptionTables = ("IOSpec", 2715324588032, 2715324588032)

Scenarios = ("IOSpec", 2715321106752, 2715321106752)

DiscountRate = ("IOSpec", 2715330669856, 2715330669856)

PremWaiverCost = ("IOSpec", 2715330671248, 2715330671248)

Assumption = ("IOSpec", 2715330671296, 2715330671296)

ProductSpec = ("IOSpec", 2715330671824, 2715330671824)

CorrData = ("IOSpec", 2715330672832, 2715330672832)

FactorData = ("IOSpec", 2715330673024, 2715330673024)