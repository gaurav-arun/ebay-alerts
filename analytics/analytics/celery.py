import os  # isort:skip
import logging  # isort:skip

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analytics.settings.base")  # isort:skip

import celery  # noqa: E402
from celery.schedules import crontab  # noqa: E402

logger = logging.getLogger(__name__)

app = celery.Celery("analytics")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "product_insights": {
        "task": "insights.tasks.send_product_insights",
        # TODO: Change the crontab frequency to `day` after testing
        "schedule": crontab(minute="*/30"),
        "kwargs": {"lookback_days": 14},
    },
}
