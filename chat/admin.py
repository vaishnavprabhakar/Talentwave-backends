from django.contrib import admin
from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "room",
        "sender",
        "reciever",
        "chat_body",
        "timestamp",
        "attachment",
    ]
    list_display_links = ["room", "sender", "reciever"]
    list_select_related = True
