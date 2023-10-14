from django.urls import path

from .views import auth, login_api, UserView, UserListView, Modify#, register

urlpatterns = [
    path('', auth),
    path('info/', UserListView.as_view()),
    path('info/<int:pk>/', UserView.as_view()),
    path('edit/', Modify.as_view()),
    path('login/', login_api),
    # path('register/', register),
]