# -*- coding:utf-8 -*-


from marshmallow import Schema
from marshmallow.fields import Str, Nested, Boolean, Time

from apps.messages import _MSG309


class PeriodSchema(Schema):
    start = Str(required=True, error_messages={'required': _MSG309})
    end = Str(required=True, error_messages={'required': _MSG309})


class DaySchema(Schema):
    sunday = Boolean(required=True, error_messages={'required': _MSG309})
    monday = Boolean(required=True, error_messages={'required': _MSG309})
    tuesday = Boolean(required=True, error_messages={'required': _MSG309})
    wednesday = Boolean(required=True, error_messages={'required': _MSG309})
    thursday = Boolean(required=True, error_messages={'required': _MSG309})
    friday = Boolean(required=True, error_messages={'required': _MSG309})
    saturday = Boolean(required=True, error_messages={'required': _MSG309})


class ForecastSettingsSchema(Schema):
    id = Str()
    user_id = Str(required=True, error_messages={'required': _MSG309})
    address = Str(required=True, error_messages={'required': _MSG309})
    period = Nested(PeriodSchema, required=True)
    days = Nested(DaySchema, required=True)
    notification = Str(required=True, error_messages={'required': _MSG309})
