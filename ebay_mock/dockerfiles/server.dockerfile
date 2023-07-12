FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ebay_mock/requirements.txt .

RUN pip install -r requirements.txt

COPY ebay_mock .

# For documentation
EXPOSE 8002

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
