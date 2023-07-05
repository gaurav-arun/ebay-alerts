FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Set the entrypoint
RUN chmod +x scripts/entrypoint.sh
ENTRYPOINT ["scripts/entrypoint.sh"]

CMD ["python", "-m", "celery", "-A", "alerts_backend", "worker", "-E", "-l", "INFO"]
