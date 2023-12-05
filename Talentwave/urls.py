from django.contrib import admin
from django.urls import path, include
from authentication import views
from .apidocs.urls import urlpatterns as swagger_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/reg/", views.UserRegisterApi.as_view()),
    path("auth/log/", views.UserLogApi.as_view(), name='login'),
    path("", include("authentication.urls")),
    path("", include("post.urls"), name="post"),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('accounts/', include('allauth.urls')),
        
]

urlpatterns += swagger_urls
