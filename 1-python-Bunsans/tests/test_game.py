import filecmp
from src.game import Game
import contextlib
import pytest


@pytest.mark.parametrize(
    "word_test, predicted_letters_test, after_change_test",
    [("aboba", ["a", "b"], "ab_ba"), ("aboba", ["a", "b", "o"], "aboba")],
)
def test_change_curr_result(word_test, predicted_letters_test, after_change_test):
    level = 1
    game = Game(level)
    game.word = word_test
    game.predicted_letters = predicted_letters_test
    game.curr_result = ""

    game.change_curr_result()

    after_change = game.curr_result
    assert after_change == after_change_test


def write_in_file(game, path_test_tmp):
    path_test_tmp = "tests/files/test_print_stage_tmp.txt"
    with open(path_test_tmp, "w") as f, contextlib.redirect_stdout(f):
        game.print_stage("Test")


@pytest.mark.parametrize(
    "word_test, predicted_letters_test, used_letters_test, path_test",
    [("aboba", ["a", "b"], ["a", "b", "g"], "tests/files/test_print_stage.txt")],
)
def test_print_stage(word_test, predicted_letters_test, used_letters_test, path_test):
    path_test_tmp = "tests/files/test_print_stage_tmp.txt"
    level = 1
    game = Game(level)
    game.word = word_test
    game.predicted_letters = predicted_letters_test
    game.used_letters = used_letters_test
    game.curr_result = ""

    write_in_file(game, path_test_tmp)

    result = filecmp.cmp(path_test_tmp, path_test)
    assert result
