"""Commutation functions and actuarial notations

The ``LifeTable`` Space includes Cells to calculate
commutation functions and actuarial notations.
``LifeTable`` is parameterized with
``Sex``, ``IntRate`` and ``TableID``. ``TableID`` and
``Sex`` are used in :py:func:`qx` below to identify
the mortality rates to be applied.

Example:

    .. code-block:: python

            >>> fastlife.LifeTable['M', 0.03, 3].AnnDuenx(x=30, n=10)
            8.752619688735953

            >>> fastlife.LifeTable['F', 0.03, 3].qx(x=50)
            0.00196

            >>> fastlife.LifeTable.MortalityTables()
                       1                 2                 3                 4
                       M        F        M        F        M        F        M        F
            0    0.00246  0.00210  0.00298  0.00252  0.00345  0.00298  0.00456  0.00383
            1    0.00037  0.00033  0.00045  0.00034  0.00051  0.00044  0.00069  0.00059
            2    0.00026  0.00023  0.00032  0.00025  0.00038  0.00030  0.00051  0.00041
            3    0.00018  0.00015  0.00022  0.00018  0.00027  0.00020  0.00037  0.00028
            4    0.00013  0.00011  0.00016  0.00013  0.00021  0.00014  0.00029  0.00021
            ..       ...      ...      ...      ...      ...      ...      ...      ...
            126  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000
            127  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000
            128  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000
            129  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000
            130  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000  1.00000

            [131 rows x 8 columns]

References:
    * `International actuarial notation by F.S.Perryman <https://www.casact.org/pubs/proceed/proceed49/49123.pdf>`_
    * `Actuarial notations on Wikipedia <https://en.wikipedia.org/wiki/Actuarial_notation>`_

.. rubric:: Space Parameters

Attributes:
    Sex: 'M' or 'F' to indicate male or female column in the mortality table.
    IntRate: Constant interest rate for discounting.
    TableID: ID of an ultimate mortality table by sex and age.

.. rubric:: References

Attributes:
    MortalityTables: `PandasData`_ object holding the data of mortality tables.
        The data is read from *MortalityTables.xlsx*. Defined also
        in :mod:`fastlife.model.LifeTable`,
        :mod:`fastlife.model.Input` and :mod:`fastlife.model.Projection.Assumptions`


.. _PandasData:
   https://docs.modelx.io/en/latest/reference/dataclient.html#pandasdata


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
    return MortalityTables()[TableID, Sex][x]


# ---------------------------------------------------------------------------
# References

IntRate = 0.01

Sex = "M"

TableID = 1

MortalityTables = ("Pickle", 3020541952136)