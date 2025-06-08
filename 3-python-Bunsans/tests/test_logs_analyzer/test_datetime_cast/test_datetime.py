import datetime
import pytest
from src.logs_analyzer import (
    _cast_to_datetime_from,
    _cast_to_datetime_to,
    _get_date_time,
)

# def _cast_to_datetime_from(datetime_str: str) -> datetime.datetime:
#     if datetime_str is None:
#         return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
#     return _get_date_time(datetime_str)


# def _cast_to_datetime_to(datetime_str: str) -> datetime.datetime:
#     if datetime_str is None:
#         return datetime.datetime.max.replace(tzinfo=datetime.timezone.utc)
#     return _get_date_time(datetime_str)


# def _get_date_time(datetime_str: str) -> datetime.datetime:
#     formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
#     for fmt in formats:
#         try:
#             return datetime.datetime.strptime(datetime_str, fmt)
#         except ValueError:
#             continue
#     raise ValueError(
#         f'Invalid datetime format: {datetime_str}\nTry to use format: "%Y-%m-%d %H:%M:%S" or "%Y-%m-%d"'
#     )
@pytest.parametrize(
    "datetime_str, result", ("2024-11-29 10:00:00", datetime.datetime())
)
def test__get_date_time(datetime_str, result, exception):
    with pytest.raises(
        ValueError,
        match=f'Invalid datetime format: {datetime_str}\nTry to use format: "%Y-%m-%d %H:%M:%S" or "%Y-%m-%d"',
    ):
        res = _get_date_time(datetime_str=datetime_str)
    assert res == result


@pytest.parametrize("datetime_str, result", ("2024-11-29 10:00:00",))
def test__cast_to_datetime_to_bad_case(datetime_str, result):
    with pytest.raises(ValueError):
        res = _cast_to_datetime_to(datetime_str=datetime_str)
    assert res == result


@pytest.parametrize(
    "datetime_str, result", ("2024-11-29 10:00:00", "%Y-%m-%d %H:%M:%S")
)
def test__cast_to_datetime_from_bad_case(datetime_str, result):
    with pytest.raises(ValueError):
        res = _cast_to_datetime_from(datetime_str=datetime_str)
    assert res == result
