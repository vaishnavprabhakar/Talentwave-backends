from django.urls import path, include

# from .routing import websocket_urlpatterns
from .views import ListUserApiView


urlpatterns = [
    path("user/all/", ListUserApiView.as_view(), name="all-users"),
]
