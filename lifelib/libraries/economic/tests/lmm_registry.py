"""Paths and helpers shared by the tests of the LMM models.

Every path is found from this library's folder, so the tests run on the models next to
them, in lifelib or in a copy made by ``lifelib.create``. The module's name is unique
among lifelib's test folders, because pytest imports the test folders of all libraries
into one session.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]      # the library folder
INPUT = ROOT / "lmm_input.xlsx"
MODEL_DIR = ROOT / "BasicLMM"
G2PP_INPUT = ROOT / "g2pp_input.xlsx"           # shares its Curve and Fund sheets


def write_workbook(path, params=None, curve=None, vol=None, fund=None, drop_params=(),
                   base=INPUT):
    """Write a copy of ``base`` to ``path``.

    ``params`` overrides values in the Params sheet (adding rows if needed) and
    ``drop_params`` removes rows. ``curve``, ``vol`` and ``fund`` replace the Curve, Vol and
    Fund sheets with the given DataFrames, which must include their ``maturity`` column.
    """
    sheets = pd.read_excel(base, sheet_name=None)
    if params or drop_params:
        table = sheets["Params"].set_index("parameter").drop(index=list(drop_params))
        for key, value in (params or {}).items():
            table.loc[key, "value"] = value
        sheets["Params"] = table.reset_index()
    for name, df in (("Curve", curve), ("Vol", vol), ("Fund", fund)):
        if df is not None:
            sheets[name] = df
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name, index=False)
    return Path(path)
