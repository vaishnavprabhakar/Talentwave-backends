# Generated by Django 4.2.7 on 2023-12-03 12:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("post", "0007_rename_user_post_created_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="like",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
