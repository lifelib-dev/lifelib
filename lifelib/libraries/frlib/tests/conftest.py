"""Shared fixtures for the reference-model tests.

The registry these fixtures read — :data:`MODELS`, :data:`LIB` and :func:`model_path` —
lives in :mod:`fr_registry` rather than here, and the test modules import it from there.
``conftest.py`` is a name pytest fixes, so with four in-library suites in one run the
files collide in ``sys.modules`` and each suite can end up locating another library's
models. See :mod:`fr_registry` for the full account.

Each product has two fixtures: the model, read once per module and closed after it, and
an **anchor** — the ItemSpace holding the model point that reproduces that product's
worked example. The anchor is ``Projection[1]`` everywhere except where the notes'
example is a second scenario, and the docstring says which model point it is so a reader
can find the row in ``model_point_table.csv``.
"""
import modelx as mx
import pytest

from fr_registry import LIB, ANNUAL, MONTHLY, MODELS, model_path  # noqa: F401


# ---------------------------------------------------------------------------
# Épargne


@pytest.fixture(scope="module")
def assurance_vie_euro():
    """The Euro_FR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Euro_FR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def fr_euro_anchor(assurance_vie_euro):
    """Model point 1 — the fonds en euros worked-example anchor cell."""
    return assurance_vie_euro.Projection[1]


@pytest.fixture(scope="module")
def assurance_vie_uc():
    """The UC_FR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("UC_FR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def fr_uc_anchor(assurance_vie_uc):
    """Model point 1 — the unités de compte worked-example anchor cell."""
    return assurance_vie_uc.Projection[1]


@pytest.fixture(scope="module")
def eurocroissance():
    """The EC_FR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("EC_FR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def fr_ec_anchor(eurocroissance):
    """Model point 1 — the eurocroissance worked-example anchor cell."""
    return eurocroissance.Projection[1]


# ---------------------------------------------------------------------------
# Retraite


@pytest.fixture(scope="module")
def per_assurance():
    """The PER_FR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("PER_FR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def fr_per_anchor(per_assurance):
    """Model point 1 — the PER worked-example anchor cell."""
    return per_assurance.Projection[1]


@pytest.fixture(scope="module")
def rente_viagere():
    """The Rente_FR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Rente_FR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def fr_rente_anchor(rente_viagere):
    """Model point 1 — the rente viagère worked-example anchor cell."""
    return rente_viagere.Projection[1]


# ---------------------------------------------------------------------------
# Prévoyance


@pytest.fixture(scope="module")
def temporaire_deces():
    """The TD_FR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("TD_FR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def fr_td_anchor(temporaire_deces):
    """Model point 1 — the temporaire décès worked-example anchor cell."""
    return temporaire_deces.Projection[1]


@pytest.fixture(scope="module")
def assurance_emprunteur():
    """The ADE_FR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("ADE_FR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def fr_ade_anchor(assurance_emprunteur):
    """Model point 1 — the assurance emprunteur worked-example anchor cell."""
    return assurance_emprunteur.Projection[1]


@pytest.fixture(scope="module")
def obseques():
    """The Obseques_FR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Obseques_FR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def fr_obseques_anchor(obseques):
    """Model point 1 — the contrat obsèques worked-example anchor cell."""
    return obseques.Projection[1]


@pytest.fixture(scope="module")
def dependance():
    """The Dep_FR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Dep_FR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def fr_dep_anchor(dependance):
    """Model point 1 — the dépendance worked-example anchor cell."""
    return dependance.Projection[1]
