"""Space to carry out cashflow projections

This space is for carrying out cashflow projections.
The only difference from its base space,
:mod:`~basiclife.BasicTermASL_ME.Base` is that
:func:`Pricing.premium_pp<basiclife.BasicTermASL_ME.Pricing.premium_pp>`
is assigned to :attr:`~pricing_premium_pp` in this space,
and :func:`premium_pp` is overridden to reference :attr:`~pricing_premium_pp`
and returns the values of it.

Attributes:

    pricing_premium_pp: :func:`Pricing.premium_pp<basiclife.BasicTermASL_ME.Pricing.premium_pp>`

.. _DataFrame:
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = [
    ".Base"
]

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def premium_pp():
    """Premium per policy

    A Series of premium per policy for all the model points.
    Defined as :func:`pricing_premium_pp`, which is ``premium_pp``
    in ``Pricing`` space.
    """
    return pricing_premium_pp()


# ---------------------------------------------------------------------------
# References

pricing_premium_pp = ("Interface", ("..", "Pricing", "premium_pp"), "auto")