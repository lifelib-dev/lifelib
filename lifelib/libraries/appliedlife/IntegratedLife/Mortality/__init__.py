"""Mortality tables

The Mortality space reads mortality tables from a mortality file
and creates a unified mortality table as a pandas Series
indexed with Table ID, Attained Age and Duration.

This space is referenced as :attr:`~appliedlife.IntegratedLife.ProductBase.mort_data`
in the :mod:`~appliedlife.IntegratedLife.ProductBase` space.

Attributes:

    base_data: Reference to the :mod:`~appliedlife.IntegratedLife.BaseData` space

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
        names = ["table_id"]
        )


# ---------------------------------------------------------------------------
# References

base_data = ("Interface", ("..", "BaseData"), "auto")