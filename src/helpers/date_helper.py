import datetime


def format_date(date: datetime.date) -> str:
    return date.strftime("%Y-%m-%d")


def get_date_today() -> str:
    return format_date(datetime.date.today())


def get_date_with_offset(offset: int) -> str:
    return format_date(datetime.date.today() + datetime.timedelta(days=offset))


def get_only_day(date_str: str) -> int:
    return int(date_str[-2:])
