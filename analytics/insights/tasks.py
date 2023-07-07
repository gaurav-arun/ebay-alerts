from __future__ import annotations

import logging

from celery import shared_task
# from .utils import mails
# from ebay_sdk import client, utils as ebay_utils
from pubsub import RedisConsumer, Event

from .models import Alert

logger = logging.getLogger(__name__)

consumer = RedisConsumer('alerts_stream', host="host.docker.internal", port=6381, db=0)


@shared_task
def consume_events():
    for event in consumer.consume():
        logger.info(f'Received event: {event.type}: {event.payload}')
