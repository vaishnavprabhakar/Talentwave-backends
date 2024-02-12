import json
import hashlib
from rest_framework.response import Response
from channels.generic.websocket import (
    AsyncWebsocketConsumer,
)
from authentication.models import User
from asgiref.sync import sync_to_async
from chat.models import Room, Message
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        self.current_user_id = (
            str(self.scope["user"].id) if self.scope["user"].id else None
        )
        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_name = (
            f"{str(self.current_user_id)}-{str(self.other_user_id)}"
            if self.current_user_id > self.other_user_id
            else f"{self.other_user_id}-{self.current_user_id}"
        )
        self.room_group_name = f"chat-{self.room_name}"
        await self.save_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        self.send(
            {
                "type": "websocket.accept",
                "sender": self.current_user_id,
                "reciever": self.other_user_id,
            }
        )

    async def websocket_receive(self, event):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "sent_by": self.scope["user"].username
                if self.scope["user"].username
                else self.scope["user"].id,
                "message": event["text"] if event["text"] else None,
            },
        )

    @database_sync_to_async
    def save_room(self):
        try:
            other_user = User.objects.get(id=self.other_user_id)
        except User.DoesNotExist:
            return Response(status=400)
        self.room, created = Room.objects.get_or_create(
            name=self.room_group_name, initiator=self.scope["user"], reciever=other_user
        )

    @sync_to_async
    def generate_unique_key(self, *args):
        id1, id2 = str(args[0]), str(args[1])
        hashed_ids = hashlib.sha256(string=f"{id1}-{id2}".encode("utf-8")).hexdigest()
        return hashed_ids

    async def chat_message(self, event):
        message = event["message"]
        await self.save_message(message)
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def save_message(self, msg):
        scope_user = User.objects.get(id=self.current_user_id)
        other_user = User.objects.get(id=self.other_user_id)
        msg_instance = Message.objects.create(
            sender=scope_user,
            reciever=other_user,
            chat_body=msg,
            room=self.room,
            attachment=None,
        )
        return msg_instance

    async def websocket_disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close()
