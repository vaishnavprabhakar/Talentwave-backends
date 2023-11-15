from django.shortcuts import render
from rest_framework.views import APIView
from authentication.models import User
from authentication.serializer import CustomUserSerializer, LogUserSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from authentication.auth.auth_tokens import get_tokens_for_user
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.


class UserRegisterApi(APIView):
    
    @extend_schema(responses=CustomUserSerializer)
    def get(self, request):
        return Response({"msg": "Register Your account."}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
                username=serializer.validated_data.get("username"),
                account_type=serializer.validated_data.get("account_type"),
            )
            get_token = get_tokens_for_user(user=user)
            return Response(
                {"data": serializer.data, "token": get_token},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLogApi(APIView):
    def get(self, request):
        return Response({"msg": "Login here to get token."})

    def post(self, request):
        serializer = LogUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                get_token = get_tokens_for_user(user=user)
            return Response(
                {"token": get_token, "msg": "login successful."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileApi(APIView):

    authentication_classes = [JWTAuthentication]
    parser_classes = [FormParser, MultiPartParser]
    
    def put(self, request):
        profile_serializer = ProfileSerializer(data=request.data, instance=request.user)
        user_serializer = CustomUserSerializer(data=request.data, instance=request.user)

        if profile_serializer.is_valid() and user_serializer.is_valid():
            profile_serializer.save()
            user_serializer.save()
            return Response({"profile data" : profile_serializer.data, "user" : user_serializer.data}, status=status.HTTP_200_OK)
        return Response({"profile error" : profile_serializer.errors, "user error" : user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    