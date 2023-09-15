# The Ticket Support project 2023

# Support platform for the website using technologies such as Django, REST, and Sqlite3. The program is equipped with everything necessary, including user authentication, creation and resolution of user resource issues using Support managers, and real-time chat for quick and easy problem-solving. An indispensable tool for multi-user websites and applications.


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
