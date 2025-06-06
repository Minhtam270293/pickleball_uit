from rest_framework import viewsets
from .models import NguoiDung, San, DanhGiaSan, HuongDan
from .serializers import NguoiDungSerializer, SanSerializer, DanhGiaSanSerializer, HuongDanSerializer

class NguoiDungViewSet(viewsets.ModelViewSet):
    queryset = NguoiDung.objects.all()
    serializer_class = NguoiDungSerializer

class SanViewSet(viewsets.ModelViewSet):
    queryset = San.objects.all()
    serializer_class = SanSerializer

class DanhGiaSanViewSet(viewsets.ModelViewSet):
    queryset = DanhGiaSan.objects.all()
    serializer_class = DanhGiaSanSerializer

class HuongDanViewSet(viewsets.ModelViewSet):
    queryset = HuongDan.objects.all()
    serializer_class = HuongDanSerializer