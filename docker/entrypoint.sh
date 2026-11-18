#!/bin/sh
# Laboratorio de una sola instancia: aplicar migraciones al arrancar es seguro aquí
# (con varias réplicas se haría como paso de despliegue aparte).
set -e
python manage.py migrate --noinput
exec gunicorn supermarket_project.wsgi:application \
    --bind 0.0.0.0:8000 --workers 2 \
    --worker-tmp-dir /dev/shm --access-logfile -
