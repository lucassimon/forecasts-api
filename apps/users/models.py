# -*- coding: utf-8 -*-
from datetime import datetime


from mongoengine import EmbeddedDocumentListField
from mongoengine import StringField, EmailField, BooleanField, DateTimeField

# Apps
from apps.db import db
from apps.forecasts.models import Forecast


class UserMixin(db.Document):
    """
    Default implementation for User fields
    """
    meta = {
        'abstract': True,
        'ordering': ['email']
    }

    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    active = BooleanField(default=True)
    created = DateTimeField(default=datetime.now)

    def is_active(self):
        return self.active


class User(UserMixin):
    '''
    Users
    '''
    meta = {'collection': 'users'}
    name = StringField(required=True)
