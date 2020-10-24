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

PolicyData = ("Pickle", 2523989600712)

MortalityTables = ("Pickle", 2523989396104)

AssumptionTables = ("Pickle", 2523998001736)

Scenarios = ("Pickle", 2523998000776)

DiscountRate = ("Pickle", 2523998176840)

PremWaiverCost = ("Pickle", 2523998175880)

Assumption = ("Pickle", 2523998660360)

ProductSpec = ("Pickle", 2523998661128)