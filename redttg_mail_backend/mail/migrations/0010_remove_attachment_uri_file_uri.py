# Generated by Django 4.2.5 on 2023-11-09 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mail", "0009_attachment_uri"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attachment",
            name="uri",
        ),
        migrations.AddField(
            model_name="file",
            name="uri",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
