# -*- coding:utf-8 -*-

# Python
from datetime import datetime, timedelta

# Flask
from flask import request


# Third
from flask_restful import Resource
# from bcrypt import hashpw, gensalt
from mongoengine.errors import NotUniqueError, ValidationError


# Apps
from apps.messages import _MSG200, _MSG201, _MSG202, _MSG203
from apps.messages import _MSG300, _MSG302, _MSG312

from apps.responses import resp_already_exists, resp_exception
from apps.responses import resp_form_invalid, resp_ok, resp_does_not_exist

# Local
from .models import User
from .schemas import UserCreateSchema, UserSchema, UpdateUserSchema
from .validate import exists_email_in_database
from .utils import get_user
from .tasks import import_users, export_users


class UsersList(Resource):
    def post(self, *args, **kwargs):
        '''
        Create an user

        payload:
        {
            "name": "Lucas Simon",
            "email": "lucassrod@gmail.com",
            "password": "teste123"
        }
        '''
        req_data = request.get_json() or None
        schema = UserCreateSchema()

        if req_data is None:
            return resp_form_invalid('Users', [], msg=_MSG312)

        data, errors = schema.load(req_data)

        if errors:
            return resp_form_invalid('Users', errors)

        if exists_email_in_database(data.get('email')):
            errors = {
                'errors': {
                    'email': [_MSG302]
                }
            }

            return resp_form_invalid('Users', errors)

        # TODO: Encrypt password with bcrypt

        try:
            model = User(**data)
            model.save()

        except NotUniqueError:
            return resp_already_exists('Users', 'usuário')

        except ValidationError as e:
            return resp_exception('Users', msg=_MSG300, description=e)

        except Exception as e:
            return resp_exception('Users', description=e)

        schema = UserSchema()
        result = schema.dump(model)

        return resp_ok(
            'Users', _MSG200.format('Usuário'), data=result.data
        )


class UserResource(Resource):
    def get(self, user_id):
        user = get_user('Users', object_id=user_id)

        if not isinstance(user, User):
            return user

        schema = UserSchema()
        result = schema.dump(user)

        return resp_ok(
            'Users', _MSG201.format('Usuário'), data=result.data
        )

    def put(self, user_id):
        req_data = request.get_json() or None

        if req_data is None:
            return resp_form_invalid('Users', [], msg=_MSG312)

        schema = UpdateUserSchema()
        user = get_user('Users', object_id=user_id)

        if not isinstance(user, User):
            return user

        data, errors = schema.load(req_data)

        if errors:
            return resp_form_invalid('Users', errors)

        try:
            for i in data.keys():
                user[i] = data[i]

            user.save()

        except NotUniqueError as e:
            return resp_already_exists('Users', 'usuário')

        except ValidationError as e:
            return resp_exception('Users', msg=_MSG300, description=e)

        except Exception as e:
            return resp_exception('Users', description=e)

        schema = UserSchema()
        result = schema.dump(user)

        return resp_ok(
            'Users', _MSG202.format('Usuário'), data=result.data
        )

    def delete(self, user_id):
        user = get_user('Users', object_id=user_id)

        if not isinstance(user, User):
            return user

        user.active = False

        try:
            user.save()
        except NotUniqueError as e:
            return resp_already_exists('Users', 'usuário')

        except ValidationError as e:
            return resp_exception(
                'Users', msg=_MSG300, description=e
            )

        except Exception as e:
            return resp_exception('Users', description=e)

        return resp_ok('Users', _MSG203.format('Usuário'))


class UserImport(Resource):
    def get(self, *args, **kwargs):
        from apps.api import api
        eta = datetime.utcnow() + timedelta(seconds=10)
        task = import_users.apply_async(eta=eta)
        # task = export_users.apply()
        data = {
            'task': task.id,
            'links': api.url_for(
                UserImportStatus, task_id=task.id, _external=True
            )
        }

        return resp_ok(
            'Users', _MSG201.format('Usuário'), data=data
        )


class UserImportStatus(Resource):
    def get(self, *args, **kwargs):
        task = import_users.AsyncResult(kwargs.get('task_id'))
        if task.state == 'PENDING':
            data = {'state': task.state, 'status': 'Pending...'}

        elif task.state == 'PROGRESS':
            data = {
                'state': task.state, 'total': task.result.get('total'),
                'current': task.result.get('current', ''),
                'status': task.result.get('status', ''),
                'imported': task.result.get('imported', ''),
            }

        elif task.state != 'FAILURE':
            data = {
                'state': task.state, 'total': task.result.get('total', 1),
                'status': task.result.get('status', ''),
                'imported': task.result.get('imported', ''),
                'errors': task.result.get('errors', ''),
            }

        else:
            data = {'state': task.state, 'status': task.result.get('status')}

        return resp_ok(
            'Users', _MSG201.format('Usuário'), data=data
        )


class UserExport(Resource):
    def get(self, *args, **kwargs):
        from apps.api import api
        eta = datetime.utcnow() + timedelta(seconds=10)
        task = export_users.apply_async(eta=eta)
        # task = export_users.apply()
        data = {
            'task': task.id,
            'links': api.url_for(
                DownloadExport, task_id=task.id, _external=True
            )
        }

        return resp_ok(
            'Users', _MSG201.format('Usuário'), data=data
        )


class DownloadExport(Resource):
    def get(self, *args, **kwargs):
        task_id = kwargs.get("task_id")
        result = export_users.AsyncResult(task_id)
        if result.ready():
            filename = '{}.csv'.format(task_id)
            data = {
                'filename': filename,
                'message': 'Verifique a pasta /tmp',
                'links': "CDN url or static url from flask"
            }
            return resp_ok(
                'Users', _MSG201.format('Usuário'), data=data
            )
        else:
            return resp_does_not_exist(
                'Users', 'The file is not ready. Try again in a few minutes.'
            )
