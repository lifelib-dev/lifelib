"""Commutation functions and actuarial notations

The ``LifeTable`` Space provides
commutation functions and actuarial notations, such as
:math:`D_{x}` and :math:`\\require{enclose}{}_{f|}\\overline{A}_{x}`.
Mortality tables are read from *input.xlsx* into an `ExcelRange`_ object.
The `ExcelRange`_ object is bound to a Reference, :attr:`MortalityTable`.

This Space is included in:

* :mod:`simplelife`
* :mod:`nestedlife`
* :mod:`ifrs17sim`
* :mod:`solvency2`

.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

.. rubric:: Parameters

``LifeTable`` Space is parameterized with :attr:`Sex`,
:attr:`IntRate` and :attr:`TableID`::

        >>> simplelife.LifeTable.parameters
        ('Sex', 'IntRate', 'TableID')

Each ItemSpace represents commutations functions actuarial notations
for a combination of :attr:`Sex`, :attr:`IntRate` and :attr:`TableID`.
For example, ``LifeTable['M', 0.03, 1]`` contains commutation functions
and actuarial notations for Male, the interest rate of 3%, mortality table 1.


Attributes:
    Sex(:obj:`str`): 'M' or 'F' to indicate male or female column in the mortality table.
    IntRate(:obj:`float`): The constant interest rate for discounting.
    TableID(:obj:`int`): The identifier of the mortality table


.. rubric:: References

Attributes:
    MortalityTable: `ExcelRange`_ object holding mortality tables.
        The data is read from *MortalityTables* range in *input.xlsx*.

Example:

    An example of ``LifeTable`` in the :mod:`simplelife` model::

        >>> simplelife.LifeTable['M', 0.03, 1].AnnDuenx(40, 10)
        8.725179890621531

External Links:
    * `International actuarial notation by F.S.Perryman <https://www.casact.org/pubs/proceed/proceed49/49123.pdf>`_
    * `Actuarial notations on Wikipedia <https://en.wikipedia.org/wiki/Actuarial_notation>`_

"""

from modelx.serialize.jsonvalues import *

_formula = lambda Sex, IntRate, TableID: None

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
    return MortalityTable[TableID, Sex, x]


# ---------------------------------------------------------------------------
# References

Sex = "M"

IntRate = 0.01

TableID = 1

MortalityTable = ("IOSpec", 2556818466448, 2556818466448)