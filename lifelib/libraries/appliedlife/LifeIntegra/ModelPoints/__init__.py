"""Model points

The ModelPoints space represents a set of policy model points.
This space is parameterized with mp_file_id and space_name,
and serves as the base space to create its subspaces dynamically
that correspond to combinations of mp_file_id and space_name values.

.. rubric:: Parameters

Attributes:

    mp_file_id: a string key representing a set of model points
    space_name: a string key representing the name of a product space

.. rubric:: References in the space

Attributes:

    base_data: Reference to the :mod:`~appliedlife.LifeIntegra.BaseData` space

"""

from modelx.serialize.jsonvalues import *

_formula = lambda mp_file_id, space_name: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point_table():
    """Reads a raw model point table from a file and returns it.

    Returns a DataFrame representing a model point table read from a model point file.
    The model point table is for a product space identified by :attr:`space_name`.
    By default, a CSV file is expected for the model point file.
    The path to the model point file is obtained from the value of the "model_point_dir"
    parameter in :func:`~appliedlife.LifeIntegra.BaseData.const_params`.

    The file name is constructed using a prefix, :attr:`mp_file_id` and :attr:`space_name`,
    all concatenated by underscores, followed by ".csv".
    The prefix is obtained from the value of the "model_point_file_prefix" parameter
    in :func:`~appliedlife.LifeIntegra.BaseData.const_params`.
    """
    dir_name: str = base_data.const_params().at["model_point_dir", "value"]
    file_name: str = (base_data.const_params().at["model_point_file_prefix", "value"]
                      + "_" + mp_file_id + "_" + space_name + ".csv")

    return pd.read_csv(_model.path.parent / dir_name / file_name, index_col="point_id", parse_dates=["entry_date"])


def model_point_table_ext():
    """Extends the raw model point table with product parameters and returns it.

    Append product parameter columns to the raw model point table returned by
    :func:`model_point_table`.
    The product parameters are obtained by passing :attr:`space_name` to
    :func:`~appliedlife.LifeIntegra.BaseData.product_params`.
    For each model point row in the raw model point table, a corresponding row that has
    matching "product_id" and "plan_id" values is appended.
    """
    return pd.merge(model_point_table().reset_index(), 
                    base_data.product_params(space_name).reset_index(),
                    how="left",
                    on=["product_id", "plan_id"]).set_index('point_id')


# ---------------------------------------------------------------------------
# References

base_data = ("Interface", ("..", "BaseData"), "auto")

space_name = "GMXB"

date_id = "202312"