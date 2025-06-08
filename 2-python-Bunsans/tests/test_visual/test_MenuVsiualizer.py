import pytest
from src.visual.message_phrase import MessageWrongSize
from tests.test_cases import test_check_check_coordinate_cases, test_check_size_cases


class TestMenuVsiualizer:
    @pytest.mark.parametrize("width, height, message_wrong_res", test_check_size_cases)
    def test_check_size(self, width, height, message_wrong_res, menu_vsiualizer):
        message_wrong_in = MessageWrongSize(
            "",
            "",
            "",
        )
        message_wrong = menu_vsiualizer._check_size(message_wrong_in, width, height)

        assert message_wrong.wrong_bound == message_wrong_res.wrong_bound
        assert message_wrong.wrong_odd == message_wrong_res.wrong_odd
        assert message_wrong.wrong_answ == message_wrong_res.wrong_answ

    @pytest.mark.parametrize(
        "answer_, descr, result_",
        test_check_check_coordinate_cases,
    )
    def test_check_coordinate(self, answer_, descr, result_, menu_vsiualizer):
        answer_ = answer_
        result = menu_vsiualizer._check_coordinate(answer=answer_, max_=13, descr=descr)
        assert result == result_
