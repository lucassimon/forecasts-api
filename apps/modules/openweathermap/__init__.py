# -*- coding: utf-8 -*-

# Python


# Third
import requests
from requests.exceptions import HTTPError, ConnectionError, ProxyError
from requests.exceptions import SSLError, Timeout, ConnectTimeout, ReadTimeout
from requests.exceptions import TooManyRedirects, ContentDecodingError


class OpenWeather():

    def __init__(self, app_id):
        self.API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
        self._app_id = app_id
        self.params = {'appid': self.app_id, 'cnt': 3}

    @property
    def app_id(self):
        return self._app_id

    @app_id.setter
    def app_id(self, val):
        self._app_id = val

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, val):
        self._params = val

    def request(self, url, **kwargs):
        info = {}
        error = False
        self.params.update(kwargs)

        try:
            res = requests.get(url, params=self.params)

        except ConnectionError as e:
            error = True

            info = {'error': error, 'message': e.message}

            return error, info

        except (
            HTTPError, ProxyError, SSLError, Timeout,
            ConnectTimeout, ReadTimeout, TooManyRedirects, ContentDecodingError
        ) as e:
            error = True

            info = {'error': error, 'message': e.message}

            return error, info

        except Exception as e:
            error = True

            info = {'error': error, 'message': e.message}

            return error, info

        if res.status_code == requests.codes.ok:
            data = self.translate_fields(res.json())

            info = {'error': error, 'message': 'Success.', 'data': data}
            return error, info

        else:
            error = True
            info = {'error': error, 'message': res.json().get('message')}

            return error, info

        error = True

        info = {'error': error, 'message': 'An error occurred.'}

        return error, info

    def translate_fields(self, info):
        data = []
        for i in info.get('list'):
            dt_txt = i.get('dt_txt').split(" ")
            data.append({
                "date": dt_txt[0], "hour": dt_txt[1],
                "rain": i.get('rain', None),
                "dt_txt": i.get('dt_txt'),
                "humidity": i.get('main').get('humidity', None),
                "temp": i.get('main').get('temp', None),
                "weather": [
                    {
                        'main': weather.get('main'),
                        'description': weather.get('description')
                    } for weather in i.get('weather')
                ]
            })

        return {
            'name': info.get('city').get('name'),
            'country': info.get('city').get('country'),
            'weather': data,
        }

    def get_by_city_name(self, city):
        params = {'q': city}
        return self.request(self.API_URL, **params)
