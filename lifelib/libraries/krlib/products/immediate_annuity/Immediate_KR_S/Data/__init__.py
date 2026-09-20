# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.Immediate_KR_S.Projection` as ``data``. :mod:`~.Immediate_KR_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many contracts
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/immediate_annuity/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so a
diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Immediate_KR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference and
a reader Cells:

=========================  ==============================  ============================
Reference                  Cells                           File
=========================  ==============================  ============================
model_point_file           model_point_table()             model_point_table.csv
mort_table_file            mort_table()                    mort_table.csv
charge_table_file          charge_table()                  charge_table.csv
crediting_table_file       crediting_table()               crediting_table.csv
=========================  ==============================  ============================

There is no lapse table, no surrender-value schedule and no commission scale, because the
product has none of those things. The 해약공제액 is nil at every duration on every retrieved
carrier, so a surrender-charge schedule would be a file of zeros; the 모집수수료 is a single
first-year rate on a single premium and sits in ``charge_table.csv`` beside the loads it has
to stay below; and **no retrieved source gives a surrender rate for 즉시연금 at all**, so
the lapse assumption is carried as a per-model-point scalar in ``model_point_table.csv``
where its effect can be isolated, and the technical notes state its level and its
sensitivity.

Substituting a filed basis means replacing ``mort_table.csv`` with a same-schema file keyed
on exactly the same ``(sex, age)`` in 보험나이, and ``charge_table.csv`` and
``crediting_table.csv`` with the filed 산출방법서's own figures. **No formula changes.**
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
    """The model point table, read from *model_point_table.csv*.

    One row per contract, indexed by ``point_id``.  Model point 1 is the technical notes'
    worked-example anchor cell: 남자, 보험나이 60, 일시납 ₩100,000,000, 종신연금형 with a
    ten-year 보증지급기간.  The columns are a *configuration* and not an assumption set,
    which is why this is the one input file in the library that carries no ``provenance``
    column — with the single exception of ``lapse_rate``, an assumption in disguise that
    is carried per model point because no source gives a surrender rate for this product
    and its effect has to be isolable.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The annuitant mortality rates by sex and 보험나이, from *mort_table.csv*.

    The 개인연금사망률 (*gaein yeongeum samangnyul*), used by the 종신연금형 alone for its
    annuity factor and by every shape for the death-benefit decrement.  It is a **[std]**
    construction and **not** the 경험생명표: the 제10회 경험생명표, applied from 2024-04, is
    produced by 보험개발원 and is not published in full — only 평균수명 and 기대여명 are
    released — so there is no Korean annuitant table to transcribe.  The shipped rates are
    a Makeham law fitted exactly to the two published 개인연금사망률 anchors at 보험나이 60
    and 70 and to the published 65세 기대여명, with ``qx = 1`` at the limiting age; the
    ``provenance`` column on every row records which of the three each row rests on and
    what the residual at 보험나이 50 is.  Sorted on read, because ``Projection.mort_rate``
    indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,
        index_col=["sex", "age"]).sort_index()


def charge_table():
    """The expense load, risk premium and commission by payout shape, from
    *charge_table.csv*.

    Indexed by ``shape``.  The 계약체결비용 and 계약관리비용 are deducted from the single
    premium **once**, at inception, as is the 위험보험료 on the two shapes that keep a death
    benefit; the 연금지급기간 charge of 0.80% of the 연금연액 is the only recurring one, and
    it is modelled as an insurer expense measured on the annuity rather than netted off the
    policyholder's payment.  ``acq_expense_rate`` is the load less the commission, so that
    the charge taken from the fund at inception exactly meets the outgo at inception.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / charge_table_file, index_col="shape")          # noqa: F821


def crediting_table():
    """The 공시이율 and the duration-stepped 최저보증이율, from *crediting_table.csv*.

    Read **without** an index, because the lookup is a duration-band test rather than a key
    lookup: each row gives a half-open band ``[dur_from, dur_to)`` in completed policy
    years and the 최저보증이율 that applies in it, beside the declared rate, which is
    uniform across the bands of a basis.  Two bases are shipped: ``decl_2017``, the
    representative one, and ``min_guar``, on which the declared rate is zero so that
    Max[공시이율, 최저보증이율] resolves to the floor at every duration and the stepping is
    exercised by a shipped model point.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / crediting_table_file)                          # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

charge_table_file = "charge_table.csv"

crediting_table_file = "crediting_table.csv"

pd = ("Module", "pandas")
