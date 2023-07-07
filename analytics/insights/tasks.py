from __future__ import annotations

import logging

from celery import shared_task
from .models import Alert, AlertEvent, Product
from django.db import transaction
# from pubsub import RedisConsumer, Event
# from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
@transaction.atomic
def process_event(alert_event_id: int):
    alert_event = AlertEvent.objects.get(id=alert_event_id)
    logger.info(f'Processing event: [{alert_event.id}]')

    # Create Alert object from event payload
    alert, _ = Alert.objects.get_or_create(
        uid=alert_event.payload['id'],
        defaults={
            'email': alert_event.payload['email'],
            'keywords': alert_event.payload['keywords'],
            'frequency': alert_event.payload['frequency'],
        }
    )

    # Create Product objects from event payload
    products = []
    for item in alert_event.payload['items']['itemSummaries']:
        product = Product.objects.create(
            item_id=item['itemId'],
            title=item['title'],
            image_url=item['image']['imageUrl'],
            price=item['price']['value'],
            currency=item['price']['currency'],
            web_url=item['itemWebUrl'],
            timestamp=alert_event.timestamp
        )
        products.append(product)

    # Update Alert object to track latest Products
    alert.products.set(products)

    # Update AlertEvent object
    alert_event.processed = True
    alert_event.save(update_fields=['processed', 'updated_at'])

    logger.info(f'Processing complete for event: [{alert_event.id}]')
