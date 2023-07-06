FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=alerts_backend.settings_local

COPY alerts_backend/requirements.txt .

RUN pip install -r requirements.txt

COPY alerts_backend .
COPY pubsub ./pubsub

# Set the entrypoint
RUN chmod +x dockerfiles/scripts/entrypoint.sh
ENTRYPOINT ["dockerfiles/scripts/entrypoint.sh"]

#CMD ["python", "-m", "celery", "-A", "alerts_backend", "worker", "-E", "-l", "INFO"]
