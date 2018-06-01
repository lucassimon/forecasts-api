from celery import Celery
from celery.schedules import crontab
from celery.contrib import rdb

from apps import create_app
from apps.forecasts.tasks import forecast_settings


def create_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.config_from_object(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


flask_app = create_app()

celery = create_celery(flask_app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls forecast_settings every 30 minutes.
    sender.add_periodic_task(
        1800.0, forecast_settings,
        name='search all forecast_settings'
    )

    # Executes every morning at 3:30 a.m.
    # Clear old notifications that are saved?
    #
    # sender.add_periodic_task(
    #     crontab(hour=3, minute=30),
    #     clear_old_notifications,
    # )
