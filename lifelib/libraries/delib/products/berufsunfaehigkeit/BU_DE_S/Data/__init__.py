# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.BU_DE_S.Projection` as ``data``. :mod:`~.BU_DE_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells cache;
if the readers lived there, every model point would re-read every file. Holding them in
an unparameterized Space reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/berufsunfaehigkeit/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``BU_DE_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

========================  ============================  ==========================
Reference                 Cells                         File
========================  ============================  ==========================
model_point_file          model_point_table()           model_point_table.csv
inception_file            inception_table()             inception_table.csv
claim_duration_file       claim_duration_table()        claim_duration_table.csv
mortality_file            mortality_table()             mortality_table.csv
occupation_file           occupation_table()            occupation_table.csv
lapse_file                lapse_table()                 lapse_table.csv
freq_loading_file         freq_loading_table()          freq_loading_table.csv
========================  ============================  ==========================

Every file but ``model_point_table.csv`` carries a per-row ``provenance`` column, which
is delib's second ruling: the citation discipline reaches the data files and is
machine-checked rather than merely practised. The model point table is the single
exemption, because a model point is a *configuration* and not an assumption.

.. rubric:: The biometric tables are [std] proxies, and what a replacement must preserve

**Nothing in this directory is a DAV table.** DAV 1997 I (*Invalidisierungswahrschein-
lichkeiten*), DAV 1997 RI (*Reaktivierungswahrscheinlichkeiten*), DAV 1997 TI
(*Sterbewahrscheinlichkeiten der Invaliden*) and DAV 2008 T are the property of the
Deutsche Aktuarvereinigung, are not published and are **not redistributed by delib**.
They are cited by name in the product's ``sources.md`` and the tables shipped beside this
model are anchored ``[std]`` constructions that reproduce their *shape* and nothing more.

Each proxy is anchored so that the technical notes' worked example reproduces exactly.
The three anchors, and what a replacement built from company or DAV data must preserve:

``inception_table.csv``
    ``inc_rate(30) = 0.001100`` exactly, on a two-slope Gompertz form
    ``0.00110 x 1.06^(min(x,45) - 30) x 1.13^(max(x,45) - 45)``. What must be preserved
    is the **age shape** — nearly flat to 30, moderate through the forties, sharply
    accelerating from the mid-forties, so that the last decade before the *Endalter*
    dominates the liability — and the declaration of whether the table is **gross or net
    of declinature**. The shipped table is gross, and ``accept_factor = 0.80`` sits on
    top of it; a table already net of declinature must be used with that factor at 1.00
    or the *Anerkennungsquote* is counted twice.

``mortality_table.csv``
    ``mort_rate_actv(30) = 0.000350`` exactly, with the disabled-lives rate at 4.00x it,
    both on ``1.095^(age - 30)``. What must be preserved is the **excess of disabled over
    active mortality** — never one rate for both states — and the fact that the active
    table is an insured-lives *Todesfall*-character shape rather than a population table.

``claim_duration_table.csv``
    ``recov_rate(1) = 0.250`` falling to ``0.006`` ultimate, with disabled-mortality
    select factors 3.0 / 2.0 / 1.6 / 1.4 / 1.3 and 1.2 from claim year 6. What must be
    preserved is the **duration shape**: reactivation is concentrated in the first one to
    two claim years and is close to zero after about five, and disabled-lives mortality
    is itself select on claim duration. A flat reactivation rate is a modelling error,
    not a simplification, and it is worth roughly a factor of two on projected benefit.

The remaining three files are market conventions rather than biometric bases:
``occupation_table.csv`` carries the five-class *Berufsgruppen* cut with BG1 at 1.00 and
BG4 at 3.00 as its anchors, ``lapse_table.csv`` a low German BU *Stornoquote* falling
from 4.0 % to a 2.0 % ultimate, and ``freq_loading_table.csv`` the
*Ratenzahlungszuschlag* ladder with the months between instalments. All three are
``[std]``: no German insurer publishes any of them.
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

    Inputs are *external* files, not data stored inside the model, so the model folder
    is pure formulas.  The path is resolved at run time from where the model was read,
    following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*.

    Thirteen policies indexed by ``point_id``, each carrying the twenty contractual
    attributes the projection reads.  The one input file with **no** ``provenance``
    column, and the only exemption from delib's second ruling: a model point is a
    *configuration* — one policy's own terms — rather than an assumption, so tagging it
    row by row would repeat the same provenance once per policy while saying nothing
    about any assumption.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def inception_table():
    """The annual *Invalidisierungswahrscheinlichkeit* by attained age, ages 18-66.

    Read from *inception_table.csv*.  A **[std]** two-slope Gompertz proxy for the
    reference occupational class BG1, unisex and **gross of declinature**, anchored at
    ``inc_rate(30) = 0.001100``; DAV 1997 I is DAV property and is not shipped.  See the
    Space docstring for what a replacement must preserve.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / inception_file, index_col="age")               # noqa: F821


def claim_duration_table():
    """The claim-duration table by claim year, from *claim_duration_table.csv*.

    Two columns on one index, because both quantities are select on the same duration:
    ``recov_rate``, the annual *Reaktivierungswahrscheinlichkeit*, and
    ``mort_dis_sel_factor``, the multiplier on disabled-lives mortality.  Rows 1-10 are
    claim years 1-10 and **row 11 is the ultimate**, applied to claim year 11 and beyond.
    Both columns are **[std]**; DAV 1997 RI and DAV 1997 TI are not shipped.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / claim_duration_file, index_col="dur_year")     # noqa: F821


def mortality_table():
    """The two annual mortality rates by attained age, ages 18-70.

    Read from *mortality_table.csv*: ``mort_rate_actv`` for lives in the *aktiv* and
    run-off ledgers and ``mort_rate_dis`` for lives in claim, before the claim-duration
    select factor.  Both are **[std]** Gompertz proxies anchored at
    ``mort_rate_actv(30) = 0.000350``, with the disabled rate at 4.00x the active one;
    DAV 2008 T and DAV 1997 TI are not shipped.  **Using one rate for both states is a
    numbered pitfall**, which is why the file carries two columns rather than one.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mortality_file, index_col="age")               # noqa: F821


def occupation_table():
    """The occupational loading by *Berufsgruppe*, from *occupation_table.csv*.

    ``occ_factor`` multiplies the **inception rate** and reaches the premium only through
    the equivalence — it is not the *Risikozuschlag*, which loads the premium alone.  The
    ``label`` column carries the class description so that a model point's
    ``berufsgruppe`` is readable without the product specification open.  **[std]**: one
    base table with occupational loadings is how German BU pricing works, but no
    insurer's *Berufsgruppenverzeichnis* was retrievable and carrier classifications are
    not comparable with one another.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / occupation_file, index_col="berufsgruppe")     # noqa: F821


def lapse_table():
    """The annual *Stornoquote* by policy year, from *lapse_table.csv*.

    Rows 1-5 are policy years 1-5 and **row 6 is the ultimate**, applied to policy year 6
    and beyond.  **[std]** and low by the standards of every other delib product, which
    is a real product fact rather than a modelling choice: once health has changed the
    cover cannot be replaced, so an insured with a claimable impairment cannot rationally
    lapse.  Lapse *selection* is not modelled; the direction of the resulting error is
    stated in the technical notes.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="policy_year")           # noqa: F821


def freq_loading_table():
    """The payment frequency table, from *freq_loading_table.csv*.

    ``prem_mode_months`` is the number of months between instalments — 12, 6, 3, 1 — and
    ``freq_load`` the *Ratenzahlungszuschlag* on the tariff premium, 1.00 / 1.02 / 1.03 /
    1.05.  The loading scales the *Bruttobeitrag* and the *Beitragsverrechnung* together,
    so the quoted *Zahlbeitrag* ratio is untouched by it.  **[std]**: the ladder is the
    recalled German market convention and no retrieved document confirms it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / freq_loading_file, index_col="prem_mode")      # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

inception_file = "inception_table.csv"

claim_duration_file = "claim_duration_table.csv"

mortality_file = "mortality_table.csv"

occupation_file = "occupation_table.csv"

lapse_file = "lapse_table.csv"

freq_loading_file = "freq_loading_table.csv"

pd = ("Module", "pandas")
