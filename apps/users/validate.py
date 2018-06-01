# -*- coding: utf-8 -*-

# Third

from mongoengine.errors import DoesNotExist


# Apps
from .models import User


def exists_email_in_database(address, object_id=None):
    try:
        user = User.objects.only('id').get(email=address)

    except DoesNotExist:
        return False

    if object_id and object_id == user.id:
        return False

    return True
