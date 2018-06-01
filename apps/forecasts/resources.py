# -*- coding:utf-8 -*-

# Python

# Flask
from flask import request


# Third
from flask_restful import Resource
from mongoengine.errors import NotUniqueError, ValidationError


# Apps
from apps.messages import _MSG200
from apps.messages import _MSG300, _MSG312

from apps.responses import resp_already_exists, resp_exception
from apps.responses import resp_form_invalid, resp_ok

from apps.users.models import User
from apps.users.utils import get_user

# Local
from .models import Forecast
from .schemas import ForecastSettingsSchema


class ForecatsSettings(Resource):
    def post(self, user_id, *args, **kwargs):
        '''
        Create settings forecast notification

        payload:

        {
            "address": "Londres, UK",
            "period": {
                "start": "08:00",
                "end": "19:00"
            },
            "days": {
                "sunday": true,
                "monday": true,
                "tuesday": true,
                "wednesday": true,
                "thursday": true,
                "friday": true,
                "saturday": true
            },
            "notification": "07:00"
        }
        '''
        user = get_user('Forecasts Settings', object_id=user_id)

        if not isinstance(user, User):
            return user

        req_data = request.get_json() or None
        schema = ForecastSettingsSchema()

        if req_data is None:
            return resp_form_invalid('Forecasts Settings', [], msg=_MSG312)

        req_data['user_id'] = '{}'.format(user_id)

        data, errors = schema.load(req_data)

        if errors:
            return resp_form_invalid('Forecasts Settings', errors)

        try:
            model = Forecast(**data)
            model.save()

        except NotUniqueError:
            return resp_already_exists('Forecasts Settings', 'usuário')

        except ValidationError as e:
            return resp_exception(
                'Forecasts Settings', msg=_MSG300, description=e
            )

        except Exception as e:
            return resp_exception('Forecasts Settings', description=e)

        result = schema.dump(model)

        return resp_ok(
            'Forecasts Settings',
            _MSG200.format('Configurações do clima'),
            data=result.data
        )
