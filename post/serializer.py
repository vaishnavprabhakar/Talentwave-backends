
from django.db.models import Count
from rest_framework import serializers
from .models import Post, Like, Comment
from Talentwave.cloud.storage import upload_to_cloud,update_image_resource
from cloudinary import uploader

class CommentCreateSerializer(serializers.Serializer):

    comment = serializers.CharField()

    def save(self,**kwargs):
        user = self.context.get('request').user
        post = kwargs.get('kwargs')
        comment = self.validated_data.get('comment')
        cmt_obj = Comment.objects.create(
        post=post,
        body=comment,
        comment_by=user
        )
        return cmt_obj


    def validate(self, attrs):
        comment = attrs.get("comment")
        if comment is None:
            raise serializers.ValidationError(
                {"Comment Body required."},
            )
        return attrs


class ListCommentSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source="comment_by.username")
    comment_body = serializers.ReadOnlyField(source="body")


    class Meta:
        model = Comment
        fields = "__all__"#["id", "post","comment_body", "username"]


class LikeCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = ["like", "post"]
        read_only_fields = ["like", "post"]


class ListLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["like",]
        read_only_fields = ["like",]

    # def to_representation(self, instance):
    #     return instance


class PostListSerializer(serializers.ModelSerializer):
    comments = ListCommentSerializer(many=True)
    likes = ListLikeSerializer()
    total_like = serializers.SerializerMethodField(method_name="get_total_likes")
    total_comments = serializers.SerializerMethodField(method_name="get_total_comments")

    class Meta:
        model = Post
        fields = [
            "id",
            "type",
            "image",
            "title",
            "description",
            "created_by",
            "created_at",
            "updated_at",
            "comments",
            "likes",
            "total_like",
            "total_comments",
        ]

    def get_total_likes(self, obj):
        instant_obj = obj
        return instant_obj.likes.like.count()

    def get_total_comments(self, obj):
        instant_obj = obj
        return instant_obj.comments.count()


class PostCreateSerializer(serializers.Serializer):
    POST_CHOICES = Post.POST_CHOICES

    type = serializers.ChoiceField(choices=POST_CHOICES, write_only=True)
    image = serializers.ImageField()
    title = serializers.CharField()
    description = serializers.CharField()

    def __init__(self, *args, **kwargs):
        if kwargs["context"]["request"].user.account_type == "jobseeker":
            fields = self.get_fields()
        elif kwargs["context"]["request"].user.account_type == "recruiter":
            self.fields.get("type").required = True
            self.fields.get("title").required = True
            self.fields.get("description").required = True
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        image = validated_data.get('image')
        post_obj = Post.objects.create(**validated_data)
        if image is not None:
            upload_to_cloud(obj=post_obj.image, folder='Talentwave/', overwrite=False)
        return post_obj
    

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        update_image_resource(folder='Talentwave/', overwrite=True,public_id=instance.image)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        return instance

    def validate(self, attrs):
        data = attrs
        image = data.get("image")
        max_size = 2 * 1024 * 1024  # 2 MB
        type = attrs.get("type")
        title = attrs.get("title")
        description = attrs.get("description")
        image = attrs.get("image")
        if image:
            if image.size > max_size:
                raise serializers.ValidationError(
                    f"Image size exceeds the allowed limit is {max_size/1024} MB."
                )
        if type == "O" and not image:
            raise serializers.ValidationError(
                {"image": ["An image is required for option 'Other'"]}, code=400
            )
        elif type == "O" and not title:
            raise serializers.ValidationError(
                {"title": ["Title is required for option 'Other'"]}, code=400
            )
        elif type == "0" and not description:
            raise serializers.ValidationError(
                {"description": ["Description is required for option 'Other'."]},
            )
        return data
