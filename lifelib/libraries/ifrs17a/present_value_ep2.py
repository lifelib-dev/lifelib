import os
from ifrs17.DataStructure import *
from ifrs17.ImportScopeCalculation import IfrsWorkspace

thisdir = os.path.dirname(os.path.abspath(__file__))
filedir = os.path.join(thisdir, 'Files/present-values')

workspace = IfrsWorkspace()

workspace.import_with_type(os.path.join(filedir, "Dimensions.xlsx"), type_=[
    ReportingNode,
    AocType,
    DeferrableAmountType,
    AmountType,
    Scenario,
    LiabilityType,
    LineOfBusiness,
    EstimateType,
    EconomicBasis,
    Currency,
    PnlVariableType,
    BsVariableType,
    Novelty,
    Profitability,
    OciType,
    ValuationApproach,
    RiskDriver,
    ProjectionConfiguration,
    ExchangeRate
])

workspace.import_with_format(os.path.join(filedir, "Dimensions.xlsx"), format_=ImportFormats.AocConfiguration)
workspace.import_with_format(os.path.join(filedir, "DataNodes.xlsx"), format_=ImportFormats.DataNode)
workspace.import_with_type(os.path.join(filedir, "YieldCurve.xlsx"), type_=YieldCurve)

workspace.import_with_format(os.path.join(filedir, "Cashflows.xlsx"), format_=ImportFormats.Cashflow)

vars = workspace.database.get_ifrsvars()

df = vars[(vars['EconomicBasis']=='L') & (vars['EstimateType']=='BE')].set_index(['Novelty', 'AocType', 'AmountType'])['Value'].groupby(level=[0, 1, 2]).sum().unstack(level=2)

# https://youtu.be/dhdA3F6ZWbs?t=448