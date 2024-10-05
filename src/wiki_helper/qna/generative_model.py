import abc
import typing as t

TI = t.TypeVar("TI")


class GenerativeModelError(Exception):
    pass


class GenerativeModel(t.Generic[TI], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self, prompt_data: TI) -> str:
        raise NotImplementedError
