.. module:: basiclife

The **basiclife** Library
==========================

Overview
---------

The **basiclife** library is for
building life insurance projection models.
The models in this library project minimum sets of cashflows
of hypothetical generic plain life policies
and no specific regulations are assumed.
The user should customize and extend the models to meet their own needs.

The modeled product is a plain term product with no surrender value.
The projected cashflows are premiums, claims, expenses and commissions.
The assumptions used are mortality rates, lapse rates, discount rates,
expense, inflation and commission rates.
The present values of the cashflows are also calculated.
The premium amount for each individual model point is calculated
as the net premium with loadings, where the net premium is calculated
from the present value of the claims.

The library currently includes 5 basic projection models.

.. toctree::
   :maxdepth: 1

   BasicTerm_S
   BasicTerm_M
   BasicTerm_SE
   BasicTerm_ME
   BasicTermASL_ME

:mod:`~basiclife.BasicTerm_S` and :mod:`~basiclife.BasicTerm_M`
are new business models, i.e. all model points are issued at time 0.
Both of the models produce the exact same results but in different ways.

The :mod:`~basiclife.BasicTerm_S` model defines and executes formulas for each model point separately,
while the :mod:`~basiclife.BasicTerm_M` model executes each formula at each time step
for all model points at once. They produce the same results for the same model point.
:mod:`~basiclife.BasicTerm_S` is straight forward, and its formulas are easier to understand,
but it runs slower. It's suitable for validation purposes.
:mod:`~basiclife.BasicTerm_M` runs fast, but its formulas are expressed as vector operations
and can be more complex in some places.

:mod:`~basiclife.BasicTerm_SE` and :mod:`~basiclife.BasicTerm_ME`
project the cashflows of in-force policies at time 0 as well as
new business policies at 0 or any future time.
:mod:`~basiclife.BasicTerm_ME` is to :mod:`~basiclife.BasicTerm_SE`
as :mod:`~basiclife.BasicTerm_M` is :mod:`~basiclife.BasicTerm_S`.
Formulas in :mod:`~basiclife.BasicTerm_ME` apply to all the model point
at a time while :mod:`~basiclife.BasicTerm_SE` carries out
projection for each model point separately.

:mod:`~basiclife.BasicTermASL_ME` model is an adjustable step length(ASL) model.
With this model, the user can specify the length of each projection step,
from 1 month to 1 year. By default, the first 60 steps are monthly
projections, while steps after that are annual.
This model reads issue date information from model point input,
and handles policy anniversaries precisely.
For more details, see :mod:`~basiclife.BasicTermASL_ME`.

How to Use the Library
------------------------------

As explained in the :ref:`create-a-project` section,
Create you own copy of the *basiclife* library.
For example, to copy as a folder named *basiclife*
under the path *C:\\path\\to\\your\\*, type below in an IPython console::

    >>> import lifelib

    >>> lifelib.create("basiclife", r"C:\path\to\your\basiclife")


Jupyter Notebooks
------------------------------

.. toctree::
   :maxdepth: 1

   generate_model_points
   generate_model_points_with_duration
   generate_model_points_ASL
   create_premium_table


Library Contents
------------------

.. table::
   :widths: 20 80

   =========================================== ===============================================================
   File or Folder                              Description
   =========================================== ===============================================================
   BasicTerm_S                                 The :mod:`~basiclife.BasicTerm_S` model.
   BasicTerm_M                                 The :mod:`~basiclife.BasicTerm_M` model.
   BasicTerm_SE                                The :mod:`~basiclife.BasicTerm_SE` model.
   BasicTerm_ME                                The :mod:`~basiclife.BasicTerm_ME` model.
   BasicTermASL_ME                             The :mod:`~basiclife.BasicTermASL_ME` model.
   basic_term.xlsx                             An Excel file that reproduces the results of a selected model point. The file also shows the derivation of the sample mortality rates.
   create_premium_table.ipynb                  A Jupyter notebbok used for creating the premium table used by :mod:`~basiclife.BasicTerm_SE` and :mod:`~basiclife.BasicTerm_ME`.
   generate_model_points.ipynb                 A Jupyter notebook used for generating the sample model points from random numbers for :mod:`~basiclife.BasicTerm_S` and :mod:`~basiclife.BasicTerm_M`.
   generate_model_points_with_duration.ipynb   A Jupyter notebook used for generating the sample model points from random numbers for :mod:`~basiclife.BasicTerm_SE` and :mod:`~basiclife.BasicTerm_ME`.
   generate_model_points_ASL.ipynb             A Jupyter notebook used for generating the sample model points from random numbers for :mod:`~basiclife.BasicTermASL_ME`.
   =========================================== ===============================================================



