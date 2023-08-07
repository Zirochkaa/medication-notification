from datetime import datetime


TIME_FORMAT = "%H:%M"


def is_time_right_format(time_string: str) -> bool:
    try:
        datetime.strptime(time_string, TIME_FORMAT).time()
        return True
    except ValueError:
        return False
