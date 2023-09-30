from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate


@csrf_exempt
def auth(request):
    if request.user.pk is not None:
        response = HttpResponse(status=200, content='YES')
    else:
        response = HttpResponse(status=401, content='NO')

    return response

@require_POST
@csrf_exempt
def login_api(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username is None or password is None:
        return HttpResponse(status=400)
    
    if username.endswith('@redttg.com'):
        username = username.replace('@redttg.com', '')
    username = username.strip()

    user = authenticate(username=username, password=password)

    if user is None:
        return HttpResponse(status=401)
    else:
        login(request, user)
        return HttpResponse(status=200)