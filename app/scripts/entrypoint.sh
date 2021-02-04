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

crond -s /var/spool/cron/crontabs -b -L /var/log/cron/cron.log "$@"

python manage.py migrate
python manage.py crontab add

exec "$@"
