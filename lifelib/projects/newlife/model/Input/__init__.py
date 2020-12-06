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

PolicyData = ("Pickle", 2281926053768)

MortalityTables = ("Pickle", 2281929384328)

AssumptionTables = ("Pickle", 2281883138568)

Scenarios = ("Pickle", 2281883137608)

DiscountRate = ("Pickle", 2281883313672)

PremWaiverCost = ("Pickle", 2281883312712)

Assumption = ("Pickle", 2281900439240)

ProductSpec = ("Pickle", 2281900440008)