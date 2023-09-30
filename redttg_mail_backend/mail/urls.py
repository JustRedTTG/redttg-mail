import os
from django.urls import path

from .views import mail

urlpatterns = [
    path(os.environ.get("EXTERNAL_API_MAIL", ''), mail),
]