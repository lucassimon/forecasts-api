# -*- coding: utf-8 -*-
# Python
import os
from datetime import datetime

# Flask
from flask import current_app

# Third
from celery.signals import task_postrun
from celery.utils.log import get_task_logger
from celery.contrib import rdb

# Apps
from apps.celery import celery
from apps.modules.openweathermap import OpenWeather
from apps.modules.gw import weather as weather_gateway
from apps.notifications.models import Notification

# Local
from .utils import check_period_is_valid, get_settings_by_weekday

logger = get_task_logger(__name__)


@celery.task
def log(message):
    """Print some log messages"""
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)


@celery.task
def forecast_settings():
    """fetch all settings in DB"""

    today = datetime.now()

    settings = get_settings_by_weekday(today.weekday())

    for setting in settings:
        if not check_period_is_valid(
            setting.period.start, today.time(), setting.period.end
        ):
            continue

        # ow = OpenWeather(os.getenv('OPEN_WEATHER'))
        # error, data = ow.get_by_city_name(setting.address)

        error, data = weather_gateway(setting.address)

        if error:
            continue

        infos = data.get('data').get('weather')

        print(infos)
        for info in infos:
            for weather in info.get('weather'):
                if 'rain' in weather.get('main').lower():

                    # TODO: Flag on notification not to send repeated alerts
                    # if it sended. See Notification model

                    # TODO: Send Notification to RabbitMQ or
                    # another messaging queue or third service
                    message = 'Remember to grab the umbrella'
                    data = {
                        'user_id': '{}'.format(setting.user_id),
                        'message': message,
                    }

                    # TODO: When sucesseful push the message
                    # save the notification data in model Notifications
                    # or the consumer can create the register in database


