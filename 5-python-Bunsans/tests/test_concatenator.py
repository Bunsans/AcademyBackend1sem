from loguru import logger
import pytest


@pytest.fixture(
    params=[int(1e3), int(1e4), int(1e5)],
)
def test_list_of_strings(request, benchmark) -> str:
    """Fixture for making list of strings for concatenation."""
    benchmark.group = f"concatenate with size {request.param} elements"
    return ["string_" + str(i) for i in range(request.param)]


@pytest.mark.benchmark(group="test_concatenator")
def test__concatenate_with_plus__benchmark(
    test_concatenator, test_list_of_strings, benchmark
):
    benchmark(test_concatenator.plus_concatenate, test_list_of_strings)
    logger.warning(f"result: {test_list_of_strings}")
    test_list_of_strings = list(test_list_of_strings)


@pytest.mark.benchmark(group="test_concatenator")
def test__concatenate_with_join__benchmark(
    test_concatenator, test_list_of_strings, benchmark
):
    benchmark(test_concatenator.join_concatenate, test_list_of_strings)
