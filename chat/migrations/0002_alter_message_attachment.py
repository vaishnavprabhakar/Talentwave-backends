# Generated by Django 4.2.7 on 2024-02-12 08:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="attachment",
            field=models.FileField(max_length=256, upload_to=""),
        ),
    ]
