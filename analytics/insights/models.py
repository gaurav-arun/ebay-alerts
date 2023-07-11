from django.db import models

from pubsub import PubSubEventType


class TimestampedModel(models.Model):
    """
    Abstract model to inject created_at and updated_at fields in models
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ConsumedPubSubEvent(TimestampedModel):
    """
    Model to track events consumed from PubSub
    """

    type = models.CharField(max_length=255, choices=PubSubEventType.choices())
    payload = models.JSONField()
    timestamp = models.DateTimeField(null=True, blank=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.id}]:[{self.type}]:[{self.processed}]"


class ProductPriceLog(models.Model):
    """
    Model to track price changes for products. This model is populated by processing
    the consumed events from PubSub. This model is used to generate insights.
    """

    item_id = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    timestamp = models.DateTimeField(blank=False, null=False)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    web_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return (
            f"[{self.id}]:[{self.item_id}]:[{self.title}]:"
            f"[{self.price}]:[{self.currency}]"
        )


class ActiveAlert(TimestampedModel):
    """
    Model to track alerts configured by the user and the products associated with
    the alert. This model is populated by processing the consumed events from PubSub.
    """

    uid = models.IntegerField(null=False, blank=False, db_index=True, unique=True)
    email = models.EmailField(max_length=128, db_index=True)
    keywords = models.TextField(null=False, blank=False)
    frequency = models.IntegerField(null=False)
    is_active = models.BooleanField(default=True)
    tracked_products = models.ManyToManyField(ProductPriceLog, blank=True)

    def __str__(self):
        return f"[{self.uid}]:[{self.email}]:[{self.keywords}]:[{self.frequency}]"
