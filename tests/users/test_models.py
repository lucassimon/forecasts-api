# -*- coding: utf-8 -*-

# Python

# Third

from mongoengine import BooleanField, StringField
from mongoengine import EmbeddedDocumentListField

# Apps

from apps.users.models import User


class TestUser:

    def setup_method(self):
        self.data = {
            'email': 'teste1@teste.com', 'password': 'teste123',
            'active': True,
        }
        self.model = User(**self.data)

    def test_email_field_exists(self):
        assert 'email' in self.model._fields

    def test_email_field_is_required(self):
        assert self.model._fields['email'].required is True

    def test_email_field_is_unique(self):
        assert self.model._fields['email'].unique is True

    def test_email_field_is_str(self):
        assert isinstance(self.model._fields['email'], StringField)

    def test_password_field_exists(self):
        assert 'password' in self.model._fields

    def test_password_field_is_required(self):
        assert self.model._fields['password'].required is True

    def test_password_field_is_str(self):
        assert isinstance(self.model._fields['password'], StringField)

    def test_active_field_exists(self):
        assert 'active' in self.model._fields

    def test_active_field_is_default_true(self):
        assert self.model._fields['active'].default is True

    def test_active_field_is_bool(self):
        assert isinstance(self.model._fields['active'], BooleanField)

    def test_all_fields_in_model(self):
        fields = [
            'active', 'email', 'name', 'id', 'password', 'created'
        ]

        for field in self.model._fields.keys():
            assert field in fields
