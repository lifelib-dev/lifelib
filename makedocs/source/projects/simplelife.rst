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

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=150;
     simplelife [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC"]
     PresentValue [style=dotted];
     simplelife <- PresentValue;
     Proj [label="Projection[PolicyID]", stacked];
     PresentValue <- Proj [folded, hstyle=generalization]
     simplelife <- Proj [hstyle=composition];
     Proj -> BaseProj [folded, hstyle=generalization]
     BaseProj [style=dotted];
     simplelife <- BaseProj [hstyle=composition, style=dotted];
     Econ[label="Economic[ScenID]", stacked];
     simplelife <- Econ[hstyle=composition];
     Assumption [label="Assumption[PolicyID]", stacked];
     simplelife <- Assumption [hstyle=composition];
     Policy [label="Policy[PolicyID]", stacked];
     simplelife <- Policy [hstyle=composition];
     LifeTable [label="LifeTable\n[Sex, IntRate, TableID]", stacked];
     simplelife <- LifeTable [hstyle=composition];
     simplelife <- Input [hstyle=composition];
     "various..." [stacked];
     Input <- "various..."[hstyle=composition];
   }

.. Begin diagram how-to

How to interpret the diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are three types of relationships between spaces, namely composition, inheritance, and dependency.
The diagram above only depicts composition and inheritance relationships, but does not show dependency
relationships. Spaces that each module depends on are listed in the *ref* section on the page of each source module.

**Composition**

Lines with the filled diamond arrowheads denote that
the spaces on the arrowhead ends contain(and owns) the spaces on the other ends of the lines.
In the example diagram below, Space A contains Space B, i.e.
Space A is the parent of the Space B,
and in tern Space B is a child of Space A.
Note that spaces can be directly under their model, in which case the parent
of the spaces is the model.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=70;
     A <- B[hstyle=composition];
   }


**Inheritance**

Lines with the hollow triangle arrowheads denote that the spaces on the ends without
the arrowheads are derived from the spaces pointed by the arrowheads.
In the example diagram below, Space B is derived from Space A, which means
copies of all the cells, spaces and refs in Space A are included
in Space B.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=70;
     model[shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC"]
     A[style=dotted];
     model<- A;
     A <- B[folded, hstyle=generalization]
     model<- B[hstyle=composition];
   }

The Space B above is drawn as a dotted rectangular to indicate that the space acts
solely as a base space of others, and it's not meant to be directly accessed
by the user.

**Dependency**

When Space B is dependent on Space A, then cells in Space B refer to members of Space A to calculate their values by their formulas.
Dependency is not necessarily the relationship between spaces, but it could be the cells

**Dynamic Spaces**

Dynamic spaces are drawn as a stacked rectangular shape.
Dynamic spaces are, in fact, a 'normal' space with its child spaces dynamically
created when accessed via subscription(``[]``) or call(``()``) operator.
In the example diagram below, Spaces ``A[x]`` are dynamic spaces.
Space A is a normal space and it has a ``x`` parameter.
If A is accessed by, for example ``A[1]``, then a dynamic child space is created under
Space A, and in the dynamic child space ``A[1]``,
Variable ``x`` is available in the child space and it is set to ``1``.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=70;
     model[shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC"]
     model<- "A[x]"[hstyle=composition];
     "A[x]" [stacked]
   }

.. End diagram how-to

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











   

   
   
   

   
   
   