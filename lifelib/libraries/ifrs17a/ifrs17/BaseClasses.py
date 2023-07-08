import dataclasses
import uuid
from dataclasses import dataclass
from typing import (TypeVar, Generic, Iterable, Collection)
import pandas as pd

__all__ = ('Guid', 'BaseDatabase', 'INamed', 'IOrdered', 'IKeyedType', 'IDataSet', 'IDataRow')

IdentityType = TypeVar('IdentityType')
StorageType = TypeVar('StorageType')

IEnumerable = Iterable

Guid = uuid.UUID


class INamed:
    pass


class IOrdered:
    pass

@dataclass
class IScope(Generic[IdentityType, StorageType]):
    Identiry: IdentityType


@dataclass
class IDataSet:
    Tables: dict[str, 'pandas.DataFrame']


class IDataRow:
    pass


class IKeyedType(type):
    pass



class _Partition:

    def __init__(self, data: 'BaseDatabase'):
        self._querysource = data

    def GetKeyForInstance(self, PartitionType: IKeyedType, args: Generic):
        try:
            partitions = self._querysource.Query(PartitionType)
        except KeyError:
            return uuid.uuid4()

        fields = set(f.name for f in dataclasses.fields(PartitionType))
        fields.remove('Id')

        found = False
        for x in partitions:
            if all(getattr(args, f) == getattr(x, f) for f in fields):
                found = True
                break

        if found:
            return x.Id
        else:
            return uuid.uuid4()

    def Set(self, PartitionType: IKeyedType, Id: Guid):
        self._querysource._current_partition[PartitionType.__name__] = Id

    def GetCurrent(self, TypeName: str):
        return self._querysource._current_partition[TypeName]


class BaseDatabase:

    def __init__(self):

        self._data = {}
        self._current_partition = {}
        self.Partition = _Partition(self)

    def Reset(self):
        self._data.clear()
        self._current_partition.clear()

    @staticmethod
    def _query2df(query) -> pd.DataFrame:

        data = []
        for q in query:
            data.append(dataclasses.asdict(q))

        return pd.DataFrame.from_records(data)

    def Query(self, type_: type, partition=None, include_sub=True, as_df=False):

        result = []
        if include_sub:
            for k in self._data:
                if issubclass(k, type_):
                    result.extend(self._data[k])
        else:
            result.extend(self._data[type_])

        if partition is not None:
            result = [v for v in result if v.Partition == partition]

        if as_df:
            return self._query2df(result)
        else:
            return result

    def Delete(self, type_: type, data: Collection):
        records = self._data.get(type_, [])
        for r in records.copy():
            if r in data:
                records.remove(r)

    def Update(self, type_: type, data: Collection):
        vals = self._data.setdefault(type_, [])
        if hasattr(type_, '__eq__'):
            for x in data:
                if x not in vals:
                    vals.append(x)
        else:
            vals.extend(data)

    def Update2(self, data):
        self.Update(type(data), [data])

    def Update3(self, datalist):
        assert len(set(type(x) for x in datalist)) <= 1
        for x in datalist:
            self.Update2(x)







