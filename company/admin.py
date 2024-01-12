from django.contrib import admin
from .models import Job
# Register your models here.


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = ["user", 'job_title','company','workplace_type','location','job_type', 'description']