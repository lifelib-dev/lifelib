.. module:: simplelife

Project **simplelife**
======================

**simplelife** is a project template to build an annual projection
model of basic traditional life policies.

A simplelife model projects life insurance cashflows and reserves for policies
represented by model points. Projection items include:

* premium income,
* investment income,
* commissions and expenses,
* benefit outgo, change in reserves.

Required capital and investment assets are not modeled.
Input data, such as:

* model point data,
* product specs,
* actuarial assumptions,
* economic scenarios,

are read from an Excel file.

How to use the template
-----------------------

Create a project folder as explained in :ref:`create-a-project` section.
To build the model, simply run :py:mod:`simplelife <simplelife.simplelife>`,
then move to the interactive mode. In Spyder, you can do so by opening the
:py:mod:`simplelife <simplelife.simplelife>` and simply run it.
After the script is run, the model is accessible
as :py:data:`model<simplelife.simplelife.model>` global variable
in the IPython console in `Spyder`_.


You want to make sure the Python session will not terminate after the script is run,
in order for you to do manipulate the model.

The model is accessible through the global variable named :py:data:`model<simplelife.simplelife.model>`.
It is a Model object. Some components of the model are also accessible through global variables.
These are Space objcets. Model and Space are classes defined in modelx package.
For the complete list of model componets available as global variables,
see :py:mod:`simplelife <simplelife.simplelife>` page.

See :py:mod:`simplelife <simplelife.simplelife>` page for further details on the building process,

There is no explicit 'Run' command to run the model. The model calculates its values on the fly, when requested.

.. _Spyder: https://pythonhosted.org/spyder/

Model structure
---------------

The diagram below shows the spaces contained in a simplelife model.
Note that the subspaces under Input space are not drawn in the diagram,
as they are quite a few. For details on the Input subspaces, see :py:mod:`simplelife.build_input` page.

.. figure:: /images/simplelife_drawio.png
   :width: 50%


.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~simplelife
   ~build_input
   ~lifetable
   ~policy
   ~assumptions
   ~economic
   ~projection


There are three types of relationships between spaces, namely containment,  dependency, and inheritance.
This diagram only depicts containment and inheritance relationships, but does not show dependency
relationships. Spaces that each module depends on are listed in the *ref* section on the page of each source module.

Containment
   Lines with the filled diamond arrowheads denote that the spaces on the arrowhead ends
   contain the spaces on the other ends of the lines.
   If Space A contains Space B, then Space B is a subspace of Space A.

Inheritance
   Lines with the triangle arrowheads denote that the spaces on the ends without the arrowheads are derived from the spaces pointed by the arrowheads.
   If Space B is derived from Space A, then cells, refs and static subspaces of Space A are inherited to Space B.

Dependency
   When Space B is dependent on Space A, then cells in Space B refer to members of Space A to calculate their values by their formulas.
   Dependency is not necessarily the relationship between spaces, but it could be the cells









   

   
   
   

   
   
   