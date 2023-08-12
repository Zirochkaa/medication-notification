from datetime import datetime


TIME_FORMAT = "%H:%M"


def is_time_right_format(time_string: str) -> bool:
    try:
        t = datetime.strptime(time_string, TIME_FORMAT).time()

        # This filters out situation when user passed one number as minutes, like `16:0` or `09:5`.
        # Minutes must contain 2 digits.
        if len(time_string.split(":")[1]) != 2:
            return False

        return t.minute % 5 == 0
    except ValueError:
        return False
