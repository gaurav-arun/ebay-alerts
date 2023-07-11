# Create your views here.

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import AlertSerializer
from .models import Alert
import logging
from .utils.mails import send_html_mail
from ebay_sdk import client, utils as ebay_utils
from .utils.pubsub import publish_event
from pubsub import PubSubEventType

logger = logging.getLogger(__name__)


class AlertViewSet(ModelViewSet):
    serializer_class = AlertSerializer
    queryset = Alert.objects.all().order_by("id")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        publish_event(event_type=PubSubEventType.ALERT_CREATED, payload=response.data)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        publish_event(event_type=PubSubEventType.ALERT_UPDATED, payload=response.data)
        return response

    def destroy(self, request, *args, **kwargs):
        instance_id = self.get_object().id
        response = super().destroy(request, *args, **kwargs)
        publish_event(event_type=PubSubEventType.ALERT_DELETED, payload={'id': instance_id})
        return response
