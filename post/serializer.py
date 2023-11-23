from rest_framework import serializers
from .models import Post

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('__all__')



class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('__all__')
        