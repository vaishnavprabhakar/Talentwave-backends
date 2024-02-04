import json
from django.conf import settings
from channels.generic.websocket import (
            AsyncWebsocketConsumer,
            )
# from channels import auth
from authentication.models import User
from django.contrib.auth.models import AnonymousUser
from djangochannelsrestframework.decorators import transaction
from channels.consumer import get_channel_layer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer




class ChatConsumer(AsyncWebsocketConsumer):    

    async def connect(self):

        if self.scope['user'] is not None:
            
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f"chat-{self.room_name}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

        else:
            await self.close(code=1006)

        await self.send(text_data=json.dumps({
            'type': 'connection established',
            'message': 'Hi, this is a websocket connection.'
        }))


    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.load(text_data)
        message = text_data_json['message']
        return message
                




    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close(code=1006)