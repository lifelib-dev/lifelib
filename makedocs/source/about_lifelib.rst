
About lifelib
=============

.. _what-is-lifelib:

What is lifelib?
----------------

**lifelib** is a collection of life actuarial models written in Python.
lifelib includes a variety of models, with sample scripts
and Jupyter notebooks to demonstrate how to use the models.
lifelib is being continuously developed, and more models will be added
in future.

The lifelib depends on `modelx`_, an open-source
Python package for building object-oriented models in Python.


.. _what-for:

What for?
---------

lifelib models are highly versatile and transparent.
You can customize lifelib models and utilize them
in various practical areas, such as:

- Model validation / testing
- Pricing / profit testing
- Research / educational projects
- Valuation / cashflow projections
- Asset-liability modeling
- Risk and capital modeling
- Actuarial modernization to replace spreadsheet models


Why lifelib?
------------

lifelib models are built using `modelx`_.
Below is a non-exhaustive list of the advantages of using modelx:

* Models run fast!
* Formulas are easy to read
* Easy to trace formula dependency and errors
* Formulas are instantly evaluated
* Pandas and Numpy can be utilized
* Object-oriented
* Input from Excel and CSV files
* Documents can be integrated
* Models are saved in text files

Consequently, you can expect following benefits from
model development and governance perspectives:

- More efficient, transparent and faster model development
- Model integration with Python ecosystem (Pandas, Numpy, SciPy, etc..)
- Spreadsheet error elimination
- Better version control / model governance
- Automated model testing


.. _how-lifelib-works:

How lifelib works
------------------

lifelib is a Python package, and it includes a variety of *libraries*.
A library is a folder containing models, sample scripts and Jupyter notebooks.
Choose a library you want to use as the base for
your own project, and copy the library from the package
to your own location. See :ref:`here <create-a-project>` for how to make
a copy of a library.

To interface with the model interactively,
start your favorite IPython console, import `modelx`_
and read the model into the IPython session by `modelx.read_model`_ function.
You can use any IPython console, but Spyder with the plugin for modelx
is the recommended IDE as it provides graphical user interface
to lifelib models. Read more about
:doc:`/spyder`.


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
.. _Model: https://docs.modelx.io/en/latest/reference/model.html
.. _Spaces: https://docs.modelx.io/en/latest/reference/space/index.html
.. _Cells: https://docs.modelx.io/en/latest/reference/cells.html

.. toctree::
   :hidden:
   :maxdepth: 2

   archive