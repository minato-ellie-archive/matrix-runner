from abc import ABCMeta, abstractmethod
from typing import Optional, Dict, List, TypeVar, Callable, Union
from itertools import product

from matrunner.engine import BaseEngine, SingleThreadEngine

TEngine = TypeVar('TEngine', bound=BaseEngine)


def filter_include(args_list: List[dict], include: dict) -> List[dict]:
    """
    Filters the given list of dictionaries based on the given filter dictionary. \n
    For each object in the include list, the key:value pairs in the object will be added to \
    each of the matrix combinations if none of the key:value pairs overwrite any of the original matrix values. \
    If the object cannot be added to any of the matrix combinations, a new matrix combination will be created \
    instead. Note that the original matrix values will not be overwritten, \
    but added matrix values can be overwritten.
    :param args_list: The list of dictionaries to filter.
    :param include: The dictionary to filter the list of dictionaries with.
    :return: The filtered list of dictionaries.
    """
    if not include:
        return args_list

    filtered_args = []
    for args in args_list:
        if all(
                (key not in args or args[key] == value for key, value in include.items())
        ):
            args.update(include)
        filtered_args.append(args)
    return filtered_args


def filter_exclude(args_list: List[dict], exclude: dict) -> List[dict]:
    """
    Filters the given list of dictionaries based on the given filter dictionary. \n
    An excluded configuration only has to be a partial match for it to be excluded.

    :param args_list: The list of dictionaries to filter.
    :param exclude: The dictionary to filter the list of dictionaries with.
    :return: The filtered list of dictionaries.
    """
    if not exclude:
        return args_list

    filtered_args = []
    for args in args_list:
        if all(
            exclude_item in args.items() for exclude_item in exclude.items()
        ):
            continue

        filtered_args.append(args)
    return filtered_args


class MatrixRunner:
    engine_dict: Dict[str, TEngine] = {
        'single_thread': SingleThreadEngine
    }

    def __init__(
            self,
            func: Union[Callable, TEngine],
            engine: Optional[Union[TEngine, str]] = None,
    ):
        self.fn = func
        if engine is not None:
            if isinstance(engine, str):
                engine = self._get_engine(engine)
            func = engine(func)

        if isinstance(func, BaseEngine):
            self._engine = func
        else:
            self._engine = SingleThreadEngine(func)

    @classmethod
    def _get_engine(cls, engine: str) -> TEngine:
        if engine not in cls.engine_dict:
            raise ValueError(f'Engine {engine} not found')

        return cls.engine_dict[engine]

    @staticmethod
    def _make_cartesian_product(matrix: Dict[str, list]) -> List[dict]:
        """
        Returns a new dictionary with the Cartesian product of each list in the original dictionary. \n
        Each key in the new dictionary corresponds to a key in the original dictionary, and the value \
        is the Cartesian product of the list that the key maps to in the original dictionary.
        :param matrix: The dictionary to make the Cartesian product of.
        :return: A new dictionary with the Cartesian product of each list in the original dictionary.
        """
        keys = matrix.keys()
        values = matrix.values()
        return [dict(zip(keys, v)) for v in product(*values)]

    @staticmethod
    def _filter_args(args: List[dict], filter_dict: List[dict], include: bool = False) -> List[dict]:
        """
        Filters the given list of dictionaries based on the given filter dictionary. \n
        If include is True, For each object in the include list, the key:value pairs in the object will be added to \
        each of the matrix combinations if none of the key:value pairs overwrite any of the original matrix values. \
        If the object cannot be added to any of the matrix combinations, a new matrix combination will be created \
        instead. Note that the original matrix values will not be overwritten, \
        but added matrix values can be overwritten. \n
        If include is False, An excluded configuration only has to be a partial match for it to be excluded. \
        :param args: The list of dictionaries to filter.
        :param filter_dict: The dictionary to filter the list of dictionaries with.
        :param include: Whether to include or exclude the given filter dictionary.
        :return: The filtered list of dictionaries.
        """
        if include:
            for filter_ in filter_dict:
                args = filter_include(args, filter_)
            return args
        else:
            for filter_ in filter_dict:
                args = filter_exclude(args, filter_)
            return args

    def __call__(
            self,
            matrix: Dict[str, list],
            *,
            include: Optional[Dict[str, list]] = None,
            exclude: Optional[Dict[str, list]] = None,
    ):
        assert all(isinstance(v, list) for v in matrix.values()), "matrix values must be lists"
        if include is not None:
            assert isinstance(include, dict), "include must be a dict"
            assert all(isinstance(v, list) for v in include.values()), "include values must be lists"
        if exclude is not None:
            assert isinstance(exclude, dict), "exclude must be a dict"
            assert all(isinstance(v, list) for v in exclude.values()), "exclude values must be lists"

        kwargs_list: list = self._make_cartesian_product(matrix)
        if include is not None:
            kwargs_list = self._filter_args(kwargs_list, include, True)
        if exclude is not None:
            kwargs_list = self._filter_args(kwargs_list, exclude, False)

        return self._engine(kwargs_list=kwargs_list)
