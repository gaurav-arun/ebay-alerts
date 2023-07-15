FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry and pin version
RUN pip install poetry==1.5.1

WORKDIR /app

# Copy poetry dist for installation
COPY pubsub/dist/ /app/pubsub/dist
COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --only analytics_backend_docker --no-interaction --no-ansi --no-root

# Remove pubsub dist files after installation
RUN rm -rfv /pubsub

# Copy the source code
COPY analytics .

# Set the entrypoint
RUN chmod +x dockerfiles/scripts/entrypoint.sh
ENTRYPOINT ["dockerfiles/scripts/entrypoint.sh"]

CMD celery -A analytics beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler & \
    celery -A analytics worker --loglevel=info & \
    python manage.py pubsub_event_consumer
