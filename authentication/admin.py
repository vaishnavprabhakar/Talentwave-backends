from django.contrib import admin
from authentication.models import User, Profile, RecruiterProfile, Post




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
    


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user',)
