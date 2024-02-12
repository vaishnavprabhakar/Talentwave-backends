import jwt
from jwt.exceptions import DecodeError
from django.conf import settings
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken
from channels.db import database_sync_to_async
from rest_framework.response import Response
from authentication.models import User


class ChatMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive=None, send=None):
        authorization_header = dict(scope.get("headers", {})).get(b"authorization")
        jwt_token = str(authorization_header).split(" ")[1].strip("'")
        user_obj = await self.get_user_from_token(jwt_token)
        scope["user"] = user_obj
        return await super().__call__(scope=scope, receive=receive, send=send)

    @database_sync_to_async
    def get_user_from_token(self, jwt_token):
        try:
            payload = jwt.decode(
                jwt_token,
                settings.SECRET_KEY,
                [
                    "HS256",
                ],
            )
            user_id = payload.get("user_id")
            user = User.objects.get(id=user_id)
        except DecodeError:
            return Response(
                {"info": "Something is not working, Token cannot decode."}, status=401
            )
        return user
