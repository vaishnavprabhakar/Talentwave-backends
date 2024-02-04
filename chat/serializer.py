from rest_framework import serializers
from .models import Room, Message
from authentication.models import User


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ["id"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
