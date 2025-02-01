"""
The :mod:`~basiclife.BasicTerm_SC.Projection` space includes
projection logic for individual model points.

:mod:`~basiclife.BasicTerm_SC.Projection` is derived from
:mod:`basiclife.BasicTerm_S.Projection`
by applying changes
to make its compiled model run faster.

Policy attributes and other input data are read from
:mod:`~basiclife.BasicTerm_SC.Data`, which is referenced as
:attr:`data` in :mod:`~basiclife.BasicTerm_SC.Projection`.

In :mod:`~basiclife.BasicTerm_SC.Data`,
policy attributes, such as :func:`~basiclife.BasicTerm_SC.Data.policy_term`,
are returned as 1-dimensional numpy arrays.
Consequently, :mod:`~basiclife.BasicTerm_SC.Projection` is parameterized with
:attr:`idx`, which represents the array index to identify model points.


.. rubric:: Parameters and References

(In all the sample code below,
the global variable `BasicTerm_SC` refers to the
:mod:`~basiclife.BasicTerm_SC` model.)

Attributes:

    idx: Array index to identify a model point.
        Policy attributes, such as :func:`~basiclife.BasicTerm_SC.Data.policy_term`,
        are returned as 1-dimensional numpy arrays
        in :mod:`~basiclife.BasicTerm_SC.Data`.
        ``idx`` is defined as a Reference, and its value
        is used for determining the selected model point.
        By default, ``0`` is assigned. To select another model point,
        assign its array index to it::

            >>> BasicTerm_SC.Projection.idx = 2

        ``idx`` is also defined as the parameter of the
        :mod:`~basiclife.BasicTerm_SC.Projection` Space,
        which makes it possible to create dynamic child space
        for multiple model points::

            >>> BasicTerm_SC.Projection.parameters
            ('idx',)

            >>> BasicTerm_SC.Projection[1]
            <ItemSpace BasicTerm_SC.Projection[1]>

            >>> BasicTerm_SC.Projection[2]
            <ItemSpace BasicTerm_SC.Projection[2]>

    data: The :mod:`~basiclife.BasicTerm_SC.Data` space.
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

_formula = lambda idx: None

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
    """The age at entry of the selected model point

    The element of :func:`basiclife.BasicTerm_SC.Data.age_at_entry`
    at index :attr:`idx`.
    """
    return data.age_at_entry()[idx]


def check_pv_net_cf():
    """Check present value summation

    Check if the present value of :func:`net_cf` matches the
    sum of the present values each cashflows.
    Returns the check result as :obj:`True` or :obj:`False`.

     .. seealso::

        * :func:`net_cf`
        * :func:`pv_net_cf`

    """
    import math

    pv: float = 0

    for t in range(proj_len()):
        pv += net_cf(t) * disc_factor(t)


    return math.isclose(pv, pv_net_cf())


def claim_pp(t):
    """Claim per policy

    The claim amount per plicy. Defaults to :func:`sum_assured`.
    """
    return sum_assured()


def claims(t):
    """Claims

    Claims during the period from ``t`` to ``t+1`` defined as::

        claim_pp(t) * pols_death(t)

    .. seealso::

        * :func:`claim_pp`
        * :func:`pols_death`

    """
    return claim_pp(t) * pols_death(t)


def commissions(t): 
    """Commissions

    By default, 100% premiums for the first year, 0 otherwise.

    .. seealso::

        * :func:`premiums`
        * :func:`duration`

    """
    return premiums(t) if duration(t) == 0 else 0


def disc_factor(t):
    """Discount factor at time ``t``.

    Defined as the inverse of ``(1 + disc_rate_mth(t))`` to the ``t``-th power.

    .. seealso::

        :func:`disc_rate_mth`
    """
    return (1 + disc_rate_mth(t))**(-t)


def disc_rate_mth(t):
    """Monthly discount rate

    Nummpy array of monthly discount rates from time 0 to :func:`proj_len` - 1
    defined as::

        (1 + disc_rate_ann)**(1/12) - 1

    .. seealso::

        :func:`~basiclife.BasicTerm_SC.Data.disc_rate_ann_array`

    """
    return (1 + data.disc_rate_ann_array()[t//12])**(1/12) - 1


def duration(t):
    """Duration in force in years"""
    return t//12


def expense_acq():
    """Acquisition expense per policy

    ``300`` by default.
    """
    return 300


def expense_maint():
    """Annual maintenance expense per policy

    ``60`` by default.
    """
    return 60


def expenses(t):
    """Acquisition and maintenance expenses

    Expense cashflow during the period from ``t`` to ``t+1``.
    For any ``t``, the maintenance expense is recognized,
    which is defined as::

        pols_if(t) * expense_maint()/12 * inflation_factor(t)

    At ``t=0`` only, the acquisition expense,
    defined as :func:`expense_acq`, is recognized.

    .. seealso::

        * :func:`pols_if`
        * :func:`expense_maint`
        * :func:`inflation_factor`

    .. versionchanged:: 0.2.0
       The maintenance expense is also recognized for ``t=0``.

    """
    maint = pols_if(t) * expense_maint()/12 * inflation_factor(t)

    if t == 0:
        return expense_acq() + maint
    else:
        return maint


def inflation_factor(t):
    """The inflation factor at time t

    .. seealso::

        * :func:`inflation_rate`

    """
    return (1 + inflation_rate())**(t/12)


def inflation_rate():
    """Inflation rate"""
    return 0.01


def lapse_rate(t):
    """Lapse rate

    By default, the lapse rate assumption is defined by duration as::

        max(0.1 - 0.02 * duration(t), 0.02)

    .. seealso::

        :func:`duration`

    """
    return max(0.1 - 0.02 * duration(t), 0.02)


def loading_prem():
    """Loading per premium

    ``0.5`` by default.

    .. seealso::

        * :func:`premium_pp`

    """
    return 0.50


def mort_rate(t):
    """Mortality rate to be applied at time t

    .. seealso::

       * :func:`~basiclife.BasicTerm_SC.Data.mort_table_array`

    """
    return data.mort_table_array()[age(t), max(min(5, duration(t)),0)]


def mort_rate_mth(t):
    """Monthly mortality rate to be applied at time t

    .. seealso::

       * :func:`mort_rate`

    """
    return 1-(1- mort_rate(t))**(1/12)


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
    return pv_claims() / pv_pols_if()


def policy_term():
    """The policy term of the selected model point.

    The element of :func:`~basiclife.BasicTerm_SC.Data.policy_term`
    at index :attr:`idx`.
    """
    return data.policy_term()[idx]


def pols_death(t):
    """Number of death occurring at time t"""
    return pols_if(t) * mort_rate_mth(t)


def pols_if(t):
    """Number of policies in-force

    Number of in-force policies calculated recursively.
    The initial value is read from :func:`pols_if_init`.
    Subsequent values are defined recursively as::

        pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1) - pols_maturity(t)

    .. seealso::
        * :func:`pols_lapse`
        * :func:`pols_death`
        * :func:`pols_maturity`

    """
    if t==0:
        return pols_if_init()
    elif t > policy_term() * 12:
        return 0
    else:
        return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1) - pols_maturity(t)


def pols_if_init(): 
    """Initial Number of Policies In-force

    Number of in-force policies at time 0 referenced from :func:`pols_if`.
    Defaults to 1.
    """
    return 1


def pols_lapse(t):
    """Number of lapse occurring at time t

    .. seealso::
        * :func:`pols_if`
        * :func:`lapse_rate`

    """
    return (pols_if(t) - pols_death(t)) * (1-(1 - lapse_rate(t))**(1/12))


def pols_maturity(t):
    """Number of maturing policies

    The policy maturity occurs at ``t == 12 * policy_term()``,
    after death and lapse during the last period::

        pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)

    otherwise ``0``.
    """
    if t == policy_term() * 12:
        return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)
    else:
        return 0


def premium_pp():
    """Monthly premium per policy

    Monthly premium amount per policy defined as::

        round((1 + loading_prem()) * net_premium(), 2)

    .. versionchanged:: 0.2.0
       The ``t`` parameter is removed.

    .. seealso::

        * :func:`loading_prem`
        * :func:`net_premium_pp`

    """
    return round((1 + loading_prem()) * net_premium_pp(), 2)


def premiums(t):
    """Premium income

    Premium income during the period from ``t`` to ``t+1`` defined as::

        premium_pp(t) * pols_if(t)

    .. seealso::

        * :func:`premium_pp`
        * :func:`pols_if`

    """
    return premium_pp() * pols_if(t)


def proj_len():
    """Projection length in months

    Projection length in months defined as::

        12 * policy_term() + 1

    .. seealso::

        :func:`policy_term`

    """
    return 12 * policy_term() + 1


def pv_claims():
    """Present value of claims

    .. seealso::

        * :func:`claims`

    """
    pv = 0.0

    for t in range(proj_len()):
        pv += claims(t) * disc_factor(t)

    return pv


def pv_commissions():
    """Present value of commissions

    .. seealso::

        * :func:`expenses`

    """
    pv = 0.0

    for t in range(proj_len()):
        pv += commissions(t) * disc_factor(t)

    return pv


def pv_expenses():
    """Present value of expenses

    .. seealso::

        * :func:`expenses`

    """
    pv = 0.0

    for t in range(proj_len()):
        pv += expenses(t) * disc_factor(t)

    return pv


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


def pv_pols_if():
    """Present value of policies in-force

    The discounted sum of the number of in-force policies at each month.
    It is used as the annuity factor for calculating :func:`net_premium_pp`.

    """
    pv = 0.0

    for t in range(proj_len()):
        pv += pols_if(t) * disc_factor(t)

    return pv


def pv_premiums():
    """Present value of premiums

    .. seealso::

        * :func:`premiums`

    """
    pv = 0.0

    for t in range(proj_len()):
        pv += premiums(t) * disc_factor(t)

    return pv


def result_cf():
    """Result table of cashflows

    .. seealso::

       * :func:`premiums`
       * :func:`claims`
       * :func:`expenses`
       * :func:`commissions`
       * :func:`net_cf`

    """

    t_len = range(proj_len())

    data = {
        "Premiums": [premiums(t) for t in t_len],
        "Claims": [claims(t) for t in t_len],
        "Expenses": [expenses(t) for t in t_len],
        "Commissions": [commissions(t) for t in t_len],
        "Net Cashflow": [net_cf(t) for t in t_len]
    }
    return pd.DataFrame.from_dict(data)


def result_pv():
    """Result table of present value of cashflows

    .. seealso::

       * :func:`pv_premiums`
       * :func:`pv_claims`
       * :func:`pv_expenses`
       * :func:`pv_commissions`
       * :func:`pv_net_cf`

    """

    cols = ["Premiums", "Claims", "Expenses", "Commissions", "Net Cashflow"]
    pvs = [pv_premiums(), pv_claims(), pv_expenses(), pv_commissions(), pv_net_cf()]
    per_prem = [x / pv_premiums() for x in pvs]

    return pd.DataFrame.from_dict(
            data={"PV": pvs, "% Premium": per_prem},
            columns=cols,
            orient='index')


def sex(): 
    """The sex of the selected model point

    .. note::
       This cells is not used by default.

    The element of :func:`~basiclife.BasicTerm_SC.Data.sex`
    at index :attr:`idx`.
    """
    return data.sex()[idx]


def sum_assured():
    """The sum assured of the selected model point

    The element of :func:`~basiclife.BasicTerm_SC.Data.sum_assured`
    at index :attr:`idx`.
    """
    return data.sum_assured()[idx]


# ---------------------------------------------------------------------------
# References

pd = ("Module", "pandas")

np = ("Module", "numpy")

data = ("Interface", ("..", "Data"), "auto")

idx = 0