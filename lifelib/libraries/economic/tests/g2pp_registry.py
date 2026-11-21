"""Paths and helpers shared by the tests of the G2++ models.

Every path is found from this library's folder, so the tests run on the models next to
them, in lifelib or in a copy made by ``lifelib.create``. The module's name is unique
among lifelib's test folders, because pytest imports the test folders of all libraries
into one session.
"""
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]      # the library folder
INPUT = ROOT / "g2pp_input.xlsx"
MODEL_DIR = ROOT / "BasicG2PP"


def sibling_library_path(*parts):
    """Path of a file or folder in another lifelib library; skip if it is not there.

    In lifelib the libraries are folders next to each other, so the path is found next to
    this library's folder. A copy made by ``lifelib.create`` holds this library alone.
    """
    path = ROOT.parent.joinpath(*parts)
    if not path.exists():
        pytest.skip(f"{path} not found")
    return path


def write_workbook(path, params=None, curve=None, fund=None, drop_params=(), base=INPUT):
    """Write a copy of ``base`` to ``path``.

    ``params`` overrides values in the Params sheet (adding rows if needed) and
    ``drop_params`` removes rows. ``curve`` and ``fund`` replace the Curve and Fund sheets
    with the given DataFrames, which must include their ``maturity`` column.
    """
    sheets = pd.read_excel(base, sheet_name=None)
    if params or drop_params:
        table = sheets["Params"].set_index("parameter").drop(index=list(drop_params))
        for key, value in (params or {}).items():
            table.loc[key, "value"] = value
        sheets["Params"] = table.reset_index()
    if curve is not None:
        sheets["Curve"] = curve
    if fund is not None:
        sheets["Fund"] = fund
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name, index=False)
    return Path(path)
