from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()

class PreviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "name"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id", "name", 
            "date_joined", 
            "webhook", "body", "headers", 
            "is_staff", "is_superuser",
            "locked"
        ]