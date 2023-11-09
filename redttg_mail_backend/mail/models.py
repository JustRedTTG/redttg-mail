from django.contrib.auth import get_user_model
from typing import Any
from django.db import models
from .fields import *
from random import choice
import string

UserModel = get_user_model()
CHARACTERS = characters = string.ascii_letters + string.digits + "-_"



class Mail(models.Model):
    text = models.TextField(blank=True)
    html = models.TextField(blank=True)
    subject = models.CharField(max_length=255, blank=True)
    dkim = models.CharField(max_length=255, default='{}')
    sender_ip = models.GenericIPAddressField(blank=True, null=True)
    spf = models.CharField(max_length=20, blank=True)
    from_sender = models.CharField(max_length=255, blank=True)
    to_recipients = models.CharField(max_length=255, blank=True)
    envelope = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='mails')
    created = models.DateTimeField(auto_now_add=True)
    star = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    pending_webhook = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs) -> None:
        if 'data' in kwargs.keys():
            data = kwargs.pop('data')
        else:
            return super().__init__(*args, **kwargs)
        super().__init__(
            text=self.escape_data(data, 'text'),
            html=self.escape_data(data, 'html'),
            subject=self.escape_data(data, 'subject'),
            dkim=self.escape_data(data, 'dkim', None),
            sender_ip=self.escape_data(data, 'sender_ip', None),
            spf=self.escape_data(data, 'SPF', 'failure'),
            from_sender=self.escape_data(data, 'from'),
            to_recipients=self.escape_data(data, 'to'),
            envelope=self.escape_data(data, 'envelope'),
            **kwargs
        )

    @staticmethod
    def escape_data(data: dict, key: str, default: Any = '') -> str:
        encased =  data.get(key)
        if not encased:
            return default
        return list(encased)[0]


# Scrapped
# class Box(models.Model):
#     tag = models.CharField(max_length=255, unique=True)


class UserFile(models.Model):
    file = models.ForeignKey('File', on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='files')
    
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
    _uri = models.CharField(max_length=255, blank=True, null=True, name="uri")

    @property
    def uri(self):
        return self._uri if self._uri and len(self._uri) != 0 else self.generate_uri()

    @uri.setter
    def uri(self, value):
        if len(value) < 255:
            raise ValueError("uri is too small")
        self._uri = value

    def generate_uri(self):
        self.uri = ''.join(choice(characters) for _ in range(255))
        self.save()

        return self._uri