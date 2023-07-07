from __future__ import annotations

import logging

from celery import shared_task
from .models import Alert, PersistedEvent, Product
from django.db import transaction
from .insights import generate_insights
from .utils import mails

logger = logging.getLogger(__name__)


def _process_new_products_event_type(event: PersistedEvent) -> None:
    """Process persisted events of type `alert.new_products`

    The idea is to track the alert configuration as well as the products
    that were returned by the API call. We keep track of the most recent
    products for each alert.

    :param event: PersistedEvent
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
        product = Product.objects.create(
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


def _process_alert_created_event_type(event: PersistedEvent) -> None:
    """Process persisted events of type `alert.created`

    In this case we just create a new Alert object with the data from the
    event payload.
    """
    alert, _ = Alert.objects.get_or_create(
        uid=event.payload['id'],
        defaults={
            'email': event.payload['email'],
            'keywords': event.payload['keywords'],
            'frequency': event.payload['frequency'],
        }
    )


def _process_alert_updated_event_type(event:PersistedEvent):
    """Process persisted events of type `alert.updated`

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


def _process_alert_deleted_event_type(event: PersistedEvent):
    """Process persisted events of type `alert.deleted`

    In this case we delete the Alert object and the related many-to-many mapping
    with the Product objects. However, Product objects are not deleted. This is
    because we want to keep track of the product prices over time.
    """
    Alert.objects.get(uid=event.payload['id']).delete()


@shared_task
@transaction.atomic
def process_event(persisted_event_id: int):
    """Process a persisted event

    :param persisted_event_id: int
    :return:
    """
    event: PersistedEvent = PersistedEvent.objects.get(id=persisted_event_id)
    logger.info(f'Processing event {event}')

    if event.type == 'alert.new_products':
        _process_new_products_event_type(event)
    elif event.type == 'alert.created':
        _process_alert_created_event_type(event)
    elif event.type == 'alert.updated':
        _process_alert_updated_event_type(event)
    elif event.type == 'alert.deleted':
        _process_alert_deleted_event_type(event)
    else:
        raise ValueError(f'Unknown event type {event}')

    # Update AlertEvent object
    event.processed = True
    event.save(update_fields=['processed', 'updated_at'])

    logger.info(f'Processing complete for event {event}')


@shared_task
def send_product_insights():
    """Send product insights to the users
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
