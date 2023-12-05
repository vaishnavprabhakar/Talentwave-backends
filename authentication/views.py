import random
from authentication.auth.auth_tokens import get_tokens_for_user

from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from authentication.models import User, Profile
from authentication.serializer import (
    CustomUserSerializer,
    LogUserSerializer,
    ProfileSerializer,
    UserSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.


class UserRegisterApi(APIView):

    @swagger_auto_schema(operation_summary='Register user', operation_description="This will create user and send otp for users email id with smtp.", request_body=CustomUserSerializer)
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        otp = random.randint(100000, 999999)
        request.session["saved_otp"] = otp
        if serializer.is_valid():
            get_username = serializer.data.get("username")
            request.session["user_username"] = get_username
            msg = EmailMessage(
                subject="Verify your Talentwave account",
                body="Your Otp for verification is : "+ str(otp),
                from_email=settings.EMAIL_HOST_USER,
                to=[get_username.get("email")],
                reply_to=[settings.EMAIL_REPLY],
            )
            msg.send()
            return Response(
                {"otp": otp},
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# Verification of One Time Password and saving user data.
class VerifyOtp(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.FORMAT_EMAIL),
                'entered_otp': openapi.Schema(type=openapi.FORMAT_BASE64),
            },
            required=['phone_number', 'otp_code'],
        ),
        responses={200: 'OK', 400: 'Bad Request'}
    )
    
    def post(self, request):
        get_data = request.session.get("user_username")
        generated_otp = request.session.get("saved_otp")
        entered_otp = request.data.get("entered_otp")
        try:
            user = User.objects.get(email=get_data["email"])
        except User.DoesNotExist:
            if int(generated_otp) == int(entered_otp):
                user = User.objects.create_user(
                    email=get_data["email"],
                    username=get_data["username"],
                    password=get_data["password"],
                    account_type=get_data["account_type"],
                )

                tokens = get_tokens_for_user(user=user)
                return Response(
                    {"msg": "successful", "token": tokens},
                    status=status.HTTP_201_CREATED,
                )

        return Response(
            {"error": "Otp doesn't match"}, status=status.HTTP_429_TOO_MANY_REQUESTS
        )


class UserLogApi(APIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    @swagger_auto_schema(operation_summary='Login Api', request_body=LogUserSerializer)
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
            return Response(
                {"info": "Invalid login credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @swagger_auto_schema(operation_summary='Profile create')
    def get(self, request):
        request_user = request.user
        print(request_user.profile)
        
        try:
            request_user.profile
        
        except Profile.DoesNotExist:
            return Response(
                {"info": "No profile match found."}, status=status.HTTP_204_NO_CONTENT
            )
        
        user_serializer = UserSerializer(data=request_user)
        data = {"user_data": user_serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)


    @swagger_auto_schema(operation_summary="Profile Update", request_body=ProfileSerializer)
    def put(self, request):
        request_user = request.user.profile
        profile_serializer = ProfileSerializer(
            request_user, data=request.data, partial=True
        )

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(
                {
                    "profile data": profile_serializer.data,
                },
                status=status.HTTP_206_PARTIAL_CONTENT,
            )
        return Response(
            {
                "profile error": profile_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )