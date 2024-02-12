from rest_framework import serializers
from .models import Room, Message
from authentication.models import User


class ListRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ["id"]


class ListMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
