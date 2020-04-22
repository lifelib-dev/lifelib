.. _installation:

Manual Installation
===================

.. Note::

    This page explains how to install liflib on `Anaconda`_ manually.
    If you get lifelib with WinPython from the download page,
    lifelib and all the relevant packages are pre-installed and pre-configured,
    so no need to follow the steps on this page.

Set up Python Environment
-------------------------

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
---------------

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


Install Spyder plugin for modelx
--------------------------------

`Spyder`_ is a popular open-source Python IDE,
and it's bundled in with `Anaconda <https://www.anaconda.com/>`_ by default.
To launch Spyder, go to Windows menu, select Spyder inside *Anaconda3* menu.

.. figure:: /images/SpyderMenu.png

`Spyder`_ allows plugins to be installed to add extra features to itself.
**Spyder plugin for modelx** enriches user interface to modelx in Spyder.
The plugin adds custom IPython consoles
and GUI widgets for using modelx in Spyder.

The plugin is under active development, and currently comes with
a primary version of components, including:

* MxConsole
* MxExplorer
* MxDataView

Spyder plugin for modelx is available on PyPI as a separate Python package.
If you're using Anaconda, you can install the plugin by the following
command::

    > pip install --no-deps spyder-modelx

For more about Spyder plugin for modelx, refer to
`Spyder plugin`_ page
on modelx documentation site.

.. Note::
    lifelib models are built in the form of `modelx`_ objects.
    Refer to `modelx`_ documentation when you have
    questions about `modelx`_ as you proceed with this guide.
    To learn Python itself, there are many good tutorials out there on the web,
    such as
    `the one on Python's official web site <https://docs.python.org/3/tutorial/>`_.

.. _Pandas: http://pandas.pydata.org/
.. _modelx: http://docs.modelx.io
.. _Spyder: https://www.spyder-ide.org/
.. _Spyder plugin: https://docs.modelx.io/en/latest/spyder.html

.. contents:: Contents
   :depth: 1
   :local:

Configure Spyder
----------------

There are 2 Spyder settings that you want to consider changing from their
default values.
Note that you need to restart Spyder to bring your changes into effect.

**Disable User Module Reloader**

Reloading modelx module creates multiple instances of modelx systems within
the same Python process,
causing models created before and after a reload to reside in different
modelx systems. To prevent this, you need to change *User Module Reloader (UMR)*
setting.

From the Spyder menu, select *Tools->Preferences* to bring up Preferences window.
Choose *Python interpreter* in the left pane, and you'll find an area titled
*User Module Reloader (UMR)* on the bottom right side of the Preferences window.
Leave *Enable UMR* option checked,
click *Set UMR excluded(not reloaded) modules* and then UMR dialog box pops up
as the figure blow.
Enter "modelx" in the dialog box. This prevents
Spyder from reloading the modelx module every time you re-run the same script
from *Run* menu, while allowing other modules to be reloaded.


.. figure:: /images/spyder/PreferencesUMR.png

   User Module Reloader setting

**Graphic Backend**

By defult, *Graphic Backend* option is set to *Inline*. This option affects
where graphs are placed, and how modelx GUI widgets behaves.

If *Graphic Backend* is set to *Inline*, graphs are embedded in the IPython
console as an output. If it is set to *Automatic*, graphs are drawn
in separate windows, which pop up upon calling plot methods on matplotlib objects.

If you're fine with the default *Inline* mode, then no need to change anything.
To change *Graphic Backend* option, go to *Tools->Preferences*, and on the
left side of the Preferences window, select *IPython console* then
*Graphics* tab on the right pane.

.. figure:: /images/spyder/PreferencesGraphicsBackend.png

   Graphics Backend setting
