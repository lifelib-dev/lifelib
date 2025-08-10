:html_theme.sidebar_secondary.remove:

.. lifelib documentation master file, created by
   sphinx-quickstart on Sat Nov 11 16:48:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: lifelib

**lifelib**: Actuarial models in Python
=======================================

.. raw:: html

   <div class="lead">

lifelib is an open-source Python package featuring practical actuarial models, tools, and examples.
Contribute your excellent work to lifelib and share it with actuaries from all around the world!

.. raw:: html

   </div>


.. grid:: 1 2 4 4

   .. grid-item::

      .. card::
         :img-background: /_static/thumb1.png
         :img-alt: Thumbnail for simplelife example
         :link: generated_examples/index
         :link-type: doc
         :class-card: sd-border-0 sd-bg-transparent
         :class-body: sd-bg-transparent sd-p-0

   .. grid-item::

      .. card::
         :img-background: /_static/thumb2.png
         :img-alt: Thumbnail for savings example
         :link: generated_examples/index
         :link-type: doc
         :class-card: sd-border-0 sd-bg-transparent
         :class-body: sd-bg-transparent sd-p-0

   .. grid-item::

      .. card::
         :img-background: /_static/thumb3.png
         :img-alt: Thumbnail for cluster notebook
         :link: libraries/cluster/cluster_model_points
         :link-type: doc
         :class-card: sd-border-0 sd-bg-transparent
         :class-body: sd-bg-transparent sd-p-0

   .. grid-item::

      .. card::
         :img-background: /_static/thumb4.png
         :img-alt: Thumbnail for Spyder example
         :link: quickstart/spyder
         :link-type: doc
         :class-card: sd-border-0 sd-bg-transparent
         :class-body: sd-bg-transparent sd-p-0


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


.. grid:: 1 1 2 2

   .. grid-item-card:: :doc:`about`

      * :ref:`what-is-lifelib`
      * :ref:`how-lifelib-works`
      * :doc:`contributing`
      * :ref:`modindex`
      * :ref:`genindex`
      * :ref:`search`
      * :ref:`past-documents`


   .. grid-item-card:: :doc:`Quick Start<quickstart/index>`

      * :ref:`getting-lifelib`
      * :ref:`using-spyder`
      * :ref:`running-notebooks`
      * :ref:`faq`


   .. grid-item-card:: :doc:`Libraries<libraries/index>`

      * :doc:`libraries/basiclife/index`
      * :doc:`libraries/savings/index`
      * :doc:`libraries/appliedlife/index`
      * :doc:`libraries/assets/index`
      * :doc:`libraries/ifrs17a/index`
      * :doc:`libraries/economic/index`
      * :doc:`libraries/economic_curves/index`
      * :doc:`libraries/cluster/index`


   .. grid-item-card:: :ref:`Past Libraries<past-libraries>`

      * :ref:`project_fastlife`
      * :ref:`project_simplelife`
      * :ref:`project_nestedlife`
      * :ref:`project_ifrs17sim`
      * :ref:`project_solvency2`
      * :ref:`project_smithwilson`
      * :doc:`projects/devguide/index`


   .. grid-item-card:: :doc:`Gallery<generated_examples/index>`

      * :ref:`savings_examples`
      * :ref:`economic_examples`
      * :ref:`fastlife_examples`
      * :ref:`simplelife_examples`
      * :ref:`nestedlife_examples`
      * :ref:`ifrs17sim_examples`
      * :ref:`solvency2_examples`
      * :ref:`smithwilson_examples`


   .. grid-item-card:: :doc:`Notebooks<notebooks>`

      * :ref:`notebooks_basiclife`
      * :ref:`notebooks_savings`
      * :ref:`notebooks_ifrs17a`
      * :ref:`notebooks_economic`
      * :ref:`notebooks_economic_curves`
      * :ref:`notebooks_cluster`
      * :ref:`notebooks_fastlife`
      * :ref:`notebooks_simplelife`
      * :ref:`notebooks_ifrs17sim`
      * :ref:`notebooks_smithwilson`


   .. grid-item-card:: :doc:`Videos<videos>`

      * :ref:`getting-started-videos`

   .. grid-item-card:: :doc:`Download<download>`

      Download lifelib with WinPython from :doc:`here<download>`.
      No installation is required. Just unzip the file and it's all set.


.. 3rd row, modelx sites, links & contact ---------------------------------

**lifelib** sites
--------------------

Submit an issue on
`lifelib development site <https://github.com/lifelib-dev/lifelib/issues>`_
on GitHub to report a bug.
Start a discussion on
the `Discussions <https://github.com/lifelib-dev/lifelib/discussions>`_ site
to ask a question about lifelib, propose a new feature,
or share your experience with lifelib. Follow
`lifelib's LinkedIn page <https://www.linkedin.com/company/lifelib/>`_
to receive updates.

========================== ================================================
Development site           https://github.com/lifelib-dev/lifelib
Discussions                https://github.com/lifelib-dev/lifelib/discussions
lifelib on PyPI            https://pypi.org/project/lifelib/
LinkedIn page              https://www.linkedin.com/company/lifelib/
========================== ================================================


**modelx** sites
----------------------

**modelx** is a Python package to use Python like a spreadsheet.
modelx provides the foundation of lifelib. Find out more
about modelx on the following sites.

========================== ====================================
Home page & Blog           https://modelx.io
Documentation site         https://docs.modelx.io
Development site           https://github.com/fumitoh/modelx
modelx on PyPI             https://pypi.org/project/modelx/
========================== ====================================



.. toctree::
   :hidden:
   :maxdepth: 2

   about
   quickstart/index
   videos
   libraries/index
   download
   generated_examples/index
   notebooks
