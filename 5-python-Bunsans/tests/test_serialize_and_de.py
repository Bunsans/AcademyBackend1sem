import random
import string
import pytest


@pytest.fixture(params=[1024, 1024 * 1024, 10 * 1024 * 1024])
def test_data_serialize_and_de_with_size(benchmark, request) -> str:
    """Fixture for making list of strings serialize and deserialize."""

    size_in_bytes = request.param
    benchmark.group = (
        f"serialize and deserialize with size {size_in_bytes / (1024 * 1024)} bytes"
    )
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=size_in_bytes)
    )


def test__serialize_and_de_json__benchmark(
    test_serilizer, test_data_serialize_and_de_with_size, benchmark
):
    benchmark(
        test_serilizer.serialize_and_de_json, data=test_data_serialize_and_de_with_size
    )


def test__serialize_and_de_pickle__benchmark(
    test_serilizer, test_data_serialize_and_de_with_size, benchmark
):
    benchmark(
        test_serilizer.serialize_and_de_pickle,
        data=test_data_serialize_and_de_with_size,
    )


def test__serialize_and_de_msgpack__benchmark(
    test_serilizer, test_data_serialize_and_de_with_size, benchmark
):
    benchmark(
        test_serilizer.serialize_and_de_msgpack,
        data=test_data_serialize_and_de_with_size,
    )
