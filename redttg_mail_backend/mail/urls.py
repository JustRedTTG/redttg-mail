import os
from django.urls import path

from .views import receive_mail, MailListView, MailView, test

urlpatterns = [
    path(os.environ.get('EXTERNAL_API_MAIL', ''), receive_mail),
    path(f"{os.environ.get('EXTERNAL_API_MAIL', '')}fetch/", MailListView.as_view()),
    path(f"{os.environ.get('EXTERNAL_API_MAIL', '')}fetch/<int:pk>/", MailView.as_view()),
    path(f"{os.environ.get('EXTERNAL_API_MAIL', '')}test/", test),
]