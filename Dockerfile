FROM python:latest

WORKDIR /app/
COPY . .

RUN apt-get update \
    && apt install -y speedtest-cli \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install pipenv

RUN pipenv sync --dev --system

CMD python manage.py migrate && gunicorn config.wsgi --reload --bind 0.0.0.0:8000