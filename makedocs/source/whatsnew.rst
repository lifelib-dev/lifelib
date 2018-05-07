.. py:currentmodule:: lifelib.projects

==========
What's New
==========

.. warning::

   **lifelib** and `modelx`_ are in their early alpha-release stage,
   and their specifications are
   subject to changes without consideration on backward compatibility.
   The source files of you models may need to be modified manually,
   if there are updates that break backward compatibility in newer versions
   of modelx.

   Likewise, model files saved with one version may not load with a newer version.
   When updating modelx to a newer version,
   make sure you rebuild model files saved using older versions of modelx
   from their source code.

.. _modelx: http://docs.modelx.io

Updates
=======

.. include:: updates.rst
   :start-after: Latest Updates Begin
   :end-before: Latest Updates End

.. :doc:`... See more updates<updates>`

.. toctree::
   :hidden:

   updates

.. _releases:

Releases
========

.. The contents of `lifelib.io <http://lifelib.io>`_ are constantly
   updated based on the development version of lifelib.
   Documentation for released versions of lifelib is available under
   :doc:`archive` page.


v0.0.6 (7 May 2018)
-------------------

Enhancements
~~~~~~~~~~~~
- :attr:`~simplelife.policy.Product` defined in the table
  in *PolicyData* tab in *input.xlsm* are now strings
  (``TERM``, ``WL``, ``ENDW``) instead of integer IDs (1, 2, 3).

- The assumption data is updated so that the selected sample policies
  become profitable. The default scenario number is changed from 3 to 1.

- Removed redundant local variables in cells in :mod:`~simplelife.assumptions`.

- Fixed a bug in the formula of :func:`~simplelife.assumptions.ExpsMaintSA`.

- Input loading messages are now output to the standard error.

- :func:`~simplelife.build_input` now saves models as their template names.

- New project template :doc:`projects/ifrs17sim` and its examples are added.

- Insuranc in-force cells and present value cells are added
  in :mod:`projection <simplelife.projection>` module.


- ``new_space_from_module`` methods are replaced with ``import_module``.



