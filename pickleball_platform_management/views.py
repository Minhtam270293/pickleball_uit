from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import NguoiDung, San, DanhGiaSan, HuongDan, DatSan
from .serializers import NguoiDungSerializer, SanSerializer, DanhGiaSanSerializer, HuongDanSerializer, DatSanSerializer
from .tinh_toan.tinh_tien_san import tinh_tien_dat_san, tinh_doanh_thu_tat_ca_san

class NguoiDungViewSet(viewsets.ModelViewSet):
    queryset = NguoiDung.objects.all()
    serializer_class = NguoiDungSerializer

class SanViewSet(viewsets.ModelViewSet):
    queryset = San.objects.all()
    serializer_class = SanSerializer

    @action(detail=False, methods=['get'])
    def revenue(self, request):
        cac_san_cap_nhat_doanh_thu = tinh_doanh_thu_tat_ca_san()
        serializer = self.get_serializer(cac_san_cap_nhat_doanh_thu, many=True)
        return Response(serializer.data)

class DanhGiaSanViewSet(viewsets.ModelViewSet):
    queryset = DanhGiaSan.objects.all()
    serializer_class = DanhGiaSanSerializer

class HuongDanViewSet(viewsets.ModelViewSet):
    queryset = HuongDan.objects.all()
    serializer_class = HuongDanSerializer

class DatSanViewSet(viewsets.ModelViewSet):
    queryset = DatSan.objects.all()
    serializer_class = DatSanSerializer

    def perform_create(self, serializer):
        dat_san = serializer.save()
        tinh_tien_dat_san(dat_san.id)

    def perform_update(self, serializer):
        dat_san = serializer.save()
        tinh_tien_dat_san(dat_san.id)