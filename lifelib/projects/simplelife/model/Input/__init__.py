"""Input from files

The ``Input`` Space includes References that hold input values read from
the Excel input file, *input.xlsx*.
It also includes a few Cells to loock up values from the Referneces.

The References in this Space refer to `ExcelRange`_ objects.
The `ExcelRange` objects hold values read from ranges in the input
Excel file, *input.xlsx*. `ExcelRange`_ objects are Python's mapping objects,
so they support most methods that :obj:`dict` has, and can be
converted to :obj:`dict`. The table below lists the References
and their associated named ranges in *input.xlsx*.

==================== ====================
 References            Named ranges
==================== ====================
PolicyData             PolicyData
MortalityTables        MortalityTables
AssumptionTables       AsmpByDuration
Scenarios              Scenarios
DiscountRate           LargePolDiscount
==================== ====================


.. rubric:: References in this Space

Attributes:
    PolicyData: `ExcelRange`_ object holding policy data. The data
        is read from *PolicyData* range in *input.xlsx*.


    ProductSpec: `ExcelRange`_ object holding the data of product specs.
        The data is read from *ProductSpecTable* range in *input.xlsx*.

    Assumption: `ExcelRange`_ object holding the data of the assumption table.
        The data is read from *AssumptionTable* range in *input.xlsx*.

    MortalityTables: `ExcelRange`_ object holding the data of mortality Tables.
        The data is read from *MortalityTables* range in *input.xlsx*.

    AssumptionTables: `ExcelRange`_ object holding the data of assumptions by duration.
        The data is read from *AsmpByDuration* range in *input.xlsx*.

    Scenarios: `ExcelRange`_ object holding the data of economic scenarios.
        The data is read from *Scenarios* range in *input.xlsx*.

    DiscountRate: `ExcelRange`_ object holding the data of premium discount.
        The data is read from *LargePolDiscount* range in *input.xlsx*.


.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

.. _mapping:
   https://docs.python.org/3/glossary.html#term-mapping

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = True

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def AsmpLookup(asmp, prod=None, polt=None, gen=None):
    """Look up assumptions"""
    return Assumption.get((asmp, prod, polt, gen), None)


def SpecLookup(spec, prod=None, polt=None, gen=None):
    """Look up product specs"""
    return ProductSpec.get((spec, prod, polt, gen), None)


# ---------------------------------------------------------------------------
# References

PolicyData = ("Pickle", 2325069946056)

MortalityTables = ("Pickle", 2325070426248)

AssumptionTables = ("Pickle", 2325077011464)

Scenarios = ("Pickle", 2325077012168)

DiscountRate = ("Pickle", 2325077179528)

PremWaiverCost = ("Pickle", 2325077179336)

Assumption = ("Pickle", 2325077658952)

ProductSpec = ("Pickle", 2325077658888)