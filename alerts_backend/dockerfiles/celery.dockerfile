FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=alerts_backend.settings_local

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Set the entrypoint
RUN chmod +x scripts/entrypoint.sh
ENTRYPOINT ["scripts/entrypoint.sh"]

#CMD ["python", "-m", "celery", "-A", "alerts_backend", "worker", "-E", "-l", "INFO"]
