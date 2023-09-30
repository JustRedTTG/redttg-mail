import os
from django.urls import path, include

urlpatterns = [
    path(os.environ.get("EXTERNAL_API_AUTH", ''), include('redttg_mail_backend.auth_app.urls')),
    path('', include('redttg_mail_backend.mail.urls')),
]
