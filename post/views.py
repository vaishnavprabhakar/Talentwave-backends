from .serializer import PostCreateSerializer, PostListSerializer
from .models import Post
from authentication.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class PostCreateApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(operation_summary='Get all Post',)
    def get(self, request):
        user_posts = Post.objects.filter(user=request.user)
        serializer = PostListSerializer(data=user_posts, many=True)
        serializer.is_valid()
        return Response({"data": serializer.data}, status=200)
    
    
    # @parser_classes([MultiPartParser, FormParser])
    @swagger_auto_schema(operation_summary='Create Post', request_body=PostCreateSerializer)
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=201)


    @swagger_auto_schema(operation_summary='Update Post', request_body=PostCreateSerializer)
    def put(self, request, pk):
        id = pk
        try:
            user_post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return Response(
                {"info": "Requested Post doesn't shown"},
                status=status.HTTP_204_NO_CONTENT,
            )

        post_serializer = PostCreateSerializer(data=user_post)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response({"data": post_serializer.data}, status=status.HTTP_200_OK)
