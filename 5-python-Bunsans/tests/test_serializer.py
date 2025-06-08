import random
import string
import pytest


@pytest.fixture(params=[1024, 1024 * 1024, 10 * 1024 * 1024])
def test_data_serialize_with_size(benchmark, request) -> str:
    """Fixture for making list of strings serialize."""
    size_in_bytes = request.param
    benchmark.group = f"serialize with size {size_in_bytes / (1024 * 1024)} mb"
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=size_in_bytes)
    )


def test__serialize_json__benchmark(
    test_serilizer, test_data_serialize_with_size, benchmark
):
    benchmark(test_serilizer.serialize_json, data=test_data_serialize_with_size)


def test__serialize_pickle__benchmark(
    test_serilizer, test_data_serialize_with_size, benchmark
):
    benchmark(test_serilizer.serialize_pickle, data=test_data_serialize_with_size)


def test__serialize_msgpack__benchmark(
    test_serilizer, test_data_serialize_with_size, benchmark
):
    benchmark(test_serilizer.serialize_msgpack, data=test_data_serialize_with_size)
