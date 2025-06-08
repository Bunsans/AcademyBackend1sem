import pytest

from src.concatenator_ import Concatenator
from src.list_creator_ import ListCreator
from src.serializer_ import Serializer


@pytest.fixture(scope="session")
def test_concatenator() -> Concatenator:
    return Concatenator()


@pytest.fixture(scope="session")
def test_list_creator() -> ListCreator:
    return ListCreator()


@pytest.fixture(scope="session")
def test_serilizer() -> Serializer:
    return Serializer()
