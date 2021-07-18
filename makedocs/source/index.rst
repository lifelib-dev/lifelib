.. lifelib documentation master file, created by
   sphinx-quickstart on Sat Nov 11 16:48:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: lifelib

**lifelib**: Actuarial models in Python
=======================================

.. raw:: html

   <div class="lead">

An open-source library of life actuarial models written in Python.
You can run the models right out of the box,
customize them in any way you like, or create your own models from scratch.

.. raw:: html

   </div>


.. panels::
    :container: container-fluid pb-3 examples-container
    :column: col-lg-3 col-md-3 col-sm-12 col-xs-12 p-2

    .. image:: /_static/thumb1.png
       :target: generated_examples/index.html
       :alt: Thumbnail for image example
    ---
    .. image:: /_static/thumb2.png
       :target: generated_examples/index.html
       :alt: Thumbnail for Anscombe's quartet example
    ---
    .. image:: /_static/thumb3.png
       :target: generated_examples/index.html
       :alt: Thumbnail for stocks example
    ---
    .. image:: /_static/thumb4.png
       :target: spyder.html
       :alt: Thumbnail for Lorenz attractor example



.. 1st row: Updates & Quick Start ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-12">
          <h2><a href="whatsnew.html">Last Updates</a></h2>

.. include:: updates.rst
   :start-after: Latest Updates Begin
   :end-before: Latest Updates End

:doc:`... See more updates<updates>`

.. raw:: html

       </div>
     </div>
   </div>

.. 2nd row, Projects & Gallery & Notebooks ---------------------------------


.. panels::
    :container: container-fluid pb-3
    :column: col-lg-3 col-md-3 col-sm-12 col-xs-12 p-2
    :header: h3

    :doc:`About<about_lifelib>`
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    * :ref:`what-is-lifelib`
    * :ref:`how-lifelib-works`
    * :ref:`modindex`
    * :ref:`genindex`
    * :ref:`search`
    * :ref:`past-documents`

    ---

    :doc:`Quick Start<quickstart>`
    ^^^^^^^^^^^^^^^^^^^^^^^

    * :ref:`getting-lifelib`
    * :ref:`using-spyder`
    * :ref:`running-notebooks`

    ---

    :doc:`Libraries<libraries/index>`
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    * :doc:`libraries/basiclife/index`

    ---

    :ref:`Past Libraries<past-libraries>`
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    * :ref:`project_fastlife`
    * :ref:`project_simplelife`
    * :ref:`project_nestedlife`
    * :ref:`project_ifrs17sim`
    * :ref:`project_solvency2`
    * :ref:`project_smithwilson`
    * :doc:`projects/devguide/index`

    ---

    :doc:`Download<download>`
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Download lifelib with WinPython from :doc:`here<download>`.
    No installation is required. Just unzip the file and it's all set.

    ---

    :doc:`Gallery<generated_examples/index>`
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    * :ref:`fastlife_examples`
    * :ref:`simplelife_examples`
    * :ref:`nestedlife_examples`
    * :ref:`ifrs17sim_examples`
    * :ref:`solvency2_examples`
    * :ref:`smithwilson_examples`

    ---

    :doc:`Notebooks<notebooks>`
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    * :ref:`notebooks_fastlife`
    * :ref:`notebooks_simplelife`
    * :ref:`notebooks_ifrs17sim`
    * :ref:`notebooks_smithwilson`


.. 3rd row, modelx sites, links & contact ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-6">

          <h2><strong>modelx</strong> sites</h2>

**modelx** is a Python package to use Python like a spreadsheet.
modelx provides the foundation of lifelib. Find out more
about modelx on the following sites.

========================== ====================================
Home page & Blog           https://modelx.io
Documentation site         https://docs.modelx.io
Development site           https://github.com/fumitoh/modelx
modelx on PyPI             https://pypi.org/project/modelx/
========================== ====================================


.. raw:: html

       </div>
       <div class="col-md-6">

          <h2><strong>lifelib</strong> sites</h2>

If you find a bug, submit an issue on
`lifelib development site <https://github.com/fumitoh/lifelib/issues>`_
on GitHub. Start a discussion on
the `Discussions <https://github.com/fumitoh/lifelib/discussions>`_ site
to ask a question about lifelib, propose a new feature,
or share your experience with lifelib.

========================== ================================================
Development site           https://github.com/fumitoh/lifelib
Discussions                https://github.com/fumitoh/lifelib/discussions
lifelib on PyPI            https://pypi.org/project/lifelib/
Author's profile           https://www.linkedin.com/in/fumito-hamamura
========================== ================================================

.. raw:: html

       </div>
     </div>
   </div>


.. toctree::
   :hidden:
   :maxdepth: 2

   about
   quickstart
   libraries/index
   download
   generated_examples/index
   notebooks
