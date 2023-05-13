
def GetElementOrDefault(array: list, index: int):
    return array[min(index, len(array) - 1)] if array else 0


def AggregateDoubleArray(source):

    if not (size := max((len(nested) for nested in source), default=0)):
        return []

    result = [0] * size

    for nested in source:
        for i in range(len(nested)):
            result[i] += nested[i]

    return result
