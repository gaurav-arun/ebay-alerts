FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry and pin version
RUN pip install poetry==1.5.1

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --only ebay_mock_docker --no-interaction --no-ansi --no-root

COPY ebay_mock .

# For documentation
EXPOSE 8002

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
