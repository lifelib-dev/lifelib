"""Shared fixtures for the reference-model tests.

The registry these fixtures read — :data:`MODELS`, :data:`LIB` and :func:`model_path` —
lives in :mod:`de_registry` rather than here, and the test modules import it from there.
``conftest.py`` is a name pytest fixes, so with five in-library suites in one run the
files collide in ``sys.modules`` and each suite can end up locating another library's
models. See :mod:`de_registry` for the full account.

Each product has two fixtures: the model, read once per module and closed after it, and
an **anchor** — the ItemSpace holding the model point that reproduces that product's
worked example. The anchor is ``Projection[1]`` everywhere, and the docstring says which
model point it is so a reader can find the row in ``model_point_table.csv``.
"""
import modelx as mx
import pytest

from de_registry import LIB, ANNUAL, MONTHLY, MODELS, model_path  # noqa: F401


# ---------------------------------------------------------------------------
# Kapitalbildende Lebensversicherung und private Rentenversicherung (Schicht 3)


@pytest.fixture(scope="module")
def kapitallebensversicherung():
    """The KLV_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("KLV_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_klv_anchor(kapitallebensversicherung):
    """Model point 1 — the Kapitallebensversicherung worked-example anchor cell."""
    return kapitallebensversicherung.Projection[1]


@pytest.fixture(scope="module")
def klassische_rentenversicherung():
    """The RV_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("RV_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_rv_anchor(klassische_rentenversicherung):
    """Model point 1 — the klassische Rentenversicherung worked-example anchor cell."""
    return klassische_rentenversicherung.Projection[1]


@pytest.fixture(scope="module")
def fondsgebundene_rentenversicherung():
    """The FRV_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("FRV_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_frv_anchor(fondsgebundene_rentenversicherung):
    """Model point 1 — the fondsgebundene Rentenversicherung worked-example anchor cell."""
    return fondsgebundene_rentenversicherung.Projection[1]


@pytest.fixture(scope="module")
def indexpolice():
    """The Index_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Index_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_index_anchor(indexpolice):
    """Model point 1 — the Indexpolice worked-example anchor cell."""
    return indexpolice.Projection[1]


# ---------------------------------------------------------------------------
# Geförderte Altersvorsorge (Schicht 1 und Schicht 2)


@pytest.fixture(scope="module")
def basisrente():
    """The Basis_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Basis_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_basis_anchor(basisrente):
    """Model point 1 — the Basisrente worked-example anchor cell."""
    return basisrente.Projection[1]


@pytest.fixture(scope="module")
def riester_rente():
    """The Riester_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Riester_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_riester_anchor(riester_rente):
    """Model point 1 — the Riester-Rente worked-example anchor cell."""
    return riester_rente.Projection[1]


# ---------------------------------------------------------------------------
# Rentenbezug


@pytest.fixture(scope="module")
def sofortrente():
    """The Sofort_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Sofort_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_sofort_anchor(sofortrente):
    """Model point 1 — the Sofortrente worked-example anchor cell."""
    return sofortrente.Projection[1]


# ---------------------------------------------------------------------------
# Biometrie


@pytest.fixture(scope="module")
def risikolebensversicherung():
    """The RLV_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("RLV_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_rlv_anchor(risikolebensversicherung):
    """Model point 1 — the Risikolebensversicherung worked-example anchor cell."""
    return risikolebensversicherung.Projection[1]


@pytest.fixture(scope="module")
def berufsunfaehigkeit():
    """The BU_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("BU_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_bu_anchor(berufsunfaehigkeit):
    """Model point 1 — the Berufsunfähigkeitsversicherung worked-example anchor cell."""
    return berufsunfaehigkeit.Projection[1]


@pytest.fixture(scope="module")
def pflegerentenversicherung():
    """The Pflege_DE_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Pflege_DE_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def de_pflege_anchor(pflegerentenversicherung):
    """Model point 1 — the Pflegerentenversicherung worked-example anchor cell."""
    return pflegerentenversicherung.Projection[1]
