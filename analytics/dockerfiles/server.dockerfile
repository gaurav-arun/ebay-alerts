FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY analytics/requirements.txt .

RUN pip install -r requirements.txt

COPY analytics .
COPY pubsub ./pubsub

# For documentation
EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
