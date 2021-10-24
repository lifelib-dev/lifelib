"""The main Space in the :mod:`~savings.CashValue_ME` model.

:mod:`~savings.CashValue_ME.Projection` is the only Space defined
in the :mod:`~savings.CashValue_ME` model, and it contains
all the logic and data used in the model.

.. rubric:: Parameters and References

(In all the sample code below,
the global variable ``Projection`` refers to the
:mod:`~savings.CashValue_ME.Projection` Space.)

Attributes:

    model_point_table: All model points as a DataFrame.
        By default, 4 model points are defined.
        The DataFrame has an index named ``point_id``.

            * ``spec_id``
            * ``age_at_entry``
            * ``sex``
            * ``policy_term``
            * ``policy_count``
            * ``sum_assured``
            * ``duration_mth``
            * ``premium_pp``
            * ``av_pp_init``

        Cells defined in :mod:`~savings.CashValue_ME.Projection`
        with the same names as these columns return
        the corresponding column's values for the selected model point.

        .. code-block::

            >>> Projection.model_poit_table
                     spec_id  age_at_entry sex  ...  premium_pp  av_pp_init
            poind_id                            ...
            1              A            20   M  ...      500000           0
            2              B            50   M  ...      500000           0
            3              C            20   M  ...        1000           0
            4              D            50   M  ...        1000           0

            [4 rows x 10 columns]

        The DataFrame is saved in the Excel file *model_point_samples.xlsx*
        placed in the model folder.
        :attr:`model_point_table` is created by
        Projection's `new_pandas`_ method,
        so that the DataFrame is saved in the separate file.
        The DataFrame has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.model_point_table._mx_dataclient
            <PandasData path='model_point_table_samples.xlsx' filetype='excel'>

        .. seealso::

           * :func:`model_point`
           * :func:`age_at_entry`
           * :func:`sex`
           * :func:`policy_term`
           * :func:`pols_if_init`
           * :func:`sum_assured`
           * :func:`duration_mth`
           * :func:`premium_pp`
           * :func:`av_pp_init`

    model_point_10000: Alternative model point table

        This model point table contains 10000 model points and
        is saved as the Excel file *model_point_10000.xlsx*
        placed in the folder. To use this table, assign it to
        :attr:`model_point_table`::

            >>> Projection.model_point_table = Projection.model_point_10000


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

    std_norm_rand: Random numbers drawn from the standard normal distribution

        A Series of random numbers drawn from the standard normal distribution
        indexed with ``scen_id`` and ``t``.
        Used for generating investment returns. See :func:`inv_return_table`.

    scen_id: Selected scenario ID

        An integer indicating the selected scenario ID.
        :attr:`scen_id` is referenced in by :func:`inv_return_mth`
        as one of the keys to select a scenario from :attr:`std_norm_rand`.

    surr_charge_table: Surrender charge rates by duration

        A DataFrame of multiple patterns of surrender charge rates by duration.
        The column labels indicate :func:`surr_charge_id`.
        By default, ``"type_1"``, ``"type_2"`` and ``"type_3"`` are defined.

    product_spec_table: Table of product specs

        A DataFrame of product spec parameters by ``spec_id``.
        :attr:`model_point_table` and :attr:`product_spec_table` columns
        are joined in :func:`model_point_table_ext`,
        and the :attr:`product_spec_table` columns become part
        of the model point attributes.
        The :attr:`product_spec_table` columns are read
        by the Cells with the same names as the columns:

        * :func:`premium_type`
        * :func:`has_surr_charge`
        * :func:`surr_charge_id`
        * :func:`load_prem_rate`
        * :func:`is_wl`

        .. code-block::

            >>> Projection.product_spec_table
                    premium_type  has_surr_charge surr_charge_id  load_prem_rate  is_wl
            spec_id
            A             SINGLE            False            NaN            0.10  False
            B             SINGLE             True         type_1            0.00  False
            C              LEVEL            False            NaN            0.10   True
            D              LEVEL             True         type_3            0.05   True


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

def age(t):
    """The attained age at time t.

    Defined as::

        age_at_entry() + duration(t)

    .. seealso::

        * :func:`age_at_entry`
        * :func:`duration`

    """
    return age_at_entry() + duration(t)


def age_at_entry():
    """The age at entry of the model points

    The ``age_at_entry`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()["age_at_entry"]


def av_at(t, timing):
    """Account value in-force

    :func:`av_at(t, timing)<av_at>` calculates
    the total amount of account value at time ``t`` for the policies represented
    by a model point.

    At each ``t``, the events that change the account value balance
    occur in the following order:

        * Maturity
        * New business and premium payment
        * Fee deduction

    The second parameter ``timing`` takes a string to
    indicate the timing of the account value, which is either
    ``"BEF_MAT"``, ``"BEF_NB"`` or ``"BEF_FEE"``.


    .. rubric:: BEF_MAT

    The amount of account value before maturity, defined as::

        av_pp_at(t, "BEF_PREM") * pols_if_at(t, "BEF_MAT")

    .. rubric:: BEF_NB

    The amount of account value before new business after maturity,
    defined as::

        av_pp_at(t, "BEF_PREM") * pols_if_at(t, "BEF_NB")

    .. rubric:: BEF_FEE

    The amount of account value before lapse and death after new business,
    defined as::

        av_pp_at(t, "BEF_FEE") * pols_if_at(t, "BEF_DECR")


    .. seealso::
        * :func:`pols_if_at`
        * :func:`av_pp_at`


    """
    if timing == "BEF_MAT":
        return av_pp_at(t, "BEF_PREM") * pols_if_at(t, "BEF_MAT")

    elif timing == "BEF_NB":
        return av_pp_at(t, "BEF_PREM") * pols_if_at(t, "BEF_NB")

    elif timing == "BEF_FEE":
        return av_pp_at(t, "BEF_FEE") * pols_if_at(t, "BEF_DECR")

    else:
        raise ValueError("invalid timing")


def av_change(t):
    """Change in account value

    Change in account value during each period, defined as::

        av_at(t+1, 'BEF_MAT') - av_at(t, 'BEF_MAT')

    .. seealso::

        * :func:`net_cf`

    """
    return av_at(t+1, 'BEF_MAT') - av_at(t, 'BEF_MAT')


def av_pp_at(t, timing):
    """Account value per policy

    :func:`av_at(t, timing)<av_at>` calculates
    the total amount of account value at time ``t`` for the policies in-force.

    At each ``t``, the events that change the account value balance
    occur in the following order:

        * Premium payment
        * Fee deduction

    Investment income is assumed to be earned throughout each month,
    so at the middle of the month when death and lapse occur,
    half the investment income for the month is credited.

    The second parameter ``timing`` takes a string to
    indicate the timing of the account value, which is either
    ``"BEF_PREM"``, ``"BEF_FEE"``, ``"BEF_INV"`` or ``"MID_MTH"``.


    .. rubric:: BEF_PREM

    Account value before premium payment.
    At the start of the projection (i.e. when ``t=0``),
    the account value is set to :func:`av_pp_init`.

    .. rubric:: BEF_FEE

    Account value after premium payment before fee deduction


    .. rubric:: BEF_INV

    Account value after fee deduction before crediting investemnt return

    .. rubric:: MID_MTH

    Account value at middle of month (``t+0.5``) when
    half the investment retun for the month is credited


    .. seealso::
        * :func:`av_pp_init`
        * :func:`inv_income_pp`
        * :func:`prem_to_av_pp`
        * :func:`maint_fee_pp`
        * :func:`coi_pp`
        * :func:`av_at`

    """
    if timing == "BEF_PREM":
        if t == 0:
            return av_pp_init()
        else:
            return av_pp_at(t-1, "BEF_INV") + inv_income_pp(t-1)

    elif timing == "BEF_FEE":
        return av_pp_at(t, "BEF_PREM") + prem_to_av_pp(t)

    elif timing == "BEF_INV":
        return av_pp_at(t, "BEF_FEE") - maint_fee_pp(t) - coi_pp(t)

    elif timing == "MID_MTH":
        return av_pp_at(t, "BEF_INV") + 0.5 * inv_income_pp(t)

    else:
        raise ValueError("invalid timing")


def av_pp_init():
    """Initial account value per policy

    For existing business at time ``0``,
    returns initial per-policy accout value read from
    the ``av_pp_init`` column in :func:`model_point`.
    For new business, 0 should be entered in the column.

    .. seealso::

        * :func:`model_point`
        * :func:`av_pp_at`

    """
    return model_point()["av_pp_init"]


def check_av_roll_fwd():
    """Check account value roll-forward

    Returns ``Ture`` if ``av_at(t+1, "BEF_NB")`` equates to
    the following expression for all ``t``, otherwise returns ``False``::

        av_at(t, "BEF_MAT")
              + prem_to_av(t)
              - maint_fee(t)
              - coi(t)
              + inv_income(t)
              - claims_from_av(t, "DEATH")
              - claims_from_av(t, "LAPSE")
              - claims_from_av(t, "MATURITY"))

    .. seealso::

        * :func:`av_at`
        * :func:`prem_to_av`
        * :func:`maint_fee`
        * :func:`coi`
        * :func:`inv_income`
        * :func:`claims_from_av`

    """
    for t in range(max_proj_len()):

        av = (av_at(t, "BEF_MAT")
              + prem_to_av(t)
              - maint_fee(t)
              - coi(t)
              + inv_income(t)
              - claims_from_av(t, "DEATH")
              - claims_from_av(t, "LAPSE")
              - claims_from_av(t, "MATURITY"))

        if np.all(np.isclose(av_at(t+1, "BEF_MAT"), av)):
            continue
        else:
            return False

    return True


def check_margin():
    """Check consistency between net cashflow and margins

    Returns ``True`` if :func:`net_cf` equates to the sum of
    :func:`margin_expense` and :func:`margin_mortality` for all ``t``,
    otherwise, returns ``False``.

    .. seealso::

        * :func:`net_cf`
        * :func:`margin_expense`
        * :func:`margin_mortality`

    """
    res = []
    for t in range(max_proj_len()):
        res.append(np.all(np.isclose(net_cf(t), margin_expense(t) + margin_mortality(t))))

    return all(res)


def check_pv_net_cf():
    """Check present value summation

    Check if the present value of :func:`net_cf` matches the
    sum of the present values of each cashflow.
    Returns the check result as :obj:`True` or :obj:`False`.

     .. seealso::

        * :func:`net_cf`
        * :func:`pv_net_cf`

    """
    cfs = np.array(list(net_cf(t) for t in range(max_proj_len()))).transpose()
    pvs = cfs @ disc_factors()[:max_proj_len()]

    return np.all(np.isclose(pvs, pv_net_cf()))


def claim_pp(t, kind):
    """Claim per policy

    The claim amount per policy. The second parameter
    is to indicate the type of the claim, and
    it takes a string, which is either ``"DEATH"``, ``"LAPSE"`` or ``"MATURITY"``.

    The death benefit as denoted by ``"DEATH"``, is
    the greater of :func:`sum_assured` and
    mid-month account value (:func:`av_pp_at(t, "MID_MTH")<av_pp_at>`).

    The surrender benefit as denoted by ``"LAPSE"`` and
    the maturity benefit as denoted by ``"MATURITY"`` are
    equal to the mid-month account value.

    .. seealso::

        * :func:`sum_assured`
        * :func:`av_pp_at`

    """

    if kind == "DEATH":
        return np.maximum(sum_assured(), av_pp_at(t, "MID_MTH"))

    elif kind == "LAPSE":
        return av_pp_at(t, "MID_MTH")

    elif kind == "MATURITY":
        return av_pp_at(t, "BEF_PREM")

    else:
        raise ValueError("invalid kind")


def claims(t, kind=None):
    """Claims

    The claim amount during the period from ``t`` to ``t+1``.
    The optional second parameter is for indicating the type of the claim, and
    it takes a string, which is either ``"DEATH"``, ``"LAPSE"`` or ``"MATURITY"``,
    or defaults to ``None`` to indicate the total of all the types of claims
    during the period.


    The death benefit as denoted by ``"DEATH"`` is defined as::

        claim_pp(t) * pols_death(t)

    The surrender benefit as denoted by ``"LAPSE"`` is defined as::

        claims_from_av(t, "LAPSE") - surr_charge(t)

    The maturity benefit as denoted by ``"MATURITY"`` is defined as::

        claims_from_av(t, "MATURITY")

    .. seealso::

        * :func:`claim_pp`
        * :func:`pols_death`
        * :func:`claims_from_av`
        * :func:`surr_charge`

    """

    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)

    elif kind == "LAPSE":
        return claims_from_av(t, "LAPSE") - surr_charge(t)

    elif kind == "MATURITY":
        return claim_pp(t, "MATURITY") * pols_maturity(t)

    elif kind is None:
        return sum(claims[t, k] for k in ["DEATH", "LAPSE", "MATURITY"])

    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):
    """Account value taken out to pay claim

    The part of the claim amount that is paid from account value.
    The second parameter takes a string indicating the type of the claim,
    which is either ``"DEATH"``, ``"LAPSE"`` or ``"MATURITY"``.


    Death benefit is denoted by ``"DEATH"``, is defined as::

        av_pp_at(t, "MID_MTH") * pols_death(t)

    When the account value is greater than the death benefit,
    the death benefit equates to the account value.

    Surrender benefit as denoted by ``"LAPSE"`` is defined as::

        av_pp_at(t, "MID_MTH") * pols_lapse(t)

    As the surrender benefit is defined as account value less surrender
    charge, when there is no surrender charge the surrender benefit
    equates to the account value.

    Maturity benefit as denoted by ``"MATURITY"`` is defined as::

        av_pp_at(t, "BEF_PREM") * pols_maturity(t)

    By default, the maturity benefit equates to the account value
    of maturing policies.

    .. seealso::

        * :func:`av_pp_at`
        * :func:`pols_death`
        * :func:`pols_lapse`
        * :func:`pols_maturity`

    """

    if kind == "DEATH":
        return av_pp_at(t, "MID_MTH") * pols_death(t)

    elif kind == "LAPSE":
        return av_pp_at(t, "MID_MTH") * pols_lapse(t)

    elif kind == "MATURITY":
        return av_pp_at(t, "BEF_PREM") * pols_maturity(t)

    else:
        raise ValueError("invalid kind")


def claims_over_av(t, kind):
    """Claim in excess of account value

    The amount of death benefits in excess of account value.
    :func:`coi` net of this amount represents mortality margin.

    .. seealso::

        * :func:`margin_mortality`
        * :func:`coi`

    """
    return claims(t, kind) - claims_from_av(t, kind)


def coi(t):
    """Cost of insurance charges

    The cost of insurance charges deducted from acccount values
    each period.

    .. seealso::

        * :func:`pols_if_at`
        * :func:`coi_pp`

    """
    return coi_pp(t) * pols_if_at(t, "BEF_DECR")


def coi_pp(t):
    """Cost of insurance charges per policy

    The cost of insurance charges per policy.
    Defined as the coi charge rate times net amount at risk per policy.

    .. seealso::

        * :func:`coi`
        * :func:`coi_rate`
        * :func:`net_amt_at_risk`

    """
    return coi_rate(t) * net_amt_at_risk(t)


def coi_rate(t):
    """Cost of insurance rate per account value

    The cost of insuranc rate per account value per month.
    By default, it is set to 1.1 times the monthly mortality rate.

    .. seealso::

        * :func:`mort_rate_mth`
        * :func:`coi_pp`
        * :func:`coi_rate`

    """
    return 1.1 * mort_rate_mth(t)


def commissions(t):
    """Commissions

    By default, 100% premiums for the first year, 0 otherwise.

    .. seealso::

        * :func:`premiums`
        * :func:`duration`

    """
    return 0.05 * premiums(t)


def disc_factors():
    """Discount factors.

    Vector of the discount factors as a Numpy array. Used for calculating
    the present values of cashflows.

    .. seealso::

        :func:`disc_rate_mth`
    """
    return np.array(list((1 + disc_rate_mth()[t])**(-t) for t in range(max_proj_len())))


def disc_rate_mth():
    """Monthly discount rate

    Nummpy array of monthly discount rates from time 0 to :func:`max_proj_len` - 1
    defined as::

        (1 + disc_rate_ann)**(1/12) - 1

    .. seealso::

        :func:`disc_rate_ann`

    """
    return np.array(list((1 + disc_rate_ann[t//12])**(1/12) - 1 for t in range(max_proj_len())))


def duration(t):
    """Duration of model points at ``t`` in years

    .. seealso:: :func:`duration_mth`

    """
    return duration_mth(t) //12


def duration_mth(t):
    """Duration of model points at ``t`` in months

    Indicates how many months the policies have been in-force at ``t``.
    The initial values at time 0 are read from the ``duration_mth`` column in
    :attr:`model_point_table` through :func:`model_point`.
    Increments by 1 as ``t`` increments.
    Negative values of :func:`duration_mth` indicate future new business
    policies. For example, If the :func:`duration_mth` is
    -15 at time 0, the model point is issued at ``t=15``.

    .. seealso:: :func:`model_point`

    """

    if t == 0:
        return model_point()['duration_mth']
    else:
        return duration_mth(t-1) + 1


def expense_acq():
    """Acquisition expense per policy

    ``5000`` by default.
    """
    return 5000


def expense_maint():
    """Annual maintenance expense per policy

    ``500`` by default.
    """
    return 500


def expenses(t):
    """Expenses

    Expenses during the period from ``t`` to ``t+1``
    defined as the sum of acquisition expenses and maintenance expenses.
    The acquisition expenses are modeled as :func:`expense_acq`
    times :func:`pols_new_biz`.
    The maintenance expenses are modeled as :func:`expense_maint`
    times :func:`inflation_factor` times :func:`pols_if_at` before
    decrement.

    .. seealso::

        * :func:`expense_acq`
        * :func:`expense_maint`
        * :func:`inflation_factor`
        * :func:`pols_new_biz`
        * :func:`pols_if_at`
    """

    return expense_acq() * pols_new_biz(t) \
        + pols_if_at(t, "BEF_DECR") * expense_maint()/12 * inflation_factor(t)


def has_surr_charge():
    """Whether surrender charge applies

    ``True`` if surrender charge on account value applies upon lapse,
    ``False`` if other wise.
    By default, the value is read from the ``has_surr_charge`` column
    in :func:`model_point`.

    .. seealso::

        * :func:`model_point`

    """
    return model_point()['has_surr_charge']


def inflation_factor(t):
    """The inflation factor at time t

    .. seealso::

        * :func:`inflation_rate`

    """
    return (1 + inflation_rate())**(t/12)


def inflation_rate():
    """Inflation rate

    The inflation rate to be applied to the expense assumption.
    By defualt it is set to ``0.01``.

    .. seealso::

        * :func:`inflation_factor`

    """
    return 0.01


def inv_income(t):
    """Investment income on account value

    Investment income earned on account value during each period.
    For the plicies decreased by lapse and death, half
    the investment income is credited.

    .. seealso::

        * :func:`inv_income_pp`
        * :func:`pols_if_at`
        * :func:`pols_death`
        * :func:`pols_lapse`

    """
    return (inv_income_pp(t) * pols_if_at(t+1, "BEF_MAT")
            + 0.5 * inv_income_pp(t) * (pols_death(t) + pols_lapse(t)))


def inv_income_pp(t):
    """Investment income on account value per policy

    Investment income on account value defined as::

        inv_return_mth(t) * av_pp_at(t, "BEF_INV")

    .. seealso::

        * :func:`inv_return_mth`
        * :func:`av_pp_at`

    """
    return inv_return_mth(t) * av_pp_at(t, "BEF_INV")


def inv_return_mth(t):
    """Rate of investment return

    Rate of monthly investment return for :attr:`scen_id` and ``t``
    read from :func:`inv_return_table`

    .. seealso::

        * :func:`inv_return_table`
        * :attr:`scen_id`

    """
    return inv_return_table()[scen_id, t]


def inv_return_table():
    r"""Table of investment return rates

    Returns a Series of monthly investment retuns.
    The Series is indexed with ``scen_id`` and ``t`` which
    is inherited from :attr:`std_norm_rand`.

    .. math::

        \exp\left(\left(\mu-\frac{\sigma^{2}}{2}\right)\Delta{t}+\sigma\sqrt{\Delta{t}}\epsilon\right)-1

    where :math:`\mu=2\%`, :math:`\sigma=3\%`, :math:`\Delta{t}=\frac{1}{12}`, and
    :math:`\epsilon` is a randome number from the standard normal distribution.

    .. seealso::

        * :attr:`std_norm_rand`
        * :attr:`scen_id`

    """
    mu = 0.02
    sigma = 0.03
    dt = 1/12

    return np.exp(
        (mu - 0.5 * sigma**2) * dt + sigma * dt**0.5 * std_norm_rand
        ) - 1


def is_wl():
    """Whether the model point is whole life

    ``True`` if the model point is whole life, ``False`` if other wise.
    By default, the value is read from the ``is_wl`` column
    in :func:`model_point`.
    This attribute is used to determin :func:`policy_term`.
    If ``True``, :func:`policy_term` is defined
    as :func:`mort_table_last_age` minus :func:`age_at_entry`.
    If ``False``, :func:`policy_term` is read from :func:`model_point`.


    .. seealso::

        * :func:`model_point`

    """
    return model_point()['is_wl']


def lapse_rate(t):
    """Lapse rate

    By default, the lapse rate assumption is defined by duration as::

        max(0.1 - 0.02 * duration(t), 0.02)

    .. seealso::

        :func:`duration`

    """
    return np.maximum(0.1 - 0.02 * duration(t), 0.02)


def load_prem_rate():
    """Rate of premium loading

    This rate times :func:`premium_pp` is collected from each premium
    and the rest is added to the account value.

    By default, the value is read from the ``load_prem_rate`` column
    in :func:`model_point`.

    .. seealso::

        * :func:`premium_pp`

    """
    return model_point()['load_prem_rate']


def maint_fee(t):
    """Maintenance fee deducted from account value

    .. seealso::

        * :func:`maint_fee_pp`

    """
    return maint_fee_pp(t) * pols_if_at(t, "BEF_DECR")


def maint_fee_pp(t):
    """Maintenance fee per policy

    .. seealso::

        * :func:`maint_fee_rate`
        * :func:`av_pp_at`

    """
    return maint_fee_rate() * av_pp_at(t, "BEF_FEE")


def maint_fee_rate():
    """Maintenance fee per account value

    The rate of maintenance fee on account value each month.
    Set to ``0.01 / 12`` by default.

    .. seealso::

        * :func:`maint_fee`

    """
    return 0.01 / 12


def margin_expense(t):
    """Expense margin

    Expense margin is defined as the sum of
    premium loading, surrender charge and maintenance fees
    net of commissions and expenses.

    The sum of the expense margin and mortality margin add
    up to the net cashflow.


    .. seealso::

        * :func:`load_prem_rate`
        * :func:`premium_pp`
        * :func:`pols_if_at`
        * :func:`surr_charge`
        * :func:`maint_fee`
        * :func:`commissions`
        * :func:`expenses`
        * :func:`check_margin`

    """
    return (load_prem_rate()* premium_pp(t) * pols_if_at(t, "BEF_DECR")
            + surr_charge(t)
            + maint_fee(t)
            - commissions(t)
            - expenses(t))


def margin_mortality(t):
    """Mortality margin

    Mortality margin is defined :func:`coi` net of :func:`claims_over_av`.

    The sum of the expense margin and mortality margin add
    up to the net cashflow.

    .. seealso::

        * :func:`coi`
        * :func:`claims_over_av`

    """
    return coi(t) - claims_over_av(t, 'DEATH')


max_proj_len = lambda: max(proj_len())
"""The max of all projection lengths

Defined as ``max(proj_len())``

.. seealso::
    :func:`proj_len`
"""

def model_point():
    """Target model points

    Returns as a DataFrame the model points to be in the scope of calculation.
    By default, this Cells returns the entire :func:`model_point_table_ext`
    without change.
    :func:`model_point_table_ext` is the extended model point table,
    which extends :attr:`model_point_table` by joining the columns
    in :attr:`product_spec_table`. Do not directly refer to
    :attr:`model_point_table` in this formula.
    To select model points, change this formula so that this
    Cells returns a DataFrame that contains only the selected model points.

    Examples:
        To select only the model point 1::

            def model_point():
                return model_point_table_ext().loc[1:1]

        To select model points whose ages at entry are 40 or greater::

            def model_point():
                return model_point_table[model_point_table_ext()["age_at_entry"] >= 40]

    Note that the shape of the returned DataFrame must be the
    same as the original DataFrame, i.e. :func:`model_point_table_ext`.

    When selecting only one model point, make sure the
    returned object is a DataFrame, not a Series, as seen in the example
    above where ``model_point_table_ext().loc[1:1]`` is specified
    instead of ``model_point_table_ext().loc[1]``.

    Be careful not to accidentally change the original table
    held in :func:`model_point_table_ext`.

    .. seealso::

        * :func:`model_point_table_ext`

    """
    return model_point_table_ext()


def model_point_table_ext():
    """Extended model point table

    Returns an extended :attr:`model_point_table` by joining
    :attr:`product_spec_table` on the ``spec_id`` column.

    .. seealso::

        * :attr:`model_point_table`
        * :attr:`product_spec_table`


    """
    return model_point_table.join(product_spec_table, on='spec_id')


def mort_rate(t):
    """Mortality rate to be applied at time t

    Returns a Series of the mortality rates to be applied at time t.
    The index of the Series is ``point_id``,
    copied from :func:`model_point`.

    .. seealso::

       * :func:`mort_table_reindexed`
       * :func:`mort_rate_mth`
       * :func:`model_point`

    """

    # mi is a MultiIndex whose values are
    # pairs of age at t and duration at t capped at 5 for all the model points.

    # ``mort_table_reindexed().reindex(mi, fill_value=0)`` returns
    # a Series of mortality rates whose indexes match the MultiIndex values.
    # The ``set_axis`` method replace the MultiIndex with ``point_id``

    mi = pd.MultiIndex.from_arrays([age(t), np.minimum(duration(t), 5)])
    return mort_table_reindexed().reindex(
        mi, fill_value=0).set_axis(model_point().index, inplace=False)


def mort_rate_mth(t):
    """Monthly mortality rate to be applied at time t

    .. seealso::

       * :attr:`mort_table`
       * :func:`mort_rate`

    """
    return 1-(1- mort_rate(t))**(1/12)


def mort_table_last_age():
    """The last age of mortality tables

    Returns the last age whose mortality rates are all 1.
    If no such age is found, return the last index of the tables

    .. seealso::

        * :attr:`mort_table`

    """
    for i in mort_table.index:
        mort_i = mort_table.loc[i]
        if (mort_i == 1).all():
            return i

    return i


def mort_table_reindexed():
    """MultiIndexed mortality table

    Returns a Series of mortlity rates reshaped from :attr:`mort_table`.
    The returned Series is indexed by age and duration capped at 5.

    """
    result = []
    for col in mort_table.columns:
        df = mort_table[[col]]
        df = df.assign(Duration=int(col)).set_index('Duration', append=True)[col]
        result.append(df)

    return pd.concat(result)


def net_amt_at_risk(t):
    """Net amount at risk per policy

    Return sum assured net of account value per policy.

    .. seealso::

        * :func:`sum_assured`
        * :func:`av_pp_at`


    """
    return np.maximum(sum_assured() - av_pp_at(t, 'BEF_FEE'), 0)


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
    return (premiums(t)
            + inv_income(t) - claims(t) - expenses(t) - commissions(t) - av_change(t))


def policy_term():
    """The policy term of the model points.

    The ``policy_term`` column of the DataFrame returned by
    :func:`model_point`.
    """

    return (is_wl() * (mort_table_last_age() - age_at_entry()) 
            + (is_wl() == False) * model_point()["policy_term"])


def pols_death(t):
    """Number of death

    Number of policies decreased by death between ``t`` and ``t+1``
    """
    return pols_if_at(t, "BEF_DECR") * mort_rate_mth(t)


def pols_if(t):
    """Number of policies in-force

    :func:`pols_if(t)<pols_if>` is an alias
    for :func:`pols_if_at(t, "BEF_MAT")<pols_if_at>`.

    .. seealso::
        * :func:`pols_if_at`

    """
    return pols_if_at(t, "BEF_MAT")


def pols_if_at(t, timing):
    """Number of policies in-force

    :func:`pols_if_at(t, timing)<pols_if_at>` calculates
    the number of policies in-force at time ``t``.
    The second parameter ``timing`` takes a string value to
    indicate the timing of in-force,
    which is either
    ``"BEF_MAT"``, ``"BEF_NB"`` or ``"BEF_DECR"``.

    .. rubric:: BEF_MAT

    The number of policies in-force before maturity after lapse and death.
    At time 0, the value is read from :func:`pols_if_init`.
    For time > 0, defined as::

        pols_if_at(t-1, "BEF_DECR") - pols_lapse(t-1) - pols_death(t-1)

    .. rubric:: BEF_NB

    The number of policies in-force before new business after maturity.
    Defined as::

        pols_if_at(t, "BEF_MAT") - pols_maturity(t)

    .. rubric:: BEF_DECR

    The number of policies in-force before lapse and death after new business.
    Defined as::

        pols_if_at(t, "BEF_NB") + pols_new_biz(t)

    .. seealso::
        * :func:`pols_if_init`
        * :func:`pols_lapse`
        * :func:`pols_death`
        * :func:`pols_maturity`
        * :func:`pols_new_biz`
        * :func:`pols_if`

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


def pols_if_init():
    """Initial number of policies in-force

    Number of in-force policies at time 0 referenced from
    :func:`pols_if_at(0, "BEF_MAT")<pols_if_at>`.
    """
    return model_point()["policy_count"].where(duration_mth(0) > 0, other=0)


def pols_lapse(t):
    """Number of lapse

    Number of policies decreased by lapse during ``t`` and ``t+1``.

    .. seealso::
        * :func:`pols_if_at`
        * :func:`lapse_rate`

    """
    return (pols_if_at(t, "BEF_DECR") - pols_death(t)) * (1-(1 - lapse_rate(t))**(1/12))


def pols_maturity(t):
    """Number of maturing policies

    The policy maturity occurs when
    :func:`duration_mth` equals 12 times :func:`policy_term`.
    The amount is equal to :func:`pols_if_at(t, "BEF_MAT")<pols_if_at>`.

    otherwise ``0``.
    """
    return (duration_mth(t) == policy_term() * 12) * pols_if_at(t, "BEF_MAT")


def pols_new_biz(t):
    """Number of new business policies

    The number of new business policies.
    The value :func:`duration_mth(0)<duration_mth>`
    for the selected model point is read from the ``policy_count`` column in
    :func:`model_point`. If the value is 0 or negative,
    the model point is new business at t=0 or at t when
    :func:`duration_mth(t)<duration_mth>` is 0, and the
    :func:`pols_new_biz(t)<pols_new_biz>` is read from the ``policy_count``
    in :func:`model_point`.

    .. seealso::
        * :func:`model_point`

    """
    return model_point()['policy_count'].where(duration_mth(t) == 0, other=0)


def prem_to_av(t):
    """Premium portion put in account value

    The amount of premiums net of loadings, which is put in the accoutn value.

    .. seealso::

        * :func:`load_prem_rate`
        * :func:`premium_pp`
        * :func:`pols_if_at`

    """
    return  prem_to_av_pp(t) * pols_if_at(t, "BEF_DECR")


def prem_to_av_pp(t):
    """Per-policy premium portion put in the account value

    The amount of premium per policy net of loading,
    which is put in the accoutn value.

    .. seealso::

        * :func:`load_prem_rate`
        * :func:`premium_pp`
        * :func:`pols_if_at`

    """
    return (1 - load_prem_rate()) * premium_pp(t)


def premium_pp(t):
    """Premium amount per policy

    Single premium amount if :func:`premium_type` is ``"SINGLE"``,
    monthly premium amount if :func:`premium_type` is ``"LEVEL"``.

    .. seealso::

        * :func:`premium_type`
        * :func:`sum_assured`
        * :func:`age_at_entry`
        * :func:`policy_term`

    """
    # mi is a MultiIndex whose values are
    # pairs of issue ages and policy terms for all the model points.

    # ``premium_table.reindex(mi)`` returns
    # a Series of premium rates whose indexes match the MultiIndex values.
    # The ``set_axis`` method replace the MultiIndex with ``point_id``

    # mi = pd.MultiIndex.from_arrays([age_at_entry(), policy_term()])
    # prem_rates = premium_table.reindex(mi).set_axis(
    #     model_point().index, inplace=False)
    # return np.around(sum_assured() * prem_rates, 2)

    sp = model_point()['premium_pp'].where((premium_type() == 'SINGLE') & (duration_mth(t) == 0), other=0)
    lp = model_point()['premium_pp'].where(
        (premium_type() == 'LEVEL') & (duration_mth(t) < 12 * policy_term()),
        other=0)
    return sp + lp


def premium_type():
    """Type of premium payment

    Returns a string indicating the payment type, which is either
    ``"LEVEL"`` if level payment, or ``"SINGLE"`` if single payment.

    """
    return model_point()['premium_type']


def premiums(t):
    """Premium income

    Premium income during the period from ``t`` to ``t+1`` defined as::

        premium_pp() * pols_if_at(t, "BEF_DECR")

    .. seealso::

        * :func:`premium_pp`
        * :func:`pols_if_at`

    """
    return premium_pp(t) * pols_if_at(t, "BEF_DECR")


def proj_len():
    """Projection length in months

    :func:`proj_len` returns how many months the projection
    for each model point should be carried out
    for all the model point. Defined as::

        np.maximum(12 * policy_term() - duration_mth(0) + 1, 0)

    Since this model carries out projections for all the model points
    simultaneously, the projections are actually carried out
    from 0 to :attr:`max_proj_len` for all the model points.

    .. seealso::

        * :func:`policy_term`
        * :func:`duration_mth`
        * :attr:`max_proj_len`

    """
    return np.maximum(12 * policy_term() - duration_mth(0) + 1, 0)


def pv_av_change():
    """Present value of change in account value

    .. seealso::

        * :func:`av_change`
        * :func:`disc_factors`
        * :func:`proj_len`

    """
    result = np.array(list(av_change(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_claims(kind=None):
    """Present value of claims

    See :func:`claims` for the parameter ``kind``.

    .. seealso::

        * :func:`claims`
        * :func:`proj_len`
        * :func:`disc_factors`


    """
    cl = np.array(list(claims(t, kind) for t in range(max_proj_len()))).transpose()

    return cl @ disc_factors()[:max_proj_len()]


def pv_commissions():
    """Present value of commissions

    .. seealso::

        * :func:`expenses`
        * :func:`proj_len`
        * :func:`disc_factors`

    """
    result = np.array(list(commissions(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_expenses():
    """Present value of expenses

    .. seealso::

        * :func:`expenses`
        * :func:`proj_len`
        * :func:`disc_factors`

    """
    result = np.array(list(expenses(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_inv_income():
    """Present value of investment income

    The discounted sum of monthly investment income.

    .. seealso::

        * :func:`inv_income`
        * :func:`proj_len`
        * :func:`disc_factors`

    """
    result = np.array(list(inv_income(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_net_cf():
    """Present value of net cashflows.

    Defined as::

        pv_premiums() + pv_inv_income()
        - pv_claims() - pv_expenses() - pv_commissions() - pv_av_change()

    .. seealso::

        * :func:`pv_premiums`
        * :func:`pv_claims`
        * :func:`pv_expenses`
        * :func:`pv_commissions`

    """
    return (pv_premiums() 
            + pv_inv_income() 
            - pv_claims() 
            - pv_expenses() 
            - pv_commissions() 
            - pv_av_change())


def pv_pols_if():
    """Present value of policies in-force

    .. note::
       This cells is not used by default.

    The discounted sum of the number of in-force policies at each month.
    It is used as the annuity factor for calculating :func:`net_premium_pp`.

    """
    result = np.array(list(pols_if_at(t, "BEF_DECR") for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_premiums():
    """Present value of premiums

    .. seealso::

        * :func:`premiums`
        * :func:`proj_len`
        * :func:`disc_factors`

    """
    result = np.array(list(premiums(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


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


def result_pols():
    """Result table of policy decrement

    .. seealso::

       * :func:`pols_if`
       * :func:`pols_maturity`
       * :func:`pols_new_biz`
       * :func:`pols_death`
       * :func:`pols_lapse`

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
            "Premiums": pv_premiums(), 
            "Death": pv_claims("DEATH"),
            "Surrender": pv_claims("LAPSE"),
            "Maturity": pv_claims("MATURITY"),
            "Expenses": pv_expenses(), 
            "Commissions": pv_commissions(), 
            "Investment Income": pv_inv_income(),
            "Change in AV": pv_av_change(),
            "Net Cashflow": pv_net_cf()
        }

    return pd.DataFrame(data, index=model_point().index)


def sex():
    """The sex of the model points

    .. note::
       This cells is not used by default.

    The ``sex`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()["sex"]


def sum_assured():
    """The sum assured of the model points

    The ``sum_assured`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()['sum_assured']


def surr_charge(t):
    """Surrender charge

    Surrender charge rate times account values of lapsed policies

    .. seealso::

        * :func:`surr_charge_rate`
        * :func:`av_pp_at`
        * :func:`pols_lapse`
        * :func:`proj_len`
        * :func:`disc_factors`

    """
    return surr_charge_rate(t) * av_pp_at(t, "MID_MTH") * pols_lapse(t)


def surr_charge_id():
    """ID of surrender charge pattern

    A string to indicate the ID of the surrender charge pattern.
    The ID should be one of the column names in :attr:`surr_charge_table`
    if :func:`has_surr_charge` is ``True``.

    .. seealso::

        * :attr:`surr_charge_table`
        * :func:`has_surr_charge`

    """
    return model_point()['surr_charge_id']


def surr_charge_max_idx():
    """maximum index of surrender charge table

    The maximum index(duration) of :attr:`surr_charge_table`.

    .. seealso::

        * :attr:`surr_charge_rate`
        * :func:`has_surr_charge`

    """
    return max(surr_charge_table.index)


def surr_charge_rate(t):
    """Surrender charge rate

    Surrender charge rate to be applied for lapsed policies

    .. seealso::

        * :func:`surr_charge_rate`
        * :func:`av_pp_at`
        * :func:`pols_lapse`
        * :func:`proj_len`
        * :func:`disc_factors`
        * :func:`surr_charge_max_idx`
        * :func:`surr_charge_table_stacked`
    """
    idx = pd.MultiIndex.from_arrays(
        [has_surr_charge() * surr_charge_id(),
         np.minimum(duration(t), surr_charge_max_idx())])

    return surr_charge_table_stacked().reindex(idx, fill_value=0).set_axis(
        model_point().index, inplace=False)


def surr_charge_table_stacked():
    """Stacked surrender charge table

    :attr:`surr_charge_table` converted to a Series indexed
    with surrender charge ID and duration.

    .. seealso::

        * :attr:`surr_charge_table`
        * :func:`surr_charge_rate`

    """
    return surr_charge_table.stack().reorder_levels([1, 0]).sort_index()


# ---------------------------------------------------------------------------
# References

disc_rate_ann = ("DataClient", 1882832352832)

mort_table = ("DataClient", 1882837214640)

np = ("Module", "numpy")

pd = ("Module", "pandas")

std_norm_rand = ("DataClient", 1882832427664)

surr_charge_table = ("DataClient", 1882832427424)

product_spec_table = ("DataClient", 1882837029552)

model_point_samples = ("DataClient", 1882838121440)

scen_id = 1

model_point_10000 = ("DataClient", 1882837472592)

model_point_table = ("DataClient", 1882838121440)