# Generated by Django 4.2.5 on 2023-11-09 07:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mail", "0008_mail_pending_webhook"),
    ]

    operations = [
        migrations.AddField(
            model_name="attachment",
            name="uri",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
