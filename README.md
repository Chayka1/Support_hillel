# The support project 2023

## Application setup

```bash
pip install pipenv

pipenv shell
pipenv sync --dev

gunicorn config.wsgi --reload
```

## Celery workers start

```bash
pipenv shell
celery worker -A config ...
```
