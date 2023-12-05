from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from authentication.models import Profile, User
from rest_framework.validators import ValidationError
from post.serializer import PostListSerializer


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
        password = value.get("password")
        confirm_password = value.get("confirm_password")
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
            "phone",
            "city",
        )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.profile_image = validated_data.get(
            "profile_image", instance.profile_image
        )
        instance.bio = validated_data.get("bio", instance.bio)
        instance.title = validated_data.get("title", instance.title)
        instance.dob = validated_data.get("dob", instance.dob)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.city = validated_data.get("city", instance.city)
        validated_user = validated_data.get("user", {})
        if validated_user:
            user_data = instance.user
            user_data.username = validated_user.get("username", user_data.username)
            user_data.email = validated_user.get("email", user_data.email)
            user_data.save()
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    profile = ProfileSerializer()
    posts = PostListSerializer()

    class Meta:
        model = User
        fields = ("username", "profile", "posts")

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        return instance
