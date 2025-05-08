from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import NguoiDung

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class NguoiDungSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer()

    class Meta:
        model = NguoiDung
        fields = '__all__'