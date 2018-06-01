# -*- coding: utf-8 -*-

# Python
import csv
import time
# Flask


# Third

from celery.utils.log import get_task_logger

# Apps
from apps.celery import celery
from celery.contrib import rdb
# Local
from .models import User

logger = get_task_logger(__name__)


@celery.task(bind=True)
def import_users(self):
    filename = "import-users.csv"
    # rdb.set_trace()
    with open("{}{}".format("/tmp/", filename)) as f:
        reader = csv.reader(f, delimiter=',')
        total = sum(1 for line in reader)
        imported = 0
        errors = []
        f.seek(0)
        for index, row in enumerate(reader):
            message = 'Process the user {}'.format(row[0])
            try:
                data = {
                    'name': row[0], 'email': row[1], 'password': row[2]
                }
                User(**data).save()
                imported += 1
            except Exception as e:
                errors.append({'error': '{}'.format(e), 'line': index})
                continue

            self.update_state(
                state='PROGRESS',
                meta={
                    'current': index + 1,
                    'status': message,
                    'total': total,
                    'imported': imported
                }
            )

            time.sleep(18)

    return {
        'status': 'Task completed!', 'total': total, 'imported': imported,
        'errors': errors
    }


@celery.task(bind=True)
def export_users(self):
    filename = "{}.csv".format(self.request.id)

    # TODO: Save in CDN or static directory
    # TODO: Delete old files in another task
    with open("{}{}".format("/tmp/", filename), "w+") as f:
        writer = csv.writer(f, dialect=csv.excel)

        for i in User.objects():
            # message = 'Exportando o usuário {}'.format(i.name)
            writer.writerow([i.name, i.email])

    return filename
