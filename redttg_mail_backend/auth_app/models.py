import random
import re
import string

import django.contrib.auth.models as auth_models
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from django.apps import apps


class AccountManager(auth_models.BaseUserManager):
    def _create_user(self, name, password, **extra_fields):
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, password, **extra_fields)

    def create_superuser(self, name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(name, password, **extra_fields)


class AccountModel(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'name'
    name = models.CharField(unique=True, blank=False, null=False, max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    webhook = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    headers = models.JSONField(default=dict)
    send_attachments = models.BooleanField(default=False)

    objects = AccountManager()

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
