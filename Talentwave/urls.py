from django.contrib import admin
from django.urls import path, include
from authentication import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/reg/", views.UserRegisterApi.as_view()),
    path("auth/log/", views.UserLogApi.as_view()),
    path("", include("authentication.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("", include("post.urls"), name="post"),
]
