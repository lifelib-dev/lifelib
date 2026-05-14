
.. _quick_start:

Quick Start
===========

.. _getting-lifelib:

Getting lifelib
---------------

If you are on Windows, simply download lifelib with WinPython from :doc:`here </download>`.
Unzip the file. No installation is required. The file
contains a custom Python distribution based on `WinPython`_ distribution,
which includes preinstalled
lifelib, modelx, spyder-modelx and all other relevant packages.

.. _WinPython: https://winpython.github.io/

If you are on Linux or Mac, follow the manual installation instruction below.
If you do not wish to use the WinPython-based distribution, and want to use
lifelib on your `Anaconda`_ environment, follow the instruction.

.. toctree::
   :maxdepth: 1

   installation

.. _create-a-project:

Copying a Library
------------------

lifelib is essentially a collection of folders called *libraries*,
which contain models and some other files.
You can create your copy of a library, either from IPython console
or from command prompts.

.. rubric:: Creating a library copy from IPython

You can create a copy of a lifelib library from an IPython console using
``lifelib.create`` function::

    >>> import lifelib

    >>> lifelib.create("basiclife", "mylife")

The first parameter is the name of the lifelib library to copy.
The second parameter is the folder path to create.
If only a folder name is given, the folder is created under the current
folder.
The *Files* widget in *Spyder* shows where the current folder is.
Alternatively, the current folder can be reported by ``os.getcwd`` function::

    >>> import os

    >>> os.getcwd()

If the second argument is omitted, the first parameter, which is
the library name is used.

.. rubric:: Creating a library from command prompt

Alternatively, you can copy a library
by a command ``lifelib-create`` from the command prompt
named "WinPython Command Prompt.exe" included in the unzipped folder.

For example, to create a project folder named
``mylife`` under the path ``C:\Users\fumito`` by copying lifelib's default
library :py:mod:`~basiclife`,

Go to the unzipped folder and start *WinPython Command Prompt.exe*.
Type the following command on the command prompt::

    > lifelib-create --template basiclife C:\Users\fumito\mylife

Alternatively, since :py:mod:`~basiclife` is the default library,
you can get away with `--template` option like this::

    > lifelib-create C:\Users\fumito\mylife


.. _using-spyder:

Using lifelib with Spyder
-------------------------

After creating your copy of the desired library,
you can begin exploring and customizing its contents.
For interactive exploration and customization,
IPython consoles in any Python development tool are suitable.

One recommended tool is `Spyder`_,
a popular scientific Python IDE.
It is included by default in the WinPython distribution.
`Spyder`_ is advantageous because of its **Spyder plugin for modelx**.
This plugin enhances Spyder by adding widgets that allow for a graphical interface
with lifelib models built using modelx.
These widgets facilitate the development, execution, and analysis of models more efficiently.

For detailed guidance on using Spyder with lifelib,
refer to the following documentation pages.

.. toctree::
   :maxdepth: 2

   use_with_spyder
   spyder

.. _Spyder: https://www.spyder-ide.org/
.. _Anaconda: https://www.anaconda.com/

Running Notebooks
-----------------

lifelib libraries includes many Jupyter Notebooks for demonstrating
the functionality of library contents.
The following pages shows how to runs the notebooks:

.. toctree::
   :maxdepth: 2

   run_notebooks


Frequently Asked Questions and How-Tos
---------------------------------------

.. toctree::
   :maxdepth: 1

   faq