from rest_framework import serializers
from rest_framework.fields import empty
from authentication.models import Profile, User


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
            "password": {
                "write_only": True
            },  # to hide the password field in GET requests
        }
    
   

    def get_username(self, obj):
        email = obj.get('email', '')  
        username = email.split('@')[0] 
        result = self.create(obj,username)
        return result
    

    def create(self, validated_data,username):
        validated_data['username']=username
        return validated_data
    
    

class LogUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    # def validate(self, data):
    #     email = data.get("email")
    #     user= User.objects.filter(email=email).exists()
        
    #     if user is not True:
    #         serializers.ValidationError("Entered email already in use.")
    #     return data


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ("username", "email")
    

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        return instance



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

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
            "user",
        )

    def update(self, instance, validated_data):
        
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.profile_image = validated_data.get(
            "profile_image", instance.profile_image
        )
        instance.bio = validated_data.get("bio", instance.bio)
        instance.title = validated_data.get("dob", instance.dob)
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
