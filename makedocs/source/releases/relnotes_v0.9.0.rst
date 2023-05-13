.. currentmodule:: lifelib.libraries

.. _relnotes_v0.9.0:

==================================
lifelib v0.9.0 (13 May 2023)
==================================

This release adds a new library, :mod:`~ifrs17a`.

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


New Library
===============

This release adds a new library :mod:`~ifrs17a`.

This library includes Python modules that calculate `IFRS 17`_ figures
for sample sets of input data.
The modules read input data such as dimensions, data nodes, discount rates,
and both actual and nominal cashflows,
then calculate items used for IFRS 17 reporting, such as present value
of cashflows, contractual service margin, loss component and loss recovery component.
The calculation logic is based on `IFRS 17 Calculation Engine`_,
which is developed and made open-source under the MIT license by `Systemorph`_, a Swiss software firm.

See :mod:`~ifrs17a`  for more details.

.. _IFRS 17: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-17-insurance-contracts/
.. _IFRS 17 Calculation Engine: https://github.com/Systemorph/IFRS17CalculationEngine
.. _Systemorph: https://systemorph.com/

.. seealso::

    * `Systemorph's repository on github <https://github.com/Systemorph/IFRS17CalculationEngine>`_
    * `Systemorph's site <https://systemorph.com/>`_
    * `Systemorph's YouTube channel <https://www.youtube.com/@systemorph>`_
    * `Crude primary transltion of Systemorph's C# codebase into Python <https://github.com/lifelib-dev/IFRS17CalculationEnginePython>`_





