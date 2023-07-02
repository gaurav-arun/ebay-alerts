# Create your views here.

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import AlertSerializer
from .models import Alert
import logging
from .utils.mails import send_html_mail

logger = logging.getLogger(__name__)

class AlertViewSet(ModelViewSet):
    serializer_class = AlertSerializer
    queryset = Alert.objects.all().order_by("id")

    # def create(self, request, *args: Any, **kwargs: Any) -> Response:
    #     pass
    #
    # def retrieve(self, request, pk=None, *args, **kwargs) -> Response:
    #     pass
    #
    def update(self, request, pk=None, *args, **kwargs) -> Response:
        # logger.info("=========> Sending Email...")
        #
        # send_mail(
        #     subject='Email with TLS on',
        #     message='That’s your message body',
        #     from_email='from@yourdjangoapp.com',
        #     recipient_list=['grathore07@yourbestuser.com', 'gaurav@somedomain.in'],
        #     auth_user='be6c3e73d086a1',
        #     auth_password='e98802c26bf19d',
        #     fail_silently=False,
        # )
        # logger.info("=========> Email Sent...")
        # from django.core.mail import EmailMultiAlternatives
        #
        # subject, from_email, to = "hello", "from@example.com", "to@example.com"
        # text_content = "This is an important message."
        # html_content = "<p>This is an <strong>important</strong> message.</p>"
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
        # from ebay_alerts.alerts.utils import send_html_mail
        logger.info("=========> Sending Email...")
        send_html_mail(
            template_name='mails/test.html',
            # TODO: Add default from email in settings
            from_email='noreply@ebayalerts.com',
            to=['user@gmail.com'],
            context={},
        )
        logger.info("=========> Sent Email...")

        return Response(data={"message": "Email sent"})

    # def destroy(self, request, pk=None, *args, **kwargs) -> Response:
    #     pass
