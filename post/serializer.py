from rest_framework import serializers
from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("type", "image", "description", "title")

    def create(self, validated_data):
        user = self.instance
        print(validated_data, self.instance)
        type = validated_data.get("type")
        image = validated_data.get("image")
        title = validated_data.get("title")
        description = validated_data.get("description")

        post = Post.objects.create(
            user=user, type=type, image=image, title=title, description=description
        )
        return post

    def update(self, instance, validated_data):
        self.type = validated_data.get("type", instance.type)
        self.image = validated_data.get("image", instance.image)
        self.title = validated_data.get("title", instance.title)
        self.description = validated_data.get("description", instance.description)
        return instance

    def validate(self, attrs):
        type = attrs.get("type")
        title = attrs.get("title")
        description = attrs.get("description")
        image = attrs.get("image")

        if type == "O" and not image:
            raise serializers.DjangoValidationError(
                {"image"["An image is required for option 'Other'"]}
            )
        elif type == "O" and not title:
            raise serializers.DjangoValidationError(
                {"title": ["Title is required for option 'Other'"]}
            )
        elif type == "0" and not description:
            raise serializers.DjangoValidationError(
                {"description": ["Description is required for option 'Other'."]}
            )
        return attrs


class PostListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = "__all__"
