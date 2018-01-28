.. lifelib documentation master file, created by
   sphinx-quickstart on Sat Nov 11 16:48:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

lifelib: Actuarial models in Python
=====================================


.. raw:: html

   <!-- Modified from https://github.com/mwaskom/seaborn/blob/master/doc/index.rst -->

    <div style="clear: both"></div>
    <div class="container-fluid">
      <!-- div class="row" -->
        <a href="projects/simplelife.html">
            <img src="_static/LiabilityCashflow.png">
        </a>
      <!-- /div -->
    </div>
    <br>

**lifelib** is a collection of customizable
life actuarial models written in Python.

lifelib is built on top of `modelx`_, a Python package for building
complex models of formulas and data.
Once lifelib models are built, they are avaialable as modelx `Model`_ objects.

A model is composed of `Space`_ objects.
Spaces are units for grouping relevant formulas and data in a model.
Within each spaces, there are `Cells`_ objects.
`Cells`_ are much like cells in spreadsheets. Formulas are associated with cells and
values are stored in them.

With lifelib, you can:

- Create a project folder from a lifelib project template,
- Build a model from Python modules input data in the project,
- Get calculated values by simply accessing model elements,
- Customize the model by changing input and writing formulas in Python,
- Output results to Pandas objects,
- Save the model, load it back again, and do much more.

Start from :doc:`quickstart` page.


.. _modelx: http://docs.modelx.io
.. _Model: http://docs.modelx.io/en/latest/reference/generated/modelx.core.model.Model.html
.. _Space: http://docs.modelx.io/en/latest/reference/generated/modelx.core.model.Space.html
.. _Cells: http://docs.modelx.io/en/latest/reference/generated/modelx.core.model.Cells.html

Features
--------

- Cells containing formulas and data
- Cells graph to track cells interdependency
- Spaces to organize cells by related calculations
- Sub-spacing (having nested spaces within spaces)
- Space inheritance
- Dynamic parametrized spaces created automatically
- Saving to / loading from files
- Conversion to Pandas objects
- Reading data from Excel files

Links
-----

`modelx`_
   A Python package for building complex models of formulas and data.

`lifelib on PyPI <https://pypi.python.org/pypi/lifelib/>`_
   lifelib's Python Package Index page.

`Development site <https://github.com/fumitoh/lifelib>`_
   Github repository of lifelib.


.. currentmodule:: lifelib

.. toctree::
   :hidden:
   :maxdepth: 2

   quickstart
   projects/simplelife


