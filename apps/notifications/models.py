# -*- coding: utf-8 -*-

# Python
from datetime import datetime

# Third

from mongoengine import (
    BooleanField, ObjectIdField, StringField, DateTimeField
)

# Apps
from apps.db import db


class Notification(db.Document):
    '''
    Forecast settings
    '''
    meta = {
        'collection': 'notifications',
        'indexes': [{
            'fields': ['$user_id'],
        }]
    }
    user_id = ObjectIdField()
    message = StringField(required=True)
    dt_txt = StringField(required=True)
    sent = BooleanField(default=False)
    read = BooleanField(default=False)
    created = DateTimeField(default=datetime.now)
