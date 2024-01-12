import random
from requests.exceptions import HTTPError
from threading import Thread
from authentication.auth.auth_tokens import get_tokens_for_user
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from authentication.models import RecruiterProfile, User, Follow,Profile
from authentication.serializer import (
    CustomUserSerializer,
    LogUserSerializer,
    ProfileSerializer,
    UserSerializer,
    SocialSerializer,
    FollowSerializer,
    RecruiterProfileCreateSerializer,
    ListRecruiterProfile
)
from authentication.permissions import RecruitersOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics
from social_django.utils import load_strategy
from social_core.exceptions import MissingBackend, AuthTokenError  # AuthForbidden
from social_core.backends.google import GoogleOAuth2
from authentication.permissions import RecruitersOnly
from django.db.models import Prefetch
from django.db.models import Q,Count,F
# Create your views here.


class RecruiterProfileApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, RecruitersOnly]

    @swagger_auto_schema(operation_summary='Listing the Recruiter Profie', operation_description='This will list the current recruiter profile', request_body=ListRecruiterProfile)
    def get(self, request):
        current_user = request.user
        user_profile = RecruiterProfile.objects.get(user=current_user)
        serializer = ListRecruiterProfile(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    @swagger_auto_schema(
        operation_summary="Register user",
        operation_description="This will create user and send otp for users email id with smtp.",
        request_body=RecruiterProfileCreateSerializer,
    )
    def post(self, request):
        current_user = User.objects.get(email=request.user)
        if isinstance(current_user,RecruiterProfile):
            serializer = RecruiterProfileCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(kwargs=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"msg": "Account not found"},
            status=status.HTTP_412_PRECONDITION_FAILED,
        )


class FollowAPI(APIView):
    
    @swagger_auto_schema(
        operation_summary="Register user",
        operation_description="This will create user and send otp for users email id with smtp.",
        request_body=FollowSerializer,
    )
    def put(self, request, pk):
        user_id = pk
        current_user = request.user
        follow_obj = Follow.objects.get(id=user_id)

        if follow_obj:
            follow_obj.following.add(current_user)
            message = "Followed"
        else:
            follow_obj.following.remove(current_user)
            message = "Unfollowed"
        serializer = FollowSerializer(data=request.data)
        return Response(
            {"msg": message, "data": serializer.data},
            status=status.HTTP_206_PARTIAL_CONTENT,
        )


class GoogleSocialAuthView(generics.CreateAPIView):
    serializer_class = SocialSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token = serializer.validated_data["access_token"]
        strategy = load_strategy(request)

        try:
            backend = load_strategy(
                strategy=strategy, name="google-oauth2", redirect_uri=None
            )
        except MissingBackend:
            return Response(
                {
                    "error": "Google social authentication is not available at the moment."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if isinstance(backend, GoogleOAuth2):
                user = backend.do_auth(access_token)
        except AuthTokenError as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            return Response(
                {"detail": "Google social authentication successful."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Google social authentication failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserRegisterApi(APIView):
    @swagger_auto_schema(
        operation_summary="Register user",
        operation_description="This will create user and send otp for users email id with smtp.",
        request_body=CustomUserSerializer,
    )
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        otp = random.randint(100000, 999999)
        request.session["saved_otp"] = otp
        if serializer.is_valid():
            get_username = serializer.data.get("username")
            request.session["user_username"] = get_username
            msg = EmailMessage(
                subject="Verify your Talentwave account",
                body="Your Otp for verification is : " + str(otp),
                from_email=settings.EMAIL_HOST_USER,
                to=[get_username.get("email")],
                reply_to=[settings.EMAIL_REPLY],
            )
            t = Thread(target=msg.send)
            t.start()
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
                "email": openapi.Schema(type=openapi.FORMAT_EMAIL),
                "entered_otp": openapi.Schema(type=openapi.FORMAT_BASE64),
            },
            required=["phone_number", "otp_code"],
        ),
        responses={200: "OK", 400: "Bad Request"},
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

    @swagger_auto_schema(operation_summary="Login Api", request_body=LogUserSerializer)
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
   

    @swagger_auto_schema(operation_summary="Profile create",request_body=ProfileSerializer)
    def get(self, request):
        current_user = request.user
        profile_related_obj = Profile.objects.select_related('user').filter(user=current_user).first()
        user_serializer = ProfileSerializer(
            instance=profile_related_obj, context={"request": request}
        )
        return Response({"user_data": user_serializer.data}, status=status.HTTP_200_OK)



    @swagger_auto_schema(
        operation_summary="Profile Update", request_body=UserSerializer
    )
    def put(self, request):
        current_user = request.user
        profile_serializer = ProfileSerializer(
            data=request.data, instance=current_user.profile, context={"request": request},
        )

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(
                {"msg": "profile Updated", "profile data": profile_serializer.data},
                status=200,
            )
        return Response(
            {"errors": profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
