

class FxType:
    Spot = 0
    Average = 1
    

class FxPeriod:
    NotApplicable = 0
    BeginningOfPeriod = 1
    Average = 2
    EndOfPeriod = 3


class CurrencyType:
    Functional = 0
    Group = 1
    Contractual = 2
    Transactional = 3


class PeriodType:
    NotApplicable = 'NotApplicable'      #0
    BeginningOfPeriod = 'BeginningOfPeriod'     #1
    EndOfPeriod = 'EndOfPeriod'                 #2


class ValuationPeriod:
    NotApplicable = 'NotApplicable'         # 0
    BeginningOfPeriod = 'BeginningOfPeriod' # 1
    MidOfPeriod = 'MidOfPeriod' # 2
    Delta = 'Delta'             # 3
    EndOfPeriod = 'EndOfPeriod' # 4


class PortfolioView:
    Gross = 1
    Reinsurance = 2
    Net = Gross | Reinsurance


class StructureType:
    None_ = 'None'      #0
    AoC = 'AoC'        #1


class State:
    Active = 0
    Inactive = 1
    

class Periodicity:
    Monthly = 0     # Default
    Quarterly = 1
    Yearly = 2
    

class InputSource:
    NotApplicable = 'NotApplicable' #0
    Opening = 'Opening' #1
    Actual = 'Actual' #2
    Cashflow = 'Cashflow'   #4


class DataType:
    Optional = 'Optional'
    Mandatory = 'Mandatory'
    Calculated = 'Calculated'
    CalculatedTelescopic = 'CalculatedTelescopic'


class ImportScope:
    Primary = 0
    Secondary = 1


