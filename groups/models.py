from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NhomChoi(models.Model):
    ten_nhom = models.CharField(max_length=100)
    nguoi_tao = models.ForeignKey(User, on_delete=models.CASCADE)
    mo_ta = models.TextField()
    thoi_gian_hoat_dong = models.CharField(max_length=100)
    dia_diem_hoat_dong = models.CharField(max_length=255)

    def __str__(self):
        return self.ten_nhom

class ThanhVienNhom(models.Model):
    nhom = models.ForeignKey(NhomChoi, on_delete=models.CASCADE)
    thanh_vien = models.ForeignKey(User, on_delete=models.CASCADE)
    ngay_tham_gia = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('nhom', 'thanh_vien')

    def __str__(self):
        return f"{self.thanh_vien.username} in {self.nhom.ten_nhom}"
