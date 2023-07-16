import os  # isort:skip
import logging  # isort:skip

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analytics.settings.base")  # isort:skip

import celery  # noqa: E402
from celery.schedules import crontab  # noqa: E402
from django.conf import settings  # noqa: E402

logger = logging.getLogger(__name__)

app = celery.Celery("analytics")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "product_insights": {
        "task": "insights.tasks.send_product_insights",
        "schedule": crontab(
            minute=f"*/{settings.PRODUCT_INSIGHTS_FREQUENCY_IN_MINUTES}"
        ),
        "kwargs": {"lookback_days": 14},
    },
}
