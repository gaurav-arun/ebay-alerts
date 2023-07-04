from __future__ import annotations

import logging
import time

import pandas as pd
from celery import shared_task

from .models import Alert

logger = logging.getLogger(__name__)


@shared_task()
def send_alert():
    logger.info("Sending alerts")
    for alert in Alert.objects.all():
        logger.info(f"Sending alert to {alert.email}")
