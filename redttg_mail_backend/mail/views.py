from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .file_functions import calculate_md5
from .models import Mail, Attachment


@csrf_exempt
@require_POST
def mail(request: HttpRequest):
    d = dict(request.POST)

    mail = Mail(data=d)

    for file in request.FILES:
        md5_hash = calculate_md5(file)

        attachment = Attachment.objects.filter(md5_hash=md5_hash).first()

        if not attachment:
            # Create a new Attachment record
            attachment = Attachment(file=file, md5_hash=md5_hash)
            attachment.save()




    Mail.objects.create(data=d).save()

    return HttpResponse(status=200)