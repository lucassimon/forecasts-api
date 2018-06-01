# -*- coding: utf-8 -*-
# Python
from datetime import timedelta
from os import getenv
from os.path import dirname, isfile, join

# Third
from dotenv import load_dotenv

_ENV_FILE = join(dirname(__file__), './.env')


if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

APP_PORT = int(getenv('APP_PORT'))
DEBUG = eval(getenv('DEBUG').title())
SENTRY_DSN = getenv('SENTRY_DSN')
SECRET_KEY = getenv('SECRET_KEY')
MONGODB_HOST = getenv('MONGODB_URI')
MONGODB_HOST_TEST = getenv('MONGODB_URI_TEST')
AMQP_HOST = getenv('AMQP_URI')
OPEN_WEATHER = getenv('OPEN_WEATHER')
CELERY_TIMEZONE = getenv('CELERY_TIMEZONE')
BROKER_URL = getenv('BROKER_URL')
CELERY_RESULT_BACKEND = getenv('CELERY_RESULT_BACKEND')
CELERY_SEND_TASK_SENT_EVENT = getenv('CELERY_SEND_TASK_SENT_EVENT')
