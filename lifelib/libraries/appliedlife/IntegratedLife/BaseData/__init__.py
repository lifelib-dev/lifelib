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

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def run_params():
    """Run parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="RunParams",
                         index_col="run_id",
                         dtype={"date_id": object, "asmp_id": object})


def const_params():
    """Constant parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="ConstParams",
                         index_col="parameter")


def space_params():
    """Space parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="SpaceParams",
                         index_col="space")


def product_params(space_name: str):
    """Product parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name=space_name,
                         index_col=[0, 1])


def param_list():
    """List of fixed parameters"""
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="ParamList",
                         index_col="parameter")


def surr_charge_tables():
    """Surrender charge tables"""
    dir_ = _model.path.parent / const_params().at["table_dir", "value"]
    file = const_params().at["spec_tables", "value"]
    return pd.read_excel(dir_ / file, sheet_name="SurrCharge", index_col=0)


def stacked_surr_charge_tables():
    """Stacked surrender charge tables"""
    return surr_charge_tables().stack().swaplevel(0, 1).sort_index()


def surr_charge_len():
    """Duration length of the surrender charge table"""
    return len(surr_charge_tables())


# ---------------------------------------------------------------------------
# References

parameter_file = "model_parameters.xlsx"