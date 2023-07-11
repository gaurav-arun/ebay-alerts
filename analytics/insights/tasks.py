from __future__ import annotations

import logging

from celery import shared_task
from .models import Alert, PubSubEventStore, ProductPriceLog
from django.db import transaction
from .insights import generate_insights
from .utils import mails
from pubsub import PubSubEventType

logger = logging.getLogger(__name__)


def _process_new_products_event_type(event: PubSubEventStore) -> None:
    """
    Process events of type `PubSubEventType.NEW_PRODUCTS`

    The idea is to track the alert configuration as well as the products
    that were returned by the API call. We keep track of the most recent
    products for each alert configuration.

    :param event: PubSubEvent
    """
    alert, _ = Alert.objects.get_or_create(
        uid=event.payload['id'],
        defaults={
            'email': event.payload['email'],
            'keywords': event.payload['keywords'],
            'frequency': event.payload['frequency'],
        }
    )

    # Create Product objects from event payload
    products = []
    for item in event.payload['items']['itemSummaries']:
        product = ProductPriceLog.objects.create(
            item_id=item['itemId'],
            title=item['title'],
            image_url=item['image']['imageUrl'],
            price=item['price']['value'],
            currency=item['price']['currency'],
            web_url=item['itemWebUrl'],
            timestamp=event.timestamp
        )
        products.append(product)

    # Update Alert object to track latest Products
    alert.products.set(products)


def _process_alert_created_event_type(event: PubSubEventStore) -> None:
    """
    Process stored PubSubEvent of type PubSubEventType.ALERT_CREATED

    In this case we just create a new Alert object.
    """
    alert, _ = Alert.objects.get_or_create(
        uid=event.payload['id'],
        defaults={
            'email': event.payload['email'],
            'keywords': event.payload['keywords'],
            'frequency': event.payload['frequency'],
        }
    )


def _process_alert_updated_event_type(event: PubSubEventStore):
    """
    Process persisted events of type `alert.updated`

    In this case we update the Alert object with the data from the
    event payload.
    """
    alert = Alert.objects.get(
        uid=event.payload['id']
    )
    alert.email = event.payload['email']
    alert.frequency = event.payload['frequency']
    alert.keywords = event.payload['keywords']
    alert.save()


def _process_alert_deleted_event_type(event: PubSubEventStore):
    """Process persisted events of type `alert.deleted`

    In this case we delete the Alert object and the related many-to-many mapping
    with the Product objects. However, Product objects are not deleted. This is
    because we want to keep track of the product prices over time.
    """
    Alert.objects.get(uid=event.payload['id']).delete()


@shared_task
@transaction.atomic
def process_event(id: int):
    """
    Process an event from the PubSubEventStore.
    Entire processing happens within an atomic transaction.

    :param id: ID of the PubSubEventStore object
    """
    event = PubSubEventStore.objects.get(id=id)

    logger.info(f'Processing an event from PubSubEventStore: {event}')
    if event.type == PubSubEventType.NEW_PRODUCTS:
        _process_new_products_event_type(event)
    elif event.type == PubSubEventType.ALERT_CREATED:
        _process_alert_created_event_type(event)
    elif event.type == PubSubEventType.ALERT_UPDATED:
        _process_alert_updated_event_type(event)
    elif event.type == PubSubEventType.ALERT_DELETED:
        _process_alert_deleted_event_type(event)
    else:
        raise ValueError(f'Unknown PubSubEvent: {event}')

    # Update AlertEvent object
    event.processed = True
    event.save(update_fields=['processed', 'updated_at'])

    logger.info(f'Processing complete for an event'
                f' from from PubSubEventStore: {event}')


@shared_task
def send_product_insights():
    """
    Send product insights to the users with active alerts
    """
    insights: list[dict] = generate_insights()
    for insight in insights:
        mails.send_html_mail(
            to=insight['email'],
            subject=f'New Product Insights',
            context=insight,
            template_name='mails/insight.html',
        )
        logger.info(f"Sent product insights to {insight['email']}")
