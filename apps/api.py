# -*- coding: utf-8 -*-

# Third
from flask_restful import Api, Resource

# Apps
from apps.messages import _MSG900, _MSG901, _MSG902, _MSG903, _MSG904

from apps.users.resources import UsersList, UserResource
from apps.users.resources import UserImport, UserImportStatus
from apps.users.resources import UserExport, DownloadExport

from apps.forecasts.resources import ForecatsSettings

_API_ERRORS = {
    'UserAlreadyExistsError': {
        'status': 409,
        'message': _MSG901
    },
    'ResourceDoesNotExist': {
        'status': 410,
        'message': _MSG902
    },
    'MethodNotAllowed': {
        'status': 405,
        'message': _MSG903
    },
    'NotFound': {
        'status': 404,
        'message': _MSG904
    },
    'BadRequest': {
        'status': 400,
        'message': _MSG900
    },
    'InternalServerError': {
        'status': 500,
        'message': _MSG900
    }
}


# API Restful
class Index(Resource):
    def get(self):
        return {'hello': 'world by apps'}


api = Api(errors=_API_ERRORS)


def configure_api(app):

    # register the resources
    api.add_resource(Index, '/')
    api.add_resource(UsersList, '/users')
    api.add_resource(UserImport, '/users/import/data')
    api.add_resource(UserImportStatus, '/users/import/status/<string:task_id>')
    api.add_resource(UserExport, '/users/export/data')
    api.add_resource(
        DownloadExport, '/users/export/download/<string:task_id>'
    )
    api.add_resource(UserResource, '/users/<string:user_id>')
    api.add_resource(
        ForecatsSettings, '/users/<string:user_id>/forecasts'
    )
    api.init_app(app)
