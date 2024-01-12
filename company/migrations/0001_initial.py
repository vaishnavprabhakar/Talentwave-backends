# Generated by Django 4.2.7 on 2024-01-05 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField()),
                (
                    "industry",
                    models.CharField(
                        choices=[
                            ("Technology", "Technology"),
                            ("Finance", "Finance"),
                            ("Healthcare", "Healthcare"),
                            ("Manufacturing", "Manufacturing"),
                            ("Education", "Education"),
                            ("Retail", "Retail"),
                            ("Telecommunications", "Telecommunications"),
                        ],
                        max_length=150,
                    ),
                ),
                ("website", models.URLField(max_length=256)),
                (
                    "logo",
                    models.ImageField(
                        error_messages="Image file is in .jpeg format",
                        upload_to="company_logos/",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
