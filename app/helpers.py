from datetime import datetime, date, time, timedelta
from typing import Union


TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%Y-%m-%d"


def is_time_right_format(time_string: str) -> bool:
    try:
        t = datetime.strptime(time_string, TIME_FORMAT).time()

        # This filters out situation when user passed one number as minutes, like `16:0` or `09:5`.
        # Minutes must contain 2 digits.
        if len(time_string.split(":")[1]) != 2:
            return False

        # Time has to be between `05:00` and `19:55`.
        if t.hour < 5 or t.hour > 19:
            return False

        # Minutes must be divisible by 5.
        return t.minute % 5 == 0
    except ValueError:
        return False


def dt_time_min(dt: Union[datetime, date]) -> datetime:
    """
    Converts any datetime/date to new datetime with same date and time=0:00:00
    """
    return datetime.combine(dt, time.min)


def dt_time_max(dt: Union[datetime, date]) -> datetime:
    """
    Converts any datetime/date to new datetime with same date and time=23:59:59.999999
    """
    return datetime.combine(dt, time.max)


def subtract_days_from_datetime(input_datetime: datetime, days_to_subtract: int) -> datetime:
    """
    Returns a new datetime that is the specified number of days earlier.
    """
    return input_datetime - timedelta(days=days_to_subtract)


def get_dates_between(start_date: datetime, end_date: datetime) -> list[date]:
    """
    Get a list of all dates between the given start and end datetimes, inclusive.
    """
    return [(start_date + timedelta(days=i)).date() for i in range((end_date - start_date).days + 1)]
