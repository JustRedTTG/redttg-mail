from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserModel
    fields = ["id", "name"]