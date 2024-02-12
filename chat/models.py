from django.db import models


class Room(models.Model):
    initiator = models.ForeignKey("authentication.User", on_delete=models.DO_NOTHING, related_name='sender', null=True)
    reciever = models.ForeignKey("authentication.User", on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "chat"


class Message(models.Model):
    sender = models.ForeignKey(
        "authentication.User", on_delete=models.DO_NOTHING, related_name="sent_msg"
    )
    reciever = models.ForeignKey("authentication.User", on_delete=models.DO_NOTHING)
    chat_body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    attachment = models.FileField(max_length=256)

    def __str__(self):
        return f"{self.sender}-{self.reciever}"

    class Meta:
        app_label = "chat"
