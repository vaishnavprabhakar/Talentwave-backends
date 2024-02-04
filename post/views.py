from authentication.models import User
from post.models import Like
from django.db.models import Prefetch, Count
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializer import (
    PostCreateSerializer,
    PostListSerializer,
    ListCommentSerializer,
    LikeCreateSerializer,
    CommentCreateSerializer,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import (
    throttle_classes,
    parser_classes,
    permission_classes,
)
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from .throttling import OnePostPerDay
from django.db.models import Q, F
from .permissions import IsOwnerOrReadOnly

# Create your views here.


class PostCreateApiView(APIView):
    authentication_classes = [JWTAuthentication]
    throttle_classes = [OnePostPerDay]
    serializer_classes = PostListSerializer

    @swagger_auto_schema(
        operation_summary="Get all Post",
    )
    @permission_classes([IsAuthenticated])
    def get(self, request, pk=None):
        post_id = pk
        current_user = request.user

        if post_id is not None:
            post_with_related_obj = (
                Post.objects.filter(Q(id=post_id) & Q(type="O"))
                .prefetch_related(
                    Prefetch(
                        "likes",
                        queryset=Like.objects.filter(post_id=post_id).select_related(
                            "post"
                        ),
                    ),
                    Prefetch(
                        "comments",
                        queryset=Comment.objects.filter(post_id=post_id).select_related(
                            "comment_by"
                        ),
                    ),
                )
                .annotate(
                    total_likes=Count("likes__like__liked_user"),
                    total_comments=Count("comments"),
                )
                .first()
            )
            serializer = self.serializer_classes(
                post_with_related_obj,
                context={"request": request},
            )
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            posts_with_likes = Post.objects.filter(
                Q(created_by=current_user) & Q(type="O")
            ).annotate(likes_count=Count("likes__like"))
            serializer = self.serializer_classes(posts_with_likes, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create Post", request_body=PostCreateSerializer
    )
    @parser_classes([MultiPartParser, FormParser])
    @permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = PostCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response({"data": serializer.data}, status=201)

    @swagger_auto_schema(
        operation_summary="Update Post", request_body=PostCreateSerializer
    )
    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        id = pk
        try:
            user_post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return Response(
                {"info": "Requested Post doesn't shown"},
                status=404,
            )

        post_serializer = PostCreateSerializer(
            data=request.data,
            instance=user_post,
            context={"request": request},
            partial=True,
        )
        if post_serializer.is_valid(raise_exception=True):
            post_serializer.save()
            return Response({"data": post_serializer.data}, status=status.HTTP_200_OK)
        return Response(
            {"err": post_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    @permission_classes([IsOwnerOrReadOnly, IsAuthenticated])
    def delete(self, request, pk):
        post_id = pk
        try:
            post = Post.objects.get(pk=post_id, created_by=request.user)
        except Post.DoesNotExist:
            return Response(status=404)

        post.delete()
        return Response(
            {"msg": "successfuly deleted the post."}, status=status.HTTP_200_OK
        )


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_summary="Like the post.", request_body=LikeCreateSerializer
    )
    def put(self, request, pk):
        post_id = pk
        current_user = request.user

        try:
            liked_post = Like.objects.get(post=post_id)
        except Like.DoesNotExist:
            return Response({"err": "Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)

        if current_user in liked_post.like.all():
            liked_post.like.remove(current_user)
            msg = "Unliked Post"
        else:
            liked_post.like.add(current_user)
            msg = "Liked Post"
        serializer = LikeCreateSerializer(liked_post)

        return Response(
            {
                "msg": msg,
            },
            status=status.HTTP_200_OK,
        )


class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        post_id = pk
        # current_user = request.user
        requested_post = get_object_or_404(Post, id=post_id)
        post_related_obj = Comment.objects.filter(Q(post=requested_post))
        serializer = ListCommentSerializer(post_related_obj, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post_id = pk
        try:
            requested_post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"info": "Post doesn't exist"}, status=status.HTTP_204_NO_CONTENT
            )
        serializer = CommentCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(kwargs=requested_post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id, cmt_id):
        post_id = post_id
        cmt_id = cmt_id
        current_user = request.user
        post_comments = Comment.objects.filter(
            Q(post=get_object_or_404(Post, id=post_id))
            & Q(comment_by=current_user)
            & Q(id=cmt_id)
        ).first()
        if post_comments:
            post_comments.delete()
            return Response({"info": "Comment deleted"}, status=status.HTTP_200_OK)
        return Response(
            {
                "err": "something went wrong.",
            },
            status=404,
        )
