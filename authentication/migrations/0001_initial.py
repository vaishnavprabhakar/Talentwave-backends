# Generated by Django 4.2.7 on 2023-11-15 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


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
                ("username", models.CharField(max_length=100, unique=True)),
                ("email", models.EmailField(max_length=154, unique=True)),
                (
                    "account_type",
                    models.CharField(
                        choices=[
                            ("jobseeker", "Job Seeker"),
                            ("recruiter", "Recruiter"),
                        ],
                        error_messages="J - Jobseeker, R - Recruiter.",
                        max_length=150,
                        null=True,
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("first_name", models.CharField(max_length=120)),
                ("last_name", models.CharField(max_length=120)),
                (
                    "profile_image",
                    models.ImageField(blank=True, null=True, upload_to="profile/"),
                ),
                ("bio", models.TextField(null=True)),
                ("title", models.CharField(max_length=201, null=True)),
                (
                    "dob",
                    models.DateField(
                        editable=False, null=True, verbose_name="date of birth"
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, null=True, region="IN"
                    ),
                ),
                ("city", models.CharField(max_length=200, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("resume", models.FileField(upload_to="profile/resumes/")),
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