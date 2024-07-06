"""The space representing assumptions

The Assumptions space represents a set of assumptions.
This space is parameterized with :attr:`asmp_id`.
For each value of :attr:`asmp_id`,
a dynamic subspace of this space is created,
representing the specific assumption set associated
with the value of :attr:`asmp_id`.

.. rubric:: Parameters

Attributes:

    asmp_id: a string ID representing an assumption set

.. rubric:: References

Attributes:

    base_data: Reference to the :mod:`~appliedlife.LifeIntegra.BaseData` space

"""

from modelx.serialize.jsonvalues import *

_formula = lambda asmp_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def lapse_tables():
    """Lapse ratre assumptions"""
    return pd.read_excel(
        asmp_file(),
        sheet_name="Lapse",
        index_col=0)


def asmp_file():
    """The file path to an assumption file"""

    dir_ = base_data.const_params().at["table_dir", "value"]

    return _model.path.parent / dir_ / ("assumptions_" + date_id + ".xlsx")


def mort_scalar_tables():
    """Mortality scalar tables"""
    df = pd.read_excel(
        asmp_file(),
        sheet_name="Mortality",
        index_col=0)
    return df


lapse_len = lambda: len(lapse_tables())

mort_scalar_len = lambda: len(mort_scalar())

def stacked_lapse_tables():
    """Stacked lapse tables"""
    return lapse_tables().stack().swaplevel(0, 1).sort_index()


def stacked_mort_scalar_tables():
    """Stacked mortality scalar tables"""
    return mort_scalar_tables().stack().swaplevel(0, 1).sort_index()


def dyn_lapse_params():
    """Dynamic lapse parameters"""
    return pd.read_excel(
        asmp_file(),
        sheet_name="DynLapse",
        index_col=0)


# ---------------------------------------------------------------------------
# References

base_data = ("Interface", ("..", "BaseData"), "auto")

date_id = "202312"