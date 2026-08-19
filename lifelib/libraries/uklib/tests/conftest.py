"""Shared fixtures for the reference-model tests.

The registry these fixtures read — :data:`MODELS`, :data:`LIB` and :func:`model_path` —
lives in :mod:`uk_registry` rather than here, and the test modules import it from there.
``conftest.py`` is a name pytest fixes, so with two in-library suites in one run the two
files collide in ``sys.modules`` and each suite can end up locating the *other* library's
models.  See :mod:`uk_registry` for the full account.
"""
import modelx as mx
import pytest

from uk_registry import LIB, ANNUAL, MONTHLY, MODELS, model_path  # noqa: F401


@pytest.fixture(scope="module")
def term_assurance():
    """The Term_UK_A model, closed after the module finishes."""
    model = mx.read_model(model_path("Term_UK_A"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_term_anchor(term_assurance):
    """Model point 1 — the UK term worked-example anchor cell."""
    return term_assurance.Projection[1]


@pytest.fixture(scope="module")
def critical_illness():
    """The CI_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("CI_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_ci_anchor(critical_illness):
    """Model point 1 — the UK critical illness worked-example anchor cell."""
    return critical_illness.Projection[1]


@pytest.fixture(scope="module")
def income_protection():
    """The IP_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("IP_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_ip_claim(income_protection):
    """Model point 2 — the claims-in-payment cell the worked example computes."""
    return income_protection.Projection[2]


@pytest.fixture(scope="module")
def whole_of_life():
    """The WOL_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("WOL_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_o50_anchor(whole_of_life):
    """Model point 1 — the over-50s worked-example anchor cell."""
    return whole_of_life.Projection[1]


@pytest.fixture(scope="module")
def unit_linked_bond():
    """The ULB_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("ULB_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_bond_anchor(unit_linked_bond):
    """Model point 1 — the unit-linked bond worked-example anchor cell."""
    return unit_linked_bond.Projection[1]


@pytest.fixture(scope="module")
def with_profits():
    """The WP_UK_A model, closed after the module finishes."""
    model = mx.read_model(model_path("WP_UK_A"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_wp_up(with_profits):
    """Model point 1 — the worked example's scenario A, the up market."""
    return with_profits.Projection[1]


@pytest.fixture(scope="module")
def uk_wp_down(with_profits):
    """Model point 2 — the worked example's scenario B, the down market."""
    return with_profits.Projection[2]


@pytest.fixture(scope="module")
def pension_annuity():
    """The PA_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("PA_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_pa_scenario(pension_annuity):
    """Model point 1 — the worked example's scenario configuration."""
    return pension_annuity.Projection[1]
