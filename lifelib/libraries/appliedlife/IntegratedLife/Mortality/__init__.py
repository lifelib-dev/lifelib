"""Mortality tables

The :mod:`~appliedlife.IntegratedLife.Mortality` space reads
mortality tables from a mortality file
and creates a unified mortality table as a pandas Series
indexed with Table ID, Attained Age and Duration.

This space is referenced as :attr:`~appliedlife.IntegratedLife.ProductBase.mort_data`
in the :mod:`~appliedlife.IntegratedLife.ProductBase` space.

Attributes:

    base_data: Reference to the :mod:`~appliedlife.IntegratedLife.BaseData` space

Example:

    The sample code below demonstrates how to examine the contents of
    :mod:`~appliedlife.IntegratedLife.Mortality`.

    .. code-block:: python

        >>> import modelx as mx

        >>> m = mx.read_model("IntegratedLife")

        >>> m.Mortality.mort_file()
        WindowsPath('C:/Users/User1/appliedlife/input_tables/mortality_tables.xlsx')

        >>> m.Mortality.table_defs()

                  is_used sex  ... has_select                             description
        table_id               ...
        T3363        True   M  ...       True    2017 Unloaded CSO Composite Male ALB
        T3364        True   F  ...       True  2017 Unloaded CSO Composite Female ALB
        T3275        True   M  ...       True              2015 VBT Unismoke Male ALB
        T3276        True   F  ...       True            2015 VBT Unismoke Female ALB
        T884         True   F  ...      False               Annuity 2000 Basic Female
        T885         True   M  ...      False                 Annuity 2000 Basic Male

        >>> m.Mortality.select_table('T3276')

                 0        1        2        3   ...       21       22       23       24
        0   0.00022  0.00012  0.00008  0.00007  ...  0.00029  0.00032  0.00035  0.00036
        1   0.00012  0.00008  0.00007  0.00007  ...  0.00032  0.00035  0.00036  0.00036
        2   0.00008  0.00007  0.00007  0.00007  ...  0.00035  0.00036  0.00036  0.00035
        3   0.00007  0.00007  0.00007  0.00007  ...  0.00036  0.00036  0.00035  0.00035
        4   0.00007  0.00007  0.00007  0.00007  ...  0.00036  0.00035  0.00035  0.00036
        ..      ...      ...      ...      ...  ...      ...      ...      ...      ...
        91  0.02529  0.06300  0.13175  0.16683  ...  0.50000  0.50000  0.50000  0.50000
        92  0.03682  0.09384  0.16683  0.18406  ...  0.50000  0.50000  0.50000  0.50000
        93  0.05460  0.12337  0.18406  0.20412  ...  0.50000  0.50000  0.50000  0.50000
        94  0.08008  0.16292  0.20412  0.22599  ...  0.50000  0.50000  0.50000  0.50000
        95  0.11495  0.20412  0.22599  0.24952  ...  0.50000  0.50000  0.50000  0.50000

        [96 rows x 25 columns]

        >>> m.Mortality.merged_table('T3276')

        att_age  duration
        0        0           0.00022
        1        1           0.00012
        2        2           0.00008
        3        3           0.00007
        4        4           0.00007

        116      25          0.50000
        117      25          0.50000
        118      25          0.50000
        119      25          0.50000
        120      25          0.50000
        Length: 2521, dtype: float64

        >>> m.Mortality.unified_table()

        table_id  att_age  duration
        T3363     0        0           0.00019
                  1        1           0.00012
                  2        2           0.00011
                  3        3           0.00009
                  4        4           0.00009

        T885      116      0           1.00000
                  117      0           1.00000
                  118      0           1.00000
                  119      0           1.00000
                  120      0           1.00000
        Length: 10326, dtype: float64

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def merged_table(table_id: str):
    """Merged mortality table for a given table ID"""
    has_select = table_defs().at[table_id, "has_select"]
    has_ultimate = table_defs().at[table_id, "has_ultimate"]

    if has_select:

        select = select_table(table_id).stack()
        select.name = "rate"
        select.index.names = ["entry_age", "duration"]
        select = select.reset_index()
        select["att_age"] = select["entry_age"] + select["duration"]
        select = select.set_index(["att_age", "duration"])["rate"]

    if has_ultimate:

        ultimate = ultimate_tables()[[table_id]].copy()
        ultimate["duration"] = select_duration_len()[table_id]
        ultimate = ultimate.set_index("duration", append=True)[table_id]


    if has_select and has_ultimate:
        return pd.concat([select, ultimate])

    elif has_select and not has_ultimate:
        return select

    elif not has_select and has_ultimate:
        return ultimate

    else:
        raise ValueError(f"Table {table_id} neither has select nor ultimate")


def mort_file():
    """Mortality table file"""
    dir_ = base_data.const_params().at["table_dir", "value"]
    file = base_data.const_params().at["mort_file", "value"]

    return _model.path.parent / dir_ / file


def select_duration_len():
    """Selection period length"""
    ids = table_defs().index
    dur_len = []
    for id_ in ids:
        if table_defs().at[id_, "has_select"]:
            dur_len.append(len(select_table(id_).columns))
        else:
            dur_len.append(0)  # 0 for ultimate only

    return pd.Series(dur_len, index=ids)


def select_table(table_id: str):
    """Reads a select mortality table with the given table ID"""
    df = pd.read_excel(
        mort_file(),
        sheet_name=table_id,
        index_col=0)
    df.columns = range(len(df.columns))
    return df


def table_defs():
    """Table definitions"""
    df = pd.read_excel(
        mort_file(), 
        sheet_name="TableDefs",
        index_col=0)

    return df.loc[df["is_used"] == True]


def table_last_age():
    """Mortality table last age"""
    return unified_table().index.to_frame(index=False).groupby("table_id")["att_age"].max()


def ultimate_tables():
    """Reads the ultimate mortality tables"""
    df = pd.read_excel(
        mort_file(),
        sheet_name="Ultimate",
        index_col=0)
    df.index.name = "att_age"
    return df


def unified_table():
    """Unified mortality table"""
    return pd.concat(
        {id_: merged_table(id_) for id_ in table_defs().index},
        names=["table_id"]
        )


# ---------------------------------------------------------------------------
# References

base_data = ("Interface", ("..", "BaseData"), "auto")