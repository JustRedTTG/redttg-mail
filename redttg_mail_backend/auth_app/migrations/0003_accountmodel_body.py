# Generated by Django 4.2.5 on 2023-10-14 19:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_app", "0002_accountmodel_headers_accountmodel_webhook"),
    ]

    operations = [
        migrations.AddField(
            model_name="accountmodel",
            name="body",
            field=models.TextField(blank=True),
        ),
    ]
