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

The library currently includes 2 basic projection models,
:doc:`BasicTerm_S<model_BasicTerm_S>` and :doc:`BasicTerm_M<model_BasicTerm_M>`.
Both of the models produces the exact same results but in different ways.

The :doc:`BasicTerm_S<model_BasicTerm_S>` model defines and executes formulas for each model point separately,
while the :doc:`model_BasicTerm_M` model executes each formula at each time step
for all model points at once. They produce the same results for the same model point.
:doc:`BasicTerm_S<model_BasicTerm_S>` is straight forward, and its formulas are easier to understand,
but it runs slower. It's suitable for validation purposes.
:doc:`BasicTerm_M<model_BasicTerm_M>` is runs fast, but its formulas are expressed as vector operations
and can be more complex in some places.


.. toctree::
   :maxdepth: 2

   model_BasicTerm_S
   model_BasicTerm_M


How to Use the Library
------------------------------

As explained in the :ref:`create-a-project` section,
Create you own copy of the *basiclife* library.
For example, to copy as a folder named *basiclife*
under the path *C:\\path\\to\\your\\*, type below in an IPython console::

    >>> import lifelib

    >>> lifelib.create("basiclife", r"C:\path\to\your\basiclife")


Library Contents
------------------

=========================== ===============================================================
File or Folder              Description
=========================== ===============================================================
model_BasicTerm_S           The :doc:`BasicTerm_S<model_BasicTerm_S>` model.
model_BasicTerm_M           The :doc:`BasicTerm_M<model_BasicTerm_M>` model.
basic_term.xlsx             An Excel file that reproduces the results of a selected model point. The file also shows the derivation of the sample mortality rates.
generate_model_points.ipynb A Jupyter notebook used for generating the sample model points from random numbers.
=========================== ===============================================================



