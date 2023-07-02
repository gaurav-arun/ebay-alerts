"""
Celery configuration

Gist with best practices -
https://gist.github.com/IrSent/5e4820f6b187d3654967b55e27d5d204
"""

# pylint: disable=wrong-import-position

import os  # isort:skip
import logging  # isort:skip

import celery
from celery.schedules import crontab

# pylint: enable=wrong-import-position
logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ebay_alerts.settings")  # isort:skip

app = celery.Celery("ebay_alerts")

# Using a string here means the worker does not have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
# Include `airbase_backend` module so that we can add tasks
# there that don't belong to any specific application.
# settings.INSTALLED_APPS.append("airbase_backend")
app.autodiscover_tasks()

# NOTE: TIME_ZONE is set to UTC. Pick times outside of working hours in the US
# (6 am PT to 6 pm PT), if possible.
# Only configure stateless scheduled tasks that are not impacted by arbitrary
# restarts of the Celery beat daemon
app.conf.beat_schedule = {
    # Customer app scheduled tasks
    "test_beat_schedule": {
        "task": "absa.tasks.sleepy",
        "schedule": crontab(),
    }
}
