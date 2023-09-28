from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Mail


@csrf_exempt
@require_POST
def mail(request: HttpRequest):
    d = dict(request.POST)

    print(request.FILES)

    Mail.objects.create(data=d).save()

    return HttpResponse(status=200)