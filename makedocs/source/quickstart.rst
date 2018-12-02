
.. _quick_start:

Quick Start
===========

Running Online
--------------

Jupyter Notebook enables you to run Python code in your browser.
lifelib comes with some Jupyter notebooks, and the quickest way
to try lifelib is to run the notebooks online.
Go to :doc:`notebooks` page and click one of the banner links.
The link will take you to a web page where the selected notebook starts loading.
Once the notebook loads, select **Cell** menu,
and then select **Run All** to run & build models and get results and draw graphs.
To run the notebooks locally on your computer,
refer to `running-notebooks`_ section.

.. _installation:

Installation
------------

Set up Python Environment
^^^^^^^^^^^^^^^^^^^^^^^^^

To run lifelib models locally on your PC,
you need to have a Python environment.
This guide assumes users are on Windows platform,
but lifelib runs on both Windows and Linux,
and probably on Mac as well although it's not tested on Mac.

If you don't have Python environment set up on your computer,
downlowd and install `Anaconda distribution`_.
`Anaconda`_ is a bundle of Python, its major packages and IDEs including
packages required or optionally used by for lifelib,
such as `openpyxl`_, `Pandas`_, `Spyder`_, and provides a Python environment
out-of-the-box, just by installing it with few clicks.

lifelib requires Python 3.6 or newer.
If you already have `Anaconda`_ installed, make sure the Python version is
3.6 or newer. lifelib does not work with Python 2.7.

Microsoft Excel is not required. You would only need Excel or its alternatives
if you want to edit input data files.

.. _modelx: http://docs.modelx.io
.. _openpyxl: https://openpyxl.readthedocs.io
.. _Pandas: http://pandas.pydata.org/
.. _Spyder: https://www.spyder-ide.org/
.. _Anaconda: https://www.anaconda.com/
.. _Anaconda distribution: https://www.anaconda.com/download/

.. Note::

  Although we assume we use  `Anaconda`_ and `Spyder`_ in this guide,
  you should be completely fine with using lifelib with
  other distributions or IDEs, as long as all the relevant
  packages are installed and configured.


Install lifelib
^^^^^^^^^^^^^^^

lifelib is avalable on `PyPI`_ - the Python Package Index.
To install lifelib, use ``pip`` command from an *Anaconda* command prompt.
Go to Windows menu and
start *Anaconda Prompt* inside *Anaconda3* submenu to bring up a command prompt.

.. figure:: /images/AnacondaPrompt.png

Then in the *Anaconda Prompt*, execute the following command::

    > pip install lifelib

When you update your existing installation to the newest release, use ``-U`` option::

    > pip install -U lifelib

The command also installs `modelx`_ package, because lifelib depends on it.
All the other required or optionally used packages are included
in `Anaconda`_, so no need to install them separately.

.. _PyPI: https://pypi.org/project/lifelib/


.. Note::
   *(For advanced users)* To install the latest development version instead of
   the released version,
   clone the `lifelib repository`_ and `modelx repository`_ on github,
   and install them from the cloned repos in `editable mode`_.

.. _lifelib repository: https://github.com/fumitoh/lifelib
.. _modelx repository: https://github.com/fumitoh/modelx
.. _editable mode: https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs

.. _create-a-project:

Creating a Project
------------------

lifelib is essentially a collections of folders called projects, containing
source and data files to build models. You use lifelib by copying
a project from lifelib package to your own path.

A command ``lifelib-create`` helps you create a new project folder
by copying a template project from within the lifelib package to your desired
folder path.

For example, to create a project folder named
``mylife`` under the path ``C:\Users\fumito`` by copying lifelib's default project
template :py:mod:`simplelife<simplelife>`,
type the following command on the *Anaconda* prompt::

    > lifelib-create --template simplelife C:\Users\fumito\mylife

Alternatively, since :py:mod:`simplelife<simplelife>` is the default template,
you can get away with `--template` option like this::

    > lifelib-create C:\Users\fumito\mylife

Check that the folder is created and populated with files
copied from lifelib's default project.

.. _running-notebooks:

Running Notebooks
-----------------

Jupyter notebooks on :doc:`notebooks` page are also included in lifelib
projects, and can be executed on your local computer by running
Jupyter Notebook locally.
For example, if you create a project folder named ``myifrs17sim`` from
the project template :py:mod:`ifrs17sim<ifrs17sim>`,
you can go to the folder by ``cd`` command and launch Jupyter Notebook::

    > cd myifrs17sim

    > jupyter notebook

The command above opens a new tab in your web browser,
and Jupyter Notebook session starts in the tab.

.. figure:: /images/notebook/myifrs17sim-files.png

files with ``ipynb`` extension are Jupyter notebooks. By double-clicking one,
it opens in another tab, and you'll see the same page as you see it online.

Using Spyder
------------
`Spyder`_ is a popular scientific Python IDE,
and it's bundled in with `Anaconda`_ by default.
**Spyder plugin for modelx** adds widgets to Spyder,
letting users to
develop models with modelx more intuitively in Spyder.
Go on to :doc:`spyder` page for more details.

.. toctree::
   :maxdepth: 2

   spyder