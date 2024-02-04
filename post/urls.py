from django.urls import path
from .views import PostCreateApiView, PostLikeView, CommentAPIView

urlpatterns = [
    path("post/", PostCreateApiView.as_view(), name="post"),
    path("post/<int:pk>/", PostCreateApiView.as_view(), name="post"),
    path("post/<int:pk>/like/", PostLikeView.as_view(), name="like"),
    path("post/<int:pk>/comment/", CommentAPIView.as_view(), name="comment"),
    path(
        "post/<int:post_id>/comment/<int:cmt_id>/",
        CommentAPIView.as_view(),
        name="comment delete",
    ),
]
