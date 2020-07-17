Using Spyder plugin
===================

.. figure:: /images/spyder/MxPluginImage.png

   Spyder plugin for modelx

`Spyder`_ is a popular open-source Python IDE.
To launch Spyder, go to the unzipped folder,
and run *Spyder.exe* by dobule-clicking it.


`Spyder`_ allows plugins to be installed to add extra features to itself.
**Spyder plugin for modelx** enriches user interface to modelx in Spyder.
The plugin adds custom IPython consoles
and GUI widgets for using modelx in Spyder.

The plugin is under active development, and currently comes with
a primary version of components, including:

* MxConsole
* MxExplorer
* MxDataView

For more about Spyder plugin for modelx, refer to
`Spyder plugin`_ page on modelx documentation site.

.. Note::
    lifelib models are built in the form of **modelx** objects.
    The `modelx documentation`_ site includes a step-by-step tutorial
    using simpler examples.
    Check out `modelx documentation`_  site to learn modelx, or
    when you have
    questions about modelx as you proceed with this guide.
    To learn Python itself, there are many good online tutorials,
    such as
    `the one on Python's official web site <https://docs.python.org/3/tutorial/>`_.

.. _Pandas: http://pandas.pydata.org/
.. _modelx documentation: http://docs.modelx.io
.. _Spyder: https://www.spyder-ide.org/
.. _Spyder plugin: https://docs.modelx.io/en/latest/spyder.html

.. contents:: Contents
   :depth: 1
   :local:


.. _create-a-project:

Creating a Project
------------------

lifelib is essentially a collections of folders called projects, containing
source and data files to build models.
You can create your copies of lifelib projects, either from IPython consoles
or from command prompts.

.. rubric:: Creating a project from IPython

You can create a copy of a lifelib project from Spyder's IPython console using
``lifelib.create`` function::

    >>> import lifelib

    >>> lifelib.create("simplelife", "folder")

The first parameter is the name of a lifelib project. If not given,
"simplelife" is assigned. The second parameter is the folder path to create.
If only a folder name is given, the folder is created under the current
folder. The current folder can be reported by ``os.getcwd`` function::

    >>> import os

    >>> os.getcwd()

If the second argument is omitted, the first parameter, which is
the project name is used.

.. rubric:: Creating a project from command prompt

Alternatively, you can create a project from a command prompt.
A command ``lifelib-create`` helps you create a new project folder
by copying a template project from within the lifelib package to your desired
folder path.

For example, to create a project folder named
``mylife`` under the path ``C:\Users\fumito`` by copying lifelib's default project
template :py:mod:`simplelife<simplelife>`,

Go to the unzipped folder and start *WinPython Command Prompt.exe*.
Type the following command on the command prompt::

    > lifelib-create --template simplelife C:\Users\fumito\mylife

Alternatively, since :py:mod:`simplelife<simplelife>` is the default template,
you can get away with `--template` option like this::

    > lifelib-create C:\Users\fumito\mylife

Check that the folder is created and populated with files
copied from lifelib's default project.

.. _read-a-model:

Reading a Model
----------------

The project folder you just created contains a model folder named ``model``.
The model is read from the model folder into a live IPython session.

To read in the model,
show MxExplorer and MxDataView as instructed in the `Spyder plugin`_ page
on the modelx documentation site.
Make sure a **MxConsole** is the active IPython console in the IPython widget.
See the `Spyder plugin`_ page to learn how to create a new MxConsole if you don't
have one.

Right click on the blank space in MxExplorer then a context menu shows up.
Select *Read Model* item in the menu.

.. figure:: /images/spyder/MxExplorerContextMenu.png

Click the folder icon next to the text box at the top,
select the ``model`` folder in the project folder then click *OK*.
After model is read successfully, the components of the model
appear as a tree in the MxExplorer.

.. figure:: /images/spyder/MxExplorerSimpleLife.png

By selecting a space in the MxExplorer and right clicking and selecting
*Show Formulas* in the context menu, the formulas of the cells
in the selected space are listed next to the model tree in the MxExplorer.

.. figure:: /images/spyder/MxExplorerSimpleLifeWithFormulas.png

The model object is available as a global varialbe named ``simplelife``
in the active MxConsole.

.. Note::

    Before lifelib v0.0.15, models are created from Python modules in the
    project folder. With the release of lifelib v0.0.15, the models
    are read from *model* folder in the project folder,
    by `modelx.read_model <https://docs.modelx.io/en/latest/reference/generated/modelx.read_model.html>`_
    function. The Python modules from the older releases are still available
    in *scripts* folder under the project folder.


Run Projection
--------------

By default, :py:mod:`simplelife<simplelife>` model is set up for you to
carry out projections and store results by policy under
:py:mod:`Projection<simplelife.projection>`. The attributes of the
sample policies are defined on *PolicyData* tab in *Input.xlsm*.

To calculate net liability cashflow of the Policy 1 from time 0 to 15::

   >> proj = simplelife.Projection[1]
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

