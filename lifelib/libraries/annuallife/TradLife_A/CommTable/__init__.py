# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Commutation functions and actuarial notations.

The :mod:`~annuallife.TradLife_A.CommTable` Space provides commutation
functions and actuarial notations, such as :math:`D_{x}` and
:math:`\\require{enclose}{}_{f|}\\overline{A}_{x}`.
Mortality tables are read from the ``MortalityTables`` range in
*input.xlsx* through
:func:`~annuallife.TradLife_A.InputData.mortality_tables` and indexed
through :func:`mortality_rates`.

.. rubric:: Parameters

This Space is parameterized with :attr:`Sex`, :attr:`IntRate` and
:attr:`TableID`::

        >>> m.CommTable.parameters
        ('Sex', 'IntRate', 'Table')

Each ItemSpace represents commutation functions and actuarial notations
for a combination of :attr:`Sex`, :attr:`IntRate` and :attr:`TableID`.
For example, ``CommTable[SexID.M, 0.03, 1]`` contains commutation
functions and actuarial notations for Male, an interest rate of 3% and
mortality table 1.

Attributes:
    Sex: A :mod:`~annuallife.TradLife_A.Enums.SexID` code identifying
        the column in the mortality table.
    IntRate(:obj:`float`): The constant interest rate for discounting.
    Table: Identifier of the mortality table within
        :func:`~annuallife.TradLife_A.InputData.mortality_tables`.

.. rubric:: References

Attributes:
    mortality_tables: Alias for
        :func:`~annuallife.TradLife_A.InputData.mortality_tables`.
    pol: Alias for :mod:`~annuallife.TradLife_A.PolicyAttrs`.

Example:

    An example of :mod:`~annuallife.TradLife_A.CommTable`::

        >>> m.CommTable[SexID.M, 0.03, 1].AnnDuenx(40, 10)
        8.725179890621531

External Links:
    * `International actuarial notation by F.S.Perryman <https://www.casact.org/pubs/proceed/proceed49/49123.pdf>`_
    * `Actuarial notations on Wikipedia <https://en.wikipedia.org/wiki/Actuarial_notation>`_

"""

from modelx.serialize.jsonvalues import *

_formula = lambda Sex, IntRate, Table: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def AnnDuenx(x, n, k=1, f=0):
    """ The present value of an annuity-due.

    .. math::

        \\require{enclose}{}_{f|}\\ddot{a}_{x:\\enclose{actuarial}{n}}^{(k)}


    Args:
        x(int): age
        n(int): length of annuity payments in years
        k(int, optional): number of split payments in a year
        f(int, optional): waiting period in years

    """
    if Dx(x) == 0:
        return 0

    result = (Nx(x+f) - Nx(x+f+n)) / Dx(x)

    if k > 1:
        return result - (k-1) / (2*k) * (1 - Dx(x+f+n) / Dx(x))
    else:
        return result


def AnnDuex(x, k, f=0):
    """The present value of a lifetime annuity due.

    Args:
        x(int): age
        k(int, optional): number of split payments in a year
        f(int, optional): waiting period in years
    """
    if Dx(x) == 0:
        return 0

    result = (Nx(x+f)) / Dx(x)

    if k > 1:
        return result - (k-1) / (2*k)
    else:
        return result


def Ax(x, f=0):
    """The present value of a lifetime assurance on a person at age ``x``
    payable immediately upon death, optionally with an waiting period of ``f`` years.

    .. math::

        \\require{enclose}{}_{f|}\\overline{A}_{x}
    """
    if Dx(x) == 0:
        return 0
    else:
        return Mx(x+f) / Dx(x)


def Axn(x, n, f=0):
    """The present value of an assurance on a person at age ``x`` payable
    immediately upon death, optionally with an waiting period of ``f`` years.

    .. math::

        \\require{enclose}{}_{f|}\\overline{A}^{1}_{x:\\enclose{actuarial}{n}}

    """
    if Dx(x) == 0:
        return 0
    else:
        return (Mx(x+f) - Mx(x+f+n)) / Dx(x)


def Cx(x):
    """The commutation column :math:`\\overline{C_x}`.
    """

    return dx(x) * disc()**(x+1/2)


def Dx(x):
    """The commutation column :math:`D_{x} = l_{x}v^{x}`.
    """
    return lx(x) * disc() ** x


def Exn(x, n):
    """ The value of an endowment on a person at age ``x``
    payable after n years

    .. math::

        {}_{n}E_x

    """
    if Dx(x) == 0:
        return 0
    else:
        return Dx(x+n) / Dx(x)


def Mx(x):
    """The commutation column :math:`M_x`."""

    if x >= 110:
        return Dx(x)
    else:
        return Mx(x+1) + Cx(x)


def Nx(x):
    """The commutation column :math:`N_x`."""
    if x >= 110:    # TODO: Get the last age from the table
        return Dx(x)
    else:
        return Nx(x+1) + Dx(x)


def disc():
    """The discount factor :math:`v = 1/(1 + i)`."""
    return 1 / (1 + IntRate)


def dx(x):
    """The number of persons who die between ages ``x`` and ``x+1``"""
    return lx(x) * qx(x)


def lx(x):
    """The number of persons remaining at age ``x``. """
    if x == 0:
        return 100000
    else:
        return lx(x-1) - dx(x-1)


def qx(x):
    """Probability that a person at age ``x`` will die in one year."""
    return mortality_rates()[x]


def mortality_rates():
    """Mortality rates for the selected ``Sex`` and ``Table``.

    Selects the column of :func:`~annuallife.TradLife_A.InputData.mortality_tables`
    matching this Space's :attr:`Table` and :attr:`Sex` parameters and
    returns the resulting per-age mortality rate Series.
    """
    pos = list((t, getattr(SexID, s)) for t, s in mortality_tables().columns).index((Table, Sex))

    return mortality_tables().iloc[:, pos]


# ---------------------------------------------------------------------------
# References

Sex = "M"

IntRate = 0.01

TableID = 1

mortality_tables = ("Interface", ("..", "InputData", "mortality_tables"), "absolute")

pol = ("Interface", ("..", "PolicyAttrs"), "auto")