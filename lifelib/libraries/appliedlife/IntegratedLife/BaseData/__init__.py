"""Basic parameters and data

This space reads parameters from a parameter file.
The parameters are then be referenced in other parts of the model.

There are a few types of parameters depending on the variability of their values.
Constant parameters have values that are constant anywhere in the model.
Run parameters can have different values for different runs.
Space parameters can have different values for different product spaces.
These three types of parameters are called fixed parameters,
because they have fixed values in each product space.

Product parameters are specific to individual product spaces.
Each product space has product parameters.
The values of product parameters vary by "product_id" and "plan_id"
defined for the product space.
Product parameters are appended to the model point table for the product space
in :func:`~appliedlife.IntegratedLife.ModelPoints.model_point_table_ext`.

Other spaces reference this space as ``base_data`` as a convention.

In addition to the parameters, this space also reads surrender charge tables
to be used in other spaces.

.. rubric:: References

Attributes:

    parameter_file: The name of the parameter file

Example:

    The sample code below demonstrates how to examine the contents of
    :mod:`~appliedlife.IntegratedLife.BaseData`.

    .. code-block:: python

        >>> import modelx as mx

        >>> m = mx.read_model("IntegratedLife")

        >>> m.BaseData.const_params()
                                             value
        parameter
        model_point_dir           model_point_data
        mp_file_prefix                 model_point
        asmp_file_prefix               assumptions
        table_dir                     input_tables
        scen_dir                     economic_data
        scen_param_file      index_parameters.xlsx
        scen_file_prefix                 risk_free
        mort_file            mortality_tables.xlsx
        spec_tables       product_spec_tables.xlsx

        >>> m.BaseData.run_params()
                base_date  ...                                description
        run_id             ...
        1      2023-12-31  ...                  New business  in Jan 2024
        2      2023-12-31  ...                   Base run end of Dec 2023
        3      2023-12-31  ...  Interest rate sensitivity end of Dec 2023
        4      2023-12-31  ...  Interest rate sensitivity end of Dec 2023
        5      2022-12-31  ...                   Base run end of Dec 2022

            [5 rows x 6 columns]

        >>> m.BaseData.space_params()
               expense_acq  expense_maint currency  is_lapse_dynamic
        space
        FIA           5000            500      USD              True
        GMXB          5000            500      USD              True
        GLWB          6000            600      USD              True

        >>> m.BaseData.product_params("GMXB")
                            has_gmdb  has_gmab  ... dyn_lapse_param_id  dyn_lapse_floor
        product_id plan_id                      ...
        GMDB       PLAN_A       True     False  ...             DL001A             0.00
                   PLAN_B       True     False  ...             DL001B             0.00
        GMAB       PLAN_A       True      True  ...             DL002A             0.03
                   PLAN_B       True      True  ...             DL002B             0.05

        [4 rows x 16 columns]
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def const_params():
    """Constant parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="ConstParams",
                         index_col="parameter")


def param_list():
    """List of fixed parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="ParamList",
                         index_col="parameter")


def product_params(space_name: str):
    """Product parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name=space_name,
                         index_col=[0, 1])


def run_params():
    """Run parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="RunParams",
                         index_col="run_id",
                         dtype={"date_id": object, "asmp_id": object})


def space_params():
    """Space parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="SpaceParams",
                         index_col="space")


def stacked_surr_charge_tables():
    """Stacked surrender charge tables"""
    return surr_charge_tables().stack().swaplevel(0, 1).sort_index()


def surr_charge_len():
    """Duration length of the surrender charge table"""
    return len(surr_charge_tables())


def surr_charge_tables():
    """Surrender charge tables"""
    dir_ = _model.path.parent / const_params().at["table_dir", "value"]
    file = const_params().at["spec_tables", "value"]
    return pd.read_excel(dir_ / file, sheet_name="SurrCharge", index_col=0)


# ---------------------------------------------------------------------------
# References

parameter_file = "model_parameters.xlsx"