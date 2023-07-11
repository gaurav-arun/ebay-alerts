import os  # isort:skip
import logging  # isort:skip

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "alerts_backend.settings_docker"
)  # isort:skip

import celery  # noqa: E402
from celery.schedules import crontab  # noqa: E402

logger = logging.getLogger(__name__)

app = celery.Celery("alerts_backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "alert_every_2_minutes": {
        "task": "alerts.tasks.send_alert",
        "schedule": crontab(minute="*/2"),
        "kwargs": {"frequency": 2},
    },
    "alert_every_10_minutes": {
        "task": "alerts.tasks.send_alert",
        "schedule": crontab(minute="*/10"),
        "kwargs": {"frequency": 10},
    },
    "alert_every_30_minutes": {
        "task": "alerts.tasks.send_alert",
        "schedule": crontab(minute="*/30"),
        "kwargs": {"frequency": 30},
    },
}
