"""The space representing economic data

This space is parameterized with :attr:`date_id` and :attr:`sens_id`.
For each combination of :attr:`date_id` and :attr:`sens_id` values,
a dynamic subspace of this space is created,
representing a specific set of economic assumptions.

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


Example:

    The sample code below demonstrates how to examine the contents of
    :mod:`~appliedlife.IntegratedLife.Scenarios`
    for specific values of :attr:`date_id` and :attr:`sens_id`, '202312' and 'BASE'.

    .. code-block:: python

        >>> import modelx as mx

        >>> m = mx.read_model("IntegratedLife")

        >>> m.Scenarios['202312', 'BASE'].spot_rates()

                 EUR      GBP      JPY      USD
        0    0.03357  0.04735  0.00072  0.04760
        1    0.02690  0.04021  0.00191  0.04056
        2    0.02439  0.03668  0.00280  0.03724
        3    0.02350  0.03475  0.00363  0.03571
        4    0.02323  0.03355  0.00448  0.03499
        ..       ...      ...      ...      ...
        145  0.03241  0.03229  0.03006  0.03364
        146  0.03243  0.03231  0.03010  0.03365
        147  0.03244  0.03232  0.03013  0.03365
        148  0.03245  0.03234  0.03016  0.03366
        149  0.03247  0.03235  0.03019  0.03366

        [150 rows x 4 columns]

        >>> m.Scenarios['202312', 'BASE'].forward_rates()

                  EUR       GBP       JPY       USD
        0    0.033570  0.047350  0.000720  0.047600
        1    0.020273  0.033119  0.003101  0.033567
        2    0.019388  0.029656  0.004582  0.030632
        3    0.020835  0.028982  0.006124  0.031134
        4    0.022151  0.028764  0.007887  0.032115
        ..        ...       ...       ...       ...
        145  0.033861  0.033741  0.034419  0.035091
        146  0.035354  0.035234  0.035957  0.035111
        147  0.033911  0.033791  0.034550  0.033650
        148  0.033931  0.035304  0.034610  0.035141
        149  0.035454  0.033841  0.034670  0.033660

        [150 rows x 4 columns]

        >>> m.Scenarios['202312', 'BASE'].cont_fwd_rates()

                  EUR       GBP       JPY       USD
        0    0.033019  0.046263  0.000720  0.046502
        1    0.020070  0.032582  0.003097  0.033016
        2    0.019203  0.029225  0.004572  0.030172
        3    0.020621  0.028570  0.006105  0.030659
        4    0.021909  0.028358  0.007856  0.031610
        ..        ...       ...       ...       ...
        145  0.033300  0.033184  0.033840  0.034489
        146  0.034744  0.034628  0.035325  0.034509
        147  0.033349  0.033233  0.033966  0.033096
        148  0.033368  0.034695  0.034024  0.034538
        149  0.034840  0.033281  0.034082  0.033106

        [150 rows x 4 columns]

        >>> m.Scenarios['202312', 'BASE'].log_return_mth()

                      FUND1     FUND2     FUND3     FUND4     FUND5     FUND6
        scen t
        1    0    -0.030397  0.047032 -0.010060  0.000816  0.000665 -0.040567
             1    -0.029103  0.025734  0.004162 -0.018741  0.084592  0.058125
             2    -0.015052  0.034508 -0.005399  0.003108  0.030602 -0.070345
             3     0.015784  0.051717  0.015262  0.000348  0.034553 -0.091414
             4    -0.001168  0.018826 -0.015521  0.002865  0.063022  0.153368
                    ...       ...       ...       ...       ...       ...
        100  1795  0.005044  0.005891  0.006421 -0.009772  0.006747 -0.018034
             1796  0.005050 -0.030197 -0.027247  0.002810 -0.017504  0.011297
             1797  0.070869  0.008339  0.012401 -0.002405  0.014219 -0.023541
             1798 -0.001515  0.049597  0.013523 -0.015077  0.070503  0.027821
             1799  0.000753 -0.019089  0.017222  0.004629  0.005042  0.000108

        [180000 rows x 6 columns]

        >>> m.Scenarios['202312', 'BASE'].return_mth()

                      FUND1     FUND2     FUND3     FUND4     FUND5     FUND6
        scen t
        1    0    -0.029940  0.048156 -0.010010  0.000816  0.000665 -0.039755
             1    -0.028684  0.026068  0.004171 -0.018567  0.088273  0.059847
             2    -0.014940  0.035111 -0.005384  0.003113  0.031075 -0.067928
             3     0.015909  0.053078  0.015379  0.000348  0.035157 -0.087360
             4    -0.001168  0.019004 -0.015401  0.002869  0.065050  0.165754
                    ...       ...       ...       ...       ...       ...
        100  1795  0.005057  0.005909  0.006442 -0.009724  0.006770 -0.017872
             1796  0.005063 -0.029746 -0.026880  0.002814 -0.017352  0.011361
             1797  0.073441  0.008374  0.012478 -0.002402  0.014320 -0.023266
             1798 -0.001514  0.050848  0.013615 -0.014964  0.073048  0.028211
             1799  0.000753 -0.018908  0.017371  0.004640  0.005055  0.000108

        [180000 rows x 6 columns]
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