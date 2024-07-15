from datetime import datetime, timezone


def get_utc_datetime_now_without_timezone():
    return datetime.now(timezone.utc).replace(tzinfo=None)
