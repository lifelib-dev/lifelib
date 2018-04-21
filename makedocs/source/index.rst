.. lifelib documentation master file, created by
   sphinx-quickstart on Sat Nov 11 16:48:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: lifelib

**lifelib**: Actuarial models in Python
=======================================


.. raw:: html

   <!-- Modified from https://github.com/mwaskom/seaborn/blob/master/doc/index.rst -->

    <div style="clear: both"></div>
    <div class="container-fluid">
      <!-- div class="row" -->
        <a href="projects/simplelife.html">
            <img src="_images/LiabilityCashflow.png">
        </a>
      <!-- /div -->
    </div>
    <br>


**lifelib** is a collection of actuarial projection models.
lifelib models are built as `modelx`_ models, ready to be used out of the box
with sample formulas and input files, and they are
fully customizable by users.

Latest Updates
--------------

.. include:: updates.rst
   :start-after: Latest Updates Begin
   :end-before: Latest Updates End

.. :doc:`... See more updates<updates>`

How **lifelib** works
---------------------

You can create an actuarial projection model as `modelx`_ `Model`_ object by:

- Creating a project folder from a lifelib project template,
- Build a `modelx`_ `Model`_ from source modules and
  input data in the project, by running
  :py:func:`build <simplelife.simplelife.build>` function.

Once the model is built, they are available as a modelx `Model`_ object
in Python console. The model is composed of `Space`_.
Spaces contain `Cells`_ and other spaces.
`Cells`_ are much like cells in spreadsheets, which in turn, can store
formulas and associated values.

With a lifelib model, you can:

- Get calculated values by simply accessing model elements,
- Change the model by changing input and writing formulas in Python,
- View the tree of model elements in graphical user interface,
- Output results to Pandas objects,
- Save the model, load it back again, and do much more.

Start from :doc:`quickstart` page.


.. _modelx: http://docs.modelx.io
.. _Model: http://docs.modelx.io/en/latest/reference/generated/modelx.core.model.Model.html
.. _Space: http://docs.modelx.io/en/latest/reference/generated/modelx.core.space.Space.html
.. _Cells: http://docs.modelx.io/en/latest/reference/generated/modelx.core.cells.Cells.html


Feature highlights
------------------

- Formulas and their calculated values paired as `Cells`_,
  just like spreadsheet cells
- Relevant cells grouped together as a `Space`_, just like a spreadsheet
- Spaces in other spaces (subspaces), forming trees of spaces
- Object-oriented `Model`_ composed of spaces
- Space inheritance
- Parametrized dynamic subspaces created automatically
- Saving to / loading from files
- Conversion to Pandas objects
- Reading data from Excel files
- Cells graph to track cells interdependency

Why **lifelib**?
----------------

- Better model integrity and extensibility
- For readable formula expressions
- For eliminating spreadsheet errors
- For better version control/model governance

What for?
---------

- Pricing / Profit testing
- Model validation / testing
- Prototyping for production models
- As corporate models
- For simulations
- As replacement for any spreadsheet models

Got questions?
--------------
If you have troubles to shoot, questions to be answered,
post them on `stackoverflow <https://stackoverflow.com/>`_
and add ``lifelib`` tag to the posts.
If you find bugs or want to request new features,
submit issues on
`lifelib development site <https://github.com/fumitoh/lifelib/issues>`_
on github.

Links
-----

`modelx`_
   A Python package for building complex models of formulas and data.

`lifelib on PyPI <https://pypi.python.org/pypi/lifelib/>`_
   lifelib's Python Package Index page.

`Development site <https://github.com/fumitoh/lifelib>`_
   Github repository of lifelib.

.. toctree::
   :hidden:
   :maxdepth: 2

   whatsnew
   quickstart
   generated_examples/index
   projects/index
   archive


Indexes
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

