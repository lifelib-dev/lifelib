import dataclasses
import uuid

from .Database import IfrsDatabase
from .Validations import *
from .ImportScopeCalculation import *
from .ImportCalculationMethods import *


class ParsingStorage:

    # Hierarchy Cache

    ReportingNode: ReportingNode
    DataNodeDataBySystemName: dict[str, DataNodeData]

    # Dimensions

    EstimateType: dict[str, EstimateType] 
    AmountType: dict[str, AmountType]

    AocTypeMap: set[AocStep] 
    estimateTypes: set[str] 
    amountTypes: set[str]

    @cached_property
    def amountTypesByEstimateType(self) -> dict[str, set[str]]:
        return GetAmountTypesByEstimateType()

    @cached_property
    def TechnicalMarginEstimateTypes(self) -> set[str]:
        return GetTechnicalMarginEstimateType()

    DimensionsWithExternalId: dict[type, dict[str, str]]

    # Partitions

    TargetPartitionByReportingNode: PartitionByReportingNode 
    TargetPartitionByReportingNodeAndPeriod: PartitionByReportingNodeAndPeriod 

    # Constructor
    def __init__(self, args: ImportArgs, database: IfrsDatabase):
        self.args: ImportArgs = args
        self.database: IfrsDatabase = database

        ## Initialize
        # Partition Workspace and DataSource
        node_ = [p for p in self.database.Query(PartitionByReportingNode) if p.ReportingNode == self.args.ReportingNode]

        self.TargetPartitionByReportingNode = node_[0] if len(node_) else None

        if not self.TargetPartitionByReportingNode:
            raise ParsedPartitionNotFound

        self.database.Partition.Set(PartitionByReportingNode, self.TargetPartitionByReportingNode.Id)

        if self.args.Year != 0 and self.args.Month != 0:

            node_ = [p for p in self.database.Query(PartitionByReportingNodeAndPeriod)  # TODO: Original code queries workspace instead. Don't know why.
                     if p.ReportingNode == self.args.ReportingNode and
                     p.Year == self.args.Year and
                     p.Month == self.args.Month and
                     p.Scenario == self.args.Scenario]

            self.TargetPartitionByReportingNodeAndPeriod = node_[0] if len(node_) else None

            if self.TargetPartitionByReportingNodeAndPeriod is None:
                raise ParsedPartitionNotFound

            self.database.Partition.Set(PartitionByReportingNodeAndPeriod, self.TargetPartitionByReportingNodeAndPeriod.Id)

        reportingNodes = [x for x in self.database.Query(ReportingNode) if x.SystemName == self.args.ReportingNode]
        if not reportingNodes:
            raise ReportingNodeNotFound

        self.ReportingNode = reportingNodes[0]

        aocConfigurationByAocStep = self.database.LoadAocStepConfiguration(self.args.Year, self.args.Month)

        if self.args.ImportFormat == ImportFormats.Cashflow:

            self.AocTypeMap = set(AocStep(x.AocType, x.Novelty) for x in aocConfigurationByAocStep
                            if (InputSource.Cashflow in x.InputSource
                                and not x.DataType in (DataType.Calculated,
                                                       DataType.CalculatedTelescopic)))

        elif self.args.ImportFormat == ImportFormats.Actual:

            self.AocTypeMap = set(AocStep(x.AocType, x.Novelty) for x in aocConfigurationByAocStep
                               if (InputSource.Cashflow in x.InputSource
                                and not x.DataType in (DataType.Calculated,
                                                       DataType.CalculatedTelescopic)
                                   and (x.AocType, x.Novelty) != (AocTypes.BOP, Novelties.I)))

        elif self.args.ImportFormat == ImportFormats.Opening:

            self.AocTypeMap = set(AocStep(x.AocType, x.Novelty) for x in aocConfigurationByAocStep
                            if (InputSource.Opening in x.InputSource
                                and x.DataType in DataType.Optional))

        elif self.args.ImportFormat == ImportFormats.SimpleValue:

            self.AocTypeMap = (
                    set(AocStep(x.AocType, x.Novelty) for x in aocConfigurationByAocStep) |
                    set(AocStep(vt.SystemName, '') for vt in self.database.Query(PnlVariableType)))
        else:
            self.AocTypeMap = set()


        # DataNodes

        if self.args.ImportFormat == ImportFormats.Opening:
            self.DataNodeDataBySystemName = {k: v for k, v in self.database.LoadDataNodes(self.args).items() if v.Year == self.args.Year}
        else:
            self.DataNodeDataBySystemName = self.database.LoadDataNodes(self.args)

        # Dimensions

        self.EstimateType = {x.SystemName: x for x in self.database.Query(EstimateType)}
        self.AmountType = {x.SystemName: x for x in self.database.Query(AmountType) if not isinstance(x, DeferrableAmountType)}
        self.amountTypes = set(x.SystemName for x in self.database.Query(AmountType))

        if self.args.ImportFormat == ImportFormats.SimpleValue:
            self.estimateTypes = set(et.SystemName for et in self.database.Query(EstimateType))
        elif self.args.ImportFormat == ImportFormats.Opening:
            self.estimateTypes = set(et.SystemName for et in self.database.Query(EstimateType)
                                     if et.StructureType == StructureType.AoC and
                                     InputSource.Opening in et.InputSource)
        else:
            self.estimateTypes = set()

        # DimensionsWithExternalId

        self.DimensionsWithExternalId = {
            AmountType: self.GetDimensionWithExternalIdDictionary(AmountType),
            EstimateType: self.GetDimensionWithExternalIdDictionary(EstimateType)
        }

    def GetDimensionWithExternalIdDictionary(self, T: type) -> dict[str, str]: # T = KeyedOrderedDimension

        dict_ = {}
        items = self.database.Query(T)
        for item in items:
            if item.SystemName not in dict_:
                dict_[item.SystemName] = item.SystemName

            if issubclass(T, KeyedOrderedDimensionWithExternalId):
                externalIds = item.ExternalId
                if not externalIds:
                    continue
                    
                for extId in externalIds:
                    if not extId:
                        continue    # skip ''
                    if extId not in dict_:
                        dict_[extId] = item.SystemName

        return dict_

    # Getters

    def IsDataNodeReinsurance(self, goc: str) -> bool:
        return self.DataNodeDataBySystemName[goc].IsReinsurance

    def IsValidDataNode(self, goc: str) -> bool:
        return goc in self.DataNodeDataBySystemName

    # Validations

    def ValidateEstimateType(self, et: str, goc: str) -> str:

        allowedEstimateTypes = self.estimateTypes
        dataNodeData = self.DataNodeDataBySystemName.get(goc, None)

        if dataNodeData and dataNodeData.LiabilityType == LiabilityTypes.LIC:
            for elm in self.TechnicalMarginEstimateTypes:
                self.estimateTypes.remove(elm)

        if et not in allowedEstimateTypes:
            raise EstimateTypeNotFound

        return et

    def ValidateAmountType(self, at: str) -> str:
        if at and at not in self.amountTypes:
            raise AmountTypeNotFound

        return at

    def ValidateAocStep(self, aoc: AocStep) -> AocStep:
        if aoc not in self.AocTypeMap:
            raise AocTypeMapNotFound

        return aoc

    def ValidateDataNode(self, goc: str) -> str:
        if goc not in self.DataNodeDataBySystemName:
            raise InvalidDataNode
        return goc

    def ValidateEstimateTypeAndAmountType(self, estimateType: str, amountType: str):
        ats = self.amountTypesByEstimateType.get(estimateType, None)
        if ats and any(ats) and amountType not in ats:
            raise InvalidAmountTypeEstimateType


## Update the Database

# AocConfiguration

def _FormatAocConfiguration(target: IfrsDatabase, dataSet: IDataSet):

    s_to_i = {k: v for k, v in InputSource.__dict__.items() if k[0] != '_'}

    dataSet.Tables['AocConfiguration']['InputSource'] = dataSet.Tables['AocConfiguration']['InputSource'].apply(lambda x: [s_to_i[s.strip()] for s in x.split(',')])

    aocTypes = sorted(target.Query(AocType), key=lambda x: x.Order)
    aocTypesCompulsory = [v for k, v in AocTypes.__dict__.items() if k[0] != '_']

    if any(x not in [y.SystemName for y in aocTypes] for x in aocTypesCompulsory):
        raise AocTypeCompulsoryNotFound

    target.FromDataSet(dataSet, AocConfiguration)

    orderByName = {x.SystemName: x.Order for x in aocTypes}

    temp: dict[(AocTypes, Novelties), list[AocConfiguration]] = {}
    for x in target.Query(AocConfiguration):
        k = (x.AocType, x.Novelty)
        if k in temp:
            temp[k].append(x)
        else:
            temp[k] = [x]

    aocConfigs: dict[(AocTypes, Novelties), AocConfiguration] = {}
    for k, v in temp.items():
        aocConfigs[k] = max(v, key=lambda x: x.Year * 100 + x.Month)

    aocOrder: dict[(AocTypes, Novelties), int] = {k: v.Order for k, v in aocConfigs.items()}

    newAoCTypes: list[str] = [x for x in orderByName.keys() if (
        (x, Novelties.I) not in aocConfigs.keys()
        and (x, Novelties.N) not in aocConfigs.keys()
        and (x, Novelties.C) not in aocConfigs.keys()
        and not any(y.Parent == x for y in aocTypes)
        and not x in aocTypesCompulsory
    )]

    for newAocType in newAoCTypes:

        if orderByName[newAocType] < orderByName[AocTypes.RCU]:
            step = (AocTypes.MC, Novelties.I)

            temp2: AocConfiguration = dataclasses.replace(aocConfigs[step])
            temp2.AocType = newAocType
            temp2.DataType = DataType.Optional
            temp2.Order = aocOrder[step] + 1
            target.Update2(temp2)

        elif (orderByName[newAocType] > orderByName[AocTypes.RCU] and orderByName[newAocType] < orderByName[AocTypes.CF]):
            
            step = (AocTypes.RCU, Novelties.I)

            temp2: AocConfiguration = dataclasses.replace(aocConfigs[step])
            temp2.AocType = newAocType
            temp2.DataType = DataType.Optional
            temp2.Order = aocOrder[step] + 1
            target.Update2(temp2)

        elif (orderByName[newAocType] > orderByName[AocTypes.IA] and orderByName[newAocType] < orderByName[AocTypes.YCU]):
            
            for novelty in (Novelties.I, Novelties.N):
                step = (AocTypes.AU, novelty)
                order = aocOrder[(AocTypes.IA, novelty)] + 1 if orderByName[newAocType] < orderByName[AocTypes.AU] else aocOrder[(AocTypes.AU, novelty)] + 1
                
                temp2: AocConfiguration = dataclasses.replace(aocConfigs[step])
                temp2.AocType = newAocType
                temp2.DataType = DataType.Optional
                temp2.Order = order
                target.Update2(temp2)

        elif (orderByName[newAocType] > orderByName[AocTypes.CRU] and orderByName[newAocType] < orderByName[AocTypes.WO]):
            
            stepI = (AocTypes.EV, Novelties.I)
            orderI = aocOrder[(AocTypes.CRU, Novelties.I)] + 1 if orderByName[newAocType] < orderByName[AocTypes.EV] else aocOrder[(AocTypes.EV, Novelties.I)] + 1

            temp2: AocConfiguration = dataclasses.replace(aocConfigs[stepI])
            temp2.AocType = newAocType
            temp2.DataType = DataType.Optional
            temp2.Order = orderI
            target.Update2(temp2)

            stepN = (AocTypes.EV, Novelties.N)
            orderN = aocOrder[(AocTypes.AU, Novelties.N)] + 1 if orderByName[newAocType] < orderByName[AocTypes.EV] else aocOrder[(AocTypes.EV, Novelties.N)] + 1

            temp2: AocConfiguration = dataclasses.replace(aocConfigs[stepN])
            temp2.AocType = newAocType
            temp2.DataType = DataType.Optional
            temp2.Order = orderN
            target.Update2(temp2)

        elif (orderByName[newAocType] > orderByName[AocTypes.WO] and orderByName[newAocType] < orderByName[AocTypes.CL]):

            step = (AocTypes.WO, Novelties.C)

            temp2: AocConfiguration = dataclasses.replace(aocConfigs[step])
            temp2.AocType = newAocType
            temp2.DataType = DataType.Optional
            temp2.Order = aocOrder[step] + 1
            target.Update2(temp2)

        else:
            raise AocTypePositionNotSupported


IfrsDatabase.DefineFormat(ImportFormats.AocConfiguration, _FormatAocConfiguration)


# Data Nodes

def _FormatDataNode(target: IfrsDatabase, dataSet: IDataSet):

    # target.Initialize(DataSource, DisableInitialization=[RawVariable, IfrsVariable, DataNodeState, DataNodeParameter])

    # Activity.Start()
    args = target.GetArgsFromMain(PartitionByReportingNode, dataSet)

    storage = ParsingStorage(args, target)

    def _FromDataSetInsurancePortfolio(dataSet, datarow):
        return InsurancePortfolio(
            SystemName=datarow["SystemName"],
            DisplayName=datarow["DisplayName"],
            Partition=storage.TargetPartitionByReportingNode.Id,
            ContractualCurrency=datarow["ContractualCurrency"],
            FunctionalCurrency=storage.ReportingNode.Currency,
            LineOfBusiness=datarow["LineOfBusiness"],
            ValuationApproach=datarow["ValuationApproach"],
            OciType=datarow["OciType"]
        )
                                                                                    
    importLogPortfolios = target.FromDataSet(
        dataSet, 
        type_=InsurancePortfolio,
        body=_FromDataSetInsurancePortfolio)
    
    def _FromDataSetReinsurancePortfolio(dataSet, datarow):
        return ReinsurancePortfolio(
            SystemName=datarow["SystemName"],
            DisplayName=datarow["DisplayName"],
            Partition=storage.TargetPartitionByReportingNode.Id,
            ContractualCurrency=datarow["ContractualCurrency"],
            FunctionalCurrency=storage.ReportingNode.Currency,
            LineOfBusiness=datarow["LineOfBusiness"],
            ValuationApproach=datarow["ValuationApproach"],
            OciType=datarow["OciType"]
        )

    if ReinsurancePortfolio.__name__ in dataSet.Tables:

        target.FromDataSet(
            dataSet,
            type_=ReinsurancePortfolio,
            body=_FromDataSetReinsurancePortfolio)

    portfolios = {x.SystemName: x for x in target.Query(Portfolio)}
    
    def _FromDataSetGroupOfContracts(dataset, datarow):

        gicSystemName = datarow["SystemName"]
        pf = datarow["InsurancePortfolio"]

        portfolioData = portfolios.get(pf, None)

        if not portfolioData:
            raise PortfolioGicNotFound

        gic = GroupOfInsuranceContract(
            SystemName=gicSystemName,
            DisplayName=datarow["DisplayName"],
            Partition=storage.TargetPartitionByReportingNode.Id,
            ContractualCurrency=portfolioData.ContractualCurrency,
            FunctionalCurrency=portfolioData.FunctionalCurrency,
            LineOfBusiness=portfolioData.LineOfBusiness,
            ValuationApproach=portfolioData.ValuationApproach,
            OciType=portfolioData.OciType,
            AnnualCohort= int(datarow["AnnualCohort"]),
            LiabilityType=datarow["LiabilityType"],
            Profitability=datarow["Profitability"],
            Portfolio=pf,
            YieldCurveName=datarow["YieldCurveName"] if "YieldCurveName" in dataset.Tables["GroupOfInsuranceContract"].columns else '',
            Partner='',
            IsReinsurance=False
        )

        return ExtendGroupOfContract(gic, datarow)

    def _FromDataSetGroupOfReinsuranceContract(dataset, datarow):

        gricSystemName = datarow["SystemName"]
        pf = datarow["ReinsurancePortfolio"]
        
        portfolioData = portfolios.get(pf, None)
        if not portfolioData:
            raise PortfolioGicNotFound
        
        gric = GroupOfReinsuranceContract(
    
            SystemName=gricSystemName,
            DisplayName=datarow["DisplayName"],
            Partition=storage.TargetPartitionByReportingNode.Id,
            ContractualCurrency=portfolioData.ContractualCurrency,
            FunctionalCurrency=portfolioData.FunctionalCurrency,
            LineOfBusiness=portfolioData.LineOfBusiness,
            ValuationApproach=portfolioData.ValuationApproach,
            OciType=portfolioData.OciType,
            AnnualCohort=int(datarow["AnnualCohort"]),
            LiabilityType=datarow["LiabilityType"],
            Profitability=datarow["Profitability"],
            Portfolio=pf,
            Partner=datarow["Partner"],
            YieldCurveName=datarow["YieldCurveName"] if "YieldCurveName" in dataset.Tables["GroupOfInsuranceContract"].columns.values else '',
            IsReinsurance=True
        )
        return ExtendGroupOfContract(gric, datarow)
    
    importLogGroupOfContracts = target.FromDataSet(dataSet, GroupOfInsuranceContract, _FromDataSetGroupOfContracts)
    if "GroupOfReinsuranceContract" in dataSet.Tables:
        importLogGroupOfContracts = target.FromDataSet(dataSet, GroupOfReinsuranceContract, _FromDataSetGroupOfReinsuranceContract)


IfrsDatabase.DefineFormat(ImportFormats.DataNode, _FormatDataNode)

# Data Node State

def _FormatDataNodeState(target: IfrsDatabase, dataSet: IDataSet):

    args = target.GetArgsFromMain(PartitionByReportingNodeAndPeriod, dataSet)

    storage = ParsingStorage(args, target)
    importLog = target.FromDataSet(dataSet, DataNodeState,
                                   lambda dataset, datarow: DataNodeState(
            Id=uuid.uuid4(),
            DataNode=datarow["DataNode"],
            State=datarow["State"],
            Year=args.Year,
            Month=args.Month,
            Partition=storage.TargetPartitionByReportingNode.Id,
            Scenario=''
        )
    )


IfrsDatabase.DefineFormat(ImportFormats.DataNodeState, _FormatDataNodeState)


# Data Node Parameters

def _FormatDataNodeParameter(target: IfrsDatabase, dataSet: IDataSet):

    args = target.GetArgsFromMain(PartitionByReportingNodeAndPeriod, dataSet)
    args = dataclasses.replace(args, ImportFormat=ImportFormats.DataNodeParameter)

    storage = ParsingStorage(args, target)

    singleDataNode = []     #new List<string>()
    interDataNode = []      #new List<(string,string)>()

    def _FromDataSetSingleDataNodeParameter(dataset, datarow):
        
        # read and validate DataNodes
        dataNode = datarow["DataNode"]
        if not storage.IsValidDataNode(dataNode):
            raise InvalidDataNode
        
        # check for duplicates
        if dataNode in singleDataNode:
           raise DuplicateSingleDataNode

        singleDataNode.append(dataNode)

        # Instantiate SingleDataNodeParameter

        return SingleDataNodeParameter(
            Id=uuid.uuid4(),
            Year=args.Year,
            Month=args.Month,
            Partition=storage.TargetPartitionByReportingNode.Id,
            DataNode=dataNode,
            PremiumAllocation=datarow["PremiumAllocation"],
            Scenario=''
        )

    def _FromDataSetInterDataNodeParameter(dataset, datarow):

        # read and validate DataNodes

        dataNode = datarow["DataNode"]
        if not storage.IsValidDataNode(dataNode):
            raise InvalidDataNode

        linkedDataNode = datarow["LinkedDataNode"]
        if not storage.IsValidDataNode(linkedDataNode):
            raise InvalidDataNode

        dataNodes = sorted([dataNode, linkedDataNode])

        # validate ReinsuranceGross Link

        isDn1Reinsurance = storage.IsDataNodeReinsurance(dataNodes[0])
        isDn2Reinsurance = storage.IsDataNodeReinsurance(dataNodes[1])
        isGrossReinsuranceLink = (isDn1Reinsurance and not isDn2Reinsurance) != (not isDn1Reinsurance and isDn2Reinsurance)
        reinsCov = datarow["ReinsuranceCoverage"]

        if(not isGrossReinsuranceLink and abs(reinsCov) > Precision):
            raise ReinsuranceCoverageDataNode

        # check for duplicates
        if ((dataNodes[0], dataNodes[1]) in interDataNode or (dataNodes[1], dataNodes[0]) in interDataNode):
            raise DuplicateInterDataNode

        interDataNode.append((dataNodes[0], dataNodes[1]))

        # Instantiate InterDataNodeParameter
        return InterDataNodeParameter(
            Id=uuid.uuid4(),
            Year=args.Year,
            Month=args.Month,
            Partition=storage.TargetPartitionByReportingNode.Id,
            DataNode=dataNodes[0],
            LinkedDataNode=dataNodes[1],
            ReinsuranceCoverage=reinsCov,
            Scenario=''
        )

    importLog = target.FromDataSet(dataSet, SingleDataNodeParameter, _FromDataSetSingleDataNodeParameter)
    importLog = target.FromDataSet(dataSet, InterDataNodeParameter, _FromDataSetInterDataNodeParameter)

IfrsDatabase.DefineFormat(ImportFormats.DataNodeParameter, _FormatDataNodeParameter)

# Cashflows

def ParseCashflowsToWorkspace(dataSet: IDataSet, args: ImportArgs, target: IfrsDatabase):

    parsingStorage = ParsingStorage(args, target)

    def _FromDataSetCashflow(dataset, datarow):

            aocType = datarow["AocType"]
            novelty = datarow["Novelty"]
            dataNode = datarow["DataNode"]

            dataNodeData = parsingStorage.DataNodeDataBySystemName.get(dataNode, None)

            if not dataNodeData:
                raise InvalidDataNode

            # Error if AocType is not present in the mapping
            if AocStep(aocType, novelty) not in parsingStorage.AocTypeMap:
                raise AocTypeMapNotFound

            # Filter out cash flows for DataNode that were created in the past and are still active and come with AocType = BOPI

            if dataNodeData.Year < args.Year and aocType == AocTypes.BOP and novelty == Novelties.I:
                raise RuntimeError("ActiveDataNodeWithCashflowBOPI")

            amountTypeFromFile = datarow["AmountType"]
            isEstimateType = amountTypeFromFile in parsingStorage.EstimateType
            amountType = '' if isEstimateType else amountTypeFromFile
            estimateType =  amountTypeFromFile if isEstimateType else EstimateTypes.BE
            values = []
            for k, v in datarow.items():
                if k[:6] == "Values":
                    assert len(values) == int(k[6:])    # Check if Values are in ascending order.
                    values.append(float(v))

            # Filter out empty raw variables for AocType != CL#
            if len(values) == 0 and aocType != AocTypes.CL:
                return None  #TODO: extend this check for all mandatory step and not just for CL

            accyr = datarow['AccidentYear'] if 'AccidentYear' in dataset.Tables[ImportFormats.Cashflow].columns else 0

            item = RawVariable(
                Id=uuid.uuid4(),
                DataNode=dataNode,
                AocType=aocType,
                Novelty=novelty,
                AmountType=amountType,
                EstimateType=estimateType,
                AccidentYear=accyr,
                Partition=parsingStorage.TargetPartitionByReportingNodeAndPeriod.Id,
                Values=values
            )
            return item

    importLog = target.FromDataSet(dataSet, RawVariable, _FromDataSetCashflow, format_=ImportFormats.Cashflow)


def _FormatCashflow(target: IfrsDatabase, dataSet: IDataSet):

    # Replace nan to '' or 0
    if 'Scenario' in dataSet.Tables['Main'].columns:
        dataSet.Tables['Main']['Scenario'].fillna('', inplace=True)
    if 'AccidentYear' in dataSet.Tables['Cashflow'].columns:
        dataSet.Tables['Cashflow']['AccidentYear'].fillna(0, inplace=True)

    args = target.GetArgsFromMain(PartitionByReportingNodeAndPeriod, dataSet)
    args = dataclasses.replace(args, ImportFormat=ImportFormats.Cashflow)
    target.DataNodeFactory(dataSet, ImportFormats.Cashflow, args)

    ParseCashflowsToWorkspace(dataSet, args, target)
    # storage = ImportStorage(args, target)
    #
    # universe = IModel(storage)
    # identities = sorted([i for s in universe.GetScopes(GetIdentities, storage.DataNodesByImportScope[ImportScope.Primary]) for i in s.Identities])
    #
    # ivs = [x for s in universe.GetScopes(ComputeIfrsVarsCashflows, identities) for x in s.CalculatedIfrsVariables]
    #
    # target.Update(IfrsVariable, ivs)

    return args


IfrsDatabase.DefineFormat(ImportFormats.Cashflow, _FormatCashflow)


# Actuals

def ParseActualsToWorkspace(dataSet: IDataSet, args: ImportArgs, target: IfrsDatabase):

    parsingStorage = ParsingStorage(args, target)

    def _FromDataSetActuals(dataset, datarow):

        dataNode = datarow["DataNode"]

        dataNodeData = parsingStorage.DataNodeDataBySystemName.get(dataNode, None)

        if not dataNodeData:
            raise InvalidDataNode

        valueType = datarow["ValueType"]

        if not valueType:
            raise ValueTypeNotFound

        amountType = parsingStorage.DimensionsWithExternalId[AmountType].get(valueType, None)
        isStdActual = valueType in parsingStorage.AmountType
        estimateType = EstimateTypes.A if isStdActual else parsingStorage.DimensionsWithExternalId[EstimateType].get(valueType, '')

        if not estimateType or not amountType:
            raise ValueTypeNotValid

        aocType = datarow["AocType"]

        if((not isStdActual and aocType != AocTypes.CF and aocType != AocTypes.WO) or (isStdActual and aocType != AocTypes.CF)):
            raise AocTypeNotValid

        item = IfrsVariable(
            Id=uuid.uuid4(),
            DataNode=dataNode,
            AocType=aocType,
            Novelty=Novelties.C,
            AccidentYear=int(datarow['AccidentYear']) if datarow['AccidentYear'] else 0,
            EconomicBasis='',
            AmountType=amountType,
            EstimateType=estimateType,
            Partition=parsingStorage.TargetPartitionByReportingNodeAndPeriod.Id,
            Value=datarow["Value"]
        )
        return item

    target.FromDataSet(dataSet, IfrsVariable, _FromDataSetActuals, format_=ImportFormats.Actual)
    

def _FormatActual(target: IfrsDatabase, dataSet: IDataSet):

    if 'AccidentYear' in dataSet.Tables['Actual'].columns:
        dataSet.Tables['Actual']['AccidentYear'].fillna(0, inplace=True)

    args = target.GetArgsFromMain(PartitionByReportingNodeAndPeriod, dataSet)
    args = dataclasses.replace(args, ImportFormat=ImportFormats.Actual)
    target.DataNodeFactory(dataSet, ImportFormats.Actual, args)

    ParseActualsToWorkspace(dataSet, args, target)
    # storage = ImportStorage(args, target)
    #
    # universe = IModel(storage)
    # identities = sorted([i for s in universe.GetScopes(GetIdentities, storage.DataNodesByImportScope[ImportScope.Primary]) for i in s.Identities])
    #
    # ivs = [x for s in universe.GetScopes(ComputeIfrsVarsActuals, identities) for x in  s.CalculatedIfrsVariables]
    # target.Update(IfrsVariable, ivs)

    return args


IfrsDatabase.DefineFormat(ImportFormats.Actual, _FormatActual)

# Simple Value

def ParseSimpleValueToWorkspace(dataSet: IDataSet, args: ImportArgs, target: IfrsDatabase):

    importFormat = args.ImportFormat
    parsingStorage = ParsingStorage(args, target)

    def _FromDataSetSimpleValue(dataset, datarow):

            dataNode = parsingStorage.ValidateDataNode(datarow["DataNode"])
            amountType = parsingStorage.ValidateAmountType(datarow["AmountType"])
            estimateType = parsingStorage.ValidateEstimateType(datarow["EstimateType"], dataNode)    #TODO LIC/LRC dependence

            aocStep = parsingStorage.ValidateAocStep(AocStep(datarow["AocType"], datarow["Novelty"])) if importFormat == ImportFormats.SimpleValue else AocStep(AocTypes.BOP, Novelties.I)
            economicBasis = datarow["EconomicBasis"] if importFormat == ImportFormats.SimpleValue else ''
            parsingStorage.ValidateEstimateTypeAndAmountType(estimateType, amountType)

            iv = IfrsVariable(
                Id=uuid.uuid4(),
                DataNode=dataNode,
                AocType=aocStep.AocType,
                Novelty=aocStep.Novelty,
                AccidentYear=int(datarow["AccidentYear"]) if datarow["AccidentYear"] else 0,
                AmountType=amountType,
                EstimateType=estimateType,
                EconomicBasis=economicBasis,
                Partition=parsingStorage.TargetPartitionByReportingNodeAndPeriod.Id,
                Value=datarow["Value"]

            )
            return iv

    importLog = target.FromDataSet(dataSet, IfrsVariable, _FromDataSetSimpleValue, format_=importFormat)    # This should indicate the table name, not the input format

    # Checking if there are inconsistencies in the TechnicalMarginEstimateTypes --> double entries in the steps where we expect to have unique values

    temp = [iv for iv in target.Query(IfrsVariable) if iv.EstimateType in parsingStorage.TechnicalMarginEstimateTypes]
    temp = [iv for iv in temp if iv.AocType == AocTypes.BOP or iv.AocType == AocTypes.EOP or iv.AocType == AocTypes.AM or iv.AocType == AocTypes.EA]
    temp2 = {}

    for iv in temp:
        temp2.setdefault((iv.DataNode, iv.AocType, iv.Novelty), []).append(iv)


def _FormatSimpleValue(target: IfrsDatabase, dataSet: IDataSet):

    # Replace nan to '' or 0
    if 'Scenario' in dataSet.Tables['Main'].columns:
        dataSet.Tables['Main']['Scenario'].fillna('', inplace=True)
    for col, nul in [('AccidentYear', 0), ('AmountType', ''), ('EconomicBasis', '')]:
        dataSet.Tables['SimpleValue'][col].fillna(nul, inplace=True)

    args = target.GetArgsFromMain(PartitionByReportingNodeAndPeriod, dataSet)
    args = dataclasses.replace(args, ImportFormat=ImportFormats.SimpleValue)

    target.DataNodeFactory(dataSet, ImportFormats.SimpleValue, args)
    ParseSimpleValueToWorkspace(dataSet, args, target)

    return args


IfrsDatabase.DefineFormat(ImportFormats.SimpleValue, _FormatSimpleValue)

# Opening

def _FormatOpening(target: IfrsDatabase, dataSet: IDataSet):

    dataSet.Tables['Opening']['AccidentYear'].fillna(0, inplace=True)
    dataSet.Tables['Opening']['AmountType'].fillna('', inplace=True)

    args = target.GetArgsFromMain(PartitionByReportingNodeAndPeriod, dataSet)
    args = dataclasses.replace(args, ImportFormat=ImportFormats.Opening)
    target.DataNodeFactory(dataSet, ImportFormats.Opening, args)

    ParseSimpleValueToWorkspace(dataSet, args, target)
    # storage = ImportStorage(args, target)
    #
    # universe = IModel(storage)
    # identities = sorted([i for s in universe.GetScopes(GetIdentities, storage.DataNodesByImportScope[ImportScope.Primary]) for i in s.Identities])
    # ivs = [x for s in universe.GetScopes(ComputeIfrsVarsOpenings, identities) for x in s.CalculatedIfrsVariables]
    #
    # target.Update(IfrsVariable, ivs)

    return args


IfrsDatabase.DefineFormat(ImportFormats.Opening, _FormatOpening)

