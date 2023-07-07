from django.apps import AppConfig


class InsightsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'insights'

    # def ready(self):
    #     from .tasks import consume_events
    #     consume_events.apply_async()
