# -*- coding:utf-8 -*-


from marshmallow import Schema
from marshmallow.fields import Str

from apps.messages import _MSG309


class UserCreateSchema(Schema):
    email = Str(required=True, error_messages={'required': _MSG309})
    password = Str(required=True, error_messages={'required': _MSG309})
    name = Str(required=True, error_messages={'required': _MSG309})


class UserSchema(Schema):
    id = Str()
    email = Str(required=True, error_messages={'required': _MSG309})
    name = Str(required=True, error_messages={'required': _MSG309})


class UpdateUserSchema(Schema):
    email = Str()
    name = Str()
