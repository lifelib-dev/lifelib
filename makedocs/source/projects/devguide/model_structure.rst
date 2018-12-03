Model Structure
===============

.. Begin diagram how-to

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
     A[style=dotted]
     A <- B[hstyle=generalization]
   }

The Space A above is drawn as a dotted rectangular to indicate that the space acts
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
