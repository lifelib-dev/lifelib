.. lifelib documentation master file, created by
   sphinx-quickstart on Sat Nov 11 16:48:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: lifelib

**lifelib**: Actuarial models in Python
=======================================

.. raw:: html

   <div class="lead">

An open-source library of life actuarial models written in Python.
You can run the models right out of the box,
customize them in any way you want, or create your own models from scratch.

.. raw:: html

   </div>

.. raw:: html

   <!-- Modified from https://github.com/mwaskom/seaborn/blob/master/doc/index.rst -->

    <div style="clear: both"></div>
    <div class="container-fluid hidden-xs">
      <div class="row">
        <a href="generated_examples/index.html">
          <div class="col-sm-3 thumbnail">
            <img src="_static/thumb1.png">
          </div>
        </a>
        <a href="generated_examples/index.html">
          <div class="col-sm-3 thumbnail">
            <img src="_static/thumb2.png">
          </div>
        </a>
        <a href="generated_examples/index.html">
          <div class="col-sm-3 thumbnail">
            <img src="_static/thumb3.png">
          </div>
        </a>
        <a href="spyder.html">
          <div class="col-sm-3 thumbnail">
            <img src="_static/thumb4.png">
          </div>
        </a>
      </div>
    </div>

.. 1st row: Updates & Quick Start ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-6">
          <h2><a href="whatsnew.html">Last Updates</a></h2>

.. include:: updates.rst
   :start-after: Latest Updates Begin
   :end-before: Latest Updates End

:doc:`... See more updates<updates>`

.. raw:: html

       </div>
       <div class="col-md-6">
          <h2><a href="quickstart.html">Quick Start</a></h2>

* :ref:`installation`
* :ref:`create-a-project`
* :ref:`running-notebooks`
* :doc:`spyder`

.. raw:: html

       </div>
     </div>
   </div>

.. 2nd row, Projects & Gallery & Notebooks ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-4">
          <h2><a href="projects/index.html">Projects</a></h2>

* :ref:`project_simplelife`
* :ref:`project_nestedlife`
* :ref:`project_ifrs17sim`
* :ref:`project_solvency2`
* :ref:`project_smithwilson`
* :doc:`projects/devguide/index`

.. raw:: html

       </div>
       <div class="col-md-4">
          <h2><a href="generated_examples/index.html">Gallery</a></h2>

* :ref:`simplelife_examples`
* :ref:`nestedlife_examples`
* :ref:`ifrs17sim_examples`
* :ref:`solvency2_examples`

.. raw:: html

       </div>
       <div class="col-md-4">
          <h2><a href="notebooks.html">Jupyter Notebooks</a></h2>

* :ref:`notebooks_simplelife`
* :ref:`notebooks_ifrs17sim`
* :ref:`notebooks_smithwilson`

.. raw:: html

       </div>
     </div>
   </div>

.. 3rd row, Features & Why & What for ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-4">
          <h2>Feature highlights</h2>

* Readable formulas
* Multidimensional data structure
* Instant evaluation
* Dependency tracking (Under development)
* Reusable code
* Object oriented models
* Interface with Excel/Pandas
* Version control
* Documentation integration

.. raw:: html

       </div>
       <div class="col-md-4">
          <h2>Why <strong>lifelib</strong>?</h2>

- Better model integrity and extensibility
- For readable formula expressions
- For eliminating spreadsheet errors
- For better version control/model governance

.. raw:: html

       </div>
       <div class="col-md-4">
          <h2>What for?</h2>

- For research/educational projects
- As communication tools to convey model specifications
- Model validation / testing
- Prototyping for production models
- Pricing / Profit testing
- As corporate models
- For simulations
- As replacement for any spreadsheet models

.. raw:: html

       </div>
     </div>
   </div>

.. 4th row, How it works & questions ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-6">
          <h2>How <strong>lifelib</strong> works</h2>

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

.. raw:: html

       </div>
       <div class="col-md-6">
          <h2>Got questions?</h2>

If you have troubles to shoot, questions to be answered,
post them on `stackoverflow <https://stackoverflow.com/>`_
and add ``lifelib`` tag to the posts.
If you find bugs or want to request new features,
submit issues on
`lifelib development site <https://github.com/fumitoh/lifelib/issues>`_
on github.
Or, connect with
`Fumito Hamamura <https://www.linkedin.com/in/fumito-hamamura>`_
on Linkedin and send a message to him (He may take a while to respond).

.. raw:: html

       </div>
     </div>
   </div>


.. last row, Links & Indexes & Archive ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-6">
          <h2>Links</h2>

* `modelx`_: A Python package for building complex models of
  formulas and data.

* `lifelib on PyPI <https://pypi.python.org/pypi/lifelib/>`_: lifelib's Python
  Package Index page.

* `Development site <https://github.com/fumitoh/lifelib>`_: Github repository of lifelib.


.. raw:: html

       </div>
       <div class="col-md-3">
          <h2>Indexes</h2>


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. raw:: html

       </div>
       <div class="col-md-3">
          <h2>Archive</h2>

.. include:: archive.rst
   :start-after: Past Docs Begin

.. raw:: html

       </div>
     </div>
   </div>


.. toctree::
   :hidden:
   :maxdepth: 2

   whatsnew
   quickstart
   projects/index
   generated_examples/index
   notebooks