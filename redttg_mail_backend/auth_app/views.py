from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from ..mail.models import File, UserFile
from .models import AccountModel
from .serializers import UserSerializer, PreviewUserSerializer


@csrf_exempt
def auth(request):
    if request.user.pk is not None:
        uri = request.headers.get('X-Original-URI')

        if not 'files' in uri:
            return HttpResponse(status=200, content=request.user.pk)

        attachment = uri.lstrip('/files/')
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


class UserView(LoginRequiredMixin, APIView):
    def get(self, request, pk: int):
        if not request.user.pk != pk and not request.user.is_superuser:
            return Response(status=401)
        serializer = UserSerializer(AccountModel.objects.get(pk=pk))
        return Response(serializer.data)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListAPIView):
    serializer_class = PreviewUserSerializer
    queryset = AccountModel.objects.all().order_by('-date_joined')
    def test_func(self):
        return self.request.user.is_superuser # type: ignore

