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
    && poetry install --only alerts_backend_docker --no-interaction --no-ansi --no-root

# Remove pubsub dist files after installation
RUN rm -rfv /pubsub

# Copy the source code
COPY alerts_backend .

# Set the entrypoint
RUN chmod +x dockerfiles/scripts/entrypoint.sh
ENTRYPOINT ["dockerfiles/scripts/entrypoint.sh"]

# Run celery and celery beat
CMD celery -A alerts_backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler & \
    celery -A alerts_backend worker --loglevel=info -Q alerts_backend
