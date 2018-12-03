.. module:: simplelife

.. _project_simplelife:

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

.. contents:: Contents
   :depth: 1
   :local:

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

**Composition Structure**

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=150;
     simplelife [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96]
     Proj [label="Projection[PolicyID]", stacked];
     simplelife <- Proj [hstyle=composition];
     Econ[label="Economic[ScenID]", stacked];
     simplelife <- Econ[hstyle=composition];
     Assumption [label="Assumption[PolicyID]", stacked];
     simplelife <- Assumption [hstyle=composition];
     Policy [label="Policy[PolicyID]", stacked];
     simplelife <- Policy [hstyle=composition];
     LifeTable [label="LifeTable\n[Sex, IntRate, TableID]", stacked];
     simplelife <- LifeTable [hstyle=composition];
     simplelife <- Input [hstyle=composition];
     "various..." [stacked, width=96];
     Input <- "various..."[hstyle=composition];
   }

**Inheritance Structure**

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     BaseProj[style=dotted]
     BaseProj <- OuterProj [hstyle=generalization]
     PresentValue[style=dotted]
     PresentValue <- OuterProj [hstyle=generalization];
   }



Project Modules
---------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~simplelife
   ~build_input
   ~lifetable
   ~policy
   ~assumption
   ~economic
   ~projection
   ~present_value











   

   
   
   

   
   
   