#!/bin/sh

if [ "$1" = "web" ]; then
  python manage.py migrate
  python manage.py collectstatic --noinput
  gunicorn --bind :8000 --workers 5 datastore.wsgi
elif [ "$1" = "beat" ]; then
  celery -A datastore beat -l INFO
elif [ "$1" = "worker" ]; then
  celery -A datastore worker -l INFO
else
  exec "$@"
fi
