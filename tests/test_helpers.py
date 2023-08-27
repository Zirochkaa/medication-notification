from datetime import datetime, date
from typing import Union

import pytest

from app.helpers import (
    is_time_right_format, dt_time_min, dt_time_max, subtract_days_from_datetime, get_dates_between
)


@pytest.mark.parametrize(
    "time_string,expected_result",
    (
        ("00:0", False),
        ("10:5", False),
        ("18:8", False),

        ("00:00", False),
        ("03:10", False),
        ("06:01", False),
        ("20:33", False),

        ("04:55", False),
        ("20:00", False),
        ("22:55", False),
        ("23:59", False),

        ("21:68", False),

        ("05:00", True),
        ("10:05", True),
        ("18:25", True),
        ("19:55", True),
    )
)
def test_is_time_right_format(time_string: str, expected_result: bool):
    assert is_time_right_format(time_string) is expected_result


@pytest.mark.parametrize(
    "dt,expected_result",
    (
        (
            date(year=2023, month=8, day=16),
            datetime(year=2023, month=8, day=16, hour=0, minute=0)
        ),
        (
            datetime(year=2023, month=8, day=16, hour=11, minute=39, second=1),
            datetime(year=2023, month=8, day=16, hour=0, minute=0)
        ),
    )
)
def test_dt_time_min(dt: Union[datetime, date], expected_result: datetime):
    assert dt_time_min(dt) == expected_result


@pytest.mark.parametrize(
    "dt,expected_result",
    (
        (
            date(year=2023, month=8, day=16),
            datetime(year=2023, month=8, day=16, hour=23, minute=59, second=59, microsecond=999999)
        ),
        (
            datetime(year=2023, month=8, day=16, hour=11, minute=39, second=13, microsecond=123456),
            datetime(year=2023, month=8, day=16, hour=23, minute=59, second=59, microsecond=999999)
        ),
    )
)
def test_dt_time_max(dt: Union[datetime, date], expected_result: datetime):
    assert dt_time_max(dt) == expected_result


@pytest.mark.parametrize(
    "input_datetime,days_to_subtract,expected_result",
    (
        (
            datetime(year=2023, month=8, day=27, hour=23, minute=59, second=59, microsecond=999999),
            7,
            datetime(year=2023, month=8, day=20, hour=23, minute=59, second=59, microsecond=999999)
        ),
        (
            datetime(year=2023, month=8, day=27, hour=11, minute=39, second=13, microsecond=123456),
            0,
            datetime(year=2023, month=8, day=27, hour=11, minute=39, second=13, microsecond=123456),
        ),
    )
)
def test_subtract_days_from_datetime(input_datetime: datetime, days_to_subtract: int, expected_result: datetime):
    assert subtract_days_from_datetime(input_datetime, days_to_subtract) == expected_result


@pytest.mark.parametrize(
    "start_date,end_date,expected_result",
    (
        (
            datetime(year=2023, month=8, day=27, hour=2, minute=45, second=39, microsecond=999999),
            datetime(year=2023, month=8, day=27, hour=23, minute=59, second=59, microsecond=999999),
            [
                date(year=2023, month=8, day=27),
            ],
        ),
        (
            datetime(year=2023, month=8, day=26, hour=2, minute=45, second=39, microsecond=999999),
            datetime(year=2023, month=8, day=27, hour=23, minute=59, second=59, microsecond=999999),
            [
                date(year=2023, month=8, day=26),
                date(year=2023, month=8, day=27),
            ],
        ),
        (
            datetime(year=2023, month=8, day=27, hour=2, minute=45, second=39, microsecond=999999),
            datetime(year=2023, month=8, day=25, hour=23, minute=59, second=59, microsecond=999999),
            [],
        ),
        (
            datetime(year=2023, month=8, day=22, hour=2, minute=45, second=39, microsecond=999999),
            datetime(year=2023, month=8, day=27, hour=23, minute=59, second=59, microsecond=999999),
            [
                date(year=2023, month=8, day=22),
                date(year=2023, month=8, day=23),
                date(year=2023, month=8, day=24),
                date(year=2023, month=8, day=25),
                date(year=2023, month=8, day=26),
                date(year=2023, month=8, day=27),
            ],
        ),
    )
)
def test_get_dates_between(start_date: datetime, end_date: datetime, expected_result: datetime):
    assert get_dates_between(start_date, end_date) == expected_result
