import pytest

from app.helpers import is_time_right_format


@pytest.mark.parametrize(
    "time_string,expected_result",
    (
        ("00:0", False),
        ("06:01", False),
        ("10:5", False),
        ("18:8", False),
        ("20:33", False),
        ("21:68", False),
        ("23:59", False),
        ("00:00", True),
        ("03:10", True),
        ("18:25", True),
        ("22:55", True),
    )
)
def test_is_time_right_format(time_string: str, expected_result: bool):
    assert is_time_right_format(time_string) is expected_result
