import logging

from django.conf import settings

from pubsub import PubSubEvent, PubSubEventType, RedisProducer

logger = logging.getLogger(__name__)


def publish_event(event_type: PubSubEventType, payload: dict) -> None:
    """
    Publishes an event to the pubsub channel

    :param event_type: PubSubEventType
    :param payload: A dictionary containing the payload for the event
    """
    try:
        producer = RedisProducer(
            channel=settings.PUBSUB_CHANNEL,
            host=settings.PUBSUB_HOST,
            port=settings.PUBSUB_PORT,
            db=settings.PUBSUB_DEFAULT_DB,
        )
        event = PubSubEvent(type=event_type, payload=payload)
        producer.produce(event=event)
        logger.info(
            f"Published event for alert: "
            f'[alert_id - {event.payload.get("id", "N/A")}]:[{event.type}]'
        )
    except Exception as e:
        logger.error(f"Error publishing event: {e}")
