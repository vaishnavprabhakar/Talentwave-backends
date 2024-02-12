from django.dispatch import receiver
from django.db.models.signals import post_save
from chat.models import Room, Message

@receiver(post_save, sender=Room)
def create_message_with_room(instance, created, **kwargs):
    if created:
        Message.objects.create(room=instance)

