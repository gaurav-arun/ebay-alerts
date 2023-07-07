import os  # isort:skip
import logging  # isort:skip
from django.conf import settings  # isort:skip

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analytics.settings_docker")  # isort:skip

import celery
from celery.schedules import crontab

logger = logging.getLogger(__name__)

app = celery.Celery("analytics")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    # "insights": {
    #     "task": "alerts.tasks.send_alert",
    #     "schedule": crontab(hour="*/12"),
    # },
    # "alert_every_10_minutes": {
    #     "task": "alerts.tasks.send_alert",
    #     "schedule": crontab(minute="*/10"),
    #     "kwargs": {"frequency": 10},
    # },
    # "alert_every_30_minutes": {
    #     "task": "alerts.tasks.send_alert",
    #     "schedule": crontab(minute="*/10"),
    #     "kwargs": {"frequency": 30},
    # }
}
