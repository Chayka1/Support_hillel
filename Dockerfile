FROM python:latest

WORKDIR /app/
COPY . .

RUN apt-get update \
    && apt install -y speedtest-cli \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install pipenv

RUN pipenv sync --dev --system

CMD bash