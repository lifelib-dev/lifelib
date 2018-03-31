.. module:: nestedlife

Project Template: **nestedlife**
================================

**nestedlife** is a project template to build the same annual projection
model of basic traditional life policies
as :mod:`simplelife`, but at each projection step,
a nested projection going forward from the step is carried out.
The outer and nested projections shares the same base assumptions, but
the assumptions of the nested projections can be adjusted based on how
the outer projection develops upto each projection step at which point a
nested projection starts.

The main purpose of this template is to simulate actual/realistic
cashflows as the outer projection, and expected future cashflows at each
projection step as each of the nested projection.


Model structure
---------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~nestedlife
   ~build_input
   ~lifetable
   ~policy
   ~assumptions
   ~economic
   ~projection
