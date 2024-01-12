from django.contrib import admin
from post.models import Post, Like, Comment

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "image",
        "created_by",
        "description",
        "title",
        "created_at",
        "updated_at",
    )

    list_display_links = ("description", "type")

    ordering = ("-created_at",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("post_id", "id")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post_id",
        "post",
        "body",
        "comment_by",
        "created_at",
        "id",
    )
    list_display_links = ["post", "comment_by"]
