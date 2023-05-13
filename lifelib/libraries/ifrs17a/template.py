import os.path
from ifrs17.DataStructure import *
from ifrs17.ImportScopeCalculation import IfrsWorkspace

workspace = IfrsWorkspace()

thisdir = os.path.dirname(os.path.abspath(__file__))
filedir = os.path.join(thisdir, 'Files/ifrs17-template')

result = workspace.import_with_type(os.path.join(filedir, "Dimensions.xlsx"), type_=[
    ReportingNode,
    Novelty,
    AocType,
    PnlVariableType,
    BsVariableType,
    AmountType,
    DeferrableAmountType,
    RiskDriver,
    EconomicBasis,
    EstimateType,
    ValuationApproach,
    LineOfBusiness,
    OciType,
    LiabilityType,
    Profitability,
    Currency,
    Partner,
    CreditRiskRating,
    Scenario,
    ProjectionConfiguration
])


workspace.import_with_format(os.path.join(filedir, "Dimensions.xlsx"), format_=ImportFormats.AocConfiguration)

# Import Parameters

workspace.import_with_type(os.path.join(filedir, "YieldCurve.xlsx"), type_=YieldCurve)
workspace.import_with_type(os.path.join(filedir, "PartnerRating.xlsx"), type_=PartnerRating)
workspace.import_with_type(os.path.join(filedir, "CreditDefaultRate.xlsx"), type_=CreditDefaultRate)
workspace.import_with_format(os.path.join(filedir, "DataNodes_CH.xlsx"), format_=ImportFormats.DataNode)
workspace.import_with_format(os.path.join(filedir, "DataNodeStates_CH_2020_12.xlsx"), format_=ImportFormats.DataNodeState)
workspace.import_with_format(os.path.join(filedir, "DataNodeParameters_CH_2020_12.xlsx"), format_=ImportFormats.DataNodeParameter)


workspace.import_with_format(os.path.join(filedir, "Openings_CH_2020_12.xlsx"), format_=ImportFormats.Opening)
workspace.import_with_format(os.path.join(filedir, "SimpleValue_CH_2020_12.xlsx"), format_=ImportFormats.SimpleValue)
workspace.import_with_format(os.path.join(filedir, "NominalCashflows_CH_2020_12.xlsx"), format_=ImportFormats.Cashflow)
workspace.import_with_format(os.path.join(filedir, "Actuals_CH_2020_12.xlsx"), format_=ImportFormats.Actual)


workspace.import_with_format(os.path.join(filedir, "NominalCashflows_CH_2021_3.xlsx"), format_=ImportFormats.Cashflow)
workspace.import_with_format(os.path.join(filedir, "Actuals_CH_2021_3.xlsx"), format_=ImportFormats.Actual)

ifrsvars = workspace.database.get_ifrsvars(add_goc_attrs=True)
