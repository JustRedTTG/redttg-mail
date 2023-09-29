import json
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from .file_functions import calculate_md5
from .models import Mail, Attachment, File

UserModel = get_user_model()


@csrf_exempt
@require_POST
def mail(request: HttpRequest):
    d = dict(request.POST)

    envelope = json.loads(Mail.escape_data(d, 'envelope', '{}'))
    to = envelope.get('to', [])

    if len(to) == 0:
        return HttpResponse(status=400)

    for recipient in to:
        if not recipient.endswith('@redttg.com'):
            return HttpResponse(status=400)
        recipient_name = recipient.split('@')[0]
        user = UserModel.objects.filter(name=recipient_name).first()
        if not user:
            return HttpResponse(status=400)
        mail = user.mails.create(data=d) # type: ignore

        attachments = []
        for file in request.FILES.values():
            md5_hash = calculate_md5(file)

            attachment = File.objects.filter(md5_hash=md5_hash).first()

            if not attachment:
                # Create a new Attachment record
                attachment = File(file=file, md5_hash=md5_hash)
                attachment.save()
            attachments.append(attachment)

        attachment_info = json.loads(mail.escape_data(d, 'attachment-info', '{}'))
        
        mail.save()

        for info, attachment in zip(attachment_info.values(), attachments):
            mail.attachments.create(file=attachment, filename=info['filename'], name=info['name']).save() # type: ignore


        Mail.objects.create(data=d).save()

    return HttpResponse(status=200)