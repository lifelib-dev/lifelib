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

PolicyData = ("Pickle", 1338028857992)

MortalityTables = ("Pickle", 1338041233224)

AssumptionTables = ("Pickle", 1338047252680)

Scenarios = ("Pickle", 1338047251720)

DiscountRate = ("Pickle", 1338047411400)

PremWaiverCost = ("Pickle", 1338047410440)

Assumption = ("Pickle", 1338047890824)

ProductSpec = ("Pickle", 1338047891592)