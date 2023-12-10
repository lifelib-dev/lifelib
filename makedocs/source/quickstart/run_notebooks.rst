.. _running-notebooks:

Running Notebooks
-----------------

Running Notebooks online
^^^^^^^^^^^^^^^^^^^^^^^^

Jupyter Notebook enables you to run Python code in your browser.
lifelib comes with some Jupyter notebooks, and the quickest way
to try lifelib is to run the notebooks online.
Go to :doc:`/notebooks` page and click one of the banner links.
The link will take you to a web page where the selected notebook starts loading.
Once the notebook loads, select **Cell** menu,
and then select **Run All** to run & build models and get results and draw graphs.

Running Notebooks locally
^^^^^^^^^^^^^^^^^^^^^^^^^

Jupyter notebooks on :doc:`/notebooks` page are also included in lifelib
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
