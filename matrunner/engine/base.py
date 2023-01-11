from abc import ABCMeta, abstractmethod
from typing import Callable, List, TypeVar, Union, Any
from functools import wraps

TResult = TypeVar('TResult')


class BaseEngine(metaclass=ABCMeta):
    def __init__(self, fn: Callable[..., TResult]):
        self.__name__ = fn.__name__
        self.fn = fn

    @abstractmethod
    def run(self, args_list: Union[list, tuple], kwargs_list: Union[list, tuple]) -> List[TResult]: ...

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


BaseEngineDecorator = Callable[[Callable[..., TResult]], BaseEngine]
