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


What is **lifelib**?
--------------------

**lifelib** is a collection of open-source life actuarial models written in Python.
You can run the models right out of the box,
customize them in any way you want, or create your own models from scratch.


Latest Updates
--------------

.. include:: updates.rst
   :start-after: Latest Updates Begin
   :end-before: Latest Updates End

:doc:`... See more updates<updates>`


Feature highlights
------------------

* Readable formulas
* Multidimensional data structure
* Instant evaluation
* Dependency tracking (Under development)
* Reusable code
* Object oriented models
* Interface with Excel/Pandas
* Version control
* Documentation integration


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


Why **lifelib**?
----------------

- Better model integrity and extensibility
- For readable formula expressions
- For eliminating spreadsheet errors
- For better version control/model governance

What for?
---------

- For research/educational projects
- As communication tools to convey model specifications
- Model validation / testing
- Prototyping for production models
- Pricing / Profit testing
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
Or, connect with
`Fumito Hamamura <https://www.linkedin.com/in/fumito-hamamura>`_
on Linkedin and send a message to him (May take about a week to respond).

Links
-----

* `modelx`_: A Python package for building complex models of
  formulas and data.

* `lifelib on PyPI <https://pypi.python.org/pypi/lifelib/>`_: lifelib's Python
  Package Index page.

* `Development site <https://github.com/fumitoh/lifelib>`_: Github repository of lifelib.

.. toctree::
   :hidden:
   :maxdepth: 2

   whatsnew
   quickstart
   projects/index
   generated_examples/index



Indexes
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Archive
-------

.. include:: archive.rst
   :start-after: Past Docs Begin
