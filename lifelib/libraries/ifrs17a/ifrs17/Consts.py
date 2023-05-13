
# Numerical Precision
Precision = 1E-5
ProjectionPrecision = 1E-3
BenchmarkPrecision = 1E-4


# Time Period
CurrentPeriod: int = 0
PreviousPeriod: int = -1
MonthInAYear: int = 12


# Defaults
DefaultDataNodeActivationMonth: int = 1
DefaultPremiumExperienceAdjustmentFactor: float = 1.0


# Names
Main = 'Main'
Default = 'Default'
ValueType = 'ValueType'
GroupCurrency = 'CHF'


# Import Formats
class ImportFormats:
    Cashflow = 'Cashflow'                      # Importer for Nominal Cash flows
    Actual = 'Actual'                          # Importer for Actuals
    Opening = 'Opening'                        # Importer for Opening Balances (BOP Inforce of CSM/LC)
    SimpleValue = 'SimpleValue'                # Importer for Simple Values (pre-calculated direct import)
    DataNode = 'DataNode'                      # Importer for Data Node
    DataNodeState = 'DataNodeState'            # Importer for Data Node State
    DataNodeParameter = 'DataNodeParameter'    # Importer for Data Node Parameters
    AocConfiguration = 'AocConfiguration'      # Importer for Analysis of Change Configuration settings


# IFRS specific

class ValuationApproaches:
    BBA = 'BBA'     # Building Block Approach
    VFA = 'VFA'     # Variable Fee Approach
    PAA = 'PAA'     # Premium Allocation Approach


class LiabilityTypes:
    LRC = 'LRC'   # Liability for Remaining Coverage
    LIC = 'LIC'   # Liability Incurred Claims


class EstimateTypes:
    BE = 'BE'     #Best Estimate
    RA = 'RA'     #Risk Adjustment
    CU = 'CU'     #Coverage Units
    A = 'A'       #Actuals
    AA = 'AA'     #Advance Actuals
    OA = 'OA'     #Overdue Actuals
    DA = 'DA'     #Deferrable Actuals
    C = 'C'       #Contractual Service Margin
    L = 'L'       #Loss Component
    LR = 'LR'     #Loss Recovery
    F = 'F'       #Factors
    FCF = 'FCF'   #Fulfilment Cash flows
    BEPA = 'BEPA' #Experience Adjusted BE Premium to Csm
    APA = 'APA'   #Experience Adjusted Written Actual Premium to Csm


class AocTypes:
    BOP = 'BOP'     # Beginning of Period (opening value of an AOC chain)
    MC = 'MC'      # Model Corrections (changes to the model)
    PC = 'PC'       # Portfolio Changes
    RCU = 'RCU'    # Reinsurance Coverage Update
    CF = 'CF'      # Cash flow (Nominal)
    IA = 'IA'      # Interest Accretion
    AU = 'AU'       # Assumptions Update (changes to general assumptions)
    FAU = 'FAU'     # Financial Assumptions Update (changes to financial assumptions)
    YCU = 'YCU'    # Yield Curve Update
    CRU = 'CRU'    # Credit Default Risk Parameters Update
    WO = 'WO'      # Write-off
    EV = 'EV'      # Experience Variance
    CL = 'CL'      # Combined Liabilities (control run where all changes are calculated together for all novelties)
    EA = 'EA'      # Experience Adjustment
    AM = 'AM'      # Amortization
    FX = 'FX'      # Foreing Exchange
    EOP = 'EOP'     # End of Period (closing value of an AOC chain)


class Novelties:
    I = 'I'     #  In-Force
    N = 'N'     #  New Business
    C = 'C'     #  All Novelties Combined


class EconomicBases:
    L = 'L'     #  Locked Interest Rates
    C = 'C'     #  Current Interest Rates
    N = 'N'     #  Nominal Interest Rates


class AmountTypes:
    ACA = 'ACA'  #  Attributable Commissions Acquisition
    AEA = 'AEA'  #  Attributable Expenses Acquisition
    CDR = 'CDR'  #  Credit Default Risk
    CL = 'CL'    #  Claims
    PR = 'PR'    #  Premiums
    NIC = 'NIC'  #  Claims Non-Investment component
    ICO = 'ICO'  #  Claims Investment component
    NE = 'NE'    #  Non Attributable Expenses
    ACM = 'ACM'  #  Attributable Commissions Maintenance
    AEM = 'AEM'  #  Attributable Expenses Maintenance
    AC = 'AC'    #  Attributable Commissions
    AE = 'AE'    #  Attributable Expenses


class Scenarios:
    YCUP1pct = 'YCUP1pct'    # Yield Curve Up 1.0pct
    YCDW1pct = 'YCDW1pct'    # Yield Curve Down 1.0pct
    SRUP1pct = 'SRUP1pct'    # Spread Rate Up 1.0pct
    SRDW1pct = 'SRDW1pct'    # Spread Rate Down 1.0pct
    EUP1pct  = 'EUP1pct'     # Equity Up 1.0pct
    EDW1pct  = 'EDW1pct'     # Equity Down 1.0pct
    FXUP1pct = 'FXUP1pct'    # Exchange Rate Up 1.0pct
    FXDW1pct = 'FXDW1pct'    # Exchange Rate Down 1.0pct
    MTUP10pct= 'MTUP10pct'   # Mortality Up 10pct
    MTDW10pct= 'MTDW10pct'   # Mortality Down 10pct
    LUP10pct = 'LUP10pct'    # Longevity Up 10pct
    LDW10pct = 'LDW10pct'    # Longevity Down 10pct
    DUP10pct = 'DUP10pct'    # Disability Up 10pct
    DDW10pct = 'DDW10pct'    # Disability Down 10pct
    LICUP10pct = 'LICUP10pct'  # Lic Up 10pct
    LICDW10pct = 'LICDW10pct'  # Lic Down 10pct


# Insurance specific


class LineOfBusinesses:
    LI = 'LI'    #Life
    NL = 'NL'    #Non-Life







 