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

PolicyData = ("Pickle", 2184206177096)

MortalityTables = ("Pickle", 2184217069128)

AssumptionTables = ("Pickle", 2184218238536)

Scenarios = ("Pickle", 2184218243720)

DiscountRate = ("Pickle", 2184218414664)

PremWaiverCost = ("Pickle", 2184218413704)

Assumption = ("Pickle", 2184218898184)

ProductSpec = ("Pickle", 2184218897736)