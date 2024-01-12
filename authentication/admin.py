from django.contrib import admin
from .models import User, Profile, Follow, RecruiterProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
    )
    readonly_fields = ("password",)
    list_display_links = ("email",)
    

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "profile_image",
        "city",
        "bio",
        "title"
    )
    list_display_links = ['first_name','last_name']

    

@admin.register(RecruiterProfile)
class RecruiterProfile(admin.ModelAdmin):
    list_display = ("user", "company_name", "position")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


