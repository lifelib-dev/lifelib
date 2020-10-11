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

PolicyData = ("Pickle", 1381394076296)

MortalityTables = ("Pickle", 1381395254152)

AssumptionTables = ("Pickle", 1381401144008)

Scenarios = ("Pickle", 1381401142408)

DiscountRate = ("Pickle", 1381401356104)

PremWaiverCost = ("Pickle", 1381401355144)

Assumption = ("Pickle", 1381401835592)

ProductSpec = ("Pickle", 1381401836360)