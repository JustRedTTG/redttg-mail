from django.urls import path

from .views import mail

urlpatterns = [
    path('', mail),
]