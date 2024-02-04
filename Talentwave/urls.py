import debug_toolbar
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from authentication import views
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="Talent Wave API",
        default_version="v1",
        description="Talent Wave description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("auth/reg/", views.UserRegisterApi.as_view()),
    path("auth/log/", views.UserLogApi.as_view(), name="login"),
    path(
        "google/social-auth/",
        views.GoogleSocialAuthView.as_view(),
        name="google-signup",
    ),
    path("au/", include("authentication.urls")),
    path("", include("post.urls"), name="post"),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("accounts/", include("allauth.urls"), name="allauth"),
    path("debug/", include(debug_toolbar.urls)),
    path("company/", include("company.urls")),
    path("w/", include("chat.urls")),
]
