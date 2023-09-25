import django.contrib.auth.models as auth_models
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from django.apps import apps


# TODO: Implementation of a full fledged mail model