from datetime import datetime

from pytz import timezone


def get_datetime() -> datetime:
    return datetime.now(timezone("Asia/Kuala_Lumpur"))
