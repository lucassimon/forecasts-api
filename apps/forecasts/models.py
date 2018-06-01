# -*- coding: utf-8 -*-

# Python

# Third

from mongoengine import (
    BooleanField, EmbeddedDocument, EmbeddedDocumentField,
    ObjectIdField, StringField
)

# Apps
from apps.db import db


class Period(EmbeddedDocument):
    start = StringField(required=True)
    end = StringField(required=True)


class Day(EmbeddedDocument):
    sunday = BooleanField(default=False)
    monday = BooleanField(default=False)
    tuesday = BooleanField(default=False)
    wednesday = BooleanField(default=False)
    thursday = BooleanField(default=False)
    friday = BooleanField(default=False)
    saturday = BooleanField(default=False)


class Forecast(db.Document):
    '''
    Forecast settings
    '''
    meta = {
        'collection': 'forecasts',
        'indexes': [{
            'fields': ['$user_id'],
        }]
    }
    user_id = ObjectIdField()
    address = StringField(required=True)
    period = EmbeddedDocumentField(Period, default=Period)
    days = EmbeddedDocumentField(Day, default=Day)
    notification = StringField(required=True)
