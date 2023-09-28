from typing import Any
from django.db import models
from .fields import *

class Mail(models.Model):
    text = models.TextField(blank=True)
    html = models.TextField(blank=True)
    subject = models.CharField(max_length=255, blank=True)
    dkim = models.CharField(max_length=255, default='{}')
    sender_ip = models.GenericIPAddressField(blank=True, null=True)
    spf = models.CharField(max_length=20, blank=True)

    def __init__(self, data) -> None:
        super().__init__(
            text=self.escape_data(data, 'text'),
            html=self.escape_data(data, 'html'),
            subject=self.escape_data(data, 'subject'),
            dkim=self.escape_data(data, 'dkim', None),
            sender_ip=self.escape_data(data, 'sender_ip', None),
            spf=self.escape_data(data, 'SPF', 'failure')
        )

    def escape_data(self, data: dict, key: str, default: Any = '') -> str:
        encased =  data.get(key)
        if not encased:
            return default
        return list(encased)[0]

    
class File(models.Model):
    file = models.FileField(upload_to='attachments_files/')
    md5_hash = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.md5_hash

      
class Attachment(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, related_name='attachments')