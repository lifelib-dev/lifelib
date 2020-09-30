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

PolicyData = ("Pickle", 1889857683520)

MortalityTables = ("Pickle", 1889853839344)

AssumptionTables = ("Pickle", 1889862980512)

Scenarios = ("Pickle", 1889864428704)

DiscountRate = ("Pickle", 1889857891920)

PremWaiverCost = ("Pickle", 1889857800752)

Assumption = ("Pickle", 1889855741424)

ProductSpec = ("Pickle", 1889853520480)