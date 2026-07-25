import datetime


def format_date(date):
    return date.strftime('%Y-%m-%d')


def get_date_today():
    return format_date(datetime.date.today())


def get_future_date(delta_in_days):
    return format_date(datetime.date.today() + datetime.timedelta(days=delta_in_days))


def get_past_date(delta_in_days):
    return format_date(datetime.date.today() - datetime.timedelta(days=delta_in_days))


def get_only_day(date_str):
    return int(date_str[-2:])
