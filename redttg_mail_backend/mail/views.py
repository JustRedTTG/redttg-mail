import json
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from .file_functions import calculate_md5
from .models import Mail, Attachment, File
from .serializers import PreviewMailSerializer, MailSerializer
from .validation import validate_email
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

UserModel = get_user_model()


@csrf_exempt
@require_POST
def receive_mail(request: HttpRequest):
    d = dict(request.POST)

    envelope = json.loads(Mail.escape_data(d, 'envelope', '{}'))
    to = envelope.get('to', [])

    if len(to) == 0:
        return HttpResponse(status=400)

    for recipient in to:
        if not (recepient_name := validate_email(to)):
            return HttpResponse(status=400)
        user = UserModel.objects.filter(name=recipient_name).first()
        if not user:
            return HttpResponse(status=400)
        mail = user.mails.create(data=d)  # type: ignore

        attachments = []
        for file in request.FILES.values():
            md5_hash = calculate_md5(file)

            attachment = File.objects.filter(md5_hash=md5_hash).first()

            if not attachment:
                # Create a new Attachment record
                attachment = File(file=file, md5_hash=md5_hash)
                attachment.save()
            attachments.append(attachment)

        attachment_info = json.loads(
            mail.escape_data(d, 'attachment-info', '{}'))

        mail.save()

        for info, attachment in zip(attachment_info.values(), attachments):
            mail.attachments.create(
                file=attachment, filename=info['filename'], name=info['name']).save()  # type: ignore

    return HttpResponse(status=200)

class MailListView(ListAPIView):
    serializer_class = PreviewMailSerializer
    queryset = Mail.objects.all().order_by('-created')

class MailView(APIView):
    def get(self, request, pk):
        try:
            # Retrieve the Mail object with the given primary key
            mail = Mail.objects.get(pk=pk)

            # Check if the Mail object belongs to the logged-in user
            if mail.user == request.user:
                serializer = MailSerializer(mail)
                return Response(serializer.data)
            else:
                return Response(status=403)
        except Mail.DoesNotExist:
            return Response(status=404)