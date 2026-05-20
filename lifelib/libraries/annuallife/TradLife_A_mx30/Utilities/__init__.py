"""Helper cells shared by :mod:`~annuallife.TradLife_A.Assumptions` and
:mod:`~annuallife.TradLife_A.PolicyAttrs`.

This Space is used as a base Space (``_bases``) for
:mod:`~annuallife.TradLife_A.Assumptions` and
:mod:`~annuallife.TradLife_A.PolicyAttrs`, which both derive their
per-policy values by mapping pandas tables onto the rows of the policy
data.

Parameters and References
-------------------------

Attributes:
    return_array(:obj:`bool`): When ``True`` (the default), helper
        functions defined in this Space return NumPy arrays instead of
        pandas objects. Inherited by
        :mod:`~annuallife.TradLife_A.Assumptions` and
        :mod:`~annuallife.TradLife_A.PolicyAttrs`.


Cells Summary
-------------

Helpers that convert pandas objects to per-policy NumPy arrays and
reindex assumption tables onto the policy data.

.. autosummary::

   ~pandas_to_array
   ~map_to_policies

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def pandas_to_array(df_or_series):
    """Return ``df_or_series`` as a NumPy array or as is.

    If the inheriting space sets ``return_array = True`` (the default
    for :mod:`~annuallife.TradLife_A.Assumptions` and
    :mod:`~annuallife.TradLife_A.PolicyAttrs`), the input is converted
    via :meth:`~pandas.Series.to_numpy`. Otherwise the original pandas
    object is returned unchanged.

    This is an uncached cell, so it is recomputed on every call.
    """
    return df_or_series.to_numpy() if return_array else df_or_series


_is_cached = False

def map_to_policies(series):
    """Reindex an assumption ``series`` to one entry per policy.

    Looks up the values of ``series`` for each row of
    :func:`~annuallife.TradLife_A.InputData.policy_data` using the
    columns identified by ``series.index.names`` (e.g. ``Product``,
    ``PolType``, ``Gen``), and returns a Series whose index matches
    ``policy_data`` so it aligns with the per-policy NumPy arrays used
    elsewhere in the model.

    This is an uncached cell, so it is recomputed on every call.
    """
    index_names = series.index.names
    target = input_data.policy_data()[index_names]

    if isinstance(series.index, pd.MultiIndex):
        new_index = pd.MultiIndex.from_frame(target)
    else:
        new_index = pd.Index(target.iloc[:, 0], name=index_names[0])

    result = series.reindex(new_index)
    result.index = target.index
    return result


_is_cached = False

# ---------------------------------------------------------------------------
# References

return_array = True
