from django.db import models
from django.contrib.auth.models import User
from courts.models import SanChoi
from django.core.validators import MinValueValidator, MaxValueValidator

class DanhGiaSan(models.Model):
    khu_vuc_san = models.ForeignKey(SanChoi, on_delete=models.CASCADE)
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)
    diem_so = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Điểm số phải từ 1 đến 5'),
            MaxValueValidator(5, message='Điểm số phải từ 1 đến 5')
        ]
    )
    nhan_xet = models.TextField()
    ngay_danh_gia = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('khu_vuc_san', 'nguoi_dung')

    def __str__(self):
        return f"Đánh giá của {self.nguoi_dung.username} cho {self.khu_vuc_san.ten_khu_vuc}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure nhan_xet is not empty
        if not self.nhan_xet.strip():
            raise ValidationError('Nhận xét không được để trống')
        
        # Ensure nhan_xet has minimum length
        if len(self.nhan_xet.strip()) < 5:
            raise ValidationError('Nhận xét phải có ít nhất 5 ký tự')
