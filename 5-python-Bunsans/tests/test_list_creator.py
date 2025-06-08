import numpy as np
import pytest


@pytest.fixture(
    params=[
        int(1e3),
        int(1e4),
        int(1e5),
    ],
    autouse=True,
)
def test_length(request, benchmark) -> str:
    """Fixture for making group of bench and size of list."""
    benchmark.group = f"make list with size {request.param} elements"
    return request.param


def test__comprehension_list__benchmark(test_list_creator, test_length, benchmark):
    result = benchmark(test_list_creator.comprehension_list, test_length)
    assert result == list(range(test_length))


def test__loop_list__benchmark(test_list_creator, test_length, benchmark):
    result = benchmark(test_list_creator.loop_list, test_length)
    assert result == list(range(test_length))


def test__numpy_list__benchmark(test_list_creator, test_length, benchmark):
    result = benchmark(test_list_creator.numpy_list, test_length)
    assert (result == np.arange(test_length)).all()
