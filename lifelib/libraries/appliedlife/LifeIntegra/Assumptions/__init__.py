from modelx.serialize.jsonvalues import *

_formula = lambda asmp_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def lapse_tables():

    return pd.read_excel(
        asmp_file(),
        sheet_name="Lapse",
        index_col=0)


def asmp_file():

    dir_ = base_data.const_params().at["table_dir", "value"]

    return _model.path.parent / dir_ / ("assumptions_" + date_id + ".xlsx")


def mort_scalar_tables():

    df = pd.read_excel(
        asmp_file(),
        sheet_name="Mortality",
        index_col=0)
    return df


lapse_len = lambda: len(lapse_tables())

mort_scalar_len = lambda: len(mort_scalar())

def stacked_lapse_tables():
    return lapse_tables().stack().swaplevel(0, 1).sort_index()


def stacked_mort_scalar_tables():
    return mort_scalar_tables().stack().swaplevel(0, 1).sort_index()


def dyn_lapse_params():

    return pd.read_excel(
        asmp_file(),
        sheet_name="DynLapse",
        index_col=0)


# ---------------------------------------------------------------------------
# References

base_data = ("Interface", ("..", "BaseData"), "auto")

date_id = "202312"