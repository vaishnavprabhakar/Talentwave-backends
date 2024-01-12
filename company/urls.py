from django.urls import path
from .views import (JobPostAPIView,
                    )


urlpatterns = [
    path('re/jobs/', JobPostAPIView.as_view(),name='post job'),
    
]