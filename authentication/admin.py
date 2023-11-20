from django.contrib import admin
from django.forms import ModelForm
from .models import User, Profile




admin.site.register(User)
admin.site.register(Profile)
