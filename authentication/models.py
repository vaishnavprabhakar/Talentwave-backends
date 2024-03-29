from datetime import date
from django.db import models
from company.models import Job
from authentication.managers import CustomBaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, blank=True)
    email = models.EmailField(
        max_length=154,
        unique=True,
    )
    account_type = models.CharField(
        max_length=150,
        choices=(
            ("jobseeker", "Job Seeker"),
            ("recruiter", "Recruiter"),
        ),
    )

    is_admin = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=False,
    )

    @property
    def is_staff(self):
        return self.is_admin

    # Simplest possible answer: True, always
    def has_perm(self, perm, obj=None):
        return True

    # Simplest possible answer: True, always
    def has_module_perms(self, authentication):
        return True

    objects = CustomBaseUserManager()

    def __str__(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(
        max_length=120,
        null=True,
    )

    last_name = models.CharField(max_length=120, null=True)

    profile_image = models.TextField(null=True)

    bio = models.TextField(null=True)

    title = models.CharField(max_length=201, null=True)

    dob = models.DateField(verbose_name="date of birth", null=True)

    phone = PhoneNumberField(region="IN", null=True, unique=True)

    city = models.CharField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)

    resume = models.FileField(upload_to="resumes/", blank=True, default=None)

    def __str__(self):
        return f"{self.user}'s Profile"

    @property
    def get_age(self):
        if self.dob:
            today = date.today()
            return (
                today.year
                - self.dob.year
                - ((today.month, today.day) < (self.dob.month, self.dob.day))
            )
        return None


class RecruiterProfile(models.Model):
    POSITION_CHOICE = (
        ("HR", "HUMAN RESOURCE"),
        ("Recruiter", "RECRUITER"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=256)
    position = models.CharField(max_length=150, choices=POSITION_CHOICE)
    proffessional_card = models.FileField(
        upload_to="proffessional_cards/", serialize=True, unique=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.user}"


class Follow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name="following")
    follower = models.ManyToManyField(User, related_name="follower")

    def __str__(self):
        return f"{self.user}'s followers"
