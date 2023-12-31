# Create your views here.

import logging

from rest_framework.viewsets import ModelViewSet

from pubsub import PubSubEventType

from .models import Alert
from .serializers import AlertSerializer
from .utils.pubsub import publish_event

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
        publish_event(
            event_type=PubSubEventType.ALERT_DELETED, payload={"id": instance_id}
        )
        return response
