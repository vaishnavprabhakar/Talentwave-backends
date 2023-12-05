from django.urls import path
from .views import PostCreateApiView

urlpatterns = [
    path("post/", PostCreateApiView.as_view(), name="post"),
    path("post/<int:pk>/", PostCreateApiView.as_view(), name="post"),
]
