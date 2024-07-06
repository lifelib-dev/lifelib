"""The space representing economic data

The Scenarios space represents economic data.
This space serves as the base space for its dynamic sub spaces.
and it is parameterized with date_id and sens_id.
Both parameters are string IDs, indicating what date and sensitivity
combination should be used for each dynamic instance of this space.

By default, the following scenarios are supported.
Users should customize the contents of this space to meet their own needs.

* Deterministic interest rate scenarios
* Stochastic risk-neutral index return scenarios

For the interest rate scenarios,
:func:`spot_rates` in this space reads annual spot rates from an Excel file into it.
:func:`spot_rates` uses sens_is as a key to select a sheet from the file.

For the stochastic risk-neutral index return scenarios,
:func:`log_return_mth` generates stochastic returns,
from the interest rates and volatility parameters read from an Excel file.

.. rubric:: Parameters

Attributes:

    date_id: a string key representing the base date
    sens_id: a string key representing interest rate sensitivity, which is either
        "BASE", "UP" or "DOWN".

.. rubric:: References in the space

Attributes:

    base_data: Reference to the :mod:`~appliedlife.IntegratedLife.BaseData` space

"""

from modelx.serialize.jsonvalues import *

_formula = lambda date_id, sens_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def cont_fwd_rates():
    """Continuous compound forward rates"""
    return np.log(1 + forward_rates())


def forward_rates():
    """Forward interest rates by duration and currency

    Returns annual forward interest rates for multiple currencies
    as a pandas DataFrame, calculated from :func:`spot_rates`.
    """
    df = (1 + spot_rates()).pow(spot_rates().index + 1, axis=0)
    return df / df.shift(fill_value=1) - 1


def index_count():
    """The number of func indexes"""
    return index_params().index.size


def index_params():
    """Fund index parameters

    Reads fund index parameters from an Excel file,
    and returns a DataFrame whose columns represents the parameters,
    and whose index represents fund index IDs.
    """

    dir_name: str = base_data.const_params().at["scen_dir", "value"]
    file_name: str = base_data.const_params().at["scen_param_file", "value"]

    file = _model.path.parent / dir_name / file_name
    df = pd.read_excel(file,
                         sheet_name="Params",
                         index_col=0)

    return df.T.astype(
        {"currency": "object", 
         "return": "float64", 
         "volatility": "float64"})


def index_vols():
    """Volatilities of fund indexes"""
    return index_params()["volatility"]


def log_return_mth():
    """Stochastic scenarios of fund indexes as monthly risk-neutral log returns

    Generates stochastic scenarios of fund indexes
    Generates monthly risk-neutral log returns of fund indexes,
    Returns a DataFrame with columns of fund IDs
    and with a MultiIndex with two levels, scenario ID and time in month.
    """

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


def mth_index():
    return scenarios()


def return_mth():
    """Monthly index returns"""
    return np.exp(log_return_mth()) - 1


def scen_index():
    """pandas MultiIndex for the scenarios"""
    return pd.MultiIndex.from_product(
    [range(1, scen_size() + 1), range(12 * scen_len())],
    names=["scen", "t"])


def scen_len():
    """The length of scenarios in years"""
    return len(spot_rates())


def scen_size():
    """The number of scenarios"""
    return 100


def spot_rates():
    """Spot interest rates by duration and currency

    Reads annual spot interest rates for multiple currencies from an Excel file,
    and returns them as a pandas DataFrame.
    The index and columns of the DataFrame represents duration
    years and currencies respectively

    The directory of the Excel file is specified by the user as a constant
    parameter named "scen_dir".
    """

    dir_name: str = base_data.const_params().at["scen_dir", "value"]
    file_prefix: str = base_data.const_params().at["scen_file_prefix", "value"]

    path = _model.path.parent / dir_name / f"{file_prefix}_{date_id}.xlsx"
    return pd.read_excel(path, sheet_name=sens_id, index_col=0)


# ---------------------------------------------------------------------------
# References

base_data = ("Interface", ("..", "BaseData"), "auto")

date_id = "202312"

sens_id = "BASE"