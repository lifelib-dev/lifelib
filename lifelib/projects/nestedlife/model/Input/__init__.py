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

PolicyData = ("Pickle", 2366637431880)

MortalityTables = ("Pickle", 2366631136840)

AssumptionTables = ("Pickle", 2366657887496)

Scenarios = ("Pickle", 2366641454728)

DiscountRate = ("Pickle", 2366641481992)

PremWaiverCost = ("Pickle", 2366641481032)

Assumption = ("Pickle", 2366640245192)

ProductSpec = ("Pickle", 2366640245960)