"""Shared fixtures for the reference-model tests.

The registry these fixtures read — :data:`MODELS`, :data:`LIB` and :func:`model_path` —
lives in :mod:`us_registry` rather than here, and the test modules import it from there.
``conftest.py`` is a name pytest fixes, so with two in-library suites in one run the two
files collide in ``sys.modules`` and each suite can end up locating the *other* library's
models.  See :mod:`us_registry` for the full account.
"""
import modelx as mx
import pytest

from us_registry import LIB, ANNUAL, MONTHLY, MODELS, model_path  # noqa: F401


@pytest.fixture(scope="module")
def term_life():
    """The Term_US_A model, closed after the module finishes."""
    model = mx.read_model(model_path("Term_US_A"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(term_life):
    """Model point 1 — the worked-example anchor cell."""
    return term_life.Projection[1]
