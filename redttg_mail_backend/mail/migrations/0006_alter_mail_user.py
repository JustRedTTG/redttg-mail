# Generated by Django 4.2.5 on 2023-10-01 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mail", "0005_mail_created_mail_deleted_mail_read_mail_star"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mail",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mails",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
