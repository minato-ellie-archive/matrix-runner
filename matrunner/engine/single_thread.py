from typing import Callable, List, Optional

from .base import BaseEngine, TResult


class SingleThreadEngine(BaseEngine):
    def __init__(self, func: Callable[..., TResult], *args, **kwargs):
        super().__init__(func)

    def run(
            self,
            args_list: Optional[List[tuple]] = None,
            kwargs_list: Optional[List[dict]] = None
    ) -> List[TResult]:
        if args_list is None:
            args_list = [()] * len(kwargs_list)
        if kwargs_list is None:
            kwargs_list = [{}] * len(args_list)
        assert len(args_list) == len(kwargs_list), "args_list and kwargs_list must have the same length"
        return [self.fn(*args, **kwargs) for args, kwargs in zip(args_list, kwargs_list)]
