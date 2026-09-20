"""The model registry, and the locator that resolves it against this library.

Models are located relative to **this library directory**, so the suite runs from a clean
clone with no installation step, and keeps running from a copy made by
``lifelib.create()`` — where it tests *that copy's* models, which is the whole point of
shipping the tests inside the library.

That is why the path here is relative and not :data:`lifelib._dirs.TEMPLATES`: the
canonical locator resolves to the *installed* library, so a copy would silently test
lifelib's pristine models instead of the user's edited ones, and pass while proving
nothing.

:data:`MODELS` is the registry ``test_model_conventions_kr.py`` is parametrized over, so
registering a model here subjects it to the whole house style: it then either conforms or
fails.  The metadata records the projection basis, which is now **monthly on all ten**, the
age basis, which is *not* uniform and in Korea cannot be left implicit (see below), and that
none of them discount.  That last entry is a property of the library, not an omission:
every ``technical-notes.md`` specifies *gross liability cash flows* and leaves discounting,
the ``책임준비금``, the IFRS 17 CSM and the K-ICS 요구자본 to a separate layer that
consumes them.

**Why this is not in `conftest.py`.**  Six libraries now ship in-library suites, and
``conftest.py`` is a name pytest fixes.  Collecting them in one run puts several files
called ``conftest`` on ``sys.path``, one wins ``sys.modules``, and every ``from conftest
import LIB`` in *any* of the suites silently resolves to another library — a green run
against the wrong models, or the ``FileNotFoundError`` that revealed it in frlib.  The
registry therefore lives under a library-unique module name and ``conftest.py`` re-exports
it for its fixtures.

**Why the short names are English.**  Everywhere else in this library the English name
leads and the Korean name follows, which is the arrangement jplib, frlib and delib settled
on.  A model name cannot carry the Korean at all: it is a Python identifier and the name of
a directory on disk.  Nor is there much of a market short form to borrow — Korea says
"CI보험" and writes ``CI``, and after that the abbreviations run out — so the short names
are chosen rather than found, and the pairing to the Korean product is written down in the
library index rather than inferred.

Four of them are worth naming explicitly.  ``Medical_KR_S`` is 실손의료보험, the
**indemnity** reimbursement contract that sits on top of 국민건강보험 — it is not a daily
hospitalization benefit, and it is the only indemnity product anywhere in this repository;
the fixed-benefit third-sector chassis is ``Cancer_KR_S``.  ``LTC_KR_S`` is 간병보험,
private cover written on top of the public 노인장기요양보험 scheme, not that scheme itself,
and its trigger is the state's own 장기요양등급.  ``Pension_KR_S`` is 연금저축보험, the
tax-qualified *deferred* contract, and not the payout one, which is ``Immediate_KR_S``.
And ``Child_KR_S`` is 어린이보험, a bundled child health policy commonly written **in
utero**, which has no counterpart in any sister library.
"""
import pathlib

LIB = pathlib.Path(__file__).resolve().parents[1]

# ``ANNUAL`` is retained although no model currently carries it: the grid is a property a
# model declares rather than a property of the library, ``test_model_conventions_kr.py``
# resolves the name suffix from it, and a model added on an annual step would register here
# without a change to the suite.
ANNUAL = {"grid": "annual", "discounted": False}
MONTHLY = {"grid": "monthly", "discounted": False}

# The age basis is NOT uniform here, and leaving it implicit would be a modelling error
# rather than an omission.  Korea uses two age conventions and this library uses both,
# because its sources do.
#
# 보험나이 (*boheom nai*, insurance age) is the contractual age: months of age are rounded
# by the six-month rule, so a life 40 years and 7 months old is 41.  It is what every
# 보험료 산출 basis is graduated on, what a carrier's rate card is indexed by, and what the
# 경험생명표 — the industry table this library must proxy rather than ship — is built on.
#
# 만나이 (*man nai*, age last birthday) is what the **public statistical series** are
# published on: 통계청 완전생명표, 국가암등록통계 연령별 발생률, 국민건강보험공단
# 노인장기요양보험 통계연보 연령별 인정률.  Those series are the only citable basis for the
# three products whose decrements are morbidity rather than mortality, so those models are
# 만나이 models and say so.
#
# The mismatch is a modelled quantity and not a footnote: a 만나이 model point read against
# a 보험나이 rate table understates the rate by roughly half a year of ageing, and the
# models that straddle the two carry an explicit shift for it.  Recording the basis per
# model is what keeps them apart, and ``test_model_conventions_kr.py`` asserts that each
# model's ``Projection`` docstring names the basis registered here.
BOHEOM = {"age_basis": "보험나이"}   # insurance age, six-month rounding rule
MAN = {"age_basis": "만나이"}        # age last birthday, the public-statistics basis

# name -> (path relative to the library root, metadata)
#
# The name is <short name>_<country>_<grid>: a short English descriptor of the product,
# then KR, then _A for an annual step or _S for a monthly one.  The grid letters follow
# lifelib, where annuallife/TradLife_A is the annual-step model and basiclife/BasicTerm_S
# and savings/CashValue_SE are the monthly ones.  Every model in this library is monthly, so
# every name here carries `_S`; the `_A` half of the convention is still enforced by
# test_model_conventions_kr.py against the registry metadata, so a model added on an annual
# step would have to be named for it.  `S` carries a second sense in lifelib — scalar, one
# model point at a time, as against the vectorized `_M` models — and that is true of all ten
# here.
#
# This pairing is not derivable from the folder slug — "indemnity_medical" spelled out is
# unusable in a model name — so it lives here, and test_model_conventions_kr.py asserts
# that the name, the folder and the model's own _name all agree.
MODELS = {
    # 보장성 — protection
    "WholeLife_KR_S": ("products/whole_life/WholeLife_KR_S", MONTHLY | BOHEOM),
    "Term_KR_S": ("products/term_life/Term_KR_S", MONTHLY | BOHEOM),
    "CI_KR_S": ("products/ci_insurance/CI_KR_S", MONTHLY | BOHEOM),
    # 제3보험 — third insurance (보험업법 제4조제1항제3호)
    "Medical_KR_S": ("products/indemnity_medical/Medical_KR_S", MONTHLY | MAN),
    "Cancer_KR_S": ("products/cancer/Cancer_KR_S", MONTHLY | MAN),
    "LTC_KR_S": ("products/long_term_care/LTC_KR_S", MONTHLY | MAN),
    "Child_KR_S": ("products/child/Child_KR_S", MONTHLY | BOHEOM),
    # 저축·연금 — savings and annuity
    "Pension_KR_S": ("products/pension_savings/Pension_KR_S", MONTHLY | BOHEOM),
    "VA_KR_S": ("products/variable_annuity/VA_KR_S", MONTHLY | BOHEOM),
    "Immediate_KR_S": ("products/immediate_annuity/Immediate_KR_S", MONTHLY | BOHEOM),
}


# name -> the exact set of input files a full sweep of the shipped model point table reads.
#
# ``test_model_conventions_kr.py`` asserts this set, not merely that whatever was read was
# read once.  Counting only the files that happen to be read makes the check self-
# fulfilling: a file that stops being read drops out of the counter, and the read-once
# assertion then passes over less coverage rather than failing.  Registering the set is
# what turns "each file is read once per model" into a statement about *which* files.
#
# It also fixes how far the sweep has to run: a model that first reads some table at model
# point 7 of 9 would drop out of a check over a truncated table.
#
# Regenerate with ``python tools/gen_input_files.py lifelib/libraries/krlib`` rather than
# editing by hand — a load-bearing map that is hand-transcribed is how it goes stale.
INPUT_FILES = {
    "CI_KR_S": {
        "ci_incidence_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv"},
    "Cancer_KR_S": {
        "care_table.csv", "incidence_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_table.csv", "survival_table.csv",
        "tier_share_table.csv", "tier_table.csv"},
    "Child_KR_S": {
        "av_table.csv", "basis_table.csv", "incidence_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_table.csv", "neonatal_table.csv"},
    "Immediate_KR_S": {
        "charge_table.csv", "crediting_table.csv", "model_point_table.csv",
        "mort_table.csv"},
    "LTC_KR_S": {
        "av_table.csv", "dementia_table.csv", "grade_share_table.csv",
        "incidence_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv", "prevalence_table.csv"},
    "Medical_KR_S": {
        "claim_shape_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv", "oop_ceiling_table.csv", "severity_table.csv",
        "utilisation_table.csv"},
    "Pension_KR_S": {
        "decl_rate_table.csv", "expense_table.csv", "guar_rate_table.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_anchor_table.csv",
        "mort_table.csv", "pricing_table.csv", "tax_table.csv"},
    "Term_KR_S": {
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "prem_rate_table.csv", "rate_class_table.csv"},
    "VA_KR_S": {
        "charge_table.csv", "crediting_table.csv", "fund_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_table.csv", "return_scenario.csv",
        "risk_prem_table.csv"},
    "WholeLife_KR_S": {"lapse_table.csv", "model_point_table.csv", "mort_table.csv"},
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return LIB / MODELS[name][0]
