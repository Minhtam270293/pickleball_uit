from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class NguoiDung(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ho_ten = models.CharField(max_length=100)
    # Vietnamese phone number validation (10-11 digits, starting with 0)
    so_dien_thoai = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^0\d{9,10}$',
                message='Số điện thoại phải bắt đầu bằng 0 và có 10-11 chữ số'
            )
        ]
    )
    dia_chi = models.CharField(max_length=255)
    
    loai_nguoi_dung = models.CharField(max_length=10, choices=[
        ('admin', 'Quản trị viên'),
        ('user', 'Người dùng')
    ])

    def __str__(self):
        return f"{self.ho_ten} ({self.user.username})"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure ho_ten is not empty
        if not self.ho_ten or not self.ho_ten.strip():
            raise ValidationError('Họ tên không được để trống')
