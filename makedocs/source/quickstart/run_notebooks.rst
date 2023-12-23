.. include:: /banners.rst

.. _running-notebooks:

Running Notebooks
-----------------

Running Notebooks Online
^^^^^^^^^^^^^^^^^^^^^^^^

Jupyter Notebook enables you to run Python code in your browser.
lifelib libraries include various Jupyter notebooks,
which you can run online immediately on Google Colab.
To do this, go to the :doc:`/notebooks` page,
and click the |colab badge| that is next to the notebook you with to run.
This will redirect you to Google Colab, where your selected notebook begins loading.

Once the notebook has loaded, select *Runtime* from the menu,
and then click *Run anyway* when the warning pop-up appears.
The notebook will then execute from the top to the bottom.
Feel free to experiment by modifying the code, rerunning it, and observing the output.

Running Notebooks Locally
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
