# Generated by Django 4.2.7 on 2023-12-03 12:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0006_alter_post_like"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="user",
            new_name="created_by",
        ),
    ]
