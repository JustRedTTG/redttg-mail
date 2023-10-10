from django.urls import path

from .views import auth, login_api, UserView#, register

urlpatterns = [
    path('', auth),
    path('info/', UserView.as_view()),
    path('login/', login_api),
    # path('register/', register),
]