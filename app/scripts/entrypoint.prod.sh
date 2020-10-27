#!/bin/sh

set -e

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"

python manage.py collectstatic --no-input

uwsgi --socket :8000 --master --enable-threads --module bop.wsgi


