Using Spyder plugin
===================

.. figure:: /images/spyder/MxPluginImage.png

   Spyder plugin for modelx

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

Building a Model
----------------

Building a model is a process to construct a Model object in a live
Python session from script and source files in your project folder.

By default, you have a project module in your project folder, which has
the same name as the project name, such as
:mod:`simplelife.py <simplelife.simplelife>`.
To build a model, import the project module into a Python session and
call ``build`` function in the module. Let's see how this can be
done in Spyder.

First, Show MxExplorer and MxDataView as instructed in `Spyder plugin`_ page,
and make sure a MxConsole is the active IPython console in the IPython widget.

You'll find *File explorer* in the upper right pane of the main Spyder window.
Bring it up and navigate to your project folder. By doing so, the working
directory(folder) of the MxConsole is
set to the project folder. Then, Type::

  >>> import simplelife
  >>> model = simplelife.build()

Instead of directly typing the code in the console,
you can create a Python script in your project folder,
write the code in the script using *Editor* pane on the left side of the window,
and *Run* it by clicking the green play button in the tool bar.
The script is executed in the MxConsole.

During the build, messages appear as the input file is read in. The next time
you build the model, you can pass ``True`` as ``load_saved`` parameter
of the build function to save loading time::

  >>> model = simplelife.build(load_saved=True)

After model is built successfully, The objects that compose ``model`` object
are shown as a tree in the MxExplorer.

.. figure:: /images/spyder/MxExplorerSimpleLife.png

By selecting a space in the MxExplorer and right clicking and selecting
*Show Formulas* in the context menu, the formulas of the cells
in the selected space are listed next to the model tree in the MxExplorer.

.. figure:: /images/spyder/MxExplorerSimpleLifeWithFormulas.png


Run Projection
--------------

By default, :py:mod:`simplelife<simplelife>` model is set up for you to
carry out projections and store results by policy under
:py:mod:`Projection<simplelife.projection>`. The attributes of the
sample policies are defined on *PolicyData* tab in *Input.xlsm*.

To calculate net liability cashflow of the Policy 1 from time 0 to 15::

   >> proj = model.Projection[1]
   >> result = [proj.NetInsurCF[t] for t in range(16)]

The first line of the above creates ``Projection[1]`` space under
``Projection`` for the Policy 1, and assign a shorter name to it for
convenience.
The second line calculate net liability cashflow of the Policy 1 for
15 years (from time=0 to 15) and store the results in a list ``result``.
To see the values, type ``result``::

   >> result
   [-2090.721539115584,
    1593.887335778444,
    1403.8230981682598,
    1247.2761938300212,
    1113.2288348112097,
    1106.8034770880981,
    979.7641693356699,
    857.345650426334,
    745.0110777520256,
    649.2535254400561,
    567.927885159707,
    496.5241286816653,
    431.8978250326952,
    371.9666103072977,
    317.486904907175,
    0.0]

A dynamic space for the Policy 1 appears in the model tree:

.. figure:: /images/spyder/MxExplorerSimpleLifeDynamicSpace.png

You can see under *Dynamic Spaces* under Projection space, a space
for policy No. 1 (PolicyID=1, ScenID=1) is created.


Output to Pandas objects
------------------------

By calculating ``NetInsurCF`` cells,
other cells that the ``NetInsurCF`` directly or indirectly
refers to are also calculated.
To get the values of all cells in a space, access ``frame`` property of the
space, which returns the values of all the child cells as
`Pandas`_ DataFrame object::

   >> df = proj.frame

`Pandas`_ is a widely-used data analysis library for Python that provides
feature rich data types for data manipulation, such as *DataFrame*.

To see the contents of ``df`` the DataFrame object we have just created,
bring up *Variable explorer* tab on the top right side of the *Spyder* window,
then click on ``df`` row.

.. figure:: /images/spyder/simplelife_df.png

There are many Pandas tutorials and books out there for you to learn
how to slice and dice the data as you like.

Another way to view data in a tabular form is to use MxDataView from
Spyder plugin for modelx.

.. figure:: /images/spyder/MxDataView.png

You can see in the figure above that
the following Python expression is entered in the text box
labeled *Expression*::

    proj.cells['NetInsurCF', 'PremIncome', 'BenefitTotal'].to_frame()

The expression is re-evaluated every time a command in MxConsole
is executed, so the data in table is always up to date.

Run Sample Scripts
------------------

By default, the project folder also contains sample scripts. Files whose
names start with ``plot_`` are the sample scripts that are on
:doc:`generated_examples/index` pages.

Let's run a sample script to draw a graph of liability cashflows.

In `Spyder`_, open ``plot_simplelife.py`` file
in the project folder, from *File* menu or from *File explorer*
and *Run* it. The grpah below shows up in another window.

.. figure:: /images/LiabilityCashflow.png

After execution of the script, the session will move to
interactive mode. The session is available in an IPython console
in `Spyder`_ for you to interface with the created model.

The :py:mod:`Projection <simplelife.projection>` space becomes available as
a global variable ``proj`` in the MxConsole::

    >>> proj
    <Space Projection[171, 1] in lifelib>

