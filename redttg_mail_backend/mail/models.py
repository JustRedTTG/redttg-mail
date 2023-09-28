from django.db import models


# TODO: I need to test the api first
class Mail(models.Model):
    data = models.TextField()