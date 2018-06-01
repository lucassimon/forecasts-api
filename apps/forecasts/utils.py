# -*- coding: utf-8 -*-

# Python
import datetime

# Apps


# Local

from .models import Forecast


def convert_period_to_time(value):
    if not isinstance(value, str):
        raise ValueError('Value is a string and format HH:MM')

    value = value.split(":")
    return datetime.time(int(value[0]), int(value[1]))


def check_period_is_valid(start, period, end):
    start = convert_period_to_time(start)
    end = convert_period_to_time(end)

    return start <= period <= end


def get_settings_by_weekday(weekday):
    settings = []

    if weekday == 1:
        settings = Forecast.objects.filter(days__monday=True)
    elif weekday == 2:
        settings = Forecast.objects.filter(days__tuesday=True)
    elif weekday == 3:
        settings = Forecast.objects.filter(days__wednesday=True)
    elif weekday == 4:
        settings = Forecast.objects.filter(days__thursday=True)
    elif weekday == 5:
        settings = Forecast.objects.filter(days__friday=True)
    elif weekday == 6:
        settings = Forecast.objects.filter(days__saturday=True)
    elif weekday == 7:
        settings = Forecast.objects.filter(days__sunday=True)

    return settings
