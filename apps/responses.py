# -*- coding: utf-8 -*-

# Flask
from flask import jsonify

# Local
from .messages import _MSG102, _MSG206, _MSG300, _MSG301, _MSG906


def resp_notallowed_user(resource, msg=_MSG102):

    if not isinstance(resource, str):
        raise ValueError('Recurso precisa ser uma string')

    resp = jsonify({
        'status': 401,
        'resource': resource,
        'message': msg
    })

    resp.status_code = 401

    return resp


def resp_form_invalid(resource, errors, msg=_MSG300):
    if not isinstance(resource, str):
        raise ValueError('Recurso precisa ser uma string')

    resp = jsonify({
        'resource': resource,
        'message': msg,
        'errors': errors,
        'status': 400,
    })

    resp.status_code = 400

    return resp


def resp_does_not_exist(resource, description):

    if not isinstance(resource, str):
        raise ValueError('Recurso precisa ser uma string')

    if not description:
        raise ValueError('A descrição não pode ser nula ou vazia')

    resp = jsonify({
        'status': 404,
        'message': _MSG206.format(description),
        'resource': resource
    })

    resp.status_code = 404

    return resp


def resp_exception(resource, msg=_MSG906, description=''):
    if not isinstance(resource, str):
        raise ValueError('Recurso precisa ser uma string')

    resp = jsonify({
        'status': 500,
        'message': msg,
        'resource': resource,
        'description': '{}'.format(description)
    })

    resp.status_code = 500

    return resp


def resp_already_exists(resource, description=''):
    if not isinstance(resource, str):
        raise ValueError('Recurso precisa ser uma string')

    resp = jsonify({
        'resource': resource,
        'message': _MSG301.format(description),
        'status': 400
    })

    resp.status_code = 400

    return resp


def resp_ok(resource, message, status=200, data=None, **extras):
    '''
    Response ok
    '''
    response = {'status': status, 'message': message, 'resource': resource}

    if data:
        response['data'] = data
    else:
        response['data'] = []

    response.update(extras)

    resp = jsonify(response)

    resp.status_code = status

    return resp
