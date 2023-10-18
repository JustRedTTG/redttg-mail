from .models import Mail
from .serializers import MailSerializer
from ..auth_app.models import AccountModel
from celery import shared_task
from django.conf import settings
import requests

def variables(variable_map: dict, text: str) -> str:
    for key, value in variable_map.items():
        text = text.replace('{{'+key+'}}', value)
    return text


def deliver_webhook(user: AccountModel, mail: Mail, host: str):
     variable_map = {
         "user_id": str(user.pk),
         "user_name": user.name,
         "user_mail": f"{user.name}@redttg.com", 
         "mail_id": str(mail.pk),
         "mail_url": f'https://{host}/mail/{mail.pk}',
         "mail_from": mail.from_sender,
         "mail_subject": mail.subject
     }
 
     webhook = variables(variable_map, user.webhook)
     if not webhook: return
     body = variables(variable_map, user.body)
     headers = {
         variables(variable_map, key): variables(variable_map, value)
         for key, value in user.headers.items()
     }
 
     requests.post(webhook, data=body, headers=headers)
     mail.pending_webhook = False
     mail.save()
 

@shared_task()
def send_webhook(mail_id: int, host: str):
    mail = Mail.objects.get(id=mail_id)
    user: AccountModel = mail.user # type: ignore
    deliver_webhook(user, mail, host)
 
@shared_task
def test_webhook(user_id: int, host: str):
    user = AccountModel.objects.get(id=user_id)
    mail = Mail(
        id=-1, 
        text = "Hello, world", 
        html = "<p>Hello, world</p>", 
        subject = "This is a webhook test email!", 
        from_sender = "from@redttg.com"
    )
    deliver_webhook(user, mail, host)