from .models import Mail
from ..auth_app.models import AccountModel
from celery import shared_task
from django.conf import settings
import requests

def variables(variable_map: dict, text: str) -> str:
    for key, value in variable_map.items():
        text = text.replace('{{'+key+'}}', value)
    return text

@shared_task()
def send_webhook(mail_id: int, host: str):
    mail = Mail.objects.get(id=mail_id)
    user: AccountModel = mail.user # type: ignore

    variable_map = {
        "user_id": user.pk,
        "user_name": user.name,
        "mail_id": mail.pk,
        "mail_url": f'{host}/mail/{mail_id}',
    }

    webhook = variables(variable_map, user.webhook)
    body = variables(variable_map, user.body)
    headers = {
        variables(variable_map, key): variables(variable_map, value)
        for key, value in user.headers.items()
    }

    requests.post(webhook, data=body, headers=headers)
    mail.pending_webhook = False
    mail.save()
