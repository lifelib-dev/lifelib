
About lifelib
=============

.. _what-is-lifelib:

What is lifelib?
----------------

lifelib is a collection of life insurance models.
The lifelib models are built using `modelx`_, an open-source
Python package for building object-oriented models in Python.
lifelib includes a variety of models along with some sample scripts
and Jupyter notebooks that demonstrate how to use the models and draw
graphs. More models will be added in future.

.. _what-for:

What for?
---------

lifelib models are highly customizable, and
thanks to modelx's strong inspection capability,
they are best suited for such purposes as model validation, where
you need to inspect calculations for each individual model point.

- For model validation / testing
- For pricing / profit testing
- For research/educational projects
- For prototyping production models in agile developments
- For defining model requirements in replacement for documents
- As replacement for any spreadsheet models

Why lifelib?
------------

lifelib models are built using `modelx`_.
Below is a non-exaustive list of the advantages of using modelx:

* Readable formulas
* Multidimensional data structure
* Instant evaluation
* Dependency tracking
* Reusable code
* Object oriented models
* Interface with Excel/Pandas
* Version control
* Documentation integration

Consequently, you can expect following benefits from
model development and governance perspectives:

- More efficient, transparent and faster model development
- Model integration with Python ecosystem (Pandas, Numpy, SciPy, etc..)
- Spreadsheet error elimination
- Better version control/model governance
- Automated model testing


.. _how-lifelib-works:

How lifelib works
------------------

lifelib is a Python package, and it includes a variety of projects.
A project is a folder containing a model, sample scripts and Jupyter notebooks.
You can choose a project you want to use as the base for
your own project, and copy the project from the package
to your own location. See :ref:`here <create-a-project>` for how to make
a copy of a project.

Once you make your own copy of the project, you can run the scripts
or the notebooks in the project.

To interface with the model interactively,
start your favorite IPython console, import `modelx`_
and read the model into the IPython session by `modelx.read_model`_ function.

.. _modelx.read_model: https://docs.modelx.io/en/latest/reference/generated/modelx.read_model.html

Once the model is read, it is available as a modelx `Model`_ object
in the IPython session. The model is composed of `Spaces`_.
Spaces contain `Cells`_ and other Spaces.
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
.. _Spaces: http://docs.modelx.io/en/latest/reference/generated/modelx.core.space.Space.html
.. _Cells: http://docs.modelx.io/en/latest/reference/generated/modelx.core.cells.Cells.html


.. toctree::
   :hidden:
   :maxdepth: 2

   archive