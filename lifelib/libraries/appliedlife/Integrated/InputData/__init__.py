from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def run_params():
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="RunParams",
                         index_col="run_id",
                         dtype={"date_id": object})


def const_params():
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="ConstParams",
                         index_col="parameter")


def space_params():
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="SpaceParams",
                         index_col="space")


def product_params(space_name: str):
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name=space_name,
                         index_col=[0, 1])


def param_list():
    return pd.read_excel(_model.path.parent / parameter_file,
                         sheet_name="ParamList",
                         index_col="parameter")


def surr_charge_tables():

    dir_ = _model.path.parent / const_params().at["table_dir", "value"]
    file = const_params().at["spec_tables", "value"]
    return pd.read_excel(dir_ / file, sheet_name="SurrCharge", index_col=0)


def stacked_surr_charge_tables():
    return surr_charge_tables().stack().swaplevel(0, 1).sort_index()


surr_charge_len = lambda: len(surr_charge_tables())

# ---------------------------------------------------------------------------
# References

parameter_file = "model_parameters.xlsx"