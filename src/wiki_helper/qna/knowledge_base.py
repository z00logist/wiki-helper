import abc
import typing as t


TI = t.TypeVar("TI")
TO = t.TypeVar("TO")


class KnowledgeBaseError(Exception):
    pass


class KnowledgeBase(t.Generic[TI, TO], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_content(self, location_key: TI) -> TO:
        raise NotImplementedError
