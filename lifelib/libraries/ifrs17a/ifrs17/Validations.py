"""Custom exception definitions"""

class NoMainTab(Exception):
    pass
class IncompleteMainTab(Exception):
    pass
class ParsingScientificNotation(Exception):
    pass
class ValueTypeNotFound(Exception):
    pass
class ValueTypeNotValid(Exception):
    pass

class ReportingNodeInMainNotFound(Exception):
    pass
class YearInMainNotFound(Exception):
    pass
class MonthInMainNotFound(Exception):
    pass
class AocTypeNotValid(Exception):
    pass
class AocTypeCompulsoryNotFound(Exception):
    pass
class AocTypePositionNotSupported(Exception):
    pass
class AocConfigurationOrderNotUnique(Exception):
    pass

# Partition(Exception):

class PartitionNotFound(Exception):
    pass
class ParsedPartitionNotFound(Exception):
    pass
class PartititionNameNotFound(Exception):
    pass
class PartitionTypeNotFound(Exception):
    pass

# Dimensions(Exception):
class AmountTypeNotFound(Exception):
    pass
class EstimateTypeNotFound(Exception):
    pass
class ReportingNodeNotFound(Exception):
    pass
class AocTypeMapNotFound(Exception):
    pass
class AocTypeNotFound(Exception):
    pass
class PortfolioGicNotFound(Exception):
    pass
class PortfolioGricNotFound(Exception):
    pass
class InvalidAmountTypeEstimateType(Exception):
    pass
class MultipleTechnicalMarginOpening(Exception):
    pass

# Exchange Rate(Exception):

class ExchangeRateNotFound(Exception):
    pass
class ExchangeRateCurrency(Exception):
    pass

# Data Note State(Exception):
class ChangeDataNodeState(Exception):
    pass
class InactiveDataNodeState(Exception):
    pass

# Parameters(Exception):
class ReinsuranceCoverageDataNode(Exception):
    pass
class DuplicateInterDataNode(Exception):
    pass
class DuplicateSingleDataNode(Exception):
    pass
class InvalidDataNode(Exception):
    pass

# Storage(Exception):
class DataNodeNotFound(Exception):
    pass
class PartnerNotFound(Exception):
    pass
class RatingNotFound(Exception):
    pass
class CreditDefaultRateNotFound(Exception):
    pass
class MissingPremiumAllocation(Exception):
    pass
class ReinsuranceCoverage(Exception):
    pass

class YieldCurveNotFound(Exception):
    pass
class YieldCurvePeriodNotApplicable(Exception):
    pass
class EconomicBasisNotFound(Exception):
    pass
class AccountingVariableTypeNotFound(Exception):
    pass

# Scopes(Exception):

class NotSupportedAocStepReference(Exception):
    pass
class MultipleEoP(Exception):
    pass

# Data completeness(Exception):

class MissingDataAtPosting(Exception):
    pass
class MissingCombinedLiability(Exception):
    pass
class MissingCoverageUnit(Exception):
    pass


