# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data loaded from *input.xlsx*.

This Space is :mod:`TradLife_A.InputData <annuallife.TradLife_A.InputData>` with additional
Cells that read the Solvency II life-shock and correlation inputs. The
existing readers (policy data, assumptions, mortality tables, scenarios,
product specs and scalar constants) are unchanged; see
:mod:`TradLife_A.InputData <annuallife.TradLife_A.InputData>` for them.

Cells Summary
-------------

New Cells
^^^^^^^^^

:func:`life_shock_data` reads the ``LifeShocks`` named range and returns
a :obj:`dict` of shock factors keyed by ``(risk, shock, scope,
extra_key)`` integer codes. :func:`life_corr_data` reads the ``LifeCorr``
named range and returns the life-risk correlation matrix as a
:class:`~pandas.DataFrame` indexed on both axes by ``LifeRiskID`` codes.

.. autosummary::

   ~life_shock_data
   ~life_corr_data

Updated Cells
^^^^^^^^^^^^^

:func:`const_params` now also exposes the new ``CoCRate``
(cost-of-capital) parameter read from the ``ConstParams`` range.

.. autosummary::

   ~const_params

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = True

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def input_workbook():
    """Open and return the input Excel workbook.

    Loads the workbook named :attr:`input_file_name` from the parent
    directory of the model with ``data_only=True``, so that formula
    cells return their last cached values.
    """
    return openpyxl.load_workbook(
        _model.path.parent / input_file_name,
        data_only=True)


def policy_data():
    """Policy data table.

    Returns the ``PolicyData`` named range as a ``DataFrame``, indexed by
    the first column (the policy ID).
    """
    return get_named_range_as_df('PolicyData', index_len=1)


def mortality_tables():
    """Mortality tables.

    Reads the ``MortalityTables`` named range, which has a two-row
    header of ``(MortTable, Sex)`` and an age column, and returns a
    ``DataFrame`` indexed by age with a ``MultiIndex`` over the columns.
    """
    wb = input_workbook()

    sheet_name, cell_range = next(wb.defined_names["MortalityTables"].destinations)
    ws = wb[sheet_name]

    rows = list(ws[cell_range.replace('$', '')])

    # Extract the two header rows
    top_header = [cell.value for cell in rows[0]]
    sub_header = [cell.value for cell in rows[1]]

    # Forward-fill None values in the top header (from merged cells)
    filled_top = []
    last = None
    for v in top_header:
        if v is not None:
            last = v
        filled_top.append(last)

    # Skip the first entry of each header row (those are the index's "name" cells)
    columns = pd.MultiIndex.from_arrays([filled_top[1:], sub_header[1:]],
                                        names=[filled_top[0], sub_header[0]])

    # Data: first column becomes index, rest becomes the DataFrame body
    # Convert None to np.nan in cell values
    raw = [[np.nan if cell.value is None else cell.value for cell in row] for row in rows[2:]]

    index = [row[0] for row in raw]
    data = [row[1:] for row in raw]

    df = pd.DataFrame(data, columns=columns, index=index)

    return df


def mort_table_last_ages():
    """First Age (the row index) at which mortality reaches 1, per column.

    Returns a Series indexed by ``mortality_tables().columns``
    (a MultiIndex of (MortTable, Sex)) with the Age value from the row index.
    """
    df = mortality_tables()
    return (df == 1).idxmax()


def assumption_tables():
    """Assumption tables by duration.

    Returns the ``AsmpByDuration`` named range as a ``DataFrame``,
    indexed by the first column (typically duration).
    """
    return get_named_range_as_df('AsmpByDuration', index_len=1)


def get_named_range_as_df(name, index_len=0):
    """Read an Excel named range as a ``DataFrame``.

    Args:
        name(:obj:`str`): The Excel defined-name to read.
        index_len(:obj:`int`, optional): Number of leading columns to
            use as the DataFrame index. Defaults to 0 (no index column).
    """
    wb = input_workbook()

    sheet_name, cell_range = next(wb.defined_names[name].destinations)
    ws = wb[sheet_name]

    rows = list(ws[cell_range.replace('$', '')])
    headers = [cell.value for cell in rows[0]]
    data = [[cell.value if cell.value is not None else np.nan for cell in row] 
            for row in rows[1:]]

    df = pd.DataFrame(data, columns=headers)

    if index_len > 0:
        return df.set_index(headers[:index_len])
    else:
        return df


_is_cached = False

def scenarios():
    """Economic scenarios.

    Returns the ``Scenarios`` named range as a ``DataFrame``, indexed by
    the first two columns (scenario ID and time).
    """
    return get_named_range_as_df('Scenarios', index_len=2)


def get_named_range_as_dict(name):
    """Read an Excel named range as a :obj:`dict`.

    The right-most column of the range becomes the dict values.
    If the range has exactly two columns, the first column becomes the
    keys. If it has more than two columns, the keys are tuples of the
    values of all columns except the right-most one.
    """
    wb = input_workbook()

    sheet_name, cell_range = next(wb.defined_names[name].destinations)
    ws = wb[sheet_name]

    rows = list(ws[cell_range.replace('$', '')])

    result = {}
    for row in rows:
        *key_cells, value_cell = row
        if len(key_cells) == 1:
            key = key_cells[0].value
        else:
            key = tuple(cell.value for cell in key_cells)
        result[key] = value_cell.value

    return result


_is_cached = False

def discount_rate():
    """Per-policy premium discount based on sum-assured bands.

    Reads the ``LargePolDiscount`` named range, builds the breakpoints
    of the sum-assured bands and returns a ``Series`` aligned with
    :func:`policy_data` giving the discount that applies to each policy.
    """
    table = get_named_range_as_dict('LargePolDiscount')

    bins = [-np.inf] + list(table.keys())[:-1] + [np.inf]
    vals = list(table.values())

    return pd.cut(
         policy_data()['SumAssured'],
         bins=bins,
         labels=vals,
         right=False,        # left-closed: [x, y)
     ).astype(float)


def prem_waiver_cost():
    """Premium-waiver cost lookup as a :obj:`dict`.

    Returns the ``PremiumWaiverCost`` named range, mapping the upper
    bound of a policy-term band to its premium-waiver loading.
    """
    return get_named_range_as_dict('PremiumWaiverCost')


def assumption(name):
    """Lookup column ``name`` of the ``AssumptionTable`` range.

    Returns a ``Series`` keyed by the lookup levels (such as
    ``Product``, ``PolType``, ``Gen``) that are not entirely empty
    for column ``name``.
    """
    return get_param_series('AssumptionTable', name)


def product_spec(name):
    """Lookup column ``name`` of the ``ProductSpecTable`` range.

    Returns a ``Series`` keyed by the lookup levels (such as
    ``Product``, ``PolType``, ``Gen``) that are not entirely empty
    for column ``name``.
    """
    return get_param_series('ProductSpecTable', name)


def get_param_series(range_name, col_name):
    """Helper that reads column ``col_name`` from ``range_name`` as a ``Series``.

    The named range is loaded via :func:`get_named_range_as_df` with the
    first three columns used as a `MultiIndex`. Any index level that is
    entirely empty for ``col_name`` is dropped, and a partially empty
    level raises :class:`ValueError`.
    """
    df = get_named_range_as_df(range_name, index_len=3)[col_name].dropna()

    levels_to_drop = []

    for key in df.index.names:
        if df.index.get_level_values(key).isna().all():
            levels_to_drop.append(key)
        elif df.index.get_level_values(key).isna().any():
            raise ValueError(f"'{key}' contains missing values for {col_name}")

    if levels_to_drop:
        df = df.droplevel(levels_to_drop)

    return df


_is_cached = False

def const_params():
    """Scalar parameters from the ``ConstParams`` named range as a :obj:`dict`."""
    return get_named_range_as_dict('ConstParams')


def life_shock_data():
    """Life shock factors from the ``LifeShocks`` named range.

    Returns a :obj:`dict` of shock factors keyed by
    ``(risk, shock, scope, extra_key)``. The enum-name strings in the
    input (e.g. ``MORT``, ``UP``, ``LIMIT``) are converted to the
    corresponding integer codes of :mod:`~annuallife.TradLife_A_EX1.Enums`,
    and a blank qualifier maps to ``0``. Consumed per key by
    :func:`~annuallife.TradLife_A_EX1.Assumptions.life_shock_param`.
    """

    d = get_named_range_as_dict('LifeShocks')

    result = {}
    for (risk, shock, scope, extra_key), value in d.items():
        risk = getattr(LifeRiskID, risk)
        shock = getattr(LapseShockID, shock) if shock is not None else 0
        scope = getattr(LapseScopeID, scope) if scope is not None else 0
        extra_key = getattr(ExtraKeyID, extra_key) if extra_key is not None else 0

        result[(risk, shock, scope, extra_key)] = value

    return result


def life_corr_data():
    """Life-risk correlation matrix from the ``LifeCorr`` named range.

    Returns a square :class:`~pandas.DataFrame` whose row and column
    labels are ``LifeRiskID`` integer codes (the enum-name headers in the
    input are converted to codes). Consumed by
    :func:`~annuallife.TradLife_A_EX1.Assumptions.life_corr`.
    """
    df = get_named_range_as_df('LifeCorr', index_len=1)
    df.columns = [getattr(LifeRiskID, c) for c in df.columns]
    df.index = [getattr(LifeRiskID, r) for r in df.index]
    return df


# ---------------------------------------------------------------------------
# References

input_file_name = "input.xlsx"

openpyxl = ("Module", "openpyxl")

LifeRiskID = ("Interface", ("..", "Enums", "LifeRiskID"), "auto")

LapseShockID = ("Interface", ("..", "Enums", "LapseShockID"), "auto")

ExtraKeyID = ("Interface", ("..", "Enums", "ExtraKeyID"), "auto")

LapseScopeID = ("Interface", ("..", "Enums", "LapseScopeID"), "auto")