import json
from traceback import print_exc
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .file_functions import calculate_md5
from .models import Mail, File, UserFile
from .serializers import PreviewMailSerializer, MailSerializer
from .validation import validate_email
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import send_webhook, test_webhook, DeliveryError

UserModel = get_user_model()


@require_POST
def receive_mail(request: HttpRequest):
    d = dict(request.POST)
    d['pending_webhook'] = True

    envelope = json.loads(Mail.escape_data(d, 'envelope', '{}'))
    to = envelope.get('to', [])

    if len(to) == 0:
        return HttpResponse(status=400)

    for recipient in to:
        if not (recipient_name := validate_email(recipient)):
            return HttpResponse(status=400)
        if recipient_name.startswith('notebookrepr-'):
            user = UserModel.objects.filter(notebook_repr=recipient_name.split('repr-', 1)).first()
            d['notebook_mail'] = True
        else:
            user = UserModel.objects.filter(name=recipient_name).first()
        if not user:
            return HttpResponse(status=400)
        mail = user.mails.create(data=d)  # type: ignore

        attachments = []
        for file in request.FILES.values():
            md5_hash = calculate_md5(file)

            file_object = File.objects.filter(md5_hash=md5_hash).first()

            if not file_object:
                # Create a new Attachment record
                file_object = File(file=file, md5_hash=md5_hash)
                file_object.save()
            attachments.append(file_object)

        attachment_info = json.loads(
            mail.escape_data(d, 'attachment-info', '{}'))

        mail.save()

        for info, attachment in zip(attachment_info.values(), attachments):
            mail.attachments.create(
                file=attachment, filename=info['filename'], name=info['name']).save()  # type: ignore
            UserFile.objects.create(user=user, file=attachment).save()

    try:
        send_webhook.apply_async(
            args=(mail.pk, request.get_host()), # type: ignore
            retry=True, 
            retry_policy={
                'max_retries': None,
                'interval_start': 0,
                'interval_step': 30,
                'interval_max': 3600,
                'retry_errors': (DeliveryError,)
            }, 
            countdown=2) 
    except Exception as e:
        print_exc()
        mail.delete() # type: ignore
        return HttpResponse(status=500)
    return HttpResponse(status=200)


class MailListView(ListAPIView):
    serializer_class = PreviewMailSerializer
    def get_queryset(self):
        return Mail.objects.filter(user=self.request.user).order_by('-created')


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


@login_required
def test(request):
    test_webhook.apply_async(
        args=(request.user.pk, request.get_host()),
        retry=True, 
        retry_policy={
            'max_retries': 3,
        }, 
        countdown=1)
    return HttpResponse(status=200)
