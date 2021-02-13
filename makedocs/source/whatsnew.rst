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

:doc:`... See more updates<updates>`

.. toctree::
   :hidden:

   updates

.. _releases:

Releases
========

The contents of `lifelib.io <https://lifelib.io>`_ are constantly
updated based on the development version of lifelib.
Documentation for released versions of lifelib is available under
:doc:`archive` page.


v0.0.16 (14 February 2021)
------------------------------

.. warning::

   `modelx`_ needs to be updated to v0.12.1 for this version of lifelib.

- :doc:`fastlife <projects/fastlife>` project is added. See the project page for details.

**Related links**

* `modelx blog: Introduction to fastlife and parallel modeling <http://modelx.io/blog/2020/12/12/introduction-to-fastlife-and-parallel-modeling/>`_
* `modelx blog: fastlife got faster <http://modelx.io/blog/2021/01/31/fastlife-got-faster/>`_


v0.0.15 (6 December 2020)
------------------------------

This release includes models updated from the previous version.
The updated models are:

* :doc:`projects/simplelife`
* :doc:`projects/nestedlife`
* :doc:`projects/ifrs17sim`
* :doc:`projects/solvency2`

The updated models produce the same results as the previous version's.
The updated models are much simpler than previous versions, thanks to
2 new enhancements introduced in `modelx v0.9.0`_ and `modelx v0.10.0`_.
One of the enhancements is ExcelRange introduced in `modelx v0.9.0`_.
Input data read from the Excel input file is now stored as *ExcelRange*
objects in the models.
The other enhancement is the introduction of *Relative Reference*.
Thanks to the introduction of the relative reference,
Space formulas in the models got simpler and easier to understand. Read
`this blog post <http://modelx.io/blog/2020/09/19/modelx-v010-introduce-relative-reference/>`_
on modelx site to know more about how *Relative Reference* makes lifelib models simpler.

From this release, models are provided in the form of modelx models,
which are folders containing files and data to construct models.
Models are read into IPython sessions by
`modelx.read_model`_ function. See updated :doc:`spyder` section for how to read models.

Python scripts for building models are not provided from this release.
All the example notebooks now read models using `modelx.read_model`_.

Models from the previous release are also included in the projects.
Those models are files named "model_0_0_14.zip". The zip files
can also be read by `modelx.read_model`_ directly, and no unzipping needed.

.. _modelx.read_model: https://docs.modelx.io/en/latest/reference/generated/modelx.read_model.html

**Related links**

* `modelx blog: Heads-up on lifelib development <http://modelx.io/blog/2020/07/23/heads-up-on-lifelib-development/>`_
* `modelx blog: modelx 0.9.0 introduces a new interface to Excel <http://modelx.io/blog/2020/08/10/modelx-v090-introduce-excel-range/>`_
* `modelx blog: modelx v0.10.0 will make lifelib simpler <http://modelx.io/blog/2020/09/19/modelx-v010-introduce-relative-reference/>`_

* `modelx v0.9.0 release notes <https://docs.modelx.io/en/latest/releases/relnotes_v0_9_0.html>`_
* `modelx v0.10.0 release notes <https://docs.modelx.io/en/latest/releases/relnotes_v0_10_0.html>`_

.. _modelx v0.10.0: https://docs.modelx.io/en/latest/releases/relnotes_v0_10_0.html
.. _modelx v0.9.0: https://docs.modelx.io/en/latest/releases/relnotes_v0_9_0.html


v0.0.14 (18 April 2020)
-----------------------

This release reflects changes for models to run on `modelx`_ v0.5.0.

.. warning::

    Due to backward incompatible changed introduced in `modelx`_
    v0.5.0, models based on lifelib versions prior to this
    release need manual changes in their source code.
    See `commit 605802a`_ and `commit df083f6`_ for where and
    how to make changes in such models.

.. _commit 605802a: https://github.com/fumitoh/lifelib/commit/605802a0ea52d8fbec9a7380b6a0a0717de9bd71
.. _commit df083f6: https://github.com/fumitoh/lifelib/commit/df083f681752eab16508e676c63f9e2f6ae7ca4f


v0.0.13 (27 Dec 2019)
---------------------

.. warning::

   `modelx`_ needs to be updated to v0.1.0 for this version of lifelib.

- :doc:`smithwilson <projects/smithwilson>` project is added. See the project page for details.


v0.0.12 (6 July 2019)
---------------------

.. warning::

   `modelx`_ needs to be updated to v0.0.22 for this version of lifelib.

This version fixes the trouble resulted from erroneous packaging in v0.0.11,
and includes minor code improvements.

- Fix the packaging error in v0.0.11 (`Issue #6 <https://github.com/fumitoh/lifelib/issues/6>`_).
- Update :mod:`~ifrs17sim.ifrs` to include the loss component logic.
- Fix the sign in :func:`~ifrs17sim.ifrs.AmortAcqCashflow`.
- Update :mod:`~simplelife.build_input` to make a better use of
  updated ``new_space_from_excel``.


v0.0.11 (24 March 2019)
-----------------------

.. warning::
    This version of lifelib should not be used, as the uploaded files in
    `PyPI <https://pypi.org/project/lifelib/>`_ were
    not properly packaged and some older files were included
    by mistake.
    You will see an error when you try to run the default models.
    For more on th error and how to fix it,
    see `this discussion on github <https://github.com/fumitoh/lifelib/issues/6>`_.


.. warning::

   `modelx`_ needs to be updated to v0.0.21 for this version of lifelib.

- :doc:`projects/notebooks/simplelife/simplelife-space-overview` notebook is added.
- The input file is renamed from "input.xlsm" to "input.xlsx" and redundant
  data and macros are removed from the file to gain speed in reading.
- Parameter ``module_`` of Space's ``import_module`` method is renamed to ``module``.
- Reserved name ``_self`` is renamed to ``_space``.

v0.0.10 (2 February 2019)
-------------------------

- :doc:`projects/solvency2` project is added. See the project page for details.

- :doc:`projects/notebooks/ifrs17sim/ifrs17sim_charts_lapsescen` notebook is added.

- Override formulas are included in :mod:`~nestedlife.nestedlife` and
  :mod:`~ifrs17sim.ifrs17sim`.

- Update :doc:`projects/ifrs17sim` model to pay out profits each period.

- Fix miscalculation in :func:`~ifrs17sim.projection.IntAccumCF`
  in :mod:`~ifrs17sim.projection`.

- :mod:`~ifrs17sim.ifrs17sim` and :mod:`~ifrs17sim.ifrs` modules are
  modified to correct discounting and surrender in nested projections.


v0.0.9 (5 August 2018)
----------------------

.. warning::

   `modelx`_ needs to be updated to v0.0.13 for this version of lifelib.

   Accordingly, Support for Python 3.4 and 3.5 is dropped. Now Python 3.6 or
   3.7 is required.

- Due to an update in modelx, updating existing cells with ``new_cells``
  method of Space no longer works.
  Accordingly, ``new_cells`` in
  :doc:`generated_examples/nestedlife/plot_actest` and
  :doc:`generated_examples/nestedlife/plot_pvnetcf` examples are replaced
  with ``set_fomula`` method.
  Check `this commit on github <https://github.com/fumitoh/lifelib/commit/c580487d414ae535ff65755d3cdfb46f3aab139a>`__
  to see the exact changes.

- Due to a spec change in modelx, dynamic spaces now inherit their
  parent spaces by default.
  Accordingly, :func:`simplelife.simplelife.build`, :func:`nestedlife.nestedlife.build` and
  :func:`ifrs17sim.ifrs17sim.build` are updated.
  Check `this commit on github <https://github.com/fumitoh/lifelib/commit/14f3263d32de873a672a09ad34f578703ea46180>`__
  to see the exact changes.

v0.0.8 (17 June 2018)
---------------------

- :doc:`/projects/devguide/naming_convention` is introduced, and most source
  functions and some space and modules are renamed to be consistent
  with the naming convention and to improve readability.

- The source code of gallery examples is updated, and it's shorter,
  cleaner and more readable, thanks to the introduction of
  ``space.cells[varnames].to_frame(args)`` expression.


v0.0.7 (3 June 2018)
--------------------

- Replace present value cells in :mod:`~simplelife.projection` with those in :mod:`~simplelife.present_value`.
- Add cells to draw IFRS17 P&L in :mod:`~ifrs17sim.ifrs`.
- Add ``draw_waterfall`` function in ``draw_charts`` module.
- Add a Jupyter notebook and gallery sample for IFRS waterfall chart.
- Add a Jupyter notebook for CSM waterfal chart.
- Update IFRS charts in the gallery of examples.

v0.0.6 (7 May 2018)
-------------------

- :attr:`~simplelife.policy.Product` defined in the table
  in *PolicyData* tab in *input.xlsm* are now strings
  (``TERM``, ``WL``, ``ENDW``) instead of integer IDs (1, 2, 3).

- The assumption data is updated so that the selected sample policies
  become profitable. The default scenario number is changed from 3 to 1.

- Removed redundant local variables in cells in :mod:`~simplelife.assumption`.

- Fixed a bug in the formula of :func:`~simplelife.assumption.ExpsMaintSA`.

- Input loading messages are now output to the standard error.

- :func:`~simplelife.build_input` now saves models as their template names.

- New project template :doc:`projects/ifrs17sim` and its examples are added.

- Insuranc in-force cells and present value cells are added
  in :mod:`projection <simplelife.projection>` module.


- ``new_space_from_module`` methods are replaced with ``import_module``.



