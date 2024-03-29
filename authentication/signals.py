from django.dispatch import receiver
from django.db.models.signals import post_save
from authentication.models import Profile, User, RecruiterProfile, Follow


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    if created and not instance.is_admin:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_recruiter_profile(instance, created, **kwargs):
    if created and instance.account_type == "recruiter":
        RecruiterProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_follower_instance(instance, created, **kwargs):
    if created:
        Follow.objects.create(user=instance)
