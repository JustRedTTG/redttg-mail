# Generated by Django 4.2.5 on 2023-09-30 22:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("mail", "0004_mail_envelope_mail_from_sender_mail_to_recipients_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="mail",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="mail",
            name="deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="mail",
            name="read",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="mail",
            name="star",
            field=models.BooleanField(default=False),
        ),
    ]
