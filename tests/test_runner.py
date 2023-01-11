import pytest

from matrunner.runner import *


class TestMatrixRunner:
    def _gen_sample_fn(self):
        def sample_fn(*args, **kwargs):
            return 1, args, kwargs

        return sample_fn

    def test_make_cartesian_product(self):
        dict_matrix = {
            "a": [1, 2],
            "b": [3, 4],
            "c": [5, 6],
        }
        expected = [
            {"a": 1, "b": 3, "c": 5},
            {"a": 1, "b": 3, "c": 6},
            {"a": 1, "b": 4, "c": 5},
            {"a": 1, "b": 4, "c": 6},
            {"a": 2, "b": 3, "c": 5},
            {"a": 2, "b": 3, "c": 6},
            {"a": 2, "b": 4, "c": 5},
            {"a": 2, "b": 4, "c": 6},
        ]
        runner = MatrixRunner(self._gen_sample_fn())
        assert runner._make_cartesian_product(dict_matrix) == expected

    def test_filter_include(self):
        args_list = [
            {"a": 1, "b": 3, "c": 5},
            {"a": 1, "b": 3, "c": 6},
            {"a": 1, "b": 4, "c": 5},
            {"a": 1, "b": 4, "c": 6},
            {"a": 2, "b": 3, "c": 5},
            {"a": 2, "b": 3, "c": 6},
            {"a": 2, "b": 4, "c": 5},
            {"a": 2, "b": 4, "c": 6},
        ]
        include = [{"a": 1, "b": 3, "d": 7}, ]
        target = [
            {"a": 1, "b": 3, "c": 5, "d": 7},
            {"a": 1, "b": 3, "c": 6, "d": 7},
            {"a": 1, "b": 4, "c": 5},
            {"a": 1, "b": 4, "c": 6},
            {"a": 2, "b": 3, "c": 5},
            {"a": 2, "b": 3, "c": 6},
            {"a": 2, "b": 4, "c": 5},
            {"a": 2, "b": 4, "c": 6},
        ]
        runner = MatrixRunner(self._gen_sample_fn())

        assert filter_exclude(args_list, include[0]) == target
        assert runner._filter_args(args_list, include, True) == target

        include = [
            {"a": 1, "b": 3, "d": 7},
            {"b": 4, "z": 0}
        ]
        target = [
            {"a": 1, "b": 3, "c": 5, "d": 7},
            {"a": 1, "b": 3, "c": 6, "d": 7},
            {"a": 1, "b": 4, "c": 5, "z": 0},
            {"a": 1, "b": 4, "c": 6, "z": 0},
            {"a": 2, "b": 3, "c": 5},
            {"a": 2, "b": 3, "c": 6},
            {"a": 2, "b": 4, "c": 5, "z": 0},
            {"a": 2, "b": 4, "c": 6, "z": 0},
        ]
        assert runner._filter_args(args_list, include, True) == target

    def test_filter_exclude(self):
        args_list = [
            {"a": 1, "b": 3, "c": 5},
            {"a": 1, "b": 3, "c": 6},
            {"a": 1, "b": 4, "c": 5},
            {"a": 1, "b": 4, "c": 6},
            {"a": 2, "b": 3, "c": 5},
            {"a": 2, "b": 3, "c": 6},
            {"a": 2, "b": 4, "c": 5},
            {"a": 2, "b": 4, "c": 6},
        ]
        exclude = [{"a": 1, "b": 3, "d": 5}, ]
        target = [
            {"a": 1, "b": 3, "c": 5},
            {"a": 1, "b": 3, "c": 6},
            {"a": 1, "b": 4, "c": 5},
            {"a": 1, "b": 4, "c": 6},
            {"a": 2, "b": 3, "c": 5},
            {"a": 2, "b": 3, "c": 6},
            {"a": 2, "b": 4, "c": 5},
            {"a": 2, "b": 4, "c": 6},
        ]
        runner = MatrixRunner(self._gen_sample_fn())

        assert filter_exclude(args_list, exclude[0]) == target
        assert runner._filter_args(args_list, exclude, False) == target

        exclude = [
            {"a": 1, "b": 3}
        ]
        target = [
            {"a": 1, "b": 4, "c": 5},
            {"a": 1, "b": 4, "c": 6},
            {"a": 2, "b": 3, "c": 5},
            {"a": 2, "b": 3, "c": 6},
            {"a": 2, "b": 4, "c": 5},
            {"a": 2, "b": 4, "c": 6},
        ]
        assert runner._filter_args(args_list, exclude, False) == target
