import uuid

import pytest

from g2pp_registry import MODEL_DIR, write_workbook


@pytest.fixture
def workbook(tmp_path):
    """Factory: ``workbook(params=..., curve=..., fund=...)`` writes a modified input copy."""
    def make(**kwargs):
        return write_workbook(tmp_path / f"input_{uuid.uuid4().hex[:8]}.xlsx", **kwargs)
    return make


@pytest.fixture
def model():
    """A fresh copy of BasicG2PP read from disk, closed after the test."""
    import modelx as mx
    if not (MODEL_DIR / "__init__.py").exists():
        pytest.skip("BasicG2PP has not been built; run scripts/build_model.py")
    m = mx.read_model(MODEL_DIR, name=f"BasicG2PP_{uuid.uuid4().hex[:8]}")
    yield m
    m.close()
