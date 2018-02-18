Quick Start
===========

Below is a step-by-step guide to introduce you to lifelib.
This guide assumes readers know the basics of Python,
so if you have never used Python, you may want to familiarize yourself
with Python first, and then come back to this introduction to proceed
with this guide. There are many good tutorials out there for learning Python,
such as
`the one on Python's official web site <https://docs.python.org/3/tutorial/>`_.

lifelib models are built in the form of `modelx`_ objects.
Refer to `modelx`_ documentation when you have
questions about `modelx`_ as you proceed with this tutorial.

By going through this guide, you will see how to:

* Prepare Python environment for lifelib,
* Install lifelib,
* Create a project folder,
* Build a model by running a script


Prerequisites
-------------
lifelib runs on Windows or Linux, It probably runs on Mac as well, although
it's not tested on Mac.
Microsoft Excel is not required. You would only need Excel or its alternatives
if you want to edit input data.

lifelib is a Python package, so before building and running liflib models,
you need to have Python environment set up.
You need:

* Python itself,
* Required packages, and
* Python development environment

lifelib supports Python 3.4 or newer versions, so if you are using
Python 2 or a version of Python 3 earlier than 3.4, you should get the
latest version of Python 3.

lifelib depends on other Python packages. Those are:

* `modelx`_
* `openpyxl`_
* `pandas`_

So you also need to get those packages installed with your Python.

Lastly, for you to interface with lifelib models, you would need a Python development
environment. You can still use lifelib through primitive Python consoles,
but you are way better off if you use more sophisticated integrated development
environment(IDE), such as `Spyder`_.

If you want to avoid all the hustle of upgrading and installing Python,
the packages, the IDE, I recommend installing `Anaconda distribution`_.
`Anaconda`_ is a bundle of Python, its major packages and IDEs including
`openpyxl`_, `pandas`_, `Spyder`_, and
it provides a Python environment out-of-the-box,
just by installing it with few clicks.
From here in this page, we'll assume using Anaconda, but most of the contents would
be also valid for non-Aanaconda platform.

.. _modelx: http://docs.modelx.io
.. _openpyxl: https://openpyxl.readthedocs.io
.. _pandas: http://pandas.pydata.org/
.. _Spyder: https://pythonhosted.org/spyder/
.. _Anaconda: https://www.anaconda.com/
.. _Anaconda distribution: https://www.anaconda.com/download/


Installation
------------

lifelib is avalable on `PyPI`_ - the Python Package Index.
To install lifelib, use ``pip`` command from a command prompt.
If you installed `Anaconda`_ on Windows, go to Windows menu and
start *Anaconda Promt* inside *Anaconda3* submenu to bring up a command prompt,
then type::

    > pip install lifelib

The command also installs `modelx`_ the package lifelib depends on.
All the other packages are included `Anaconda`_, so no need to install them
separately.


.. _PyPI: https://pypi.python.org/pypi

.. _create-a-project:

Create a Project
----------------

A lifelib project is a folder(or directory) containing all the source files and data
for building life actuarial models.
A console script ``lifelib-create`` helps you create a new project folder
by copying a template project from within the lifelib package to your desired
folder path.

For example, if you're on Windows and want to create a project folder named
``mylife`` under the path ``C:\Users\fumito`` by copying lifelib's default project
template :py:mod:`simplelife <simplelife>`,
type the following command on the *Anaconda* prompt::

    > lifelib-create --template simplelife C:\Users\fumito\mylife

Alternatively, since :py:mod:`simplelife <simplelife>` is the default tamplate,
so you can get away with `--template` option like this::

    > lifelib-create C:\Users\fumito\mylife

You can check the created folder that are populated with Python scripts
copied from lifelib's default project.

Building the model
------------------

:py:mod:`simplelife <simplelife.simplelife>` file in the project folder is the script for bringing the
actuarial model to existence as a Python object.

If you simply run :py:mod:`simplelife <simplelife.simplelife>` from a command prompt, Python will terminate
when the execution of the script finishes,
To keep the session alive, you need have the session move to the interactive mode
after it finishes the execution of :py:mod:`simplelife <simplelife.simplelife>`.
On `Spyder`_, this is the default behaviour.
When you open :py:mod:`simplelife <simplelife.simplelife>` from *File* menu and *Run* it,
it is executed and the session will move to
interactive mode. The session is available in an IPython console
in `Spyder`_ for you to interface with the created model.

After the model is built, it becomes available as
a global variable :py:data:`model<simplelife.build.model>`
in the Python console.



