# -*- coding: utf-8 -*-

# Python
from json import loads, dumps
# Third

# apps
from apps.messages import _MSG300, _MSG312, _MSG309


class TestUserResource:
    def setup_method(self):
        self.data = {}
        self.ENDPOINT = '/users'

    def test_response_400_when_there_are_empty_post_data(self, test_client):
        resp = test_client.post(self.ENDPOINT)
        assert resp.status_code == 400

    def test_message_312_when_there_are_empty_post_data(self, test_client):
        resp = test_client.post(self.ENDPOINT)
        data = loads(resp.data.decode('utf-8'))
        assert data['message'] == _MSG312

    def test_response_400_when_payload_is_invalid(self, test_client):
        resp = test_client.post(
            self.ENDPOINT, data=dumps(dict(foo='bar')),
            content_type='application/json'
        )

        assert resp.status_code == 400

    def test_message_300_when_form_is_invalid(self, test_client):
        resp = test_client.post(
            self.ENDPOINT, data=dumps(dict(foo='bar')),
            content_type='application/json'
        )
        data = loads(resp.data.decode('utf-8'))
        assert data['message'] == _MSG300

    def test_show_all_errors_required_when_form_is_invalid(self, test_client):
        resp = test_client.post(
            self.ENDPOINT, data=dumps(dict(foo='bar')),
            content_type='application/json'
        )
        data = loads(resp.data.decode('utf-8'))

        require_fields = [
            'name', 'email', 'password'
        ]

        for field in require_fields:
            assert field in data['errors'].keys()
            assert data['errors'][field][0] == _MSG309
