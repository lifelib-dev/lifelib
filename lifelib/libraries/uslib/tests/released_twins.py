"""Use the released S model text for the upstream SEC assertions."""

import atexit
from functools import cache
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

import modelx as mx

from us_registry import is_sec, model_path


@cache
def _workspace():
    directory = TemporaryDirectory(prefix="uslib-sec-")
    atexit.register(directory.cleanup)
    return Path(directory.name)


@cache
def sec_test_model_path(name):
    """Resolve SEC models in place and materialize their released S twins.

    The saved S models locate their CSVs beside the model folder. Put the
    released formulas and the product's shipped CSVs together in a temporary
    directory, where tests can also copy them to create edited inputs.
    """
    shipped = model_path(name)
    if is_sec(name):
        return shipped

    source = Path(__file__).resolve().with_name("_released") / name
    product_dir = _workspace() / shipped.parent.name
    twin = product_dir / name
    shutil.copytree(source, twin, ignore=shutil.ignore_patterns("__pycache__"))
    for csv in shipped.parent.glob("*.csv"):
        shutil.copyfile(csv, product_dir / csv.name)
    return twin


def read_released_twin(name, *, model_name):
    """Read a released S twin against the same live input files as its SEC model."""
    source = Path(__file__).resolve().with_name("_released") / name
    model = mx.read_model(source, name=model_name)
    model.Data.input_dir[()] = model_path(name).parent
    return model
