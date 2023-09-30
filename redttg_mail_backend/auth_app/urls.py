from django.urls import path

from .views import auth, login_api#, register

urlpatterns = [
    path('/', auth),
    path('login/', login_api),
    # path('register/', register),
]