from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Like, Post

@receiver(post_save, sender=Post)
def creating_instance_of_likable_post(instance, created, **kwargs):
    if created and instance.type == "O":
        Like.objects.create(post=instance)