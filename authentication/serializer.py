import re
from enum import auto, Enum
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.fields import empty
from authentication.models import Profile, User, Follow, RecruiterProfile
from rest_framework.validators import ValidationError
from post.serializer import PostListSerializer
from cloudinary import uploader


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"

    def update(self, instance, **kwargs):
        return instance


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """

    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True
    )


class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "confirm_password",
            "account_type",
        )
        extra_kwargs = {
            "confirm_password": {
                "write_only": True
            },  # to hide the password field in GET requests
        }

    def validate(self, data):
        value = data
        pattern = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        password = value.get("password")
        confirm_password = value.get("confirm_password")
        if not pattern or not re.search(r"\d", password):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter atleast one special charector and one digit."
            )

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        if password != confirm_password:
            raise serializers.ValidationError("Passwords doesn't match...")
        return data

    def get_username(self, obj):
        email = obj.get("email", "")
        get_username = email.split("@")[0]
        username = self.create(obj, get_username)
        return username

    def create(self, validated_data, username):
        validated_data["username"] = username
        return validated_data


class LogUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "profile_image",
            "bio",
            "title",
            "dob",
            "city",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "profile_image": {"required": False},
            "bio": {"required": True},
            "title": {"required": True},
            "dob": {"required": True},
            "phone": {"required": True},
            "city": {"required": True},
        }

    def create(self, validated_data):
        return super().create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        # instance.profile_image = validated_data.get(
        #     "profile_image", instance.profile_image
        # )
        # instance.profile_image = validated_data.get('profile_image')
        # uploader.upload(instance.profile_image,folder='Talentwave')
        instance.bio = validated_data.get("bio", instance.bio)
        instance.title = validated_data.get("title", instance.title)
        instance.city = validated_data.get("city", instance.city)
        validated_user = validated_data.get("user", {})
        if validated_user:
            user_data = instance.user
            user_data.username = validated_user.get("username", user_data.username)
            user_data.email = validated_user.get("email", user_data.email)
            user_data.save()
        instance.save()
        return instance


class ListRecruiterProfile(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = [
            "user",
            "company_name",
            "position",
            "proffessional_card",
            "created_at",
        ]
        read_only_fields = ["user"]


class RecruiterProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model: RecruiterProfile
        fields = [
            "user",
            "company_name",
            "position",
        ]
        read_only_fields = ["user"]

    def create(self, validate_data):
        return super().create(validated_data=validate_data)

    def update(self, instance, **kwargs):
        return


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ("email", "username", "account_type", "profile",)