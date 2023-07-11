from django.db import models


class TimestampedModel(models.Model):
    """
    Abstract model to inject created_at and updated_at fields in models
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Alert(TimestampedModel):
    """
    Model to track alerts configured by the user
    """

    email = models.EmailField(max_length=128, db_index=True)
    keywords = models.TextField(null=False, blank=False)
    frequency = models.IntegerField(null=False)

    def __str__(self):
        return f"[{self.id}]:[{self.email}]:[{self.keywords}]:[{self.frequency}]"
