import os
from django.urls import path

from .views import receive_mail

urlpatterns = [
    path(os.environ.get("EXTERNAL_API_MAIL", ''), receive_mail),
]