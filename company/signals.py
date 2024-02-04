from django.dispatch import receiver
from django.db.models.signals import post_save
from authentication.models import User
from company.models import Job


@receiver(post_save, sender=User)
def user_instance_for_company(sender, instance, created, **kwargs):
    if created and instance.account_type == "recruiter":
        Job.objects.create(user=instance)
