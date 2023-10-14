from django.urls import path

from .views import auth, login_api, UserView, UserListView, edit#, register

urlpatterns = [
    path('', auth),
    path('info/', UserListView.as_view()),
    path('info/<int:pk>/', UserView.as_view()),
    path('edit/', edit),
    path('login/', login_api),
    # path('register/', register),
]