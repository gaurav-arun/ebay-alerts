from django.core.management.base import BaseCommand
from pubsub import RedisConsumer, PubSubEvent
from django.conf import settings
import logging
from insights import tasks as insight_tasks
from insights.models import PubSubEventStore


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Starts the event consumer process'

    @staticmethod
    def process(event: PubSubEvent):
        """
        Initiates the processing of the consumed event by
        persisting in the DB first the invoking the celery task
        :param event: PubSubEvent
        :return:None
        """
        stored_event = PubSubEventStore.objects.create(
            type=event.type,
            payload=event.payload,
            timestamp=event.timestamp,
            processed=False
        )

        # Invoke celery task that processes the event
        insight_tasks.process_event.delay(id=stored_event.id)

    def handle(self, *args, **options):
        """
        Starts the event consumer process and listens for events on the pubsub channel
        """
        logger.info('Starting event consumer process...')
        consumer = RedisConsumer(
            channel=settings.PUBSUB_CHANNEL,
            host=settings.PUBSUB_HOST,
            port=settings.PUBSUB_PORT,
            db=settings.PUBSUB_DEFAULT_DB
        )

        for pubsub_event in consumer.consume():
            # Generic exception handling to avoid crashing the consumer!
            try:
                logger.info(f'Received PubSubEvent : [{pubsub_event}]')
                self.process(pubsub_event)
            except Exception as error:
                logger.error(f'Error processing PubSubEvent: {error} : {pubsub_event}')
