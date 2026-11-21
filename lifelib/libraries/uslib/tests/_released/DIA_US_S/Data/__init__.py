# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.DIA_US_S.Projection` as ``data``.
:mod:`~.DIA_US_S.Projection` is parameterized by ``point_id``, so each
``Projection[N]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file. Holding them in an unparameterized
Space reads each file once no matter how many contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/deferred_income_annuity/``, rather than data stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``DIA_US_S`` folder without its parent's CSVs produces a model that reads
and then fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

========================  ==============================  ==========================
Reference                 Cells                           File
========================  ==============================  ==========================
model_point_file          model_point_table()             model_point_table.csv
premium_schedule_file     premium_schedule_table()        premium_schedule.csv
mort_table_file           mort_table()                    mort_table.csv
improvement_scale_file    improvement_scale()             improvement_scale.csv
payout_factor_file        payout_factor_table()           payout_factor_table.csv
rop_factor_file           rop_factor_table()              rop_factor_table.csv
========================  ==============================  ==========================

**Why the premium schedule is a separate table.** A DIA is a flexible-premium contract:
"any number of premiums during the deferral period" [S2][S3][S4][R13], each buying its
own paid-up income slice at the purchase rate then in force. A fixed set of premium
columns on the model point table would cap that number, so the schedule is a long table
keyed by ``point_id`` with one row per slice, and
:func:`~.DIA_US_S.Projection.premium_by_mth` collapses it to a
month-to-amount mapping once per contract.

**The two factor tables are the pricing kernel's data, and both are [std].** No
purchase-rate table was obtained and none is published — the Compact expressly relieves
the insurer of disclosing the deferral-period mortality and interest basis
[R13 §1.B(1)(a)] — so ``payout_factor_table.csv`` and ``rop_factor_table.csv`` carry the
technical notes' *illustrative* factors, marked as such in their ``provenance`` columns.
A model point can bypass them entirely by setting ``factor_basis = "formula"``, which
computes equation (2) and the equation (3) mid-band approximation from the shipped
mortality table instead.

The mortality table and the improvement scale are keyed by ``(age, sex)``. They are
separate files on purpose: the technical notes prescribe the **2012 IAM Basic** table
projected generationally with **Projection Scale G2** [R9][REG-R59], two distinct
objects with distinct provenance, and neither may be embedded in the model — the shipped
tables are illustrative **[std]** stand-ins, the mortality table being the one that
reproduces the notes' worked-example survival anchors. To swap in a licensed basis,
replace ``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at a
different name, then clear the cache. No formula changes.
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


def premium_schedule_table():
    """The premium schedules of every model point, from *premium_schedule.csv*.

    Long format, one row per premium slice, keyed by ``point_id`` - deliberately not
    indexed, so that selecting a contract's rows returns a DataFrame whether it has one
    slice or many.
    """
    return pd.read_csv(input_dir() / premium_schedule_file)           # noqa: F821


def mort_table():
    """The base annuitant mortality table by age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def improvement_scale():
    """The generational improvement scale by age and sex, from *improvement_scale.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / improvement_scale_file, index_col=["age", "sex"])  # noqa: F821


def payout_factor_table():
    """The illustrative payout annuity factors, from *payout_factor_table.csv*.

    Keyed by ``(income_start_age, sex, payout_form)``; the value is
    ``a^(m)_y(f; i_p)``, the APV at the income start age of $1 per annum of income.
    **[std]** - no insurer publishes payout factors for this product.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / payout_factor_file,                            # noqa: F821
        index_col=["income_start_age", "sex", "payout_form"])


def rop_factor_table():
    """The illustrative return-of-premium factors, from *rop_factor_table.csv*.

    Keyed by ``(issue_age, sex, deferral_years)``; the value is ``A_rop(x, d; i_p)``,
    the APV at the premium date of $1 payable at the end of the month of death within a
    ``d``-year deferral.  **[std]**.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rop_factor_file,                               # noqa: F821
        index_col=["issue_age", "sex", "deferral_years"])


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

premium_schedule_file = "premium_schedule.csv"

mort_table_file = "mort_table.csv"

improvement_scale_file = "improvement_scale.csv"

payout_factor_file = "payout_factor_table.csv"

rop_factor_file = "rop_factor_table.csv"

pd = ("Module", "pandas")