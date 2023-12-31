from .models import Mail
from .serializers import MailSerializer
from ..auth_app.models import AccountModel
from celery import shared_task
from django.conf import settings
from traceback import print_exc
import requests
import rsa
import base64

def variables(variable_map: dict, text: str) -> str:
    for key, value in variable_map.items():
        text = text.replace('{{'+key+'}}', value)
    return text

class DeliveryError(Exception):
    pass

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
    attachments = [f"https://{host}/files/{attachment.file.file}?uri={attachment.file.uri}" for attachment in mail.attachments.all()] # type: ignore

    variable_map.update({
        f"attachment_{index}":attachment
        for index, attachment in enumerate(attachments) # type: ignore
    })
    variable_map['attachments'] = ', '.join(attachments)
    
 
    webhook = variables(variable_map, user.webhook)
    if not webhook: return
    body = variables(variable_map, user.body)
    headers = {
        variables(variable_map, key): variables(variable_map, value)
        for key, value in user.headers.items()
    }
 
    response = requests.post(webhook, data=body, headers=headers)
    if response.status_code != 200:
        print(f"Webhook response: {response.status_code} - '{response.text}' headers: {headers} data: {body}")
    if mail.pk > 0:
        mail.pending_webhook = False
        mail.save()
 

def deliver_notebook(user: AccountModel, mail: Mail, host: str):
    headers = {
        'File': [f"https://{host}/files/{attachment.file.file}?uri={attachment.file.uri}" for attachment in mail.attachments.all()][0],
        'Subject': mail.subject,
        'Authorization': base64.b64encode(rsa.encrypt(user.notebook_repr.encode(), settings.NOTEBOOK_PUBLIC_KEY)).decode()
    }
    response = requests.post(f"https://notebook.redttg.com/port/{mail.notebook_mail}", headers=headers)
    if response.status_code != 200:
        print(f"Notebook response: {response.status_code} - '{response.text}' headers: {headers}")
    if mail.pk > 0:
        mail.pending_webhook = False
        mail.save()

@shared_task()
def send_webhook(mail_id: int, host: str):
    mail = Mail.objects.get(id=mail_id)
    user: AccountModel = mail.user # type: ignore
    print(mail.notebook_mail)
    try:
        if mail.notebook_mail >= 0:
            print("Attemping a delivery of notebook")
            deliver_notebook(user, mail, host)
        else:
            print("Attemping a delivery of webhook")
            deliver_webhook(user, mail, host)
    except:
        print_exc()
        raise DeliveryError("Failed to deliver")
 
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