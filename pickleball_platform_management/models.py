from django.db import models
from rest_framework import serializers

from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class NguoiDung(models.Model):
    ho_ten = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(
        max_length=15,
        blank=True, null=True,
        validators=[
            RegexValidator(
                regex=r'^0\d{9,10}$',
                message='Số điện thoại phải bắt đầu bằng 0 và có 10-11 chữ số'
            )
        ]
    )
    ngay_sinh = models.DateField(blank=True, null=True)
    gioi_tinh = models.CharField(
        max_length=10,
        choices=[('nam', 'Nam'), ('nu', 'Nữ'), ('khac', 'Khác')],
        blank=True, null=True
    )
    vai_tro = models.CharField(
        max_length=20,
        default='nguoi_dung'
    )
    ngay_dang_ky = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ho_ten

class San(models.Model):
    ten_san = models.CharField(max_length=100)
    dia_diem = models.CharField(max_length=255)
    gia_thue_theo_gio = models.DecimalField(max_digits=10, decimal_places=2)
    mo_ta = models.TextField(blank=True, null=True)
    so_san_con = models.PositiveIntegerField()
    gio_mo_cua = models.TimeField()
    gio_dong_cua = models.TimeField()

    def clean(self):
        if self.gio_mo_cua >= self.gio_dong_cua:
            raise ValidationError("Giờ mở cửa phải trước giờ đóng cửa.")

    def __str__(self):
        return self.ten_san

class DanhGiaSan(models.Model):
    diem = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    noi_dung = models.TextField()
    ngay_danh_gia = models.DateTimeField(auto_now_add=True)
    san_id = models.ForeignKey('San', on_delete=models.CASCADE, related_name='danh_gias')
    nguoi_dung_id = models.ForeignKey('NguoiDung', on_delete=models.CASCADE, related_name='danh_gias')

    def __str__(self):
        return f"{self.san.ten_san} - {self.nguoi_dung.ho_ten} ({self.diem}★)"
    
class HuongDan(models.Model):
    tieu_de = models.CharField(max_length=200)
    thoi_gian_tao = models.DateTimeField(auto_now_add=True)
    noi_dung = models.TextField()
    nguoi_tao = models.ForeignKey('NguoiDung', on_delete=models.CASCADE, related_name='huong_dans')
    cap_do = models.CharField(
        max_length=20,
        choices=[('de', 'Dễ'), ('trung binh', 'Trung bình'), ('kho', 'Khó')],
        blank=True,
        null=True
    )

    def __str__(self):
        return self.tieu_de