import abc
import typing as t

from yarl import URL

TO = t.TypeVar("TO")


class RagSystemError(Exception):
    pass


class RagSystem(t.Generic[TO], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def train(self, location: URL) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def answer(self, query: str) -> TO:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self) -> None:
        raise NotImplementedError
