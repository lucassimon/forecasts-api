# -*- coding: utf-8 -*-
'''
We can use postmon or cepaberto, to get the address info
This file uses postmon because there is no necessary autenticate it
'''
# Python
import os

# Flask
from flask import current_app

# Third


# Apps
from apps.modules.openweathermap import OpenWeather


def weather(city):
    '''
    Use multiple providers.

    Example:
        - openweathermap
        - yahooweather
    '''

    openweather_enable = os.getenv('OPEN_WEATHER_ENABLE')
    yahooweather_enable = os.getenv('YAHOO_WEATHER_ENABLE')

    # TODO: search in another provider

    # TODO: Do a while or loop until error is false
    # and info is success

    # TODO: Attemps in each provider

    if openweather_enable:
        ow = OpenWeather(os.getenv('OPEN_WEATHER'))
        error, info = ow.get_by_city_name(city)

        return error, info

    elif yahooweather_enable:
        raise NotImplementedError('This provider is not implemented')

    return True, {'error': True, 'message': 'An error occurred.'}
