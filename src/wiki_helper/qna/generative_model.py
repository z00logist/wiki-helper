import abc
import typing as t

TI = t.TypeVar("TI")
TO = t.TypeVar("TO")


class GenerativeModelError(Exception):
    pass


class GenerativeModel(t.Generic[TI, TO], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self, prompt_data: TI) -> TO:
        raise NotImplementedError
