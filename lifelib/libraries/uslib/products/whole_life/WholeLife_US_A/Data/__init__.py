# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.WholeLife_US_A.Projection` as ``data``. :mod:`~.WholeLife_US_A.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/whole_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WholeLife_US_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
cv_file                 cv_table()                  cv_table.csv
nsp_file                nsp_table()                 nsp_table.csv
np_guar_file            np_guar_table()             np_guar_table.csv
mort_table_file         mort_table()                mort_table.csv
premium_rates_file      premium_rates()             premium_rates.csv
======================  ==========================  ==============================

The four guarantee-basis tables belong together. ``mort_table.csv`` holds the
guaranteed mortality ``q^g``, ``nsp_table.csv`` the endowment-at-100 net single
premiums that price paid-up additions, ``np_guar_table.csv`` the nonforfeiture net
level premium that the dividend's interest margin is credited on, and ``cv_table.csv``
the guaranteed cash value schedule. The technical notes' first "known modeling
pitfall" is exactly a mismatch between them, and it prescribes regenerating all four
from one 2017 CSO / 4% source.

**The shipped four are not one construction, and no set carrying the worked example's
anchors could be.** On a single mortality basis at 4% the notes' own definition
collapses to ``NNLP = 1000 d NSP_45 / (1 - NSP_45)``, so the worked example's
``NNLP = 13.00`` forces ``NSP_45 = 0.252616`` and hence ``NSP_55 <= 0.252616 x 1.04^10
= 0.373933`` — short of the worked example's ``NSP_55 = 0.42``, whatever mortality is
assumed. Each shipped table is therefore pinned to its own worked-example anchor
independently: ``q^g_54 = 0.00320``, ``NSP_55 = 0.42``, ``NP_g = 13.00``,
``CV_9 = 95.00`` and ``CV_10 = 112.00``. Reconciling ``nsp_table.csv`` with
``mort_table.csv`` would need a guarantee interest rate falling from 5.99% at age 45
to 0.02% at age 99. The model README and the ``Projection`` docstring carry the
arithmetic; a test pins the mismatch by age so it cannot quietly close.

What *is* guaranteed, because the two consequences the pitfall names would otherwise
bite, is the pair of endpoints: ``nsp = 1.000000`` at attained age 100, so the
paid-up-additions cash value reaches paid-up-additions face at maturity, and
``cv_per_1000 = 1000.00`` in the final policy year, so the base block endows at face.
Both are asserted by the tests. Every rate is also **sex-distinct**, as the notes
require — including the pay-to-100 cash value schedule.

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name, then clear the cache. No
formula changes — but regenerate ``nsp_table.csv``, ``np_guar_table.csv`` and
``cv_table.csv`` from the same basis, or the pitfall above is exactly what happens.
Doing so is the only way to satisfy the notes' one-basis instruction, and it will stop
the worked example reproducing.
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def input_dir():
    """The directory holding the input CSVs: the model folder's parent.

    Inputs are *external* files, not data stored inside the model, so the model
    folder is pure formulas.  The path is resolved at run time from where the model
    was read, following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*."""
    return pd.read_csv(input_dir() / model_point_file, index_col="point_id")  # noqa: F821


def cv_table():
    """The guaranteed cash value schedule per $1,000 of face, from *cv_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / cv_file,                                       # noqa: F821
        index_col=["premium_period", "sex", "issue_age", "policy_year"])


def nsp_table():
    """The endowment-at-100 net single premiums by attained age, from *nsp_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / nsp_file, index_col=["sex", "age"])            # noqa: F821


def np_guar_table():
    """The nonforfeiture net level premiums per $1,000, from *np_guar_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / np_guar_file,                                  # noqa: F821
        index_col=["premium_period", "sex", "issue_age"])


def mort_table():
    """The guaranteed mortality table by sex and age, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"])     # noqa: F821


def premium_rates():
    """The final-expense premium rates per $1,000, read from *premium_rates.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / premium_rates_file,                            # noqa: F821
        index_col=["product", "sex", "risk_class", "issue_age"])


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

cv_file = "cv_table.csv"

nsp_file = "nsp_table.csv"

np_guar_file = "np_guar_table.csv"

mort_table_file = "mort_table.csv"

premium_rates_file = "premium_rates.csv"

pd = ("Module", "pandas")