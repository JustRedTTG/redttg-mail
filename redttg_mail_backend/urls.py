import os
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(os.environ.get("EXTERNAL_API_AUTH", ''), include('redttg_mail_backend.auth_app.urls')),
    path('', include('redttg_mail_backend.mail.urls')),
]
