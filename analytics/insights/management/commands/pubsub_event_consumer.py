import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from insights import tasks as insight_tasks
from insights.models import ConsumedPubSubEvent

from pubsub import PubSubEvent, RedisConsumer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Starts the event consumer process"

    @staticmethod
    def process(pubsub_event: PubSubEvent):
        """
        Initiates the processing of the consumed event by first
        persisting it in the DB, and then invoking the celery task
        that processes the event.

        :param pubsub_event: PubSubEvent
        :return:None
        """
        consumed_event = ConsumedPubSubEvent.objects.create(
            type=pubsub_event.type.value,
            payload=pubsub_event.payload,
            timestamp=pubsub_event.timestamp,
            processed=False,
        )

        # Invoke celery task that processes the event
        insight_tasks.process.delay(id=consumed_event.id)

    def handle(self, *args, **options):
        """
        Starts the event consumer process and listens for events on the pubsub channel
        """
        logger.info("Starting event consumer process...")
        consumer = RedisConsumer(
            channel=settings.PUBSUB_CHANNEL,
            host=settings.PUBSUB_HOST,
            port=settings.PUBSUB_PORT,
            db=settings.PUBSUB_DEFAULT_DB,
        )

        for pubsub_event in consumer.consume():
            # Generic exception handling to avoid crashing the consumer!
            try:
                logger.info(
                    f"PubSubEvent received by Analytics consumer: [{pubsub_event.type}]"
                )
                self.process(pubsub_event)
            except Exception as error:
                logger.error(f"Error processing PubSubEvent: {error} : {pubsub_event}")
