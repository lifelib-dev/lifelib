"""The main space in the Smith-Wilson model

``SmithWilson`` is the only space in the Smith-Wilson model.

The Smith-Wilson method is used for extrapolating risk-free interest rates under the Solvency II framework.
The method is described in
*"QIS 5 Risk-free interest rates – Extrapolation method"*,
a technical paper issued by CEIOPS (the predecessor of EIOPA).
The technical paper is available on `EIOPA's web site`_.
Cells in this space are named consistently
with the mathematical symbols in `the technical paper`_.

.. rubric:: References

Attributes:
    log: `log <https://docs.python.org/3/library/math.html#math.log>`_ function from `the standard math library`_
    exp: `exp <https://docs.python.org/3/library/math.html#math.exp>`_ function from `the standard math library`_
    np: `Numpy`_ module
    N: Number of durations for which the observed spot rates are available
    spot_rates: List of the observed spot rates (annual compound)
    UFR: The ultimate forward rate (continuous compound)
    alpha: The convergence parameter :math:`\alpha`

.. _Numpy : https://numpy.org/

.. _EIOPA's web site: https://wayback.archive-it.org/org-1495/20191229100044/https:/eiopa.europa.eu/publications/qis/insurance/insurance-quantitative-impact-study-5/background-documents

.. _the technical paper: https://wayback.archive-it.org/org-1495/20191229100044/https:/eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf

.. _the standard math library: https://docs.python.org/3/library/math.html
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def u(i):
    """Time (:math:`u_i`)

    :func:`u` is a series of discrete time points.
    ``i`` is a 1-based index. By default, :func:`u` just returns ``i``.

    For i = 1, ..., :attr:`N`, :func:`u` corresponds to
    :math:`u_i` in `the technical paper`_,
    The time to maturities of the observed zero-coupon bond prices.

    :attr:`spot_rates`, the observed spot rates must exist at each
    ``u(i)`` from i = 1 to :attr:`N`. Note that :attr:`spot_rates` is
    0-based, so the sport rate at ``u(i)`` is ``spot_rates[i-1]``.

    Args:
        i: The time index (1, 2, ...)

    """
    return i


def m(i):
    r"""Observed zero-coupon bond prices at time :math:`u_i`.

    :func:`m` is calculated from :attr:`spot_rates` as
    :math:`(1 + spot\_rates[i-1])^{-u_i}`

    Args:
        i(int): Time index (1, 2, ..., :attr:`N`)
    """
    return (1 + spot_rates[i-1]) ** (-u(i))


def mu(i):
    r"""Ultimate Forward Rate (UFR) discount factors

    :func:`mu` is defined as :math:`e^{-UFR\cdot u_i}`.

    Args:
        i(int): Time index (1, 2, ...)
    """
    return exp(-UFR * u(i))


def W(i, j):
    r"""The Wilson functions.

    :func:`W` corresponds to formula (2) on page 16 in `the technical paper`_
    defined as:

    .. math::

        W(t, u_j)=  \
            e^{-UFR\cdot (t+u_j)}\cdot  \
            \left\{   \
                \alpha\cdot\min(t, u_j) \
                -0.5\cdot e^{-\alpha\cdot\max(t, u_j)}\cdot(    \
                    e^{\alpha\cdot\min(t, u_j)}     \
                    -e^{-\alpha\cdot\min(t, u_j)}    \
                    )   \
            \right\}

    where :math:`t = u_i`.

    Args:
        i(int): Time index (1, 2, ..., :attr:`N`)
        j(int): Time index (1, 2, ..., :attr:`N`)
    """
    t = u(i)
    uj = u(j)

    return exp(-UFR * (t+uj)) * (
            alpha * min(t, uj) - 0.5 * exp(-alpha * max(t, uj)) * (
                    exp(alpha*min(t, uj)) - exp(-alpha*min(t, uj))
            ))


def m_vector():
    """The :func:`m` vector.

    :func:`m` as 1-dimensional :attr:`N` length numpy array.
    """
    return np.array([m(i) for i in range(1, N+1)])


def mu_vector():
    """The :func:`mu` vector.

    :func:`mu` as 1-dimensional :attr:`N` length numpy array.
    """
    return np.array([mu(i) for i in range(1, N+1)])


def W_matrix():
    """The :func:`W` matrix.

    :func:`W` as a 2-dimensional :attr:`N` x :attr:`N` numpy array.
    """
    return np.array([[W(i, j) for j in range(1, N+1)] for i in range(1, N+1)])


def zeta_vector():
    r"""The :func:`zeta` vector.

    :func:`zeta_vector` returns :math:`\zeta` parameters calculated
    by formula (5) on page 17 in `the technical paper`_, which is

    .. math::

        \bf \zeta= W^{-1}(p-\mu)

    """
    return np.linalg.inv(W_matrix()) @ (m_vector() - mu_vector())


def zeta(i):
    r"""The :math:`\zeta_i` parameters fitted to the observed spot rates.

    Args:
        i(int): Time index (1, 2, ..., :attr:`N`)
    """
    return zeta_vector()[i-1]


def P(i):
    r"""Zero-coupon bond prices extrapolated by the Smith-Wilson method.

    :func:`P` corresponds to formula (1) on page 16 or formula (6)
    on page 18 in `the technical paper`_, defined as:

    .. math::

        P(t) = e^{-UFR\cdot t}+\sum_{j=1}^{N}\zeta_{j}\cdot W(t, u_j)

    substituting :math:`t` with :math:`u_i`.

    The values of :func:`P` for ``i=1, ..., N`` should be the same
    as the values of :func:`m`, the observed bond prices.

    Args:
        i(int): Time index (1, 2, ...)
    """
    return mu(i) + sum(zeta(j) * W(i, j) for j in range(1, N+1))


def R(i):
    r"""The extrapolated annual compound sport rates.

    :func:`R` corresponds to :math:`R_t` defined as:

    .. math::

        R_t = \left(\frac{1}{P(t)}\right)^\left(\frac{1}{t}\right)-1

    on page 18 in `the technical paper`_,
    substituting :math:`t` with :math:`u_i`.

    The values of :func:`R` for ``i=1,...,N`` should be same as the values
    of the observed spot rates :attr:`spot_rates` for 0, ... ,N-1.

    Args:
        i(int): Time index (1, 2, ...)
    """
    return (1 / P(i)) ** (1 / u(i)) - 1


# ---------------------------------------------------------------------------
# References

np = ("Module", "numpy")

log = ("Pickle", 2074070178376)

exp = ("Pickle", 2074070177016)

UFR = 0.028587456851912472

alpha = 0.128562

N = 25

spot_rates = ("Pickle", 2072439860616)