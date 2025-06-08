import contextlib
from src.visual import print_hangman
import pytest
import filecmp


def write_in_file(lifes_test, path_test_tmp):
    with open(path_test_tmp, "w") as f, contextlib.redirect_stdout(f):
        print_hangman(lifes=lifes_test)


@pytest.mark.parametrize(
    "lifes_test",
    [i for i in range(11)],
)
def test_print_hangman(lifes_test):
    path_test_tmp = "tests/files/test_print_hangman_tmp.txt"
    write_in_file(lifes_test, path_test_tmp)
    result = filecmp.cmp(
        path_test_tmp, f"tests/files/test_print_hangman_lifes={lifes_test}.txt"
    )
    assert result
