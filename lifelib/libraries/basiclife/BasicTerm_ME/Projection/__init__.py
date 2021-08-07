"""The main Space in the :mod:`~basiclife.BasicTerm_M` model.

:mod:`~basiclife.BasicTerm_M.Projection` is the only Space defined
in the :mod:`~basiclife.BasicTerm_M` model, and it contains
all the logic and data used in the model.

.. rubric:: Parameters and References

(In all the sample code below,
the global variable ``Projection`` refers to the
:mod:`~basiclife.BasicTerm_M.Projection` Space.)

Attributes:

    model_point_table: All model point data as a DataFrame.
        The sample model point data was generated by
        *generate_model_points.ipynb* included in the library.
        By default, :func:`model_point` returns this :attr:`model_point_table`.
        The DataFrame has columns labeled ``age_at_entry``,
        ``sex``, ``policy_term``, ``policy_count``
        and ``sum_assured``.
        Cells defined in :mod:`~basiclife.BasicTerm_M.Projection`
        with the same names as these columns return
        the corresponding columns.
        (``policy_count`` is not used by default.)

        .. code-block::

            >>> Projection.model_poit_table
                       age_at_entry sex  policy_term  policy_count  sum_assured
            point_id
            1                    47   M           10             1       622000
            2                    29   M           20             1       752000
            3                    51   F           10             1       799000
            4                    32   F           20             1       422000
            5                    28   M           15             1       605000
                            ...  ..          ...           ...          ...
            9996                 47   M           20             1       827000
            9997                 30   M           15             1       826000
            9998                 45   F           20             1       783000
            9999                 39   M           20             1       302000
            10000                22   F           15             1       576000

            [10000 rows x 5 columns]

        The DataFrame is saved in the Excel file *model_point_table.xlsx*
        placed in the model folder.
        :attr:`model_point_table` is created by
        Projection's `new_pandas`_ method,
        so that the DataFrame is saved in the separate file.
        The DataFrame has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.model_point_table._mx_dataclient
            <PandasData path='model_point_table.xlsx' filetype='excel'>

        .. seealso::

           * :func:`model_point`
           * :func:`age_at_entry`
           * :func:`sex`
           * :func:`policy_term`
           * :func:`sum_assured`


    disc_rate_ann: Annual discount rates by duration as a pandas Series.

        .. code-block::

            >>> Projection.disc_rate_ann
            year
            0      0.00000
            1      0.00555
            2      0.00684
            3      0.00788
            4      0.00866

            146    0.03025
            147    0.03033
            148    0.03041
            149    0.03049
            150    0.03056
            Name: disc_rate_ann, Length: 151, dtype: float64

        The Series is saved in the Excel file *disc_rate_ann.xlsx*
        placed in the model folder.
        :attr:`disc_rate_ann` is created by
        Projection's `new_pandas`_ method,
        so that the Series is saved in the separate file.
        The Series has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.disc_rate_ann._mx_dataclient
            <PandasData path='disc_rate_ann.xlsx' filetype='excel'>

        .. seealso::

           * :func:`disc_rate_mth`
           * :func:`disc_factors`

    mort_table: Mortality table by age and duration as a DataFrame.
        See *basic_term_sample.xlsx* included in this library
        for how the sample mortality rates are created.

        .. code-block::

            >>> Projection.mort_table
                        0         1         2         3         4         5
            Age
            18   0.000231  0.000254  0.000280  0.000308  0.000338  0.000372
            19   0.000235  0.000259  0.000285  0.000313  0.000345  0.000379
            20   0.000240  0.000264  0.000290  0.000319  0.000351  0.000386
            21   0.000245  0.000269  0.000296  0.000326  0.000359  0.000394
            22   0.000250  0.000275  0.000303  0.000333  0.000367  0.000403
            ..        ...       ...       ...       ...       ...       ...
            116  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            117  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            118  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            119  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            120  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000

            [103 rows x 6 columns]

        The DataFrame is saved in the Excel file *mort_table.xlsx*
        placed in the model folder.
        :attr:`mort_table` is created by
        Projection's `new_pandas`_ method,
        so that the DataFrame is saved in the separate file.
        The DataFrame has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.mort_table._mx_dataclient
            <PandasData path='mort_table.xlsx' filetype='excel'>

        .. seealso::

           * :func:`mort_rate`
           * :func:`mort_rate_mth`

    np: The `numpy`_ module.
    pd: The `pandas`_ module.

.. _numpy:
   https://numpy.org/

.. _pandas:
   https://pandas.pydata.org/

.. _new_pandas:
   https://docs.modelx.io/en/latest/reference/space/generated/modelx.core.space.UserSpace.new_pandas.html

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """Target model points

    Returns as a DataFrame the model points to be in the scope of calculation.
    By default, this Cells returns the entire :attr:`model_point_table`
    without change.
    To select model points, change this formula so that this
    Cells returns a DataFrame that contains only the selected model points.

    Examples:
        To select only the model point 1::

            def model_point():
                return model_point_table.loc[1:1]

        To select model points whose ages at entry are 40 or greater::

            def model_point():
                return model_point_table[model_point_table["age_at_entry"] >= 40]

    Note that the shape of the returned DataFrame must be the
    same as the original DataFrame, i.e. :attr:`model_point_table`.

    When selecting only one model point, make sure the
    returned object is a DataFrame, not a Series, as seen in the example
    above where ``model_point_table.loc[1:1]`` is specified
    instead of ``model_point_table.loc[1]``.

    Be careful not to accidentally change the original table.
    """
    return model_point_table


def sum_assured():
    """The sum assured of the model points

    The ``sum_assured`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()["sum_assured"]


def age_at_entry():
    """The age at entry of the model points

    The ``age_at_entry`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()["age_at_entry"]


def sex():
    """The sex of the model points

    The ``sex`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()["sex"]


def proj_len():
    """Projection length in months

    Projection length in months defined as::

        12 * policy_term() + 1

    .. seealso::

        :func:`policy_term`

    """
    return np.maximum(12 * policy_term() - duration_mth(0) + 1, 0)


max_proj_len = lambda: max(proj_len())
"""The max of all projection lengths"""

def disc_factors():
    """Discount factors.

    Vector of the discount factors as a Numpy array. Used for calculating
    the present values of cashflows.

    .. seealso::

        :func:`disc_rate_mth`
    """
    return np.array(list((1 + disc_rate_mth()[t])**(-t) for t in range(max_proj_len())))


def net_cf(t):
    """Net cashflow

    Net cashflow for the period from ``t`` to ``t+1`` defined as::

        premiums(t) - claims(t) - expenses(t) - commissions(t)

    .. seealso::

        * :func:`premiums`
        * :func:`claims`
        * :func:`expenses`
        * :func:`commissions`

    """
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


def premium_pp(t):
    """Monthly premium per policy

    Monthly premium amount per policy defined as::

        round((1 + loading_prem()) * net_premium(), 2)

    .. seealso::

        * :func:`loading_prem`
        * :func:`net_premium_pp`

    """
    return np.around((1 + loading_prem()) * net_premium_pp(), 2)


def claim_pp(t):
    """Claim per policy

    The claim amount per plicy. Defaults to :func:`sum_assured`.
    """
    return sum_assured()


def inflation_factor(t):
    """The inflation factor at time t

    .. seealso::

        * :func:`inflation_rate`

    """
    return (1 + inflation_rate())**(t//12)


def premiums(t):
    """Premium income

    Premium income during the period from ``t`` to ``t+1`` defined as::

        premium_pp(t) * pols_if(t)

    .. seealso::

        * :func:`premium_pp`
        * :func:`pols_if`

    """
    return premium_pp(t) * pols_if_at(t, "BEF_DECR")


def duration(t):
    """Duration in force in years"""
    return duration_mth(t) //12


def claims(t):
    """Claims

    Claims during the period from ``t`` to ``t+1`` defined as::

        claim_pp(t) * pols_death(t)

    .. seealso::

        * :func:`claim_pp`
        * :func:`pols_death`

    """
    return claim_pp(t) * pols_death(t)


def expenses(t):
    """Expenses

    Expense during the period from ``t`` to ``t+1``.
    At ``t=0``, it is defined as :func:`expense_acq`.
    For ``t=1`` and onwards, defined as::

        pols_if(t) * expense_maint()/12 * inflation_factor(t)

    .. seealso::

        * :func:`pols_if`
        * :func:`expense_maint`
        * :func:`inflation_factor`

    """

    return expense_acq() * pols_new_biz(t) \
        + pols_if_at(t, "BEF_DECR") * expense_maint()/12 * inflation_factor(t)


def age(t):
    """The attained age at time t.

    Defined as::

        age_at_entry() + duration(t)

    .. seealso::

        * :func:`age_at_entry`
        * :func:`duration`

    """
    return age_at_entry() + duration(t)


def disc_rate_mth():
    """Monthly discount rate

    Nummpy array of monthly discount rates from time 0 to :func:`max_proj_len` - 1
    defined as::

        (1 + disc_rate_ann)**(1/12) - 1

    .. seealso::

        :func:`disc_rate_ann`

    """
    return np.array(list((1 + disc_rate_ann[t//12])**(1/12) - 1 for t in range(max_proj_len())))


def lapse_rate(t):
    """Lapse rate

    By default, the lapse rate assumption is defined by duration as::

        max(0.1 - 0.02 * duration(t), 0.02)

    .. seealso::

        :func:`duration`

    """
    return np.maximum(0.1 - 0.02 * duration(t), 0.02)


def pv_pols_if():
    """Present value of policies in-force

    The discounted sum of the number of in-force policies at each month.
    It is used as the annuity factor for calculating :func:`net_premium_pp`.

    """
    result = np.array(list(pols_if_at(t, "BEF_DECR") for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_net_cf():
    """Present value of net cashflows.

    Defined as::

        pv_premiums() - pv_claims() - pv_expenses() - pv_commissions()

    .. seealso::

        * :func:`pv_premiums`
        * :func:`pv_claims`
        * :func:`pv_expenses`
        * :func:`pv_commissions`

    """
    return pv_premiums() - pv_claims() - pv_expenses() - pv_commissions()


def commissions(t):
    """Commissions

    By default, 100% premiums for the first year, 0 otherwise.

    .. seealso::

        * :func:`premiums`
        * :func:`duration`

    """
    return (duration(t) == 0) * premiums(t)


def inflation_rate():
    """Inflation rate"""
    return 0.01


def pols_death(t):
    """Number of death occurring at time t"""
    return pols_if_at(t, "BEF_DECR") * mort_rate_mth(t)


def pols_if(t):
    """Number of Policies In-force

    Number of in-force policies calculated recursively.
    The initial value is read from :func:`pols_if_init`.
    Subsequent values are defined recursively as::

        pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1) - pols_maturity(t)

    .. seealso::
        * :func:`pols_lapse`
        * :func:`pols_death`
        * :func:`pols_maturity`

    """
    return pols_if_at(t, "BEF_MAT")


def pols_lapse(t):
    """Number of lapse occurring at time t

    .. seealso::
        * :func:`pols_if`
        * :func:`lapse_rate`

    """
    return pols_if_at(t, "BEF_DECR") * (1-(1 - lapse_rate(t))**(1/12))


def pv_claims():
    """Present value of claims

    .. seealso::

        * :func:`claims`

    """
    cl = np.array(list(claims(t) for t in range(max_proj_len()))).transpose()

    return cl @ disc_factors()[:max_proj_len()]


def pv_commissions():
    """Present value of commissions

    .. seealso::

        * :func:`expenses`

    """
    result = np.array(list(commissions(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_expenses():
    """Present value of expenses

    .. seealso::

        * :func:`expenses`

    """
    result = np.array(list(expenses(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_premiums():
    """Present value of premiums

    .. seealso::

        * :func:`premiums`

    """
    result = np.array(list(premiums(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def expense_acq():
    """Acquisition expense per policy

    ``300`` by default.
    """
    return 300


def expense_maint():
    """Annual maintenance expence per policy

    ``60`` by default.
    """
    return 60


def loading_prem():
    """Loading per premium

    ``0.5`` by default.

    .. seealso::

        * :func:`premium_pp`

    """
    return 0.5


def mort_rate(t):
    """Mortality rate to be applied at time t

    .. seealso::

       * :attr:`mort_table`
       * :func:`mort_rate_mth`

    """
    # result = mort_table[str(min(5, duration(t)))][age(t)]
    # result.index = model_point().index
    # return result

    mi = pd.MultiIndex.from_arrays([age(t), np.minimum(duration(t), 5)])
    return mort_table_reindexed().reindex(
        mi, fill_value=0).set_axis(model_point().index)


def mort_rate_mth(t):
    """Monthly mortality rate to be applied at time t

    .. seealso::

       * :attr:`mort_table`
       * :func:`mort_rate`

    """
    return 1-(1- mort_rate(t))**(1/12)


def result_pv():
    """Result table of present value of cashflows

    .. seealso::

       * :func:`pv_premiums`
       * :func:`pv_claims`
       * :func:`pv_expenses`
       * :func:`pv_commissions`
       * :func:`pv_net_cf`

    """


    data = {
        "PV Premiums": pv_premiums(),
        "PV Claims": pv_claims(),
        "PV Expenses": pv_expenses(),
        "PV Commissions": pv_commissions(),
        "PV Net Cashflow": pv_net_cf()
    }

    return pd.DataFrame(data, index=model_point().index)


def result_cf():
    """Result table of cashflows

    .. seealso::

       * :func:`premiums`
       * :func:`claims`
       * :func:`expenses`
       * :func:`commissions`
       * :func:`net_cf`

    """

    t_len = range(max_proj_len())

    data = {
        "Premiums": [sum(premiums(t)) for t in t_len],
        "Claims": [sum(claims(t)) for t in t_len],
        "Expenses": [sum(expenses(t)) for t in t_len],
        "Commissions": [sum(commissions(t)) for t in t_len],
        "Net Cashflow": [sum(net_cf(t)) for t in t_len]
    }

    return pd.DataFrame(data, index=t_len)


def pols_if_init():
    """Initial Number of Policies In-force

    Number of in-force policies at time 0 referenced from :func:`pols_if`.
    Defaults to 1.
    """
    return model_point()["policy_count"].where(duration_mth(0) > 0, other=0)


def policy_term():
    """The policy term of the model points.

    The ``policy_term`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()["policy_term"]


def net_premium_pp():
    """Net premium per policy

    The net premium per policy is defined so that
    the present value of net premiums equates to the present value of
    claims::

        pv_claims() / pv_pols_if()

    .. seealso::

        * :func:`pv_claims`
        * :func:`pv_pols_if`

    """
    # return pv_claims() / pv_pols_if()
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.nan_to_num(pv_claims() / pv_pols_if())


def pols_maturity(t):
    """Number of maturing policies

    The policy maturity occurs at ``t == 12 * policy_term()``,
    after death and lapse during the last period::

        pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)

    otherwise ``0``.
    """
    return (duration_mth(t) == policy_term() * 12) * pols_if_at(t, "BEF_MAT")


def duration_mth(t):
    if t == 0:
        return model_point()['duration_mth']
    else:
        return duration_mth(t-1) + 1


def pols_new_biz(t):
    return model_point()['policy_count'].where(duration_mth(t) == 0, other=0)


def pols_if_at(t, timing):
    """

    - t-1, "AFT_DECR", "BEF_MAT"
    - t-1, "AFT_MAT", "BEF_NB"
    - t-1, "AFT_NB", "BEF_DECR"
    - t, "AFT_DECR", "BEF_MAT"

    """
    if timing == "BEF_MAT":

        if t == 0:
            return pols_if_init()
        else:
            return pols_if_at(t-1, "BEF_DECR") - pols_lapse(t-1) - pols_death(t-1)

    elif timing == "BEF_NB":

        return pols_if_at(t, "BEF_MAT") - pols_maturity(t)

    elif timing == "BEF_DECR":

        return pols_if_at(t, "BEF_NB") + pols_new_biz(t)

    else:
        raise ValueError("invalid timing")


def mort_table_reindexed():
    """MultiIndexed Mortality Table

    Returns a Series of mortlity rates reshaped from :attr:`mortality_table`.
    The returned Series is indexed by age and duration.

    """
    result = []
    for col in mort_table.columns:
        df = mort_table[[col]]
        df = df.assign(Duration=int(col)).set_index('Duration', append=True)[col]
        result.append(df)

    return pd.concat(result)


def result_pols():
    """Result table of cashflows

    .. seealso::

       * :func:`premiums`
       * :func:`claims`
       * :func:`expenses`
       * :func:`commissions`
       * :func:`net_cf`

    """

    t_len = range(max_proj_len())

    data = {
        "pols_if": [sum(pols_if(t)) for t in t_len],
        "pols_maturity": [sum(pols_maturity(t)) for t in t_len],
        "pols_new_biz": [sum(pols_new_biz(t)) for t in t_len],
        "pols_death": [sum(pols_death(t)) for t in t_len],
        "pols_lapse": [sum(pols_lapse(t)) for t in t_len]
    }

    return pd.DataFrame(data, index=t_len)


# ---------------------------------------------------------------------------
# References

disc_rate_ann = ("DataClient", 2234521425280)

mort_table = ("DataClient", 2234521427152)

np = ("Module", "numpy")

pd = ("Module", "pandas")

model_point_table = ("DataClient", 2234543164384)