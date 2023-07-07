FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY analytics/requirements.txt .

RUN pip install -r requirements.txt

COPY analytics .
COPY pubsub ./pubsub

# Set the entrypoint
RUN chmod +x dockerfiles/scripts/entrypoint.sh
ENTRYPOINT ["dockerfiles/scripts/entrypoint.sh"]

CMD celery -A analytics beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler & \
    celery -A analytics worker --loglevel=info & \
    python manage.py pubsub_event_consumer