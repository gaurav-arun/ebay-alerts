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
    "product_insights": {
        "task": "insights.tasks.send_product_insights",
        # TODO: Change to day after testing
        "schedule": crontab(hours="*/3"),
    },
}