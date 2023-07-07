from pubsub import RedisProducer, Event
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def publish_event(type: str, payload: dict) -> None:
    """Publishes an event to the pubsub channel"

    :param type: str ['alert.created', 'alert.updated', 'alert.deleted', 'alert.new_products']
    :param payload: dict
    """
    try:
        producer = RedisProducer(
            channel=settings.PUBSUB_CHANNEL,
            host=settings.PUBSUB_HOST,
            port=settings.PUBSUB_PORT,
            db=settings.PUBSUB_DEFAULT_DB
        )
        event = Event(type=type, payload=payload)
        producer.produce(event=event)
        logger.info(f'Published event for alert: [{event.type}]: [{event.payload["id"]}]')
    except Exception as e:
        logger.error(f'Error publishing event: {e}')
