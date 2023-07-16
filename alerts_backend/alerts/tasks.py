import logging

from celery import shared_task
from django.conf import settings
from ebay_sdk import client
from ebay_sdk import models as ebay_models
from ebay_sdk import utils as ebay_utils

from pubsub import PubSubEventType

from .models import Alert
from .utils import mails
from .utils import pubsub as pubsub_utils

logger = logging.getLogger(__name__)


@shared_task(queue=settings.CELERY_DEFAULT_QUEUE)
def send_alert(frequency: int) -> None:
    """
    This task will be executed periodically by celery beat.
    It will fetch the alerts for the given frequency and send
    emails to the users.

    :param frequency: It is used to filter the Alerts based on the frequency
    """
    alerts = Alert.objects.filter(frequency=frequency)
    logger.info(f"Found {len(alerts)} alerts for frequency {frequency}")

    for alert in alerts:
        keywords: str = alert.keywords
        response: dict = client.BuyApi.find_items_by_keyword(keyword=keywords)

        # Publish the details of newly fetched products
        payload = {
            "id": alert.id,
            "email": alert.email,
            "keywords": alert.keywords,
            "frequency": alert.frequency,
            "items": response,
        }
        pubsub_utils.publish_event(
            event_type=PubSubEventType.NEW_PRODUCTS, payload=payload
        )

        # Send email to the user
        items: list[ebay_models.ItemSummary] = ebay_utils.parse_response(response)
        mails.send_html_mail(
            to=alert.email,
            subject=f"Alert for {keywords}",
            context={"items": items, "keywords": keywords},
            template_name="mails/alert.html",
        )
        logger.info(f"Sent email for alert - {alert}")
