# Generated by Django 4.2.7 on 2023-11-18 12:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="dob",
            field=models.DateField(null=True, verbose_name="date of birth"),
        ),
    ]
