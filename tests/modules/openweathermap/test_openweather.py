# -*- coding: utf-8 -*-

# Python


# Third

# apps
from apps.modules.openweathermap import OpenWeather


class TestOpenWeather:
    def setup_method(self):
        self.city = 'Calgary, CA'

    def test_ow(self, test_client):

        ow = OpenWeather(test_client.application.config['OPEN_WEATHER'])
        error, info = ow.get_by_city_name(self.city)

        assert error is False
        assert info.get('message') == 'Success.'
