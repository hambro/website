#!/bin/bash
printenv > /etc/environment
cd /
# Wait for Postgres to start
echo "Waiting for postgres..."
while ! nc -z database $PGPORT; do
    # While database connection not open: wait
    sleep 0.5
done
echo "PostgreSQL started"

python manage.py migrate
if [ "$DEBUG" == "False" ]
then
  python manage.py collectstatic --noinput
fi

# Cronmanager uwsgi: starts conjobs
uwsgi -d /dev/null --chdir=./ --module=chemie.chemie.cron_wsgi:application --env DJANGO_SETTINGS_MODULE=chemie.chemie.settings.production \
--master --pidfile=/tmp/project-master-cron.pid --http=0.0.0.0:8001 --processes=5 \
--harakiri=20 --max-requests=5000 --vacuum

# Django main uwsgi: starts website
uwsgi --chdir=./ --module=chemie.chemie.wsgi:application --env DJANGO_SETTINGS_MODULE=chemie.chemie.settings.production \
--master --pidfile=/tmp/project-master.pid --http=0.0.0.0:8000 --processes=5 \
--harakiri=20 --max-requests=5000 --vacuum
