from typing import Any
from django.db import models
from .fields import *

class Mail(models.Model):
    text = models.TextField(blank=True)
    html = models.TextField(blank=True)
    subject = models.CharField(max_length=255, blank=True)


    def __init__(self, data) -> None:
        super().__init__(
            text=data.get('text'),
            html=data.get('html'),
            subject=data.get('subject')
        )

    
class File(models.Model):
    file = models.FileField(upload_to='attachments_files/')
    md5_hash = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.md5_hash

      
class Attachment(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, related_name='attachments')