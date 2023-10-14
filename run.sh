#!/bin/sh

echo "Applying database migrations"
python manage.py migrate

python -m celery -A redttg_mail_backend worker &

exec "$@"