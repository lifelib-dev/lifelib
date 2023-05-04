import os
from ifrs17.DataStructure import *
from ifrs17.ImportScopeCalculation import IfrsWorkspace

thisdir = os.path.dirname(os.path.abspath(__file__))
filedir = os.path.join(thisdir, 'Files/present-values')

workspace = IfrsWorkspace()

result = workspace.import_with_type(os.path.join(filedir, "Dimensions.xlsx"), type_=[
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
workspace.import_with_format(os.path.join(filedir, "DataNodes_CH.xlsx"), format_=ImportFormats.DataNode)
workspace.import_with_format(os.path.join(filedir, "DataNodes_DE.xlsx"), format_=ImportFormats.DataNode)

workspace.import_with_type(os.path.join(filedir, "YieldCurve.xlsx"), type_=YieldCurve)
workspace.import_with_format(os.path.join(filedir, "Cashflows.xlsx"), format_=ImportFormats.Cashflow)
workspace.import_with_format(os.path.join(filedir, "CF_CH_2021_12.xlsx"), format_=ImportFormats.Cashflow)
workspace.import_with_format(os.path.join(filedir, "CF_DE_2021_12.xlsx"), format_=ImportFormats.Cashflow)
workspace.import_with_format(os.path.join(filedir, "CF_DE_2022_12.xlsx"), format_=ImportFormats.Cashflow)

# https://www.youtube.com/watch?v=bhtSm0cJudo&t=115s

# https://youtu.be/bhtSm0cJudo?t=475

vars = workspace.database.get_ifrsvars(add_goc_attrs=True)

df = vars[(vars['EconomicBasis']=='L') & (vars['EstimateType']=='BE') & (vars['ReportingNode']=='CH') & (vars['Year']==2021) & (vars['Month']==12)].set_index(['Novelty', 'AocType', 'AmountType'])['Value'].groupby(level=[0, 1, 2]).sum().unstack(level=2)

# # In-Force
#
# df.loc[(df['Year'] == 2022) & (df['EconomicBasis'] == 'L') & (df['AmountType'] == 'PR') & (df['Novelty'] == 'I')]
# df.loc[(df['Year'] == 2022) & (df['EconomicBasis'] == 'L') & (df['AmountType'] == 'CL') & (df['Novelty'] == 'I')]
#
# # New Business
#
# df.loc[(df['Year'] == 2022) & (df['EconomicBasis'] == 'L') & (df['AmountType'] == 'PR') & (df['Novelty'] == 'N')]
# df.loc[(df['Year'] == 2022) & (df['EconomicBasis'] == 'L') & (df['AmountType'] == 'CL') & (df['Novelty'] == 'N')]

