from django.db import models
from authentication.models import User

# Create your models here.


class Post(models.Model):
    POST_CHOICES = (
        ("J", "Job"),
        ("O", "Other"),
    )

    type = models.CharField(choices=POST_CHOICES, default="O")
    image = models.ImageField(upload_to="post/", blank=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creates"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"This Post created by {self.created_by}"


class Like(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="likes")
    like = models.ManyToManyField(User, related_name="liked_user", serialize=True)

    def __str__(self):
        return f"{self.post}"

    # @property
    # def total_like(self):
    #     return self.like.user_id.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"commented by {self.comment_by}"
