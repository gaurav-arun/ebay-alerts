FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY alerts_backend/requirements.txt .

RUN pip install -r requirements.txt

COPY alerts_backend .
COPY pubsub ./pubsub

# For documentation
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
