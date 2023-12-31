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
    title = models.CharField(max_length=256, null=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"This Post created by {self.created_by}"
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    like = models.ManyToManyField(User, related_name="likes", )


    def __str__(self):
        return f"{self.post}"
