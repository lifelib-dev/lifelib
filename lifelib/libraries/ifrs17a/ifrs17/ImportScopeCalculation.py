import math
import uuid
from collections import namedtuple as _namedtuple
from typing import TypeVar, Generic
from functools import cached_property
from typing import get_type_hints, Union, Collection, Callable
import numbers

import pandas as pd

from .ImportStorage import *
from .Extensions import *
from .ImportCalculationMethods import *
from .Database import *
from .Validations import *

DelegateKey = _namedtuple('DalegateKey', ['Identity', 'storage'])

ScopeType = TypeVar('ScopeType')
T = TypeVar('T')
U = TypeVar('U')


class IfrsWorkspace:

    compute_targets: dict[ImportFormats, type] = {}

    def __init__(self):
        self.database = IfrsDatabase()
        self.models: dict[ImportArgs, IModel] = {}
        self.storages: dict[ImportArgs, ImportStorage] = {}

    def import_with_type(self, path: str, type_: Union[type, list[type]]):
        self.database.ImportFile(path, type_=type_)

    def import_with_format(self, path: str, format_: ImportFormats):
        args = self.database.ImportFile(path, format_=format_)
        if format_ in (ImportFormats.Cashflow, ImportFormats.Actual, ImportFormats.Opening):
            assert args not in self.storages
            storage = self.storages[args] = ImportStorage(args, self.database)
            assert args not in self.models
            self.models[args] = IModel(storage)
            self.compute(args)

    def compute(self, args: ImportArgs):

        storage = self.storages[args]
        models = self.models[args]

        identities = sorted(
            [i for s in models.GetScopes(GetIdentities, storage.DataNodesByImportScope[ImportScope.Primary]) for i in
             s.Identities])

        target = self.compute_targets[args.ImportFormat]
        ivs = [x for s in models.GetScopes(target, identities) for x in s.CalculatedIfrsVariables]
        self.database.Update(IfrsVariable, ivs)

    def compute_all(self):  # Not Used
        for args in self.models:
            self.compute(args)


def idtuple_to_dict(idtuple):

    importid = idtuple.Id.to_dict()
    ex_importid =  {k: getattr(idtuple, k) for k in idtuple._fields if k != 'Id'}
    return {**importid, **ex_importid}


class IModel:

    def __init__(self, storage: ImportStorage):
        self.storage = storage
        self.scope_cache: dict[ScopeType, dict[str, dict[T, IScope]]] = {}

    def GetScopes(self, scope: type, arglist: Collection[Union[str, ImportIdentity]]):
        result = []
        for arg in arglist:
            result.append(self.GetScope(scope, arg, ''))

        return result

    def GetScope(self, scope: ScopeType, id_: T, context: str):

        assert context in scope.valid_contexts

        if scope.Applicability:
            key = DelegateKey(Identity=id_, storage=self.storage)
            for sub_t, cond in scope.Applicability.items():
                if cond(key):
                    return self._get_scope(sub_t, id_, context)

        return self._get_scope(scope, id_, context)    # Default

    def _get_scope(self, scope: ScopeType, id_: T, context: str):

        v = self.scope_cache.setdefault(scope, {})
        v = v.setdefault(context, {})

        if (s := v.get(id_, None)) is None:
            s = scope(id_, self, context)
            v[id_] = s
        else:
            return s

        return s

    def _get_cached_scope(self, scope: type, context: str, **kwargs):

        data = self.scope_cache[scope][context]

        def _importid_match(kwargs: dict, importid: ImportIdentity):
            for param, arg in kwargs.items():
                if hasattr(importid, param):
                    a = getattr(importid, param)
                    if arg != a:
                        return False

            return True

        def _namedtuple_match(kwargs: dict, identity: tuple):
            fields = identity._fields
            for param, arg in kwargs.items():
                if param in fields:
                    if getattr(identity, param) != arg:
                        return False
                elif hasattr(identity, 'Id') and hasattr(importid := getattr(identity, 'Id'), param):
                    if getattr(importid, param) != arg:
                        return False

            return True

        id_t = scope.identity_type
        result = {}
        if isinstance(id_t, str):   # DataNode
            key = kwargs[id_t]
            result[key] = data[key]

        elif issubclass(id_t, ImportIdentity):
            for key, val in data.items():
                if _importid_match(kwargs, key):
                    result[key] = val
            return result

        elif issubclass(id_t, tuple):
            for key, val in data.items():
                if _namedtuple_match(kwargs, key):
                    result[key] = val

        else:
            raise KeyError

        return result

    @staticmethod
    def cached_scope_to_df(scope: type, cached_scope):

        result = []
        for k, v in cached_scope.items():

            if isinstance(scope.identity_type, str):
                key = {scope.identity_type: k}
            elif issubclass(scope.identity_type, ImportIdentity):
                key = k.to_dict()
            elif issubclass(scope.identity_type, tuple):
                key = idtuple_to_dict(k)
            else:
                raise KeyError

            cp_types = v.cached_property_types()

            vals = {}
            for cp, t in cp_types.items():
                vals[cp] = getattr(v, cp)
                #
                # if not isinstance(v, type):
                #     vals[cp] = getattr(v, cp)
                # elif issubclass(t, (numbers.Number, str)):
                #     vals[cp] = getattr(v, cp)
                # else:
                #     vals[cp] = repr(getattr(v, cp))

            result.append({**key, **vals})

        return pd.DataFrame(result)

    def debug(self, scope_name: str, include_sub=True, **kwargs):

        context = kwargs.pop('context', None)

        if include_sub:
            result = {}
            for k, v in self.scope_cache.items():
                if scope_name in set(w.__name__ for w in k.mro()):
                    sscope = k.__name__
                    if (df := self._debug_single_scope(sscope, context, **kwargs)) is not None:
                        result[sscope] = df
                        result[sscope].insert(loc=0, column='Scope', value=sscope)

            return pd.concat(result.values(), ignore_index=True)

        else:
            result = self._debug_single_scope(scope_name, context, **kwargs)
            result.insert(loc=0, column='Scope', value=scope_name)
            return result

    def _debug_single_scope(self, scope_name: str, context: str, **kwargs):

        result = {}

        for k, v in self.scope_cache.items():
            if scope_name == k.__name__:
                for c, w in v.items():
                    if context is None or c == context:
                        result[c] = self.cached_scope_to_df(
                            k,
                            self._get_cached_scope(k, context=c, **kwargs))

        return pd.concat(result.values(), ignore_index=True) if result else None


class IScope(Generic[T, U]):

    Applicability: dict[ScopeType, Callable[[ScopeType], bool]] = {}
    Identity: T
    storage: U
    has_context: bool

    def __init__(self, id_, model: IModel, context: str=None):
        self.Identity = id_
        self.model = model
        self.storage = self.model.storage
        self.context = context

    def GetScope(self, scope: ScopeType, id_: T, context: str = ''):
        return self.model.GetScope(scope, id_, context)

    @classmethod
    def cached_property_types(cls):

        result = {}
        for o in cls.mro():
            for k, v in o.__dict__.items():
                if isinstance(v, cached_property):
                    if hasattr(hints := get_type_hints(v.func), 'return'):
                        result[k] = hints['return']
                    else:
                        result[k] = None

        return result


class AllCfIdentities(IScope): # string represents a DataNode

    identity_type = 'DataNode'
    valid_contexts = ('',)

    @cached_property
    def ids(self):
        return [ImportIdentity(AocType=aocStep.AocType,
                              Novelty=aocStep.Novelty,
                              DataNode=self.Identity
                              ) for aocStep in self.storage.GetAllAocSteps(InputSource.Cashflow)]


class GetIdentities(IScope):

    identity_type = 'DataNode'
    valid_contexts = ('',)

    @cached_property
    def computedIdentities(self) -> list[ImportIdentity]:
        return [ImportIdentity(AocType=aocType, Novelty=Novelties.C,  DataNode=self.Identity)
                for aocType in [AocTypes.EA, AocTypes.AM, AocTypes.EOP]]

    @cached_property
    def allIdentities(self) -> set[ImportIdentity]:
        return set(self.ParsedIdentities + self.computedIdentities + self.SpecialIdentities)

    @cached_property
    def ParsedIdentities(self):
        return []

    @cached_property
    def SpecialIdentities(self):
        return []

    #Set DataNode properties and ProjectionPeriod

    @cached_property
    def Identities(self) -> set[ImportIdentity]:
        result = set()

        for id_ in self.allIdentities:
            kwargs = id_.__dict__.copy()
            kwargs['IsReinsurance'] = self.storage.DataNodeDataBySystemName[id_.DataNode].IsReinsurance
            kwargs['ValuationApproach'] = self.storage.DataNodeDataBySystemName[id_.DataNode].ValuationApproach

            result.add(ImportIdentity(**kwargs))

        return result


class AllCashflowIdentities(GetIdentities):

    @cached_property
    def SpecialIdentities(self):
        return self.GetScope(AllCfIdentities, self.Identity).ids


class GetActualIdentities(GetIdentities):

    @cached_property
    def actualEstimateTypes(self) -> list[str]:
        return self.storage.EstimateTypesByImportFormat[ImportFormats.Actual]

    @cached_property
    def ParsedIdentities(self) -> list[ImportIdentity]:
        return [ImportIdentity.from_iv(iv) for iv in self.storage.GetIfrsVariables(self.Identity) if iv.EstimateType in self.actualEstimateTypes]

    @cached_property
    def SpecialIdentities(self) -> list[ImportIdentity]:
        temp = self.GetScope(AllCfIdentities, self.Identity).ids
        temp2 = [ImportIdentity(
            AocType=aocStep.AocType,
            Novelty=aocStep.Novelty,
            DataNode=self.Identity) for aocStep in self.storage.GetAllAocSteps(InputSource.Opening)]

        return temp + temp2


class GetCashflowIdentities(GetIdentities):

    @cached_property
    def isReinsurance(self) -> bool:
        return self.storage.DataNodeDataBySystemName[self.Identity].IsReinsurance #clean up in the next PR

    @cached_property
    def ParsedIdentities(self) -> list[ImportIdentity]:
        return [ImportIdentity.from_rv(v) for v in self.storage.GetRawVariables(self.Identity)]

    @cached_property
    def SpecialIdentities(self) -> list[ImportIdentity]:
        temp = {id_.Novelty for id_ in self.ParsedIdentities if id_.Novelty != Novelties.C}
        temp2 = []
        for n in temp:
            if n == Novelties.N:
                temp3 = [AocTypes.IA, AocTypes.CF] #Add IA, CF, for New Business
            elif self.isReinsurance:
                temp3 = [AocTypes.IA, AocTypes.CF, AocTypes.YCU, AocTypes.CRU, AocTypes.RCU]     #Add IA, CF, YCU, CRU, RCU for in force
            else:
                temp3 = [AocTypes.IA, AocTypes.CF, AocTypes.YCU]    #Add IA, CF, YCU

            temp3 = [ImportIdentity(
                AocType = aocType,
                Novelty = n,
                DataNode = self.Identity) for aocType in temp3]

            temp2.extend(temp3)

        temp2.append(ImportIdentity(
               AocType=AocTypes.CF,     #Add CF for Deferral
               Novelty=Novelties.C,
               DataNode=self.Identity))

        temp2.extend([ImportIdentity(
            AocType=aocStep.AocType,
            Novelty=aocStep.Novelty,
            DataNode=self.Identity
                      ) for aocStep in self.storage.GetAllAocSteps(InputSource.Opening)])

        return temp2


class GetAllIdentities(GetIdentities):

    @cached_property
    def SpecialIdentities(self) -> list[ImportIdentity]:
        temp = self.GetScope(AllCfIdentities, self.Identity).ids
        temp2 = [ImportIdentity(AocType=aocStep.AocType,
                                 Novelty=aocStep.Novelty,
                                 DataNode=self.Identity)
                 for aocStep in self.storage.GetAllAocSteps(InputSource.Actual)]

        return temp + temp2


GetIdentities.Applicability = {
    AllCashflowIdentities: lambda x: x.storage.IsSecondaryScope(x.Identity),
    GetActualIdentities: lambda x: x.storage.ImportFormat == ImportFormats.Actual,
    GetCashflowIdentities: lambda x: x.storage.ImportFormat == ImportFormats.Cashflow,
    GetAllIdentities: lambda x: x.storage.ImportFormat == ImportFormats.Opening}


## Getting Amount Types


class ValidAmountType(IScope):  # IScope<string, ImportStorage>

    identity_type = 'DataNode'
    valid_contexts = ('',)
    
    @cached_property
    def BeAmountTypes(self) -> set[str]:
        temp = {rv.AmountType for rv in self.storage.GetRawVariables(self.Identity) if rv.AmountType}
        if self.storage.DataNodeDataBySystemName[self.Identity].IsReinsurance:
            temp.add(AmountTypes.CDR)
        return temp

    @cached_property
    def ActualAmountTypes(self) -> set[str]:
        return {iv.AmountType for iv in self.storage.GetIfrsVariables(self.Identity)
                if iv.EstimateType in self.storage.EstimateTypesByImportFormat[ImportFormats.Actual]}


class BeAmountTypesFromIfrsVariables(ValidAmountType):

    @cached_property
    def BeAmountTypes(self) -> set[str]:
        return {iv.AmountType for iv in self.storage.GetIfrsVariables(self.Identity)
                if iv.EstimateType in self.storage.EstimateTypesByImportFormat[ImportFormats.Cashflow] and iv.AmountType != ''}


ValidAmountType.Applicability = {
    BeAmountTypesFromIfrsVariables: lambda x: x.storage.ImportFormat != ImportFormats.Cashflow or x.storage.IsSecondaryScope(x.Identity)
}

IdentityTuple2 = _namedtuple('IdentityTuple2', ['Id', 'AmountType'])


class ParentAocStep(IScope):     #: IScope<(ImportIdentity Id, string AmountType), ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def ParsedAocSteps(self) -> set[AocStep]:
        return {AocStep(id_.AocType, id_.Novelty) for id_ in self.GetScope(GetIdentities, self.Identity.Id.DataNode).ParsedIdentities}

    @cached_property
    def OrderedParsedAocSteps(self) -> list[AocStep]:
        temp = list(self.ParsedAocSteps | set(self.CalculatedTelescopicAocStep))
        return sorted(temp, key=lambda x: self.storage.AocConfigurationByAocStep[x].Order)

    @cached_property
    def ParentParsedIdentities(self) -> dict[AocStep, list[AocStep]]:
        return GetPreviousIdentities(self.OrderedParsedAocSteps)

    @cached_property
    def identityAocStep(self) -> AocStep:
        return AocStep(self.Identity.Id.AocType, self.Identity.Id.Novelty)

    @cached_property
    def CalculatedTelescopicAocStep(self) -> list[AocStep]:
        return self.storage.GetCalculatedTelescopicAocSteps()

    @cached_property
    def Values(self) -> list[AocStep]:

        key = self.Identity.Id.AocType

        if key == AocTypes.CRU:
            return [AocStep(AocTypes.YCU, Novelties.I)]
        elif key == AocTypes.YCU:
            return [GetReferenceAocStepForCalculated(self.OrderedParsedAocSteps, self.storage.AocConfigurationByAocStep, self.identityAocStep)]
        else:
            if parents := self.ParentParsedIdentities.get(self.identityAocStep, None):
                return parents
            else:
                return []


class ParentAocStepForCreditRisk(ParentAocStep):

    @cached_property
    def CalculatedTelescopicAocStep(self) -> list[AocStep]:
        return [aoc for aoc in self.storage.GetCalculatedTelescopicAocSteps() if aoc.AocType != AocTypes.CRU]


ParentAocStep.Applicability = {
    ParentAocStepForCreditRisk: lambda x: x.Identity.AmountType != AmountTypes.CDR
}


class ReferenceAocStep(IScope):  #IScope<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def OrderedParsedAocSteps(self) -> list[AocStep]:
        temp = {AocStep(id_.AocType, id_.Novelty) for id_ in self.GetScope(GetIdentities, self.Identity.DataNode).ParsedIdentities}
        return sorted(list(temp), key=lambda aocStep: self.storage.AocConfigurationByAocStep[aocStep].Order)

    @cached_property
    def identityAocStep(self) -> AocStep:
        return AocStep(self.Identity.AocType, self.Identity.Novelty)

    def GetReferenceAocStep(self, aocType:str) -> AocStep:

        if aocType in (AocTypes.RCU, AocTypes.CF, AocTypes.IA, AocTypes.YCU, AocTypes.CRU):
            return GetReferenceAocStepForCalculated(self.OrderedParsedAocSteps, self.storage.AocConfigurationByAocStep, self.identityAocStep)

        elif aocType == AocTypes.EA:
            return AocStep(AocTypes.CF, self.Identity.Novelty)

        elif aocType in (AocTypes.AM, AocTypes.EOP):
            return AocStep(AocTypes.CL, Novelties.C)

        elif aocType == AocTypes.BOP:
            return AocStep("", "")  #BOP, C has DataType == Calculated. See ReferenceAocStep condition.

        else:
            raise NotSupportedAocStepReference

    # The Reference AocStep from which get data (Nominal or PV) to compute

    @cached_property
    def Value(self) -> AocStep:
        if (self.storage.AocConfigurationByAocStep[self.identityAocStep].DataType == DataType.Calculated
                     or self.storage.AocConfigurationByAocStep[self.identityAocStep].DataType == DataType.CalculatedTelescopic):
            return self.GetReferenceAocStep(self.Identity.AocType)
        else:
            return self.identityAocStep


IdentityTuple3 = _namedtuple('IdentityTuple3', ['Id', 'ScopeInputSource'])


class PreviousAocSteps(IScope):     #<(ImportIdentity Id, InputSource ScopeInputSource), ImportStorage>

    identity_type = IdentityTuple3
    valid_contexts = ('',)

    @cached_property
    def identityAocStep(self) -> AocStep:
        return AocStep(self.Identity.Id.AocType, self.Identity.Id.Novelty)

    @cached_property
    def aocStepOrder(self) -> int:
        return self.storage.AocConfigurationByAocStep[self.identityAocStep].Order

    @cached_property
    def allAocSteps(self) -> {AocStep}:
        return self.storage.GetAllAocSteps(self.Identity.ScopeInputSource)

    @cached_property
    def Values(self) -> list[AocStep]:

        if self.identityAocStep in self.allAocSteps:

            ids = set()
            for id_ in self.GetScope(GetIdentities, self.Identity.Id.DataNode).Identities:
                aoc = AocStep(id_.AocType, id_.Novelty)
                if aoc in self.allAocSteps and self.storage.AocConfigurationByAocStep[aoc].Order < self.aocStepOrder and (
                        aoc.Novelty == self.Identity.Id.Novelty if self.Identity.Id.Novelty != Novelties.C else True):
                    ids.add(aoc)

            return sorted(list(ids), key=lambda aoc: self.storage.AocConfigurationByAocStep[aoc].Order)
        else:
            return []


class MonthlyRate(IScope):

    identity_type = ImportIdentity
    valid_contexts = (EconomicBases.C, EconomicBases.L)
    
    @cached_property
    def EconomicBasis(self) -> str:
        return self.context    

    @cached_property
    def YearlyYieldCurve(self) -> list[float]:
        return self.storage.GetYearlyYieldCurve(self.Identity, self.EconomicBasis)    

    @cached_property
    def Perturbation(self) -> float:
        return 0 #storage.GetYieldCurvePerturbation() => switch Args.Scenario { 10ptsU => 0.1, 10ptsD => -0.1, _ => default)

    @cached_property
    def Interest(self) -> list[float]:
        return [(1 + rate)**(1 / 12) + self.Perturbation for rate in self.YearlyYieldCurve]
                        
    @cached_property
    def Discount(self) -> list[float]:
        return [x ** (-1) for x in self.Interest]


IdentityTuple = _namedtuple('IdentityTuple', ['Id', 'AmountType', 'EstimateType', 'AccidentYear', 'Scale'], defaults=(1.0,))


class NominalCashflow(IScope):  # <(ImportIdentity Id, string AmountType, string EstimateType, int? AccidentYear), ImportStorage>

    identity_type = IdentityTuple
    valid_contexts = ('',)

    @cached_property
    def referenceAocStep(self) -> AocStep:
        return self.GetScope(ReferenceAocStep, self.Identity.Id).Value

    @cached_property
    def Values(self) -> list[float]:

        importid = self.Identity.Id.copy(AocType=self.referenceAocStep.AocType, Novelty=self.referenceAocStep.Novelty)
        return self.storage.GetValues2(importid, self.Identity.AmountType, self.Identity.EstimateType, self.Identity.AccidentYear)


class CreditDefaultRiskNominalCashflow(NominalCashflow):

    Applicability = None

    @cached_property
    def NominalClaimsCashflow(self) -> list[float]:

        claims = self.storage.GetClaims()
        temp = []
        for c in claims:
            importid = self.Identity.Id.copy(AocType=self.referenceAocStep.AocType, Novelty=self.referenceAocStep.Novelty)
            temp.append(self.storage.GetValues2(importid, c, self.Identity.EstimateType, self.Identity.AccidentYear))

        return AggregateDoubleArray(temp)
                            
    @cached_property
    def nonPerformanceRiskRate(self) -> float:
        return self.storage.GetNonPerformanceRiskRate(self.Identity.Id)

    @cached_property
    def PvCdrDecumulated(self) -> list[float]:
    
        ret = [0] * len(self.NominalClaimsCashflow)
        for i in range(len(self.NominalClaimsCashflow) - 1, -1, -1):
            ret[i] = math.exp(-self.nonPerformanceRiskRate) * (ret[i + 1] if i+1 < len(ret) else 0) + self.NominalClaimsCashflow[i] - (self.NominalClaimsCashflow[i + 1] if i+1 < len(self.NominalClaimsCashflow) else 0)
        return ret

    @cached_property
    def Values(self) -> list[float]:
        return [x - y for x, y in zip(self.PvCdrDecumulated, self.NominalClaimsCashflow)]


class AllClaimsCashflow(NominalCashflow):

    Applicability = None

    @cached_property
    def Values(self) -> list[float]:

        claims = self.storage.GetClaims()
        temp = []
        for c in claims:
            importid = self.Identity.Id.copy(AocType=self.referenceAocStep.AocType, Novelty=self.referenceAocStep.Novelty)
            temp.append(self.storage.GetValues2(importid, c, self.Identity.EstimateType, self.Identity.AccidentYear))

        return AggregateDoubleArray(temp)


NominalCashflow.Applicability = {
    CreditDefaultRiskNominalCashflow: lambda x: x.Identity.AmountType == AmountTypes.CDR and x.Identity.Id.AocType == AocTypes.CF,
    AllClaimsCashflow: lambda x: x.Identity.AmountType == AmountTypes.CDR
}

# Discount Cashflow


class DiscountedCashflow(IScope):   #<(ImportIdentity Id, string AmountType, string EstimateType, int? Accidentyear), ImportStorage>

    identity_type = IdentityTuple
    valid_contexts = (EconomicBases.C, EconomicBases.L)

    @cached_property
    def periodType(self) -> PeriodType:
        return self.storage.GetPeriodType(self.Identity.AmountType, self.Identity.EstimateType)

    @cached_property
    def EconomicBasis(self) -> str:
        return self.context

    @cached_property
    def MonthlyDiscounting(self) -> list[float]:
        return self.GetScope(MonthlyRate, self.Identity.Id, self.context).Discount

    @cached_property
    def NominalValues(self) -> list[float]:
        return self.GetScope(NominalCashflow, self.Identity).Values

    @cached_property
    def Values(self) -> list[float]:
        return [-1 * x for x in self.ComputeDiscountAndCumulate(self.NominalValues, self.MonthlyDiscounting, self.periodType)]   # we need to flip the sign to create a reserve view

    @staticmethod
    def ComputeDiscountAndCumulate(nominalValues: list[float], monthlyDiscounting: list[float], periodType: PeriodType) -> list[float]:

        if not nominalValues:
            return []

        ret = [0] * len(nominalValues)

        if periodType == PeriodType.BeginningOfPeriod:
            for i in range(len(nominalValues) - 1, -1, -1):
                    ret[i] = nominalValues[i] + GetElementOrDefault(ret, i+1) * GetElementOrDefault(monthlyDiscounting, int(i/12))

            return ret

        for i in range(len(nominalValues) - 1, -1, -1):
                    ret[i] = (nominalValues[i] + GetElementOrDefault(ret, i+1)) * GetElementOrDefault(monthlyDiscounting, int(i/12))

        return ret


class DiscountedCreditRiskCashflow(DiscountedCashflow):

    @cached_property
    def nonPerformanceRiskRate(self) -> float:
        return self.storage.GetNonPerformanceRiskRate(self.Identity.Id)

    @cached_property
    def Values(self) -> list[float]:
        return [-1 * x for x in self.ComputeDiscountAndCumulateWithCreditDefaultRisk(self.NominalValues, self.MonthlyDiscounting, self.nonPerformanceRiskRate)]     # we need to flip the sign to create a reserve view

    @staticmethod
    def ComputeDiscountAndCumulateWithCreditDefaultRisk(nominalValues: list[float], monthlyDiscounting: list[float], nonPerformanceRiskRate: float) -> list[float]:

        #Is it correct that NonPerformanceRiskRate is a double? Should it be an array that takes as input tau/t?

        ret = []
        for t in range(len(nominalValues)):
            temp = []
            for tau in range(t, len(nominalValues) - t):
               temp.append(nominalValues[tau] * math.pow(GetElementOrDefault(monthlyDiscounting, int(t/12)), tau-t+1) * (math.exp(-nonPerformanceRiskRate*(tau-t)) - 1))

            ret.append(sum(temp))

        return ret


DiscountedCashflow.Applicability = {
    DiscountedCreditRiskCashflow: lambda x: x.Identity.Id.IsReinsurance and x.Identity.AmountType == AmountTypes.CDR
}


class TelescopicDifference(IScope):      #<(ImportIdentity Id, string AmountType, string EstimateType, int? Accidentyear), ImportStorage>

    identity_type = IdentityTuple
    valid_contexts = (EconomicBases.C, EconomicBases.L)

    @cached_property
    def EconomicBasis(self) -> str:
        return self.context

    @cached_property
    def CurrentValues(self) -> list[float]:
        return self.GetScope(DiscountedCashflow, self.Identity, self.context).Values

    @cached_property
    def PreviousValues(self) -> list[float]:
        parents = self.GetScope(ParentAocStep, IdentityTuple2(self.Identity.Id, self.Identity.AmountType)).Values
        result = []
        for aoc in parents:
            id_ = self.Identity.Id.copy(AocType=aoc.AocType, Novelty=aoc.Novelty)
            result.append(self.GetScope(DiscountedCashflow,
                                       IdentityTuple(id_, self.Identity.AmountType, self.Identity.EstimateType, self.Identity.AccidentYear), self.context).Values)

        result = [cf for cf in result if len(cf) > 0]

        return AggregateDoubleArray(result)

    @cached_property
    def Values(self) -> list[float]:
        return [x - y for x, y in zip(self.CurrentValues, self.PreviousValues)]


class IWithInterestAccretion(IScope):

    @cached_property
    def parentDiscountedValues(self) -> list[float]:
        return [-1 * x for x in self.GetScope(DiscountedCashflow, self.Identity, self.context).Values]

    @cached_property
    def parentNominalValues(self) -> list[float]:
        return self.GetScope(NominalCashflow, self.Identity).Values

    @cached_property
    def monthlyInterestFactor(self) -> list[float]:
        return self.GetScope(MonthlyRate, self.Identity.Id, self.context).Interest

    def GetInterestAccretion(self) -> list[float]:

        periodType = self.storage.GetPeriodType(self.Identity.AmountType, self.Identity.EstimateType)
        ret = [0] * len(self.parentDiscountedValues)

        if periodType == PeriodType.BeginningOfPeriod:

            for i in range(len(self.parentDiscountedValues)):

                ret[i] = -1 * (self.parentDiscountedValues[i] - self.parentNominalValues[i]) * (
                            GetElementOrDefault(self.monthlyInterestFactor, int(i / 12)) - 1)
        else:
            for i in range(len(self.parentDiscountedValues)):
                ret[i] = -1 * self.parentDiscountedValues[i] * (GetElementOrDefault(self.monthlyInterestFactor, int(i / 12)) - 1)

        return ret


class IWithInterestAccretionForCreditRisk(IScope):

    @cached_property
    def nominalClaimsCashflow(self) -> list[float]:
        return self.GetScope(AllClaimsCashflow, self.Identity).Values

    @cached_property
    def nominalValuesCreditRisk(self) -> list[float]:
        importid = self.Identity.Id.copy(AocType=AocTypes.CF)
        kwargs = self.Identity._asdict()
        kwargs['Id'] = importid
        identity = IdentityTuple(**kwargs)

        return -1 * self.GetScope(CreditDefaultRiskNominalCashflow, identity).Values

    @cached_property
    def monthlyInterestFactor(self) -> list[float]:
        return self.GetScope(MonthlyRate, self.Identity.Id, self.context).Interest

    @cached_property
    def nonPerformanceRiskRate(self) -> float:
        return self.storage.GetNonPerformanceRiskRate(self.Identity.Id)

    def GetInterestAccretion(self) -> list[float]:

        interestOnClaimsCashflow =  [0] * len(self.nominalClaimsCashflow)
        interestOnClaimsCashflowCreditRisk = [0] * len(self.nominalClaimsCashflow)
        effectCreditRisk = [0] * len(self.nominalClaimsCashflow)

        for i in range(len(self.nominalClaimsCashflow) - 1, -1, -1):

            interestOnClaimsCashflow[i] = 1 / GetElementOrDefault(self.monthlyInterestFactor, int(i/12)) * (
                    (interestOnClaimsCashflow[i + 1] if i+1 < len(interestOnClaimsCashflow) else 0) + self.nominalClaimsCashflow[i] - (self.nominalClaimsCashflow[i + 1] if i+1 < len(self.nominalClaimsCashflow) else 0))
            interestOnClaimsCashflowCreditRisk[i] = 1 / GetElementOrDefault(self.monthlyInterestFactor, int(i/12)) * (
                    math.exp(-self.nonPerformanceRiskRate) * (interestOnClaimsCashflowCreditRisk[i + 1] if i+1 < len(interestOnClaimsCashflowCreditRisk) else 0) + self.nominalClaimsCashflow[i] - (self.nominalClaimsCashflow[i + 1] if i+1 < len(self.nominalClaimsCashflow) else 0))
            effectCreditRisk[i] = interestOnClaimsCashflow[i] - interestOnClaimsCashflowCreditRisk[i]

        return [x - y for x, y in zip(self.nominalValuesCreditRisk, effectCreditRisk)]


class IWithGetValueFromValues(IScope):      # IScope<(ImportIdentity Id, string AmountType, string EstimateType, int? AccidentYear), ImportStorage>{

    @cached_property
    def shift(self) -> int:
        return self.storage.GetShift(0)

    @cached_property
    def timeStep(self) -> int:
        return self.storage.GetTimeStep(0)

    def GetValueFromValues(self, Values: list[float]) -> float:

        key = self.storage.GetValuationPeriod(self.Identity.Id)

        if key == ValuationPeriod.BeginningOfPeriod:
            return Values[self.shift] if self.shift < len(Values) else 0.0

        elif key == ValuationPeriod.MidOfPeriod:
            idx = self.shift + round(self.timeStep / 2) - 1
            return Values[idx] if idx < len(Values) else 0.0

        elif key == ValuationPeriod.Delta:
            return sum(Values[self.shift:][:self.timeStep])

        elif key == ValuationPeriod.EndOfPeriod:
            return Values[self.shift + self.timeStep] if self.shift + self.timeStep < len(Values) else 0

        elif key == ValuationPeriod.NotApplicable:
            return 0

        else:
            raise RuntimeError('must not happen')


class PresentValue(IWithGetValueFromValues):

    identity_type = IdentityTuple
    valid_contexts = (EconomicBases.C, EconomicBases.L)

    @cached_property
    def EconomicBasis(self) -> str:
        return self.context

    @cached_property
    def Values(self) -> list[float]:
        return self.GetScope(TelescopicDifference, self.Identity, self.context).Values

    @cached_property
    def Value(self) -> float:
        return self.Identity.Scale * self.GetValueFromValues(self.Values)


class ComputePresentValueWithIfrsVariable(PresentValue):


    @cached_property
    def Value(self) -> list[float]:
        return self.Identity.Scale * self.storage.GetValue(
            self.Identity.Id, self.Identity.AmountType, self.Identity.EstimateType, economicBasis=self.EconomicBasis, accidentYear=self.Identity.AccidentYear)

    @cached_property
    def Values(self) -> list[float]:
        return []


class PresentValueFromDiscountedCashflow(PresentValue):

    @cached_property
    def Values(self) -> list[float]:
        return self.GetScope(DiscountedCashflow, self.Identity, self.context).Values


class CashflowAocStep(PresentValue):

    @cached_property
    def Values(self) -> list[float]:
        return self.GetScope(NominalCashflow, self.Identity).Values


class PresentValueWithInterestAccretion(PresentValue, IWithInterestAccretion):

    @cached_property
    def Values(self) -> list[float]:
        return self.GetInterestAccretion()


class PresentValueWithInterestAccretionForCreditRisk(PresentValue, IWithInterestAccretionForCreditRisk):

    @cached_property
    def Values(self) -> list[float]:
        return self.GetInterestAccretion()


class EmptyValuesAocStep(PresentValue):

    @cached_property
    def Values(self) -> list[float]:
        return []


PresentValue.Applicability = {
            ComputePresentValueWithIfrsVariable: lambda x: x.storage.ImportFormat != ImportFormats.Cashflow or x.storage.IsSecondaryScope(x.Identity.Id.DataNode),
            PresentValueFromDiscountedCashflow: lambda x: (x.Identity.Id.AocType == AocTypes.BOP and x.Identity.Id.Novelty != Novelties.C) or x.Identity.Id.AocType == AocTypes.EOP,
            CashflowAocStep: lambda x: x.Identity.Id.AocType == AocTypes.CF,
            PresentValueWithInterestAccretionForCreditRisk: lambda x: x.Identity.Id.IsReinsurance and x.Identity.AmountType == AmountTypes.CDR and x.Identity.Id.AocType == AocTypes.IA,
            PresentValueWithInterestAccretion: lambda x: x.Identity.Id.AocType == AocTypes.IA,
            EmptyValuesAocStep: lambda x: x.Identity.Id.AocType in [AocTypes.BOP, AocTypes.EA, AocTypes.AM, AocTypes.RCU]   #add here combination CRU for At !CDR?
}


class PvLocked(IScope):     #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EconomicBasis(self) -> str:
        return EconomicBases.L

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.BE

    @cached_property
    def accidentYears(self) -> list[int]:
        return self.storage.GetAccidentYears(self.Identity.DataNode)

    @cached_property
    def PresentValues(self) -> list[PresentValue]:
        temp = self.GetScope(ValidAmountType, self.Identity.DataNode).BeAmountTypes
        temp2 = []
        for at in temp:
            temp2 += [self.GetScope(PresentValue, IdentityTuple(self.Identity, at, self.EstimateType, ay), self.EconomicBasis) for ay in self.accidentYears]

        return temp2

    @cached_property
    def Value(self) -> float:
        return sum(self.PresentValues)


class PvCurrent(IScope):    #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EconomicBasis(self) -> str:
        return EconomicBases.C

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.BE

    @cached_property
    def accidentYears(self) -> list[int]:
        return list(self.storage.GetAccidentYears(self.Identity.DataNode))

    @cached_property
    def PresentValues(self) -> list[PresentValue]:
        temp = self.GetScope(ValidAmountType, self.Identity.DataNode).BeAmountTypes
        temp2 = []
        for at in temp:
            temp2 += [self.GetScope(PresentValue, IdentityTuple(self.Identity, at, self.EstimateType, ay), self.EconomicBasis) for ay in self.accidentYears]

        return temp2

    @cached_property
    def Value(self):
        return sum(self.PresentValues)


class RaLocked(IScope):

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EconomicBasis(self) -> str:
        return EconomicBases.L

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.RA

    @cached_property
    def accidentYears(self) -> [int]:
        return self.storage.GetAccidentYears(self.Identity.DataNode)

    @cached_property
    def PresentValues(self) -> [PresentValue]:
        return [self.GetScope(PresentValue, IdentityTuple(self.Identity, '', self.EstimateType, ay), self.EconomicBasis) for ay in self.accidentYears]

    @cached_property
    def Value(self) -> float:
        return sum([pv.Value for pv in self.PresentValues])


class RaCurrent(IScope):

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EconomicBasis(self) -> str:
        return EconomicBases.C

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.RA

    @cached_property
    def accidentYears(self) -> [int]:
        return self.storage.GetAccidentYears(self.Identity.DataNode)

    @cached_property
    def PresentValues(self) -> [PresentValue]:
        return [self.GetScope(PresentValue, IdentityTuple(self.Identity, '', self.EstimateType, ay), self.EconomicBasis) for ay in self.accidentYears]

    @cached_property
    def Value(self) -> float:
        return sum([pv.Value for pv in self.PresentValues])


class PvToIfrsVariable(IScope):

    valid_contexts = ('',)

    @cached_property
    def PvLocked(self) -> list[IfrsVariable]:

        result = []
        for x in [pvs for pvs in self.GetScope(PvLocked, self.Identity).PresentValues if abs(pvs.Value) >= Precision]:

            result.append(IfrsVariable(
                Id=uuid.uuid4(),
                EconomicBasis = x.EconomicBasis,
                EstimateType = x.Identity.EstimateType,
                DataNode = x.Identity.Id.DataNode,
                AocType = x.Identity.Id.AocType,
                Novelty = x.Identity.Id.Novelty,
                AccidentYear = x.Identity.AccidentYear,
                AmountType = x.Identity.AmountType,
                Value = x.Value,
                Partition = self.storage.TargetPartition))

        return result


    @cached_property
    def PvCurrent(self) -> list[IfrsVariable]:

        result = []
        for x in [x for x in self.GetScope(PvCurrent, self.Identity).PresentValues if abs(x.Value) >= Precision]:
            result.append(IfrsVariable(
                Id=uuid.uuid4(),
                EconomicBasis = x.EconomicBasis,
                EstimateType = x.Identity.EstimateType,
                DataNode = x.Identity.Id.DataNode,
                AocType = x.Identity.Id.AocType,
                Novelty = x.Identity.Id.Novelty,
                AccidentYear = x.Identity.AccidentYear,
                AmountType = x.Identity.AmountType,
                Value = x.Value,
                Partition = self.storage.TargetPartition))

        return result


class RaToIfrsVariable(IScope):     # <ImportIdentity, ImportStorage>

    valid_contexts = ('',)

    @cached_property
    def RaCurrent(self) -> [IfrsVariable]:

        result = []
        for x in [x for x in self.GetScope(RaCurrent, self.Identity).PresentValues if abs(x.Value) >= Precision]:

            result.append(IfrsVariable(
                Id=uuid.uuid4(),
                EconomicBasis = x.EconomicBasis,
                EstimateType = x.Identity.EstimateType,
                DataNode = x.Identity.Id.DataNode,
                AocType = x.Identity.Id.AocType,
                Novelty = x.Identity.Id.Novelty,
                AccidentYear = x.Identity.AccidentYear,
                AmountType = '',
                Value = x.Value,
                Partition = self.storage.TargetPartition
                ))
        return result

    @cached_property
    def RaLocked(self) -> [IfrsVariable]:

        result = []
        for x in [x for x in self.GetScope(RaLocked, self.Identity).PresentValues if abs(x.Value) >= Precision]:
            result.append(IfrsVariable(
                Id=uuid.uuid4(),
                EconomicBasis = x.EconomicBasis,
                EstimateType = x.Identity.EstimateType,
                DataNode = x.Identity.Id.DataNode,
                AocType = x.Identity.Id.AocType,
                Novelty = x.Identity.Id.Novelty,
                AccidentYear = x.Identity.AccidentYear,
                AmountType = '',
                Value = x.Value,
                Partition = self.storage.TargetPartition
            ))
        return result


class CoverageUnitCashflow(IScope):      #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = (EconomicBases.C, EconomicBases.L)

    @cached_property
    def EconomicBasis(self) -> str:
        return self.context

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.CU

    @cached_property
    def Values(self) -> [float]:
        return self.GetScope(DiscountedCashflow, IdentityTuple(self.Identity, '', self.EstimateType, 0), self.context).Values


class MonthlyAmortizationFactorCashflow(IScope):     #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = (EconomicBases.C, EconomicBases.L)

    @cached_property
    def NominalCuCashflow(self) -> [float]:

        id_ = self.Identity.copy(AocType=AocTypes.CL)
        return self.GetScope(NominalCashflow, IdentityTuple(id_, '', EstimateTypes.CU, 0)).Values

    @cached_property
    def DiscountedCuCashflow(self) -> [float]:

        id_ = self.Identity.copy(AocType=AocTypes.CL)
        return [-1 * x  for x in self.GetScope(CoverageUnitCashflow, id_, self.EconomicBasis).Values]

    @cached_property
    def EconomicBasis(self) -> str:
        return self.context
    
    @cached_property
    def MonthlyAmortizationFactors(self) -> [float]:

        if self.Identity.AocType == AocTypes.AM:

            result = []
            for nominal, discountedCumulated in zip(self.NominalCuCashflow, self.DiscountedCuCashflow):
                if abs(discountedCumulated) >= Precision:
                    result.append(1 - nominal / discountedCumulated)
                else:
                    result.append(0)

            return result
        else:
            return []


class CurrentPeriodAmortizationFactor(IScope):  #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = (EconomicBases.C, EconomicBases.L)

    @cached_property
    def shift(self) -> int:
        return self.storage.GetShift(0)

    @cached_property
    def timeStep(self) -> int:
        return self.storage.GetTimeStep(0)

    @cached_property
    def amortizedFactor(self) -> float:
        temp = self.GetScope(MonthlyAmortizationFactorCashflow, self.Identity, self.context).MonthlyAmortizationFactors
        return math.prod(temp[self.shift: self.shift + self.timeStep])

    @cached_property
    def EconomicBasis(self) -> str:
        return self.context

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.F

    @cached_property
    def Value(self) -> float:
        return 1 - self.amortizedFactor if abs(self.amortizedFactor - 1) > Precision else 1.0


class AmfFromIfrsVariable(CurrentPeriodAmortizationFactor):

    @cached_property
    def Value(self) -> float:
        return self.storage.GetValue(self.Identity, '', self.EstimateType, economicBasis=self.EconomicBasis, accidentYear=0)


CurrentPeriodAmortizationFactor.Applicability = {
    AmfFromIfrsVariable: lambda x: x.storage.ImportFormat != ImportFormats.Cashflow or x.storage.IsSecondaryScope(x.Identity.DataNode)
}


class ActualBase(IScope):    # <(ImportIdentity Id, string AmountType, string EstimateType, int? AccidentYear), ImportStorage>

    identity_type = IdentityTuple
    valid_contexts = ('',)

    @cached_property
    def Value(self) -> float:
        return self.Identity.Scale * self.storage.GetValue(
            self.Identity.Id, self.Identity.AmountType,
            estimateType=self.Identity.EstimateType,
            accidentYear=self.Identity.AccidentYear)


class EndOfPeriodActual(ActualBase):

    @cached_property
    def Value(self) -> float:

        result = []

        for aocStep in self.GetScope(PreviousAocSteps, IdentityTuple3(self.Identity.Id, InputSource.Actual)).Values:
            id_ = self.Identity.Id.copy(AocType=aocStep.AocType, Novelty=aocStep.Novelty)
            result.append(self.GetScope(ActualBase,
                                        IdentityTuple(id_, self.Identity.AmountType, self.Identity.EstimateType, self.Identity.AccidentYear)).Value)

        return self.Identity.Scale * sum(result)


class EmptyValuesActual(ActualBase):

    @cached_property
    def Value(self):
        return 0


ActualBase.Applicability = {
    EmptyValuesActual: lambda x: (x.storage.ImportFormat == ImportFormats.Actual
                                  and not x.storage.IsSecondaryScope(x.Identity.Id.DataNode)
                                  and x.Identity.Id.AocType == AocTypes.AM),
    EndOfPeriodActual: lambda x: (x.storage.ImportFormat != ImportFormats.Cashflow
                                  and not x.storage.IsSecondaryScope(x.Identity.Id.DataNode)
                                  and x.Identity.Id.AocType == AocTypes.EOP
                                  and x.Identity.EstimateType != EstimateTypes.A)
}


class Actual(IScope):     #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.A

    @cached_property
    def accidentYears(self) -> [int]:
        return self.storage.GetAccidentYears(self.Identity.DataNode)

    # [NotVisible]

    @cached_property
    def Actuals(self) -> [ActualBase]:
        result = []
        for at_ in self.GetScope(ValidAmountType, self.Identity.DataNode).ActualAmountTypes:
            result.extend(
                [self.GetScope(ActualBase, IdentityTuple(self.Identity, at_, self.EstimateType, ay)) for ay in self.accidentYears]
            )
        return result


class AdvanceActual(IScope):     #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.AA

    @cached_property
    def accidentYears(self) -> [int]:
        return self.storage.GetAccidentYears(self.Identity.DataNode)

    @cached_property
    def Actuals(self) -> [ActualBase]:
        result = []
        for at_ in self.GetScope(ValidAmountType, self.Identity.DataNode).ActualAmountTypes:
            result.extend(
                [self.GetScope(ActualBase, IdentityTuple(self.Identity, at_, self.EstimateType, ay)) for ay in self.accidentYears]
            )
        return result


class OverdueActual(IScope):    #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.OA


    @cached_property
    def accidentYears(self) -> [int]:
        return self.storage.GetAccidentYears(self.Identity.DataNode)


    @cached_property
    def Actuals(self) -> [ActualBase]:
        result = []
        for at_ in self.GetScope(ValidAmountType, self.Identity.DataNode).ActualAmountTypes:
            result.extend(
                [self.GetScope(ActualBase, IdentityTuple(self.Identity, at_, self.EstimateType, ay)) for ay in self.accidentYears]
            )
        return result


class DeferrableActual(IScope):     #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.DA
    
    @cached_property
    def EconomicBasis(self) -> str:
        return EconomicBases.L
        
    @cached_property
    def Value(self) -> float:
        return self.storage.GetValue(self.Identity, '', self.EstimateType)


class DeferrableActualForCurrentBasis(DeferrableActual):

    valid_contexts = ('',)

    @cached_property
    def EconomicBasis(self) -> str:
        return EconomicBases.C


class ReleaseDeferrable(DeferrableActual):

    @cached_property
    def Value(self) -> float:
        return sum([self.GetScope(ActualBase, IdentityTuple(self.Identity, at_, EstimateTypes.A, 0)).Value
                    for at_ in self.storage.GetAttributableExpenseAndCommissionAmountType()])


class AmortizationDeferrable(DeferrableActual):

    @cached_property
    def AmortizationFactor(self) -> float:
        return self.GetScope(CurrentPeriodAmortizationFactor, self.Identity, self.EconomicBasis).Value

    @cached_property
    def AggregatedDeferrable(self) -> float:

        result = []
        for aocStep in self.GetScope(PreviousAocSteps, IdentityTuple3(self.Identity, InputSource.Actual)).Values:
            id_ = self.Identity.copy(AocType=aocStep.AocType, Novelty=aocStep.Novelty)
            result.append(self.GetScope(DeferrableActual, id_).Value)

        return sum(result)

    @cached_property
    def Value(self) -> float:
        return -1 * self.AggregatedDeferrable * self.AmortizationFactor


class EndOfPeriodDeferrable(DeferrableActual):

    @cached_property
    def Value(self) -> float:

        result = []
        for aocStep in self.GetScope(PreviousAocSteps, IdentityTuple3(self.Identity, InputSource.Actual)).Values:
            id_ = self.Identity.copy(AocType=aocStep.AocType, Novelty=aocStep.Novelty)
            result.append(self.GetScope(DeferrableActual, id_).Value)

        return sum(result)


DeferrableActual.Applicability = {
    DeferrableActualForCurrentBasis: lambda x: x.Identity.ValuationApproach == ValuationApproaches.VFA,
    ReleaseDeferrable: lambda x: x.Identity.AocType == AocTypes.CF,
    AmortizationDeferrable: lambda x: x.Identity.AocType == AocTypes.AM,
    EndOfPeriodDeferrable: lambda x: x.Identity.AocType == AocTypes.EOP
}


class BeExperienceAdjustmentForPremium(IScope):     # <ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.BEPA

    @cached_property
    def EconomicBasis(self) -> str:
        return EconomicBases.L

    @cached_property
    def ByAmountType(self) -> [PresentValue]:
        mlt = self.storage.GetPremiumAllocationFactor(self.Identity)
        result = []
        for pr in self.storage.GetPremiums():
            pv = self.GetScope(PresentValue,
                               IdentityTuple(self.Identity, pr, EstimateTypes.BE, 0, mlt),
                               self.EconomicBasis)
            result.append(pv)

        return result


class DefaultValueBeExperienceAdjustmentForPremium(BeExperienceAdjustmentForPremium):

    @cached_property
    def ByAmountType(self) -> [PresentValue]:
        return []


BeExperienceAdjustmentForPremium.Applicability = {
    DefaultValueBeExperienceAdjustmentForPremium: lambda x: x.Identity.AocType != AocTypes.CF
}


class ActualExperienceAdjustmentOnPremium(IScope):   #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def ByAmountTypeAndEstimateType(self) -> [ActualBase]:
        temp = self.storage.GetPremiums()
        mlt = self.storage.GetPremiumAllocationFactor(self.Identity)
        result = []
        for pr in temp:
            pv = self.GetScope(ActualBase, IdentityTuple(self.Identity, pr, EstimateTypes.A, 0, mlt), context='')
            result.append(pv)
        return result


class DefaultValueActualExperienceAdjustmentOnPremium(ActualExperienceAdjustmentOnPremium):

    @cached_property
    def ByAmountTypeAndEstimateType(self) -> [ActualBase]:
        return []


ActualExperienceAdjustmentOnPremium.Applicability = {
    DefaultValueActualExperienceAdjustmentOnPremium: lambda x: x.Identity.AocType != AocTypes.CF
}


class TechnicalMargin(IScope):  #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EconomicBasis(self) -> str:
        return EconomicBases.L
    
    @cached_property
    def Value(self) -> float:

        x = self.GetScope(ValidAmountType, self.Identity.DataNode).BeAmountTypes
        y = self.storage.GetNonAttributableAmountType()
        z = x - y

        temp1 = sum([self.GetScope(PresentValue, IdentityTuple(self.Identity, at_, EstimateTypes.BE, 0), self.EconomicBasis).Value for at_ in z])
        temp2 = self.GetScope(RaLocked, self.Identity).Value
        return temp1 + temp2

    @cached_property
    def AggregatedValue(self) -> float:
        
        result = []
        for aoc in self.GetScope(PreviousAocSteps, IdentityTuple3(self.Identity, InputSource.Cashflow)).Values:
            id_ = self.Identity.copy(AocType=aoc.AocType, Novelty=aoc.Novelty)
            result.append(self.GetScope(TechnicalMargin, id_).Value)
        
        return sum(result)


class TechnicalMarginForCurrentBasis(TechnicalMargin): 

    valid_contexts = ('',)

    @cached_property
    def EconomicBasis(self):
        return EconomicBases.C


class TechnicalMarginForBOP(TechnicalMargin): 

    @cached_property
    def ValueCsm(self) -> float:
        return self.storage.GetValue(self.Identity, '', estimateType=EstimateTypes.C)
    
    @cached_property
    def ValueLc(self) -> float:
        return self.storage.GetValue(self.Identity, '', estimateType=EstimateTypes.L)
    
    @cached_property
    def ValueLr(self) -> float:
        return self.storage.GetValue(self.Identity, '', estimateType=EstimateTypes.LR)
    
    @cached_property
    def Value(self) -> float:
        return -1 * self.ValueCsm + self.ValueLc + self.ValueLr


class TechnicalMarginDefaultValue(TechnicalMargin): 

    @cached_property
    def Value(self) -> float:
        return 0


class TechnicalMarginForIA(TechnicalMargin):

    @cached_property
    def timeStep(self) -> int:
        return self.storage.GetTimeStep(0)

    @cached_property
    def shift(self) -> int:
        return self.storage.GetShift(0)

    @cached_property
    def monthlyInterestFactor(self) -> [float]:
        return self.GetScope(MonthlyRate, self.Identity, self.EconomicBasis).Interest
    
    @cached_property
    def interestAccretionFactor(self) -> float:
        result = []
        for i in range(self.shift, self.timeStep):
            result.append(GetElementOrDefault(self.monthlyInterestFactor, int(i/12)))

        return math.prod(result) - 1

    @cached_property
    def Value(self) -> float:
        return self.AggregatedValue * self.interestAccretionFactor


class TechnicalMarginForEA(TechnicalMargin):

    @cached_property
    def referenceAocType(self) -> str:
        return self.GetScope(ReferenceAocStep, self.Identity).Value.AocType
    
    @cached_property
    def premiums(self) -> float:

        # Estimate
        result = []
        for n in self.storage.GetNovelties3(self.referenceAocType, InputSource.Cashflow):
            id_ = self.Identity.copy(AocType=self.referenceAocType, Novelty=n)
            result.append(sum([sc.Value for sc in self.GetScope(BeExperienceAdjustmentForPremium, id_).ByAmountType]))

        # Actual
        id_ = self.Identity.copy(AocType=self.referenceAocType, Novelty=Novelties.C)
        result.append(-1 * sum([sc.Value for sc in self.GetScope(ActualExperienceAdjustmentOnPremium, id_).ByAmountTypeAndEstimateType]))

        return sum(result)

    @cached_property
    def attributableExpenseAndCommissions(self) -> float:

        result = []
        for d in self.storage.GetAttributableExpenseAndCommissionAmountType():
            temp = self.storage.GetNovelties3(self.referenceAocType, InputSource.Cashflow)
            result_inner = []
            # Estimate
            for n in temp:
                id_ = self.Identity.copy(AocType=self.referenceAocType, Novelty=n)
                result_inner.append(self.GetScope(PresentValue, IdentityTuple(id_, d, EstimateTypes.BE, 0), self.EconomicBasis).Value)
            # Actual
            id_ = self.Identity.copy(AocType=self.referenceAocType, Novelty=Novelties.C)
            result_inner.append(-1 * self.GetScope(ActualBase, IdentityTuple(id_, d, EstimateTypes.A, 0)).Value)
            result.append(sum(result_inner))

        return sum(result)


    @cached_property
    def investmentClaims(self) -> float:

        result = []
        for ic in self.storage.GetInvestmentClaims():
            # Estimate
            result_inner = []
            for n in self.storage.GetNovelties3(self.referenceAocType, InputSource.Cashflow):
                id_ = self.Identity.copy(AocType=self.referenceAocType, Novelty=n)
                result_inner.append(self.GetScope(PresentValue, IdentityTuple(id_, ic, EstimateTypes.BE, 0), self.EconomicBasis).Value)
            # Actual
            id_ = self.Identity.copy(AocType=self.referenceAocType, Novelty=Novelties.C)
            result_inner.append(-1 * self.GetScope(ActualBase, IdentityTuple(id_, ic, EstimateTypes.A, 0)).Value)
            result.append(sum(result_inner))

        return sum(result)

    @cached_property
    def Value(self) -> float:
        return self.premiums + self.attributableExpenseAndCommissions + self.investmentClaims


class TechnicalMarginForAM(TechnicalMargin):

    @cached_property
    def Value(self) -> float:
        return -1 * self.AggregatedValue * self.GetScope(CurrentPeriodAmortizationFactor, self.Identity, self.EconomicBasis).Value


TechnicalMargin.Applicability = {
    TechnicalMarginForCurrentBasis: lambda x: x.Identity.ValuationApproach == ValuationApproaches.VFA,
    TechnicalMarginForBOP: lambda x: x.Identity.AocType == AocTypes.BOP and x.Identity.Novelty == Novelties.I,
    TechnicalMarginDefaultValue: lambda x: x.Identity.AocType == AocTypes.CF,
    TechnicalMarginForIA: lambda x: x.Identity.AocType == AocTypes.IA and x.Identity.Novelty == Novelties.I,
    TechnicalMarginForEA: lambda x: x.Identity.AocType == AocTypes.EA and not x.Identity.IsReinsurance,
    TechnicalMarginForAM: lambda x: x.Identity.AocType == AocTypes.AM
    }


TechnicalMarginForEA.Applicability = {
    TechnicalMarginDefaultValue: lambda x: x.Identity.IsReinsurance
}


class AllocateTechnicalMargin(IScope):  #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = (EstimateTypes.L, EstimateTypes.C, EstimateTypes.LR)
    
    @cached_property
    def AggregatedTechnicalMargin(self) -> float:
        return self.GetScope(TechnicalMargin, self.Identity).AggregatedValue

    @cached_property
    def TechnicalMargin(self) -> float:
        return self.GetScope(TechnicalMargin, self.Identity).Value
    
    @cached_property
    def ComputedEstimateType(self) -> str:
        return self.ComputeEstimateType(self.GetScope(TechnicalMargin, self.Identity).AggregatedValue + self.TechnicalMargin)

    @cached_property
    def HasSwitch(self) -> bool:
        return self.ComputedEstimateType != self.ComputeEstimateType(self.GetScope(TechnicalMargin, self.Identity).AggregatedValue)

    # Allocate
    @cached_property
    def EstimateType(self) -> str:
        return self.context
    
    @cached_property
    def Value(self) -> float:

        if self.HasSwitch and self.EstimateType == self.ComputedEstimateType:
            return self.TechnicalMargin + self.AggregatedTechnicalMargin

        elif self.HasSwitch and not self.EstimateType == self.ComputedEstimateType:
            return -1 * self.AggregatedTechnicalMargin

        elif not self.HasSwitch and self.EstimateType == self.ComputedEstimateType:
            return self.TechnicalMargin

        else:
            return 0

    def ComputeEstimateType(self, aggregatedTechnicalMargin: float) -> str:
        return EstimateTypes.L if aggregatedTechnicalMargin > Precision else EstimateTypes.C


class ComputeAllocateTechnicalMarginWithIfrsVariable(AllocateTechnicalMargin):

    @cached_property
    def TechnicalMargin(self) -> float:
        return self.ComputeTechnicalMarginFromIfrsVariables(self.Identity)

    @cached_property
    def AggregatedTechnicalMargin(self) -> float:
        result = []
        for aoc in self.GetScope(PreviousAocSteps, (self.Identity, InputSource.Cashflow)).Values:
            id_ = self.Identity.copy(AocType=aoc.AocType, Novelty=aoc.Novelty)
            result.append(self.ComputeTechnicalMarginFromIfrsVariables(id_))

        return sum(result)

    def ComputeTechnicalMarginFromIfrsVariables(self, id_: ImportIdentity):

        return (self.storage.GetValue(self.Identity, '', EstimateTypes.LR) +
                 self.storage.GetValue(self.Identity, '', EstimateTypes.L) -
               self.storage.GetValue(self.Identity, '', EstimateTypes.C))


class AllocateTechnicalMarginForReinsurance(AllocateTechnicalMargin):


   # TODO add Reinsurance Coverage Update (RCU, Novelty=I) AocStep

    @cached_property
    def underlyingGic(self) -> [list]:
        return self.storage.GetUnderlyingGic(self.Identity)
   
    @cached_property
    def weightedUnderlyingTM(self) -> float:

        result = []
        for gic in self.underlyingGic:
            id_ = self.Identity.copy(DataNode=gic, IsReinsurance=False)
            result.append(self.storage.GetReinsuranceCoverage(self.Identity, gic) * self.GetScope(AllocateTechnicalMargin, id_, self.context).TechnicalMargin)

        return sum(result)
                                                                      
    @cached_property
    def weightedUnderlyingAggregatedTM(self) -> float:
        result = []
        for gic in self.underlyingGic:
            id_ = self.Identity.copy(DataNode=gic, IsReinsurance=False)
            # The original code refers to AllocateTechnicalMargin.AggregatedTechnicalMargin, which contains balancingValue. Don't know why.
            result.append(self.storage.GetReinsuranceCoverage(self.Identity, gic) * self.GetScope(TechnicalMargin, id_).AggregatedValue)

        return sum(result)

    def ComputeReinsuranceEstimateType(self, aggregatedFcf: float) -> str:
        return EstimateTypes.LR if aggregatedFcf > Precision else EstimateTypes.C
    
    @cached_property
    def ComputedEstimateType(self) -> str:
        return self.ComputeReinsuranceEstimateType(self.weightedUnderlyingAggregatedTM + self.weightedUnderlyingTM)

    @cached_property
    def HasSwitch(self) -> bool:
        return self.ComputedEstimateType != self.ComputeReinsuranceEstimateType(self.weightedUnderlyingAggregatedTM)


class AllocateTechnicalMarginForReinsuranceCL(AllocateTechnicalMargin):

    # In common1

    @cached_property
    def underlyingGic(self) -> list[str]:
        return self.storage.GetUnderlyingGic(self.Identity)
   
    @cached_property
    def weightedUnderlyingTM(self) -> float:
        result = []
        for gic in self.underlyingGic:
            id_ = self.Identity.copy(DataNode=gic, IsReinsurance=False)
            result.append(self.storage.GetReinsuranceCoverage(self.Identity, gic) * self.GetScope(AllocateTechnicalMargin, id_, self.context).TechnicalMargin)

        return sum(result)
                                                                      
    @cached_property
    def weightedUnderlyingAggregatedTM(self) -> float:
        result = []
        for gic in self.underlyingGic:
            id_ = self.Identity.copy(DataNode=gic, IsReinsurance=False)
            # The original code refers to AllocateTechnicalMargin.AggregatedTechnicalMargin, which contains balancingValue. Don't know why.
            result.append(self.storage.GetReinsuranceCoverage(self.Identity, gic) * self.GetScope(TechnicalMargin, id_).AggregatedValue)

        return sum(result)

    def ComputeReinsuranceEstimateType(self, aggregatedFcf: float) -> str:
        return EstimateTypes.LR if aggregatedFcf > Precision else EstimateTypes.C
    
    @cached_property
    def ComputedEstimateType(self) -> str:
        return self.ComputeReinsuranceEstimateType(self.weightedUnderlyingAggregatedTM + self.weightedUnderlyingTM)

     # In common2

    @cached_property
    def balancingValue(self) -> float:

        result = {}
        for x in self.GetScope(PreviousAocSteps, IdentityTuple3(self.Identity, InputSource.Cashflow)).Values:
            result.setdefault(x.Novelty, []).append(x)

        temp = [g[-1] for g in result.values()]
        result = []
        for aoc in temp:
            id_ = self.Identity.copy(AocType=aoc.AocType, Novelty=aoc.Novelty)
            result.append(
                (self.GetScope(AllocateTechnicalMargin, id_, self.context).TechnicalMargin
                    + self.GetScope(AllocateTechnicalMargin, id_, self.context).AggregatedTechnicalMargin) if (
                        self.GetScope(AllocateTechnicalMargin, id_, self.context).ComputedEstimateType != self.ComputedEstimateType) else 0
            )

        return sum(result)
                                                   
    @cached_property
    def HasSwitch(self) -> bool:
        return abs(self.balancingValue) > Precision

    @cached_property
    def AggregatedTechnicalMargin(self) -> float:
        return self.balancingValue


class AllocateTechnicalMarginForCl(AllocateTechnicalMargin):

    @cached_property
    def balancingValue(self) -> float:

        result = {}
        for x in self.GetScope(PreviousAocSteps, IdentityTuple3(self.Identity, InputSource.Cashflow)).Values:
            result.setdefault(x.Novelty, []).append(x)

        temp = [g[-1] for g in result.values()]
        result = []
        for aoc in temp:
            id_ = self.Identity.copy(AocType=aoc.AocType, Novelty=aoc.Novelty)
            result.append(
                (self.GetScope(AllocateTechnicalMargin, id_, self.context).TechnicalMargin
                    + self.GetScope(AllocateTechnicalMargin, id_, self.context).AggregatedTechnicalMargin) if (
                        self.GetScope(AllocateTechnicalMargin, id_, self.context).ComputedEstimateType != self.ComputedEstimateType) else 0
            )
        return sum(result)

    @cached_property
    def HasSwitch(self) -> bool:
        return abs(self.balancingValue) > Precision
    
    @cached_property
    def AggregatedTechnicalMargin(self) -> float:
        return self.balancingValue


class AllocateTechnicalMarginForBop(AllocateTechnicalMargin):

    @cached_property
    def HasSwitch(self) -> bool:
        return False


class AllocateTechnicalMarginForEop(AllocateTechnicalMargin):

    @cached_property
    def Value(self) -> float:
        result = []
        for aoc in self.GetScope(PreviousAocSteps, IdentityTuple3(self.Identity, InputSource.Cashflow)).Values:
            id_ = self.Identity.copy(AocType=aoc.AocType, Novelty=aoc.Novelty)
            result.append(self.GetScope(AllocateTechnicalMargin, id_, self.context).Value)

        return sum(result)

    @cached_property
    def ComputedEstimateType(self) -> str:
        return self.ComputeEstimateType(self.AggregatedTechnicalMargin)

# x.Identity.AocType != AocTypes.EOP is added to AllocateTechnicalMarginForReinsurance
# to use AllocateTechnicalMarginForEop for reinsurance & EOP
AllocateTechnicalMargin.Applicability = {
    AllocateTechnicalMarginForReinsuranceCL: lambda x: x.Identity.IsReinsurance and x.Identity.AocType == AocTypes.CL,
    AllocateTechnicalMarginForReinsurance: lambda x: x.Identity.IsReinsurance and x.Identity.AocType != AocTypes.EOP,
    ComputeAllocateTechnicalMarginWithIfrsVariable: lambda x: x.storage.IsSecondaryScope(x.Identity.DataNode),
    AllocateTechnicalMarginForBop: lambda x: x.Identity.AocType == AocTypes.BOP,
    AllocateTechnicalMarginForCl: lambda x: x.Identity.AocType == AocTypes.CL,
    AllocateTechnicalMarginForEop: lambda x: x.Identity.AocType == AocTypes.EOP
}


class ContractualServiceMargin(IScope):      #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.C
    
    @cached_property
    def Value(self) -> float:
        return -1 * self.GetScope(AllocateTechnicalMargin, self.Identity, self.EstimateType).Value


class LossComponent(IScope):     #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.L
    
    @cached_property
    def Value(self) -> float:
        return self.GetScope(AllocateTechnicalMargin, self.Identity, self.EstimateType).Value


class LossRecoveryComponent(IScope):     #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EstimateType(self) -> str:
        return EstimateTypes.LR

    @cached_property
    def Value(self) -> float:
        return self.GetScope(AllocateTechnicalMargin, self.Identity, self.EstimateType).Value


class DeferrableToIfrsVariable(IScope):   #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def DeferrableActual(self) -> [IfrsVariable]:

        x = self.GetScope(DeferrableActual, self.Identity)

        if abs(x.Value) >= Precision:
            return [IfrsVariable(
                Id=uuid.uuid4(),
                EstimateType=x.EstimateType,
                 DataNode=x.Identity.DataNode,
                 AocType=x.Identity.AocType,
                 Novelty=x.Identity.Novelty,
                 AccidentYear=0,
                 AmountType='',
                 Value=x.Value,
                 Partition=self.storage.TargetPartition
                 )]
        else:
            return []


class EaForPremiumToIfrsVariable(IScope):  #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def BeEAForPremium(self) -> [IfrsVariable]:

        if self.storage.DataNodeDataBySystemName[self.Identity.DataNode].LiabilityType == LiabilityTypes.LIC or self.Identity.IsReinsurance:
            return []
        else:
            result = []
            for sc in self.GetScope(BeExperienceAdjustmentForPremium, self.Identity).ByAmountType:
                if abs(sc.Value) >= Precision:
                     result.append( IfrsVariable(
                         Id=uuid.uuid4(),
                        EstimateType=self.GetScope(BeExperienceAdjustmentForPremium, self.Identity).EstimateType,
                        DataNode=sc.Identity.Id.DataNode,
                        AocType=sc.Identity.Id.AocType,
                        Novelty=sc.Identity.Id.Novelty,
                        AccidentYear=sc.Identity.AccidentYear,
                        EconomicBasis=sc.EconomicBasis,
                        AmountType=sc.Identity.AmountType,
                        Value=sc.Value,
                        Partition=sc.storage.TargetPartition ))

        return result

    @cached_property
    def ActEAForPremium(self) -> [IfrsVariable]:

        if self.storage.DataNodeDataBySystemName[self.Identity.DataNode].LiabilityType == LiabilityTypes.LIC or self.Identity.IsReinsurance:
            return []
        else:
            result = []
            for sc in self.GetScope(ActualExperienceAdjustmentOnPremium, self.Identity).ByAmountTypeAndEstimateType:
                if abs(sc.Value) >= Precision:
                                result.append(IfrsVariable(
                                    Id=uuid.uuid4(),
                                    EstimateType=self.storage.ExperienceAdjustEstimateTypeMapping[sc.Identity.EstimateType],
                                                 DataNode=sc.Identity.Id.DataNode,
                                                 AocType=sc.Identity.Id.AocType,
                                                 Novelty=sc.Identity.Id.Novelty,
                                                 AccidentYear=sc.Identity.AccidentYear,
                                                 #EconomicBasis=scope.EconomicBasis,
                                                 AmountType=sc.Identity.AmountType,
                                                 Value=sc.Value,
                                                 Partition=self.storage.TargetPartition))

        return result


class TmToIfrsVariable(IScope):    #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def EconomicBasis(self) -> str:
        return EconomicBases.C if self.Identity.ValuationApproach == ValuationApproaches.VFA else EconomicBases.L

    @cached_property
    def AmortizationFactor(self) -> list[IfrsVariable]:

        if self.Identity.AocType == AocTypes.AM:

            result = []
            x = self.GetScope(CurrentPeriodAmortizationFactor, self.Identity, self.EconomicBasis)
            if abs(x.Value) >= Precision:
                result.append(IfrsVariable(
                    Id=uuid.uuid4(),
                    AmountType='',
                    AccidentYear=0,
                    EstimateType=x.EstimateType,
                    DataNode=x.Identity.DataNode,
                    AocType=x.Identity.AocType,
                    Novelty=x.Identity.Novelty,
                    EconomicBasis=x.EconomicBasis,
                    Value=x.Value,
                    Partition=self.storage.TargetPartition
                    ))
            return result
        else:
            return []


    @cached_property
    def Csms(self) -> list[IfrsVariable]:

        if self.storage.DataNodeDataBySystemName[self.Identity.DataNode].LiabilityType == LiabilityTypes.LIC:
            return []
        else:
            result = []
            x = self.GetScope(ContractualServiceMargin, self.Identity)
            if abs(x.Value) >= Precision:
                if not (existing := self.storage.GetIfrsVariable(
                    id_=x.Identity,
                    amountType='',
                    estimateType=x.EstimateType,
                    economicBasis='',
                    accidentYear=0)
                ):
                    result.append(IfrsVariable(
                        Id=uuid.uuid4(),
                        AmountType='',
                        AccidentYear=0,
                        EconomicBasis='',
                        EstimateType=x.EstimateType,
                        DataNode=x.Identity.DataNode,
                        AocType=x.Identity.AocType,
                        Novelty=x.Identity.Novelty,
                        Value=x.Value,
                        Partition=self.storage.TargetPartition))
                else:
                    assert abs(existing.Value - x.Value) < Precision

            return result


    @cached_property
    def Loss(self) -> list[IfrsVariable]:
        if self.storage.DataNodeDataBySystemName[self.Identity.DataNode].LiabilityType == LiabilityTypes.LIC:
            return []

        else:
            if self.Identity.IsReinsurance:
                result = []
                x = self.GetScope(LossRecoveryComponent, self.Identity)
                if abs(x.Value)>= Precision:
                    result.append(IfrsVariable(
                        Id=uuid.uuid4(),
                        AmountType='',
                        AccidentYear=0,
                        EconomicBasis='',
                        EstimateType=x.EstimateType,
                        DataNode=x.Identity.DataNode,
                        AocType=x.Identity.AocType,
                        Novelty=x.Identity.Novelty,
                        Value=x.Value,
                        Partition=self.storage.TargetPartition
                    ))
            else:
                result = []
                x = self.GetScope(LossComponent, self.Identity)
                if abs(x.Value) >= Precision:
                   result.append(
                       IfrsVariable(
                           Id=uuid.uuid4(),
                           AmountType='',
                           AccidentYear=0,
                           EconomicBasis='',
                           EstimateType=x.EstimateType,
                           DataNode=x.Identity.DataNode,
                           AocType=x.Identity.AocType,
                           Novelty=x.Identity.Novelty,
                           Value=x.Value,
                           Partition=self.storage.TargetPartition
                                                            ))

            return result


class ActualToIfrsVariable(IScope):    #<ImportIdentity, ImportStorage>

    identity_type = ImportIdentity
    valid_contexts = ('',)

    @cached_property
    def Actual(self) -> list[IfrsVariable]:

        result = []
        for x in self.GetScope(Actual, self.Identity).Actuals:
            if x.Identity.Id.AocType != AocTypes.CF and x.Identity.Id.AocType != AocTypes.WO:
                if abs(x.Value) >= Precision:
                    if not (existing := self.storage.GetIfrsVariable(
                            id_=x.Identity.Id,
                            amountType=x.Identity.AmountType,
                            estimateType=x.Identity.EstimateType,
                            economicBasis='',
                            accidentYear=x.Identity.AccidentYear
                    )):
                        result.append(IfrsVariable(
                            Id=uuid.uuid4(),
                            EstimateType=x.Identity.EstimateType,
                            DataNode=x.Identity.Id.DataNode,
                            AocType=x.Identity.Id.AocType,
                            Novelty=x.Identity.Id.Novelty,
                            AccidentYear=x.Identity.AccidentYear,
                            AmountType=x.Identity.AmountType,
                            Value=x.Value,
                            Partition=self.storage.TargetPartition
                        ))
                    else:
                        assert existing.Value == x.Value
        return result

    @cached_property
    def AdvanceActual(self) -> list[IfrsVariable]:
        result = []
        for x in self.GetScope(AdvanceActual, self.Identity).Actuals:
            if x.Identity.Id.AocType != AocTypes.CF and x.Identity.Id.AocType != AocTypes.WO:
                if abs(x.Value) >= Precision:
                    if not (existing := self.storage.GetIfrsVariable(
                            id_=x.Identity.Id,
                            amountType=x.Identity.AmountType,
                            estimateType=x.Identity.EstimateType,
                            economicBasis='',
                            accidentYear=x.Identity.AccidentYear
                    )):
                        result.append(IfrsVariable(
                            Id=uuid.uuid4(),
                            EstimateType=x.Identity.EstimateType,
                            DataNode=x.Identity.Id.DataNode,
                            AocType=x.Identity.Id.AocType,
                            Novelty=x.Identity.Id.Novelty,
                            AccidentYear=x.Identity.AccidentYear,
                            AmountType=x.Identity.AmountType,
                            Value=x.Value,
                            Partition=self.storage.TargetPartition
                        ))
                    else:
                        assert existing.Value == x.Value
        return result

    @cached_property
    def OverdueActual(self) -> list[IfrsVariable]:
        result = []
        for x in self.GetScope(OverdueActual, self.Identity).Actuals:
            if x.Identity.Id.AocType != AocTypes.CF and x.Identity.Id.AocType != AocTypes.WO:
                if abs(x.Value) >= Precision:
                    if not (existing := self.storage.GetIfrsVariable(
                            id_=x.Identity.Id,
                            amountType=x.Identity.AmountType,
                            estimateType=x.Identity.EstimateType,
                            economicBasis='',
                            accidentYear=x.Identity.AccidentYear
                    )):
                        result.append(IfrsVariable(
                            Id=uuid.uuid4(),
                            EstimateType=x.Identity.EstimateType,
                            DataNode=x.Identity.Id.DataNode,
                            AocType=x.Identity.Id.AocType,
                            Novelty=x.Identity.Id.Novelty,
                            AccidentYear=x.Identity.AccidentYear,
                            AmountType=x.Identity.AmountType,
                            Value=x.Value,
                            Partition=self.storage.TargetPartition
                        ))
                    else:
                        assert existing.Value == x.Value
        return result


class ComputeIfrsVarsCashflows(
    PvToIfrsVariable, RaToIfrsVariable, DeferrableToIfrsVariable, EaForPremiumToIfrsVariable, TmToIfrsVariable):

    @cached_property
    def CalculatedIfrsVariables(self) -> list[IfrsVariable]:
        return (self.PvLocked + self.PvCurrent + self.RaCurrent
                + self.RaLocked + self.AmortizationFactor
                + self.BeEAForPremium) # + self.DeferrableActual
                # + self.Csms + self.Loss)


class ComputeIfrsVarsActuals(ActualToIfrsVariable, DeferrableToIfrsVariable, EaForPremiumToIfrsVariable, TmToIfrsVariable):

    @cached_property
    def CalculatedIfrsVariables(self) -> list[IfrsVariable]:
        return self.Actual + self.AdvanceActual + self.OverdueActual + self.ActEAForPremium + self.DeferrableActual + self.Csms + self.Loss


class ComputeIfrsVarsOpenings(ActualToIfrsVariable, DeferrableToIfrsVariable, TmToIfrsVariable):

    @cached_property
    def CalculatedIfrsVariables(self) -> list[IfrsVariable]:
        return []
        # return self.AdvanceActual + self.OverdueActual + self.DeferrableActual # + self.Csms + self.Loss


IfrsWorkspace.compute_targets[ImportFormats.Cashflow] = ComputeIfrsVarsCashflows
IfrsWorkspace.compute_targets[ImportFormats.Actual] = ComputeIfrsVarsActuals
IfrsWorkspace.compute_targets[ImportFormats.Opening] = ComputeIfrsVarsOpenings



