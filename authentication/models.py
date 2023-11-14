from django.db import models
from authentication.managers import CustomBaseUserManager
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.




class User(AbstractBaseUser):

    email = models.EmailField(max_length=154, unique=True)
    username = models.CharField(max_length=100, unique=True)

    accont_type = models.CharField(
        max_length=150,
        choices=(
            ("jobseeker", "Job Seeker"),
            ("recruiter", "Recruiter"),
        ),
    )

    is_admin = models.BooleanField(default=False,)

    is_active = models.BooleanField(default=False)

    
    
    @property
    def is_staff(self):
        return self.is_admin
    
    
    objects = CustomBaseUserManager()

    def __str__(self):
        return self.email
    

    

    USERNAME_FIELD = 'email'