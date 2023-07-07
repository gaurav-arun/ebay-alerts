import logging

from celery import shared_task
from .utils import mails
from ebay_sdk import client, utils as ebay_utils
from pubsub import RedisProducer, Event

from .models import Alert
import time
from django.conf import settings

logger = logging.getLogger(__name__)


producer = RedisProducer(
    channel=settings.PUBSUB_CHANNEL,
    host=settings.PUBSUB_HOST,
    port=settings.PUBSUB_PORT,
    db=settings.PUBSUB_DEFAULT_DB
)


def publish_event(alert, response) -> None:
    payload = {
        'id': alert.id,
        'timestamp': time.time(),
        'keywords': alert.keywords,
        'frequency': alert.frequency,
        'response': response,
    }
    producer.produce(Event(type='products', payload=payload))


@shared_task
def send_alert(frequency: int):
    alerts = Alert.objects.filter(frequency=frequency)
    logger.info(f"Found {len(alerts)} alerts for frequency {frequency}")

    for alert in alerts:
        keywords = alert.keywords
        response = client.BuyApi.find_items_by_keyword(keyword=keywords)

        logger.info('Publishing event...')
        publish_event(alert, response)

        items = ebay_utils.parse_response(response)
        mails.send_html_mail(
            to=alert.email,
            subject=f'Alert for {keywords}',
            context={'items': items, 'keywords': keywords},
            template_name='mails/alert.html',
        )
        logger.info(f"Sent email for alert - {alert}")
