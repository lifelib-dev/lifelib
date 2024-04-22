.. module:: basiclife.BasicTermASL_ME

The **BasicTermASL_ME** Model
==============================

.. py:currentmodule:: basiclife.BasicTermASL_ME

Overview
-----------

The :mod:`~basiclife.BasicTermASL_ME`
is an adjustable step length(ASL) model, and projects the cashflows of
in-force policies at time 0 and future new business
policies issued after time 0.
As is the case with :mod:`~basiclife.BasicTerm_ME`,
time-dependent cells in :mod:`~basiclife.BasicTermASL_ME` carry out
calculations for all model points, and returns values for all the model points
as pandas Series or numpy array objects.

Unlike :mod:`~basiclife.BasicTerm_ME`, with :mod:`~basiclife.BasicTermASL_ME`
the user can specify the length of each projection step,
from 1 month to 1 year. By default, the first 60 steps are monthly
projections, while steps after that are annual.
This model reads issue date information from model point input,
and handles policy anniversaries precisely.

Space Inheritance
------------------

:mod:`~basiclife.BasicTermASL_ME` has 3 spaces, namely
:mod:`~basiclife.BasicTermASL_ME.Base`,
:mod:`~basiclife.BasicTermASL_ME.Projection`
and :mod:`~basiclife.BasicTermASL_ME.Pricing`.
:mod:`~basiclife.BasicTermASL_ME.Base` is the base space
of :mod:`~basiclife.BasicTermASL_ME.Projection` and
and :mod:`~basiclife.BasicTermASL_ME.Pricing`, and
most Cells and References are defined in
:mod:`~basiclife.BasicTermASL_ME.Base`.
:mod:`~basiclife.BasicTermASL_ME.Pricing` is for calculating premiums.
In :mod:`~basiclife.BasicTermASL_ME.Pricing`,
the issue dates of all model points are set to the projection start date
in :func:`~basiclife.BasicTermASL_ME.Pricing.model_point`.
:func:`~basiclife.BasicTermASL_ME.Pricing.premium_pp` calculates
premiums per 1000 sum assured per payment from
:func:`~basiclife.BasicTermASL_ME.Base.loading_prem` and
the present values of claims over present value of polices in-force for premium payments.
:func:`Pricing.premium_pp` is brought in to :mod:`~basiclife.BasicTermASL_ME.Projection`
as :attr:`~Projection.pricing_premium_pp` and
referenced by :func:`Projection.premium_pp`.

.. figure:: /images/libraries/basiclife/BasicTermASL_ME/diagram1.png


Projection Steps
----------------

Projection steps are indexed with ``i``.
Step ``i`` starts from one day after :func:`date_(i)<Base.date_>`
and ends on :func:`date_(i+1)<Base.date_>`.
:func:`date_(0)<Base.date_>` is the projection start date.
The start date is specified by a date string assigned to :attr:`~Base.date_init`.
:func:`date_(i)<Base.date_>` returns a `Timestamp`_ object.
The length of each projection step can be specified by
:func:`~Base.offset` cells. :func:`offset(i)<Base.offset>` should return
the length of step ``i`` as a pandas `DateOffset`_ object,
so that the object can be added to
the `Timestamp`_ values of :func:`date_(i)<Base.date_>`.
:func:`date_(i)<Base.date_>` should always be an end-of-month date,
so :func:`offset(i)<Base.offset>` should return `DateOffset`_ objects
such that :func:`date_(i)<Base.date_>` are always end-of-month dates.
`YearEnd`_ and `MonthEnd`_ objects are good examples.
By default, '2021-12-31' is set to :attr:`~Base.date_init`,
and the first 60 steps are monthly and steps after that are annual.

.. code-block::

    >>> BasicTermASL_ME.Base.date_(0)
    Timestamp('2021-12-31 00:00:00')

    >>> BasicTermASL_ME.Base.date_(60)
    Timestamp('2026-12-31 00:00:00')

    >>> BasicTermASL_ME.Base.date_(61)
    Timestamp('2027-12-31 00:00:00')

    >>> BasicTermASL_ME.Base.offset(0)
    <MonthEnd>

    >>> BasicTermASL_ME.Base.offset(60)
    <YearEnd: month=12>



.. _DateOffset: https://pandas.pydata.org/docs/reference/offset_frequency.html
.. _Timestamp: https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html
.. _YearEnd: https://pandas.pydata.org/docs/reference/api/pandas.tseries.offsets.YearEnd.html
.. _MonthEnd: https://pandas.pydata.org/docs/reference/api/pandas.tseries.offsets.MonthEnd.html


Policy Anniversary
--------------------

.. py:currentmodule:: basiclife.BasicTermASL_ME.Base

When a policy's anniversary date is in a projection step,
some cells, such as :func:`pols_lapse` and :func:`premiums` calculate their values by separately
calculating the parts before and after the anniversary and then adding them up.
For example, the formula of :func:`pols_lapse` looks like below:

.. code-block::

    def pols_lapse(i, j=None):

        if j is None:
            return pols_lapse(i, 'LAST') + pols_lapse(i, 'NEXT')

        elif j == 'LAST':
            lapse = 1 - (1 - lapse_rate(i))**(last_part(i) / 12)
            return (pols_if_at(i, "BEG_STEP") - pols_death(i, 'LAST')) * lapse

        elif j == 'NEXT':
            lapse = 1 - (1 - lapse_rate(i+1))**(next_part(i) / 12)
            return (pols_if_at(i, "AFT_NB") - pols_death(i, 'NEXT')) * lapse

        else:
            raise ValueError('invalid j')

When the second parameter ``j`` is not given,
:func:`pols_lapse(i)<pols_lapse>` adds :func:`pols_lapse(i, 'LAST')<pols_lapse>`
and :func:`pols_lapse(i, 'NEXT')<pols_lapse>`
and returns the their sum.
:func:`pols_lapse(i, 'LAST')<pols_lapse>` returns
the number of lapsed policies before the
policy anniversary in Step ``i``.
:func:`pols_lapse(i, 'NEXT')<pols_lapse>` returns
the number of lapsed policies during Step ``i`` after the
policy anniversary in Step ``i``.
If the length of Step ``i`` is shorter than a full year,
then there may not be an anniversary date in Step ``i``, in which
case :func:`pols_lapse(i, 'LAST')<pols_lapse>` should
be the entire :func:`pols_lapse(i)<pols_lapse>` and
:func:`pols_lapse(i, 'NEXT')<pols_lapse>` should be zero.

The figure below illustrates adjacent policy terms
and the policy anniversary between them occurring during Step ``i``.
:func:`next_anniversary(i)<next_anniversary>` returns
the first anniversary date after :func:`date_(i)<date_>`
for all model points as a Series of `Timestamp`_ objects.
:func:`months_in_step(i)<months_in_step>` returns the number of
months in Step ``i`` as an integer.

:func:`last_part(i)<last_part>` returns the length of time
from :func:`date_(i)<date_>` to :func:`next_anniversary(i)<next_anniversary>`  in months.
:func:`next_part(i)<next_part>` returns the length of time
from :func:`next_anniversary(i)<next_anniversary>` to :func:`date_(i+1)<date_>` in months.
The fractional portions of :func:`last_part(i)<last_part>`
and :func:`next_part(i)<next_part>` represent residual days.

.. figure:: /images/libraries/basiclife/policy_anniversary.png

Model Specifications
---------------------

The :mod:`~.Base` space
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:currentmodule:: basiclife.BasicTermASL_ME.Base

.. automodule:: basiclife.BasicTermASL_ME.Base

Projection parameters
^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~date_
    ~months_
    ~months_in_step
    ~step_to_month
    ~max_proj_len
    ~month_to_step
    ~offset

Model point data
^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~age
    ~age_at_entry
    ~issue_date
    ~model_point
    ~duration_m
    ~duration_y
    ~sex
    ~sum_assured
    ~policy_term
    ~payment_freq
    ~payment_lag
    ~payment_term

Assumptions
^^^^^^^^^^^^^

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~mort_rate
    ~mort_table_reindexed
    ~expense_acq
    ~expense_maint
    ~inflation_factor
    ~inflation_rate
    ~lapse_rate
    ~proj_len
    ~disc_factors
    ~disc_factors_prem
    ~disc_rate


Policy attributes
^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~claim_pp
    ~loading_prem
    ~premium_pp
    ~is_active
    ~is_paying
    ~is_maturing
    ~last_part
    ~next_part
    ~next_anniversary
    ~net_premium_rate
    ~pay_count


Policy decrement
^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~pols_death
    ~pols_if
    ~pols_if_at
    ~pols_if_avg
    ~pols_if_init
    ~pols_lapse
    ~pols_maturity
    ~pols_new_biz
    ~pols_if_pay

Cashflows
^^^^^^^^^^^^^

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~premiums
    ~claims
    ~commissions
    ~expenses
    ~net_cf

Present values
^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~pv_claims
    ~pv_commissions
    ~pv_expenses
    ~pv_net_cf
    ~pv_pols_if
    ~pv_pols_if_pay
    ~pv_premiums

Results
^^^^^^^^^^^^

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~result_cells
    ~result_cf
    ~result_pols
    ~result_pv

Validation
^^^^^^^^^^^^

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~check_pay_count



The :mod:`~basiclife.BasicTermASL_ME.Pricing` space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:currentmodule:: basiclife.BasicTermASL_ME.Pricing

.. automodule:: basiclife.BasicTermASL_ME.Pricing

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~model_point
    ~premium_pp
    ~net_premium_rate

The :mod:`~basiclife.BasicTermASL_ME.Projection` space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:currentmodule:: basiclife.BasicTermASL_ME.Projection

.. automodule:: basiclife.BasicTermASL_ME.Projection

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~premium_pp





