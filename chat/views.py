from .serializer import ListRoomSerializer, ListMessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User, Follow
from django.db.models import Prefetch
from authentication.serializer import UserSerializer, FollowSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from authentication.models import Profile
from django.db.models import Q


class ListUserApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_followed = (
            User.objects.filter(Q(id=request.user.id))
            .prefetch_related(
                Prefetch("profile", queryset=Follow.objects.filter(user=request.user))
            )
            .first()
        )
        serializer = UserSerializer(user_followed)
        return Response(serializer.data, status=200)
