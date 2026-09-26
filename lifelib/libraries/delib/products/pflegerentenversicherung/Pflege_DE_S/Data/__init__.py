# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The nine input CSVs are read here, **once per model**, and referenced from
:mod:`~.Pflege_DE_S.Projection` as ``data``. :mod:`~.Pflege_DE_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/pflegerentenversicherung/``, rather than data stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Pflege_DE_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  =========================
Reference                  Cells                           File
=========================  ==============================  =========================
model_point_file           model_point_table()             model_point_table.csv
benefit_scale_file         benefit_scale_table()           benefit_scale_table.csv
mort_table_file            mort_table()                    mort_table.csv
incidence_file             incidence_table()               incidence_table.csv
care_file                  care_table()                    care_table.csv
lapse_file                 lapse_table()                   lapse_table.csv
surrender_file             surrender_table()               surrender_table.csv
expense_file               expense_table()                 expense_table.csv
basis_file                 basis_table()                   basis_table.csv
=========================  ==============================  =========================

Every file but ``model_point_table.csv`` carries a final ``provenance`` column, one tag
per row — the library's second ruling, asserted by
``tests/test_model_conventions_de.py``. A model point is a *configuration* rather than an
assumption, which is why it is the single exemption.

.. rubric:: The tables are ``[std]`` proxies, and what a replacement must preserve

**DAV 2008 P, the German market's standard multi-state *Pflegetafel*, is the property of
the Deutsche Aktuarvereinigung, is not public, and is not redistributed by this library.**
Neither is DAV 2008 T, DAV 2004 R or any other DAV table. They are cited by name in
``sources.md`` and nothing here is derived from them. What ships instead is a set of
shaped proxies, and the anchors below are what a substitute must reproduce for the
technical notes' worked example to close to the cent:

* ``mort_table.csv`` — active-life mortality, a **Gompertz proxy**
  ``1 - exp(-B c**age)`` by sex over ages 18 to 108, with ``mort_rate = 1.0`` at age 109.
  Anchored at ``q(65) = 1.35 %`` and ``q(85) = 10.5 %`` male, ``q(65) = 0.75 %`` and
  ``q(85) = 7.0 %`` female, which fix ``B_M = 1.47884e-05``, ``c_M = 1.110680``,
  ``B_F = 4.76290e-06``, ``c_F = 1.119962``. **A replacement must preserve those four
  anchor rates.**
* ``incidence_table.csv`` — the rate at which an active life enters *any* *Pflegegrad*,
  ``min(I0 exp(g (age - 65)), 0.50)`` with ``I0_F = 0.0110``, ``g_F = 0.1400``,
  ``I0_M = 0.0085``, ``g_M = 0.1380``. The slope is anchored on the one shape the research
  file states with confidence — prevalence roughly doubling every five years of age above
  75, a growth rate of ``ln 2 / 5 = 0.1386``.
* ``care_table.csv`` — the whole in-care basis in five rows. ``mort_mult`` is a multiple
  on the **force** of active mortality at the same age, not on the rate.

A replacement table must preserve four properties: **(a)** incidence by attained age, sex
and *grade of entry*, because a stroke or a fracture enters directly at grade 3 or 4;
**(b)** deterioration dominating recovery above age 75; **(c)** mortality in care as a
grade-increasing multiple of active mortality; and **(d)** transition probabilities out of
each state summing, with the stay probability, to one. Dropping a licensed or company
table in place of these changes the basis with no formula change.

The remaining tables are standardizations of a different kind: ``lapse_table.csv`` and
``surrender_table.csv`` encode a shape argued from the *Zillmerung* and the § 169 VVG
five-year spread rather than from data — no lapse rate and no *Rückkaufswert* for a German
*Pflegerente* at any duration was established — and ``expense_table.csv`` carries five
placeholder levels whose only cited element is the 25 ‰ ceiling the acquisition charge is
set exactly at. ``basis_table.csv`` holds the *Rechnungszins*, the terminal age, the
unisex mix, the recovery-damping shape, the *Beitragssumme* convention, the check
tolerance and the five first-order prudence margins; only the *Rechnungszins* is cited.
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

    Inputs are *external* files, not data stored inside the model, so the model folder is
    pure formulas.  The path is resolved at run time from where the model was read,
    following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The fourteen model points, read from *model_point_table.csv*.

    The only input file without a ``provenance`` column: a model point is a
    *configuration* — one policy's own terms — rather than an assumption, and that is the
    single exemption from the library's second ruling.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def benefit_scale_table():
    """The *Leistungsstaffel* by schedule and *Pflegegrad*, from *benefit_scale_table.csv*.

    Two schedules ship.  ``delib_std`` is 0 / 30 / 50 / 75 / 100 % — the flatter, higher
    shape a *Pflegerente* aimed at the residential funding gap tends to use, and a
    **[std]** choice within an observed range.  ``bahr`` is the statutory
    10 / 20 / 30 / 40 / 100 % minimum grid of § 127 SGB XI, the only *Leistungsstaffel*
    fixed by German statute; it is carried for comparison, since a *Pflegerente* written
    by a *Lebensversicherer* cannot be a *geförderter Tarif*.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / benefit_scale_file,                            # noqa: F821
        index_col=["staffel_id", "pflegegrad"])


def mort_table():
    """Annual **active-life** mortality by sex and attained age, from *mort_table.csv*.

    A **[std]** Gompertz proxy over ages 18 to 108 with the limiting-age rate of 1.0 at
    age 109, not a fitted or standard table; see the Space docstring for the four anchor
    rates a replacement must preserve.  In-care mortality is not tabulated: it is this
    rate's force multiplied by ``mort_mult`` from *care_table.csv*.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"])     # noqa: F821


def incidence_table():
    """Annual incidence into **any** *Pflegegrad* by sex and age, from *incidence_table.csv*.

    A **[std]** exponential proxy capped at ``inc_cap``.  It is the rate of leaving the
    active state for care; the grade actually entered is drawn from ``entry_share`` in
    *care_table.csv*, because entry is not uniformly at the lowest grade.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / incidence_file, index_col=["sex", "age"])      # noqa: F821


def care_table():
    """The whole in-care basis in five rows, from *care_table.csv*.

    ``entry_share`` is the distribution of the grade first entered and sums to 1.00;
    ``det_rate`` the annual deterioration rate to the next grade up, zero at grade 5;
    ``rec_rate`` the annual recovery rate to the grade below — to the active state from
    grade 1 — before the age damping; and ``mort_mult`` the multiple on the **force** of
    active mortality at the same age.

    ``entry_share`` is deliberately **not** the stock distribution of about
    9 / 44 / 27 / 14 / 6 %: entrants skew lower than the stock because deterioration moves
    people up over a spell, and using the stock as the entry mix is a listed pitfall.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / care_file, index_col="pflegegrad")             # noqa: F821


def lapse_table():
    """Annual lapse rates from the **active** state by policy year, from *lapse_table.csv*.

    Policy years 1 to 40; year 40's rate applies to every later year.  A **[std]** shape:
    no lapse rate for a German *Pflegerente* at any duration was established, and the
    profile is argued from the *Zillmerung* — the *Rückkaufswert* is near zero for the
    first years, so an early lapse is expensive to the policyholder.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="policy_year")           # noqa: F821


def surrender_table():
    """The guaranteed *Rückkaufswert* as a fraction of premiums paid to date.

    Read from *surrender_table.csv*, by *Versicherungsjahr* ``y(t) = t // 12 + 1``, 1 to 40:
    year ``k``'s ratio applies throughout policy year ``k``, ``t = 12(k - 1) … 12k - 1``,
    and year 40's applies thereafter, intermediate years interpolated in the shipped file.
    It is the **current** policy year, not the completed one — a surrender at ``t = 24``,
    two completed years, already takes year 3's ratio.  The
    scale-free form, which is the form a German contract states.  The shape encodes two
    cited facts — the 25 ‰ *Zillmerung* allowance, which is why the first two years are
    zero, and the § 169 Abs. 3 VVG five-year spread floor, which is why it turns positive
    in year three — and no cited level, because none was established.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surrender_file, index_col="policy_year")       # noqa: F821


def expense_table():
    """The five expense assumptions and their units, from *expense_table.csv*.

    ``acq_permille`` (‰ of *Beitragssumme*, charged once at ``t = 0``),
    ``admin_prem_pct`` (fraction of each *Beitrag* collected), ``admin_mth_pp`` (EUR per
    policy in force per month at ``t = 0`` prices), ``claim_expense_pp`` (EUR per annuity
    payment made) and ``expense_infl`` (annual).  All five levels are **[std]**; only the
    25 ‰ ceiling the first is set exactly at is cited.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / expense_file, index_col="item")                # noqa: F821


def basis_table():
    """The scalar bases and conventions, from *basis_table.csv*.

    The *Rechnungszins*; the terminal age ``omega_age``; the unisex pricing mix; the
    ``rec_age_ref`` / ``rec_age_decay`` recovery damping; the ``inc_cap`` shape device; the
    ``beitragssumme_cap_age`` convention the *Zillmerung* base is struck on; the
    ``roll_fwd_tol`` every ``check_*`` identity uses; and the five first-order prudence
    margins ``inc_margin``, ``det_margin``, ``rec_margin``, ``care_mort_margin`` and
    ``act_mort_margin``.  Only the *Rechnungszins* is cited; everything else is **[std]**.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / basis_file, index_col="param")                 # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

benefit_scale_file = "benefit_scale_table.csv"

mort_table_file = "mort_table.csv"

incidence_file = "incidence_table.csv"

care_file = "care_table.csv"

lapse_file = "lapse_table.csv"

surrender_file = "surrender_table.csv"

expense_file = "expense_table.csv"

basis_file = "basis_table.csv"

pd = ("Module", "pandas")
