Spyder Plugin for modelx
========================

`Spyder`_ is a popular open-source Python IDE.
`Spyder`_ allows plugins to be installed to add extra features to itself.
**Spyder plugin for modelx** enriches user interface to modelx in Spyder.
The plugin adds following GUI widgets for using modelx in Spyder.

MxConsole
---------

.. figure:: /images/spyder_plugin/MxIPythonConsole.png

*MxConsoles* appear as tabs in Spyder's default IPython console widget,
and host custom IPython shells.
The custom shells function exactly as the default IPython shells,
except that the custom shells are connected to the plugin widgets.
You should use the custom shells instead of
Spyder's default shells in order for the other plugin widgets
to interface with the user's Python sessions.
You can have multiple *MxConsoles* open at the same time,
and each console runs its own IPython session.

MxExplorer
-----------

.. figure:: /images/spyder_plugin/MxExplorer.png

*MxExplorer* is the main plugin widget, and
it contains an object tree pane showing the object tree of
a selected Model. From the context menu on the object tree,
you can perform various operations, such as creating
and deleting modelx objects, defining names bound to objects in the selected
Model, etc. On the right-hand side of MxExplorer, there are
the *Properties* tab and the *Formulas* tab for showing detail information.
The bottom half of the property tab is the *Formula* pane
and it shows the formula of the selected object.
You can edit the formula here and save the change.
When the change is saved, calculated values in the model that depends
on the formula are cleared.

MxDataViewer
-------------

.. figure:: /images/spyder_plugin/MxDataViewer.png

*MxDataViewer* lets you see values of
vector and tabular data in modelx objects,
such as :obj:`list`, :obj:`set`, :obj:`tuple`,
:obj:`dict`, `numpy`_ `array`_, in addition to
`pandas`_ `DataFrame`_, `Series`_, and `Index`_ in a tabular format.
It also shows the values and types of scalar objects,
such as :obj:`int` and :obj:`str`.

.. _numpy: https://numpy.org/
.. _array: https://numpy.org/doc/stable/reference/generated/numpy.array.html
.. _DataFrame: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
.. _Series: https://pandas.pydata.org/docs/reference/api/pandas.Series.html
.. _Index: https://pandas.pydata.org/docs/reference/api/pandas.Index.html

MxAnalyzer
-----------

.. figure:: /images/spyder_plugin/MxAnalyzer.png

*MxAnalyzer* enables you to visually trace calculation dependency.
For a specified combination of a Cell and arguments called *node*,
MxAnalyzer shows a tree of preceding nodes or descending nodes.

For more about Spyder plugin for modelx, refer to
`Spyder plugin`_ page on modelx documentation site.

.. Note::
    lifelib models are built in the form of **modelx** objects.
    The `modelx documentation`_ site includes a step-by-step tutorial
    and reference manual.

.. _Pandas: http://pandas.pydata.org/
.. _modelx documentation: http://docs.modelx.io
.. _Spyder: https://www.spyder-ide.org/
.. _Spyder plugin: https://docs.modelx.io/en/latest/spyder.html

