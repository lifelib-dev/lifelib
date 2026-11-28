"""Tests for name mapping from annuallife/model_new to annuallife/TradLife_A.

Issue #103: Records how names in annuallife/model_new were renamed in
annuallife/TradLife_A to ensure consistency across legacy libraries
(nestedlife, ifrs17sim, fastlife, etc.).
"""
import ast
import pathlib

import lifelib.libraries.annuallife.mapping as mapping_alias
from lifelib.libraries.annuallife.name_mapping import (
    CELL_NAME_MAPPING,
    MODEL_NAME_MAPPING,
    PARAM_NAME_MAPPING,
    REF_NAME_MAPPING,
    SPACE_NAME_MAPPING,
    get_space_mapping,
    map_cell,
    map_name,
    map_param,
    map_ref,
    map_space,
    reverse_map_cell,
)

TRADLIFE_A_DIR = (
    pathlib.Path(__file__).resolve().parents[2]
    / "libraries"
    / "annuallife"
    / "TradLife_A"
)


def test_mapping_alias():
    assert mapping_alias.map_space("Input") == "InputData"
    assert mapping_alias.map_cell("BaseProj", "AccumCF") == "accum_cf"
    assert mapping_alias.MODEL_NAME_MAPPING == MODEL_NAME_MAPPING


def test_model_and_space_mapping():
    assert MODEL_NAME_MAPPING["simplelife"] == "TradLife_A"
    assert SPACE_NAME_MAPPING["Input"] == "InputData"
    assert map_space("Input") == "InputData"
    assert map_space("BaseProj") == "BaseProj"
    assert map_space("Assumptions") == "Assumptions"
    assert map_space("Economic") == "Economic"
    assert map_space("PV") == "PV"
    assert map_space("PolicyAttrs") == "PolicyAttrs"
    assert map_space("CommTable") == "CommTable"
    assert map_space("Utilities") == "Utilities"
    assert map_space("Projection") == "Projection"
    assert map_space("Enums") == "Enums"


def test_input_data_mapping():
    assert map_cell("Input", "InputWorkbook") == "input_workbook"
    assert map_cell("Input", "PolicyData2") == "policy_data"
    assert map_cell("Input", "MortalityTables2") == "mortality_tables"
    assert map_cell("Input", "AssumptionTables2") == "assumption_tables"
    assert map_cell("Input", "Scenarios2") == "scenarios"
    assert map_cell("Input", "DiscountRate2") == "discount_rate"
    assert map_cell("Input", "PremWaiverCost2") == "prem_waiver_cost"
    assert map_cell("Input", "Assumption2") == "assumption"
    assert map_cell("Input", "ProductSpec2") == "product_spec"
    assert map_cell("Input", "ConstParams") == "const_params"
    assert map_cell("Input", "get_named_range_as_df") == "get_named_range_as_df"
    assert (
        map_cell("Input", "get_named_range_as_dict")
        == "get_named_range_as_dict"
    )
    assert map_cell("Input", "get_param_series") == "get_param_series"

    assert map_ref("Input", "InputFileName") == "input_file_name"
    assert map_ref("Input", "openpyxl") == "openpyxl"


def test_assumptions_mapping():
    assert map_cell("Assumptions", "BaseMortRate") == "mort_rate"
    assert map_cell("Assumptions", "CnsmpTax") == "cnsmp_tax"
    assert map_cell("Assumptions", "CommInitPrem") == "comm_init_prem"
    assert map_cell("Assumptions", "CommRenPrem") == "comm_ren_prem"
    assert map_cell("Assumptions", "CommRenTerm") == "comm_ren_term"
    assert map_cell("Assumptions", "ExpsAcqAnnPrem") == "exps_acq_ann_prem"
    assert map_cell("Assumptions", "ExpsAcqPol") == "exps_acq_pol"
    assert map_cell("Assumptions", "ExpsAcqSA") == "exps_acq_sa"
    assert map_cell("Assumptions", "ExpsMaintAnnPrem") == "exps_maint_ann_prem"
    assert map_cell("Assumptions", "ExpsMaintPol") == "exps_maint_pol"
    assert map_cell("Assumptions", "ExpsMaintSA") == "exps_maint_sa"
    assert map_cell("Assumptions", "InflRate") == "inflation_rate"
    assert map_cell("Assumptions", "MortalityTables") == "mortality_tables"
    assert map_cell("Assumptions", "MortTableIndex") == "mort_table_index"
    assert map_cell("Assumptions", "MortArrayIndex") == "mort_array_index"
    assert map_cell("Assumptions", "AsmpTables") == "asmp_tables"
    assert map_cell("Assumptions", "MortFactorIndex") == "mort_factor_index"
    assert map_cell("Assumptions", "LapseRateIndex") == "lapse_rate_index"
    assert map_cell("Assumptions", "AsmpTableLen") == "asmp_table_len"

    assert map_ref("Assumptions", "AsmpLookup") == "asmp_lookup"
    assert map_ref("Assumptions", "Input") == "input_data"


def test_baseproj_mapping():
    # Aggregates and cashflows
    assert map_cell("BaseProj", "AccumCF") == "accum_cf"
    assert map_cell("BaseProj", "AttAge") == "age"
    assert map_cell("BaseProj", "BenefitDeath") == "claims_death"
    assert map_cell("BaseProj", "BenefitTotal") == "claims"
    assert map_cell("BaseProj", "ChangeRsrv") == "change_rsrv"
    assert map_cell("BaseProj", "ExpsTotal") == "expenses"
    assert map_cell("BaseProj", "ExpsCommInit") == "commissions_init"
    assert map_cell("BaseProj", "ExpsCommRen") == "commissions_ren"
    assert map_cell("BaseProj", "ExpsCommTotal") == "commissions"
    assert map_cell("BaseProj", "NetInsurCF") == "net_cf"
    assert map_cell("BaseProj", "PolsIF_End") == "pols_if"
    assert map_cell("BaseProj", "PolsNewBiz") == "pols_if_init"
    assert map_cell("BaseProj", "PolsSurr") == "pols_lapse"
    assert map_cell("BaseProj", "PremIncome") == "premiums"

    # Per policy (_pp)
    assert map_cell("BaseProj", "SizeAnnPrem") == "ann_prem_pp"
    assert map_cell("BaseProj", "SizeBenefitDeath") == "claims_death_pp"
    assert map_cell("BaseProj", "SizeBenefitSurr") == "claims_surr_pp"
    assert map_cell("BaseProj", "SizeExpsAcq") == "expense_acq_pp"
    assert map_cell("BaseProj", "SizeExpsCommInit") == "commissions_init_pp"
    assert map_cell("BaseProj", "SizeExpsCommRen") == "commissions_ren_pp"
    assert map_cell("BaseProj", "SizeExpsMaint") == "expense_maint_pp"
    assert map_cell("BaseProj", "SizePremium") == "premium_pp"
    assert map_cell("BaseProj", "SizeSumAssured") == "sum_assured"

    # Rates and helpers
    assert map_cell("BaseProj", "SurrRate") == "lapse_rate"
    assert map_cell("BaseProj", "last_t") == "proj_len"
    assert map_cell("BaseProj", "LastAge") == "last_mort_age"
    assert map_cell("BaseProj", "DiscRate") == "disc_rate"


def test_commtable_mapping():
    assert map_cell("CommTable", "MortalityRates") == "mortality_rates"
    assert map_cell("CommTable", "AnnDuenx") == "AnnDuenx"
    assert map_cell("CommTable", "qx") == "qx"
    assert map_ref("CommTable", "MortalityTables2") == "mortality_tables"


def test_economic_mapping():
    assert map_cell("Economic", "DiscRate") == "disc_rate"
    assert map_cell("Economic", "InvstRetRate") == "invst_ret_rate"
    assert map_param("Economic", "ScenID") == "scen_id"
    assert map_ref("Economic", "Input") == "input_data"
    assert PARAM_NAME_MAPPING["Economic"]["ScenID"] == "scen_id"


def test_pv_mapping():
    assert map_cell("PV", "InterestNetCF") == "interest_net_cf"
    assert map_cell("PV", "PV_BenefitDeath") == "pv_claims_death"
    assert map_cell("PV", "PV_BenefitTotal") == "pv_claims"
    assert map_cell("PV", "PV_ExpsTotal") == "pv_expenses"
    assert map_cell("PV", "PV_ExpsCommTotal") == "pv_commissions"
    assert map_cell("PV", "PV_NetCashflow") == "pv_net_cf"
    assert map_cell("PV", "PV_PremIncome") == "pv_premiums"


def test_policyattrs_mapping():
    assert map_cell("PolicyAttrs", "GrossPremTable") == "gross_prem_table"
    assert map_cell("PolicyAttrs", "InitSurrCharge") == "init_surr_charge"
    assert map_cell("PolicyAttrs", "IntRate") == "int_rate"
    assert map_cell("PolicyAttrs", "Product") == "product"
    assert map_cell("PolicyAttrs", "PolicyType") == "policy_type"
    assert map_cell("PolicyAttrs", "Gen") == "gen"
    assert map_cell("PolicyAttrs", "Channel") == "channel"
    assert map_cell("PolicyAttrs", "Sex") == "sex"
    assert map_cell("PolicyAttrs", "Duration") == "duration"
    assert map_cell("PolicyAttrs", "IssueAge") == "issue_age"
    assert map_cell("PolicyAttrs", "PremFreq") == "prem_freq"
    assert map_cell("PolicyAttrs", "PolicyTerm") == "policy_term"
    assert map_cell("PolicyAttrs", "PolicyCount") == "policy_count"
    assert map_cell("PolicyAttrs", "SumAssured") == "sum_assured"

    assert map_ref("PolicyAttrs", "LifeTable") == "life_table"
    assert map_ref("PolicyAttrs", "Input") == "input_data"
    assert map_ref("PolicyAttrs", "PremTerm") == "prem_term"
    assert REF_NAME_MAPPING["PolicyAttrs"]["LifeTable"] == "life_table"


def test_projection_mapping():
    assert map_param("Projection", "PolicyID") == "idx"
    assert map_param("Projection", "ScenID") == "scen_id"


def test_reverse_mapping():
    assert reverse_map_cell("BaseProj", "claims_death") == "BenefitDeath"
    assert reverse_map_cell("BaseProj", "pols_lapse") == "PolsSurr"
    assert reverse_map_cell("InputData", "policy_data") == "PolicyData2"


def test_map_name_generic():
    assert map_name("BaseProj", "BenefitDeath") == "claims_death"
    assert map_name("Assumptions", "AsmpLookup") == "asmp_lookup"
    assert map_name("Projection", "PolicyID") == "idx"
    assert map_name("UnknownSpace", "Something") == "Something"


def test_get_space_mapping():
    proj_map = get_space_mapping("Projection")
    assert proj_map["space"] == "Projection"
    assert proj_map["params"]["PolicyID"] == "idx"
    assert proj_map["refs"]["pol"] == "pol"

    input_map = get_space_mapping("Input")
    assert input_map["space"] == "InputData"
    assert input_map["cells"]["PolicyData2"] == "policy_data"


def test_all_mapped_cells_exist_in_tradlife_a():
    """Verify that mapped target cells exist in TradLife_A.

    Note: In Assumptions, BaseMortRate was renamed to mort_rate in #95,
    and later removed in commit 2b7ce59 as unreachable dead code.
    All other mapped cells exist in TradLife_A.
    """
    for space, cells in CELL_NAME_MAPPING.items():
        actual_space = map_space(space)
        init_file = TRADLIFE_A_DIR / actual_space / "__init__.py"
        assert init_file.exists(), f"Space file {init_file} does not exist"
        tree = ast.parse(init_file.read_text(encoding="utf-8"))
        defined_funcs = {
            n.name for n in tree.body if isinstance(n, ast.FunctionDef)
        }
        for old_cell, new_cell in cells.items():
            if space == "Assumptions" and new_cell == "mort_rate":
                continue  # removed in 2b7ce59 as dead code
            assert new_cell in defined_funcs, (
                f"Mapped cell '{new_cell}' (from '{old_cell}') not found "
                f"in TradLife_A.{actual_space}"
            )
