from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import NguoiDung
from django.contrib.auth.models import User
from .serializers import NguoiDungSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

class UserListAPIView(APIView):
     def get(self, request):
        users = NguoiDung.objects.select_related('user').all()
        serializer = NguoiDungSerializer(users, many=True)
        return Response(serializer.data)
     
class UserDetailAPIView(APIView):
      def get(self, request, user_id):
        user = get_object_or_404(NguoiDung, user__id = user_id)
        serializer = NguoiDungSerializer(user)
        return Response(serializer.data)
