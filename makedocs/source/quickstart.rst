
.. _quick_start:

Quick Start
===========

.. _getting-lifelib:

Getting lifelib
---------------

If you are on Windows, simply download lifelib with WinPython from :doc:`here <download>`.
Unzip the file. No installation is required. The file
contains a custom Python distribution based on `WinPython`_ distribution,
with lifelib, modelx and spyder-modelx preinstalled.

.. _WinPython: https://winpython.github.io/

If you are on Linux or Mac, follow the manual installation instruction below.
If you do not wish to use the WinPython-based distribution, and want to use
lifelib on your `Anaconda`_ environment, follow the instruction.

.. toctree::
   :maxdepth: 1

   installation


.. _using-spyder:

Using lifelib on Spyder
-------------------------
`Spyder`_ is a popular scientific Python IDE,
and it's bundled in with WinPython by default.
**Spyder plugin for modelx** adds widgets to Spyder,
letting users to
develop models with modelx more intuitively in Spyder.
Go on to :doc:`spyder` page for more details.

The Spyder plugin for modelx is pre-installed in the zip file :doc:`here <download>`,
and the Spyder in the file is pre-configured and customized.

.. toctree::
   :maxdepth: 2

   spyder

.. _Spyder: https://www.spyder-ide.org/
.. _Anaconda: https://www.anaconda.com/

.. _running-notebooks:

Running Notebooks
-----------------

Running Notebooks online
^^^^^^^^^^^^^^^^^^^^^^^^

Jupyter Notebook enables you to run Python code in your browser.
lifelib comes with some Jupyter notebooks, and the quickest way
to try lifelib is to run the notebooks online.
Go to :doc:`notebooks` page and click one of the banner links.
The link will take you to a web page where the selected notebook starts loading.
Once the notebook loads, select **Cell** menu,
and then select **Run All** to run & build models and get results and draw graphs.

Running Notebooks locally
^^^^^^^^^^^^^^^^^^^^^^^^^

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

