import logging

from celery import shared_task
from .utils import mails
from ebay_sdk import client

from .models import Alert
from .utils import pubsub as pubsub_utils

logger = logging.getLogger(__name__)


@shared_task
def send_alert(frequency: int):
    alerts = Alert.objects.filter(frequency=frequency)
    logger.info(f"Found {len(alerts)} alerts for frequency {frequency}")

    for alert in alerts:
        keywords: str = alert.keywords
        response: dict = client.BuyApi.find_items_by_keyword(keyword=keywords)

        # items: list[ebay_models.ItemSummary] = ebay_utils.parse_response(response)
        # mails.send_html_mail(
        #     to=alert.email,
        #     subject=f'Alert for {keywords}',
        #     context={'items': items, 'keywords': keywords},
        #     template_name='mails/alert.html',
        # )
        logger.info(f"Sent email for alert - {alert}")

        # Publish the details of newly fetched products
        payload = {
            'id': alert.id,
            'email': alert.email,
            'keywords': alert.keywords,
            'frequency': alert.frequency,
            'items': response
        }
        pubsub_utils.publish_event(type='alert.new_products', payload=payload)
