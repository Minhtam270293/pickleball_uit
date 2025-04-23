from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class SanChoi(models.Model):
    ten_khu_vuc = models.CharField(max_length=100)
    dia_diem = models.CharField(max_length=255)
    gio_mo_cua = models.TimeField()
    gio_dong_cua = models.TimeField()
    gia_thue_theo_gio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0, message='Giá thuê phải lớn hơn 0')]
    )
    mo_ta = models.TextField()
    so_san_con = models.IntegerField(
        validators=[
            MinValueValidator(0, message='Số sân phải lớn hơn 0'),
        ]
    )

    def __str__(self):
        return f"{self.ten_khu_vuc} - {self.dia_diem}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure closing time is after opening time
        if self.gio_dong_cua <= self.gio_mo_cua:
            raise ValidationError('Giờ đóng cửa phải sau giờ mở cửa')
        
        # Ensure ten_khu_vuc is not empty
        if not self.ten_khu_vuc.strip():
            raise ValidationError('Tên khu vực không được để trống')
        
        # Ensure dia_diem is not empty
        if not self.dia_diem.strip():
            raise ValidationError('Địa điểm không được để trống')
