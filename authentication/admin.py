from django.contrib import admin
from .models import User, Profile, RecruiterProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username',)
    readonly_fields = ('password',)
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','profile_image', 'phone', 'city', 'bio', 'title', 'resume')


@admin.register(RecruiterProfile)
class RecruiterProfile(admin.ModelAdmin):
    list_display = ('user','company_name', 'position')
    