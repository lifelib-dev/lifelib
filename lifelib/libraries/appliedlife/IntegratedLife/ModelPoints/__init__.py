"""Model points

The :mod:`~appliedlife.IntegratedLife.ModelPoints` space represents
a set of policy model points.
This space is parameterized with :attr:`mp_file_id` and :attr:`space_name`.
For each combination of :attr:`mp_file_id` and :attr:`space_name` values,
a dynamic subspace of this space is created,
representing a specific set of model points of :attr:`space_name`.

.. rubric:: Parameters

Attributes:

    mp_file_id: a string key representing a set of model points
    space_name: a string key representing the name of a product space

.. rubric:: References in the space

Attributes:

    base_data: Reference to the :mod:`~appliedlife.IntegratedLife.BaseData` space


Example:

    The sample code below demonstrates how to examine the contents of
    :mod:`~appliedlife.IntegratedLife.ModelPoints`.

    .. code-block:: python

        >>> import modelx as mx

        >>> m = mx.read_model("IntegratedLife")

        >>> m.ModelPoints["202401NB", "GMXB"].model_point_table()

                 product_id plan_id  ... av_pp_init  accum_prem_init_pp
        point_id                     ...
        1              GMDB  PLAN_A  ...          0                   0
        2              GMDB  PLAN_A  ...          0                   0
        3              GMDB  PLAN_B  ...          0                   0
        4              GMDB  PLAN_B  ...          0                   0
        5              GMAB  PLAN_A  ...          0                   0
        6              GMAB  PLAN_A  ...          0                   0
        7              GMAB  PLAN_B  ...          0                   0
        8              GMAB  PLAN_B  ...          0                   0

        [8 rows x 13 columns]

        >>> m.ModelPoints["202401NB", "GMXB"].model_point_table_ext()

                 product_id plan_id  ... dyn_lapse_param_id  dyn_lapse_floor
        point_id                     ...
        1              GMDB  PLAN_A  ...             DL001A             0.00
        2              GMDB  PLAN_A  ...             DL001A             0.00
        3              GMDB  PLAN_B  ...             DL001B             0.00
        4              GMDB  PLAN_B  ...             DL001B             0.00
        5              GMAB  PLAN_A  ...             DL002A             0.03
        6              GMAB  PLAN_A  ...             DL002A             0.03
        7              GMAB  PLAN_B  ...             DL002B             0.05
        8              GMAB  PLAN_B  ...             DL002B             0.05

        [8 rows x 29 columns]
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
    parameter in :func:`~appliedlife.IntegratedLife.BaseData.const_params`.

    The file name is constructed using a prefix, :attr:`mp_file_id` and :attr:`space_name`,
    all concatenated by underscores, followed by ".csv".
    The prefix is obtained from the value of the "model_point_file_prefix" parameter
    in :func:`~appliedlife.IntegratedLife.BaseData.const_params`.
    """
    dir_name: str = base_data.const_params().at["model_point_dir", "value"]
    file_name: str = (base_data.const_params().at["mp_file_prefix", "value"]
                      + "_" + mp_file_id + "_" + space_name + ".csv")

    return pd.read_csv(_model.path.parent / dir_name / file_name, index_col="point_id", parse_dates=["entry_date"])


def model_point_table_ext():
    """Extends the raw model point table with product parameters and returns it.

    Append product parameter columns to the raw model point table returned by
    :func:`model_point_table`.
    The product parameters are obtained by passing :attr:`space_name` to
    :func:`~appliedlife.IntegratedLife.BaseData.product_params`.
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