# -*- coding: utf-8 -*-

# Python


# Third
from mongoengine.errors import DoesNotExist

# Apps

from apps.responses import resp_does_not_exist, resp_exception
from .models import User


def get_user(resource, identity=None, object_id=None):
    try:
        if object_id:
            return User.objects.get(id=object_id)
        else:
            return User.objects.get(email=identity)

    except DoesNotExist:
        return resp_does_not_exist(resource, 'usuário')

    except Exception as e:
        return resp_exception(resource, description=e)
