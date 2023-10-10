from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from ..mail.models import File, UserFile
from .models import AccountModel
from .serializers import UserSerializer

@csrf_exempt
def auth(request):
    if request.user.pk is not None:
        uri = request.headers.get('X-Original-URI')
        if not uri:
            return HttpResponse(status=200, content='YES')

        attachment = uri.lstrip('/files/')
        print(attachment)
        response = HttpResponse(status=401, content='NO')
        file = File.objects.get(file=attachment)
        if file is not None:
            userfile = UserFile.objects.filter(file=file, user=request.user)
            print(userfile)
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
        return redirect('/login')
    else:
        login(request, user)
        return redirect('/')
    
class UserView(APIView):
    def get(self, request):
        if request.user.pk:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response(status=403)