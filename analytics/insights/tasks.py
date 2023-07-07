from __future__ import annotations

import logging

from celery import shared_task

from pubsub import RedisConsumer, Event
from django.conf import settings

logger = logging.getLogger(__name__)


consumer = RedisConsumer(
    channel=settings.PUBSUB_CHANNEL,
    host=settings.PUBSUB_HOST,
    port=settings.PUBSUB_PORT,
    db=settings.PUBSUB_DEFAULT_DB
)


@shared_task
def consume_events():
    for event in consumer.consume():
        logger.info(f'Received event: {event.type}: {event.payload}')
