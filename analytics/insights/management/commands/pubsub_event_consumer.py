from django.core.management.base import BaseCommand
from pubsub import RedisConsumer
from django.conf import settings
import logging
from insights.tasks import process_event
from insights.models import AlertEvent

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Starts the event consumer process'

    def save_event(self, event) -> AlertEvent:
        return AlertEvent.objects.create(
            type=event.type,
            payload=event.payload,
            timestamp=event.timestamp,
            processed=False
        )

    def handle(self, *args, **options):
        logger.info('Starting event consumer')
        consumer = RedisConsumer(
            channel=settings.PUBSUB_CHANNEL,
            host=settings.PUBSUB_HOST,
            port=settings.PUBSUB_PORT,
            db=settings.PUBSUB_DEFAULT_DB
        )

        for event in consumer.consume():
            # Generic exception handling to avoid crashing the consumer
            try:
                logger.info(f'Received event: [{event.payload["id"]}]')

                saved_event = self.save_event(event)
                process_event.delay(saved_event.id)
            except Exception as error:
                logger.error(f'Error processing event: {error} : {event}')
