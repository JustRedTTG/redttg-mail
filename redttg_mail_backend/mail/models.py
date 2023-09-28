from django.db import models


class Mail(models.Model):
    data = models.TextField()

    
class File(models.Model):
    file = models.FileField(upload_to='attachments_files/')
    md5_hash = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.md5_hash

      
class Attachment(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, related_name='attachments')