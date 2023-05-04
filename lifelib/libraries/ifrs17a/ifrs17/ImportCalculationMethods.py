from .DataStructure import *

def GetReferenceAocStepForCalculated(identities: list[AocStep], aocConfigurationByAocStep: dict[AocStep, AocConfiguration], identityAocStep: AocStep) -> AocStep:

    for aocStep in reversed(identities):
        if (aocConfigurationByAocStep[aocStep].DataType != DataType.Calculated
                                            and aocConfigurationByAocStep[aocStep].DataType != DataType.CalculatedTelescopic
                                            and aocConfigurationByAocStep[aocStep].Order < aocConfigurationByAocStep[identityAocStep].Order
                                            and aocStep.Novelty == identityAocStep.Novelty):
            return aocStep

    return AocStep('', '')


def GetPreviousIdentities(identities: list[AocStep]) -> dict[AocStep, list[AocStep]]:

    bopNovelties = [id_.Novelty for id_ in identities if id_.AocType == AocTypes.BOP]
    previousStep = {n: AocStep(AocTypes.BOP, n) if n in bopNovelties else None for n in [Novelties.N, Novelties.I, Novelties.C]}

    temp = {}
    for id_ in identities:
        if id_.AocType != AocTypes.BOP:
            ret = [v for v in previousStep.values() if v] if id_.AocType == AocTypes.CL else [previousStep[id_.Novelty]] if previousStep[id_.Novelty] else []
            previousStep[id_.Novelty] = AocStep(id_.AocType, id_.Novelty)
            temp[id_] = ret

    return temp


def ExtendGroupOfContract(gic: GroupOfContract, datarow: IDataRow) -> GroupOfContract:
    return gic


def GetAmountTypesByEstimateType() -> dict[str, set[str]]:
    return {
        EstimateTypes.RA: set(),
        EstimateTypes.C: set(),
        EstimateTypes.L: set(),
        EstimateTypes.LR: set()
   }


def GetTechnicalMarginEstimateType() -> set[str]:
    return {EstimateTypes.C, EstimateTypes.L, EstimateTypes.LR,}

