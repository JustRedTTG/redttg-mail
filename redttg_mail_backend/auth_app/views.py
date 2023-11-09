import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from ..mail.models import File, UserFile
from .models import AccountModel
from .serializers import UserSerializer, PreviewUserSerializer


def auth(request):
    response = HttpResponse(status=401, content='NO')
    uri = request.headers.get('X-Original-URI')

    if uri is None or not 'files' in uri:
        if request.user.pk:
            return HttpResponse(status=200, content=request.user.pk)
        else:
            return response

    uri_final = uri.lstrip('/files/')
    attachment, *query = uri_final.split('?')
    if len(query) != 0:
        query = {
            (item_split := item.split('='))[0]:item_split[1]
            for item in query[0].split('&')
        }
    file = File.objects.get(file=attachment)
    if request.user.pk is not None:
        
        if file is not None:
            userfile = UserFile.objects.filter(file=file, user=request.user)
            response = HttpResponse(status=200, content='YES')
    elif file != None and (query_uri := query.get('uri')) != None and file.uri == query_uri:
        response = HttpResponse(status=200, content="guest")
    else:
        response = HttpResponse(status=401, content='NO')

    return response


@require_POST
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
        if request.user.pk != pk and not request.user.is_superuser:
            return Response(status=401)
        serializer = UserSerializer(AccountModel.objects.get(pk=pk))
        return Response(serializer.data)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListAPIView):
    serializer_class = PreviewUserSerializer
    queryset = AccountModel.objects.all().order_by('-date_joined')

    def test_func(self):
        return self.request.user.is_superuser  # type: ignore


class Modify(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        password = data.get('password')
        if password is not None:
            del data['password']
        user_id = data.get('id')
        if user_id:
            user = AccountModel.objects.get(id=user_id)
            received_user = UserSerializer(instance=user, data=data)
        else:
            received_user = UserSerializer(data=data)
        if not received_user.is_valid():
            return HttpResponse(status=400, content=received_user.errors)
        if user_id != request.user.pk and not request.user.is_superuser:
            return HttpResponse(status=401, content=request.user.id)
        
        user = received_user.save()
        if not user_id:
            user.set_password("")
            user.save()
        elif password is not None:
            user.set_password(password)
            user.save()
        serializer = UserSerializer(user)
        login(request, request.user)
        return HttpResponse(status=200, content=json.dumps(serializer.data))
    def delete(self, request):
        user_id = int(request.body)
        if user_id != request.user.pk and not request.user.is_superuser:
            return HttpResponse(status=401, content=request.user.id)
        AccountModel.objects.get(id=user_id).delete()
        return HttpResponse(status=200)
