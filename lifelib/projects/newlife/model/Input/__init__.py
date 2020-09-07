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

PolicyData = ("Pickle", 2140188366536)

MortalityTables = ("Pickle", 2140219827400)

AssumptionTables = ("Pickle", 2140223568648)

Scenarios = ("Pickle", 2140223567688)

DiscountRate = ("Pickle", 2140223727368)

PremWaiverCost = ("Pickle", 2140223726408)

Assumption = ("Pickle", 2140224210888)

ProductSpec = ("Pickle", 2140224211656)