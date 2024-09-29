import abc

from yarl import URL


class RagSystemError(Exception):
    pass


class RagSystem(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def train(self, location: URL) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def answer(self, query: str) -> str:
        raise NotImplementedError
