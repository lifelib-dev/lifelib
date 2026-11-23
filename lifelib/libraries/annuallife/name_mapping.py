"""Name mapping from annuallife/model_new to annuallife/TradLife_A.

This module records and provides lookup functions for how names in
``annuallife/model_new`` (the post-structural refactoring snapshot)
were renamed to ``annuallife/TradLife_A``.

Reference: https://github.com/lifelib-dev/lifelib/issues/103

Conventions reflected in the rename:
- Cells and references converted from CamelCase / PascalCase to snake_case.
- Per-policy cells renamed with ``..._pp`` suffix (e.g. ``SizeBenefitDeath``
  -> ``claims_death_pp``).
- ``Benefit...`` family renamed to ``claims_...`` (cashflows) and
  ``claims_..._pp`` (per policy).
- ``ExpsComm...`` family renamed to ``commissions...``.
- Aggregates: ``ExpsTotal`` -> ``expenses``, ``BenefitTotal`` -> ``claims``,
  ``PremIncome`` -> ``premiums``.
- Surrenders: ``PolsSurr`` / ``SurrRate`` -> ``pols_lapse`` / ``lapse_rate``.
- In-force counts: ``PolsIF_End`` -> ``pols_if``,
  ``PolsNewBiz`` -> ``pols_if_init``.
- Projection bounds: ``last_t`` -> ``proj_len``,
  ``LastAge`` -> ``last_mort_age``.
- Input space: ``Input`` -> ``InputData``, dropping the ``2`` suffix
  (``PolicyData2`` -> ``policy_data``).
- Space parameters: ``PolicyID`` -> ``idx``, ``ScenID`` -> ``scen_id``.
"""

MODEL_NAME_MAPPING = {
    "simplelife": "TradLife_A",
}

SPACE_NAME_MAPPING = {
    "Input": "InputData",
    "Economic": "Economic",
    "BaseProj": "BaseProj",
    "PV": "PV",
    "Projection": "Projection",
    "Assumptions": "Assumptions",
    "PolicyAttrs": "PolicyAttrs",
    "Utilities": "Utilities",
    "CommTable": "CommTable",
    "Enums": "Enums",
}

CELL_NAME_MAPPING = {
    "Input": {
        "InputWorkbook": "input_workbook",
        "PolicyData2": "policy_data",
        "MortalityTables2": "mortality_tables",
        "AssumptionTables2": "assumption_tables",
        "Scenarios2": "scenarios",
        "DiscountRate2": "discount_rate",
        "PremWaiverCost2": "prem_waiver_cost",
        "Assumption2": "assumption",
        "ProductSpec2": "product_spec",
        "ConstParams": "const_params",
        "get_named_range_as_df": "get_named_range_as_df",
        "get_named_range_as_dict": "get_named_range_as_dict",
        "get_param_series": "get_param_series",
    },
    "Assumptions": {
        "BaseMortRate": "mort_rate",
        "CnsmpTax": "cnsmp_tax",
        "CommInitPrem": "comm_init_prem",
        "CommRenPrem": "comm_ren_prem",
        "CommRenTerm": "comm_ren_term",
        "ExpsAcqAnnPrem": "exps_acq_ann_prem",
        "ExpsAcqPol": "exps_acq_pol",
        "ExpsAcqSA": "exps_acq_sa",
        "ExpsMaintAnnPrem": "exps_maint_ann_prem",
        "ExpsMaintPol": "exps_maint_pol",
        "ExpsMaintSA": "exps_maint_sa",
        "InflRate": "inflation_rate",
        "MortalityTables": "mortality_tables",
        "MortTableIndex": "mort_table_index",
        "MortArrayIndex": "mort_array_index",
        "AsmpTables": "asmp_tables",
        "MortFactorIndex": "mort_factor_index",
        "LapseRateIndex": "lapse_rate_index",
        "AsmpTableLen": "asmp_table_len",
    },
    "BaseProj": {
        # Aggregates and cash flows
        "AccumCF": "accum_cf",
        "AttAge": "age",
        "BenefitAccDth": "claims_acc_dth",
        "BenefitAccHosp": "claims_acc_hosp",
        "BenefitAnn": "claims_ann",
        "BenefitDeath": "claims_death",
        "BenefitLiving": "claims_living",
        "BenefitMat": "claims_mat",
        "BenefitOther": "claims_other",
        "BenefitSickHosp": "claims_sick_hosp",
        "BenefitSurg": "claims_surg",
        "BenefitSurr": "claims_surr",
        "BenefitTotal": "claims",
        "ChangeRsrv": "change_rsrv",
        "ExpsAcq": "exps_acq",
        "ExpsAcqTotal": "exps_acq_total",
        "ExpsCommInit": "commissions_init",
        "ExpsCommRen": "commissions_ren",
        "ExpsCommTotal": "commissions",
        "ExpsMaint": "exps_maint",
        "ExpsMaintTotal": "exps_maint_total",
        "ExpsOther": "exps_other",
        "ExpsTotal": "expenses",
        "IncomeTotal": "income_total",
        "InsurIF_Beg1": "insur_if_beg1",
        "InsurIF_End": "insur_if_end",
        "IntAccumCF": "int_accum_cf",
        "InvstIncome": "invst_income",
        "NetInsurCF": "net_cf",
        "PolsAccDeath": "pols_acc_death",
        "PolsAccHosp": "pols_acc_hosp",
        "PolsAnnuity": "pols_annuity",
        "PolsDeath": "pols_death",
        "PolsIF_AftMat": "pols_if_aft_mat",
        "PolsIF_Beg": "pols_if_beg",
        "PolsIF_Beg1": "pols_if_beg1",
        "PolsIF_End": "pols_if",
        "PolsLiving": "pols_living",
        "PolsMaturity": "pols_maturity",
        "PolsNewBiz": "pols_if_init",
        "PolsOther": "pols_other",
        "PolsRenewal": "pols_renewal",
        "PolsSickHosp": "pols_sick_hosp",
        "PolsSurg": "pols_surg",
        "PolsSurr": "pols_lapse",
        "PremIncome": "premiums",
        "ProfitBefTax": "profit_bef_tax",
        "ReserveHospRsrvEnd": "reserve_hosp_rsrv_end",
        "ReservePremRsrvEnd": "reserve_prem_rsrv_end",
        "ReserveTotal_End": "reserve_total_end",
        "ReserveUernPremEnd": "reserve_uern_prem_end",
        # Per-policy cells (Size... -> ..._pp)
        "SizeAnnPrem": "ann_prem_pp",
        "SizeBenefitAccDth": "claims_acc_dth_pp",
        "SizeBenefitAccHosp": "claims_acc_hosp_pp",
        "SizeBenefitAnn": "claims_ann_pp",
        "SizeBenefitDeath": "claims_death_pp",
        "SizeBenefitLiving": "claims_living_pp",
        "SizeBenefitMat": "claims_mat_pp",
        "SizeBenefitOther": "claims_other_pp",
        "SizeBenefitSickHosp": "claims_sick_hosp_pp",
        "SizeBenefitSurg": "claims_surg_pp",
        "SizeBenefitSurr": "claims_surr_pp",
        "SizeExpsAcq": "expense_acq_pp",
        "SizeExpsCommInit": "commissions_init_pp",
        "SizeExpsCommRen": "commissions_ren_pp",
        "SizeExpsMaint": "expense_maint_pp",
        "SizeExpsOther": "exps_other_pp",
        "SizeInvstIncome": "invst_income_pp",
        "SizePremium": "premium_pp",
        "SizeReservePremRsrvAftMat": "reserve_prem_rsrv_aft_mat_pp",
        "SizeReservePremRsrvEnd": "reserve_prem_rsrv_end_pp",
        "SizeReserveTotalAftMat": "reserve_total_aft_mat_pp",
        "SizeReserveUernPremAftMat": "reserve_uern_prem_aft_mat_pp",
        "SizeReserveUernPremEnd": "reserve_uern_prem_end_pp",
        "SizeSumAssured": "sum_assured",
        # Rates and helpers
        "BaseMortRate": "mort_rate",
        "GrossPremRate": "gross_prem_rate",
        "MortFactor": "mort_factor",
        "SurrRate": "lapse_rate",
        "AnnPremRate": "ann_prem_rate",
        "CashValueRate": "cash_value_rate",
        "NetPremRate": "net_prem_rate",
        "ReserveNLP_Rate": "reserve_nlp_rate",
        "SurrCharge": "surr_charge",
        "LastAge": "last_mort_age",
        "InflFactor": "inflation_factor",
        "DiscRate": "disc_rate",
        "last_t": "proj_len",
    },
    "CommTable": {
        "MortalityRates": "mortality_rates",
        "AnnDuenx": "AnnDuenx",
        "AnnDuex": "AnnDuex",
        "Ax": "Ax",
        "Axn": "Axn",
        "Cx": "Cx",
        "Dx": "Dx",
        "Exn": "Exn",
        "Mx": "Mx",
        "Nx": "Nx",
        "disc": "disc",
        "dx": "dx",
        "lx": "lx",
        "qx": "qx",
    },
    "Economic": {
        "DiscRate": "disc_rate",
        "InvstRetRate": "invst_ret_rate",
    },
    "Enums": {},
    "PV": {
        "InterestNetCF": "interest_net_cf",
        "PV_BenefitDeath": "pv_claims_death",
        "PV_BenefitMat": "pv_claims_mat",
        "PV_BenefitSurr": "pv_claims_surr",
        "PV_BenefitTotal": "pv_claims",
        "PV_Check": "pv_check",
        "PV_ExpsAcq": "pv_exps_acq",
        "PV_ExpsCommTotal": "pv_commissions",
        "PV_ExpsMaint": "pv_exps_maint",
        "PV_ExpsTotal": "pv_expenses",
        "PV_NetCashflow": "pv_net_cf",
        "PV_NetCashflowForCheck": "pv_net_cf_for_check",
        "PV_PremIncome": "pv_premiums",
        "PV_SumInsurIF": "pv_sum_insur_if",
    },
    "PolicyAttrs": {
        "GrossPremTable": "gross_prem_table",
        "InitSurrCharge": "init_surr_charge",
        "IntRate": "int_rate",
        "LoadAcqSA": "load_acq_sa",
        "LoadAcqSAParam1": "load_acq_sa_param1",
        "LoadAcqSAParam2": "load_acq_sa_param2",
        "LoadMaintPrem": "load_maint_prem",
        "LoadMaintPremParam1": "load_maint_prem_param1",
        "LoadMaintPremParam2": "load_maint_prem_param2",
        "LoadMaintPremWaiverPrem": "load_maint_prem_waiver_prem",
        "LoadMaintSA": "load_maint_sa",
        "LoadMaintSA2": "load_maint_sa2",
        "ReserveRate": "reserve_rate",
        "SurrChargeParam1": "surr_charge_param1",
        "SurrChargeParam2": "surr_charge_param2",
        "TableID": "table_id",
        "UernPremRate": "uern_prem_rate",
        "Product": "product",
        "PolicyType": "policy_type",
        "Gen": "gen",
        "Channel": "channel",
        "Sex": "sex",
        "Duration": "duration",
        "IssueAge": "issue_age",
        "PremFreq": "prem_freq",
        "PolicyTerm": "policy_term",
        "PolicyCount": "policy_count",
        "SumAssured": "sum_assured",
    },
    "Projection": {},
    "Utilities": {
        "pandas_to_array": "pandas_to_array",
        "map_to_policies": "map_to_policies",
    },
}

REF_NAME_MAPPING = {
    "Input": {
        "InputFileName": "input_file_name",
        "openpyxl": "openpyxl",
    },
    "Assumptions": {
        "AsmpLookup": "asmp_lookup",
        "Input": "input_data",
        "gen": "gen",
        "polt": "polt",
        "prod": "prod",
        "sex": "sex",
        "return_array": "return_array",
    },
    "BaseProj": {
        "scen": "scen",
        "asmp": "asmp",
        "pol": "pol",
        "comm_table": "comm_table",
    },
    "CommTable": {
        "MortalityTables2": "mortality_tables",
        "Sex": "Sex",
        "IntRate": "IntRate",
        "TableID": "TableID",
        "pol": "pol",
    },
    "Economic": {
        "Input": "input_data",
    },
    "PolicyAttrs": {
        "LifeTable": "life_table",
        "Input": "input_data",
        "PremTerm": "prem_term",
        "return_array": "return_array",
    },
    "Projection": {
        "scen": "scen",
        "asmp": "asmp",
        "pol": "pol",
        "comm_table": "comm_table",
    },
}

PARAM_NAME_MAPPING = {
    "Economic": {
        "ScenID": "scen_id",
    },
    "Projection": {
        "PolicyID": "idx",
        "ScenID": "scen_id",
    },
}


def _canonical_space(space):
    """Resolve space alias to its canonical model_new / TradLife_A key."""
    if space == "InputData":
        return "Input"
    return space


def map_space(space):
    """Return the TradLife_A space name for a model_new space name.

    If unchanged or not found, returns ``space``.
    """
    return SPACE_NAME_MAPPING.get(space, space)


def map_cell(space, cell_name):
    """Return the TradLife_A cell name for a model_new space and cell name.

    If unchanged or not found, returns ``cell_name``.
    """
    canon = _canonical_space(space)
    mapping = CELL_NAME_MAPPING.get(canon, {})
    return mapping.get(cell_name, cell_name)


def map_ref(space, ref_name):
    """Return the TradLife_A reference name for a space and reference name.

    If unchanged or not found, returns ``ref_name``.
    """
    canon = _canonical_space(space)
    mapping = REF_NAME_MAPPING.get(canon, {})
    return mapping.get(ref_name, ref_name)


def map_param(space, param_name):
    """Return the TradLife_A parameter name for a space and parameter name.

    If unchanged or not found, returns ``param_name``.
    """
    canon = _canonical_space(space)
    mapping = PARAM_NAME_MAPPING.get(canon, {})
    return mapping.get(param_name, param_name)


def map_name(space, name):
    """Map a cell, reference, or parameter name in ``space``.

    Checks cells first, then references, then parameters.
    If not found in any mapping, returns ``name`` unchanged.
    """
    canon = _canonical_space(space)
    if canon in CELL_NAME_MAPPING and name in CELL_NAME_MAPPING[canon]:
        return CELL_NAME_MAPPING[canon][name]
    if canon in REF_NAME_MAPPING and name in REF_NAME_MAPPING[canon]:
        return REF_NAME_MAPPING[canon][name]
    if canon in PARAM_NAME_MAPPING and name in PARAM_NAME_MAPPING[canon]:
        return PARAM_NAME_MAPPING[canon][name]
    return name


def reverse_map_cell(space, new_cell_name):
    """Return the model_new cell name given the TradLife_A cell name.

    If not found, returns ``new_cell_name``.
    """
    canon = _canonical_space(space)
    mapping = CELL_NAME_MAPPING.get(canon, {})
    for old_name, new_name in mapping.items():
        if new_name == new_cell_name:
            return old_name
    return new_cell_name


def get_space_mapping(space):
    """Return a combined dictionary of all mappings for a given space.

    Returns a dict with keys: ``'space'``, ``'cells'``, ``'refs'``,
    ``'params'``.
    """
    canon = _canonical_space(space)
    return {
        "space": map_space(canon),
        "cells": dict(CELL_NAME_MAPPING.get(canon, {})),
        "refs": dict(REF_NAME_MAPPING.get(canon, {})),
        "params": dict(PARAM_NAME_MAPPING.get(canon, {})),
    }
