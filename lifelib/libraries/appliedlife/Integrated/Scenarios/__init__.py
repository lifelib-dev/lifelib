from modelx.serialize.jsonvalues import *

_formula = lambda date_id, sensitivity: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def spot_rates():

    dir_name: str = input_data.const_params().at["scen_dir", "value"]
    file_prefix: str = input_data.const_params().at["int_rate_prefix", "value"]

    path = _model.path.parent / dir_name / f"{file_prefix}_{date_id}.xlsx"
    return pd.read_excel(path, sheet_name=sensitivity, index_col=0)


def forward_rates():
    df = (1 + spot_rates()).pow(spot_rates().index + 1, axis=0)
    return df / df.shift(fill_value=1) - 1


def index_vols():
    return index_params()["volatility"]


scen_size = lambda: 100

scen_index = lambda: pd.MultiIndex.from_product(
    [range(1, scen_size() + 1), range(12 * scen_len())],
    names=["scen", "t"])

def scenarios():

    # Initialize random number generator
    rng = np.random.default_rng(12345)

    # Define parameters
    dt = 1/12
    rf =  cont_fwd_rates()[index_params()["currency"]].loc[np.repeat(cont_fwd_rates().index, 12)]
    vols = index_vols().values
    mean = (rf  - 0.5 * vols**2) * dt
    var = vols * dt**0.5

    # Generate
    result = np.zeros((scen_size() * scen_len() * 12, index_count()))
    for i in range(scen_size()):
        scen = rng.normal(loc=mean, scale=var)
        result[i * scen.shape[0]:(i + 1) * scen.shape[0], 0:scen.shape[1]] = scen

    return pd.DataFrame(result, index=scen_index(), columns=index_params().index)


cont_fwd_rates = lambda: np.log(1 + forward_rates())

scen_len = lambda: len(spot_rates())

def index_params():

    dir_name: str = input_data.const_params().at["scen_dir", "value"]
    file_name: str = input_data.const_params().at["scen_param_file", "value"]

    file = _model.path.parent / dir_name / file_name
    df = pd.read_excel(file,
                         sheet_name="Params",
                         index_col=0)

    return df.T.astype(
        {"currency": "object", 
         "return": "float64", 
         "volatility": "float64"})


def index_count():
    return index_params().index.size


def mth_index():
    return scenarios()


# ---------------------------------------------------------------------------
# References

input_data = ("Interface", ("..", "InputData"), "auto")

date_id = "202312"

sensitivity = "BASE"