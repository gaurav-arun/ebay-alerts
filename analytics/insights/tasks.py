from __future__ import annotations

import logging

from celery import shared_task
from django.db import transaction

from pubsub import PubSubEventType

from .insights import generate_insights
from .models import ActiveAlert, ConsumedPubSubEvent, ProductPriceLog
from .utils import mails

logger = logging.getLogger(__name__)


def _process_new_products_event_type(event: ConsumedPubSubEvent) -> None:
    """
    Process events of type `PubSubEventType.NEW_PRODUCTS`

    The idea is to track new/existing alerts as well as the products associated
    with the alert.

    :param event: ConsumedPubSubEvent
    """
    alert, _ = ActiveAlert.objects.get_or_create(
        uid=event.payload["id"],
        defaults={
            "email": event.payload["email"],
            "keywords": event.payload["keywords"],
            "frequency": event.payload["frequency"],
        },
    )

    # Create Product objects from event payload
    products: list[ProductPriceLog] = []
    for item in event.payload["items"]["itemSummaries"]:
        product = ProductPriceLog.objects.create(
            item_id=item["itemId"],
            title=item["title"],
            image_url=item["image"]["imageUrl"],
            price=item["price"]["value"],
            currency=item["price"]["currency"],
            web_url=item["itemWebUrl"],
            timestamp=event.timestamp,
        )
        products.append(product)

    # Update Alert object to track latest Products
    alert.tracked_products.set(products)


def _process_alert_created_event_type(event: ConsumedPubSubEvent) -> None:
    """
    Process `ConsumedPubSubEvent` of `PubSubEventType.ALERT_CREATED`

    In this case we just create a new ActiveAlert. The `ActiveAlert` object
    will be used to track an alert and the products associated with the alert.
    It will also be used to send insights email to the user.

    NOTE: We do get_or_create because it is possible that we get multiple events
    for an alert with the same keywords and email address. In this case we don't
    want to create a new ActiveAlert object. We want to use the existing one.

    :param event: ConsumedPubSubEvent
    """
    ActiveAlert.objects.get_or_create(
        uid=event.payload["id"],
        defaults={
            "email": event.payload["email"],
            "keywords": event.payload["keywords"],
            "frequency": event.payload["frequency"],
        },
    )


def _process_alert_updated_event_type(event: ConsumedPubSubEvent):
    """
    Process `ConsumedPubSubEvent` of `PubSubEventType.ALERT_UPDATED

    In this case we update or create an ActiveAlert object with the new values.
    It could be the case that the user has updated the alert with new keywords
    or a new email address. We need to update the ActiveAlert object with the
    new values to reflect the changes and to be able to send the email to the
    correct email address.

    NOTE: We are creating a new ActiveAlert object if it doesn't exist in the
    DB because it is possible that on or more events reach the consumer before the
    `PubSubEventType.ALERT_CREATED` event. So we need to create a new ActiveAlert
    object in such case.
    """
    ActiveAlert.objects.update_or_create(
        uid=event.payload["id"],
        defaults={
            "email": event.payload["email"],
            "frequency": event.payload["frequency"],
            "keywords": event.payload["keywords"],
        },
    )


def _process_alert_deleted_event_type(event: ConsumedPubSubEvent):
    """Process persisted events of type `alert.deleted`

    In this case we simply set ActiveAlert object as inactive in the DB.
    It could be the case that the user has unsubscribed from the Alert.
    So we need to deactivate the ActiveAlert object so that we don't send
    any emails to the user. Note that we don't delete the associated
    ProductPriceLog objects from the DB. We keep them around for future
    reference and analysis.
    """
    alert = ActiveAlert.objects.get(uid=event.payload["id"])
    alert.is_active = False
    alert.save(update_fields=["is_active", "updated_at"])


@shared_task
@transaction.atomic
def process(id: int):
    """
    Process an event stored in ConsumedPubSubEvent.

    :param id: ID of the PubSubEventStore object
    """
    event = ConsumedPubSubEvent.objects.get(id=id)

    logger.info(f"Processing a ConsumedPubSubEvent: {event}")
    if event.type == PubSubEventType.NEW_PRODUCTS.value:
        _process_new_products_event_type(event)
    elif event.type == PubSubEventType.ALERT_CREATED.value:
        _process_alert_created_event_type(event)
    elif event.type == PubSubEventType.ALERT_UPDATED.value:
        _process_alert_updated_event_type(event)
    elif event.type == PubSubEventType.ALERT_DELETED.value:
        _process_alert_deleted_event_type(event)
    else:
        raise ValueError(f"Unknown ConsumedPubSubEvent type: {event}")

    # Update AlertEvent object
    event.processed = True
    event.save(update_fields=["processed", "updated_at"])

    logger.info(f"Processing complete for ConsumedPubSubEvent: {event}")


@shared_task
def send_product_insights():
    """
    Send product insights to the users with active alerts
    """
    insights: list[dict] = generate_insights(lookback_days=14)

    logger.info(f"Sending product insights to {len(insights)} users: {insights}")
    for insight in insights:
        mails.send_html_mail(
            to=insight["email"],
            subject="New Product Insights",
            context=insight,
            template_name="mails/insight.html",
        )
        logger.info(f"Sent product insights to {insight['email']}: [{insight}]")
