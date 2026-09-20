"""Shared fixtures for the reference-model tests.

The registry these fixtures read — :data:`MODELS`, :data:`LIB` and :func:`model_path` —
lives in :mod:`kr_registry` rather than here, and the test modules import it from there.
``conftest.py`` is a name pytest fixes, so with six in-library suites in one run the
files collide in ``sys.modules`` and each suite can end up locating another library's
models. See :mod:`kr_registry` for the full account.

Each product has two fixtures: the model, read once per module and closed after it, and
an **anchor** — the ItemSpace holding the model point that reproduces that product's
worked example. The anchor is ``Projection[1]`` everywhere, and by library convention
model point 1 is the row the technical notes project, so a reader can find it in
``model_point_table.csv`` without being told which.

A test module needing a second model point takes it from the model fixture inside its own
module (``term_life.Projection[4]``) rather than adding a fixture here, so that the
fixture list stays one line of thought per model.
"""
import modelx as mx
import pytest

from kr_registry import LIB, ANNUAL, MONTHLY, BOHEOM, MAN, MODELS, model_path  # noqa: F401


# ---------------------------------------------------------------------------
# 보장성 — protection


@pytest.fixture(scope="module")
def whole_life():
    """The WholeLife_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("WholeLife_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_whole_life_anchor(whole_life):
    """Model point 1 — the 종신보험 (whole life) worked-example anchor cell."""
    return whole_life.Projection[1]


@pytest.fixture(scope="module")
def term_life():
    """The Term_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Term_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_term_anchor(term_life):
    """Model point 1 — the 정기보험 (term life) worked-example anchor cell."""
    return term_life.Projection[1]


@pytest.fixture(scope="module")
def ci_insurance():
    """The CI_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("CI_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_ci_anchor(ci_insurance):
    """Model point 1 — the CI보험 (critical illness) worked-example anchor cell."""
    return ci_insurance.Projection[1]


# ---------------------------------------------------------------------------
# 제3보험 — third insurance (보험업법 제4조제1항제3호)


@pytest.fixture(scope="module")
def indemnity_medical():
    """The Medical_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Medical_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_medical_anchor(indemnity_medical):
    """Model point 1 — the 실손의료보험 (indemnity medical) worked-example anchor cell."""
    return indemnity_medical.Projection[1]


@pytest.fixture(scope="module")
def cancer():
    """The Cancer_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Cancer_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_cancer_anchor(cancer):
    """Model point 1 — the 암보험 (cancer) worked-example anchor cell."""
    return cancer.Projection[1]


@pytest.fixture(scope="module")
def long_term_care():
    """The LTC_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("LTC_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_ltc_anchor(long_term_care):
    """Model point 1 — the 간병보험 (long-term care) worked-example anchor cell."""
    return long_term_care.Projection[1]


@pytest.fixture(scope="module")
def child():
    """The Child_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Child_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_child_anchor(child):
    """Model point 1 — the 어린이보험 (children's insurance) worked-example anchor cell."""
    return child.Projection[1]


# ---------------------------------------------------------------------------
# 저축·연금 — savings and annuity


@pytest.fixture(scope="module")
def pension_savings():
    """The Pension_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Pension_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_pension_anchor(pension_savings):
    """Model point 1 — the 연금저축보험 (tax-qualified pension savings) worked-example anchor cell."""
    return pension_savings.Projection[1]


@pytest.fixture(scope="module")
def variable_annuity():
    """The VA_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("VA_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_va_anchor(variable_annuity):
    """Model point 1 — the 변액연금보험 (variable annuity) worked-example anchor cell."""
    return variable_annuity.Projection[1]


@pytest.fixture(scope="module")
def immediate_annuity():
    """The Immediate_KR_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Immediate_KR_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def kr_immediate_anchor(immediate_annuity):
    """Model point 1 — the 즉시연금 (immediate annuity) worked-example anchor cell."""
    return immediate_annuity.Projection[1]
