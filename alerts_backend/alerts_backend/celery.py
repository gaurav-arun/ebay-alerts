import os  # isort:skip
import logging  # isort:skip
from django.conf import settings  # isort:skip

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alerts_backend.settings_docker")  # isort:skip

import celery
from celery.schedules import crontab

app = celery.Celery("alerts_backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "alert_every_2_minutes": {
        "task": "alerts.tasks.send_alert",
        "schedule": crontab(minute="*/1"),
        "args": (2,)
    },
    "alert_every_10_minutes": {
        "task": "alerts.tasks.send_alert",
        "schedule": crontab(minute="*/10"),
        "kwargs": {"frequency": 10},
    },
    "alert_every_30_minutes": {
        "task": "alerts.tasks.send_alert",
        "schedule": crontab(minute="*/10"),
        "kwargs": {"frequency": 30},
    }
}
