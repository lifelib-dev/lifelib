"""Common Input Data

The ``Input`` Space contains References holding input data used in
multiple Spaces and associated Cells to process the input data.

The ``Input`` Space in the ``fastlife`` model contains
a PandasData object containing mortality tables as a pandas DataFrame.
The PandasData object is assigned to the Refernce, ``MortalityTables``.
The DataFrame is read from *MortalityTables.xlsx* in the model folder.
The DataFrame's index indicates age, and the columns are MultiIndex
whose first level indicates table ID, and second level values indicate
sex (``M`` or ``F``).

.. rubric:: References in this Space

Attributes:
    MortalityTables: `PandasData`_ object holding the data of mortality tables.
        The data is read from *MortalityTables.xlsx*. Defined also
        in :mod:`fastlife.model.LifeTable`,
        :mod:`fastlife.model.Input` and :mod:`fastlife.model.Projection.Assumptions`


.. _PandasData:
   https://docs.modelx.io/en/latest/reference/dataclient.html#pandasdata

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

def TableLastAge():
    """The last ages of MortalityTables"""

    result = MortalityTables().idxmax()
    result.name = 'TableLastAge'
    return result


# ---------------------------------------------------------------------------
# References

MortalityTables = ("Pickle", 3020541952136)