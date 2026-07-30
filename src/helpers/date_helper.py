import datetime


def format_date(date):
    return date.strftime('%Y-%m-%d')


def get_date_today():
    return format_date(datetime.date.today())


def get_date_with_offset(offset):
    return format_date(datetime.date.today() + datetime.timedelta(days=offset))


def get_only_day(date_str):
    return int(date_str[-2:])
