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

    base_data: Reference to the :mod:`~appliedlife.IntegratedLife.BaseData` space

Example:

    The sample code below demonstrates how to examine the contents of
    :mod:`~appliedlife.IntegratedLife.Assumptions`
    for a specific value of :attr:`asmp_id`.

    .. code-block:: python

        >>> import modelx as mx

        >>> m = mx.read_model("IntegratedLife")

        >>> m.Assumptions["202312"].asmp_file()
        WindowsPath('C:/Users/User1/appliedlife/input_tables/assumptions_202312.xlsx')

        >>> m.Assumptions["202312"].lapse_tables()

                  L001  L002  L003  L004
        duration
        0         0.03  0.03  0.01  0.05
        1         0.04  0.04  0.02  0.05
        2         0.05  0.05  0.03  0.05
        3         0.06  0.06  0.04  0.05
        4         0.07  0.07  0.05  0.05
        5         0.08  0.08  0.06  0.05
        6         0.09  0.09  0.07  0.05
        7         0.20  0.10  0.08  0.05
        8         0.15  0.11  0.09  0.05
        9         0.10  0.20  0.10  0.05
        10        0.10  0.15  0.10  0.05
        11        0.10  0.10  0.10  0.05
        12        0.10  0.10  0.10  0.05
        13        0.10  0.10  0.10  0.05
        14        0.10  0.10  0.10  0.05
"""

from modelx.serialize.jsonvalues import *

_formula = lambda asmp_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def asmp_file():
    """The file path to an assumption file

    Return a `pathlib`_ Path object representing the file path
    of the assumption file.

    The file location is specified by the constant parameter, "table_dir".
    The file name is constructed using a prefix and :attr:`asmp_id`
    concatenated by an underscore, followed by ".xlsx".

    .. _pathlib: https://docs.python.org/3/library/pathlib.html
    """

    dir_ = base_data.const_params().at["table_dir", "value"]
    prefix = base_data.const_params().at["asmp_file_prefix", "value"]

    return _model.path.parent / dir_ / (prefix + "_" + asmp_id + ".xlsx")


def dyn_lapse_params():
    """Dynamic lapse parameters"""
    return pd.read_excel(
        asmp_file(),
        sheet_name="DynLapse",
        index_col=0)


def lapse_len():
    """Duration length of the lapse table"""
    return len(lapse_tables())


def lapse_tables():
    """Lapse rate assumptions"""
    return pd.read_excel(
        asmp_file(),
        sheet_name="Lapse",
        index_col=0)


def mort_scalar_len():
    """Duration length of the mortality scalar table"""
    return len(mort_scalar_tables())


def mort_scalar_tables():
    """Mortality scalar tables"""
    df = pd.read_excel(
        asmp_file(),
        sheet_name="Mortality",
        index_col=0)
    return df


def stacked_lapse_tables():
    """Stacked lapse tables"""
    return lapse_tables().stack().swaplevel(0, 1).sort_index()


def stacked_mort_scalar_tables():
    """Stacked mortality scalar tables"""
    return mort_scalar_tables().stack().swaplevel(0, 1).sort_index()


# ---------------------------------------------------------------------------
# References

base_data = ("Interface", ("..", "BaseData"), "auto")

asmp_id = "202312"