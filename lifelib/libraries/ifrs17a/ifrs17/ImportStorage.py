import dataclasses
from collections import namedtuple
from typing import Collection, Union, Callable, Optional
from functools import cached_property
from .DataStructure import *
from .Database import IfrsDatabase
from .Validations import *

__all__ = ('ImportStorage',)

YearMonth = namedtuple('YearMonth', ['Year', 'Month'])


class ImportStorage:

    database: IfrsDatabase
    args: ImportArgs
    

    # Constants

    @cached_property
    def periodicityInMonths(self) -> int:
        return 3 # Revisit

    #Format

    @cached_property
    def ImportFormat(self) -> str:
        return self.args.ImportFormat

    #Time Periods 

    @cached_property
    def CurrentReportingPeriod(self) -> YearMonth:
        return YearMonth(self.args.Year, self.args.Month)

    @cached_property
    def PreviousReportingPeriod(self)  -> YearMonth:
        return YearMonth(self.args.Year - 1, MonthInAYear)     # YTD Logic


    #Partitions

    PartitionByRn: Guid
    TargetPartition: Guid
    DefaultPartition: Guid
    PreviousPeriodPartition: Guid

    #Projections

    ProjectionConfiguration: list[ProjectionConfiguration]

    #DataNodes

    DataNodeDataBySystemName: dict[str, DataNodeData]
    DataNodesByImportScope: dict[ImportScope, set[str]]
    AccidentYearsByDataNode: dict[str, Collection[int]]

    #Variables

    RawVariablesByImportIdentity: dict[str, Collection[RawVariable]]
    IfrsVariablesByImportIdentity: dict[str, Collection[IfrsVariable]]

    #Parameters

    LockedInYieldCurve: dict[str, YieldCurve]
    CurrentYieldCurve: dict[str, dict[int, YieldCurve]]
    PartnerRating: dict[str, dict[int, PartnerRating]]
    CreditDefaultRates: dict[str, dict[int, CreditDefaultRate]]
    SingleDataNodeParametersByGoc: dict[str, dict[int, SingleDataNodeParameter]]
    InterDataNodeParametersByGoc: dict[str, dict[int, set[InterDataNodeParameter]]]
    AocConfigurationByAocStep: dict[AocStep, AocConfiguration]

    aocStepByInputSource: dict[InputSource, set[AocStep]]

    #Dimensions

    AmountTypeDimension: dict[str, AmountType]
    NoveltyDimension: dict[str, Novelty]
    EstimateTypeDimension: dict[str, EstimateType]
    EstimateTypesByImportFormat: dict[str, set[str]]
    ExperienceAdjustEstimateTypeMapping: dict[str, str]

    def __init__(self, args: ImportArgs, database: IfrsDatabase):

        self.database: IfrsDatabase = database
        self.args: ImportArgs = args

        ## Initialize

        #Dimensions

        estimateTypes = self.database.Query(EstimateType)

        self.EstimateTypeDimension     = {x.SystemName: x for x in estimateTypes}
        self.AmountTypeDimension       = {x.SystemName: x for x in self.database.Query(AmountType)}
        self.NoveltyDimension          = {x.SystemName: x for x in self.database.Query(Novelty)}

        self.ExperienceAdjustEstimateTypeMapping = {EstimateTypes.A: EstimateTypes.APA}    #TODO move this logic

        #Hierarchy Cache

        # await hierarchyCache.InitializeAsync<AmountType>()

        #EstimateType to load and to update

        temp = [InputSource.Opening, InputSource.Actual, InputSource.Cashflow]
        temp2 = {}
        for x in temp:
            temp2[str(x)] = {et.SystemName for et in estimateTypes if x in et.InputSource}

        self.EstimateTypesByImportFormat = temp2

        # self.EstimateTypesByImportFormat = {str(x): [et.SystemName for et in estimateTypes if x in et.InputSource] for x in [InputSource.Opening, InputSource.Actual, InputSource.Cashflow]}

        #ProjectionConfiguration : Current Period + projection for every Quarter End for current Year and next Years as in projectionConfiguration.csv

        self.ProjectionConfiguration = sorted([x for x in self.database.Query(ProjectionConfiguration)
         if x.Shift > 0 or x.TimeStep == self.args.Month or (x.TimeStep > self.args.Month and x.TimeStep % self.periodicityInMonths == 0)],
               key=lambda x: x.Shift * 100 + x.TimeStep)

        #Get Partitions

        if len(temp := [p for p in self.database.Query(PartitionByReportingNode) if p.ReportingNode == self.args.ReportingNode]) != 1:
            raise ValueError('Not a single element list')
        self.PartitionByRn = temp[0].Id

        if len(temp := [p for p in self.database.Query(PartitionByReportingNodeAndPeriod) if
                        p.ReportingNode == self.args.ReportingNode and
                        p.Year == self.CurrentReportingPeriod.Year and
                        p.Month == self.CurrentReportingPeriod.Month and
                        p.Scenario == self.args.Scenario]) != 1:
            raise ValueError
        self.TargetPartition = temp[0].Id

        if len(temp := [p for p in self.database.Query(PartitionByReportingNodeAndPeriod) if p.ReportingNode == self.args.ReportingNode and
                                                                                             p.Year == self.CurrentReportingPeriod.Year and
                                                                                             p.Month == self.CurrentReportingPeriod.Month and
                                                                                             not p.Scenario]) != 1:
            raise ValueError('Not a single element')

        self.DefaultPartition = temp[0].Id

        #Set Partitions

        self.database.Partition.Set(PartitionByReportingNode, self.PartitionByRn)
        self.database.Partition.Set(PartitionByReportingNodeAndPeriod, self.TargetPartition)

        #Get data from Workspace (result of parsing)

        parsedRawVariables = self.database.Query(RawVariable, partition=self.TargetPartition)
        parsedIfrsVariables = self.database.Query(IfrsVariable, partition=self.TargetPartition)

        #DataNodes

        self.DataNodeDataBySystemName = self.database.LoadDataNodes(self.args)

        #Accident Years

        result = {}
        if self.ImportFormat == ImportFormats.Cashflow:
            for x in parsedRawVariables:
                result.setdefault(x.DataNode, set()).add(x.AccidentYear)
        else:
            for x in parsedIfrsVariables:
                result.setdefault(x.DataNode, set()).add(x.AccidentYear)

        self.AccidentYearsByDataNode = result

        # Import Scopes and Data Node relationship parameters

        self.InterDataNodeParametersByGoc = self.database.LoadInterDataNodeParameters(self.args)

        primaryScopeFromParsedVariables =  set(x.DataNode for x in parsedRawVariables) if self.ImportFormat == ImportFormats.Cashflow else set(x.DataNode for x in parsedIfrsVariables)

        temp = set(goc for goc in primaryScopeFromParsedVariables if not self.DataNodeDataBySystemName[goc].IsReinsurance and
                                                self.DataNodeDataBySystemName[goc].LiabilityType == LiabilityTypes.LRC)

        primaryScopeFromLinkedReinsurance = set()
        for goc in temp:
            if interDataNodeParamByPeriod := self.InterDataNodeParametersByGoc.get(goc, None):
                temp2 = set(param.LinkedDataNode if param.DataNode == goc else param.DataNode  for param in interDataNodeParamByPeriod[CurrentPeriod] if goc not in primaryScopeFromParsedVariables)
            else:
                temp2 = set()
            primaryScopeFromParsedVariables |= temp2


        primaryScope = primaryScopeFromParsedVariables | primaryScopeFromLinkedReinsurance

        temp = {k: v for k, v in self.InterDataNodeParametersByGoc.items() if k in primaryScope}
        secondaryScope = set()
        for key, val in temp.items():
            temp = set(
                param.LinkedDataNode if param.DataNode == key else param.DataNode for param in val[CurrentPeriod])
            secondaryScope |= set(goc for goc in temp if goc not in primaryScope)

        allImportScopes = primaryScope | secondaryScope
        self.DataNodesByImportScope = { ImportScope.Primary: primaryScope, ImportScope.Secondary: secondaryScope }

        # Parameters

        self.PartnerRating = self.database.LoadCurrentAndPreviousParameter(PartnerRating, self.args, lambda x :x.Partner)
        self.CreditDefaultRates = self.database.LoadCurrentAndPreviousParameter(CreditDefaultRate, self.args, lambda x: x.CreditRiskRating)
        self.SingleDataNodeParametersByGoc = self.database.LoadSingleDataNodeParameters(self.args)
        self.LockedInYieldCurve = self.database.LoadLockedInYieldCurve(self.args, [self.DataNodeDataBySystemName[dn] for dn in allImportScopes])
        self.CurrentYieldCurve = self.database.LoadCurrentYieldCurve(self.args, [self.DataNodeDataBySystemName[dn] for dn in allImportScopes])        #TODO Rename this variable
        self.AocConfigurationByAocStep = self.database.LoadAocStepConfigurationAsDictionary(self.args.Year, self.args.Month)
        self.aocStepByInputSource = {}

        temp = [v for k, v in InputSource.__dict__.items() if k[0] != '_']
        for x in temp:
            self.aocStepByInputSource[x] = {k for k, v in self.AocConfigurationByAocStep.items() if x in v.InputSource}

        #Previous Period

        openingRawVariables: list[RawVariable] = []
        openingIfrsVariables: list[IfrsVariable] = []

        temp = [self.DataNodeDataBySystemName[dn] for dn in allImportScopes]
        allImportScopesAtInceptionYear = {dnd.DataNode for dnd in temp if dnd.Year == self.args.Year}
        allImportScopesNotAtInceptionYear = allImportScopes - allImportScopesAtInceptionYear

        if allImportScopesNotAtInceptionYear:

            temp = [p for p in self.database.Query(PartitionByReportingNodeAndPeriod)
                if (p.ReportingNode == self.args.ReportingNode and p.Year == self.PreviousReportingPeriod.Year and
                    p.Month == self.PreviousReportingPeriod.Month and not p.Scenario)]

            assert len(temp) == 1
            self.PreviousPeriodPartition = temp[0].Id

            self.database.Partition.Set(PartitionByReportingNodeAndPeriod, self.PreviousPeriodPartition)

            #Perform queries to previous Period

            temp = [rv for rv in self.database.Query(RawVariable) if rv.Partition == self.PreviousPeriodPartition and rv.AocType == AocTypes.CL]
            temp = [v for v in temp if v.DataNode in primaryScope]
            openingRawVariables = []
            for rv in temp:
                x = dataclasses.replace(rv)
                x.AocType = AocTypes.BOP
                x.Novelty = Novelties.I
                x.Values = rv.Values[MonthInAYear:]
                x.Partition = self.TargetPartition
                openingRawVariables.append(x)

            temp = [iv for iv in self.database.Query(IfrsVariable) if iv.Partition == self.PreviousPeriodPartition and iv.AocType == AocTypes.EOP]
            temp = [v for v in temp if v.DataNode in allImportScopesNotAtInceptionYear]
            openingIfrsVariables = []
            for iv in temp:
                x = dataclasses.replace(iv)
                x.AocType = AocTypes.BOP
                x.Novelty = Novelties.I
                x.Partition = self.TargetPartition
                openingIfrsVariables.append(x)

            # TODO: print error if

            #openingRawVariables.Select(x => x.DataNode).ToHashSet() != dataNodesWithPreviousPeriod


        #SetPartition to current Period

        self.database.Partition.Set(PartitionByReportingNodeAndPeriod, self.TargetPartition)

        primaryScopeAtInceptionYear = {dn for dn in allImportScopesAtInceptionYear if dn in primaryScope}
        secondaryScopeAtInceptionYear = {dn for dn in allImportScopesAtInceptionYear if dn in secondaryScope}
        if allImportScopesAtInceptionYear and self.ImportFormat != ImportFormats.Opening:

            temp = [iv for iv in self.database.Query(IfrsVariable) if
                    iv.Partition == self.TargetPartition and iv.AocType == AocTypes.BOP and iv.Novelty == Novelties.I]
            temp = [iv for iv in temp if iv.DataNode in primaryScopeAtInceptionYear
                            and iv.EstimateType in self.EstimateTypesByImportFormat["Opening"]
                            or iv.DataNode in secondaryScopeAtInceptionYear]
            openingIfrsVariables.extend(temp)

        #Variables

        rawVariables = parsedRawVariables + openingRawVariables + [rv for rv in self.database.Query(RawVariable)
                                                                   if rv.Partition == self.TargetPartition and rv.DataNode in primaryScopeFromLinkedReinsurance]

        ifrsVariables = parsedIfrsVariables + openingIfrsVariables + [iv for iv in self.database.Query(IfrsVariable)
                                                                      if iv.Partition == self.TargetPartition
                                                                      and not (iv.AocType == AocTypes.BOP and iv.Novelty == Novelties.I)
                                                                      and (iv.DataNode in primaryScopeFromParsedVariables
                                                                      and not iv.EstimateType in self.EstimateTypesByImportFormat[self.ImportFormat]
                                                                      or iv.DataNode in primaryScopeFromLinkedReinsurance
                                                                      or iv.DataNode in secondaryScope)]


        if(self.DefaultPartition != self.TargetPartition):

            self.database.Partition.Set(PartitionByReportingNodeAndPeriod, self.DefaultPartition)
            defaultRawVariables = [rv for rv in self.database.Query(RawVariable) if rv.Partition == self.DefaultPartition and rv.DataNode in primaryScope]
            defaultIfrsVariables = [iv for iv in self.database.Query(IfrsVariable) if iv.Partition == self.DefaultPartition and
                                    (iv.DataNode in primaryScopeFromParsedVariables
                and not iv.EstimateType in self.EstimateTypesByImportFormat[self.ImportFormat]
                or iv.DataNode in primaryScopeFromLinkedReinsurance
                or iv.DataNode in secondaryScope)]

            def _rawVariablesCompare(x: RawVariable,  y: RawVariable, ignoreValues:bool=False):
                if (x.AccidentYear == y.AccidentYear and x.AmountType == y.AmountType and x.DataNode == y.DataNode and x.AocType == y.AocType and
                        x.Novelty == y.Novelty and x.EstimateType == y.EstimateType):
                    if ignoreValues:
                        return True
                    else:
                        if len(x.Values) != len(y.Values):
                            return False
                        for i in range(len(x.Values)):
                            if x.Values[i] != y.Values[i]:
                                return False
                        return True
                else:
                    return False

            def _ifrsVariablesCompare(x: IfrsVariable,  y: IfrsVariable, ignoreValues:bool=False):
                if (x.AccidentYear == y.AccidentYear and x.AmountType == y.AmountType and x.DataNode == y.DataNode and x.AocType == y.AocType and
                        x.Novelty == y.Novelty and x.EstimateType == y.EstimateType):
                    if ignoreValues:
                        return True
                    else:
                        if x.Value == y.Value:
                            return False
                        else:
                            return True
                else:
                    return False

            for drv in defaultRawVariables:
                if all(_rawVariablesCompare(drv, rv) for rv in rawVariables):
                    rawVariables.append(drv)

            for div in defaultIfrsVariables:
                if all(_ifrsVariablesCompare(div, iv) for iv in ifrsVariables):
                    ifrsVariables.append(div)

            self.database.Partition.Set(PartitionByReportingNodeAndPeriod, self.TargetPartition)

        self.RawVariablesByImportIdentity = {}
        for v in rawVariables:
            self.RawVariablesByImportIdentity.setdefault(v.DataNode, []).append(v)

        self.IfrsVariablesByImportIdentity = {}
        for v in ifrsVariables:
            self.IfrsVariablesByImportIdentity.setdefault(v.DataNode, []).append(v)

    #Getters

    #Periods

    def GetValuationPeriod(self, id_: ImportIdentity) -> ValuationPeriod:
        return self.AocConfigurationByAocStep[AocStep(id_.AocType, id_.Novelty)].ValuationPeriod

    def GetYieldCurvePeriod(self, id_: ImportIdentity) -> PeriodType:
        return self.AocConfigurationByAocStep[AocStep(id_.AocType, id_.Novelty)].YcPeriod
    
    def GetCreditDefaultRiskPeriod(self, id_: ImportIdentity) -> PeriodType:
        return self.AocConfigurationByAocStep[AocStep(id_.AocType, id_.Novelty)].CdrPeriod

    def GetAllAocSteps(self, source: InputSource) -> set[AocStep]:
        return self.aocStepByInputSource[source]
    
    def GetCalculatedTelescopicAocSteps(self) -> list[AocStep]:
        return [k for k, v in self.AocConfigurationByAocStep.items() if v.DataType == DataType.CalculatedTelescopic]

    #YieldCurve

    def GetYearlyYieldCurve(self, id_: ImportIdentity, economicBasis: str) -> list[float]:
        yc = self.GetYieldCurve(id_, economicBasis)
        return yc.Values[self.args.Year - yc.Year:]   #Check if the returned array is empty? Log Warning?

    def GetYieldCurve(self, id_: ImportIdentity, economicBasis: str) -> YieldCurve:
        
        if (economicBasis, self.GetYieldCurvePeriod(id_)) == (EconomicBases.C, PeriodType.BeginningOfPeriod):
            return self.CurrentYieldCurve[self.DataNodeDataBySystemName[id_.DataNode].ContractualCurrency][PreviousPeriod]
        elif (economicBasis, self.GetYieldCurvePeriod(id_)) == (EconomicBases.C, PeriodType.EndOfPeriod):
            return self.CurrentYieldCurve[self.DataNodeDataBySystemName[id_.DataNode].ContractualCurrency][CurrentPeriod]
        elif economicBasis == EconomicBases.L:
            return self.LockedInYieldCurve[id_.DataNode]
        elif self.GetYieldCurvePeriod(id_) == PeriodType.NotApplicable:
            raise YieldCurvePeriodNotApplicable
        else:
            raise EconomicBasisNotFound

    #int Identity.ProjectionPeriod 

    def GetProjectionCount(self) -> int:
        return len(self.ProjectionConfiguration)

    def GetShift(self, projectionPeriod: int) -> int:
        return self.ProjectionConfiguration[projectionPeriod].Shift

    def GetTimeStep(self, projectionPeriod: int) -> int:
        return self.ProjectionConfiguration[projectionPeriod].TimeStep

    def GetPeriodType(self, amountType: str, estimateType: str) -> PeriodType:
        at_ = self.AmountTypeDimension.get(amountType, None)
        if amountType and at_:
            return at_.PeriodType
        else:
            ct = self.EstimateTypeDimension.get(estimateType, None)
            if estimateType and ct:
                return ct.PeriodType
            else:
                return PeriodType.EndOfPeriod

    #Variables and Cash flows

    def GetRawVariables(self, dataNode: str) -> list[RawVariable]:

        return self.RawVariablesByImportIdentity.get(dataNode, [])

    def GetIfrsVariables(self, dataNode: str) -> list[IfrsVariable]:
        return list(v for v in self.IfrsVariablesByImportIdentity.get(dataNode, []) if v.Partition == self.TargetPartition)

    def GetIfrsVariable(self,
                 id_: ImportIdentity,
                 amountType: str,
                 estimateType: str,
                 economicBasis: str,
                 accidentYear: int
                 ) -> Union[IfrsVariable, None]:
        vars = list(v for v in self.database.Query(IfrsVariable, include_sub=False) if (
                v.DataNode == id_.DataNode
                and v.Partition == self.TargetPartition
                and v.AocType == id_.AocType and v.Novelty == id_.Novelty
                and v.AccidentYear == accidentYear and v.AmountType == amountType
                and v.EstimateType == estimateType and v.EconomicBasis == economicBasis))

        assert len(vars) < 2
        return vars[0] if vars else None

    def GetValues(self, id_: ImportIdentity, whereClause: Callable[[RawVariable], bool]) -> list[float]:

        temp = [v for v in self.GetRawVariables(id_.DataNode) if (v.AocType, v.Novelty) == id_.AocStep and whereClause(v)]
        return temp[-1].Values if temp else []

    def GetValues2(self, id_: ImportIdentity, amountType: str, estimateType: str, accidentYear: int) -> list[float]:
        return self.GetValues(id_, lambda v: (v.AccidentYear == accidentYear and v.AmountType == amountType and v.EstimateType == estimateType))

    def GetValue(self,
                 id: ImportIdentity,
                 amountTypeORwhereClause: Union[str, Callable[[IfrsVariable], bool]],
                 estimateType: Optional[str]='',
                 *,
                 economicBasis: Optional[str]='',
                 accidentYear: Optional[int]=0
                 ) -> float:
        if isinstance(amountTypeORwhereClause, str) or amountTypeORwhereClause is None:
            amountType = amountTypeORwhereClause
            return self.GetValue(
                id, lambda v: (v.AccidentYear == accidentYear and v.AmountType == amountType
                              and v.EstimateType == estimateType and v.EconomicBasis == economicBasis))
        else:
            whereClause = amountTypeORwhereClause
            vals = [v.Value for v in self.GetIfrsVariables(id.DataNode) if (v.AocType, v.Novelty) == id.AocStep and whereClause(v)]
            return vals[-1] if vals else 0    # Aggregate() returns last element

    #Novelty

    def GetNoveltiesForAocType(self, aocType: str, aocConfiguration: set[AocStep]) -> list[str]:
        return [aocStep.Novelty for aocStep in aocConfiguration if aocStep.AocType == aocType]

    def GetNovelties(self) -> list[str]:
        return list(self.NoveltyDimension.keys())

    def GetNovelties2(self, aocType: str) -> list[str]:
        return self.GetNoveltiesForAocType(aocType, set(self.AocConfigurationByAocStep.keys()))

    def GetNovelties3(self, aocType: str, inputSource: InputSource) -> list[str]:
        return self.GetNoveltiesForAocType(aocType, self.aocStepByInputSource[inputSource])

    #Accident years

    def GetAccidentYears(self, dataNode: str) -> Collection[int]:
        accidentYear = self.AccidentYearsByDataNode.get(dataNode, None)
        if accidentYear:
            return accidentYear
        else:
            return []

    # Parameters

    def GetNonPerformanceRiskRate(self, identity: ImportIdentity) -> float:

        period = PreviousPeriod if self.GetCreditDefaultRiskPeriod(identity) == PeriodType.BeginningOfPeriod else CurrentPeriod
        dataNodeData = self.DataNodeDataBySystemName.get(identity.DataNode, None)

        if not dataNodeData:
            raise DataNodeNotFound

        if not dataNodeData.Partner:
            raise PartnerNotFound

        # if Partner == Internal then return 0
        rating = self.PartnerRating.get(dataNodeData.Partner)
        if not rating:
            raise RatingNotFound

        rate = self.CreditDefaultRates.get(rating[period].CreditRiskRating, None)
        if not rate:
            raise CreditDefaultRateNotFound

        return rate[period].Values[0]

    def GetPremiumAllocationFactor(self, id_: ImportIdentity) -> float:
        singleDataNodeParameter = self.SingleDataNodeParametersByGoc.get(id_.DataNode)
        if singleDataNodeParameter:
            return singleDataNodeParameter[CurrentPeriod].PremiumAllocation
        else:
            return DefaultPremiumExperienceAdjustmentFactor

    # Data Node relationships

    def GetUnderlyingGic(self, id_: ImportIdentity) -> list[str]:
        interDataNodeParameters = self.InterDataNodeParametersByGoc.get(id_.DataNode)
        if not interDataNodeParameters:
            return []
        else:
            temp = [x.DataNode  if x.DataNode != id_.DataNode else x.LinkedDataNode for x in interDataNodeParameters[CurrentPeriod]]
            return [goc for goc in temp if not self.DataNodeDataBySystemName[goc].IsReinsurance]

    def GetReinsuranceCoverage(self, id_: ImportIdentity, gic: str) -> float:

        targetPeriod = CurrentPeriod if self.AocConfigurationByAocStep[AocStep(id_.AocType, id_.Novelty)].RcPeriod == PeriodType.EndOfPeriod else PreviousPeriod

        interDataNodeParameters = self.InterDataNodeParametersByGoc.get(id_.DataNode, None)

        if interDataNodeParameters:
            return next(x for x in interDataNodeParameters[targetPeriod] if  (x.DataNode == gic or x.LinkedDataNode == gic)).ReinsuranceCoverage
        else:
            raise ReinsuranceCoverage

    # Import Scope

    def IsPrimaryScope(self, dataNode: str) -> bool:
        return dataNode in self.DataNodesByImportScope[ImportScope.Primary]

    def IsSecondaryScope(self, dataNode: str) -> bool:
        return dataNode in self.DataNodesByImportScope[ImportScope.Secondary]

    # Other

    def GetNonAttributableAmountType(self) -> set[str]:
        return {AmountTypes.NE}

    def GetAttributableExpenseAndCommissionAmountType(self) -> list[str]:
        return [AmountTypes.ACA, AmountTypes.AEA] #U+ specific

    def GetInvestmentClaims(self) -> list[str]:
        result = []
        for x in self.database.Query(AmountType):
            if x.SystemName == AmountTypes.ICO or x.Parent == AmountTypes.ICO:
                result.append(x.SystemName)

        return result

    def GetPremiums(self) -> list[str]:
        result = []
        for x in self.database.Query(AmountType):
            if x.SystemName == AmountTypes.PR or x.Parent == AmountTypes.PR:
                result.append(x.SystemName)

        return result

    def GetClaims(self) -> list[str]:
        result = []
        for x in self.database.Query(AmountType):
            if x.Parent == AmountTypes.CL:
                result.append(x.SystemName)
        return result

