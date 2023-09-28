from django.db import models


# TODO: I need to test the api first
class Mail(models.Model):
    data = models.TextField()


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    md5_hash = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.md5_hash
