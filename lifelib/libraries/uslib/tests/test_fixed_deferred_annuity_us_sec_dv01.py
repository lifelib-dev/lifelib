"""Tests for the key-rate DV01 and CS01 model on MYGA_US_SEC (``dv01_sec``).

The model (``products/fixed_deferred_annuity/dv01-sec.md``) values MYGA_US_SEC's shipped book on
ESG path 1 at the closes before years 0, 1 and 2, on the base curve and on twelve key-rate
curves, and reports DV01 and CS01 by tenor.  These tests hold:

* its shape: the six Spaces, the key tenors read from ``dv01_sec/shock_steps.csv``, and
  ``Valuation``'s opening state read from ``Actual`` through the dynamic Reference ``act``;
* the live report: every value of the annual risk report of the shipped book, computed by live
  modelx (``report.live_report``), against the values stored below, which live modelx computed
  when the example was added (rel 1e-10, abs 1e-7);
* the compiled report: the model compiled with modelx-cython (``compiled.build``) and run by
  the pooled driver (``report.pooled_report``) with 1 and with 4 worker threads, each run in a
  fresh process, equal to the live report under the same rule.
* the report through collect (``report.collect_report``): at 1 and 4 workers, equal to the
  pooled driver's and the live report within the financial tolerance.

The live report takes about five minutes, and the build about ten more.  The compile test
carries the ``cython`` marker and skips where modelx-cython or a C compiler is missing, or
fails there under ``USLIB_REQUIRE_CYTHON=1``, as the other compile tests do.  It builds into a
temporary directory, never into the library tree.

The stored values change when an input of the shipped book, MYGA_US_SEC's formulas, the ESG
or ``shock_steps.csv`` changes; recompute them with ``run_dv01_sec.py --json FILE``.
"""
import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import sys
import sysconfig

import numpy as np
import pytest

from us_registry import LIB

PRODUCT = LIB / "products" / "fixed_deferred_annuity"
RUNNER = PRODUCT / "run_dv01_sec.py"

# The live report of the shipped book: rows are years 0, 1 and 2 of ESG path 1, columns the
# tenors of shock_steps.csv, 12 to 240 months.
DV01_REFERENCE = (
    (-8.43098716228269, 21.521828251541592, 36.71257068763953, 39.67790248431265,
     324.75250390998553, 65.45434888964519, 22.401301257312298, 2.058943287935108,
     22.062096946290694, -33.94369110907428, -2.043238228885457, -0.20700253639370203),
    (12.833560524974018, 23.898503485601395, 28.84542393567972, 280.8804656902794,
     58.0029328733217, 20.254145157057792, 1.9989717004355043, 20.98916609818116,
     -37.50060140690766, 5.188528460683301, -2.3989491215907037, -0.2554631179664284),
    (15.218698239186779, 20.447505777236074, 220.70784570695832, 47.90304337115958,
     17.20208293176256, 1.915703333215788, 19.512869189493358, -34.89363002940081,
     7.882908186176792, -4.062651688233018, -1.4331870477180928, -0.14656282705254853),
)
CS01_REFERENCE = (
    (-4.890361480298452, 11.559763772995211, 43.69134375650901, 33.444227660424076,
     221.32763326040003, 142.3166581603, 34.56829521479085, 6.854612762108445,
     6.991618853178807, 56.128497480764054, 19.14607190573588, 22.965336605207995),
    (6.719316608039662, 29.58320810785517, 26.55523082613945, 189.8316373799462,
     124.78645564289764, 31.57470792112872, 6.287738252198324, 6.571495705051348,
     32.76378942327574, 28.289326773257926, 13.560474026715383, 21.341632792260498),
    (17.88292159815319, 18.990576395299286, 151.67882004240528, 102.53787482297048,
     27.02947220345959, 5.565868192585185, 6.004346717847511, 30.361646122764796,
     19.312465051189065, 10.604742059484124, 10.95666243461892, 19.829217057907954),
)
DV01_TOTAL, CS01_TOTAL = 1213.0078861005604, 1532.7233241095673

TENORS = [12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 180, 240]
RTOL, ATOL = 1e-10, 1e-7


def _close(got, want):
    got, want = np.asarray(got, float), np.asarray(want, float)
    assert got.shape == want.shape
    return np.abs(got - want) <= np.maximum(ATOL, RTOL * np.abs(want))


@pytest.fixture(scope="module")
def dv01_model():
    sys.setrecursionlimit(20_000)
    from lifelib.libraries.uslib.products.fixed_deferred_annuity.dv01_sec import build_model
    model = build_model(model_name="MYGASECDV01_test")
    yield model
    model.close()


@pytest.fixture(scope="module")
def live(dv01_model):
    from lifelib.libraries.uslib.products.fixed_deferred_annuity.dv01_sec import report
    return report.live_report(dv01_model, 1, 2)


def test_the_model_has_six_spaces(dv01_model):
    assert set(dv01_model.spaces) == {"Data", "ESG", "Market", "Actual", "Valuation", "Outer"}


def test_key_tenors_come_from_shock_steps(dv01_model):
    assert dv01_model.Data.shock_key_months() == TENORS


def test_the_book_is_the_shipped_table(dv01_model):
    assert len(dv01_model.Valuation.point_indices()) == 14


def test_valuation_opens_from_actual_through_act(dv01_model):
    """A Valuation item's ``act`` is the Actual item of its policy and path, and its opening
    account value is Actual's entering the month after the close."""
    item = dv01_model.Valuation[11, 7, 1, -1]
    assert item.act is dv01_model.Actual[7, 1]
    assert item.av_pp_init() == dv01_model.Actual[7, 1].av_pp_open(12)
    del dv01_model.Valuation[11, 7, 1, -1]


@pytest.mark.parametrize("args", [(-1, 1), (601, 1), (0, 0), (0, 1001), (0, 1, 12),
                                  (0, 1, -2), (True, 1)])
def test_market_refuses_a_key_outside_the_grid(dv01_model, args):
    """The Space formula raises ValueError, which modelx reports inside its FormulaError."""
    with pytest.raises(Exception) as raised:
        dv01_model.Market(*args)
    assert "ValueError" in str(raised.value)


def test_the_collect_route_reads_openings_through_actual_collect(dv01_model):
    """With ``collect_history`` a Valuation item's ``act`` is its policy's record of
    ``Actual.collect``: the same opening as the Actual item, with no Actual ItemSpace kept.

    It runs after the Market tests: collecting the book creates Market items, and Market(True, 1)
    would then find the item Market(1, 1) instead of raising."""
    expected = dv01_model.Actual[7, 1].av_pp_open(12)
    del dv01_model.Actual[7, 1]
    dv01_model.Valuation.collect_history = True
    try:
        item = dv01_model.Valuation[11, 7, 1, -1]
        assert item.act is dv01_model.Actual.collect(1).individual[7]
        assert item.av_pp_init() == expected
        assert len(dv01_model.Actual.itemspaces) == 0
        del dv01_model.Valuation[11, 7, 1, -1]
    finally:
        dv01_model.Valuation.collect_history = False


def test_live_report_equals_the_stored_values(live):
    dv01, cs01 = live
    assert list(dv01.columns) == TENORS and list(cs01.columns) == TENORS
    assert list(dv01.index) == [(1, 0), (1, 1), (1, 2)]
    assert _close(dv01.to_numpy(), DV01_REFERENCE).all()
    assert _close(cs01.to_numpy(), CS01_REFERENCE).all()
    assert _close(dv01.to_numpy().sum(), DV01_TOTAL) and _close(cs01.to_numpy().sum(), CS01_TOTAL)


def _cython_missing():
    if importlib.util.find_spec("modelx_cython") is None:
        return "modelx-cython is not installed"
    if os.name == "posix":
        command = os.environ.get("CC") or sysconfig.get_config_var("CC") or "cc"
        if shutil.which((shlex.split(command) or ["cc"])[0]) is None:
            return f"no C compiler: setuptools would run {command!r}"
    return None


@pytest.fixture(scope="module")
def dv01_build(tmp_path_factory):
    missing = _cython_missing()
    if missing is not None:
        if os.environ.get("USLIB_REQUIRE_CYTHON") == "1":
            pytest.fail(f"USLIB_REQUIRE_CYTHON=1 forbids a skip, and {missing}")
        pytest.skip(missing)
    from lifelib.libraries.uslib.products.fixed_deferred_annuity.dv01_sec import compiled
    folder = tmp_path_factory.mktemp("dv01_sec_build")
    compiled.build(folder)
    return folder


@pytest.mark.cython
@pytest.mark.parametrize("workers", [1, 4])
def test_compiled_report_equals_live(dv01_build, live, workers):
    """The compiled model, run by the pooled driver in a fresh process, equals live modelx."""
    done = subprocess.run([sys.executable, str(RUNNER), "--run", str(dv01_build),
                           "--workers", str(workers)], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr[-3000:]
    result = json.loads(done.stdout.strip().splitlines()[-1])
    assert result["workers"] == workers and result["policies"] == 14
    dv01, cs01 = live
    assert _close(result["dv01"], dv01.to_numpy()).all()
    assert _close(result["cs01"], cs01.to_numpy()).all()


@pytest.mark.cython
@pytest.mark.parametrize("workers", [1, 4])
def test_compiled_collect_equals_direct_and_live(dv01_build, live, workers):
    """The Collect and pooled reports agree with live within the financial tolerance."""
    results = {}
    for route in ("direct", "collect"):
        command = [sys.executable, str(RUNNER), "--run", str(dv01_build), "--workers", str(workers)]
        done = subprocess.run(command + (["--collect"] if route == "collect" else []),
                              capture_output=True, text=True)
        assert done.returncode == 0, done.stderr[-3000:]
        results[route] = json.loads(done.stdout.strip().splitlines()[-1])
    assert _close(results["collect"]["dv01"], results["direct"]["dv01"]).all()
    assert _close(results["collect"]["cs01"], results["direct"]["cs01"]).all()
    dv01, cs01 = live
    assert _close(results["collect"]["dv01"], dv01.to_numpy()).all()
    assert _close(results["collect"]["cs01"], cs01.to_numpy()).all()
