"""Space to calculate premiums

This space is for calculating premiums.
To calculate premiums, :func:`~model_point` adjusts
the issue ages read from
:attr:`~basiclife.BasicTermASL_ME.Base.model_point_table`
so that all the model points become new business issued the day after
:func:`date_(0)<basiclife.BasicTermASL_ME.Base.date_>`.

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = [
    ".Base"
]

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """Target model points

    :func:`model_point` adjusts the issue date colum of the DataFrame
    read from
    :attr:`~basiclife.BasicTermASL_ME.Base.model_point_table`
    for the pricing purpose.
    For all model points, the issue dates are set to the
    date one day after :func:`date_(0)<basiclife.BasicTermASL_ME.Base.date_>`.
    """
    iss_d = pd.Series(date_(0) + pd.DateOffset(days=1), index=model_point_table.index)
    return model_point_table.assign(issue_date=iss_d)


def net_premium_rate():
    """Net premium 1000 sum assured.

    Calculates and returns a Series of net premium rates
    per 1000 sum assured per payment for all model points.
    Defined as:

        (1000 / sum_assured()) * pv_claims() / pv_pols_if_pay()

    .. seealso::

        * :func:`sum_assured`
        * :func:`pv_claims`
        * :func:`pv_pols_if_pay`

    """
    return np.nan_to_num((1000 / sum_assured()) * pv_claims() / pv_pols_if_pay())


def premium_pp():
    """Premium per policy

    Returns a Series of premiums per policy per payment for all model points,
    defined as::

        (1 + loading_prem()) * (sum_assured() / 1000) * net_premium_rate()

    .. seealso::

        * :func:`~basiclife.BasicTermASL_ME.Base.loading_prem`
        * :func:`~basiclife.BasicTermASL_ME.Base.sum_assured`
        * :func:`~net_premium_rate`

    """
    return np.round_((1 + loading_prem()) * (sum_assured() / 1000) * net_premium_rate(), 2)


