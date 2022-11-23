.. module:: cluster

The **cluster** Library
==========================

Overview
---------

The **cluster** library includes a Jupyter notebook
that demonstrates how to apply cluster analysis
to model point selection, as well as data
used for the demonstration and 
other jupyter notebooks and models to generate the data.


How to Use the Library
------------------------------

As explained in the :ref:`create-a-project` section,
Create you own copy of the *cluster* library.
For example, to copy as a folder named *cluster*
under the path *C:\\path\\to\\your\\*, type below in an IPython console::

    >>> import lifelib

    >>> lifelib.create("cluster", r"C:\path\to\your\cluster")


Jupyter Notebooks
------------------------------

.. toctree::
   :maxdepth: 1

   cluster_model_points
   generate_model_points_for_cluster


Library Contents
------------------

.. table::
   :widths: 20 80

   =========================================== ===============================================================
   File or Folder                              Description
   =========================================== ===============================================================
   cluster_model_points.ipynb                  A Jupyter notebook to perform the cluster analysis example
   generate_model_points_for_cluster.ipynb     A Jupyter notebook to generate the seriatim policies used for the example
   BasicTerm_ME_for_Cluster                    A model derived from :mod:`~basiclife.BasicTerm_ME` to generate the cashflows and present values
   cashflows_seriatim_10K.xlsx                 Base cashflow data output from *BasicTerm_ME_for_Cluster*
   cashflows_seriatim_10K_lapse50.xlsx         Lapse-stress cashflow data output from *BasicTerm_ME_for_Cluster*
   cashflows_seriatim_10K_mort15.xlsx          Mortality-stress cashflow data output from *BasicTerm_ME_for_Cluster*
   pv_seriatim_10K.xlsx                        Present values of base cashflows output from *BasicTerm_ME_for_Cluster*
   pv_seriatim_10K_lapse50.xlsx                Present values of lapse-stress cashflows output from *BasicTerm_ME_for_Cluster*
   pv_seriatim_10K_mort15.xlsx                 Present values of mortality-stress cashflows output from *BasicTerm_ME_for_Cluster*
   =========================================== ===============================================================



