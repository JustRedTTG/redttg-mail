from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .file_functions import calculate_md5
from .models import Mail, Attachment


@csrf_exempt
@require_POST
def mail(request: HttpRequest):
    d = dict(request.POST)

    for file in request.FILES:
        md5_hash = calculate_md5(file)

        # Check if a file with the same hash exists in the database
        existing_attachment = Attachment.objects.filter(md5_hash=md5_hash).first()

        if not existing_attachment:
            # Create a new Attachment record
            new_attachment = Attachment(file=file, md5_hash=md5_hash)
            new_attachment.save()




    Mail.objects.create(data=d).save()

    return HttpResponse(status=200)