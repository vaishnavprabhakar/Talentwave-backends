from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import (
    JobPostSerializer,
)
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class JobPostAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response()

    @swagger_auto_schema(request_body=JobPostSerializer)
    def post(self, request, format=None):
        current_user = request.user
        serializer = JobPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
