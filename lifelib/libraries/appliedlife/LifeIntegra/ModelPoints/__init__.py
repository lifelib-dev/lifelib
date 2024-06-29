from modelx.serialize.jsonvalues import *

_formula = lambda mp_file_id, space_name: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point_table():

    dir_name: str = base_data.const_params().at["model_point_dir", "value"]
    file_name: str = (base_data.const_params().at["model_point_file_prefix", "value"]
                      + "_" + mp_file_id + "_" + space_name + ".csv")

    return pd.read_csv(_model.path.parent / dir_name / file_name, index_col="point_id", parse_dates=["entry_date"])


def model_point_table_ext(): 
    return pd.merge(model_point_table().reset_index(), 
                    base_data.product_params(space_name).reset_index(),
                    how="left",
                    on=["product_id", "plan_id"]).set_index('point_id')


# ---------------------------------------------------------------------------
# References

base_data = ("Interface", ("..", "BaseData"), "auto")

space_name = "GMXB"

date_id = "202312"