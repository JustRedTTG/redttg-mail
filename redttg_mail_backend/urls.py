from django.urls import path, include

urlpatterns = [
    path('auth/', include('redttg_mail_backend.auth_app.urls')),
]
