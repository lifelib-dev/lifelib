# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""input_data from files

The ``input_data`` Space includes References that hold input values read from
the Excel input file, *input.xlsx*.
It also includes a few Cells to loock up values from the Referneces.

The References in this Space refer to `ExcelRange`_ objects.
The `ExcelRange` objects hold values read from ranges in the input
Excel file, *input.xlsx*. `ExcelRange`_ objects are Python's mapping objects,
so they support most methods that :obj:`dict` has, and can be
converted to :obj:`dict`. The table below lists the References
and their associated named ranges in *input.xlsx*.

==================== ====================
 References            Named ranges
==================== ====================
PolicyData             PolicyData
mortality_tables        mortality_tables
AssumptionTables       AsmpByDuration
Scenarios              Scenarios
DiscountRate           LargePolDiscount
==================== ====================


.. rubric:: References in this Space

Attributes:
    PolicyData: `ExcelRange`_ object holding policy data. The data
        is read from *PolicyData* range in *input.xlsx*.


    ProductSpec: `ExcelRange`_ object holding the data of product specs.
        The data is read from *ProductSpecTable* range in *input.xlsx*.

    Assumption: `ExcelRange`_ object holding the data of the assumption table.
        The data is read from *AssumptionTable* range in *input.xlsx*.

    mortality_tables: `ExcelRange`_ object holding the data of mortality Tables.
        The data is read from *mortality_tables* range in *input.xlsx*.

    AssumptionTables: `ExcelRange`_ object holding the data of assumptions by duration.
        The data is read from *AsmpByDuration* range in *input.xlsx*.

    Scenarios: `ExcelRange`_ object holding the data of economic scenarios.
        The data is read from *Scenarios* range in *input.xlsx*.

    DiscountRate: `ExcelRange`_ object holding the data of premium discount.
        The data is read from *LargePolDiscount* range in *input.xlsx*.


.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

.. _mapping:
   https://docs.python.org/3/glossary.html#term-mapping

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = True

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def input_workbook():
    return openpyxl.load_workbook(
        _model.path.parent / input_file_name,
        data_only=True)


def policy_data():

    # wb = input_workbook()

    # sheet_name, cell_range = next(wb.defined_names["PolicyData"].destinations)
    # ws = wb[sheet_name]

    # rows = list(ws[cell_range.replace('$', '')])
    # headers = [cell.value for cell in rows[0]]
    # data = [[cell.value for cell in row] for row in rows[1:]]

    # return pd.DataFrame(data, columns=headers).set_index(headers[0])

    return get_named_range_as_df('PolicyData', index_len=1)


def mortality_tables():

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


def assumption_tables():

    # wb = input_workbook()

    # sheet_name, cell_range = next(wb.defined_names["AsmpByDuration"].destinations)
    # ws = wb[sheet_name]

    # rows = list(ws[cell_range.replace('$', '')])
    # headers = [cell.value for cell in rows[0]]
    # data = [[cell.value for cell in row] for row in rows[1:]]

    # return pd.DataFrame(data, columns=headers).set_index(headers[0])

    return get_named_range_as_df('AsmpByDuration', index_len=1)


def get_named_range_as_df(name, index_len=0):

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

    # wb = input_workbook()

    # sheet_name, cell_range = next(wb.defined_names["PolicyData"].destinations)
    # ws = wb[sheet_name]

    # rows = list(ws[cell_range.replace('$', '')])
    # headers = [cell.value for cell in rows[0]]
    # data = [[cell.value for cell in row] for row in rows[1:]]

    # return pd.DataFrame(data, columns=headers).set_index(headers[0])

    return get_named_range_as_df('Scenarios', index_len=2)


def get_named_range_as_dict(name):

    wb = input_workbook()

    sheet_name, cell_range = next(wb.defined_names[name].destinations)
    ws = wb[sheet_name]

    rows = list(ws[cell_range.replace('$', '')])

    return {row[0].value: row[1].value for row in rows}


_is_cached = False

def discount_rate():
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

    return get_named_range_as_dict('PremiumWaiverCost')


def assumption(name):

    return get_param_series('AssumptionTable', name)


def product_spec(name):
    return get_param_series('ProductSpecTable', name)


def get_param_series(range_name, col_name):

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
    return get_named_range_as_dict('ConstParams')


# ---------------------------------------------------------------------------
# References

input_file_name = "input.xlsx"

openpyxl = ("Module", "openpyxl")