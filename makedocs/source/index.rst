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
customize them in any way you want, or create your own models from scratch.

.. raw:: html

   </div>

.. raw:: html

   <!-- Modified from https://github.com/mwaskom/seaborn/blob/master/doc/index.rst -->

    <div style="clear: both"></div>
    <div class="container-fluid hidden-xs">
      <div class="row">
        <a href="generated_examples/index.html">
          <div class="col-sm-3 thumbnail">
            <img src="_static/thumb1.png">
          </div>
        </a>
        <a href="generated_examples/index.html">
          <div class="col-sm-3 thumbnail">
            <img src="_static/thumb2.png">
          </div>
        </a>
        <a href="generated_examples/index.html">
          <div class="col-sm-3 thumbnail">
            <img src="_static/thumb3.png">
          </div>
        </a>
        <a href="spyder.html">
          <div class="col-sm-3 thumbnail">
            <img src="_static/thumb4.png">
          </div>
        </a>
      </div>
    </div>

.. 1st row: Updates & Quick Start ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-6">
          <h2><a href="whatsnew.html">Last Updates</a></h2>

.. include:: updates.rst
   :start-after: Latest Updates Begin
   :end-before: Latest Updates End

:doc:`... See more updates<updates>`


.. raw:: html

       </div>
       <div class="col-md-3">

          <h2><a href="quickstart.html">Quick Start</a></h2>

* :ref:`getting-lifelib`
* :ref:`using-spyder`
* :ref:`running-notebooks`


.. raw:: html

       </div>
       <div class="col-md-3">
          <h2><a href="download.html">Download</a></h2>

            Download lifelib with WinPython from <a href="download.html">here</a>.
            No installation is required. Just unzip the file and it's all set.

.. raw:: html

       </div>
     </div>
   </div>

.. 2nd row, Projects & Gallery & Notebooks ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-4">
          <h2><a href="projects/index.html">Projects</a></h2>

* :ref:`project_simplelife`
* :ref:`project_nestedlife`
* :ref:`project_ifrs17sim`
* :ref:`project_solvency2`
* :ref:`project_smithwilson`
* :doc:`projects/devguide/index`

.. raw:: html

       </div>
       <div class="col-md-4">
          <h2><a href="generated_examples/index.html">Gallery</a></h2>

* :ref:`simplelife_examples`
* :ref:`nestedlife_examples`
* :ref:`ifrs17sim_examples`
* :ref:`solvency2_examples`
* :ref:`smithwilson_examples`

.. raw:: html

       </div>
       <div class="col-md-4">
          <h2><a href="notebooks.html">Jupyter Notebooks</a></h2>

* :ref:`notebooks_simplelife`
* :ref:`notebooks_ifrs17sim`
* :ref:`notebooks_smithwilson`

.. raw:: html

       </div>
     </div>
   </div>

.. 3rd row, Features & Why & What for ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-4">
          <h2>Feature highlights</h2>

* Readable formulas
* Multidimensional data structure
* Instant evaluation
* Dependency tracking
* Reusable code
* Object oriented models
* Interface with Excel/Pandas
* Version control
* Documentation integration

.. raw:: html

       </div>
       <div class="col-md-4">
          <h2>Why <strong>lifelib</strong>?</h2>

- Better model integrity and extensibility
- For readable formula expressions
- For eliminating spreadsheet errors
- For better version control/model governance

.. raw:: html

       </div>
       <div class="col-md-4">
          <h2>What for?</h2>

- For research/educational projects
- As communication tools to convey model specifications
- Model validation / testing
- Prototyping for production models
- Pricing / Profit testing
- As corporate models
- For simulations
- As replacement for any spreadsheet models

.. raw:: html

       </div>
     </div>
   </div>

.. 4th row, How it works & questions ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-6">

          <h2><strong>modelx</strong> sites</h2>

**modelx** is a Python package to use Python like a spreadsheet.
modelx provides the foundation of lifelib. Find out more
about modelx on the following sites.

========================== ====================================
Home page                  https://modelx.io
Documentation site         https://docs.modelx.io
Development site           https://github.com/fumitoh/modelx
modelx on PyPI             https://pypi.org/project/modelx/
========================== ====================================


.. raw:: html

       </div>
       <div class="col-md-6">

          <h2>Links</h2>

Connect with `Fumito Hamamura <https://www.linkedin.com/in/fumito-hamamura>`_
or follow him on LinkedIn to subscribe to updates on lifelib and modelx.

========================== ============================================
Development site           https://github.com/fumitoh/lifelib
lifelib on PyPI            https://pypi.org/project/lifelib/
Author's profile           https://www.linkedin.com/in/fumito-hamamura
========================== ============================================

.. raw:: html

       </div>
     </div>
   </div>


.. last row, Links & Indexes & Archive ---------------------------------

.. raw:: html

   <div class="container-fluid">
     <div class="row">
       <div class="col-md-6">

          <h2>Ask questions</h2>

If you have questions about lifelib, find bugs or want to request new features,
submit issues on
`lifelib development site <https://github.com/fumitoh/lifelib/issues>`_
on github.

.. raw:: html

       </div>
       <div class="col-md-3">
          <h2>Indexes</h2>


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. raw:: html

       </div>
       <div class="col-md-3">
          <h2>Archive</h2>

.. include:: archive.rst
   :start-after: Past Docs Begin

.. raw:: html

       </div>
     </div>
   </div>


.. toctree::
   :hidden:
   :maxdepth: 2

   whatsnew
   download
   quickstart
   projects/index
   generated_examples/index
   notebooks