import json
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .file_functions import calculate_md5
from .models import Mail, Attachment, File


@csrf_exempt
@require_POST
def mail(request: HttpRequest):
    d = dict(request.POST)

    mail = Mail(data=d)

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
        mail.attachments.create(file=attachment, filename=info['filename'], name=info['name']).save()


    Mail.objects.create(data=d).save()

    return HttpResponse(status=200)