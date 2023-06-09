from datetime import datetime

import pytz


def current_datetime_after_given_iso_string(value: str) -> bool:
    # Grab local timezone
    uk_tz = pytz.timezone("Europe/London")
    # Grab current localised datetime
    now_datetime = datetime.now(uk_tz)
    # Convert now_datetime to offset-naive
    now_datetime_naive = now_datetime.replace(tzinfo=None)
    # Convert value datetime to correct format for comparison
    parsed = datetime.fromisoformat(value)
    return now_datetime_naive > parsed


def current_datetime_before_given_iso_string(value: str) -> bool:
    # Grab local timezone
    uk_tz = pytz.timezone("Europe/London")
    # Grab current localised datetime
    now_datetime = datetime.now(uk_tz)
    # Convert now_datetime to offset-naive
    now_datetime_naive = now_datetime.replace(tzinfo=None)
    # Convert value datetime to correct format for camparison
    parsed = datetime.fromisoformat(value)
    return now_datetime_naive < parsed
