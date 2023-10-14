import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redttg_mail_backend.settings")

app = Celery("redttg_mail_backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()