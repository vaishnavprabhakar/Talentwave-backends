from django.contrib import admin
from post.models import Post

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "image",
        "description",
        "title",
        "created_at",
        "updated_at",
    )

    list_display_links = ("description", "type")
