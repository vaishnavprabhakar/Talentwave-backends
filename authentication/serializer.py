from rest_framework import serializers
from authentication.models import Profile, User


class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

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
            "password": {
                "write_only": True
            },  # to hide the password field in GET requests
        }


class LogUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        return data


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
