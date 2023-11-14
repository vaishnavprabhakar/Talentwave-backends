# Generated by Django 4.2.7 on 2023-11-14 08:48

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("email", models.EmailField(max_length=154, unique=True)),
                ("username", models.CharField(max_length=100, unique=True)),
                (
                    "accont_type",
                    models.CharField(
                        choices=[
                            ("jobseeker", "Job Seeker"),
                            ("recruiter", "Recruiter"),
                        ],
                        max_length=150,
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
