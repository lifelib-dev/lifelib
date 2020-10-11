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


# ---------------------------------------------------------------------------
# References

PolicyData = ("Pickle", 1777734646920)

MortalityTables = ("Pickle", 1777735372232)

AssumptionTables = ("Pickle", 1777741969416)

Scenarios = ("Pickle", 1777741968456)

DiscountRate = ("Pickle", 1777742128200)

PremWaiverCost = ("Pickle", 1777742127944)

Assumption = ("Pickle", 1777742607560)

ProductSpec = ("Pickle", 1777742608328)