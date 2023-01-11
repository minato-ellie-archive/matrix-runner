import pytest

from matrunner.engine.single_thread import *


class TestSingleThreadEngine:
    def _gen_test_fn(self):
        def test_fn(*args, **kwargs):
            return 1, args, kwargs

        return test_fn

    def _gen_test_data(self):
        return [[1, ], [2, ], [3, ]], [{'a': 1}, {'b': 2}, {'c': 3}]

    def test_run(self):
        engine = SingleThreadEngine(self._gen_test_fn())
        args, kwargs = self._gen_test_data()
        result = engine.run(args, kwargs)
        assert result == [(1, (1,), {'a': 1}), (1, (2,), {'b': 2}), (1, (3,), {'c': 3})]

    def test_run_with_exception(self):
        def sample_fn(*args, **kwargs):
            raise Exception('test exception')

        engine = SingleThreadEngine(sample_fn)
        args, kwargs = self._gen_test_data()
        with pytest.raises(Exception):
            engine.run(args, kwargs)

    def test_decorator(self):
        @SingleThreadEngine
        def sample_fn(*args, **kwargs):
            return 1, args, kwargs

        args, kwargs = self._gen_test_data()
        result = sample_fn.run(args, kwargs)
        assert result == [(1, (1,), {'a': 1}), (1, (2,), {'b': 2}), (1, (3,), {'c': 3})]
        assert sample_fn.__name__ == 'sample_fn'
        assert isinstance(sample_fn, SingleThreadEngine)
