.. currentmodule:: lifelib.libraries

==================================
lifelib v0.10 Releases
==================================

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


.. _relnotes_v0.10.0:

lifelib v0.10.0 (7 July 2024)
==================================

New Library
----------------

This release adds a new library, :mod:`~appliedlife`.
:mod:`~appliedlife` includes the :mod:`~appliedlife.IntegratedLife` model,
a comprehensive and practical projection model. See the :mod:`~appliedlife` page
for more details.

Fixes
------------

* In :mod:`~basiclife`: Error due to Mortality rate lookup
  before future entry (`GH70 <https://github.com/lifelib-dev/lifelib/pull/70>`_)
* In :mod:`~solvency2`: Eliminate multi-inheritance of dynamic spaces due to modelx update
  (`The commit reflecting changes <https://github.com/lifelib-dev/lifelib/commit/6a38eb37648f8b098f54fc3b97a5a09b3e63f53d>`_)


.. _relnotes_v0.10.1:

lifelib v0.10.1 (15 July 2024)
==================================

This release reflects the following fixes.

Fixes
-------

* In :mod:`~appliedlife.IntegratedLife`, replace ``_space.name`` with ``_space._name``
  and ``_space.cells`` with ``_space._cells`` to make the exported model work with modelx 0.26.0.

* Replace deprecated ``np.NaN`` with ``np.nan``

