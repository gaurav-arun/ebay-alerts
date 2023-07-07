from django.core.management.base import BaseCommand
from pubsub import RedisConsumer, Event
from django.conf import settings
import logging
from insights.tasks import process_event
from insights.models import PersistedEvent


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Starts the event consumer process'

    def persist(self, event: Event) -> PersistedEvent:
        """Persists the event in the database
        :param event:
        :return:
        """
        return PersistedEvent.objects.create(
            type=event.type,
            payload=event.payload,
            timestamp=event.timestamp,
            processed=False
        )

    def handle(self, *args, **options):
        """Starts the event consumer process and listens for events on the pubsub channel
        """
        logger.info('Starting event consumer process...')

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
                persisted_event = self.persist(event)
                process_event.delay(persisted_event.id)
            except Exception as error:
                logger.error(f'Error processing event: {error} : {event}')
