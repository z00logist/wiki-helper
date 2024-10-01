import abc
import typing as t


TI = t.TypeVar("TI")
TO = t.TypeVar("TO")


class StorageError(Exception):
    pass


class Storage(t.Generic[TI, TO], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def store(self, content: TI) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, key: TI) -> TO:
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self) -> None:
        raise NotImplementedError
