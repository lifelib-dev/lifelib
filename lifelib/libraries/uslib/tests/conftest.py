"""Shared fixtures for the reference-model tests, and the suite's three pytest markers.

The registry these fixtures read — :data:`MODELS`, :data:`LIB` and :func:`model_path` —
lives in :mod:`us_registry` rather than here, and the test modules import it from there.
``conftest.py`` is a name pytest fixes, so with two in-library suites in one run the two
files collide in ``sys.modules`` and each suite can end up locating the *other* library's
models.  See :mod:`us_registry` for the full account.

The ``cython`` marker is registered here rather than in a root ``pytest.ini`` because the
suite ships inside the library, and a copy made by ``lifelib.create()`` carries this file
but no configuration from above it.  The marker is what ``pytest -m cython`` selects the
compile tests by (USLIB-SEC-PLAN.md D13), and registering it keeps them free of pytest's
unknown-mark warning.  The tests themselves skip when modelx-cython or a C compiler is
absent, so a bare ``pytest`` stays green on a machine that has neither.  The ``cython`` CI
job, which installs both, sets ``USLIB_REQUIRE_CYTHON=1``, and there such a skip fails.
That job runs one shard of the compile tests to a leg, named by ``USLIB_CYTHON_SHARD``:
``toolchain``, or the product directory of an SEC model at stage ``"EC"``, whose shard
holds its product module's compile tests and its cases of ``test_compiled_conventions.py``,
so that the model compiles once a leg (D13).  :func:`pytest_collection_modifyitems`
deselects the compile tests outside the shard, by ``sec_support.cython_shard``, and fails a
shard that selects none under ``USLIB_REQUIRE_CYTHON=1``.  Unset, it deselects nothing.

The ``sec_full`` marker is registered here for the same reason.  It marks the cases of an
SEC model's full splice grid beyond the core that runs by default, which skip, with the
reason shown, unless ``USLIB_SEC_FULL=1`` is set (USLIB-SEC-PLAN.md K6), and
``pytest -m sec_full`` selects them.  CI's ``sec`` job sets it on its Linux legs, one
module to a leg, so they run in every CI run, and the ``cython`` job on its Linux leg,
where the compiled grids run at full size.

The ``docutils`` marker is registered here for the same reason.  It marks the tests that
read a model's docstrings through docutils as the docs build does, which skip where
docutils is absent: it is not a requirement of the models, and lifelib's CI does not
install it.  The CI legs that run the full grids install it and set
``USLIB_REQUIRE_DOCUTILS=1``, under which such a skip fails, as ``USLIB_REQUIRE_CYTHON=1``
fails a compile test's (USLIB-SEC-PLAN.md §5.4).
"""
import modelx as mx
import pytest

from us_registry import LIB, ANNUAL, MONTHLY, MODELS, model_path  # noqa: F401


def pytest_configure(config):
    """Register the ``cython`` marker the compile tests carry, ``sec_full`` and
    ``docutils``."""
    config.addinivalue_line(
        "markers",
        "cython: compiles a model with modelx-cython; skips without modelx-cython or a C "
        "compiler")
    config.addinivalue_line(
        "markers",
        "sec_full: a case of an SEC model's full splice grid; skips unless "
        "USLIB_SEC_FULL=1")
    config.addinivalue_line(
        "markers",
        "docutils: parses docstrings with docutils; skips where docutils is absent")


@pytest.fixture(scope="module")
def term_life():
    """The Term_US_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Term_US_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(term_life):
    """Model point 1 — the worked-example anchor cell."""
    return term_life.Projection[1]


@pytest.fixture(scope="session")
def sec_build(tmp_path_factory):
    """The SEC models compiled in this session: ``sec_build(name)`` is ``name``'s build.

    Each model is compiled once per session, into a temporary directory, never into the
    tree (USLIB-SEC-PLAN.md D12), and only when a compile test asks for it, so a session
    that selects none compiles nothing.  Without modelx-cython or a compiler the asking
    test skips, or fails under ``USLIB_REQUIRE_CYTHON=1`` (``sec_support.require_cython``).
    """
    from sec_support import SecBuilds
    return SecBuilds(tmp_path_factory)


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    """Under ``USLIB_CYTHON_SHARD``, deselect this suite's ``cython`` tests outside that
    shard.

    The shards are ``sec_support.cython_shards``, read from the registry, and a test's is
    ``sec_support.cython_shard``; a name that is no shard is a usage error, which lists
    them.  Run last, after ``-m`` has deselected, so that what is left is what the session
    runs: under ``USLIB_REQUIRE_CYTHON=1``, a shard left with no compile test is an error
    too, as a run that selects no test is (D13), and not a green leg that compiled nothing.
    Tests without the marker are left to ``-m``, and other suites' tests are not touched.
    """
    import os
    import pathlib
    shard = os.environ.get("USLIB_CYTHON_SHARD", "")
    if not shard:
        return
    from sec_support import cython_shard, cython_shards
    shards = cython_shards()
    if shard not in shards:
        raise pytest.UsageError(f"USLIB_CYTHON_SHARD={shard!r} is no shard; the shards are "
                                f"{', '.join(shards)}")
    here = pathlib.Path(__file__).resolve().parent
    kept, dropped = [], []
    for item in items:
        ours = (item.get_closest_marker("cython") is not None
                and item.path.resolve().parent == here)
        (dropped if ours and cython_shard(item, shards) != shard else kept).append(item)
    if dropped:
        config.hook.pytest_deselected(items=dropped)
        items[:] = kept
    if (os.environ.get("USLIB_REQUIRE_CYTHON") == "1"
            and not any(item.get_closest_marker("cython") is not None for item in kept)):
        raise pytest.UsageError(f"USLIB_REQUIRE_CYTHON=1, and USLIB_CYTHON_SHARD={shard!r} "
                                f"selects no compile test")


# Each marker whose skip a CI job forbids, with the variable that forbids it.
REQUIRED = (("cython", "USLIB_REQUIRE_CYTHON"), ("docutils", "USLIB_REQUIRE_DOCUTILS"))


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Under ``USLIB_REQUIRE_CYTHON=1``, report a ``cython`` test that skips as failed, and
    under ``USLIB_REQUIRE_DOCUTILS=1`` a ``docutils`` test.

    ``sec_support.require_cython`` fails a compile test that finds the toolchain missing,
    but a test can skip before its body runs: one parametrized over the SEC models at
    stage ``"EC"`` skips, "got empty parameter set", when the registry holds none.  In the
    ``cython`` CI job any such skip is a green run that compiled nothing (D13), so it is
    turned into a failure here, whatever skipped it.  A docstring parse test skips where
    docutils is absent, and on the CI leg that installs docutils such a skip is a green
    run that parsed nothing, so it fails there the same way.
    """
    import os
    report = yield
    if report.skipped and not hasattr(report, "wasxfail"):
        for marker, variable in REQUIRED:
            if (item.get_closest_marker(marker) is not None
                    and os.environ.get(variable) == "1"):
                given = report.longrepr
                reason = given[-1] if isinstance(given, tuple) else given
                report.outcome = "failed"
                report.longrepr = f"{variable}=1 forbids a skip, and it skipped: {reason}"
                break
    return report
