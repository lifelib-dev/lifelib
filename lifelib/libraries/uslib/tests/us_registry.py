"""The model registry, and the locator that resolves it against this library.

Models are located relative to **this library directory**, so the suite runs from a clean
clone with no installation step, and keeps running from a copy made by
``lifelib.create()`` — where it tests *that copy's* models, which is the whole point of
shipping the tests inside the library.

That is why the path here is relative and not :data:`lifelib._dirs.TEMPLATES`: the
canonical locator resolves to the *installed* library, so a copy would silently test
lifelib's pristine models instead of the user's edited ones, and pass while proving
nothing.

:data:`MODELS` is the registry ``test_model_conventions.py`` is parametrized over, so
registering a model here subjects it to the whole house style: it then either conforms or
fails.  The metadata records the projection basis and records that none of them discount.
That last entry is a property of the library, not an omission: every ``technical-notes.md``
specifies *gross liability cash flows* and leaves discounting and reserves to a separate
layer that consumes them.

**The SEC keys.**  USLIB-SEC-PLAN.md puts a ``_SEC`` model beside each ``_S`` one, and eight
metadata keys describe it: three from the plan's D10, two from its D5, one from its R17,
one from its R16 and one from its R14.  ``"twin"`` names the S model an SEC model is
derived from; its presence is what makes
an entry SEC (:func:`is_sec`).  ``"stage"`` is ``"E"`` while an SEC model runs in force at
``t = 0`` but does not yet compile, and ``"EC"`` once it does; the name does not change
with it.  ``"param"`` names the ``Projection`` parameter: ``"point_id"``, the default, or
``"idx"``, the position of a model point in the ``Data`` vectors, which a compiled model
takes as ``basiclife/BasicTerm_SC`` does.  ``"closing_pols_if"`` marks ``SPIA_US_SEC``
alone, whose ``pols_if`` is a closing count, not the count that weights row ``t``.
``"survival_pols_if"`` marks ``DIA_US_SEC`` alone, whose ``pols_if`` is the count on the
books weighted by ``lives_if_last(t)``, the probability that a covered life is alive at
the start of month ``t``, as ``DIA_US_S`` weights its constant count: neither the count
that weights row ``t`` nor a closing count.  And
``"reporting"``, at stage ``"EC"``, names the model's label accessors: the S cells that
return a model point's text, kept for a reader and for the twin identity, which no other
cell calls and which stay Python when the model compiles, beside ``model_point``, the
``result_*`` reports and the ``check_*`` cells.  ``"python_calls"``, at stage ``"EC"``, maps
a ``Projection`` cell to the Python builtins its formula may still call, R16's ``round`` of
a projected amount, which the typing guard's check of the generated C and the static check
of the formulas then admit in that cell alone, and nowhere else; ``WholeLife_US_SEC``'s
dividend is the first.  It names a builtin by its bare name, or a module's function by
its dotted name, ``"math.erf"``, as ``RILA_US_SEC``'s pricing keeps ``math``'s (M25), each
call wrapped in ``float(...)`` so that its locals stay C.  ``"engine"``, at
stage ``"EC"``, names S's cells of float parameters that an SEC model keeps for a reader and
for the twin identity, which no compiled cell calls and which compile with C signatures
and dict caches, their bodies Python, admitted to the typing guard and the static check
as the reporting cells are (R14); one may call another, and none returns a column, as a
label accessor does.  ``MYGA_US_SEC``'s statutory nonforfeiture rate is the first.  It
names too S's cells of no parameter that return a list, a dict or a DataFrame, which no C
type holds, kept for a reader and for the twin identity and called by no compiled cell,
as ``DIA_US_SEC``'s ``qlac_flags`` and premium schedule are (M24).  Read
them through :func:`meta`, which hands out a copy: ``MONTHLY`` is one dict, shared by every
entry that registers it.

``"reporting_columns"``, at stage ``"EC"`` beside ``"reporting"``, says what a label
accessor returns where that is not its point's column of the label's own name, in one of
three shapes: a column, for a label that takes no argument, as ``SPIA_US_SEC``'s
``payment_timing`` returns ``timing``; a dict of argument to column, for a label that
takes one argument, as its ``sex(life)`` returns ``primary_sex`` or ``joint_sex``; or a
pair of a column and a dict of value to label, for a label that returns the column's
value through the dict, a value the dict lacks as it is, as ``DIA_US_SEC``'s
``payout_form`` does.  A label it does not name returns its own column.

**Why :func:`point_keys` exists.**  An ``idx``-parameterized ``Projection`` is indexed by
position, not by table label.  The tables number their points from 1, so a test that
indexes such a model by label is off by one — ``Projection[1]`` is the second point, and the
first is never projected — and then fails at the last label, which lies past the end of
every vector, far from the line that caused it.  So no test indexes ``Projection`` by hand:
:func:`point_keys` gives the keys in table order, for whichever parameter the model takes,
and :func:`projection` turns a key into its ItemSpace.

**Why this is not in `conftest.py`.**  Two libraries now ship in-library suites, and
``conftest.py`` is a name pytest fixes.  Collecting both in one run puts two files called
``conftest`` on ``sys.path``, one wins ``sys.modules``, and every ``from conftest import
LIB`` in *either* suite silently resolves to the other library — a green run against the
wrong models, or the ``FileNotFoundError`` that revealed it.  The registry therefore lives
under a library-unique module name and ``conftest.py`` re-exports it for its fixtures.
"""
import operator
import pathlib

LIB = pathlib.Path(__file__).resolve().parents[1]

ANNUAL = {"grid": "annual", "age_basis": "ANB", "discounted": False}
MONTHLY = {"grid": "monthly", "age_basis": "ANB", "discounted": False}

# ``ANNUAL`` has no members below, and that is **not** the same as saying the library has no
# use for it.  The metadata is a statement about a model rather than about the library: a
# model added or converted to an annual step registers ``ANNUAL`` here, and
# ``test_the_name_carries_the_right_grid_suffix`` then requires its name to end ``_A``.  The
# row and the name move together, which is the point of asserting the suffix from the
# metadata rather than from the folder.

# name -> (path relative to the library root, metadata)
#
# The name is <market short name>_<country>_<grid>: the name the product is actually known
# by (MYGA, RILA, SPIA, ULSG — the same short names the taxonomy tables in the library's
# README use), then US, then _A for an annual step or _S for a monthly one.  The grid
# letters follow lifelib, where annuallife/TradLife_A is the annual-step model and
# basiclife/BasicTerm_S and savings/CashValue_SE are the monthly ones.
#
# This pairing is not derivable from the folder slug — "registered_index_linked_annuity"
# spelled out is unusable and the industry says RILA — so it lives here, and
# test_model_conventions.py asserts name, folder and the model's own _name all agree.
#
# An SEC model takes its twin's name with "EC" after the grid letter, and lives in its
# twin's product directory (USLIB-SEC-PLAN.md D1): E for running in force at t = 0, as
# basiclife/BasicTerm_SE does, C for compiling, as basiclife/BasicTerm_SC does.  The name is
# the family's from the model's first commit, at stage "E" as at "EC", so it never moves
# when the stage does (D2).  Its entry is the twin's metadata plus the SEC keys:
#
#     "Term_US_SEC": ("products/term_life/Term_US_SEC",
#                     {**MONTHLY, "twin": "Term_US_S", "stage": "E"}),
#
# with "param": "idx" and the "reporting" label accessors added at stage "EC", and there
# "python_calls" where a cell keeps a Python builtin, "engine" where it keeps S's cells
# of float parameters, "closing_pols_if": True on
# SPIA_US_SEC alone, and "survival_pols_if": True on DIA_US_SEC alone.  Phase 1 adds them
# one product at a time,
# each directly after its twin and with its INPUT_FILES set below, and Phase 2 moves each
# to stage "EC"; Term_US_SEC, the first, was entered exactly so, and is the first at "EC",
# WholeLife_US_SEC the second, UL_US_SEC the third, VUL_US_SEC the fourth, ULSG_US_SEC the
# fifth, MYGA_US_SEC the sixth, SPIA_US_SEC the seventh, DIA_US_SEC the eighth,
# FIA_US_SEC the ninth, IUL_US_SEC the tenth, VA_US_SEC the eleventh and RILA_US_SEC the
# twelfth.
MODELS = {
    # Life
    "Term_US_S": ("products/term_life/Term_US_S", MONTHLY),
    "Term_US_SEC": ("products/term_life/Term_US_SEC",
                    {**MONTHLY, "twin": "Term_US_S", "stage": "EC", "param": "idx",
                     "reporting": ("plan", "premium_mode", "rate_class", "sex")}),
    "WholeLife_US_S": ("products/whole_life/WholeLife_US_S", MONTHLY),
    "WholeLife_US_SEC": ("products/whole_life/WholeLife_US_SEC",
                         {**MONTHLY, "twin": "WholeLife_US_S", "stage": "EC",
                          "param": "idx",
                          "reporting": ("dividend_option", "premium_mode",
                                        "premium_period", "product", "risk_class", "sex"),
                          "python_calls": {"div_base": ("round",)}}),
    "UL_US_S": ("products/universal_life/UL_US_S", MONTHLY),
    "UL_US_SEC": ("products/universal_life/UL_US_SEC",
                  {**MONTHLY, "twin": "UL_US_S", "stage": "EC", "param": "idx",
                   "reporting": ("db_option", "premium_type", "qual_test", "rate_class",
                                 "sex", "surr_charge_id")}),
    "IUL_US_S": ("products/indexed_ul/IUL_US_S", MONTHLY),
    "IUL_US_SEC": ("products/indexed_ul/IUL_US_SEC",
                   {**MONTHLY, "twin": "IUL_US_S", "stage": "EC", "param": "idx",
                    "reporting": ("db_option", "premium_mode", "premium_type", "qual_test",
                                  "rate_class", "sex", "surr_charge_id"),
                    "engine": ("index_change", "index_credit", "index_credit_rate",
                               "seg_credit_base", "seg_matured_value")}),
    "VUL_US_S": ("products/variable_ul/VUL_US_S", MONTHLY),
    "VUL_US_SEC": ("products/variable_ul/VUL_US_SEC",
                   {**MONTHLY, "twin": "VUL_US_S", "stage": "EC", "param": "idx",
                    "reporting": ("db_option", "premium_type", "qual_test", "rate_class",
                                  "scenario_id", "sex", "surr_charge_id")}),
    "ULSG_US_S": ("products/guaranteed_ul/ULSG_US_S", MONTHLY),
    "ULSG_US_SEC": ("products/guaranteed_ul/ULSG_US_SEC",
                    {**MONTHLY, "twin": "ULSG_US_S", "stage": "EC", "param": "idx",
                     "reporting": ("premium_mode", "premium_type", "rate_class", "sex",
                                   "surr_charge_id"),
                     "python_calls": {"coi_rate": ("round",),
                                      "sg_coi_rate": ("round",)}}),
    # Annuity — deferred
    "MYGA_US_S": ("products/fixed_deferred_annuity/MYGA_US_S", MONTHLY),
    "MYGA_US_SEC": ("products/fixed_deferred_annuity/MYGA_US_SEC",
                    {**MONTHLY, "twin": "MYGA_US_S", "stage": "EC", "param": "idx",
                     "reporting": ("free_wd_rule", "mgsv_wd_convention", "mva_cap_rule",
                                   "mva_family", "policy_id", "renewal_architecture",
                                   "scenario_id", "sex", "tax_status", "wd_schedule_id"),
                     "engine": ("mgsv_rate_is_compliant", "mgsv_rate_statutory",
                                "mva_ref_term_years")}),
    "FIA_US_S": ("products/fixed_indexed_annuity/FIA_US_S", MONTHLY),
    "FIA_US_SEC": ("products/fixed_indexed_annuity/FIA_US_SEC",
                   {**MONTHLY, "twin": "FIA_US_S", "stage": "EC", "param": "idx",
                    "reporting": ("credit_method", "glwb_basis", "policy_id", "rollup_id",
                                  "scenario_id", "sex", "tax_status", "wd_schedule_id"),
                    "engine": ("credit_rate_on", "mgsv_rate_is_compliant",
                               "mgsv_rate_statutory", "payout_rate")}),
    "VA_US_S": ("products/variable_annuity/VA_US_S", MONTHLY),
    "VA_US_SEC": ("products/variable_annuity/VA_US_SEC",
                  {**MONTHLY, "twin": "VA_US_S", "stage": "EC", "param": "idx",
                   "reporting": ("cdsc_schedule", "designated_lives", "fee_reset_rule",
                                 "fund_set", "glwb_option", "gmdb_option", "policy_id",
                                 "rollup_rule", "scenario_id", "sex", "stepup_basis",
                                 "tax_status", "txn_id"),
                   "reporting_columns": {"stepup_basis": "glwb_stepup_basis"},
                   "engine": ("fee_rate_vix_clip", "fee_rate_vix_raw", "lapse_itm_mult",
                              "sub_ids")}),
    "RILA_US_S": (
        "products/registered_index_linked_annuity/RILA_US_S", MONTHLY),
    "RILA_US_SEC": ("products/registered_index_linked_annuity/RILA_US_SEC",
                    {**MONTHLY, "twin": "RILA_US_S", "stage": "EC", "param": "idx",
                     "reporting": ("amort_rule", "crediting_type", "iv_family",
                                   "policy_id", "scenario_id", "sex", "wd_schedule_id"),
                     "engine": ("bs_binary_call", "bs_call", "bs_d1", "bs_d2", "bs_put",
                                "credit_rate_at", "norm_cdf", "opt_budget_at_cap",
                                "opt_component", "opt_portfolio", "opt_portfolio_abs"),
                     "python_calls": {
                         "cap_solved_at_start": ("math.erf", "math.exp", "math.log",
                                                 "math.sqrt"),
                         "fixed_leg_yield": ("math.log",),
                         "fixed_proxy_factor": ("math.log",),
                         "inflation_factor": ("math.log",),
                         "mva_factor": ("math.log",),
                         "opt_budget_target": ("math.log",),
                         "opt_component_at": ("math.erf", "math.exp", "math.log",
                                              "math.sqrt")}}),
    # Annuity — payout
    "SPIA_US_S": ("products/immediate_annuity/SPIA_US_S", MONTHLY),
    "SPIA_US_SEC": ("products/immediate_annuity/SPIA_US_SEC",
                    {**MONTHLY, "twin": "SPIA_US_S", "stage": "EC", "param": "idx",
                     "closing_pols_if": True,
                     "reporting": ("form", "mort_basis", "payment_timing",
                                   "reduction_trigger", "sex"),
                     "reporting_columns": {"payment_timing": "timing",
                                           "sex": {1: "primary_sex", 2: "joint_sex"}}}),
    "DIA_US_S": ("products/deferred_income_annuity/DIA_US_S", MONTHLY),
    "DIA_US_SEC": ("products/deferred_income_annuity/DIA_US_SEC",
                   {**MONTHLY, "twin": "DIA_US_S", "stage": "EC", "param": "idx",
                    "survival_pols_if": True,
                    "reporting": ("db_form", "factor_basis", "income_form", "market_type",
                                  "mort_basis", "payment_timing", "payout_form",
                                  "reduction_trigger", "sex"),
                    "reporting_columns": {"payment_timing": "timing",
                                          "sex": {1: "sex", 2: "joint_sex"},
                                          "payout_form": ("income_form", {"LO_ROP": "LO"})},
                    "engine": ("annuity_factor", "premium_by_mth", "premium_schedule",
                               "pricing_disc_factor", "qlac_flags"),
                    "python_calls": {"purchase_rate": ("round",)}}),
}


# name -> the exact set of input files a full sweep of the shipped model point table reads.
#
# ``test_model_conventions.py`` asserts this set, not merely that whatever was read was
# read once.  Counting only the files that happen to be read makes the check self-
# fulfilling: a file that stops being read drops out of the counter, and the read-once
# assertion passes over less coverage rather than failing.  Registering the set is what
# turns "each file is read once per model" into a statement about *which* files.
#
# The set is what the **base run** reads, which is not always every CSV in the directory.
# ``VUL_US_S`` ships ``prem_persistency.csv`` and does not read it: ``prem_persistency(t)``
# short-circuits to 1.0 while ``dyn_behavior_on`` is off, which is the default, so only a
# test that switches the behaviour module on reaches the table.  Two files are reached
# late rather than not at all — ``SPIA_US_S`` first reads its mortality table and
# improvement scale at model point 7, where ``mort_basis`` stops being ``"scenario"`` —
# which is why the sweep has to run to the end of the table before this is asserted.
INPUT_FILES = {
    "DIA_US_S": {
        "improvement_scale.csv", "model_point_table.csv", "mort_table.csv",
        "payout_factor_table.csv", "premium_schedule.csv", "rop_factor_table.csv"},
    "DIA_US_SEC": {
        "improvement_scale.csv", "model_point_table_sec.csv", "mort_table.csv",
        "payout_factor_table.csv", "premium_schedule_sec.csv", "rop_factor_table.csv"},
    "FIA_US_S": {
        "model_point_table.csv", "mort_table.csv", "payout_rate_table.csv",
        "rate_scenario.csv", "rollup_table.csv", "surr_charge_table.csv",
        "withdrawal_table.csv"},
    "FIA_US_SEC": {
        "model_point_table_sec.csv", "mort_table.csv", "payout_rate_table.csv",
        "rate_scenario_sec.csv", "rollup_table.csv", "surr_charge_table.csv",
        "withdrawal_table.csv"},
    "IUL_US_S": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "surr_charge_table.csv"},
    "IUL_US_SEC": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "inforce_segments_sec.csv", "lapse_table.csv", "model_point_table_sec.csv",
        "mort_table.csv", "surr_charge_table.csv"},
    "MYGA_US_S": {
        "model_point_table.csv", "mort_table.csv", "mva_factor_table.csv",
        "rate_scenario.csv", "surr_charge_age_cap.csv", "surr_charge_table.csv",
        "withdrawal_table.csv"},
    "MYGA_US_SEC": {
        "model_point_table_sec.csv", "mort_table.csv", "mva_factor_table.csv",
        "rate_scenario.csv", "surr_charge_age_cap.csv", "surr_charge_table.csv",
        "withdrawal_table.csv"},
    "RILA_US_S": {
        "guar_min_rate_table.csv", "lapse_table.csv", "market_scenario.csv",
        "model_point_table.csv", "mort_table.csv", "surr_charge_table.csv",
        "withdrawal_table.csv"},
    "RILA_US_SEC": {
        "guar_min_rate_table.csv", "lapse_table.csv", "market_scenario_sec.csv",
        "model_point_table_sec.csv", "mort_table.csv", "surr_charge_table.csv",
        "withdrawal_table.csv"},
    "SPIA_US_S": {
        "improvement_scale.csv", "model_point_table.csv", "mort_table.csv",
        "surr_charge_table.csv"},
    "SPIA_US_SEC": {
        "improvement_scale.csv", "model_point_table_sec.csv", "mort_table.csv",
        "surr_charge_table.csv"},
    "Term_US_S": {
        "class_factor_table.csv", "model_point_table.csv", "mort_table.csv",
        "premium_rates.csv", "shock_lapse_table.csv"},
    "Term_US_SEC": {
        "class_factor_table.csv", "model_point_table_sec.csv", "mort_table.csv",
        "premium_rates.csv", "shock_lapse_table.csv"},
    "ULSG_US_S": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv", "rop_table.csv",
        "surr_charge_table.csv"},
    "ULSG_US_SEC": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table_sec.csv", "mort_table.csv",
        "rop_table.csv", "surr_charge_table.csv"},
    "UL_US_S": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "prem_persistency.csv", "surr_charge_table.csv"},
    "UL_US_SEC": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table_sec.csv", "mort_table.csv",
        "prem_persistency.csv", "surr_charge_table.csv"},
    "VA_US_S": {
        "cdsc_table.csv", "fund_table.csv", "gawa_pct_table.csv",
        "model_point_table.csv", "mort_table.csv", "rate_scenario.csv",
        "return_scenario.csv", "transaction_table.csv"},
    "VA_US_SEC": {
        "cdsc_table.csv", "fund_table.csv", "gawa_pct_table.csv",
        "model_point_table_sec.csv", "mort_table.csv", "rate_scenario_sec.csv",
        "return_scenario_sec.csv", "transaction_table.csv"},
    "VUL_US_S": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "scenario_table.csv", "subaccount_table.csv", "surr_charge_table.csv"},
    "VUL_US_SEC": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table_sec.csv", "mort_table.csv",
        "scenario_table.csv", "subaccount_table.csv", "surr_charge_table.csv"},
    "WholeLife_US_S": {
        "cv_table.csv", "model_point_table.csv", "mort_table.csv", "np_guar_table.csv",
        "nsp_table.csv", "premium_rates.csv"},
    "WholeLife_US_SEC": {
        "cv_table.csv", "model_point_table_sec.csv", "mort_table.csv",
        "np_guar_table.csv", "nsp_table.csv", "premium_rates.csv"},
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return LIB / MODELS[name][0]


def meta(name):
    """The metadata registered for ``name``, as a dict of its own.

    A copy, because the registered dict is usually :data:`MONTHLY` itself, shared by every
    entry that registers it as it stands: a test that set a key on the original would set
    it for every one of them.  Keys an entry does not carry are absent rather than
    defaulted, so a caller states its default where it reads one:
    ``meta(n).get("param", "point_id")``.
    """
    return dict(MODELS[name][1])


def is_sec(name):
    """Whether ``name`` is SEC, i.e. registered with the ``"twin"`` it is derived from."""
    return "twin" in MODELS[name][1]


def _parameter(model):
    """The name of the ``Projection`` parameter, which must be one the helpers here know."""
    parameters = tuple(model.Projection.parameters or ())
    if parameters in (("point_id",), ("idx",)):
        return parameters[0]
    raise ValueError(
        f"{model.name}: Projection is parameterized by {parameters!r}; the registry "
        "helpers know ('point_id',), the table label, and ('idx',), its position")


def point_keys(model):
    """The key of each model point's ``Projection`` ItemSpace, in table order.

    The table labels when ``Projection`` is parameterized by ``point_id``; the positions
    ``0 .. n-1`` when it is parameterized by ``idx``, where position ``i`` is row ``i`` of
    ``model.Data.model_point_table()`` — the row the ``Data`` vectors hold at ``i``.  Any
    other parameter raises ``ValueError``: a key of an unknown kind is exactly the error
    this helper exists to prevent, so it is not guessed at.
    """
    table = model.Data.model_point_table()
    if _parameter(model) == "idx":
        return list(range(len(table)))
    return list(table.index)


def projection(model, key):
    """The ``Projection`` ItemSpace for ``key``, one of :func:`point_keys`.

    modelx builds an ItemSpace for any argument at all, so a key the table does not have —
    position 0 on a ``point_id`` model, the last label on an ``idx`` one, a label of the
    wrong type — would otherwise surface later, as whatever error the first lookup inside
    the projection raises.  It raises ``KeyError`` here instead.  What it cannot catch is a
    valid key of the wrong kind, such as label 1 on an ``idx`` model, which is also
    position 1; that is why the keys come from :func:`point_keys` and not from the table.
    A position is passed on as a Python ``int``, whatever integer type it arrived as.
    """
    table = model.Data.model_point_table()
    if _parameter(model) == "idx":
        try:
            position = operator.index(key)
        except TypeError:
            position = None
        if position is None or not 0 <= position < len(table):
            raise KeyError(
                f"{model.name}: {key!r} is not a position 0 .. {len(table) - 1}; an idx "
                "Projection is indexed by position, as point_keys() gives")
        return model.Projection[position]
    if key not in table.index:
        raise KeyError(f"{model.name}: no model point labelled {key!r}")
    return model.Projection[key]
