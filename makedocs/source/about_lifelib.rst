
About lifelib
=============

.. _what-is-lifelib:

What is lifelib?
----------------

**lifelib** is a collection of Python libraries for actuaries.
lifelib includes a variety of actuarial models, tools,
sample scripts and Jupyter notebooks.
If you have a personal Python project for actuaries,
consider contributing your excellent work to lifelib
and share it with actuaries all over the world!
See :doc:`here<contributing>` for how to contribute to lifelib.


.. _what-for:

Why lifelib and What for?
---------------------------

.. rubric:: Leveraging Python in various actuarial areas

Python is one of the most popular programming languages.
It's open-source, and widely used in the data science field.

Python is such a popular language that a tremendous amount
of information about it is available on the Internet.
There are countless free learning courses, tutorials, articles and e-books on Python.
It's even hard to find questions about Python not answered by anyone.
The Python ecosystem for scientific computing includes
many high-quality third-party libraries, such as NumPy, pandas, SciPy, scikit-learn and more.

Although Python, or any programming language for that matter, is not
yet used for daily actuarial tasks so much as Excel is,
Python will be the most powerful tool for actuaries.

lifelib promotes Actuaries' usage of Python, and
can be utilized in various practical areas, such as:

- Model validation / testing
- Pricing / profit testing
- Research / educational projects
- Valuation / cashflow projections
- Experience studies
- Asset-liability modeling
- Risk and capital modeling
- Actuarial process automation
- Actuarial modernization to replace spreadsheet models

.. rubric:: lifelib as a single point of reference

If you have a Python project for actuaries, then lifelib
is a great place to showcase your project and reach out to more actuaries
than you could by putting your work on github personally.

By contributing your work to lifelib
and property documenting the contents, such as your models, tools, and scripts,
your work is beautifully rendered and presented on `lifelib.io <https://lifelib.io>`_.
lifelib as a Python package is available on `PyPI`_ and `conda-forge`_,
so the users can find, install and update your work in lifelib more easily.

.. _PyPI: https://pypi.org/project/lifelib/
.. _conda-forge: https://anaconda.org/conda-forge/lifelib

.. rubric:: Escaping from spreadsheet hell!

Many models in lifelib are using `modelx`_,
an open-source Python package for building object-oriented models in Python.
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
A library is a folder containing actuarial models, sample scripts and Jupyter notebooks.
Choose a library you want to use as the base for
your own project, and copy the library from the package
to your own location. See :ref:`here <create-a-project>` for how to make
a copy of a library.
Sample scripts and Jupyter notebooks are executable out of the box.

.. rubric:: modelx models

Most libraries include models built with `modelx`_.
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
