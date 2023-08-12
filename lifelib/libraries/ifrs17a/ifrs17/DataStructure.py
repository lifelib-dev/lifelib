from functools import (
    total_ordering as _total_ordering,
    cached_property as _cached_property
)
import dataclasses as _dataclasses
from dataclasses import (dataclass as _dataclass, field as _field)
from collections import namedtuple as _namedtuple
from .BaseClasses import *
from .Consts import *
from .Enums import *

# Data Infrastructure

## Base Interfaces

@_dataclass
class IKeyed(metaclass=IKeyedType):
    Id: Guid


@_dataclass
class IPartitioned:
    Partition: Guid


@_dataclass
class IWithYearAndMonth:
    Year: int
    Month: int


@_dataclass
class IWithYearMonthAndScenario(IWithYearAndMonth):
    Scenario: str


## Abstract Classes

class KeyedRecord(IKeyed):
    pass


@_dataclass
class KeyedDimension(INamed):
    SystemName: str
    DisplayName: str


@_dataclass
class KeyedOrderedDimension(KeyedDimension, IOrdered):
    Order: int


@_dataclass
class KeyedOrderedDimensionWithExternalId(KeyedOrderedDimension):
    ExternalId: list[str]


# Dimensions


@_dataclass
class HierarchicalDimensionWithLevel:
    SystemName: str
    DisplayName: str
    Parent: str
    Level: int


## Amount Type

@_dataclass
class AmountType(KeyedOrderedDimensionWithExternalId):
    Parent: str
    PeriodType: PeriodType


class DeferrableAmountType(AmountType):
    pass


## Risk Driver
@_dataclass
class RiskDriver(KeyedOrderedDimension):
    Parent: str


## Estimate Type
@_dataclass
class EstimateType(KeyedOrderedDimensionWithExternalId): 
    InputSource: InputSource
    StructureType: StructureType
    PeriodType: PeriodType


## Novelty
class Novelty(KeyedOrderedDimension):
    pass


## Variable Type
@_dataclass
class VariableType(KeyedOrderedDimension):
    Parent: str


### AoC Variable Type
@_dataclass
class AocType(VariableType): 
    PnlType: str = ''


AocStep = _namedtuple('AocStep', ['AocType', 'Novelty'])


class PnlVariableType(VariableType):
    pass


class BsVariableType(VariableType):
    pass


class AccountingVariableType(VariableType):
    pass


## Scenario
class Scenario(KeyedDimension):
    pass


## Line Of Business
@_dataclass
class LineOfBusiness(KeyedOrderedDimension):
    Parent: str


## Currency
class Currency(KeyedDimension):
    pass


## Economic Basis
class EconomicBasis(KeyedDimension):
    pass


## Valuation Approach
class ValuationApproach(KeyedDimension):
    pass


## Liability Type
@_dataclass
class LiabilityType(KeyedDimension):
    Parent: str


## OCI Type

class OciType(KeyedDimension):
    pass


## Profitability

class Profitability(KeyedDimension):
    pass

## Partner


class Partner(KeyedDimension):
    pass

## Credit Risk Rating


class CreditRiskRating(KeyedDimension):
    pass

## Reporting Node

@_dataclass
class ReportingNode(KeyedDimension):
    Parent: str
    Currency: str


@_dataclass
class ProjectionConfiguration(KeyedDimension):
    Shift: int
    TimeStep: int


@_dataclass
class AocConfiguration(KeyedRecord, IWithYearAndMonth, IOrdered):

    Year: int
    Month: int
    AocType: str
    Novelty: str
    DataType: DataType
    InputSource: InputSource
    FxPeriod: FxPeriod
    YcPeriod: PeriodType
    CdrPeriod: PeriodType
    ValuationPeriod: ValuationPeriod
    RcPeriod: PeriodType
    Order: int


@_dataclass
class ExchangeRate(KeyedRecord, IWithYearMonthAndScenario):

    Currency: str
    Year: int
    Month: int
    FxType: FxType
    FxToGroupCurrency: float
    # Scenario: str = ''


@_dataclass
class CreditDefaultRate(KeyedRecord, IWithYearMonthAndScenario): 

    CreditRiskRating: str
    Year: int
    Month: int
    Values: list[float]
    # Scenario: str = ''


@_dataclass
class YieldCurve(KeyedRecord, IWithYearMonthAndScenario):

    Currency: str
    Year: int
    Month: int
    Name: str
    Values: list[float]
    # Scenario: str = ''

@_dataclass
class PartnerRating(KeyedRecord, IWithYearMonthAndScenario): 

    Partner: str
    CreditRiskRating: str
    Year: int
    Month: int
    # Scenario: str = ''


# Partitions
@_dataclass
class IfrsPartition(IKeyed):
    ReportingNode: str
    Scenario: str = ''


class PartitionByReportingNode(IfrsPartition):
    pass


@_total_ordering
@_dataclass
class PartitionByReportingNodeAndPeriod(IfrsPartition):
    Year: int = 0
    Month: int = 0

    def __hash__(self):
        return hash((self.Id, self.ReportingNode, self.Scenario, self.Year, self.Month))

    def __eq__(self, other):
        return (self.Id, self.ReportingNode, self.Scenario, self.Year, self.Month) == (
            other.Id, other.ReportingNode, other.Scenario, other.Year, other.Month)

    def __lt__(self, other):
        return ((self.Id, self.ReportingNode, self.Scenario, self.Year, self.Month) < (
            other.Id, other.ReportingNode, other.Scenario, other.Year, other.Month))


# Policy-related Data Structures


@_dataclass
class DataNode(KeyedDimension, IPartitioned): 

    Partition: Guid
    ContractualCurrency: str
    FunctionalCurrency: str
    LineOfBusiness: str
    ValuationApproach: str
    OciType: str


@_dataclass
class Portfolio(DataNode): 
    pass


@_dataclass
class InsurancePortfolio(Portfolio):
    pass 


@_dataclass
class ReinsurancePortfolio(Portfolio):
    pass


@_dataclass(eq=False)
class GroupOfContract(DataNode):

    AnnualCohort: int
    LiabilityType: str
    Profitability: str
    Portfolio: str
    YieldCurveName: str
    Partner: str
    IsReinsurance: bool


@_dataclass(eq=False)
class GroupOfInsuranceContract(GroupOfContract): 
    pass
    # [Immutable]

    #  TODO: for the case of internal reinsurance the Partner would be the reporting node, hence not null.
    #  If this is true we need the [Required] attribute here, add some validation at dataNode import 
    #  and to add logic in the GetNonPerformanceRiskRate method in ImportStorage.


@_dataclass(eq=False)
class GroupOfReinsuranceContract(GroupOfContract):
    pass


@_dataclass
class DataNodeState(KeyedRecord, IPartitioned, IWithYearMonthAndScenario): 

    Partition: Guid
    DataNode: str
    Year: int
    Month: int      # = DefaultDataNodeActivationMonth
    State: State    # = State.Active
    # Scenario: str = ''


@_dataclass
class DataNodeParameter(KeyedRecord, IPartitioned, IWithYearMonthAndScenario):

    Partition: Guid
    Year: int
    Month: int  # = DefaultDataNodeActivationMonth
    DataNode: str
    # Scenario: str


@_dataclass
class SingleDataNodeParameter(DataNodeParameter):
    PremiumAllocation: float = DefaultPremiumExperienceAdjustmentFactor


@_dataclass
class InterDataNodeParameter(DataNodeParameter):
    LinkedDataNode: str
    ReinsuranceCoverage: float
    Scenario: str

    def __hash__(self):
        return hash((self.LinkedDataNode, self.ReinsuranceCoverage, self.Scenario))

    def __eq__(self, other):
        return (self.LinkedDataNode, self.ReinsuranceCoverage, self.Scenario) == (
            other.LinkedDataNode, other.ReinsuranceCoverage, other.Scenario)


@_dataclass
class DataNodeData:

    DataNode: str

    # Portfolio

    ContractualCurrency: str
    FunctionalCurrency: str
    LineOfBusiness: str
    ValuationApproach: str
    OciType: str

    # GroupOfContract

    Portfolio: str
    AnnualCohort: int
    LiabilityType: str
    Profitability: str
    Partner: str

    # DataNodeState

    Year: int
    Month: int
    State: State
    PreviousState: State
    IsReinsurance: bool
    Scenario: str


## Variables

@_dataclass
class BaseVariableIdentity:
    DataNode: str
    AocType: str
    Novelty: str


@_dataclass
class BaseDataRecord(BaseVariableIdentity, IKeyed, IPartitioned):
    AmountType: str
    AccidentYear: int


@_dataclass
class RawVariable(BaseDataRecord):
    Values: list[float]
    EstimateType: str


@_total_ordering
@_dataclass
class IfrsVariable(BaseDataRecord):
    Value: float
    EstimateType: str
    EconomicBasis: str = _field(default='')

    def __hash__(self):
        return hash((self.DataNode, self.AocType, self.Novelty, self.AmountType, self.AccidentYear, self.EstimateType, self.EconomicBasis))

    def __eq__(self, other):
        if eq := self.Id == other.Id:
            assert hash(self) == hash(other)
        return eq

    def __lt__(self, other):
        return ((self.DataNode, self.AocType, self.Novelty, self.AmountType, self.AccidentYear, self.EstimateType, self.EconomicBasis, self.Id) < (
            other.DataNode, other.AocType, other.Novelty, other.AmountType, other.AccidentYear, other.EstimateType, other.EconomicBasis, self.Id))

# Import Identity

ImportIdentityTuple = _namedtuple('ImportIdentityTuple', ['DataNode', 'AocType', 'Novelty'])


@_total_ordering
@_dataclass
class ImportIdentity(BaseVariableIdentity):

    IsReinsurance: bool = False
    ValuationApproach: str = ''
    ProjectionPeriod: int = 0
    ImportScope: ImportScope = None

    def __hash__(self):
        return hash((self.DataNode, self.AocType, self.Novelty))

    def __eq__(self, other):
        return (self.DataNode, self.AocType, self.Novelty) == (
            other.DataNode, other.AocType, other.Novelty)

    def __lt__(self, other):
        return ((self.DataNode, self.AocType, self.Novelty) < (
            other.DataNode, other.AocType, other.Novelty))

    @_cached_property
    def AocStep(self) -> AocStep:
        return AocStep(self.AocType, self.Novelty)

    @classmethod
    def from_iv(cls, iv) -> 'ImportIdentity':
        return cls(
            DataNode=iv.DataNode,
            AocType=iv.AocType,
            Novelty=iv.Novelty)

    @classmethod
    def from_rv(cls, rv) -> 'ImportIdentity':
        return cls(
            DataNode=rv.DataNode,
            AocType=rv.AocType,
            Novelty=rv.Novelty)

    def to_tuple(self):
        return ImportIdentityTuple(DataNode=self.DataNode, AocType=self.AocType, Novelty=self.Novelty)

    def to_dict(self):
        return {'DataNode': self.DataNode, 'AocType': self.AocType, 'Novelty': self.Novelty}

    def copy(self, DataNode:str=None, Novelty:str=None, AocType: str=None, IsReinsurance=None):
        other = _dataclasses.replace(self)
        if 'AocStep' in other.__dict__:
            del other.__dict__['AocStep']
        if DataNode is not None:
            other.DataNode = DataNode
        if AocType is not None:
            other.AocType = AocType
        if Novelty is not None:
            other.Novelty = Novelty
        if IsReinsurance is not None:
            other.IsReinsurance = IsReinsurance

        return other


# Args

@_dataclass(frozen=True, eq=True, unsafe_hash=True)
class Args:
    ReportingNode: str
    Year: int
    Month: int
    Periodicity: Periodicity
    Scenario: str


@_dataclass(frozen=True, eq=True, unsafe_hash=True)
class ImportArgs(Args):
    ImportFormat: ImportFormats




