FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean

COPY . .

CMD sh -c "python manage.py seed_db && gunicorn -b 0.0.0.0:5000 'app:create_app()'"
