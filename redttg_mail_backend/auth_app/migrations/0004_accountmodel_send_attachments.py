# Generated by Django 4.2.5 on 2023-11-09 07:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_app", "0003_accountmodel_body"),
    ]

    operations = [
        migrations.AddField(
            model_name="accountmodel",
            name="send_attachments",
            field=models.BooleanField(default=False),
        ),
    ]
