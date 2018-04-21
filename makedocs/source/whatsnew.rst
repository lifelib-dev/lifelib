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

Releases
========

The contents of `lifelib.io <http://lifelib.io>`_ are constantly
updated based on the development version of lifelib.
Documentation for released versions of lifelib is available under
:doc:`archive` page.


v0.0.6.dev (XX April 2018)
--------------------------

Enhancements
~~~~~~~~~~~~
- The plot sample scripts are updated.

- ``build_input`` now saves models as their template names.

- New project template :doc:`projects/ifrs17sim` is added.

- Insuranc in-force cells and present value cells are added
  in :mod:`projection <simplelife.projection>` module.

- The assumption data is updated so that the selected sample policy
  becomes profitable. The default scenario number is changed from 3 to 1.

- ``new_space_from_module`` methods are replaced with ``import_module``.



