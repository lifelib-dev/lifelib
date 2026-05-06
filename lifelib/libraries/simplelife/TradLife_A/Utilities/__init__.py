# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def pandas_to_array(df_or_series):

    return df_or_series.to_numpy() if return_array else df_or_series


_is_cached = False

def map_to_policies(series):
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

